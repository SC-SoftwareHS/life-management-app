# UX Wireframes
## AI-Assisted Life Management Application

**Version:** 1.0 MVP (API-First, Frontend TBD)
**Date:** 2025-10-16

---

## Note
Since this is an API-first MVP, these wireframes represent the **future frontend** that will consume the API. They serve as a design reference for:
- Frontend developers in Phase 2
- Understanding user flows and data display
- API response structure planning

---

## 1. Dashboard / Home

```
┌─────────────────────────────────────────────────────────────┐
│  Life Management App                     [User] [Logout]    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Daily Check-In                                      │   │
│  │  ☐ Morning meditation (Spiritual)                   │   │
│  │  ☐ Log food intake (Physical/Health)                │   │
│  │  ☐ 30 min yoga (Physical/Health)                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌───────────────────┬───────────────────┬──────────────┐  │
│  │ 💪 Physical      │ 🎨 Hobby         │ 💰 Income    │  │
│  │ 3 goals          │ 2 goals          │ 1 goal       │  │
│  │ 4 habits         │ 1 habit          │ 5 tasks      │  │
│  ├───────────────────┼───────────────────┼──────────────┤  │
│  │ 🏦 Assets        │ 💑 One-on-One    │ 👨‍👩‍👧‍👦 Family  │  │
│  │ 2 accounts       │ 3 conflicts      │ 8 contacts   │  │
│  │ 1 goal           │ 1 goal           │ 2 goals      │  │
│  ├───────────────────┼───────────────────┼──────────────┤  │
│  │ 🗳️ Politics       │ 🙏 Spiritual     │              │  │
│  │ 2 references     │ 5 habits         │              │  │
│  │ 1 task           │ 3 goals          │              │  │
│  └───────────────────┴───────────────────┴──────────────┘  │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📅 Upcoming                                         │   │
│  │  • Mom's birthday in 17 days (Nov 2)                │   │
│  │  • Schedule annual checkup (due Oct 20) [HIGH]      │   │
│  │  • Q4 savings goal review (due Oct 31)              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Life Area Detail (Physical/Health Example)

```
┌─────────────────────────────────────────────────────────────┐
│  ← Dashboard                           💪 Physical / Health  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  💡 AI Insight                                       │   │
│  │  "Philippians 4:13 - I can do all things through    │   │
│  │   Christ who strengthens me."                        │   │
│  │                                                       │   │
│  │  Consider setting a consistent bedtime to improve    │   │
│  │  sleep quality and energy levels.                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  [Goals] [Habits] [Tasks] [Health Catalog] [Journal]       │
│  ═══════                                                    │
│                                                              │
│  Goals (3)                                    [+ New Goal]   │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 🎯 Run 5K in under 30 minutes          [45%] ■■■■□□  │ │
│  │    Short-term • Due: Dec 31, 2025                    │ │
│  │    Status: In Progress                                │ │
│  │    [Edit] [Delete]                                    │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ 🎯 Lose 15 pounds                      [20%] ■□□□□□  │ │
│  │    Medium-term • Due: Mar 31, 2026                   │ │
│  │    Status: In Progress                                │ │
│  │    Contact: Dr. Sarah Johnson                        │ │
│  │    [Edit] [Delete]                                    │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ 🎯 Complete first marathon             [0%]  □□□□□□  │ │
│  │    Long-term • Due: Dec 31, 2026                     │ │
│  │    Status: Not Started                                │ │
│  │    [Edit] [Delete]                                    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Habits Tab

```
┌─────────────────────────────────────────────────────────────┐
│  💪 Physical / Health         [Goals] [Habits] [Tasks]...   │
│                                       ════════               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Habits (4)                                  [+ New Habit]   │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ ✅ Morning yoga (30 min)                              │ │
│  │    Type: Gain • Frequency: Daily                      │ │
│  │    Streak: 🔥 12 days (Longest: 30)                   │ │
│  │    Last check-in: Today                               │ │
│  │    [Check In] [Edit] [Delete]                         │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ ✅ Track calories                                     │ │
│  │    Type: Gain • Frequency: Daily                      │ │
│  │    Streak: 🔥 5 days (Longest: 14)                    │ │
│  │    Last check-in: Yesterday                           │ │
│  │    [Check In] [Edit] [Delete]                         │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ 🚫 Quit late-night snacking                           │ │
│  │    Type: Lose • Frequency: Daily                      │ │
│  │    Streak: 🔥 8 days (Longest: 8)                     │ │
│  │    Last check-in: Today                               │ │
│  │    [Check In] [Edit] [Delete]                         │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ ✅ 10,000 steps                                       │ │
│  │    Type: Gain • Frequency: 5x per week                │ │
│  │    Streak: 🔥 3 days (Longest: 21)                    │ │
│  │    Last check-in: 2 days ago                          │ │
│  │    [Check In] [Edit] [Delete]                         │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Health Catalog Tab

```
┌─────────────────────────────────────────────────────────────┐
│  💪 Physical / Health                  [Health Catalog]      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Doctors] [Food] [Supplements] [Medications] [Motion]      │
│   ════════                                                   │
│                                                              │
│  Doctors (2)                              [+ New Doctor]     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Dr. Sarah Johnson                                     │ │
│  │ Specialty: Primary Care                               │ │
│  │ Phone: 555-0123                                        │ │
│  │ Email: sjohnson@clinic.com                            │ │
│  │ Notes: Accepts Blue Cross insurance                   │ │
│  │ [Edit] [Delete]                                        │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ Dr. Michael Chen                                      │ │
│  │ Specialty: Cardiology                                 │ │
│  │ Phone: 555-0456                                        │ │
│  │ [Edit] [Delete]                                        │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  Switch to [Supplements] tab:                                │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Vitamin D3                                            │ │
│  │ Dosage: 2000 IU                                        │ │
│  │ Frequency: Daily with breakfast                       │ │
│  │ Notes: Take with fatty meal for absorption            │ │
│  │ [Edit] [Delete]                                        │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Family & Friends - Birthdays

