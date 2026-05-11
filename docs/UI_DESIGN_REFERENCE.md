# 🎨 UI Design Reference - AfterClass Frontend

**Visual guide for what to expect from Lovable**

---

## 📐 Layout Dimensions

```
┌────────────────────────────────────────────────────────┐
│                    Navigation Bar                       │  64px height
│                     (Full Width)                        │
├──────────────────┬─────────────────────────────────────┤
│                  │                                      │
│  Organizations   │    Organization Details Panel        │
│    List Panel    │                                      │
│                  │                                      │
│   30% width      │         70% width                    │
│   (min 320px)    │         (flexible)                   │
│                  │                                      │
│   Scrollable ↕   │         Scrollable ↕                 │
│                  │                                      │
│                  │                                      │
│                  │                                      │
│                  │                                      │
└──────────────────┴─────────────────────────────────────┘
     min-w-[320px]              flex-1
```

---

## 🎨 Color Palette

```css
/* Primary Brand Colors */
--primary: #2563eb (Blue-600)         /* Main buttons, links */
--primary-hover: #1d4ed8 (Blue-700)   /* Hover states */
--secondary: #9333ea (Purple-600)     /* Accents */

/* Background Colors */
--bg-main: #ffffff (White)            /* Main content area */
--bg-sidebar: #f9fafb (Gray-50)       /* Left panel, sidebar */
--bg-card: #ffffff (White)            /* Cards */
--bg-hover: #f3f4f6 (Gray-100)        /* Card hover */

/* Text Colors */
--text-primary: #111827 (Gray-900)    /* Headings */
--text-secondary: #4b5563 (Gray-600)  /* Body text */
--text-muted: #9ca3af (Gray-400)      /* Placeholder, disabled */

/* Category Badge Colors */
--sports: #2563eb (Blue-600)          /* Sports category */
--youth-centers: #16a34a (Green-600)  /* Youth centers */
--scouts: #9333ea (Purple-600)        /* Scouts */
--cultural: #f97316 (Orange-500)      /* Cultural */

/* Event Type Badges */
--recurring: #3b82f6 (Blue-500)       /* Recurring events */
--one-time: #10b981 (Green-500)       /* One-time events */

/* Borders & Shadows */
--border: #e5e7eb (Gray-200)          /* Card borders */
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05)
--shadow-md: 0 4px 6px rgba(0,0,0,0.1)
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1)
```

---

## 🧩 Component Specifications

### Navigation Bar
```
┌─────────────────────────────────────────────────────────────┐
│  🎓 AfterClass    Organizations    Events    [Discover 🔍]  │
│  ←Logo/Icon        ←Nav Items (Events grayed) ←Button→      │
│                                                    primary   │
└─────────────────────────────────────────────────────────────┘

Height: 64px (h-16)
Background: White with shadow-sm
Padding: px-6 py-4
Border-bottom: 1px solid gray-200

Logo: text-xl font-bold with gradient or icon
Nav items: text-base font-medium
Active: text-primary with underline
Disabled: text-gray-400 opacity-50
Button: bg-primary text-white rounded-lg px-4 py-2
```

---

### Organization Card (in List)
```
┌──────────────────────────────────┐
│  Södermalms Volleybollklubb      │ ← font-semibold text-base
│  Sports Club                      │ ← text-sm text-gray-600
│  ┌────────┐                       │
│  │ Sports │                       │ ← Badge (blue)
│  └────────┘                       │
└──────────────────────────────────┘

Width: 100% of left panel
Height: Auto (min 100px)
Padding: p-4
Margin: mb-3
Border: 1px solid gray-200, rounded-lg
Background: white

States:
- Default: border-gray-200 bg-white
- Hover: border-primary bg-gray-50 scale-[1.02]
- Selected: border-primary-600 border-2 bg-blue-50

Transition: all 200ms ease-in-out
```

---

### Search Bar
```
┌──────────────────────────────────┐
│  🔍  Search organizations...     │
└──────────────────────────────────┘

Width: 100%
Height: 40px (h-10)
Padding: px-4 py-2 pl-10 (for icon)
Border: 1px solid gray-300, rounded-lg
Background: white
Icon: Absolute left-3, gray-400

Focus state: border-primary ring-2 ring-primary/20
```

---

### Organization Details Header
```
┌─────────────────────────────────────────────────────┐
│  Södermalms Volleybollklubb                         │ ← text-3xl font-bold
│  ┌────────────┐                                     │
│  │Sports Club │                                     │ ← Badge
│  └────────────┘                                     │
│  📍 Södermalm, Stockholm                            │ ← text-gray-600
│                                                      │
│  A vibrant volleyball club offering training...     │ ← text-lg leading-relaxed
└─────────────────────────────────────────────────────┘

Name: mb-2
Badge: mt-2 mb-3
Location: mb-4 with icon
Description: mt-4 text-gray-700
```

