# Lovable AI Prompt - AfterClass Frontend

Copy and paste this entire prompt into Lovable AI to generate your frontend.

---

# Project Brief: AfterClass - Youth Organizations Discovery Platform

## Project Overview
Build a modern, clean web application that displays youth organizations in Stockholm with their contact information and events. The UI should be professional, user-friendly, and perfect for a hackathon demo.

---

## Tech Stack Requirements
- **Framework:** Next.js 14+ with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui (for professional, accessible components)
- **State Management:** React hooks (useState, useEffect)
- **Icons:** Lucide React
- **Color Scheme:** Modern, professional (suggest blue/purple gradient accents)

---

## Application Structure

### Route: `/` (Single Page Application)

The entire application lives on one route with a clean, split-view layout.

---

## Layout Design (CRITICAL - Follow Exactly)

```
┌─────────────────────────────────────────────────────────────┐
│  Navigation Bar (Full Width, Fixed Top)                     │
│  [AfterClass Logo] [Organizations] [Events] [Discover 🔍]  │
└─────────────────────────────────────────────────────────────┘
│                                                              │
│  ┌──────────────────┬────────────────────────────────────┐ │
│  │  Organizations   │  Organization Details              │ │
│  │  List (30%)      │  Panel (70%)                       │ │
│  │                  │                                     │ │
│  │  [Search Bar]    │  ┌──────────────────────────────┐ │ │
│  │                  │  │  Selected Organization       │ │ │
│  │  Card 1          │  │  - Name (Large, Bold)        │ │ │
│  │  • Name          │  │  - Type Badge                 │ │ │
│  │  • Type          │  │  - Location (with icon)      │ │ │
│  │  • Category Tag  │  │  - Description               │ │ │
│  │                  │  │                               │ │ │
│  │  Card 2          │  │  Contact Information         │ │ │
│  │  • Name          │  │  - 📧 Email (clickable)       │ │ │
│  │  • Type          │  │  - 📞 Phone (clickable)       │ │ │
│  │  • Category Tag  │  │  - 🌐 Website (clickable)     │ │ │
│  │                  │  │                               │ │ │
│  │  Card 3          │  │  Events Section              │ │ │
│  │  ...             │  │  - Event cards with:         │ │ │
│  │                  │  │    • Name                     │ │ │
│  │  [Load More]     │  │    • Type badge               │ │ │
│  │                  │  │    • Schedule/Date            │ │ │
│  └──────────────────┘  │    • Age Range                │ │ │
│                        │    • Description              │ │ │
│                        └──────────────────────────────┘ │ │
│                                                           │ │
└───────────────────────────────────────────────────────────┘

[Discover Sidebar - Slides from Right]
┌─────────────────────────────┐
│  × Discover Organizations   │
│  ─────────────────────────  │
│                              │
│  Select Categories:          │
│  ☐ Sports                    │
│  ☐ Youth Centers             │
│  ☐ Scouts                    │
│  ☐ Cultural                  │
│                              │
│  Max Organizations: [5]      │
│                              │
│  [Run Discovery Button]      │
│                              │
│  Status: Ready / Running     │
│  Progress indicator here     │
└─────────────────────────────┘
```

---

## Component Specifications

### 1. Navigation Bar
**Requirements:**
- Fixed at top, sticky on scroll
- Clean, modern design with gradient or solid professional color
- Logo/Brand: "AfterClass" with a simple icon (suggest 🎓 or 🌟)
- Navigation items: "Organizations" (active), "Events" (disabled/grayed out)
- Right side: "Discover" button with search icon (🔍) that opens sidebar
- Height: ~64px
- Shadow: Subtle drop shadow for depth

**Example shadcn/ui components to use:**
- Use `Button` component with variant="ghost" for nav items
- Use `Button` with variant="default" for Discover button

---

### 2. Organizations List (Left Panel - 30% width)

**Container:**
- Background: Light gray/white (bg-gray-50)
- Padding: p-4
- Overflow-y: Auto (scrollable)
- Border-right: Subtle divider

**Search Bar:**
- Position: Top of list, sticky
- Placeholder: "Search organizations..."
- Icon: Search icon (🔍) on left
- Margin bottom: mb-4
- Use shadcn/ui `Input` component