```
┌─────────────────────────────────────────────────────────────┐
│  👨‍👩‍👧‍👦 Family & Friends                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Contacts] [Birthdays] [Goals] [Habits]                    │
│              ══════════                                      │
│                                                              │
│  Upcoming Birthdays (Next 30 Days)                          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Mom                                                   │ │
│  │ Birthday: November 2, 1965                             │ │
│  │ Age: 59 years, 11 months, 14 days                     │ │
│  │ 📅 17 days away                                         │ │
│  │ Phone: 555-1234 | Email: mom@family.com               │ │
│  │ [View Contact] [Send Message]                         │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ Sarah (Sister)                                        │ │
│  │ Birthday: November 15, 1988                            │ │
│  │ Age: 36 years, 11 months, 1 day                       │ │
│  │ 📅 30 days away                                         │ │
│  │ [View Contact]                                         │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  All Contacts (8)                        [+ New Contact]     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Dad • Birthday: Aug 10 • 555-1235                     │ │
│  │ Brother • Birthday: Jan 22 • 555-9876                 │ │
│  │ Best Friend Alex • Birthday: Mar 5 • 555-4321         │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. One-on-One - Conflict Topics

```
┌─────────────────────────────────────────────────────────────┐
│  💑 One-on-One Relationship                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  💡 AI Insight                                       │   │
│  │  "Ephesians 4:2-3 - Be completely humble and gentle;│   │
│  │   be patient, bearing with one another in love."    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  [Conflict Topics] [Goals] [Entries]                        │
│   ════════════════                                          │
│                                                              │
│  3 Main Argument Topics                  [+ Add Topic]       │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. Household chores division                          │ │
│  │    Description: Disagreement on who does what         │ │
│  │                                                         │ │
│  │    💡 Resolution Strategy:                             │ │
│  │    Create weekly rotation chart together, review      │ │
│  │    every Sunday evening                                │ │
│  │                                                         │ │
│  │    📝 Progress Notes:                                  │ │
│  │    Chart implemented 2 weeks ago. Seeing improvement,  │ │
│  │    fewer arguments. Need to stick with it.            │ │
│  │                                                         │ │
│  │    Last updated: Oct 10, 2025                         │ │
│  │    [Edit] [Delete]                                     │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ 2. Financial planning differences                     │ │
│  │    Description: Different comfort levels with spending│ │
│  │                                                         │ │
│  │    💡 Resolution Strategy:                             │ │
│  │    Monthly budget meeting, agree on "fun money"       │ │
│  │    allowance for each person                          │ │
│  │                                                         │ │
│  │    [Edit] [Delete]                                     │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ 3. Quality time vs. personal space                    │ │
│  │    Description: Balancing together-time and alone-time│ │
│  │                                                         │ │
│  │    💡 Resolution Strategy:                             │ │
│  │    TBD - discussing potential approaches              │ │
│  │                                                         │ │
│  │    [Edit] [Delete]                                     │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Politics/Civics - References

