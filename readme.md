Backend Engineer Assessment - Data Pipeline

This project implements a robust ETL (Extract, Transform, Load) pipeline using a microservices architecture. The goal was to build a system that fetches customer data from a legacy-style API, processes it, and stores it securely in a PostgreSQL database, all containerized with Docker.

🏗 System Architecture
I designed this using three distinct services to mimic a real-world production environment:
- Mock Server (Flask): Acts as the external data source (Legacy API). It serves raw JSON customer data.
- Pipeline Service (FastAPI): The core worker. It ingests data from the Mock Server, cleans/validates it, and upserts (updates/inserts) it into the database.
- Database (PostgreSQL): Persistent storage for the processed customer records.

The Data Flow:
[Flask API] --> (JSON) --> [FastAPI Ingestor] --> (SQLAlchemy) --> [PostgreSQL]

📂 Project Structure
Here is how I organized the code. I split the logic to keep concerns separate—one service for serving data, one for processing it.

Plaintext
Glynac_Backend_Engineer_Assesment/
├── docker-compose.yml       # The glue that runs the whole stack
├── README.md                # You are here!
├── mock-server/             # Service 1: The Source
│   ├── app.py               # Simple Flask app serving JSON
│   ├── data/
│   │   └── customers.json   # The raw "Stranger Things" dataset
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/        # Service 2: The Ingestor
    ├── main.py              # FastAPI entry point & endpoints
    ├── database.py          # DB connection logic
    ├── models/              # SQLAlchemy ORM models
    ├── services/            # Business logic (Ingestion loop)
    ├── Dockerfile
    └── requirements.txt
    
🛠 Tech Stack & Libraries
- FastAPI: The framework used for the main pipeline service. It handles the data ingestion endpoints, processing logic, and communication with the database.
- Flask: The microframework used to run the mock server. It serves the static JSON customer data via a REST API to simulate the external data source.
- SQLAlchemy: The Object Relational Mapper (ORM) used to define database models and handle database sessions, allowing interaction with PostgreSQL using Python classes.
- Psycopg2-binary: The PostgreSQL adapter that enables the Python application to connect to and execute commands against the database.
- Docker & Docker Compose: Containerization tools used to package the applications and orchestrate the multi-container environment (Mock Server, Pipeline Service, and Database) and their networking.

🚀 Getting Started
Prerequisites:
- Docker Desktop (running)
- Git
- (Optional) Python 3.10+ if you want to run it locally without Docker.

Option 1: The "Easy" Way (Docker Compose)
This is the recommended approach. It spins up the Database, the Mock Server, and the Pipeline Service all at once with correct networking.

1. Clone the repo and navigate to the root:
cd Glynac_Backend_Engineer_Assesment

3. Build and run
docker-compose up --build

Option 2: The "Manual" Way (Local Setup)
If you prefer running things locally (or need to debug line-by-line), here is how to set up the environments manually.

1. Setup the Mock Server (Flask)
cd mock-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run it (Runs on port 5000)
python app.py

2. Setup the Pipeline Service (FastAPI)
Note: You will need a local Postgres instance running for this to work without Docker.
cd ../pipeline-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run it (Runs on port 8000)
python main.py

🧪 How to Test
Once the Docker containers are running, you can interact with the system using curl or your browser.

1. Trigger Data Ingestion
This commands the FastAPI service to go fetch data from Flask and save it to the DB.
curl -X POST http://localhost:8000/api/ingest

Expected response:
{"status": "success", 
"records_processed": 25}

2. View Data (Pagination)
Retrieve the data stored in Postgres.
curl "http://localhost:8000/api/customers?page=1&limit=5"

3. Get Single Customer
Retrieve a specific customer by their ID.
curl http://localhost:8000/api/customers/CUST-001

📝 Notes & Gotchas
Docker Networking: I configured docker-compose to use service names as hostnames. For example, FastAPI connects to http://mock-server:5000 internally, not localhost.
Upsert Logic: The ingestion script checks if a customer_id exists. If it does, it updates the record; otherwise, it creates a new one. This prevents duplicates if you run the ingestion multiple times.
The Data: I took the liberty of updating the sample data to a Stranger Things theme 🧇. Enjoy!
