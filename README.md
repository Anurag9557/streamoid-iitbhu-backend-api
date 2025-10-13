# Streamoid - CSV Upload Backend (Flask + SQLite)

## Overview
Simple Flask app that:
- Accepts CSV uploads (`POST /upload`)
- Stores validated products into SQLite
- Lists products with pagination (`GET /products`)
- Searches products with filters (`GET /products/search`)

## Install
1. Create a virtualenv (recommended)
   python -m venv venv
   venv\Scripts\activate       # windows

2. Install requirements
   pip install -r requirements.txt

3. Run the app
   python app.py
   App listens on http://127.0.0.1:8000

DB file created: `products.db` (SQLite) in project folder.

## API Documentation

### POST /upload
- Form field name: `file` (the CSV file)
- CSV header expected: sku,name,brand,color,size,mrp,price,quantity
- Validation:
  - `sku`, `name`, `brand`, `mrp`, `price` required
  - `price` must be <= `mrp`
  - `quantity` must be >= 0