**Organization Cards:**
- Design: Clean card with hover effect
- Border: Subtle border, rounded corners (rounded-lg)
- Padding: p-4
- Margin: mb-3
- Hover: Scale slightly (scale-105) and add shadow
- Active/Selected: Border color changes (blue/purple), background slightly darker

**Card Content:**
- Organization Name: Font-semibold, text-base
- Type: text-sm, text-gray-600
- Category Badge: Small pill badge with category color:
  - Sports: Blue
  - Youth Centers: Green
  - Scouts: Purple
  - Cultural: Orange

**Empty State:**
- Show when no organizations
- Icon: 📭
- Text: "No organizations found"
- Sub-text: "Click 'Discover' to find organizations"

---

### 3. Organization Details Panel (Right Panel - 70% width)

**Container:**
- Background: White
- Padding: p-8
- Overflow-y: Auto (scrollable)

**Organization Header:**
- Organization Name: text-3xl, font-bold, mb-2
- Type Badge: Colored badge/pill (e.g., "Sports Club")
- Location: text-gray-600 with location icon 📍
- Description: text-lg, text-gray-700, mt-4, leading-relaxed

**Contact Information Section:**
- Header: "Contact Information" (text-xl, font-semibold, mt-6, mb-4)
- Styled as cards or list items with icons:
  - Email: 📧 icon, clickable (mailto:), blue text on hover
  - Phone: 📞 icon, clickable (tel:), blue text on hover
  - Website: 🌐 icon, clickable link with external icon, opens in new tab
- If contact info missing: Show "Not available" in gray

**Events Section:**
- Header: "Events" (text-xl, font-semibold, mt-8, mb-4)
- Event Cards: Grid or stack of cards
  - Border: rounded-lg border
  - Padding: p-4
  - Event Name: font-semibold
  - Type Badge: Pill badge ("Recurring" in blue, "One-time" in green)
  - Schedule/Date: with calendar icon 📅
  - Age Range: with icon 👥
  - Description: text-sm, text-gray-600
- If no events: Show "No events listed" in gray

**Empty State (No org selected):**
- Center content vertically and horizontally
- Icon: 👈 or 📋
- Text: "Select an organization to view details"
- Subtext: "Choose from the list on the left"

---

### 4. Discover Sidebar (Slide-out from Right)

**Trigger:**
- Click "Discover" button in navigation
- Sidebar slides in from right with smooth animation

**Sidebar Design:**
- Width: 400px (or ~30% viewport)
- Background: White
- Shadow: Large left shadow for depth
- Close button: × in top right corner

**Content:**
- Header: "Discover Organizations" (text-xl, font-bold)
- Divider line

**Category Selection:**
- Label: "Select Categories"
- Checkboxes with labels:
  - ☐ Sports
  - ☐ Youth Centers
  - ☐ Scouts
  - ☐ Cultural
- Use shadcn/ui `Checkbox` component
- Each checkbox should have an icon next to it (⚽, 🏢, ⛺, 🎨)

**Max Organizations Input:**
- Label: "Maximum Organizations"
- Input: Number input, default value: 5, min: 1, max: 20
- Helper text: "How many organizations to discover"

**Action Button:**
- Text: "Run Discovery"
- Full width button
- Primary color (blue/purple gradient)
- Disabled state when running
- Margin top: mt-6

**Status Display:**
- Shows: "Ready", "Running...", "Completed"
- Progress indicator when running (spinner or progress bar)
- Results summary when done:
  - "Found 5 organizations"
  - "Saved 4 organizations"
  - "Filtered 1 irrelevant"

**Notes Section:**
- Small text at bottom
- "⚠️ Discovery takes 2-3 minutes"
- "💡 New organizations will appear in the list"

---

## Data Types (TypeScript Interfaces)

```typescript
interface Organization {
  id: string;
  name: string;
  type: string;
  location: string;
  description: string;
  contact: {
    email: string | null;
    phone: string | null;
  };
  website: string;
  discovery: {
    category: 'sports' | 'youth_centers' | 'scouts' | 'cultural';
    search_query: string;
  };
  events?: Event[];
}

interface Event {
  id: string;
  organization_id: string;
  name: string;
  type: 'recurring' | 'one-time';
  schedule: string | null;
  date: string | null;
  age_range: string | null;
  description: string;
}
```

