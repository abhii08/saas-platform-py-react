# SaaS Platform Frontend

React-based frontend for the Multi-Tenant SaaS Project Management Platform.

## Features

- JWT-based authentication
- Role-based UI components
- Protected routes
- Responsive design with Tailwind CSS
- Modern UI with Lucide icons

## Tech Stack

- React 18
- React Router v6
- Axios for API calls
- Tailwind CSS
- Vite

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The app will be available at http://localhost:5173

## Project Structure

```
src/
├── api/              # API client configuration
├── components/       # Reusable components
├── context/          # React context providers
├── pages/            # Page components
├── App.jsx           # Main app component
└── main.jsx          # Entry point
```

## Authentication

The app uses JWT tokens stored in localStorage:
- `access_token`: Short-lived token for API requests
- `refresh_token`: Long-lived token for refreshing access
- `user`: User information and role

## Available Routes

- `/login` - Login page
- `/register` - Registration page
- `/dashboard` - Main dashboard (protected)
- `/projects` - Projects list (protected)
- `/projects/:id` - Project details (protected)
- `/tasks` - Tasks view (protected)

## Build for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.
