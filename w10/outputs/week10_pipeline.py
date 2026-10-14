"""Week 10 reusable pipeline: prompt -> Ollama /api/chat -> JSON validation. Reused in later labs."""
import json
import time
from typing import Literal

import requests
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "qwen2.5:3b"
OPTIONS = {"temperature": 0, "seed": 11523, "num_predict": 100}


def build_prompt(template, text):
    return template.replace("{review_json}", json.dumps(text, ensure_ascii=False))


def ask_llm(text, template, schema, system="Reply with JSON only.", model=MODEL, options=OPTIONS):
    payload = {"model": model, "stream": False, "format": schema, "options": options,
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": build_prompt(template, text)}]}
    start = time.perf_counter()
    try:
        r = requests.post(OLLAMA_URL + "/api/chat", json=payload, timeout=600)
        r.raise_for_status()
        env = r.json()
        return {"raw": env["message"]["content"], "seconds": round(time.perf_counter() - start, 2),
                "model": env.get("model"), "error": ""}
    except Exception as e:
        return {"raw": "", "seconds": None, "model": model, "error": f"{type(e).__name__}: {e}"}


def normalise(s):
    return " ".join(s.lower().split())


class SentimentReply(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: Literal["positive", "negative"]
    evidence: str

    @field_validator("evidence")
    @classmethod
    def evidence_not_empty(cls, v):
        if not v.strip():
            raise ValueError("evidence is empty")
        return v


def validate_reply(raw, source_text, reply_model=SentimentReply):
    out = {"json_valid": False, "schema_valid": False, "data": None, "evidence_present": False, "problem": ""}
    if not raw:
        out["problem"] = "no reply (request failed)"
        return out
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        out["problem"] = "invalid JSON: " + e.msg
        return out
    out["json_valid"] = True
    try:
        reply = reply_model.model_validate(data)
    except ValidationError as e:
        out["problem"] = "schema: " + e.errors()[0]["msg"]
        return out
    out.update(schema_valid=True, data=reply.model_dump())
    evidence = getattr(reply, "evidence", "")
    out["evidence_present"] = bool(evidence) and normalise(evidence) in normalise(source_text)
    if not out["evidence_present"]:
        out["problem"] = "evidence not found in source text"
    return out
