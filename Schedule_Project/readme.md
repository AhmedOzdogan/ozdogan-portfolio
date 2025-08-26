# 📅 ScheduleV6 — Desktop Teaching Schedule Manager (Python + Tkinter + MySQL)

A desktop teaching schedule manager built for freelance educators to streamline lesson planning, payment tracking, and monthly income management. Developed with Python 3, Tkinter for the user interface, tkcalendar for calendar navigation, and MySQL for persistent data storage, the application combines a clean, interactive GUI with a robust relational database. It supports full CRUD operations, financial reporting, and real-time weekly scheduling, providing a week-at-a-glance timetable, context menus for quick edits, and an integrated finance tracker that automatically calculates salaries and savings. This project demonstrates expertise in Python application development, database-driven design, GUI/UX principles, and financial data management, making it highly relevant for software engineering, backend development, and full-stack roles.

---

## 🗂 Overview

- **Week-at-a-glance timetable** (Mon–Sun):  
   Displays classes with ID, name, school, date/time, rate, and payment status.
- **Calendar widget** for fast navigation.
- **Automatic financial breakdowns**.
- **Context menu** for editing, duplicating, and payment toggling.
- **“Account” module**: Logs monthly savings and computes salaries.

---

## ✨ Key Features

- **Weekly Schedule Grid**
  - Auto-sorting by start time
  - Highlight unpaid classes (`NO !!`)
- **Date Picker (tkcalendar)**
  - Quickly jump to any week
- **Financial Dashboard**
  - Weekly/monthly totals: hours, salary, received vs expected
  - ARC/OEA/private splits and ARC “periods” conversion
- **CRUD Operations**
  - Add, edit, duplicate, delete classes
  - Bulk delete by week
- **Payment Management**
  - Toggle paid/unpaid per class
  - Mark entire months as paid
- **Copy Week Tool**
  - Duplicate a week’s schedule
- **Monthly Income (Account)**
  - Track savings and salaries by month
- **Menus & Shortcuts**
  - File → Connection Settings / Exit
  - Edit → New Class (F1), Copy Classes (F4), Calculate Hours (F10), Account
  - F5 to refresh

---

## 🏗 Architecture & Data

- **Frontend (GUI):** Tkinter Treeview, clam theme, multi-line class cells
- **Calendar:** tkcalendar.Calendar & DateEntry in dialogs
- **Backend (Database):** MySQL (`mysql.connector`)
- **Configuration:** Credentials from local `SQL.txt` (host, user, password, database)

**Database Tables:**

```sql
teaching_schedule(id, class, date, starttime, endtime, school, rate, paid)
account(month, savings, salary)
```

💡 _Financial logic:_  
Rates stored in thousands of VND; totals multiply by 1000 and round. ARC periods converted at 60/35.

---

## ⚙️ Setup

### Requirements

- Python 3.x
- MySQL server & database (see schema below)
- Packages: `mysql-connector-python`, `tkcalendar`, Tkinter (standard)

### Configuration

1. Create `SQL.txt` with host, user, password, database (one per line).
2. Place it in the expected path (or update the code).
3. (Windows) Update optional assets: `icon.ico`, `refresh.png`, `payment.png`, `delete.png`.

### Run

```bash
python ScheduleV6.2.py
```

---

## 🚀 Using the App

- Pick a week via calendar → auto loads Mon–Sun
- F5 refreshes
- F1 adds a class (dialog with spinboxes & DateEntry)
- Right-click for context menu (edit, duplicate, delete, toggle paid/unpaid)
- F4 copies classes between weeks
- F10 calculates hours (filter by year/month/company/school)
- “Account” tracks savings and computed salary

---

## 🖥 UX Details

- Multi-line Treeview rows (ID, class, school, date/time, paid status, rate)
- Highlight unpaid (`NO !!`)
- Standardized dialogs with DateEntry, spinboxes, and comboboxes

---

## 🔒 Security & Portability

- Credentials in plain text → should use env variables or config manager
- Hardcoded Windows paths → make relative for cross-platform support
- All SQL uses parameterized queries (safe from injection)

---

## 🗄 Suggested DB Schema

```sql
CREATE TABLE teaching_schedule (
        id INT AUTO_INCREMENT PRIMARY KEY,
        class VARCHAR(100) NOT NULL,
        date DATE NOT NULL,
        starttime TIME NOT NULL,
        endtime TIME NOT NULL,
        school VARCHAR(100),
        rate INT NOT NULL,      -- thousands of VND
        paid ENUM('yes','no') DEFAULT 'no'
);

CREATE TABLE account (
        id INT AUTO_INCREMENT PRIMARY KEY,
        month TINYINT NOT NULL, -- 1..12
        savings BIGINT DEFAULT 0,
        salary BIGINT DEFAULT 0
);
```

---

## 🛣 Roadmap

- Settings dialog for assets & config
- Export reports (CSV, PDF)
- Per-school rates
- Replace SQL.txt with environment config
- Package executable with PyInstaller

---

## 🆘 Troubleshooting

- Nothing loads: Check SQL.txt & DB connection
- Missing icons: Update/remove image paths
- Totals mismatch: Rates are in thousands of VND

---

## ⌨️ Shortcuts

- F1: New Class
- F4: Copy Classes
- F5: Refresh
- F10: Calculate Hours

---

## 📄 License

Personal/portfolio project.  
Add MIT or another license if distributing.
