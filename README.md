# ✈️ Fly-to-Past (Refactored & Improved)

> **"Taking the legacy 2023 codebase to a modern standard."**

This branch focuses on improving the **Frontend UX**, cleaning up the **Python backend**, and adding modern features to the original 2023 flight management project.

---

## 🔥 Current Improvements (v0.1-refactor)

- [x] **Database Migration**: Simplified restoration and schema structure.
- [x] **Project Structure**: Cleaned up legacy virtual-envs and temporary files.
- [ ] **Modern Frontend**: Replacing archaic HTML/CSS with a cleaner, functional design.
- [ ] **SQL Security**: Implementing parameterized queries to prevent SQL injection (replacing legacy `f-string` queries).
- [ ] **Enhanced Reporting**: Expanding flight scheduling and maintenance logic.

---

## 🛠️ Stack Update
- **Backend**: Python 3.12, Flask 3.0, SQLAlchemy 2.0.
- **Frontend**: Vanilla HTML5, Modern CSS (in progress).
- **Database**: PostgreSQL with properly normalized tables.

---

## 🚀 Getting Started

1. Set up the local environment and restore the database (refer to [`master`](https://github.com/your-username/Fly-to-Past/tree/master/README.md#local-setup) if needed).
2. Install new dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python3 app.py
   ```

---

## 📅 Roadmap 
1. **Refactor Backend**: Use ORM-style queries (SQLAlchemy) instead of raw strings.
2. **Modernize UI**: Add a responsive navigation bar and cleaner tables.
3. **Data Dashboard**: Create a "Manager Dashboard" for high-level statistics.

---
*Follow the progress as I clean up my student-years code!* 🚀