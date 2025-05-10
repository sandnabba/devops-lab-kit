import os
from flask import Flask, request, jsonify, Response
# Import db instance, init_db function, and Inventory model from database.py
from database import db, init_db, Inventory, Pastebin
from flask_cors import CORS # Import CORS
# Import text for raw SQL execution in health check
from sqlalchemy import text
from datetime import datetime, timedelta
import uuid

# --- Configuration ---
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

app = Flask(__name__, instance_path=instance_path)
CORS(app) # Enable CORS for all routes

# --- Database Configuration ---
# To switch to MySQL later, you would change this URI.
# Example MySQL URI (requires mysqlclient or PyMySQL):
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@host/db_name'
# Consider using environment variables for sensitive info like passwords.
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Initialize Database ---
# Call the init_db function to bind db to the app and create tables
init_db(app)

# --- Route Definitions ---
# Routes remain largely the same, but ensure they use the imported 'db' and 'Inventory'
@app.route('/database/', methods=['GET'])
def get_inventory():
    print("Received GET request to fetch inventory.")
    try:
        # Use the imported Inventory model
        items = Inventory.query.all()
        print(f"Fetched items: {[item.to_dict() for item in items]}")
        return jsonify([item.to_dict() for item in items])
    except Exception as e:
        print(f"Error fetching inventory: {e}")
        app.logger.error(f"Error fetching inventory: {e}")
        return jsonify({"error": "Failed to fetch inventory"}), 500

