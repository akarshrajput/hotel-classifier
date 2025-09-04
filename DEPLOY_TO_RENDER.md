# 🚀 Deploy Hotel Service Classifier to Render (FREE)

## Step-by-Step Deployment Guide (0 to 100%)

### 📋 Prerequisites
- GitHub account
- Render account (free at render.com)
- Your Mistral AI API key

### 🛠️ Step 1: Initialize Git Repository

```bash
# Navigate to your project
cd /Users/akarshrajput/Documents/guestflowmvp-model

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Hotel AI Service Classifier"
```

### 🔗 Step 2: Push to GitHub

```bash
# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/hotel-classifier.git
git branch -M main
git push -u origin main
```

### 🌐 Step 3: Deploy on Render

1. **Go to Render.com** → Sign up/Login
2. **Click "New +"** → Select "Web Service"
3. **Connect GitHub** → Select your repository
4. **Configure Service:**
   - **Name:** `hotel-classifier-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 🔑 Step 4: Set Environment Variables

In Render Dashboard → Environment:
```
MISTRAL_API_KEY = your_actual_mistral_api_key_here
ENVIRONMENT = production
LOG_LEVEL = info
```

### ✅ Step 5: Deploy!

- Click **"Create Web Service"**
- Wait 3-5 minutes for deployment
- Your API will be live at: `https://your-service-name.onrender.com`

### 🧪 Step 6: Test Your Live API

```bash
# Test health endpoint
curl https://your-service-name.onrender.com/health

# Test classification
curl -X POST "https://your-service-name.onrender.com/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "guest_message": "I need coffee and my room is not clean",
    "guest_id": "G001",
    "room_number": "101"
  }'
```

### 📚 API Documentation

Your live docs will be available at:
- Interactive Docs: `https://your-service-name.onrender.com/docs`
- ReDoc: `https://your-service-name.onrender.com/redoc`

## 🎯 What You Get (FREE)

✅ **Live Hotel AI Classifier API**  
✅ **Auto-scaling (sleeps after 15min idle)**  
✅ **HTTPS SSL Certificate**  
✅ **Custom Domain Support**  
✅ **Automatic Deployments from GitHub**  
✅ **Build & Deploy Logs**  
✅ **Environment Variables Management**

## 🚨 Important Notes

- **Free Tier Limits:** Service sleeps after 15 min of inactivity
- **Cold Start:** First request after sleep takes ~30 seconds
- **Usage:** 750 hours/month free (enough for development)
- **Mistral API:** Make sure you have credits in your Mistral account

## 🔄 Auto-Deploy Setup

Any push to your GitHub main branch will automatically redeploy your service!

```bash
# Make changes
git add .
git commit -m "Update AI classifier"
git push

# Render automatically redeploys! 🚀
```

Your hotel AI service will be **LIVE** and ready for production use!
