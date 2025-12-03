from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import datetime

# ================== CONFIG ==================
DB_CONNECTION = (
    "mssql+pyodbc://quangAdmin:Healcare123456@healcare.database.windows.net:1433/HealCareSystem"
    "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection Timeout=30"
)

engine = create_engine(DB_CONNECTION, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ================== MODEL ==================
class ChatMessages(Base):
    __tablename__ = "ChatMessages"

    MessageID = Column(Integer, primary_key=True, index=True)
    SessionID = Column(Integer, index=True)
    Sender = Column(String, nullable=False)   # "user" hoặc "assistant"
    MessageText = Column(String, nullable=False)
    CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)


# ================== UTILS ==================
def normalize_history(history):
    """Đảm bảo history có role xen kẽ user/assistant"""
    fixed = []
    last_role = None
    for msg in history:
        if last_role == msg["role"]:
            # Nếu role trùng với tin trước -> chèn role còn lại rỗng
            if msg["role"] == "user":
                fixed.append({"role": "assistant", "content": ""})
            else:
                fixed.append({"role": "user", "content": ""})
        fixed.append(msg)
        last_role = msg["role"]
    return fixed


def get_latest_history(db: Session):
    """Trả về history đã chuẩn hóa và session_id mới nhất"""

    latest_session = db.query(func.max(ChatMessages.SessionID)).scalar()
    if latest_session is None:
        return [], None

    messages = (
        db.query(ChatMessages)
        .filter(ChatMessages.SessionID == latest_session)
        .order_by(ChatMessages.CreatedAt.asc())
        .all()
    )

    history = []
    for msg in messages:
        # chuẩn hóa role
        role = "user" if msg.Sender.lower() == "user" else "assistant"
        history.append({"role": role, "content": msg.MessageText})

    # Chuẩn hóa để tránh lỗi vLLM
    history = normalize_history(history)
    return history, latest_session
