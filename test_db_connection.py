import os
from dotenv import load_dotenv
import mysql.connector

# 環境変数をロード
load_dotenv()

# MySQL 接続テスト
try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )
    print("✅ MySQL 接続成功！")
    conn.close()
except mysql.connector.Error as e:
    print(f"❌ 接続失敗: {e}")
