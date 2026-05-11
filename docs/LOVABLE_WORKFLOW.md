# 🎯 Complete Workflow - Lovable Frontend + Backend Integration

## TL;DR

1. **Copy `LOVABLE_PROMPT.md`** into Lovable AI → Generate frontend
2. **Download** the generated project to `frontend/` folder
3. **Follow `INTEGRATION_GUIDE.md`** to connect frontend to backend
4. **Done!** Full-stack app ready for hackathon

---

## 📋 Your Questions Answered

### Q1: Can we use frontend to populate the database without pre-populating?

**YES!** ✅ 

The `POST /discover` endpoint I created allows the frontend to trigger the discovery pipeline directly. Here's how it works:

```
User clicks "Discover" button
    ↓
Frontend: POST /discover with categories
    ↓
Backend: Runs discovery pipeline (2-3 minutes)
    ↓
Backend: Saves organizations to Firebase
    ↓
Frontend: Shows success message + refreshes list
```

**Note:** Discovery takes 2-3 minutes and costs ~$0.04, so:
- Show a progress indicator with status updates
- Allow users to close sidebar while it runs
- For demo: Pre-populate once for instant load, then show live discovery as a feature

---

### Q2: Lovable Prompt for UI

**File:** `LOVABLE_PROMPT.md` ← **Copy this entire file into Lovable**

The prompt includes:
- ✅ Exact layout specifications (30% left list, 70% right details)
- ✅ Component-by-component design requirements
- ✅ Color schemes, spacing, typography
- ✅ Mock data to display
- ✅ Animations and transitions
- ✅ Responsive design requirements
- ✅ shadcn/ui component usage
- ✅ TypeScript interfaces
- ✅ File structure

**The UI will have:**
1. **Navigation bar** - AfterClass logo, Organizations, Events (disabled), Discover button
2. **Left panel (30%)** - Organizations list with search and category badges
3. **Right panel (70%)** - Organization details with contact info and events
4. **Discover sidebar** - Category checkboxes, max orgs input, run discovery button

---

## 🚀 Complete Workflow

### Step 1: Generate Frontend with Lovable

1. Open Lovable AI
2. Copy **entire contents** of `LOVABLE_PROMPT.md`
3. Paste into Lovable prompt area
4. Click Generate
5. Let Lovable build the UI with mock data
6. Preview and tweak if needed
7. Download/Export project

---

### Step 2: Set Up Frontend Locally

```bash
# Move downloaded project to your workspace
cd /Users/rishitreddy/Projects/afterclass
# Assuming Lovable exports to a folder called 'lovable-export'
mv ~/Downloads/lovable-export ./frontend

# Install dependencies
cd frontend
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Copy API client
cp ../frontend-api-client.ts lib/api.ts
```

---

### Step 3: Connect to Backend

Follow `INTEGRATION_GUIDE.md` to:

1. **Replace mock data with API calls**
   - Organizations list: Use `api.getOrganizations()`
   - Organization details: Use `api.getOrganization(id)`
   - Discover button: Use `api.runDiscovery()`

2. **Add loading states**
   - Spinner while loading organizations
   - Progress indicator during discovery

3. **Add error handling**
   - Connection errors
   - No data states

Expected time: **30-45 minutes**

---

### Step 4: Test Everything

**Terminal 1: Backend**
```bash
cd backend
python main.py
# Runs on http://localhost:8000
```

**Terminal 2: Frontend**
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

**Test Checklist:**
- [ ] Organizations list loads (empty is OK)
- [ ] Click "Discover" button
- [ ] Select "Sports" category
- [ ] Set max organizations to 3
- [ ] Click "Run Discovery"
- [ ] Wait 2-3 minutes (show progress)
- [ ] Organizations appear in list
- [ ] Click organization → Details load
- [ ] Events display correctly
- [ ] Contact info is clickable

---

## 📂 Final Project Structure

```
afterclass/
├── backend/                           ← Already complete ✅
│   ├── main.py                        # FastAPI server
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py              # API endpoints
│   │   ├── services/
│   │   │   ├── discovery.py           # Find orgs
│   │   │   └── profiling.py           # Extract data
│   │   └── integrations/
│   │       └── firebase.py            # Database
│   └── .env                           # API keys
│
├── frontend/                          ← Generate with Lovable, then integrate
│   ├── app/
│   │   ├── page.tsx                   # Main page
│   │   └── layout.tsx                 # Root layout
│   ├── components/
│   │   ├── navbar.tsx                 # Navigation
│   │   ├── organizations-list.tsx     # Left panel
│   │   ├── organization-details.tsx   # Right panel
│   │   └── discover-sidebar.tsx       # Discovery UI
│   ├── lib/
│   │   ├── api.ts                     # API client ← Add this
│   │   └── types.ts                   # TypeScript types
│   └── .env.local                     # API_URL ← Add this
│
├── LOVABLE_PROMPT.md                  ← Copy to Lovable
├── INTEGRATION_GUIDE.md               ← Follow after download
├── QUICKSTART.md                      ← Quick reference
└── frontend-api-client.ts             ← Copy to frontend/lib/api.ts
```

