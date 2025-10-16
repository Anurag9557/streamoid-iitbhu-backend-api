# Streamoid - CSV Upload Backend (Flask + SQLite)

## Overview
Simple Flask app that:
- Accepts CSV uploads (`POST /upload`)
- Stores validated products into SQLite
- Lists products with pagination (`GET /products`)
- Searches products with filters (`GET /products/search`)
- Given examples using postman see below
- Dockerized solution (See Steps to implement)

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

### Dockerized Format (with link)
- **Method 1 : directly with Docker File and YML**
  
   - Install docker
   - <img width="728" height="42" alt="image" src="https://github.com/user-attachments/assets/adbe7db1-90be-498a-80e8-e9a0f19811fa" />
   
   - This command directly reads Docker File
   - <img width="1042" height="116" alt="image" src="https://github.com/user-attachments/assets/696c2f6f-61a5-495c-8f9e-0af20009563a" />
   
   - Run
     
   - <img width="806" height="197" alt="image" src="https://github.com/user-attachments/assets/ff1674a5-88f6-459b-b78c-8ed13de030a4" />
   
   - The docker image stored locally on device
     
   - <img width="680" height="83" alt="image" src="https://github.com/user-attachments/assets/51b24212-1749-4ce8-872d-17da32891f6c" />
   
- **Method 2 : pull request from Docker**
  - I have already compiled the above first step
  - Pull the docker image and run directly
    
  - <img width="791" height="96" alt="image" src="https://github.com/user-attachments/assets/d4530320-7d17-410d-a0d0-309a96aede7c" />
  
  - docker pull anurag9557/streamoid-backend:latest
    
- **Method 3 : Directly use my tar file nothing rest needed  🙂🙂🙂**
  
  - Link : https://drive.google.com/file/d/1AKUahcWbfMmhjSocM72aSUZno4zfzlkP/view?usp=drive_link
    
  - <img width="1050" height="322" alt="image" src="https://github.com/user-attachments/assets/c1efd307-7bbb-4b23-a561-b260ec01beb4" />
 





