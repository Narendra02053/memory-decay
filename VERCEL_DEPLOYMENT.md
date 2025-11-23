# Vercel Deployment Guide

This guide will help you deploy both the frontend and backend to Vercel.

## 🚀 Quick Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

#### Prerequisites
1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

#### Deploy Backend

1. Navigate to backend directory:
   ```bash
   cd "backend (3)/backend"
   ```

2. Deploy:
   ```bash
   vercel
   ```
   
3. Follow the prompts:
   - Set up and deploy? **Yes**
   - Which scope? **Your account**
   - Link to existing project? **No** (first time) or **Yes** (if redeploying)
   - Project name: **memory-decay-backend**
   - Directory: **./** (current directory)
   - Override settings? **No**

4. Note the deployment URL (e.g., `https://memory-decay-backend.vercel.app`)

#### Deploy Frontend

1. Navigate to frontend directory:
   ```bash
   cd "../../frontend (2)/frontend"
   ```

2. Create `.env.production` file:
   ```env
   VITE_API_BASE_URL=https://your-backend-url.vercel.app
   ```
   Replace `your-backend-url` with your actual backend Vercel URL.

3. Deploy:
   ```bash
   vercel
   ```

4. Follow the prompts (similar to backend)

### Option 2: Deploy via Vercel Dashboard (Easier)

#### Deploy Backend

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your GitHub repository: `Narendra02053/memory-decay`
4. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** `backend (3)/backend`
   - **Build Command:** (leave empty)
   - **Output Directory:** (leave empty)
   - **Install Command:** `pip install -r requirements.txt`
5. Click **"Deploy"**
6. Wait for deployment to complete
7. Copy the deployment URL

#### Deploy Frontend

1. In Vercel Dashboard, click **"Add New Project"** again
2. Import the same repository: `Narendra02053/memory-decay`
3. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend (2)/frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`
4. Add Environment Variable:
   - **Name:** `VITE_API_BASE_URL`
   - **Value:** `https://your-backend-url.vercel.app` (use your backend URL)
5. Click **"Deploy"**

## 📝 Important Notes

### Backend Configuration

- The backend uses FastAPI with serverless functions
- Model files (`.pkl`) are included in the deployment
- MongoDB is optional (works without it)
- File: `backend (3)/backend/vercel.json` contains Vercel configuration

### Frontend Configuration

- Uses Vite for building
- Environment variable `VITE_API_BASE_URL` must point to your backend URL
- File: `frontend (2)/frontend/vercel.json` contains Vercel configuration

### Environment Variables

**Backend (Optional):**
- `MONGO_URI` - MongoDB connection string (optional)
- `DB_NAME` - Database name (optional)

**Frontend (Required):**
- `VITE_API_BASE_URL` - Your backend API URL

## 🔧 Troubleshooting

### Backend Issues

**Problem: Module not found**
- Solution: Ensure `requirements.txt` includes all dependencies
- Check that model files are in `models/` directory

**Problem: Function timeout**
- Solution: Vercel has a 10-second timeout for free tier
- Consider upgrading or optimizing model loading

**Problem: CORS errors**
- Solution: Backend already has CORS configured to allow all origins

### Frontend Issues

**Problem: API calls failing**
- Solution: Check `VITE_API_BASE_URL` environment variable
- Ensure backend URL is correct and includes `https://`

**Problem: Build fails**
- Solution: Check Node.js version (should be 16+)
- Run `npm install` locally first to check for errors

## 🔗 After Deployment

1. **Backend URL:** `https://your-backend-name.vercel.app`
2. **Frontend URL:** `https://your-frontend-name.vercel.app`
3. **API Docs:** `https://your-backend-name.vercel.app/docs`

## 📊 Deployment Status

Check deployment status at:
- [Vercel Dashboard](https://vercel.com/dashboard)
- Each deployment shows logs and status

## 🔄 Updating Deployment

After pushing to GitHub:
- Vercel automatically redeploys (if connected to GitHub)
- Or run `vercel --prod` to deploy manually

## 💡 Tips

1. **Use different project names** for frontend and backend
2. **Set environment variables** in Vercel dashboard
3. **Check deployment logs** if something fails
4. **Test API endpoints** using the `/docs` endpoint
5. **Monitor function execution time** (Vercel free tier has limits)

---

**Need Help?** Check Vercel documentation: https://vercel.com/docs

