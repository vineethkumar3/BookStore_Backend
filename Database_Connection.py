
import psycopg2
import os
from dotenv import load_dotenv
class Database:
    load_dotenv()
    @staticmethod
    def connection():
        # Connection details
        host = os.getenv("RENDER_DATABASE_HOST")
        database = os.getenv("RENDER_DATABASE_NAME")
        user = os.getenv("RENDER_DATABASE_USER")
        password =  os.getenv("RENDER_DATABASE_PASSWORD")
        port = 5432

        try:
            conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            cursor = conn.cursor()
            return cursor, conn
        except Exception as e:
            print("❌ Error:", e)
            return None, None

    def insert_user(self, name, email, password):
        cursor, conn = self.connection()  # Use self here
        if not cursor or not conn:
            print("⚠️ Connection failed. Cannot insert data.")
            return

        try:
            insert_query = '''
            INSERT INTO employee (name, email, password)
            VALUES (%s, %s, %s);
            '''
            cursor.execute(insert_query, (name, email, password))
            conn.commit()
            print("✅ Data inserted successfully.")
        except Exception as e:
            print("❌ Insert error:", e)
        finally:
            cursor.close()
            conn.close()

    def get_user_by_name(self,email):
        cursor, conn = Database.connection()
        if not cursor or not conn:
            print("⚠️ Connection failed. Cannot fetch data.")
            return None

        try:
            query = "SELECT * FROM employee WHERE email = %s;"
            cursor.execute(query, (email,))
            user = cursor.fetchone()  # fetch one matching row
            if user:
                print("✅ User found:", user)
                return user
            else:
                print("⚠️ No user found with that name.")
                return None
        except Exception as e:
            print("❌ Fetch error:", e)
            return None
        finally:
            cursor.close()
            conn.close()

    def upsert_cart(self, user_id, book_id, quantity):
        cursor, conn = self.connection()
        if not cursor or not conn:
            return
        try:
            query = '''
            INSERT INTO user_cart (user_id, book_id, quantity)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, book_id)
            DO UPDATE SET quantity = EXCLUDED.quantity;
            '''
            cursor.execute(query, (user_id, book_id, quantity))
            conn.commit()
        except Exception as e:
            print("❌ Upsert cart error:", e)
        finally:
            cursor.close()
            conn.close()

    def remove_from_cart(self, user_id, book_id):
        cursor, conn = self.connection()
        if not cursor or not conn:
            return
        try:
            cursor.execute("DELETE FROM user_cart WHERE user_id = %s AND book_id = %s;", (user_id, book_id))
            conn.commit()
        except Exception as e:
            print("❌ Remove cart error:", e)
        finally:
            cursor.close()
            conn.close()

    def get_all_employees(self):
        cursor, conn = self.connection()
        if not cursor or not conn:
            return
        try:
            cursor.execute("SELECT * FROM employee;")
            employees = cursor.fetchall()
            print("👤 Employees:")
            for emp in employees:
                print(emp)
        except Exception as e:
            print("❌ Error fetching employees:", e)
        finally:
            cursor.close()
            conn.close()

    def get_all_user_cart(self):
        cursor, conn = self.connection()
        if not cursor or not conn:
            return
        try:
            cursor.execute("SELECT * FROM user_cart;")
            cart_items = cursor.fetchall()
            print("🛒 User Cart:")
            for item in cart_items:
                print(item)
        except Exception as e:
            print("❌ Error fetching user cart:", e)
        finally:
            cursor.close()
            conn.close()

    def create_otp_table_if_not_exists(self):
        cursor, conn = self.connection()
        if not cursor or not conn:
            print("⚠️ Connection failed. Cannot create OTP table.")
            return

        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookstoreotp (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    otp VARCHAR(6) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            conn.commit()
            print("✅ OTP table checked/created.")
        except Exception as e:
            print("❌ OTP table creation error:", e)
        finally:
            cursor.close()
            conn.close()

    def save_otp(self, email, otp):
        self.create_otp_table_if_not_exists()
        cursor, conn = self.connection()
        if not cursor or not conn:
            print("⚠️ Connection failed. Cannot save OTP.")
            return

        try:
            cursor.execute('''
                INSERT INTO bookstoreotp (email, otp, created_at)
                VALUES (%s, %s, NOW());
            ''', (email, otp))
            conn.commit()
            print("✅ OTP saved.")
        except Exception as e:
            print("❌ Save OTP error:", e)
        finally:
            cursor.close()
            conn.close()

    def verify_otp(self, email, otp):
        cursor, conn = self.connection()
        if not cursor or not conn:
            return False

        try:
            cursor.execute('''
                SELECT created_at FROM bookstoreotp
                WHERE email = %s AND otp = %s
                ORDER BY created_at DESC
                LIMIT 1;
            ''', (email, otp))
            result = cursor.fetchone()

            if result:
                created_at = result[0]
                from datetime import datetime, timedelta
                if datetime.now() - created_at < timedelta(minutes=15):
                    return True
            return False
        except Exception as e:
            print("❌ OTP verification error:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    def cleanup_expired_otps(self):
        self.create_otp_table_if_not_exists()
        cursor, conn = self.connection()
        if not cursor or not conn:
            return

        try:
            cursor.execute('''
                DELETE FROM bookstoreotp
                WHERE created_at < NOW() - INTERVAL '15 minutes';
            ''')
            conn.commit()
            print("🧹 Expired OTPs cleaned.")
        except Exception as e:
            print("❌ Cleanup OTPs error:", e)
        finally:
            cursor.close()
            conn.close()




