# 🍞 Full-Stack Bakery & Restaurant Application

A full-stack bakery & restaurant web application built with Django 5, Django REST Framework, and a vanilla JavaScript frontend.
The app demonstrates scalable backend design with clean APIs, a modern cart and checkout flow, Stripe integration for payments, and a responsive mobile-first frontend.
It highlights role-based views, session persistence for anonymous carts, and an extendable order management system — making it ideal for full-stack and backend-focused developers.

**Tech:** Django 5 · Django REST Framework · Stripe · Vanilla JS

---

A modern, scalable bakery & restaurant web app featuring:

- Clean REST APIs
- Mobile-first responsive frontend
- Stripe-powered checkout
- Role-based views & session persistence
- Extendable order management

---

## 🛠️ Tech Stack

- **Backend:** Django 5, Django REST Framework
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6)
- **Database:** SQLite (default), swappable to PostgreSQL/MySQL
- **Payments:** Stripe (demo/test mode)
- **Auth:** Django Auth (cart persistence for anonymous → authenticated users)
- **Static Files:** WhiteNoise

---

## ✨ Features

- Responsive design (desktop, tablet, mobile)
- Dynamic menu browsing (categories & details)
- **Shopping Cart:**
  - Add items as anonymous user
  - Cart persists & merges after login
- Stripe-powered checkout flow
- User profiles & address management
- Order history & admin status updates
- REST API endpoints for products, addons, cart, orders
- Custom error pages (400, 404, 500)
- Secure session handling & static file optimization

---

## 🗂️ Website Pages

| Path          | Description               |
| ------------- | ------------------------- |
| `/`           | Home page                 |
| `/menu/`      | Menu listing              |
| `/menu/<id>/` | Individual product page   |
| `/cart/`      | Shopping cart detail      |
| `/checkout/`  | Checkout page (Stripe)    |
| `/success/`   | Successful payment page   |
| `/cancel/`    | Payment cancelled page    |
| `/profile/`   | User profile page         |
| `/addresses/` | Manage delivery addresses |
| `/orders/`    | View user orders          |

---

## 🔌 API Endpoints

| Method | Endpoint                              | Description                      |
| ------ | ------------------------------------- | -------------------------------- |
| GET    | `/api/products/`                      | List all products                |
| GET    | `/api/products/<id>/`                 | Retrieve single product          |
| GET    | `/api/addons/`                        | List all addons                  |
| GET    | `/api/addons/category/<id>/`          | Addons filtered by category      |
| POST   | `/cart/add/<product_id>/`             | Add product to cart              |
| POST   | `/cart/update/<item_id>/`             | Update cart item quantity        |
| POST   | `/cart/remove/<item_id>/`             | Remove item from cart            |
| POST   | `/cart/remove_addons/<item_id>/<id>/` | Remove addon from cart item      |
| POST   | `/cart/empty_cart/`                   | Empty the cart                   |
| GET    | `/orders/`                            | List all user orders             |
| POST   | `/orders/update/<order_id>/`          | Update order status (admin only) |

---

## 💳 Stripe Integration

- Test payments via Stripe (demo mode)
- Secure checkout session (Django + Stripe SDK)
- Redirects to success/cancel pages after payment

---

## 👤 Demo Superuser

```
username: admin
password: admin
```

---

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/bakery-app.git
cd bakery-app

# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

---

## 📸 Screenshots & Demo

Explore desktop & mobile screenshots in `screenshots/`:

| File Name            | Description                   |
| -------------------- | ----------------------------- |
| `adresslist.png`     | Address management page       |
| `landing-page.png`   | Main landing page (desktop)   |
| `landing-page2.png`  | Alternate landing page layout |
| `menu.png`           | Menu listing                  |
| `order-customer.png` | Customer order view           |
| `order-manager.png`  | Manager/admin order dashboard |
