# ⚡ Quick Reference Card - AfterClass Project

## 🎯 What You Need to Do

### Step 1: Generate Frontend (30 minutes)
1. Open Lovable AI
2. Copy **entire** `LOVABLE_PROMPT.md` 
3. Paste → Generate
4. Download project

### Step 2: Integrate (45 minutes)
1. Move to `frontend/` folder
2. Run `npm install`
3. Create `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8000`
4. Copy `frontend-api-client.ts` to `lib/api.ts`
5. Follow `INTEGRATION_GUIDE.md` to replace mock data

### Step 3: Test (30 minutes)
1. Terminal 1: `cd backend && python main.py`
2. Terminal 2: `cd frontend && npm run dev`
3. Test all features
4. Pre-populate: `python test_full_pipeline.py 1`

**Total Time: 2-3 hours** ⏱️

---

## 📋 Essential Files

| File | Purpose | Action |
|------|---------|--------|
| `LOVABLE_PROMPT.md` | Frontend generation | Copy to Lovable |
| `INTEGRATION_GUIDE.md` | Connect frontend to backend | Follow after download |
| `frontend-api-client.ts` | API client code | Copy to `frontend/lib/api.ts` |
| `UI_DESIGN_REFERENCE.md` | Visual specifications | Reference during tweaking |
| `LOVABLE_WORKFLOW.md` | Complete workflow | Read for overview |

---

## 🚀 Commands Cheat Sheet

### Backend Commands
```bash
# Start server
cd backend
python main.py

# Test API
python test_api.py

# Pre-populate database
python test_full_pipeline.py 1

# Check health
curl http://localhost:8000/health
```

### Frontend Commands
```bash
# Install dependencies
cd frontend
npm install

# Create env file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start dev server
npm run dev

# Build for production
npm run build
```

---

## 🎨 UI Layout Quick Reference

```
┌──────────────────────────────────────────────────┐
│ 🎓 AfterClass | Organizations | Events | Discover │
├─────────────────┬────────────────────────────────┤
│ [Search...]     │ Organization Name              │
│                 │ Type • Location                │
│ □ Org Card 1    │ Description...                 │
│   Sports        │                                │
│                 │ 📧 Contact Info                │
│ □ Org Card 2    │ • Email                        │
│   Youth Center  │ • Phone                        │
│                 │ • Website                      │
│ □ Org Card 3    │                                │
│   Scouts        │ 📅 Events                      │
│                 │ • Event 1                      │
└─────────────────┴────────────────────────────────┘
    30% width           70% width
```

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check if backend is running |
| `/organizations` | GET | List all organizations |
| `/organizations?category=sports` | GET | Filter by category |
| `/organizations/{id}` | GET | Get single org with events |
| `/discover` | POST | Run discovery pipeline |

---

## 💾 Data Structure

```typescript
Organization {
  id: string
  name: string
  type: string
  location: string
  description: string
  contact: { email, phone }
  website: string
  discovery: { category, search_query }
  events: Event[]
}

Event {
  name: string
  type: 'recurring' | 'one-time'
  schedule: string | null
  date: string | null
  age_range: string
  description: string
}
```

---

## 🎨 Category Colors

| Category | Badge Color |
|----------|-------------|
| Sports | Blue (#2563eb) |
| Youth Centers | Green (#16a34a) |
| Scouts | Purple (#9333ea) |
| Cultural | Orange (#f97316) |

---

## ⚙️ Environment Variables

### Backend (.env)
```bash
TAVILY_API_KEY=your_key
OPENAI_API_KEY=your_key
FIREBASE_CREDENTIALS_PATH=path/to/firebase.json
ENVIRONMENT=development
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🔍 Testing Checklist

Before Demo:
- [ ] Backend starts on port 8000
- [ ] Frontend starts on port 3000
- [ ] Health endpoint responds
- [ ] Organizations list loads
- [ ] Click organization shows details
- [ ] Contact links work
- [ ] Events display correctly
- [ ] Discover sidebar opens
- [ ] Discovery finds new orgs
- [ ] UI looks polished

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| CORS error | Check `main.py` allows localhost:3000 |
| No organizations | Run `python test_full_pipeline.py 1` |
| API not connecting | Check `.env.local` has correct URL |
| Discovery fails | Verify API keys in backend `.env` |
| Port in use | Kill process: `lsof -ti:8000 \| xargs kill -9` |

---

## 📱 Responsive Breakpoints

- **Desktop:** ≥1024px (30/70 split)
- **Tablet:** 768-1023px (35/65 split)
- **Mobile:** <768px (stacked vertical)

---

## 🎯 Demo Flow

1. **Show organizations list** (instant load - pre-populated)
2. **Click organization** → Details appear
3. **Show contact info** → Click links
4. **Show events** → Multiple events per org
5. **Click "Discover"** → Open sidebar
6. **Select category** → Run discovery (optional)
7. **Explain:** "Finding new organizations in Stockholm..."

---

## 💡 Pro Tips

✅ **Pre-populate before demo** - Instant load impresses judges  
✅ **Test discovery once** - Know how long it takes  
✅ **Have backup data** - In case API fails  
✅ **Show live discovery** - If time permits  
✅ **Explain the tech** - Tavily crawl, OpenAI extraction, Firebase

---

## 📞 Integration Code Snippets

### Load Organizations
```typescript
const [orgs, setOrgs] = useState<Organization[]>([]);

useEffect(() => {
  api.getOrganizations().then(data => {
    setOrgs(data.organizations);
  });
}, []);
```

### Run Discovery
```typescript
async function discover() {
  const result = await api.runDiscovery(['sports'], 5);
  console.log(`Found ${result.organizations_found} orgs`);
}
```

### Get Details
```typescript
const org = await api.getOrganization(orgId);
console.log(org.name, org.events);
```

---

## 🎓 Tech Stack Summary

**Frontend:** Next.js 14, TypeScript, Tailwind, shadcn/ui  
**Backend:** FastAPI, Python 3.10+  
**Database:** Firebase Firestore  
**APIs:** Tavily (crawl), OpenAI (extraction)  
**Deployment:** Vercel (frontend), Railway/Render (backend)

---

## ✅ Success Metrics

- **Discovery:** 75% success rate
- **Cost:** ~$0.008 per organization
- **Speed:** 2-3 minutes for 5 organizations
- **Data Quality:** Contact info + events extracted
- **UI:** Professional, responsive, polished

---

## 📚 Documentation Map

```
afterclass/
├── LOVABLE_PROMPT.md         ← START HERE: Copy to Lovable
├── LOVABLE_WORKFLOW.md       ← Complete workflow guide
├── INTEGRATION_GUIDE.md      ← After Lovable: Integration steps
├── UI_DESIGN_REFERENCE.md    ← Visual specs and colors
├── FRONTEND_BACKEND_GUIDE.md ← API documentation
├── QUICKSTART.md             ← Quick setup reference
└── THIS FILE (QUICK_REFERENCE.md) ← Cheat sheet
```

---

## 🚀 Ready to Start?

1. **Read:** `LOVABLE_WORKFLOW.md` for overview (5 min)
2. **Copy:** `LOVABLE_PROMPT.md` to Lovable (30 min)
3. **Follow:** `INTEGRATION_GUIDE.md` for connection (45 min)
4. **Test:** Everything works end-to-end (30 min)
5. **Demo!** 🎉

---

**Questions? Check the documentation files. Everything is documented!** 📖
