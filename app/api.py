from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from auth import verify_api_key, verify_jwt, create_jwt
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import os
from dotenv import load_dotenv
import sys
sys.path.append("/app/scanner")  # ✅ FIX: correct path inside Docker

from scanner.scanner_runner import run_security_scan

load_dotenv()  # allow env vars from Docker / GitHub Actions

APP_API_KEY = os.getenv("APP_API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

if not APP_API_KEY:
    raise RuntimeError("APP_API_KEY is missing")

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is missing")

app = FastAPI()

# =========================
# Prometheus Metrics
# =========================

promptfoo_total_tests = Counter(
    "promptfoo_tests_total",
    "Total Promptfoo tests executed"
)

promptfoo_failed_tests = Counter(
    "promptfoo_tests_failed",
    "Total Promptfoo failed tests"
)

security_gate_status = Gauge(
    "security_gate_status",
    "Security gate result (1=pass, 0=fail)"
)

trivy_high_critical = Gauge(
    "trivy_high_critical_vulns",
    "Number of HIGH/CRITICAL Trivy vulnerabilities"
)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

class LoginRequest(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    prompt: str

@app.post("/login")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "pass123":
        token = create_jwt(data.username)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/chat")
def chat(
    data: ChatRequest,
    api_key: str = Depends(verify_api_key),
    user: str = Depends(verify_jwt)
):
    fake_response = f"[LOCAL LLM] Response to: {data.prompt}"

    scan_result = run_security_scan(data.prompt, fake_response)

    return {
        "user": user,
        "prompt": data.prompt,
        "response": fake_response,
        "security_scan": scan_result,
        "backend": "local-fallback"
    }

