from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from services.ingestion import fetch_and_upsert_customers
from models.customer import Customer

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Upsert customer data from flask server JSON data
@app.post("/api/ingest")
def start_ingestion(db: Session = Depends(get_db)):
    try:
        count = fetch_and_upsert_customers(db)
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all customer from DB with pagination
@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    """
    Return paginated results from database
    """
    skip = (page - 1) * limit
    customers = db.query(Customer).offset(skip).limit(limit).all()
    
    return {
        "data": customers,
        "page": page,
        "limit": limit
    }

# Get single customer by ID from DB
@app.get("/api/customers/{customer_id}")
def get_customer_by_id(customer_id: str, db: Session = Depends(get_db)):
    """
    Return single customer or 404
    """
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    return customer