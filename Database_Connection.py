
import psycopg2
import os
class Database:

    @staticmethod
    def connection():
        # Connection details
        host = "dpg-d0lo76d6ubrc73c99m40-a.oregon-postgres.render.com"
        database = "bookstoredata"
        user = "vineeth"
        password =  "MR327oC1FEoMX1Njsnfuwzcf2YBNRo1A"
        print(password)
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

