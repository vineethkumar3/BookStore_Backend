import psycopg2

try:
    # 🔹 Replace these with your AWS details
    connection = psycopg2.connect(
        host="174.129.175.234",       # RDS endpoint OR EC2 public IP/DNS
        database="bookstoredata",    # e.g. postgres
        user="vineeth",       # e.g. postgres
        password="MR327oC1FEoMX1Njsnfuwzcf2YBNRo1A",
        port=5432,                  # default PostgreSQL port
        sslmode="disable"           # use "require" if RDS or if SSL is enabled
    )

    cursor = connection.cursor()
    print("✅ Connected to PostgreSQL on AWS")

    # Example query
    cursor.execute("SELECT version();")
    print("Postgres version:", cursor.fetchone())

    cursor.close()
    connection.close()

except Exception as e:
    print("❌ Error:", e)
