# ClipYantra Frontend

A modern, accessible video editor built with Next.js 14, React 18, TypeScript, and Tailwind CSS.

## Features

- **Next.js 14 App Router** - Server components, streaming, and optimized routing
- **TypeScript** - Strict type checking with path aliases
- **Tailwind CSS** - Design system with CSS variables for theming
- **Zustand** - Lightweight state management with persistence
- **React Hook Form + Zod** - Type-safe form validation
- **Axios** - HTTP client with interceptors and token refresh
- **Framer Motion** - Animation library
- **Lucide React** - Beautiful, consistent icons
- **Accessibility** - WCAG 2.1 AA compliant with focus management

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Auth route group
│   │   ├── login/         # Login page
│   │   └── layout.tsx     # Auth layout
│   ├── (dashboard)/       # Dashboard route group
│   │   ├── editor/        # Video editor pages
│   │   │   └── [projectId]/
│   │   ├── library/       # Media library
│   │   ├── settings/      # User settings
│   │   ├── layout.tsx     # Dashboard layout
│   │   └── page.tsx       # Dashboard home
│   ├── api/               # API routes
│   │   └── health/
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Landing page
├── components/
│   ├── ui/                # Base UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── index.ts
│   ├── shared/            # Shared layout components
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   └── layout.tsx
│   └── features/          # Feature-specific components
│       └── editor/        # Editor components
│           ├── timeline/
│           ├── preview/
│           ├── transcript/
│           └── inspector/
├── hooks/                 # Custom React hooks
├── lib/                   # Utilities and configurations
├── store/                 # Zustand stores
├── types/                 # TypeScript types
├── public/                # Static assets
└── Configuration files
```

## Getting Started

### Prerequisites

- Node.js 20+
- npm 10+ (or pnpm/yarn)

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NEXT_PUBLIC_WS_URL` | WebSocket URL | `ws://localhost:8000` |
| `NEXTAUTH_URL` | NextAuth callback URL | `http://localhost:3000` |
| `NEXTAUTH_SECRET` | NextAuth secret key | Required in production |

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run format` | Format with Prettier |
| `npm run type-check` | Run TypeScript compiler |
| `npm run test` | Run tests |
| `npm run test:watch` | Run tests in watch mode |
| `npm run test:coverage` | Generate coverage report |

## Design System

### Colors

The design system uses CSS variables for theming:

```css
:root {
  --color-brand-500: #3b82f6;
  --color-surface-100: #f3f4f6;
  --color-surface-900: #111827;
  /* ... more colors */
}

.dark {
  --color-surface-100: #1f2937;
  --color-surface-900: #f9fafb;
  /* ... dark mode overrides */
}
```

### Typography

- **Sans**: Inter (UI text)
- **Mono**: JetBrains Mono (code)
- **Display**: Plus Jakarta Sans (headings)

### Spacing & Sizing

- Base unit: 4px (0.25rem)
- Scale: 0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96

### Components

Base components in `components/ui/`:
- `Button` - Multiple variants (primary, secondary, outline, ghost, destructive, link)
- `Input` / `Textarea` / `Select` - Form controls with validation
- `Checkbox` / `RadioGroup` / `Switch` - Input types
- `Card` / `CardHeader` / `CardContent` / `CardFooter` - Content containers
- `StatCard` / `ProjectCard` - Specialized cards

## State Management

### User Store (`store/user-store.ts`)
- Authentication state (user, tokens, session)
- Theme preference
- Notification preferences

### Project Store (`store/project-store.ts`)
- Current project and clips
- Timeline state (tracks, clips, playhead)
- Media library
- Transcript data
- Inspector panel state
- Keyboard shortcuts
- Version history

## Routing

Route groups organize the application:
- `(auth)` - Public pages (login, register)
- `(dashboard)` - Protected pages requiring authentication

## API Client

The Axios client in `lib/api.ts` provides:
- Automatic token attachment
- Token refresh on 401
- Request/response interceptors
- Typed endpoint helpers
- Error handling

## Accessibility

- Semantic HTML5 elements
- ARIA labels and roles
- Focus management
- Keyboard navigation
- Reduced motion support
- High contrast mode
- Screen reader announcements

## Testing

```bash
# Unit tests
npm run test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

## Docker

```bash
# Build image
docker build -t clipyantra-frontend .

# Run container
docker run -p 3000:3000 clipyantra-frontend
```

## Deployment

### Vercel (Recommended)

1. Connect your repository to Vercel
2. Add environment variables
3. Deploy

### Docker

```bash
docker build -t clipyantra-frontend .
docker run -p 3000:3000 --env-file .env.local clipyantra-frontend
```

## Contributing

1. Follow the existing code style
2. Run `npm run lint` and `npm run type-check` before committing
3. Write tests for new features
4. Update documentation as needed

## License

MIT License - see LICENSE file for details.
