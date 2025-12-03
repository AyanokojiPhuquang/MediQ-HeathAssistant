import re
import base64

# Danh sách từ nhạy cảm (đã encode)
ENCODED_WORDS = [
    "dOG7pWM=", "YuG6rXk=", "bmd1", "Y2jhu61p", "ZnVjaw==", "c2hpdA==", "xJHhu4t0",
    "bOG7k24=", "Y+G6t2M=", "xJHDqW8=", "dsOjaQ==", "xJHhu5Mgbmd1", "xJHhu5MgxJFpw6pu",
    "xJHhu5Mga2jhu5Fu", "xJHhu5MgY2jDsw==", "xJHhu5MgbOG7q2EgxJHhuqNv", "xJHhu5MgeOG6pXU=",
    "xJHhu5MgZOG7kWkgdHLDoQ==", "xJHhu5MgZ2nhuqMgbeG6oW8=", "xJHhu5MgdsO0IGThu6VuZw==",
    "xJHhu5MgdOG7k2kgdOG7hw==", "xJHhu5Mga2jhu5FuIG7huqFu", "xJHhu5MgxJFpw6puIHLhu5M=",
    "xJHhu5Mgbmd1IG5n4buRYw==", "xJHhu5Mgbmd1IHh14bqpbg==", "xJHhu5Mgbmd1IHNp",
    "xJHhu5Mgbmd1IGThu5F0", "xJHhu5Mgbmd1IG5nxqE=", "xJHhu5Mgbmd1IHNpIGThuqFp",
    "dOG7sSB04but", "dOG7sSB24bqrbg==", "Y2jhur90", "Y8OhaSBjaOG6v3Q="
]

# Giải mã base64 -> danh sách từ nhạy cảm
SENSITIVE_WORDS = [base64.b64decode(w).decode("utf-8") for w in ENCODED_WORDS]

def check_input(text: str):
    """
    Kiểm tra input người dùng.
    Nếu chứa từ nhạy cảm -> return (False, message)
    Ngược lại -> return (True, "")
    """
    lower_text = text.lower()
    for word in SENSITIVE_WORDS:
        if re.search(rf"\b{word}\b", lower_text):
            return False, "Câu hỏi có chứa từ ngữ không phù hợp, vui lòng nhập lại."
    return True, ""
