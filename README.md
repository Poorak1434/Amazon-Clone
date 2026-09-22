# Amazon.in Clone - Django Web Application

A full-stack e-commerce clone of **Amazon.in** built with **Django** and Vanilla CSS. It recreates the authentic Amazon India shopping experience, complete with product discovery, search and category filtering, responsive homepage cards, Amazon Buy Box, session & user cart management, checkout with Indian payment methods, and order history tracking.

## 🚀 Features

- **Authentic Amazon.in Header & Navigation**:
  - Signature `#131921` navbar with Amazon India logo.
  - Deliver-to location selector modal ("Deliver to Sonipat 131021").
  - Search bar with category dropdown filter.
  - Cart item count badge.
  - Sub-header (`#232f3e`) with quick links (Rufus, Fresh, Today's Deals, Prime, Coupons, Amazon Pay, Sell, etc.).

- **Homepage & Deals**:
  - Overlapping Great Indian Festival hero banner with bank offer badges.
  - 4-up Grid Cards ("Starting ₹399", "Voice Command Routines", "Up to 30% off Smart Rings", "Samsung Neo QLED TV").
  - Recommended deals carousel with ratings, INR (₹) prices, M.R.P., and discount percentages.

- **Product Catalog & Details**:
  - Filtering by category, price range, Prime eligibility, and star ratings.
  - Product Detail Page (PDP) with high-res image gallery switcher, technical specifications table, customer reviews, and Amazon Buy Box.

- **Cart & Express Checkout**:
  - AJAX Add-to-Cart with dynamic header badge counter update.
  - Free delivery threshold calculator.
  - Shipping address selection & Indian payment options (Amazon Pay UPI, Credit/Debit Card, Net Banking, COD).
  - Authentic Amazon India Order ID generation (`408-XXXXXXX-XXXXXXX`) and order status progression.

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Django 5.x / 6.x
- **Database**: SQLite3
- **Frontend**: HTML5, Vanilla CSS3, JavaScript (ES6+), FontAwesome Icons
- **Testing**: Django `TestCase` unit test suite

## 💻 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Poorak1434/Amazon-Clone.git
cd Amazon-Clone
```

### 2. Set up virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install django pillow
```

### 3. Run database migrations & seed database
```bash
python manage.py migrate
python manage.py seed_db
```

### 4. Run development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## 🧪 Running Tests

```bash
python manage.py test
```

## 📝 License

This project is open source under the MIT License.