---

## Mock Data (Use This for Initial Development)

Create mock data to display while building the UI. Use this data structure:

```typescript
const mockOrganizations: Organization[] = [
  {
    id: '1',
    name: 'Södermalms Volleybollklubb',
    type: 'Sports Club',
    location: 'Södermalm, Stockholm',
    description: 'A vibrant volleyball club offering training for youth ages 7-19. We focus on both competitive and recreational volleyball with professional coaches.',
    contact: {
      email: 'info@sodervoll.se',
      phone: '070-123 45 67'
    },
    website: 'https://sodervoll.se',
    discovery: {
      category: 'sports',
      search_query: 'Södermalm volleyboll ungdom'
    },
    events: [
      {
        id: 'e1',
        organization_id: '1',
        name: 'Youth Training - Ages 7-12',
        type: 'recurring',
        schedule: 'Mondays and Wednesdays, 17:00-18:30',
        date: null,
        age_range: '7-12',
        description: 'Basic volleyball skills and fun games'
      },
      {
        id: 'e2',
        organization_id: '1',
        name: 'Summer Tournament 2025',
        type: 'one-time',
        schedule: null,
        date: '2025-07-15',
        age_range: '10-16',
        description: 'Annual summer volleyball tournament'
      }
    ]
  },
  {
    id: '2',
    name: 'IF Söderkamraterna',
    type: 'Sports Club',
    location: 'Södermalm, Stockholm',
    description: 'Football club for youth with teams from age 6 to 19. We emphasize teamwork, skill development, and having fun.',
    contact: {
      email: 'info@soderkamraterna.se',
      phone: '070-742 59 22'
    },
    website: 'https://soderkamraterna.se',
    discovery: {
      category: 'sports',
      search_query: 'Södermalm fotboll barn'
    },
    events: [
      {
        id: 'e3',
        organization_id: '2',
        name: 'Training - F13 Team',
        type: 'recurring',
        schedule: 'Tuesdays and Thursdays, 18:00-19:30',
        date: null,
        age_range: '13',
        description: 'Football training for 13-year-olds'
      }
    ]
  },
  {
    id: '3',
    name: 'Kungsholmens Fritidsgård',
    type: 'Youth Center',
    location: 'Kungsholmen, Stockholm',
    description: 'Open youth center with activities, workshops, and a safe space for teenagers to hang out.',
    contact: {
      email: 'info@kungsholmensfg.se',
      phone: null
    },
    website: 'https://kungsholmensfg.se',
    discovery: {
      category: 'youth_centers',
      search_query: 'Kungsholmen fritidsgård'
    },
    events: []
  }
];
```

---

## User Interactions

### 1. Select Organization
- Click on organization card in left panel
- Card highlights with border/background change
- Right panel updates to show selected organization details
- Smooth scroll animation

### 2. Search Organizations
- Type in search bar
- Filter organizations by name (real-time)
- Show "No results" if nothing matches

### 3. Click Contact Info
- Email: Opens mail client (mailto:)
- Phone: Opens phone dialer on mobile (tel:)
- Website: Opens in new tab with external link icon

### 4. Open Discover Sidebar
- Click "Discover" button in nav
- Sidebar slides in from right with smooth animation (300ms)
- Overlay darkens the main content slightly

### 5. Run Discovery
- Select categories (at least one required)
- Set max organizations
- Click "Run Discovery"
- Button shows loading spinner
- Status updates: "Running..."
- When complete: Show success message
- Sidebar can be closed

### 6. Close Sidebar
- Click × button
- Click outside sidebar (on overlay)
- Sidebar slides out with animation

---

## Responsive Design

### Desktop (Default)
- Split view as described above (30% / 70%)
- All features visible

### Tablet (768px - 1024px)
- Organizations list: 35%
- Details panel: 65%
- Slightly reduce padding

### Mobile (< 768px)
- Stack vertically
- Organizations list shows as drawer/modal
- Floating action button to open list
- Details panel takes full width
- Sidebar takes full width when open

---

## Color Scheme Suggestion

