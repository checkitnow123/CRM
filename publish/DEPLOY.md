# CheckItNow — publish checklist

## Platform roles

| Platform | Role | When |
|----------|------|------|
| **Render** | Host live demo (`demo/`) | Step 2–3 |
| **Streamlit Cloud** | Landing page + link to demo | Step 4 |
| **Itch.io** | Discovery page + same demo link | Step 5 |
| **Product Hunt** | Launch day traffic | Step 6 (after 1–5 work) |

## Step 2 — GitHub

1. Create repo `checkitnow` on GitHub (public is OK — `airlink/` is gitignored).
2. In PowerShell:

```powershell
cd C:\Users\Jerry\Desktop\Game\checkitnow
git init
git add .
git commit -m "CheckItNow demo + publish landing"
git branch -M main
git remote add origin https://github.com/YOUR_USER/checkitnow.git
git push -u origin main
```

## Step 3 — Render (live demo)

1. https://render.com → Sign up → New **Web Service**
2. Connect GitHub repo `checkitnow`
3. Settings:
   - **Root Directory:** `demo`
   - **Build:** `pip install -r requirements-cloud.txt`
   - **Start:** `python run_cloud.py`
   - **Environment:** add `PUBLIC_DEMO` = `1`
4. Deploy → copy URL (e.g. `https://checkitnow-demo.onrender.com`)

Free tier sleeps after ~15 min idle — first visit may take 30–60s to wake.

## Step 4 — Streamlit landing

1. Edit `publish/streamlit_landing.py` → set `DEMO_URL` to your Render URL
2. https://share.streamlit.io → New app → repo `checkitnow`
3. **Main file path:** `publish/streamlit_landing.py`
4. Deploy → you get `https://YOUR-APP.streamlit.app`

## Step 5 — Itch.io

1. Create project → Category: **Tools**
2. **Kind of project:** Downloadable + link
3. **Embed / link:** your Streamlit landing URL (or Render demo URL)
4. Price: **$0** (demo) or **Name your price**
5. Do **not** upload unsigned EXE as the main download — link to live demo instead.

## Step 6 — Product Hunt

Launch only when you have:

- Working live demo URL
- Landing page URL
- 1–2 screenshots
- Tagline + 2–3 sentence description
- Maker comment ready

Schedule for **Tue–Thu 00:01 PST** for best visibility.
