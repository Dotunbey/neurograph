# 🧠 NeuroGraph

A soon Production-Ready Graph Neural Network platform that visualizes networks in 3D and predicts missing links using PyTorch Geometric.

## 🚀 Deployment Instructions (Render)

### 1. Deploy Backend
1. Create a new **Web Service** on Render.
2. Connect this repo.
3. Root Directory: `backend`
4. Runtime: **Docker**
5. Plan: **Free**
6. **Wait for build.** Copy the URL (e.g., `https://neurograph-api.onrender.com`).

### 2. Configure Frontend
1. Open `frontend/app/page.tsx`.
2. Replace `const API_URL = "http://127.0.0.1:8000"` with your new Render Backend URL.
3. Commit and push changes.

### 3. Deploy Frontend
1. Create a new **Static Site** on Render.
2. Connect this repo.
3. Root Directory: `frontend`
4. Build Command: `npm run build`
5. Publish Directory: `out`
6. Deploy!
