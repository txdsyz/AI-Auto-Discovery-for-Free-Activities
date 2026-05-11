# Connecting Lovable Frontend to Backend

**After you download the frontend from Lovable, follow these steps to connect it to your backend.**

---

## Step 1: Download and Setup

1. **Download from Lovable:**
   - Export your project from Lovable
   - Extract to `/Users/rishitreddy/Projects/afterclass/frontend`

2. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Create environment file:**
   ```bash
   # Create .env.local
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

---

## Step 2: Add API Client

Create a new file: `frontend/lib/api.ts`

Copy the entire content from `/Users/rishitreddy/Projects/afterclass/frontend-api-client.ts` into this file.

Or run:
```bash
cp ../frontend-api-client.ts lib/api.ts
```

---

## Step 3: Replace Mock Data with Real API Calls

### A. Update Organizations List Component

Find the component that displays the organizations list (probably `components/organizations-list.tsx` or similar).

**Replace mock data with API call:**

```typescript
// BEFORE (Lovable mock data)
const [organizations, setOrganizations] = useState(mockOrganizations);

// AFTER (Real API)
import { api, Organization } from '@/lib/api';

const [organizations, setOrganizations] = useState<Organization[]>([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);

useEffect(() => {
  async function loadOrganizations() {
    try {
      setLoading(true);
      const data = await api.getOrganizations({ limit: 50 });
      setOrganizations(data.organizations);
      setError(null);
    } catch (err) {
      console.error('Failed to load organizations:', err);
      setError('Failed to load organizations');
    } finally {
      setLoading(false);
    }
  }
  
  loadOrganizations();
}, []);

// Add loading state
if (loading) {
  return <div className="flex items-center justify-center p-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
  </div>;
}

// Add error state
if (error) {
  return <div className="p-4 text-red-600">{error}</div>;
}
```

---

### B. Update Organization Details Component

Find the component that shows organization details (probably `components/organization-details.tsx`).

**Add API call when organization is selected:**

```typescript
import { api, Organization } from '@/lib/api';

const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null);
const [loading, setLoading] = useState(false);

// When user selects an organization
async function handleSelectOrganization(orgId: string) {
  try {
    setLoading(true);
    const org = await api.getOrganization(orgId);
    setSelectedOrg(org);
  } catch (err) {
    console.error('Failed to load organization:', err);
  } finally {
    setLoading(false);
  }
}
```

---

### C. Update Discover Sidebar Component

Find the discover sidebar component (probably `components/discover-sidebar.tsx`).

**Connect the "Run Discovery" button:**

```typescript
import { api } from '@/lib/api';

const [isDiscovering, setIsDiscovering] = useState(false);
const [discoveryStatus, setDiscoveryStatus] = useState<string>('');
const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
const [maxOrgs, setMaxOrgs] = useState(5);

async function handleRunDiscovery() {
  if (selectedCategories.length === 0) {
    alert('Please select at least one category');
    return;
  }
  
  try {
    setIsDiscovering(true);
    setDiscoveryStatus('Running discovery... This may take 2-3 minutes');
    
    const result = await api.runDiscovery(
      selectedCategories as any,
      maxOrgs
    );
    
    setDiscoveryStatus(
      `✅ Discovery complete! Found ${result.organizations_found} organizations, ` +
      `saved ${result.organizations_saved}, filtered ${result.irrelevant_filtered}`
    );
    
    // Refresh the organizations list
    window.location.reload(); // Simple approach
    // OR: Call a refresh function to reload without full page refresh
    
  } catch (err) {
    console.error('Discovery failed:', err);
    setDiscoveryStatus('❌ Discovery failed. Please try again.');
  } finally {
    setIsDiscovering(false);
  }
}
```

**Update the button:**

```typescript
<Button
  onClick={handleRunDiscovery}
  disabled={isDiscovering}
  className="w-full"
>
  {isDiscovering ? 'Running...' : 'Run Discovery'}
</Button>

{discoveryStatus && (
  <div className="mt-4 p-3 bg-blue-50 rounded-lg text-sm">
    {discoveryStatus}
  </div>
)}
```

---

### D. Add Category Filter (Optional Enhancement)

In your organizations list component, add category filtering:

```typescript
const [selectedCategory, setSelectedCategory] = useState<string | undefined>();

async function loadOrganizations(category?: string) {
  try {
    setLoading(true);
    const data = await api.getOrganizations({ category: category as any, limit: 50 });
    setOrganizations(data.organizations);
  } catch (err) {
    console.error('Failed to load organizations:', err);
  } finally {
    setLoading(false);
  }
}

// Add filter buttons in your UI
<div className="flex gap-2 mb-4">
  <Button onClick={() => loadOrganizations()}>All</Button>
  <Button onClick={() => loadOrganizations('sports')}>Sports</Button>
  <Button onClick={() => loadOrganizations('youth_centers')}>Youth Centers</Button>
  <Button onClick={() => loadOrganizations('scouts')}>Scouts</Button>
  <Button onClick={() => loadOrganizations('cultural')}>Cultural</Button>
