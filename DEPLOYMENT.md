# Production Deployment Guide

## 🚀 Overview

This guide covers deploying the Meme Generator app to production with Azure services.

## ✅ Pre-Deployment Checklist

### Required Azure Resources
- [ ] Azure OpenAI Service with `gpt-image-1` deployment (DALL-E 3)
- [ ] Azure Content Safety resource
- [ ] Azure App Service or Container Registry (for backend)
- [ ] Azure Static Web Apps or Storage Account (for frontend)
- [ ] Azure Key Vault (recommended for secrets)

### Environment Variables
Ensure all production environment variables are configured:

**Backend (.env)**
```bash
# Required
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your_production_key
AZURE_OPENAI_DEPLOYMENT=gpt-image-1
CONTENT_SAFETY_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
CONTENT_SAFETY_KEY=your_production_key

# Production settings
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend-domain.com
LOG_LEVEL=INFO
```

**Frontend (.env.production)**
```bash
REACT_APP_API_URL=https://your-backend-api.azurewebsites.net
```

---

## 🏗️ Build Process

### 1. Build Frontend

```bash
cd frontend
npm run build
```

**Output**: Optimized static files in `frontend/build/` directory
- Minified JavaScript (~62 KB gzipped)
- Minified CSS (~2 KB gzipped)
- Total size: ~800 KB

### 2. Backend Preparation

The backend is production-ready as-is. Key production features:
- ✅ FastAPI with Uvicorn ASGI server
- ✅ Pydantic validation
- ✅ Async/await for performance
- ✅ Proper error handling
- ✅ CORS configuration
- ✅ Active content safety checks

---

## 📦 Deployment Options

### Option 1: Azure App Service (Recommended)

#### Backend Deployment

1. **Create App Service**
```bash
az webapp create \
  --resource-group trustworthyai \
  --plan meme-backend-plan \
  --name silver-pancake \
  --runtime "PYTHON:3.12"
```

2. **Configure Environment Variables**
```bash
az webapp config appsettings set \
  --resource-group <your-rg> \
  --name <backend-app-name> \
  --settings \
    AZURE_OPENAI_ENDPOINT="..." \
    AZURE_OPENAI_KEY="..." \
    CONTENT_SAFETY_ENDPOINT="..." \
    CONTENT_SAFETY_KEY="..." \
    ENVIRONMENT="production"
```

3. **Deploy Code**
```bash
cd backend
az webapp up \
  --resource-group trustworthyai \
  --name silver-pancake \
  --runtime "PYTHON:3.12"
```

#### Frontend Deployment (Azure Static Web Apps)

1. **Create Static Web App**
```bash
az staticwebapp create \
  --name <frontend-app-name> \
  --resource-group <your-rg> \
  --location "eastus2"
```

2. **Deploy Build**
```bash
cd frontend/build
az staticwebapp deploy \
  --name <frontend-app-name> \
  --resource-group trustworthyai \
  --app-location ./
```

---

### Option 2: Docker Containers

#### Backend Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .

# Run with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Build and Push

```bash
# Build backend image
docker build -t <your-registry>.azurecr.io/meme-backend:latest -f backend/Dockerfile .

# Push to Azure Container Registry
az acr login --name <your-registry>
docker push <your-registry>.azurecr.io/meme-backend:latest

# Deploy to Azure Container Apps
az containerapp create \
  --name meme-backend \
  --resource-group <your-rg> \
  --image <your-registry>.azurecr.io/meme-backend:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars \
    AZURE_OPENAI_ENDPOINT="..." \
    AZURE_OPENAI_KEY="..."
```

---

## 🔒 Security Hardening

### 1. Use Managed Identity (Recommended)

Replace API keys with Azure Managed Identity:

```python
from azure.identity import DefaultAzureCredential

# In your service initialization
credential = DefaultAzureCredential()
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    ),
    api_version="2025-04-01-preview"
)
```

### 2. Azure Key Vault Integration

```bash
# Store secrets in Key Vault
az keyvault secret set \
  --vault-name <your-keyvault> \
  --name AZURE-OPENAI-KEY \
  --value "your_key"

# Reference in App Service
az webapp config appsettings set \
  --name <backend-app-name> \
  --resource-group <your-rg> \
  --settings AZURE_OPENAI_KEY="@Microsoft.KeyVault(SecretUri=https://<vault>.vault.azure.net/secrets/AZURE-OPENAI-KEY/)"
```

### 3. Network Security

- Enable **Private Endpoints** for Azure OpenAI
- Configure **Virtual Network integration** for App Service
- Set up **Azure Front Door** for DDoS protection
- Enable **Application Gateway WAF**

---

## 📊 Monitoring & Observability

### 1. Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app <insights-name> \
  --location eastus2 \
  --resource-group <your-rg>

# Link to App Service
az webapp config appsettings set \
  --name <backend-app-name> \
  --resource-group <your-rg> \
  --settings APPLICATIONINSIGHTS_CONNECTION_STRING="..."
```

### 2. Configure Logging

Update backend to use structured logging:

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
```

### 3. Set Up Alerts

Monitor for:
- High error rates (>5% 5xx responses)
- Content safety rejections (trending up)
- API response times (>2 seconds)
- Azure OpenAI quota exhaustion

---

