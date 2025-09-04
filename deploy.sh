#!/bin/bash

# 🚀 Hotel AI Classifier - Complete Deployment Script
# Run this after creating a GitHub repository

echo "🚀 Deploying Hotel AI Service Classifier to GitHub and Render..."
echo ""

# Check if GitHub repository URL is provided
if [ -z "$1" ]; then
    echo "❌ Please provide your GitHub repository URL"
    echo "Usage: ./deploy.sh https://github.com/YOUR_USERNAME/hotel-classifier.git"
    echo ""
    echo "📝 Steps to create GitHub repo:"
    echo "1. Go to github.com"
    echo "2. Click 'New repository'"
    echo "3. Name it 'hotel-classifier'"
    echo "4. Make it public"
    echo "5. Don't add README, .gitignore, or license"
    echo "6. Copy the repository URL and run this script"
    exit 1
fi

GITHUB_URL=$1

echo "📦 Adding GitHub remote..."
git remote add origin $GITHUB_URL

echo "🔄 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully deployed to GitHub!"
echo ""
echo "🌐 Next Steps for Render Deployment:"
echo "1. Go to https://render.com"
echo "2. Sign up/Login"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Connect your GitHub account"
echo "5. Select your hotel-classifier repository"
echo ""
echo "⚙️ Render Configuration:"
echo "   Name: hotel-classifier-api"
echo "   Environment: Python 3"
echo "   Build Command: pip install -r requirements.txt"
echo "   Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "🔑 Environment Variables to add in Render:"
echo "   MISTRAL_API_KEY = your_mistral_api_key"
echo "   ENVIRONMENT = production"
echo ""
echo "🎯 Your API will be live at: https://hotel-classifier-api.onrender.com"
echo "📚 Documentation: https://hotel-classifier-api.onrender.com/docs"
echo ""
echo "🎉 Deployment Ready! Check DEPLOY_TO_RENDER.md for detailed guide."