</div>
```

---

## Step 4: Test the Integration

### Terminal 1: Start Backend
```bash
cd /Users/rishitreddy/Projects/afterclass/backend
python main.py
```

### Terminal 2: Start Frontend
```bash
cd /Users/rishitreddy/Projects/afterclass/frontend
npm run dev
```

### Test Checklist:
1. ✅ Visit http://localhost:3000
2. ✅ Organizations list loads from backend
3. ✅ Click an organization → Details load
4. ✅ Click contact info → Links work
5. ✅ Open Discover sidebar
6. ✅ Select categories and run discovery
7. ✅ Wait 2-3 minutes → New orgs appear

---

## Step 5: Handle Empty State

If no organizations exist in database, show a helpful message:

```typescript
if (!loading && organizations.length === 0) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      <div className="text-6xl mb-4">📭</div>
      <h3 className="text-xl font-semibold mb-2">No organizations yet</h3>
      <p className="text-gray-600 mb-4">
        Click the "Discover" button in the navigation bar to find organizations
      </p>
    </div>
  );
}
```

---

## Step 6: Error Handling

Add proper error handling for API calls:

```typescript
// Add to api.ts or create a separate error handler
function handleAPIError(error: any) {
  if (error.message.includes('Failed to fetch')) {
    return 'Cannot connect to backend. Make sure the server is running on port 8000.';
  }
  return error.message || 'An unexpected error occurred';
}

// Use in components
catch (err) {
  const errorMessage = handleAPIError(err);
  setError(errorMessage);
  console.error('API Error:', err);
}
```

---

## Step 7: Add Loading States

Enhance user experience with loading indicators:

```typescript
// Skeleton loader for organization cards
function OrganizationCardSkeleton() {
  return (
    <div className="animate-pulse border rounded-lg p-4 mb-3">
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
      <div className="h-3 bg-gray-200 rounded w-1/2"></div>
    </div>
  );
}

// Use in list
{loading ? (
  <>
    <OrganizationCardSkeleton />
    <OrganizationCardSkeleton />
    <OrganizationCardSkeleton />
  </>
) : (
  organizations.map(org => <OrganizationCard key={org.id} org={org} />)
)}
```

---

## Step 8: Production Deployment

When ready to deploy:

### Backend (e.g., Railway, Render, or Vercel)
1. Deploy backend to a hosting service
2. Get production URL: `https://your-backend.com`
3. Update CORS in `backend/main.py`:
   ```python
   allow_origins=["https://your-frontend.com"]
   ```

### Frontend (Vercel, Netlify)
1. Add environment variable in hosting dashboard:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.com
   ```
2. Deploy frontend
3. Test production build

---

## Common Issues & Fixes

### Issue: CORS Error
**Error:** "Access to fetch blocked by CORS policy"

**Fix:** Make sure backend CORS is configured correctly in `main.py`:
```python
allow_origins=["http://localhost:3000", "https://your-frontend.com"]
```

---

### Issue: Organizations Not Loading
**Error:** Empty list or API error

**Fixes:**
1. Check backend is running: `curl http://localhost:8000/health`
2. Check database has data: `python test_full_pipeline.py 1`
3. Check browser console for errors
4. Verify `.env.local` has correct API URL

---

### Issue: Discovery Takes Too Long
**Not an issue** - Discovery takes 2-3 minutes by design

**Improvements:**
1. Show progress indicator
2. Add time estimate: "This will take 2-3 minutes"
3. Allow user to close sidebar while it runs (optional)

---

## Quick Integration Checklist

After downloading from Lovable:

- [ ] Install dependencies (`npm install`)
- [ ] Create `.env.local` with API_URL
- [ ] Copy `api.ts` client to `lib/api.ts`
- [ ] Replace mock data with API calls in organizations list
- [ ] Add API call for organization details
- [ ] Connect discover button to API
- [ ] Add loading states
- [ ] Add error handling
- [ ] Test with backend running
- [ ] Populate database with test data
- [ ] Test all features end-to-end

---

## File Changes Summary

**Files to modify after Lovable export:**

1. `lib/api.ts` - ADD (copy from backend repo)
2. `.env.local` - CREATE
3. `components/organizations-list.tsx` - MODIFY (replace mock data)
4. `components/organization-details.tsx` - MODIFY (add API call)
5. `components/discover-sidebar.tsx` - MODIFY (connect button)
6. `app/page.tsx` - MODIFY (integrate API client)

**Expected time:** 30-45 minutes to integrate

---

## Testing Before Demo

Run through this flow:

1. ✅ Backend starts without errors
2. ✅ Frontend starts without errors
3. ✅ Health check works: http://localhost:8000/health
4. ✅ Organizations list is empty (or populated)
5. ✅ Click "Discover", select "Sports", run discovery
6. ✅ Wait 2-3 minutes
7. ✅ Organizations appear in list
8. ✅ Click organization → Details load
9. ✅ Events display correctly
10. ✅ Contact links work

---

**You're ready to integrate! Follow these steps after getting the frontend from Lovable.** 🚀
