# AskMe - Django Q&A App

This is a Django-based Question and Answer web application where users can ask questions, comment on them, reply to comments, and like/dislike responses. It supports basic user authentication and profile management.

---

## 🚀 Setup Instructions

Follow these steps to get the application running on your local machine:

### 1. Clone the Repository

### 2. Activate the Virtual Environment

Make sure to activate the virtual environment already provided in the repo:

```bash
# For Windows
myenv\Scripts\activate

# For macOS/Linux
source myenv/bin/activate
```

### 3. Install the Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Navigate to the Project Directory

```bash
cd askme
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Now, open your browser and go to `http://127.0.0.1:8000/` to view the application.

---

## 🛠 Tech Stack
- **Backend**: Django 5.2
- **Database**: SQLite3
- **Frontend**: HTML, Bootstrap
- **Python**: 3.12.6

---

## 📌 Features
- User registration and login
- Ask questions
- Comment on questions
- Like/unlike comments
- Reply to comments
- Delete your own comments and replies
- User profile page

---