---

## 🎨 UI Preview (What Lovable Will Create)

```
┌────────────────────────────────────────────────────────────┐
│ [AfterClass🎓] Organizations Events              Discover 🔍│
├───────────────┬────────────────────────────────────────────┤
│               │                                             │
│ [Search...🔍] │  Södermalms Volleybollklubb                │
│               │  Sports Club · Södermalm                    │
│ ┌───────────┐ │  ───────────────────────────────────────   │
│ │ Södermalm │ │  A vibrant volleyball club offering...     │
│ │ Volley... │ │                                             │
│ │ Sports    │ │  📧 Contact Information                    │
│ └───────────┘ │  • info@sodervoll.se                       │
│               │  • 070-123 45 67                           │
│ ┌───────────┐ │  • https://sodervoll.se ↗                  │
│ │ IF Söder  │ │                                             │
│ │ kamrater  │ │  📅 Events                                 │
│ │ Sports    │ │  ┌──────────────────────────────────┐     │
│ └───────────┘ │  │ Youth Training Ages 7-12         │     │
│               │  │ Recurring · Mon & Wed 17:00      │     │
│ ┌───────────┐ │  └──────────────────────────────────┘     │
│ │ Kungshol  │ │  ┌──────────────────────────────────┐     │
│ │ mens FG   │ │  │ Summer Tournament 2025           │     │
│ │ Youth Ctr │ │  │ One-time · July 15, 2025         │     │
│ └───────────┘ │  └──────────────────────────────────┘     │
│               │                                             │
└───────────────┴────────────────────────────────────────────┘

[Discover Sidebar - slides from right]
┌──────────────────────────┐
│ × Discover Organizations │
│ ───────────────────────  │
│ Select Categories:       │
│ ☑ ⚽ Sports               │
│ ☐ 🏢 Youth Centers        │
│ ☐ ⛺ Scouts                │
│ ☐ 🎨 Cultural             │
│                          │
│ Maximum Organizations: 5 │
│                          │
│ [Run Discovery] ────────►│
│                          │
│ ⚠️ Takes 2-3 minutes      │
└──────────────────────────┘
```

---

## 💡 Pro Tips

### For Demo Day:

1. **Pre-populate database** before demo:
   ```bash
   cd backend
   python test_full_pipeline.py 1
   ```
   This adds 3-5 organizations instantly.

2. **Show discovery live** as a feature:
   - "Now let me show you how we discover new organizations..."
   - Click Discover → Select category → Run
   - Explain: "It's crawling websites right now..."
   - While waiting: Show existing orgs, click around
   - When done: "And here are the new ones!"

3. **Highlight features:**
   - Category filtering
   - Search functionality
   - Clickable contact info
   - Multiple events per organization
   - Clean, professional UI

---

## 🔧 Troubleshooting

### Lovable doesn't generate correctly?
- Break down the prompt into smaller sections
- Generate components separately
- Use the mock data provided in the prompt

### API calls not working?
- Check backend is running: `curl http://localhost:8000/health`
- Check `.env.local` has correct URL
- Check browser console for errors
- Verify CORS is enabled in backend

### Discovery takes too long?
- It's supposed to take 2-3 minutes (crawling websites)
- Reduce `max_organizations` to 2-3 for faster testing
- Pre-populate for demos

---

## ✅ Success Checklist

Before demo:
- [ ] Backend runs without errors
- [ ] Frontend runs without errors  
- [ ] Database has 5-10 organizations
- [ ] Organizations list displays correctly
- [ ] Details panel shows full information
- [ ] Contact info is clickable
- [ ] Events display properly
- [ ] Discover sidebar opens smoothly
- [ ] Discovery finds new organizations
- [ ] UI looks professional and polished
- [ ] Responsive on different screen sizes

---

## 🎬 Next Steps

1. **Now:** Copy `LOVABLE_PROMPT.md` → Generate frontend in Lovable
2. **Then:** Download → Set up locally → Copy API client
3. **Next:** Follow `INTEGRATION_GUIDE.md` → Connect to backend
4. **Finally:** Test everything → Pre-populate DB → Ready for demo!

**Estimated total time:** 2-3 hours (Lovable: 30min, Integration: 45min, Testing: 1hr)

---

## 📚 Documentation Reference

| File | Purpose |
|------|---------|
| `LOVABLE_PROMPT.md` | Copy-paste into Lovable to generate UI |
| `INTEGRATION_GUIDE.md` | Step-by-step backend integration |
| `QUICKSTART.md` | Quick reference for running everything |
| `FRONTEND_BACKEND_GUIDE.md` | Detailed API documentation |
| `frontend-api-client.ts` | Ready-to-use API client for frontend |

---

**You're all set! 🚀 Start with Lovable, then integrate, and you'll have a complete full-stack app ready for your hackathon!**
