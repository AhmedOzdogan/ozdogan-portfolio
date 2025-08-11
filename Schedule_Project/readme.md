# ScheduleV6 — Desktop Teaching Schedule Manager

A desktop app for freelance teachers to plan weekly lessons, track payments, and manage simple monthly finances.  
_Built with Python, Tkinter, tkcalendar, and MySQL._

---

## 🗂 Overview

ScheduleV6 displays a week-at-a-glance grid (Mon–Sun), listing classes for each day (ID, class, school, date/time, rate, paid status), powered by a MySQL backend.  
A side calendar lets you jump weeks quickly; totals and money breakdowns update automatically.  
Right-click any class for a context menu with edit, duplicate, and payment shortcuts.  
A small “Account” window logs monthly savings and auto-computes salary from scheduled classes.

---

## ✨ Key Features

- **Weekly schedule grid**  
    Auto-grouping and sorting by start time. Unpaid classes highlighted (e.g., `NO !!`).

- **Date picker**  
    Quickly jump to any week using tkcalendar.

- **Totals panel**  
    Weekly/monthly hours, salary, received vs expected; ARC/OEA/private hour splits; ARC “periods” conversion (35-minute periods).

- **CRUD operations**  
    - Add class (dialog with date + time spinboxes)
    - Edit class (dialog, updates DB)
    - Duplicate class (dialog)
    - Delete by class or bulk delete by week (with confirmation)

- **Payment management**  
    Toggle paid/unpaid per class; mark all classes in a month as paid.

- **Copy Week tool**  
    Select classes from a week and copy to the same weekdays of another week.

- **Monthly Income (Account)**  
    Table of months, savings, computed salary; update buttons for savings and salary.

- **Menus & Shortcuts**  
    - File → Connection Settings / Exit  
    - Edit → New Class (F1), Copy Classes (F4), Calculate Hours (F10), Account  
    - F5 refreshes the current week

---

## 🏗 Architecture & Data

- **GUI:** Tkinter Treeview for weekly grid, themed with clam, larger row height for multi-line class cells.
- **Calendar:** tkcalendar.Calendar + DateEntry in dialogs.
- **Database:** MySQL (via `mysql.connector`). Credentials read from local `SQL.txt` (host, user, password, database).
- **Tables:**
    - `teaching_schedule(id, class, date, starttime, endtime, school, rate, paid)`
    - `account(month, savings, salary)`

💡 _Salary math:_ Money rates are in thousands of VND; totals multiply by 1000 and round up for display. ARC “periods” convert from hours at 60/35, then displayed in hours again by reversing the factor.

---

## ⚙️ Setup

### Requirements

- Python 3.x
- MySQL server & database with the two tables above
- Packages: `mysql-connector-python`, `tkcalendar`, Tkinter (standard)

### Configuration

1. Create `SQL.txt` with 4 lines: host, user, password, database.
2. Place it where the app expects, or update the path.
3. _(Windows)_ Optional icon and button images: update paths for `icon.ico`, `refresh.png`, `payment.png`, `delete.png`.

### Run

```bash
python ScheduleV6.2.py
```

The main window appears centered with a fixed size; the week table and calendar load immediately.

---

## 🚀 Using the App

- **Pick a date:** Use the left calendar; app computes Monday–Sunday range and loads classes for that week.
- **Refresh:** F5 or the refresh button.
- **Add a class:** Edit → New Class (F1), fill fields, Submit.
- **Right-click a class:** Details, Delete, Edit, Duplicate, mark Un/Paid.
- **Copy Classes:** Edit → Copy Classes (F4), “Get Classes”, select or “Select All”, “Copy”.
- **Calculate Hours:** Edit → Calculate Hours (F10), choose Year/Month/Company/School → Calculate.
- **Account (Monthly Income):** Edit → Account, pick month, update Savings or compute Salary from schedule.

---

## 🖥 UX Details

- Row height & multi-line cells show ID, class, school, date/time, paid, and rate in one cell.
- Visual cues for unpaid (`NO !!`).
- Dialogs reuse DateEntry and time spinboxes; paid state edited via combobox.

---

## 🔒 Security & Portability Notes

- Credentials in plain text (`SQL.txt`) — consider environment variables or a secure config store.
- Hard-coded Windows paths for icon/images — make these relative or configurable for cross-platform use.
- Parameterized queries used throughout (good against SQL injection).

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
    rate INT NOT NULL,      -- in 'thousands of VND'
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

## 🛣 Roadmap Ideas

- Make asset/config paths relative; add a settings dialog to pick icon/images.
- Export weekly/monthly reports (CSV/PDF).
- Role-based schools/clients; separate rates per school or class type.
- Replace plain-text `SQL.txt` with env-based config.
- Package as a standalone executable (PyInstaller) for non-technical users.

---

## 🆘 Troubleshooting

- **Nothing loads:** Verify `SQL.txt` (host/user/pass/db) and DB connectivity.
- **Icons/buttons missing:** Update image paths or remove image-based buttons.
- **Totals look odd:** Rates are multiplied by 1000 for VND; ensure your rate is set to “thousands of VND”.

---

## ⌨️ Shortcuts & Menus

- **F1:** New Class
- **F4:** Copy Classes
- **F5:** Refresh
- **F10:** Calculate Hours

_File:_ Connection Settings / Exit  
_Edit:_ New Class, Copy, Calculate Hours, Account

---

## 📄 License

Personal/portfolio project.  
_Add a license (e.g., MIT) if you plan to distribute._