@app.route('/database/', methods=['POST'])
def add_item():
    print("Received POST request to add item.")
    try:
        data = request.json
        if not data or 'name' not in data or 'quantity' not in data or 'price' not in data:
             print(f"Invalid data received: {data}")
             return jsonify({"error": "Missing required fields (name, quantity, price)"}), 400
        print(f"Request data: {data}")
        # Use the imported Inventory model and db instance
        new_item = Inventory(name=data['name'], quantity=data['quantity'], price=data['price'])
        db.session.add(new_item)
        db.session.commit()
        print(f"Item added to database: {new_item.to_dict()}")
        return jsonify(new_item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding item: {e}")
        app.logger.error(f"Error adding item: {e}")
        return jsonify({"error": "Failed to add item"}), 500

@app.route('/database/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    print(f"Received PUT request for item ID: {item_id}")
    try:
        data = request.json
        if not data:
            print("No data provided for update.")
            return jsonify({"error": "No data provided"}), 400
        print(f"Request data: {data}")
        # Use the imported Inventory model and db instance
        item = db.session.get(Inventory, item_id)
        if not item:
            print(f"Item with ID {item_id} not found.")
            return jsonify({"error": "Item not found"}), 404

        item.name = data.get('name', item.name)
        item.quantity = data.get('quantity', item.quantity)
        item.price = data.get('price', item.price)
        db.session.commit()
        print(f"Item updated: {item.to_dict()}")
        return jsonify(item.to_dict())
    except Exception as e:
        db.session.rollback()
        print(f"Error updating item {item_id}: {e}")
        app.logger.error(f"Error updating item {item_id}: {e}")
        return jsonify({"error": "Failed to update item"}), 500

@app.route('/database/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    print(f"Received DELETE request for item ID: {item_id}")
    try:
        # Use the imported Inventory model and db instance
        item = db.session.get(Inventory, item_id)
        if not item:
            print(f"Item with ID {item_id} not found.")
            return jsonify({"error": "Item not found"}), 404

        db.session.delete(item)
        db.session.commit()
        print(f"Item deleted: ID {item_id}")
        return jsonify({"message": "Item deleted"})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting item {item_id}: {e}")
        app.logger.error(f"Error deleting item {item_id}: {e}")
        return jsonify({"error": "Failed to delete item"}), 500

@app.route('/environment', methods=['GET'])
def get_environment():
    """Returns all environment variables available to the process."""
    print("Received GET request for environment.")
    try:
        environment = dict(os.environ)  # Get all environment variables as a dictionary
        print(f"Environment details: {environment}")
        return jsonify(environment), 200
    except Exception as e:
        print(f"Error fetching environment details: {e}")
        app.logger.error(f"Error fetching environment details: {e}")
        return jsonify({"error": "Failed to fetch environment details"}), 500

@app.route('/healthcheck', methods=['GET'])
def health_check():
    """Checks the health of the application, including database connectivity and table access."""
    print("Received GET request for health check.")
    db_status = "disconnected"
    db_error = None
    try:
        # Perform a query against the tables to ensure they exist and are accessible
        db.session.query(Inventory.id).count()
        db.session.query(Pastebin.id).count()
        db_status = "connected_and_tables_accessible"
        print("Database connection and table access check successful.")
        return jsonify({"status": "ok", "database": db_status}), 200
    except Exception as e:
        db_error = str(e)
        # Differentiate between general connection errors and table-specific errors
        if "no such table" in db_error.lower():
            db_status = "connected_tables_missing"
            print(f"Database connection okay, but tables are missing: {db_error}")
            app.logger.error(f"Health check failed - tables missing: {db_error}")
        else:
            db_status = "connection_error"
            print(f"Database connection check failed: {db_error}")
            app.logger.error(f"Health check failed - database connection error: {db_error}")

        return jsonify({
            "status": "error",
            "database": db_status,
            "details": db_error
        }), 500

@app.route('/hello', methods=['GET'])
def hello():
    """Simple endpoint that responds with 'Hello, World!'."""
    return jsonify({"message": "Hello, World!"}), 200

@app.route('/log', methods=['POST'])
def trigger_log():
    """
    Triggers a log message at the specified level.
    Expects JSON: { "level": "info|warning|error|debug|critical", "message": "Your log message" }
    """
    data = request.json
    if not data or 'level' not in data or 'message' not in data:
        return jsonify({"error": "Missing 'level' or 'message' in request body"}), 400

    level = data['level'].lower()
    message = data['message']

    log_func = {
        "debug": app.logger.debug,
        "info": app.logger.info,
        "warning": app.logger.warning,
        "error": app.logger.error,
        "critical": app.logger.critical
    }.get(level)

    if not log_func:
        return jsonify({"error": f"Invalid log level '{level}'. Valid levels: debug, info, warning, error, critical."}), 400

    log_func(message)
    return jsonify({"status": "logged", "level": level, "message": message}), 200

@app.route('/crash', methods=['POST'])
def crash_app():
    """Endpoint to intentionally crash the entire application (for testing purposes)."""
    import os, signal
    os.kill(os.getppid(), signal.SIGTERM)
    return "Crashing...", 500  # This line likely won't be reached

@app.route('/pastebin', methods=['POST'])
def pastebin():
    """
    Accepts a text string, stores it in SQLite database with a 24h auto-delete policy,
    and returns the URL to retrieve it.
    Expects JSON: { "text": "your text here" }
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]
    paste_id = uuid.uuid4().hex
    
    try:
        # Calculate expiry time (24 hours from now)
        expiry = datetime.utcnow() + timedelta(hours=24)
        
        # Create a new paste record in the database
        new_paste = Pastebin(
            id=paste_id,
            content=text,
            expires_at=expiry,
            content_type="text/plain"
        )
        
        db.session.add(new_paste)
        db.session.commit()
        
        # Construct the URL for retrieving the paste
        # Use relative URL that works with the frontend - include /api prefix
        paste_url = f"/api/pastebin/{paste_id}"
        
        return jsonify({
            "url": paste_url, 
            "expires_at": expiry.isoformat() + "Z"
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error saving to pastebin: {e}")
        return jsonify({"error": f"Failed to save to pastebin: {str(e)}"}), 500

@app.route('/pastebin/<paste_id>', methods=['GET'])
def get_paste(paste_id):
    """
    Retrieves a paste by ID from the SQLite database.
    Returns 404 if the paste doesn't exist or has expired.
    """
    try:
        paste = Pastebin.query.get(paste_id)
        
        if not paste or paste.expires_at < datetime.utcnow():
            if paste:
                # If paste exists but has expired, delete it
                db.session.delete(paste)
                db.session.commit()
            return jsonify({"error": "Paste not found or has expired"}), 404
        
        # Set content type to match what's stored in the database
        return Response(paste.content, mimetype=paste.content_type)
    except Exception as e:
        app.logger.error(f"Error retrieving paste: {e}")
        return jsonify({"error": f"Failed to retrieve paste: {str(e)}"}), 500

@app.route('/cleanup-pastes', methods=['POST'])
def cleanup_expired_pastes():
    """
    Administrative endpoint to cleanup expired pastes from the database.
    """
    try:
        now = datetime.utcnow()
        expired_pastes = Pastebin.query.filter(Pastebin.expires_at < now).all()
        delete_count = len(expired_pastes)
        
        for paste in expired_pastes:
            db.session.delete(paste)
        
        db.session.commit()
        return jsonify({
            "status": "success", 
            "message": f"Deleted {delete_count} expired pastes"
        }), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error cleaning up expired pastes: {e}")
        return jsonify({"error": f"Failed to clean up expired pastes: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def welcome():
    """Returns a welcome page with a summary of the API endpoints."""
    welcome_text = """Welcome to the DevOps Lab Kit API!

Available endpoints:
  GET    /database/                - Retrieve all inventory items.
  POST   /database/                - Add a new inventory item.
  PUT    /database/<item_id>       - Update an inventory item by ID.
  DELETE /database/<item_id>       - Delete an inventory item by ID.
  GET    /healthcheck              - Check the health of the application.
  GET    /environment              - Retrieve environment variables.
  GET    /hello                    - Simple endpoint that responds with 'Hello, World!'.
  POST   /log                      - Log a message at a specified level.
  POST   /crash                    - Intentionally crash the application (for testing purposes).
  POST   /pastebin                 - Store text in the database with a 24h auto-delete policy.
  GET    /pastebin/<paste_id>      - Retrieve a paste by ID.
  POST   /cleanup-pastes           - Remove expired pastes from the database.
"""
    return Response(welcome_text, mimetype='text/plain')

# --- Application Runner ---
if __name__ == "__main__":
    print("Starting Flask application...")
    db_path = os.path.join(instance_path, "database.db")
    print(f"Database file expected at: {db_path}")
    if os.path.exists(db_path):
        print("Database file exists.")
    else:
        print("Database file does not exist yet, should be created by SQLAlchemy.")
    
    # Use the PORT environment variable if set, default to 5000 if not set
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