**Primary Colors:**
- Primary: Blue-600 (#2563eb) or Purple-600 (#9333ea)
- Secondary: Gray-600 (#4b5563)
- Success: Green-600 (#16a34a)
- Warning: Orange-500 (#f97316)

**Backgrounds:**
- Main: White (#ffffff)
- Sidebar/List: Gray-50 (#f9fafb)
- Cards: White with border

**Text:**
- Primary: Gray-900 (#111827)
- Secondary: Gray-600 (#4b5563)
- Muted: Gray-400 (#9ca3af)

**Accents:**
- Category badges use brand colors
- Hover states: Primary color with opacity

---

## Animations & Transitions

- Card hover: `transition-all duration-200 ease-in-out`
- Sidebar slide: `transition-transform duration-300 ease-out`
- Content fade: `transition-opacity duration-200`
- Button hover: `transition-colors duration-150`

---

## Accessibility Requirements

- All buttons have proper aria-labels
- Keyboard navigation works (Tab, Enter, Escape)
- Focus states visible on all interactive elements
- Color contrast meets WCAG AA standards
- Alt text for icons (use aria-label)

---

## Component Library Recommendations

Use **shadcn/ui** components:
- `Button` - For all buttons
- `Input` - For search and number inputs
- `Card` - For organization and event cards
- `Badge` - For category and type badges
- `Sheet` - For the discover sidebar
- `Checkbox` - For category selection
- `Separator` - For divider lines

Install with:
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input card badge sheet checkbox separator
```

---

## File Structure

```
app/
├── page.tsx                    # Main page component
├── layout.tsx                  # Root layout
├── globals.css                 # Global styles
components/
├── navbar.tsx                  # Navigation bar
├── organizations-list.tsx      # Left panel with org list
├── organization-details.tsx    # Right panel with org details
├── organization-card.tsx       # Individual org card
├── event-card.tsx              # Event display card
├── discover-sidebar.tsx        # Discover sidebar component
├── search-bar.tsx              # Search input component
└── ui/                         # shadcn/ui components
lib/
├── types.ts                    # TypeScript interfaces
└── mock-data.ts                # Mock organizations data
```

---

## Initial State Management

Use React hooks:
```typescript
const [organizations, setOrganizations] = useState(mockOrganizations);
const [selectedOrgId, setSelectedOrgId] = useState<string | null>(null);
const [searchQuery, setSearchQuery] = useState('');
const [isSidebarOpen, setIsSidebarOpen] = useState(false);
const [isDiscovering, setIsDiscovering] = useState(false);
```

---

## Key Features Checklist

- [ ] Clean, modern UI with professional design
- [ ] Split view layout (30% list / 70% details)
- [ ] Organization list with search
- [ ] Organization details with contact info
- [ ] Events display
- [ ] Discover sidebar with category selection
- [ ] Smooth animations and transitions
- [ ] Responsive design (desktop, tablet, mobile)
- [ ] Category badges with colors
- [ ] Type badges for events
- [ ] Clickable contact information
- [ ] Empty states for no data
- [ ] Loading states for discovery
- [ ] Mock data for demonstration

---

## Important Notes for Lovable

1. **Focus on UI/UX** - Make it look professional and polished
2. **Use mock data** - Don't worry about API calls yet (I'll add them later)
3. **Component library** - Use shadcn/ui for consistency
4. **Responsive** - Must work on desktop (priority), tablet, and mobile
5. **Smooth interactions** - Add transitions and hover effects
6. **Empty states** - Handle "no data" scenarios gracefully
7. **Discovery sidebar** - Just the UI for now, no actual API call needed

---

## Success Criteria

The frontend is successful if:
✅ Layout matches the design (30/70 split view)
✅ All components are properly styled with shadcn/ui
✅ Organization selection works smoothly
✅ Contact information is clickable
✅ Discover sidebar opens/closes smoothly
✅ Search filters organizations
✅ Responsive on all screen sizes
✅ Professional, modern appearance
✅ Smooth animations throughout

---

**Generate a Next.js 14+ app with TypeScript and Tailwind CSS following these specifications exactly. Focus on creating a beautiful, professional UI with smooth interactions. Use shadcn/ui components for consistency. Display mock data for now.**
