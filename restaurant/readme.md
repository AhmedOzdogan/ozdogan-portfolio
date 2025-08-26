🍽️ Full-Stack Restaurant Application (Django 5 + Django REST Framework)

A full-stack restaurant web application built with Django 5 and Django REST Framework (DRF), designed to demonstrate scalable backend development, clean API design, and responsive frontend implementation. The backend follows RESTful API best practices with structured endpoints for menu management and reservation handling, while the frontend leverages HTML5, CSS3, and JavaScript (vanilla ES6) for a mobile-first, interactive user experience. The project emphasizes clean architecture, database-driven design (SQLite), role-based views, and production-ready static file handling (WhiteNoise) — showcasing skills highly relevant for backend engineers, full-stack developers, and API integration specialists.

## 🛠️ Tech Stack

- **Backend:** Django 5, Django REST Framework
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Database:** SQLite
- **Styling:** Custom CSS, mobile-first responsive design
- **Static Files:** WhiteNoise for production

---

## ✨ Features

- Responsive design for desktop, tablet, and mobile
- Menu browsing with category filters & item detail pages
- Reservation system with creation and booking check
- Custom error pages (`400.html`, `404.html`, `500.html`)
- REST API endpoints for menu & reservations
- Per-app static files for organized assets
- WhiteNoise for static file serving in production

---

## 🗂️ Website Pages

| Path             | Description                      |
| ---------------- | -------------------------------- |
| `/`              | Home                             |
| `/menu/`         | Full menu listing                |
| `/menu/<slug>/`  | Individual menu item details     |
| `/reservations/` | Reservation form & booking check |
| `/about/`        | About the restaurant             |
| `/contact/`      | Contact page                     |

---

## 🔌 API Endpoints

| Method | Endpoint                   | Description                     |
| ------ | -------------------------- | ------------------------------- |
| GET    | `/api/menu/`               | List all menu items             |
| GET    | `/api/menu/<slug>/`        | Retrieve a single menu item     |
| POST   | `/api/reservations/`       | Create a new reservation        |
| POST   | `/api/reservations/check/` | Check reservation by ID & email |

---

## 🧾 Error Pages

- **400** – Bad request (invalid input or missing data)
- **404** – Page not found (missing menu item or wrong URL)
- **500** – Server error

---

## 👤 Superuser Credentials

```plaintext
username: admin
password: admin
```

---

## ⚡ Quick Start

```bash
# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

---

## 📸 Screenshots & Demo

## 📸 Screenshots

Explore the look and feel of the restaurant website with these sample screenshots, showcasing both desktop and mobile experiences. All images are available in the `screenshots/` directory.

| File Name               | Description                                   |
| ----------------------- | --------------------------------------------- |
| `contact.png`           | Contact page with form and restaurant details |
| `about.png`             | About Page                                    |
| `index.png`             | Home page (desktop view)                      |
| `index_(iPhone XR).png` | Home page (mobile view, iPhone XR resolution) |
| `menu.png`              | Full menu page (desktop view)                 |
| `menu_(iPhone XR).png`  | Menu page (mobile view, iPhone XR resolution) |
| `menu-item.png`         | Single menu item detail page                  |
| `menu-api.png`          | Menu API endpoint output (JSON view)          |
| `reservation.png`       | Reservation form page (desktop view)          |
| `reservation-check.png` | Reservation confirmation/check page           |
| `reservations.png`      | Reservations page (Example Reservation)       |

These previews highlight the responsive design and key features, giving you a quick visual tour of the application.

---

Enjoy exploring and customizing your restaurant website!