```
┌─────────────────────────────────────────────────────────────┐
│  🗳️ Politics / Civics                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [References] [Goals] [Tasks] [Entries]                     │
│   ══════════                                                 │
│                                                              │
│  Filter by: [All] [Federal] [State] [Local] [Websites]     │
│                    ════════                                  │
│                                                              │
│  Federal Laws & References (3)            [+ Add Reference]  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Affordable Care Act (ACA)                             │ │
│  │ Type: Federal Law                                      │ │
│  │ Summary: Key provisions on health insurance...        │ │
│  │ Tags: healthcare, insurance                           │ │
│  │ [View Details] [Edit] [Delete]                        │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ Congress.gov                                          │ │
│  │ Type: Website                                          │ │
│  │ URL: https://congress.gov                             │ │
│  │ Notes: Track federal legislation                      │ │
│  │ [Visit] [Edit] [Delete]                               │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  State Laws (California) (2)                                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ CA Prop 13 (Property Tax Limitations)                 │ │
│  │ Type: State Law                                        │ │
│  │ [View Details] [Edit] [Delete]                        │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Create/Edit Goal Modal

```
┌─────────────────────────────────────────────────────────────┐
│  Create New Goal                                       [X]   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Title: *                                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Run 5K in under 30 minutes                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Description:                                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Build up running endurance and speed through         │  │
│  │ structured training plan                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Timeframe: *        Due Date:                              │
│  [Short ▾]           ┌────────────┐                         │
│                      │ 2025-12-31 │                         │
│                      └────────────┘                         │
│                                                              │
│  Life Areas: * (select one or more)                         │
│  ☑ Physical/Health   ☐ Hobby        ☐ Income/Expenses      │
│  ☐ Assets            ☐ One-on-One   ☐ Family & Friends     │
│  ☐ Politics          ☐ Spiritual                            │
│                                                              │
│  Related Contact: (optional)                                │
│  [Select Contact ▾]                                         │
│                                                              │
│  Initial Progress:                                           │
│  ┌─────────┐ %                                              │
│  │    0    │                                                 │
│  └─────────┘                                                │
│                                                              │
│                             [Cancel]  [Create Goal]          │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. Financial Dashboard (Assets & Liabilities)

```
┌─────────────────────────────────────────────────────────────┐
│  🏦 Assets & Liabilities                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Net Worth Summary                                           │
│  ┌───────────────────┬───────────────────┬──────────────┐  │
│  │ Total Assets      │ Total Liabilities │ Net Worth    │  │
│  │ $425,420.50       │ -$295,000.00      │ $130,420.50  │  │
│  └───────────────────┴───────────────────┴──────────────┘  │
│                                                              │
│  [Banking] [Assets] [Liabilities] [Goals]                   │
│   ════════                                                   │
│                                                              │
│  Banking Accounts (2)                    [+ Add Account]     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Chase Checking (...4567)                              │ │
│  │ Current Balance: $5,420.50                             │ │
│  │ [Edit] [Delete]                                        │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ Ally Savings (...8901)                                │ │
│  │ Current Balance: $35,000.00                            │ │
│  │ [Edit] [Delete]                                        │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  Switch to [Assets] tab:                                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Home (Property) - Wells Fargo Mortgage                │ │
│  │ Est. Value: $500,000 (Equity: $215,000)               │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ 401(k) - Vanguard                                     │ │
│  │ Balance: $185,000.00                                   │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Mobile Responsive (Future)

```
┌───────────────────┐
│ ☰  Life Mgmt App │
├───────────────────┤
│                   │
│ Daily Check-In    │
│ ☐ Meditation      │
│ ☐ Yoga            │
│ ☐ Track food      │
│                   │
│ ─────────────────│
│                   │
│ Life Areas:       │
│                   │
│ 💪 Physical       │
│ 3 goals, 4 habits │
│ [View →]          │
│                   │
│ 🎨 Hobby          │
│ 2 goals, 1 habit  │
│ [View →]          │
│                   │
│ 💰 Income         │
│ 1 goal, 5 tasks   │
│ [View →]          │
│                   │
│ ... (scroll down) │
│                   │
│ ─────────────────│
│                   │
│ 📅 Upcoming       │
│ • Mom's birthday  │
│   in 17 days      │
│ • Annual checkup  │
│   due Oct 20      │
│                   │
└───────────────────┘
```

---

## Design Principles

1. **Clarity:** Clear hierarchy, obvious actions
2. **Consistency:** Repeated patterns across areas
3. **Feedback:** Immediate visual confirmation of actions
4. **Progress Visibility:** Streaks, percentages, counts
5. **AI Integration:** Inspirational content prominently displayed
6. **Accessibility:** High contrast, keyboard navigation, screen reader support
7. **Mobile-First:** Responsive design for all screen sizes

---

## Interaction Patterns

- **Check-in:** Single click/tap to record habit completion
- **Drag & Drop:** Reorder tasks, goals (future enhancement)
- **Inline Editing:** Click to edit fields directly (future)
- **Modals:** For create/edit forms
- **Filters:** Dropdowns and toggles
- **Toast Notifications:** Success/error messages
- **Loading States:** Spinners during API calls

---

## Future Enhancements
- Dark mode toggle
- Customizable dashboard widgets
- Charts/graphs for trends
- Reminders and notifications
- Calendar view
- Search functionality
- Keyboard shortcuts
- Drag-and-drop task management
- Rich text editor for entries
