# ✈️ Fly-to-Past (Refactored & Improved)

> **"Taking the legacy 2023 codebase to a modern standard."**

This branch focuses on improving the **Frontend UX**, cleaning up the **Python backend**, and adding modern features to the original 2023 flight management project.

---

## � Current Improvements (v0.2-ux-feedback)

- [x] **Database Migration**: Simplified restoration and schema structure.
- [x] **Port Redirection**: Now running on port **5005** to avoid macOS AirPlay/System conflicts.
- [x] **UI Instruction Boxes**: Added pedagogical guidance on each page.
- [x] **Graceful Error Handling**: Implemented a global exception handler and error.html page.
- [ ] **Modern Frontend**: Replacing archaic HTML/CSS with a cleaner, functional design.

---

## 🛠️ Stack Update
- **Backend**: Python 3.12, Flask 3.0, SQLAlchemy 2.0.
- **Frontend**: Vanilla HTML5, Modern CSS (in progress).
- **Database**: PostgreSQL with properly normalized tables.

---

## 🚀 Getting Started

1. Set up the local environment and restore the database.
2. Install new dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   # Running on http://127.0.0.1:5005
   python3 app.py
   ```

---

## 📅 Roadmap 
1. **Refactor Backend**: Use ORM-style queries (SQLAlchemy) instead of raw strings.
2. **Modernize UI**: Add a responsive navigation bar and cleaner tables.
3. **Data Dashboard**: Create a "Manager Dashboard" for high-level statistics.

---
*Follow the progress as I clean up my student-years code!* 🚀