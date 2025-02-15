from sqlalchemy import create_engine, text  # ← text を追加
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# .env をロード
load_dotenv()

# 環境変数からDB接続情報を取得
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# SSL 証明書のパスを環境変数から取得（デフォルトパス: backend/db_control/cert/DigiCertGlobalRootCA.crt.pem）
DB_SSL_CERT = os.getenv("DB_SSL_CERT", os.path.join(os.getcwd(), "db_control", "cert", "DigiCertGlobalRootCA.crt.pem"))

# MySQL 接続 URL (pymysql を使用)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_ca={DB_SSL_CERT}"

# SQLAlchemy のエンジンを作成
engine = create_engine(DATABASE_URL)

# DB 接続テスト
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))  # ← text() を明示的に使用
    print("✅ データベース接続成功")
except Exception as e:
    print(f"❌ データベース接続エラー: {e}")

# ORM 用の設定
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
