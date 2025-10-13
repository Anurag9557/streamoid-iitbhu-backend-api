# Streamoid - CSV Upload Backend (Flask + SQLite)

## Overview
Simple Flask app that:
- Accepts CSV uploads (`POST /upload`)
- Stores validated products into SQLite
- Lists products with pagination (`GET /products`)
- Searches products with filters (`GET /products/search`)
- Given examples using postman see below

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
    
### Examples using postman https://www.postman.com/
- upload
  <img width="1367" height="958" alt="upload_3" src="https://github.com/user-attachments/assets/90967cb1-dfa3-4adb-b4e7-c55198ea65a3" />

- health
  <img width="1408" height="742" alt="health" src="https://github.com/user-attachments/assets/29652b81-8d0d-447b-96f9-3c9414d1a9b9" />

- filter
  <img width="1338" height="936" alt="get_filter" src="https://github.com/user-attachments/assets/bc9115ec-3388-4870-9e73-3a48deaef182" />

- products
  <img width="1351" height="922" alt="get_products" src="https://github.com/user-attachments/assets/8fb003c4-6a50-4d82-ba26-8405a3342b18" />
