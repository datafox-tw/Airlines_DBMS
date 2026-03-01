# 🕰️ Fly-to-Past (Legacy Version)

> **"A journey into my first database management system."**

This is the original version of a project I built in early 2023 when I first started learning Database Management Systems. It was primarily an exercise in **SQL logic**, **Normalization**, and **ER Diagram design**.

---

## 🚩 Project Status: Legacy (Frozen)

This branch preserves the code "as-is" from the original 2023 version. 
⚠️ **The UI/Frontend in this version is primitive** and was not the focus of the initial assignment.

**Interested in the improved version?** Check out the [`refactor-flask`](https://github.com/your-username/Fly-to-Past/tree/refactor-flask) branch for modern updates and a cleaner codebase!

---

## 🛠️ Original Technical Focus
- **PostgreSQL**: Implemented a relational database for an airline system.
- **Normalization**: Applied 3rd Normal Form (3NF) to ensure data integrity.
- **ER Diagram**: Visualized the complex relationships between flights, routes, airports, and tickets.
- **SQL Logic**: Focused on complex queries for flight schedules, maintenance records, and seat availability.

## 🚀 How to Run (Local Setup)

### 1. Database Setup
- Install PostgreSQL.
- Create a database named `airline`.
- Import the provided SQL dump:
  ```bash
  pg_restore -d airline airline_utf8.sql
  ```

### 2. Configure Environment
- Rename `.env.example` (or edit existing `.env`) with your database credentials:
  ```env
  DATABASE_URL=postgresql://your_user:your_password@localhost/airline
  ```

### 3. Run the App
- It is recommended to use a virtual environment:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  python3 app.py
  ```

---

## ⚖️ Sentiment
When looking at this code, please keep in mind that this was a "Hello World" to the world of relational data. It’s messy, it’s raw, but it’s where my journey began! 🚀

---
*Created by [Vincent / BlackWingedKite] in early 2023.*