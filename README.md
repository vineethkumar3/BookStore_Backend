
# 📚 BookStore Backend

A lightweight Flask-based backend API for managing an online bookstore. This application handles user data, database interactions, and session management, serving as the backend counterpart to the [BookStore\_Frontend](https://github.com/vineethkumar3/BookStore_Frontend) project.

---

## 🚀 Features

* **Flask Framework**: Utilizes Flask for building RESTful APIs.
* **Database Integration**: Manages database connections and operations through `Database_Connection.py`.
* **Session Management**: Handles user sessions using `flask_session`.
* **User Data Handling**: Stores and manages user information via `users.json`.
* **Modular Design**: Organized codebase with clear separation of concerns.

---

## 🛠️ Technologies Used

* **Python 3.x**
* **Flask**
* **Flask-Session**
* **SQLite** (or another database as configured in `Database_Connection.py`)([YouTube][1])

---

## 📁 Project Structure

```plaintext
├── .env                         # Environment variables (e.g., secret keys, DB URIs)
├── app.py                       # Main Flask application
├── app_backup.py                # Backup of the main application
├── Database_Connection.py       # Database connection and operations
├── Database_connection_test.py  # Script to test database connectivity
├── flask_session/               # Session management configurations
├── requirements.txt             # Python dependencies
├── users.json                   # Sample user data
├── .github/workflows/           # GitHub Actions workflows (if any)
├── .idea/                       # IDE-specific settings (e.g., for PyCharm)
```



---

## ⚙️ Setup Instructions

### Prerequisites

* Python 3.x installed on your machine.
* `pip` package manager.

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/vineethkumar3/BookStore_Backend.git
   cd BookStore_Backend
   ```



2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```



3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```



4. **Configure Environment Variables**

   Create a `.env` file in the root directory and add necessary configurations:

   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   DATABASE_URI=sqlite:///bookstore.db  # Or your preferred database URI
   ```



5. **Initialize the Database**

   Ensure that the database is set up correctly. If using SQLite, the database file will be created automatically. For other databases, ensure that the connection details in `Database_Connection.py` are accurate.

6. **Run the Application**

   ```bash
   flask run
   ```



The application will be accessible at `http://localhost:5000/`.

---

## 🧪 Testing Database Connection

To verify that the database connection is functioning correctly, run:

```bash
python Database_connection_test.py
```



This script will attempt to connect to the database and perform basic operations to ensure connectivity.([amitshekhar.me][2])

---

## 📄 API Endpoints

While specific API routes are defined within `app.py`, typical endpoints might include:

* `GET /users`
* `POST /users`
* `GET /books`
* `POST /books`
* `PUT /books/<id>`
* `DELETE /books/<id>`([amitshekhar.me][2])

For detailed information on each endpoint, refer to the route definitions in `app.py`.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to enhance the project, please fork the repository and submit a pull request. For significant changes, consider opening an issue first to discuss your proposed modifications.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

Feel free to customize this `README.md` further to align with any additional features or specific configurations present in your project.

[1]: https://www.youtube.com/watch?v=D_4V2wnCkyQ&utm_source=chatgpt.com "Book Store Management System | Spring Boot Angular Project Tutorial ..."
[2]: https://amitshekhar.me/blog/go-backend-clean-architecture?utm_source=chatgpt.com "Go Backend Clean Architecture"
