from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 環境変数をロード
load_dotenv()

# MySQL接続URLを作成
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 3306)}/{os.getenv('DB_NAME')}"

# SQLAlchemyエンジンの作成
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """SQLAlchemyのセッションを取得する"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
