from fastapi import FastAPI
from pydantic import BaseModel

from classifier import RuleBasedDifficultyClassifier
from router import route_request

app = FastAPI(title="LLM Cost Optimizer")

classifier = RuleBasedDifficultyClassifier()


class OptimizeRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "LLM Cost Optimizer API"
    }


@app.post("/optimize")
def optimize(request: OptimizeRequest):
    classification = classifier.classify(request.prompt)

    decision = route_request(classification.difficulty)

    return {
        "prompt": request.prompt,
        "difficulty": classification.difficulty.value,
        "confidence": classification.confidence,
        "explanation": classification.explanation,
        "selected_model_tier": decision.model_tier.value,
        "routing_reason": decision.reason,
    }