---

### Contact Information Section
```
┌─────────────────────────────────────────┐
│  Contact Information                     │ ← text-xl font-semibold
│  ─────────────────────────────────       │
│                                           │
│  📧  info@sodervoll.se               →   │ ← Clickable, hover:text-primary
│  📞  070-123 45 67                   →   │ ← Clickable, hover:text-primary
│  🌐  https://sodervoll.se            ↗   │ ← Clickable, opens new tab
└─────────────────────────────────────────┘

Layout: Vertical stack (space-y-3)
Each item: p-3 border rounded-lg hover:bg-gray-50
Icon: mr-3, text-xl
Text: text-base, clickable
External link icon: ml-2
```

---

### Event Card
```
┌──────────────────────────────────────────────────────┐
│  Youth Training - Ages 7-12            ┌──────────┐  │
│                                        │Recurring │  │ ← Badge
│  📅  Mondays and Wednesdays, 17:00-18:30 └──────────┘  │
│  👥  Ages 7-12                                       │
│                                                       │
│  Basic volleyball skills and fun games               │
└──────────────────────────────────────────────────────┘

Width: 100%
Padding: p-4
Border: 1px solid gray-200, rounded-lg
Background: white
Margin: mb-3

Name: font-semibold text-base mb-2
Badge: Absolute top-right
Icons: text-sm mr-2
Description: text-sm text-gray-600 mt-2
```

---

### Category Badge
```
┌─────────┐
│ Sports  │  Blue background (bg-blue-100 text-blue-700)
└─────────┘

┌────────────────┐
│ Youth Centers  │  Green (bg-green-100 text-green-700)
└────────────────┘

┌─────────┐
│ Scouts  │  Purple (bg-purple-100 text-purple-700)
└─────────┘

┌────────────┐
│ Cultural   │  Orange (bg-orange-100 text-orange-700)
└────────────┘

Style: px-2.5 py-1 rounded-full text-xs font-medium
```

---

### Event Type Badge
```
┌────────────┐
│ Recurring  │  Blue (bg-blue-500 text-white)
└────────────┘

┌──────────┐
│ One-time │  Green (bg-green-500 text-white)
└──────────┘

Style: px-2 py-1 rounded text-xs font-medium
```

---

### Discover Sidebar
```
┌───────────────────────────────────┐
│  ×  Discover Organizations        │ ← Header with close button
│  ─────────────────────────────    │
│                                    │
│  Select Categories                 │ ← Label
│                                    │
│  ☑ ⚽ Sports                        │ ← Checkbox with icon
│  ☐ 🏢 Youth Centers                │
│  ☐ ⛺ Scouts                        │
│  ☐ 🎨 Cultural                     │
│                                    │
│  Maximum Organizations             │
│  ┌──┐                              │
│  │5 │                              │ ← Number input
│  └──┘                              │
│                                    │
│  ┌──────────────────────────────┐ │
│  │     Run Discovery            │ │ ← Primary button
│  └──────────────────────────────┘ │
│                                    │
│  ⚠️ Discovery takes 2-3 minutes    │
│  💡 New orgs will appear in list   │
└───────────────────────────────────┘

Width: 400px (or 30vw)
Height: 100vh
Position: Fixed right
Background: white
Shadow: -10px 0 30px rgba(0,0,0,0.1)
Padding: p-6

Animation: Slide in from right (translate-x)
Duration: 300ms ease-out
Overlay: bg-black/20 backdrop-blur-sm
```

---

## 📱 Responsive Breakpoints

### Desktop (≥ 1024px)
```
Layout: Side-by-side (30% / 70%)
Nav: Horizontal
Sidebar: 400px wide
Font sizes: Normal
Padding: Generous (p-6, p-8)
```

### Tablet (768px - 1023px)
```
Layout: Side-by-side (35% / 65%)
Nav: Horizontal, condensed
Sidebar: 350px wide
Font sizes: Slightly smaller
Padding: Moderate (p-4, p-6)
```

### Mobile (< 768px)
```
Layout: Stacked vertical
Nav: Hamburger menu or tabs
List: Full width drawer
Details: Full width main content
Sidebar: Full width slide-over
Font sizes: Optimized for mobile
Padding: Minimal (p-3, p-4)

Floating Action Button (FAB): 
  Bottom-right corner
  Opens organizations drawer
```

---

## 🎭 Animations & Transitions

