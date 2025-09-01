# HealthMate Deployment Guide for Render

## 🚀 Deploy to Render Free Tier

### Prerequisites
- GitHub repository with your HealthMate code
- Pinecone API key
- Groq API key
- Medical PDF documents uploaded to Pinecone

### Step 1: Prepare Your Repository

1. **Ensure all files are committed to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Verify these files exist in your repository:**
   - `app.py`
   - `requirements.txt`
   - `render.yaml` (created automatically)
   - `runtime.txt`
   - `Procfile`
   - `templates/chat.html`
   - `static/style.css`
   - `src/` folder with helper.py and prompt.py

### Step 2: Deploy to Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Click "New +" and select "Web Service"**

3. **Connect your GitHub repository**

4. **Configure the service:**
   - **Name:** `healthmate-ai`
   - **Environment:** `Python`
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

5. **Add Environment Variables:**
   - `PINECONE_API_KEY` = Your Pinecone API key
   - `GROQ_API_KEY` = Your Groq API key

6. **Click "Create Web Service"**

### Step 3: Monitor Deployment

1. **Watch the build logs** for any errors
2. **Check the health endpoint:** `https://your-app-name.onrender.com/health`
3. **Test the application:** `https://your-app-name.onrender.com/`

### ⚠️ Important Considerations for Free Tier

#### Limitations:
- **512 MB RAM** - Limited memory for large models
- **0.1 CPU** - Slower processing
- **Sleep after 15 minutes** - Service goes to sleep when inactive
- **750 hours/month** - Usage limits

#### Optimizations Made:
1. **Lazy Loading** - Components initialize only when needed
2. **Memory Management** - Garbage collection after each request
3. **Reduced Model Parameters** - Optimized for free tier constraints
4. **Health Check Endpoint** - For monitoring service status

### 🔧 Troubleshooting

#### Common Issues:

1. **Build Fails:**
   - Check requirements.txt for version conflicts
   - Ensure all dependencies are compatible

2. **Memory Issues:**
   - The app uses lazy loading to minimize memory usage
   - Consider upgrading to paid tier for better performance

3. **Cold Start Delays:**
   - First request after sleep may take 30-60 seconds
   - Subsequent requests will be faster

4. **API Key Errors:**
   - Verify environment variables are set correctly
   - Check API key permissions and quotas

#### Performance Tips:
- Keep your Pinecone index small and optimized
- Use efficient prompts to reduce token usage
- Monitor Groq API usage to stay within limits

### 📊 Monitoring

1. **Health Check:** `/health` endpoint returns service status
2. **Render Dashboard:** Monitor logs, performance, and errors
3. **API Usage:** Track Groq and Pinecone consumption

### 🔄 Updates

To update your deployment:
1. Push changes to GitHub
2. Render will automatically redeploy
3. Monitor the build logs for any issues

### 💰 Cost Management

Free tier includes:
- 750 hours/month
- 512 MB RAM
- 0.1 CPU
- Automatic sleep after inactivity

For production use, consider upgrading to paid plans for:
- Better performance
- No sleep mode
- More resources
- Custom domains

### 🎉 Success Indicators

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ Health check returns 200 OK
- ✅ Chat interface loads properly
- ✅ AI responses work correctly
- ✅ No memory or timeout errors

### 📞 Support

If you encounter issues:
1. Check Render documentation
2. Review build logs for errors
3. Verify environment variables
4. Test locally before deploying