## 🧪 Production Smoke Tests

After deployment, verify:

### Backend Health Check
```bash
curl https://<backend-url>/health
# Expected: {"status":"healthy","environment":"production"}
```

### Image Generation Test
```bash
curl -X POST https://<backend-url>/api/generate-visual-meme \
  -H "Content-Type: application/json" \
  -d '{"topic":"test","mood":"funny"}' \
  | jq '.message'
# Expected: "Visual meme generated successfully! 🎨"
```

### Content Safety Test
```bash
# Should pass
curl -X POST https://<backend-url>/api/generate-visual-meme \
  -H "Content-Type: application/json" \
  -d '{"topic":"cats","mood":"wholesome"}'
# Expected: HTTP 200 with image

# Should fail (if using unsafe prompt)
curl -X POST https://<backend-url>/api/generate-visual-meme \
  -H "Content-Type: application/json" \
  -d '{"topic":"violent content","mood":"angry"}'
# Expected: HTTP 400 with safety violation
```

### Frontend Test
```bash
# Visit your frontend URL
# Verify:
# - Page loads correctly
# - Can submit meme generation request
# - Images display properly
# - Error handling works
```

---

## 💰 Cost Optimization

### Azure OpenAI
- Monitor token usage in Azure Portal
- Implement rate limiting per user
- Cache common prompts (if applicable)
- Consider quota management

**Estimated Costs**:
- DALL-E 3 (1024x1024): ~$0.04 per image
- 1000 images/day = ~$40/day = ~$1,200/month

### Azure Content Safety
- ~$0.0025 per image analyzed
- 1000 images/day = ~$2.50/day = ~$75/month

### App Service
- Basic B1: ~$13/month
- Standard S1: ~$70/month (recommended for production)

### Static Web Apps
- Free tier available (100 GB bandwidth)
- Standard: ~$9/month (unlimited bandwidth)

**Total Estimated Monthly Cost**: ~$1,350 - $1,400 for 30K images

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Build Frontend
      run: |
        cd frontend
        npm ci
        npm run build
    
    - name: Deploy Frontend to Azure Static Web Apps
      uses: Azure/static-web-apps-deploy@v1
      with:
        azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
        repo_token: ${{ secrets.GITHUB_TOKEN }}
        action: "upload"
        app_location: "frontend/build"
    
    - name: Deploy Backend to Azure App Service
      uses: azure/webapps-deploy@v2
      with:
        app-name: <backend-app-name>
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        package: backend/

### Azure Static Web Apps (using the provided workflow)

This repo includes a preconfigured GitHub Actions workflow located at `.github/workflows/azure-static-web-app.yml`.

1. In the Azure Portal create a Static Web App and connect your GitHub repo (or create the app and copy the deployment token).
2. Add a repository secret named `AZURE_STATIC_WEB_APPS_API_TOKEN` with the deployment token value from Azure.
3. The workflow will build the app from `frontend` and deploy the contents of `frontend/build` automatically on pushes to `main`.

Notes:
- If you create the Static Web App through the Azure Portal it may generate its own workflow. If you prefer to use the portal-generated workflow, compare the artifact path and app location and adjust as needed.
- The workflow expects Node 20 to build the create-react-app-based frontend.
```

---

## 📋 Post-Deployment Tasks

- [ ] Update DNS records
- [ ] Configure custom domain
- [ ] Enable HTTPS (auto with Azure)
- [ ] Set up backup strategy
- [ ] Document runbook for incidents
- [ ] Train team on monitoring dashboards
- [ ] Schedule regular security reviews
- [ ] Plan for scaling (if needed)

---

## 🆘 Rollback Plan

If issues occur:

1. **Azure App Service**: Use deployment slots
```bash
az webapp deployment slot swap \
  --name <backend-app-name> \
  --resource-group <your-rg> \
  --slot staging \
  --target-slot production
```

2. **Static Web Apps**: Redeploy previous version
```bash
az staticwebapp deploy \
  --name <frontend-app-name> \
  --resource-group <your-rg> \
  --app-location ./previous-build
```

3. **Monitor**: Check Application Insights for errors

---

## 📞 Support & Resources

- **Azure OpenAI**: [Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- **Azure Content Safety**: [Documentation](https://learn.microsoft.com/azure/ai-services/content-safety/)
- **FastAPI Deployment**: [Best Practices](https://fastapi.tiangolo.com/deployment/)
- **Azure App Service**: [Documentation](https://learn.microsoft.com/azure/app-service/)

---

## ✅ Production Readiness Checklist

**Code Quality**
- [x] All tests passing
- [x] No security vulnerabilities
- [x] Code reviewed
- [x] Documentation complete

**Infrastructure**
- [ ] Azure resources provisioned
- [ ] Environment variables configured
- [ ] SSL certificates in place
- [ ] Monitoring enabled

**Security**
- [x] Content safety active
- [ ] Managed Identity configured (optional)
- [ ] Key Vault setup (optional)
- [ ] CORS properly configured
- [ ] Rate limiting implemented (recommended)

**Operations**
- [ ] Alerts configured
- [ ] Backup strategy defined
- [ ] Incident response plan
- [ ] Team training complete

---

**Last Updated**: October 9, 2025
**Status**: Ready for Production Deployment 🚀
