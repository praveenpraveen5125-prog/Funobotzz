from fastapi.testclient import TestClient
from main import app
c = TestClient(app)
def ask(m, **p): return c.post("/api/chat", json={"message": m, "profile": p or {}}).json()
def test_characters(): assert len(c.get("/api/characters").json()) == 12
def test_motor_routes_quacky(): assert "quacky" in ask("How does a robot move?")["characters"]
def test_unsupported(): assert ask("Tell me about Cuby")["notice"] == "no-approved-mapping"
def test_unclear(): assert ask("Teach me something")["notice"] == "clarify"
def test_interest_switch():
    r = ask("How does a motor work?", interest="light"); assert r["state"]["previous_interest"] == "light"
def test_levels(): assert ask("explain deeper about circuits", level="beginner")["level"] == "advanced"
def test_quiz(): assert c.get("/api/quiz/motor").status_code == 200
