import os, re
import httpx
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from knowledge import CHARACTERS, CONCEPTS, FACTS, INTEREST_OF, QUIZ

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)
LAST_ERR = {"msg": None}
app = FastAPI(title="Funobotz STEM Buddy")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","), allow_methods=["*"], allow_headers=["*"])

class Profile(BaseModel):
    age: int = Field(10, ge=4, le=18)
    interest: str = "open"
    level: str = "beginner"      # beginner | intermediate | advanced
    style: str = "story"         # story | short | detailed | experiment
class ChatReq(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    profile: Profile = Profile()
    character: str = "petalo"
    history: list[dict] = []
    previous_interest: str | None = None

def route(msg: str):
    m = msg.lower()
    named = [k for k, c in CHARACTERS.items() if c["name"].lower() in m]
    scores = {c: sum(bool(re.search(r"\b" + re.escape(k), m)) for k in kw[0]) for c, kw in CONCEPTS.items()}
    best = max(scores, key=scores.get)
    return named, (best if scores[best] else None)

def level_for(p: Profile, msg: str):
    lv = p.level
    if re.search(r"deeper|more detail|explain more|advanced|how exactly", msg.lower()): lv = "advanced"
    if re.search(r"don't understand|confus|too hard|simpler|easy", msg.lower()): lv = "beginner"
    return lv

def gemini(system, history, msg):
    key = (os.getenv("GEMINI_API_KEY") or "").strip().strip('"').strip("'")
    if not key:
        LAST_ERR["msg"] = "AQ.Ab8RN6KIlqpKyQLrBsclWrxIm-9nznqIeDSW4OExeDQ6q1nHpQ"
    first = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    contents = [{"role": "user" if h.get("role") == "user" else "model", "parts": [{"text": str(h.get("text", ""))[:500]}]} for h in req_hist(history)]
    contents.append({"role": "user", "parts": [{"text": msg}]})
    body = {"systemInstruction": {"parts": [{"text": system}]}, "contents": contents,
            "generationConfig": {"maxOutputTokens": 600, "temperature": 0.7}}
    for model in dict.fromkeys([first, "gemini-2.0-flash", "gemini-flash-latest"]):
        try:
            r = httpx.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                           headers={"x-goog-api-key": key}, timeout=30, json=body)
            if r.status_code != 200:
                LAST_ERR["msg"] = f"{model}: HTTP {r.status_code} {r.text[:160]}"; continue
            LAST_ERR["msg"] = None
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            LAST_ERR["msg"] = f"{model}: {type(e).__name__} {e}"
    return None
def req_hist(h): return h[-8:]

def system_prompt(p: Profile, lead, chars, concept, level):
    kn = "\n".join(f"- {CHARACTERS[c]['name']}: {CHARACTERS[c]['behaviour']} Approved topics: {', '.join(CHARACTERS[c]['topics'])}" for c in chars)
    return f"""You are {CHARACTERS[lead]['name']}, a Funobotz STEM learning friend (personality: {CHARACTERS[lead]['personality']}).
Learner: age {p.age}, interest {p.interest}, level {level}, style {p.style}. Current concept: {concept}.
APPROVED CHARACTER KNOWLEDGE (the ONLY source for character facts):
{kn}
Approved explanation to base your answer on: {FACTS.get(concept, {}).get(level, '')}
Rules: use short, simple, fun sentences with 1-2 emojis; match age and level; use a {p.style} style (story = tiny story, experiment = think-and-observe idea, short = 2 sentences, detailed = a bit more).
Answer the child's actual question with a relatable real-world example. Mention other relevant approved characters when useful.
NEVER invent facts about any Funobotz character beyond the approved knowledge; if unsure say you don't know yet. Never give build instructions or unsafe experiments. Never ask for personal info (name, address, phone, school).
Always end with one friendly question to check understanding. Max 90 words."""

@app.get("/api/health")
def health(): return {"ok": True, "key_loaded": bool((os.getenv("GEMINI_API_KEY") or "").strip()), "ai": "gemini" if os.getenv("GEMINI_API_KEY") else "demo-mode", "last_error": LAST_ERR["msg"]}

@app.get("/api/characters")
def characters(): return [{"id": k, **v} for k, v in CHARACTERS.items()]

