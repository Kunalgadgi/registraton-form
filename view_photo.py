import pymysql
from PIL import Image
import io
from db_config import get_connection  # Assuming this function is defined in db_config.py
def show_user_photo(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT photo FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0]:
            photo_data = result[0]
            image = Image.open(io.BytesIO(photo_data))
            image.show()
        else:
            print("❌ No photo found for this user.")
    except Exception as e:
        print("⚠️ Error:", e)
# Example usage
show_user_photo("your_username_here")