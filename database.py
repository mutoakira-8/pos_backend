from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import traceback
from dotenv import load_dotenv

# .env をロード
load_dotenv()

# 環境変数からDB接続情報を取得
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# SSL 証明書のパスを取得（.env に必須設定）
DB_SSL_CERT = os.getenv("DB_SSL_CERT")

# 証明書の存在確認
if not DB_SSL_CERT or not os.path.isfile(DB_SSL_CERT):
    raise FileNotFoundError(f"❌ 指定されたSSL証明書が見つかりません: {DB_SSL_CERT}")

# 環境変数から接続URLを取得（ない場合は手動で作成）
DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_ca={DB_SSL_CERT}")

# SQLAlchemy のエンジンを作成
engine = create_engine(DATABASE_URL)

# DB 接続テスト
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ データベース接続成功")
except Exception as e:
    print(f"❌ データベース接続エラー: {e}")
    print(traceback.format_exc())

# ORM 用の設定
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
