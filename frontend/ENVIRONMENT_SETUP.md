# Environment Setup Guide

## Fix White Screen Issue

The white screen is likely caused by missing Supabase environment variables. Follow these steps to fix it:

### 1. Create Environment File

Create a `.env` file in the `frontend` directory with the following content:

```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

### 2. Get Your Supabase Credentials

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create a new project or select an existing one
3. Go to Settings > API
4. Copy the "Project URL" and "anon public" key
5. Replace the placeholder values in your `.env` file

### 3. Example .env File

```env
VITE_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzNjQ0NjQwMCwiZXhwIjoxOTUyMDIyNDAwfQ.example
```

### 4. Restart Development Server

After creating the `.env` file:

```bash
# Stop the current server (Ctrl+C)
# Then restart it
npm run dev
```

### 5. Alternative: Run Without Supabase

If you want to test the UI without Supabase:

1. The app will now run with placeholder values
2. Authentication features won't work, but the UI will display
3. You can navigate between pages and see the design

### 6. Database Setup

Once you have Supabase configured, run the SQL from `SUPABASE_SETUP.md` in your Supabase SQL editor to set up the database tables.

## Troubleshooting

- **Still white screen?** Check the browser console for errors
- **Environment variables not loading?** Make sure the `.env` file is in the `frontend` directory
- **Vite not picking up changes?** Restart the development server
