import json
import os
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Constants
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')

def load_data():
    # load data from JSON define in Constans
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Service health check 
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "flask-mock-server"}), 200

# Get all customers data from JSON with pagination 
@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = load_data()
    
    # Get query parameters
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    
    # Calculate start and end indexes
    start_index = (page - 1) * limit
    end_index = start_index + limit
    
    # Slice the data
    paginated_data = customers[start_index:end_index]
    
    return jsonify({
        "data": paginated_data,
        "total": len(customers),
        "page": page,
        "limit": limit
    })

# Get single customer by ID
@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    customers = load_data()
    
    # Find customer (case-insensitive)
    customer = next((c for c in customers if c['customer_id'] == customer_id), None)
    
    if customer:
        return jsonify(customer)
    else:
        abort(404, description="Customer not found")

if __name__ == '__main__':
    # Running on 0.0.0.0 or for all host for docker
    app.run(host='0.0.0.0', port=5000, debug=True)