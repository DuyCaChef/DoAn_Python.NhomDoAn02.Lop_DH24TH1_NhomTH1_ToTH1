# app/database/connection.py

import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file từ thư mục gốc của project
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(env_path)

def create_connection():
    """ Tạo một kết nối đến database MySQL """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except Error as e:
        print(f"Lỗi '{e}' đã xảy ra khi kết nối đến MySQL")
        return None