```css
/* Card Hover */
.org-card:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: all 200ms ease-in-out;
}

/* Sidebar Slide In */
.sidebar-enter {
  transform: translateX(100%);
}
.sidebar-enter-active {
  transform: translateX(0);
  transition: transform 300ms ease-out;
}

/* Content Fade */
.fade-in {
  animation: fadeIn 200ms ease-in;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Button Hover */
.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  transition: all 150ms ease;
}

/* Loading Spinner */
.spinner {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## 🖼️ Empty States

### No Organizations
```
┌──────────────────────────────────────┐
│                                       │
│              📭                       │  ← text-6xl
│                                       │
│    No organizations yet               │  ← text-xl font-semibold
│                                       │
│    Click "Discover" to find some!     │  ← text-gray-600
│                                       │
└──────────────────────────────────────┘

Centered both horizontally and vertically
```

### No Organization Selected
```
┌──────────────────────────────────────┐
│                                       │
│              👈                       │  ← text-6xl
│                                       │
│    Select an organization             │  ← text-xl font-semibold
│                                       │
│    Choose from the list on the left   │  ← text-gray-600
│                                       │
└──────────────────────────────────────┘
```

### No Events
```
┌──────────────────────────────────────┐
│  Events                               │  ← Section header
│  ─────────────────────────            │
│                                       │
│  No events listed for this org        │  ← text-gray-500
│                                       │
└──────────────────────────────────────┘
```

---

## 🔄 Loading States

### Loading Organizations
```
┌──────────────────────────────┐
│  ╔═══════════╗               │  ← Skeleton card
│  ║           ║               │     Animated shimmer
│  ║ ▓▓▓▓▓▓    ║               │     bg-gray-200
│  ║ ▓▓▓       ║               │     animate-pulse
│  ╚═══════════╝               │
│                               │
│  ╔═══════════╗               │  ← Multiple skeletons
│  ║ ▓▓▓▓▓▓    ║               │
│  ╚═══════════╝               │
└──────────────────────────────┘
```

### Discovering Organizations
```
┌────────────────────────────────┐
│  Status: Running...            │
│                                 │
│  ⭕ Finding organizations...    │  ← Spinner
│                                 │
│  This may take 2-3 minutes     │
│                                 │
│  ▓▓▓▓▓▓░░░░░░░░░░░░░░  40%     │  ← Progress bar
└────────────────────────────────┘
```

---

## 💡 Interaction Patterns

### Click Organization Card
```
Before:  border-gray-200 bg-white
Click:   border-primary bg-blue-50
Effect:  Smooth transition 200ms
Action:  Load details in right panel
```

### Hover Organization Card
```
Default: border-gray-200 bg-white scale-100
Hover:   border-gray-300 bg-gray-50 scale-102
         shadow-md
Cursor:  pointer
```

### Click Contact Info
```
Email:   mailto: link, blue on hover
Phone:   tel: link, blue on hover
Website: Opens new tab, external icon shown
```

### Open Discover Sidebar
```
Trigger: Click "Discover" button
Action:  Sidebar slides in from right
         Main content darkens (overlay)
         Body scroll locks
```

### Close Discover Sidebar
```
Triggers: 
  - Click × button
  - Click overlay
  - Press Escape key
Action:  Sidebar slides out
         Overlay fades out
         Body scroll unlocks
```

---

## 📏 Spacing & Typography

### Spacing Scale
```
xs:  0.25rem (4px)
sm:  0.5rem  (8px)
md:  1rem    (16px)
lg:  1.5rem  (24px)
xl:  2rem    (32px)
2xl: 3rem    (48px)
```

### Typography Scale
```
xs:   0.75rem (12px) - Captions, badges
sm:   0.875rem (14px) - Small text, meta info
base: 1rem (16px) - Body text
lg:   1.125rem (18px) - Large body
xl:   1.25rem (20px) - Section headers
2xl:  1.5rem (24px) - Page headers
3xl:  1.875rem (30px) - Organization name
```

### Font Weights
```
normal:   400 - Body text
medium:   500 - Nav items, labels
semibold: 600 - Card titles
bold:     700 - Headers
```

---

## ✨ Visual Hierarchy

### Level 1: Organization Name
- text-3xl font-bold
- Primary text color
- Most prominent

### Level 2: Section Headers
- text-xl font-semibold  
- Adequate spacing (mt-6 mb-4)

### Level 3: Card Titles
- text-base font-semibold
- Stands out from body

### Level 4: Body Text
- text-base normal
- Gray-700

### Level 5: Meta Info
- text-sm
- Gray-600

### Level 6: Captions
- text-xs
- Gray-500

---

**This visual reference shows exactly what Lovable should generate. Use alongside LOVABLE_PROMPT.md for best results!** 🎨
