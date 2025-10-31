import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    """ Tạo một kết nối đến database MySQL (Hỗ trợ port) """
    connection = None
    try:
        # Lấy port từ .env, nếu không có thì dùng 3306
        db_port = os.getenv("DB_PORT")
        if db_port:
            db_port = int(db_port)
        else:
            db_port = 3306 # Cổng mặc định

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=db_port # THÊM DÒNG NÀY
        )
    except Error as e:
        print(f"LỖI KẾT NỐI: '{e}'")
        raise e 

    return connection