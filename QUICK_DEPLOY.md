# ⚡ Quick Vercel Deployment (5 Minutes)

## 🚀 Fastest Method: Vercel Dashboard

### Step 1: Deploy Backend (2 min)

1. Go to: https://vercel.com/new
2. Click **"Import Git Repository"**
3. Select: `Narendra02053/memory-decay`
4. Configure:
   - **Root Directory:** `backend (3)/backend`
   - **Framework Preset:** Other
   - **Build Command:** (leave empty)
   - **Output Directory:** (leave empty)
5. Click **"Deploy"**
6. **Copy the URL** (e.g., `https://memory-decay-backend.vercel.app`)

### Step 2: Deploy Frontend (2 min)

1. Click **"Add New Project"** again
2. Select same repo: `Narendra02053/memory-decay`
3. Configure:
   - **Root Directory:** `frontend (2)/frontend`
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. **Add Environment Variable:**
   - Name: `VITE_API_BASE_URL`
   - Value: `https://your-backend-url.vercel.app` (from Step 1)
5. Click **"Deploy"**

### Done! 🎉

- Frontend: `https://your-frontend.vercel.app`
- Backend: `https://your-backend.vercel.app`
- API Docs: `https://your-backend.vercel.app/docs`

---

## 🔧 Alternative: CLI (Faster if already set up)

```bash
# Install Vercel CLI (one time)
npm install -g vercel

# Deploy Backend
cd "backend (3)/backend"
vercel

# Deploy Frontend (in new terminal)
cd "frontend (2)/frontend"
vercel
# When asked for env vars, add: VITE_API_BASE_URL=https://your-backend-url.vercel.app
```

---

**That's it!** Your app will be live in ~5 minutes.

