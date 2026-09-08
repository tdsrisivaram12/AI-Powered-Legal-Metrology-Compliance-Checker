"""
FastAPI app entrypoint. Run locally with:
    uvicorn services.api.app.main:app --reload --port 8000

This wires together the six services built so far (rules -> compliance ->
evidence -> reports -> search, with notifications fired inline from
compliance). Member 1 (Tech Lead) owns this file; each router stays owned
by the service directory it wraps.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.api.app.api.v1 import compliance, evidence, reports, rules, search

app = FastAPI(
    title="AI-Powered Legal Metrology Compliance Checker API",
    version="0.1.0",
    description="Rules, compliance evaluation, evidence, reports, and search for legal metrology inspections.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rules.router)
app.include_router(compliance.router)
app.include_router(evidence.router)
app.include_router(reports.router)
app.include_router(search.router)


@app.get("/health")
def health():
    return {"status": "ok"}
