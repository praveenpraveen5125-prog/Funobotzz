# 🤖 Funobotz STEM Buddy

A personalized STEM learning chatbot where official Funobotz characters teach kids, powered by Google Gemini. Character facts come only from approved data (`backend/knowledge.py`), so the bot never invents facts about a character.

## Features
- Setup by age, interest, level and learning style (no private data collected)
- Character routing (e.g. motors → Quacky + Tiko), multi-character answers
- Interest switching mid-chat, adaptive difficulty ("explain deeper")
- Gemini answers for any kid-safe STEM question; labelled Demo mode without a key
- Quiz, progress tracking, voice input/output
- Safe handling for characters without released STEM content

## Project structure
```
funobotz/
├── backend/   main.py (FastAPI + Gemini), knowledge.py (approved data), test_api.py
├── frontend/  index.html (served by the backend)
├── render.yaml, .gitignore, .env.example
```

## Run locally
```bash
cd backend
python -m pip install -r requirements.txt
cp .env.example .env        # Windows: copy .env.example .env
# edit .env  ->  GEMINI_API_KEY=your_key   (free: https://aistudio.google.com/app/apikey)
python -m uvicorn main:app --reload
```
Open http://127.0.0.1:8000 (the backend serves the frontend). Check http://127.0.0.1:8000/api/health → `"ai":"gemini"`.
Tests: `python -m pytest`

## Publish to GitHub
1. Create a free account at github.com, then **New repository** → name `funobotz-stem-buddy` → Public → Create (do not add README).
2. Make sure `.gitignore` is in the project root. **Never upload your real `.env` / API key.**
3. In the project root terminal:
```bash
git init
git add .
git status            # confirm .env is NOT listed
git commit -m "Funobotz STEM Buddy"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/funobotz-stem-buddy.git
git push -u origin main
```
4. If push asks for a password, use a Personal Access Token (GitHub → Settings → Developer settings → Tokens).

## Host it free on Render (public link)
1. Go to render.com → sign up with GitHub.
2. **New → Web Service** → pick your `funobotz-stem-buddy` repo.
3. Settings (auto-filled if `render.yaml` is detected):
   - Runtime: Python 3
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Plan: Free
4. **Environment** → add `GEMINI_API_KEY` = your key (also `PYTHON_VERSION` = `3.12.3`).
5. Click **Create Web Service**. After 2–5 minutes you get `https://funobotz-stem-buddy.onrender.com`.
6. Open `/api/health` on that link to confirm Gemini is active.
Note: the free plan sleeps after inactivity, so the first load can take ~50 seconds.

To update: `git add . && git commit -m "update" && git push` and Render redeploys automatically.

## Embed on another website
```html
<iframe src="https://YOUR-APP.onrender.com/" style="width:420px;height:640px;border:0;border-radius:20px"></iframe>
```

## Add approved characters / topics
Edit `CHARACTERS`, `CONCEPTS`, `FACTS` in `backend/knowledge.py` (set `status="approved"` and fill `topics`).

## API
`POST /api/chat` · `GET /api/characters` · `GET /api/quiz/{topic}` · `GET /api/health`

## Safety & privacy
Only age, interest, level and style are used; progress stays in the browser. The API key lives in environment variables only. The AI is told never to ask for personal information or give unsafe instructions.

## Troubleshooting
- `uvicorn not recognized` → use `python -m uvicorn ...`
- Demo mode label → key missing/invalid; check `/api/health` and the error under the answer
- `.env` not loading → file must be named exactly `.env` (not `.env.txt`)
