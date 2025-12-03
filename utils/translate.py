import google.generativeai as genai
import os

# Lấy API key từ biến môi trường hoặc truyền thẳng vào
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyA9fZ47O0DzfFy2szhjoi9bOH-4y3jt-n0")
genai.configure(api_key=API_KEY)

# Hàm dịch: dùng Gemini để dịch text giữa 2 ngôn ngữ
def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    prompt = f"""
    You are a translation engine. 
    Translate the following text from {source_lang} to {target_lang}.
    Only return the translated text, without explanations or additional words.

    Text:
    {text}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")  # có thể đổi sang gemini-1.5-pro nếu muốn
    response = model.generate_content(prompt)
    return response.text.strip()
