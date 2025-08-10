# 🍽️ Restaurant Website (Django + DRF)

A sleek, mobile-friendly restaurant website built with **Django 5** and **Django REST Framework**. Visitors can browse the menu, view item details, make reservations, and check bookings — all through a clean, modern interface.

---

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

| Path                  | Description                          |
|-----------------------|--------------------------------------|
| `/`                   | Home                                 |
| `/menu/`              | Full menu listing                    |
| `/menu/<slug>/`       | Individual menu item details         |
| `/reservations/`      | Reservation form & booking check     |
| `/about/`             | About the restaurant                 |
| `/contact/`           | Contact page                         |

---

## 🔌 API Endpoints

| Method | Endpoint                       | Description                                 |
|--------|-------------------------------|---------------------------------------------|
| GET    | `/api/menu/`                  | List all menu items                         |
| GET    | `/api/menu/<slug>/`           | Retrieve a single menu item                 |
| POST   | `/api/reservations/`          | Create a new reservation                    |
| POST   | `/api/reservations/check/`    | Check reservation by ID & email             |

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

- **Home page:** `docs/screens/home.png`
- **Menu grid:** `docs/screens/menu.png`
- **Reservation form:** `docs/screens/reservation.png`
- **Video demo:** `docs/demo.mp4` or [YouTube link](#)

---

Enjoy exploring and customizing your restaurant website!
