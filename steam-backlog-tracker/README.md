# Steam Backlog Tracker

AI-powered game recommendation system that helps you decide what to play from your Steam library based on your current mood, available time, and energy level.

## Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python) - Coming soon
- **AI**: LangGraph - Coming soon  
- **Database**: PostgreSQL/Supabase - Coming soon
- **Hosting**: Azure/Vercel - TBD

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. Clone or download this project

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Current Features

✅ Steam-inspired UI with dark theme
✅ Mock game library display
✅ Mood selector (Chill, Focused, Social, Competitive, Story-driven)
✅ Time available selector (15min - 2+ hours)
✅ Energy level selector (Low, Medium, High)
✅ Featured "Perfect Match" recommendation with match score
✅ Game library grid with match percentages

## Coming Soon

- [ ] Steam OAuth integration
- [ ] Real Steam API integration to fetch user library
- [ ] FastAPI backend
- [ ] LangGraph AI recommendation engine
- [ ] PostgreSQL database for user preferences
- [ ] Game metadata caching
- [ ] Recommendation history
- [ ] User preference learning over time

## Project Structure

```
steam-backlog-tracker/
├── app/
│   ├── globals.css          # Global styles with Steam theme
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Main library page
│   └── login/
│       └── page.tsx          # Steam login page
├── package.json
├── tailwind.config.js        # Tailwind with Steam colors
├── tsconfig.json
└── next.config.js
```

## Design Notes

- Color scheme matches Steam's branding (dark blues, light blue accents)
- Glass-morphism effects for modern look
- Hover animations on game cards
- Responsive design for mobile and desktop
- Featured recommendation prominently displayed on landing

## Next Steps

1. Set up FastAPI backend
2. Implement Steam Web API integration
3. Create LangGraph recommendation workflow
4. Set up database schema
5. Connect frontend to backend APIs
