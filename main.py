from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, condecimal, EmailStr
from datetime import date
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# 1) Load your free LLM (here: Llama 2 7B Chat)
MODEL_ID = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",            # automatically picks GPU/CPU
    torch_dtype="auto",           # mixed precision
    load_in_4bit=False,            # quantize to 4-bit (if you install bitsandbytes)
)
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.7
)

app = FastAPI(title="ThankYouFreeLLM API")

class LetterRequest(BaseModel):
    donor_name: str = Field(..., example="Dr. Jane Smith")
    donation_amount: condecimal(decimal_places=2)
    donation_date: date
    currency: str = Field("USD", max_length=3)
    campaign: str
    organization_name: str
    contact_email: EmailStr
    org_represnetative: str
    tone: str = Field("warm", pattern="^(formal|warm|celebratory)$")
    language: str = Field("en", max_length=5)
    letter_length: str = Field("standard", pattern="^(short|standard|detailed)$")
    impact_statements: list[str] = []
    custom_message: str = ""

class LetterResponse(BaseModel):
    letter: str

@app.post("/generate", response_model=LetterResponse)
async def generate_thank_you(req: LetterRequest):
    # build the prompt
    prompt = f"""
You are a professional fundraiser writer. Draft a {req.letter_length} thank-you letter in {req.language}.
Donor: {req.donor_name}
Amount: {req.donation_amount} {req.currency}
Date: {req.donation_date}
Campaign: {req.campaign}
Organization: {req.organization_name}
Contact Email: {req.contact_email}
Tone: {req.tone}
Impact Points: {"; ".join(req.impact_statements) or "none"}
Additional Note: {req.custom_message}
From: {req.org_represnetative}
Include proper IRS tax receipt language: “No goods or services…”
    """.strip()

    try:
        out = generator(prompt)[0]["generated_text"]
        # strip off the prompt echo:
        letter = out[len(prompt):].strip()
        return {"letter": letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/")
async def home():
    return "Hello"
# To run: uvicorn your_module:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level='debug')