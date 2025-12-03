from fastapi import FastAPI, Depends
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
import torch
from translate import translate_text
from filter import check_input
from langdetect import detect  
from sqlalchemy.orm import Session
from db import SessionLocal, get_latest_history

# ========== LOAD MÔ HÌNH LOCAL ==========
model_path = "/home/student/BinhMT_DE170265/app/merged_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto"
)

# ========== FASTAPI APP ==========
app = FastAPI()

origins = [
    "https://localhost:7063",
    "http://127.0.0.1:5000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== DB DEPENDENCY ==========
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Query(BaseModel):
    text: str


@app.post("/generate")
def generate(query: Query, db: Session = Depends(get_db)):

    # 0) Kiểm tra input
    is_valid, msg = check_input(query.text)
    if not is_valid:
        return {"response": msg}

    # 1) Xác định ngôn ngữ
    try:
        lang = detect(query.text)
    except:
        lang = "en"

    # 2) Chuẩn hóa input cho model
    if lang == "vi":
        model_input = translate_text(query.text, "Vietnamese", "English")
    else:
        model_input = query.text

    # 3) Load history từ DB (SessionID mới nhất)
    history, session_id = get_latest_history(db)

    # 4) Thêm message user mới vào history
    history_for_model = history + [{"role": "user", "content": model_input}]

    # ⚠️ Normalize để tránh 2 role liên tiếp giống nhau
    from db import normalize_history
    history_for_model = normalize_history(history_for_model)

    # 5) Build prompt
    system_msg = "Please answer the question concisely and directly. Do not provide unrelated information."

    if hasattr(tokenizer, "apply_chat_template") and getattr(tokenizer, "chat_template", None):
        messages = [{"role": "system", "content": system_msg}] + history_for_model
        prompt_text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    else:
        conversation = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}" for m in history_for_model
        )
        prompt_text = f"[INST] <<SYS>>{system_msg}<</SYS>>\n{conversation} [/INST]"

    # 6) Generate
    inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
        repetition_penalty=1.05
    )

    generated = outputs[0][inputs["input_ids"].shape[-1]:]
    eng_response = tokenizer.decode(generated, skip_special_tokens=True).strip()

    # 7) Log ra console (không lưu vào DB)
    # print(f"SessionID: {session_id}, History: {history_for_model}, AI: {eng_response}")
    # print("history_for_model:", history)

    # 8) Dịch ngược nếu cần
    if lang == "vi":
        final_response = translate_text(eng_response, "English", "Vietnamese")
    else:
        final_response = eng_response

    return {"response": final_response, "lang": lang, "session_id": session_id}
