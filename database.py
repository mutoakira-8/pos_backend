import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# 環境変数をロード
load_dotenv()

# MySQL 接続情報を環境変数から取得
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),  # デフォルトポートを3306に設定
}

def get_db_connection():
    """MySQL データベース接続を確立する"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
