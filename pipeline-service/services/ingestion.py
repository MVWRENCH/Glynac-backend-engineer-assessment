import os
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from models.customer import Customer

FLASK_API_URL = os.getenv("FLASK_API_URL", "http://mock-server:5000/api/customers")

def parse_date(date_str):
    if not date_str: return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError: return None

def parse_datetime(dt_str):
    if not dt_str: return None
    try:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError: return None

def fetch_and_upsert_customers(db: Session):
    page = 1
    limit = 100
    total_processed = 0
    
    while True:
        try:
            url = f"{FLASK_API_URL}?page={page}&limit={limit}"
            print(f"Fetching: {url}")
            
            response = requests.get(url)
            if response.status_code != 200: break
            
            data = response.json().get("data", [])
            if not data: break
                
            for item in data:
                customer_data = {
                    "customer_id": item['customer_id'],
                    "first_name": item['first_name'],
                    "last_name": item['last_name'],
                    "email": item['email'],
                    "phone": item.get('phone'),
                    "address": item.get('address'),
                    "date_of_birth": parse_date(item.get('date_of_birth')),
                    "account_balance": item.get('account_balance'),
                    "created_at": parse_datetime(item.get('created_at'))
                }

                existing = db.query(Customer).filter(Customer.customer_id == item['customer_id']).first()
                if existing:
                    for k, v in customer_data.items():
                        setattr(existing, k, v)
                else:
                    db.add(Customer(**customer_data))
            
            db.commit()
            total_processed += len(data)
            page += 1
            
        except Exception as e:
            db.rollback()
            raise e

    return total_processed