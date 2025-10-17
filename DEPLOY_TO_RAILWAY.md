# Deploy to Railway.app - Complete Guide

## 🚀 Quick Deploy (5 Minutes)

Railway is **100% FREE** for your MVP and hosts both frontend + backend together!

### Step 1: Sign Up for Railway

1. Go to https://railway.app
2. Click "Login" → Sign in with GitHub
3. Authorize Railway to access your GitHub

### Step 2: Deploy from GitHub

1. Click "New Project"
2. Click "Deploy from GitHub repo"
3. Select your repository: `SC-SoftwareHS/life-management-app`
4. Railway will automatically detect it's a Python app!

### Step 3: Add Environment Variable

After deployment starts:

1. Click on your project
2. Go to "Variables" tab
3. Click "+ New Variable"
4. Add:
   ```
   Name: APP_SECRET
   Value: (click "Generate" to create a random secret)
   ```
5. Click "Add"

### Step 4: Wait for Deployment (2-3 minutes)

Railway will:
- ✅ Install Python dependencies
- ✅ Create database
- ✅ Start your server
- ✅ Generate a public URL

### Step 5: Access Your App!

Once deployed, Railway gives you a URL like:
```
https://life-management-app-production.up.railway.app
```

**Your app will be live at:**
- Frontend: `https://your-app.railway.app/static/index.html`
- API Docs: `https://your-app.railway.app/docs`
- Health Check: `https://your-app.railway.app/health`

## ✅ What's Already Configured

I've already created these files for Railway:

- ✅ `railway.json` - Railway configuration
- ✅ `Procfile` - Start command
- ✅ `runtime.txt` - Python version
- ✅ `server/requirements.txt` - Dependencies
- ✅ Frontend files ready in `/frontend`

**Everything is ready to deploy!**

## 🎯 Alternative: One-Click Deploy Button

You can also use this button (after committing):

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/SC-SoftwareHS/life-management-app)

## 🔧 Post-Deployment Configuration

### Update Frontend API URL (Optional)

If you want to use a custom domain:

1. In Railway, go to Settings → Domains
2. Add your custom domain
3. Update `frontend/js/config.js`:
   ```javascript
   API_URL_PRODUCTION: 'https://your-custom-domain.com'
   ```

### Enable HTTPS (Already Done!)

Railway automatically provides HTTPS. No configuration needed!

## 💰 Free Tier Limits

Railway's free tier includes:
- ✅ **500 hours/month** - More than enough for MVP
- ✅ **100GB outbound bandwidth**
- ✅ **Automatic HTTPS**
- ✅ **Unlimited builds**
- ✅ **GitHub auto-deploy**

**This is FREE forever** for small projects like yours!

## 🎉 After Deployment

Once deployed, share this with your neighbor:

**Your App URL:**
```
https://your-app-name.up.railway.app/static/index.html
```

They can:
1. Register for an account
2. Login and see their dashboard
3. Explore the 8 life areas
4. Use the full API at `/docs`

## 🐛 Troubleshooting

### Build Failed?
- Check Railway logs for errors
- Make sure `APP_SECRET` is set in Variables

### App Won't Start?
- Verify `requirements.txt` is in `/server` directory
- Check Railway logs (click "Deployments" → "View Logs")

### Frontend Not Loading?
- Visit: `https://your-app.railway.app/static/index.html`
- Note: Must include `/static/` in the URL

### Database Issues?
- Railway automatically handles SQLite
- Data persists between deployments
- For production, consider upgrading to PostgreSQL (still free on Railway)

## 📊 Monitoring Your App

In Railway dashboard you can see:
- Real-time logs
- CPU and memory usage
- Deployment history
- Custom metrics

## 🔄 Auto-Deploy on Git Push

Railway automatically re-deploys when you push to GitHub!

```bash
git add .
git commit -m "Update feature"
git push
```

Railway will automatically:
1. Detect the push
2. Build the new version
3. Deploy it (zero downtime)

## 🎯 Next Steps After Deployment

1. **Test the app** - Register an account, try features
2. **Share with neighbor** - Send them the URL
3. **Gather feedback** - See what they think
4. **Iterate** - Add more features based on feedback

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Your GitHub: https://github.com/SC-SoftwareHS/life-management-app

---

🚂 Ready to deploy? Just push to GitHub and follow the steps above!

**Estimated time: 5 minutes** ⏱️
**Cost: $0** 💰
**Difficulty: Easy** ⭐

Let's go! 🚀