@app.get("/api/quiz/{concept}")
def quiz(concept: str):
    if concept not in QUIZ: raise HTTPException(404, "No approved quiz for this topic yet")
    return [{"q": q, "options": o, "answer": a, "why": w} for q, o, a, w in QUIZ[concept]]

@app.post("/api/chat")
def chat(req: ChatReq):
    p, msg = req.profile, req.message.strip()
    named, concept = route(msg)
    state = {"interest": p.interest, "previous_interest": req.previous_interest, "character": req.character}
    approved = [k for k, c in CHARACTERS.items() if c["topics"]]
    # Unsupported character mapping
    unsupported = [n for n in named if not CHARACTERS[n]["topics"]]
    if unsupported and not concept:
        c = CHARACTERS[unsupported[0]]
        said = f"{c['name']}: {c['behaviour']} " if c["behaviour"] else ""
        reply = (f"{c['emoji']} {said}I don't have more learning facts about {c['name']} yet, and I won't make things up! "
                 f"But I can teach you with Petalo (light), Quacky (motors), Tolly (timers) or Tiko (moving tails). Which one?")
        return dict(reply=reply, demo=False, characters=[unsupported[0]], concept=None, state=state,
                    suggestions=["Tell me about Petalo","How does Quacky move?","What does Tolly do?"], notice="no-approved-mapping")
    # Open-ended question: let Gemini answer any kid-safe STEM question, else ask to pick a topic
    if not concept and not named:
        sysmsg = (f"You are Funobotz STEM Buddy, a friendly guide for a child aged {p.age} (level {p.level}, style {p.style}). "
                  "Answer the child's question simply in under 80 words with a fun real-world example and 1-2 emojis. "
                  "If it is not kid-safe, gently steer to STEM. Do NOT make any claims about Funobotz characters. "
                  "Never ask for personal information. End with one question to check understanding. "
                  "If relevant you may say Petalo (light), Quacky or Tiko (motors) or Tolly (timer lights) can explore related ideas.")
        text = gemini(sysmsg, req.history, msg)
        if text:
            return dict(reply=text, demo=False, characters=[], concept=None, state=state, ai_error=None,
                        suggestions=["Explain deeper","Tell me a story about it","How does a robot move?"], notice="open-question")
        return dict(reply="🌟 Great curiosity! Let's pick something to explore: light, moving robots, or lights that change in order?",
                    demo=True, characters=["petalo","quacky","tolly"], concept=None, state=state, ai_error=LAST_ERR["msg"],
                    suggestions=["How does light work?","How does a robot move?","How do traffic lights change?"], notice="clarify")
    concept = concept or (CHARACTERS[named[0]]["topics"][0] if named and CHARACTERS[named[0]]["topics"] else "light")
    # Interest switching (no session restart)
    new_int = INTEREST_OF.get(concept, p.interest)
    if p.interest not in ("open", new_int):
        state["previous_interest"], state["interest"] = p.interest, new_int
    elif p.interest == "open":
        state["interest"] = new_int
    p.interest = state["interest"]
    chars = [c for c in CONCEPTS[concept][1] if CHARACTERS[c]["topics"]]
    lead = named[0] if named and named[0] in chars else (req.character if req.character in chars else chars[0])
    state["character"] = lead
    level = level_for(p, msg)
    text = gemini(system_prompt(p, lead, chars, concept, level), req.history, msg)
    demo = text is None
    if demo:
        others = [CHARACTERS[c]["name"] for c in chars if c != lead]
        text = f"{CHARACTERS[lead]['emoji']} {FACTS[concept][level]}" + (f" 🤝 {', '.join(others)} can help with this too!" if others else "") + " Does that make sense?"
    return dict(reply=text, demo=demo, characters=chars, concept=concept, state=state, level=level, ai_error=LAST_ERR["msg"] if demo else None,
                suggestions=[f"Quiz me on {concept}", "Explain deeper", "Tell me a story about it"] if concept in QUIZ else ["Explain deeper", "Tell me a story about it"], notice=None)

FRONT = Path(__file__).resolve().parent.parent / "frontend"
@app.get("/")
def index(): return FileResponse(FRONT / "index.html")
app.mount("/static", StaticFiles(directory=FRONT), name="static")
