import os
from flask import Flask, request, jsonify, Response
# Import db instance, init_db function, and models from database.py
from database import db, init_db, Inventory, Pastebin
from flask_cors import CORS # Import CORS
# Import text for raw SQL execution in health check
from sqlalchemy import text
from datetime import datetime, timedelta
import uuid
import logging
from logging.config import dictConfig
import colorama

# Initialize colorama for colored terminal output
colorama.init()

# Configure colorized logging
class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': colorama.Fore.BLUE,
        'INFO': colorama.Fore.WHITE,  # Changed to WHITE for no color
        'WARNING': colorama.Fore.YELLOW,
        'ERROR': colorama.Fore.RED,
        'CRITICAL': colorama.Fore.RED + colorama.Style.BRIGHT
    }
    
    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        return f"{self.COLORS.get(levelname, colorama.Fore.RESET)}{message}{colorama.Style.RESET_ALL}"

# Configure the Flask logger
dictConfig({
    'version': 1,
    'formatters': {
        'colored': {
            '()': ColorFormatter,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'level': 'DEBUG',
        },
    },
    'root': {
        'level': os.environ.get('LOG_LEVEL', 'INFO'),
        'handlers': ['console'],
    },
})

# Azure Blob Storage imports removed

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
    app.logger.info("Received GET request to fetch inventory.")
    try:
        # Use the imported Inventory model
        items = Inventory.query.all()
        app.logger.info(f"Fetched items: {[item.to_dict() for item in items]}")
        return jsonify([item.to_dict() for item in items])
    except Exception as e:
        app.logger.error(f"Error fetching inventory: {e}")
        return jsonify({"error": "Failed to fetch inventory"}), 500

@app.route('/database/', methods=['POST'])
def add_item():
    app.logger.info("Received POST request to add item.")
    try:
        data = request.json
        if not data or 'name' not in data or 'quantity' not in data or 'price' not in data:
             app.logger.warning(f"Invalid data received: {data}")
             return jsonify({"error": "Missing required fields (name, quantity, price)"}), 400
        app.logger.info(f"Request data: {data}")
        # Use the imported Inventory model and db instance
        new_item = Inventory(name=data['name'], quantity=data['quantity'], price=data['price'])
        db.session.add(new_item)
        db.session.commit()
        app.logger.info(f"Item added to database: {new_item.to_dict()}")
        return jsonify(new_item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error adding item: {e}")
        return jsonify({"error": "Failed to add item"}), 500

@app.route('/database/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    app.logger.info(f"Received PUT request for item ID: {item_id}")
    try:
        data = request.json
        if not data:
            app.logger.warning("No data provided for update.")
            return jsonify({"error": "No data provided"}), 400
        app.logger.info(f"Request data: {data}")
        # Use the imported Inventory model and db instance
        item = db.session.get(Inventory, item_id)
        if not item:
            app.logger.warning(f"Item with ID {item_id} not found.")
            return jsonify({"error": "Item not found"}), 404

        item.name = data.get('name', item.name)
        item.quantity = data.get('quantity', item.quantity)
        item.price = data.get('price', item.price)
        db.session.commit()
        app.logger.info(f"Item updated: {item.to_dict()}")
        return jsonify(item.to_dict())
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating item {item_id}: {e}")
        return jsonify({"error": "Failed to update item"}), 500

@app.route('/database/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    app.logger.info(f"Received DELETE request for item ID: {item_id}")
    try:
        # Use the imported Inventory model and db instance
        item = db.session.get(Inventory, item_id)
        if not item:
            app.logger.warning(f"Item with ID {item_id} not found.")
            return jsonify({"error": "Item not found"}), 404

        db.session.delete(item)
        db.session.commit()
        app.logger.info(f"Item deleted: ID {item_id}")
        return jsonify({"message": "Item deleted"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting item {item_id}: {e}")
        return jsonify({"error": "Failed to delete item"}), 500

@app.route('/environment', methods=['GET'])
def get_environment():
    """Returns all environment variables available to the process."""
    app.logger.info("Received GET request for environment.")
    try:
        environment = dict(os.environ)  # Get all environment variables as a dictionary
        app.logger.info(f"Environment details: {environment}")
        return jsonify(environment), 200
    except Exception as e:
        app.logger.error(f"Error fetching environment details: {e}")
        return jsonify({"error": "Failed to fetch environment details"}), 500

@app.route('/healthcheck', methods=['GET'])
def health_check():
    """Checks the health of the application, including database connectivity and table access."""
    app.logger.info("Received GET request for health check.")
    db_status = "disconnected"
    db_error = None
    try:
        # Perform a query against the actual tables to ensure they exist and are accessible
        # Using count() is efficient and confirms table access.
        inventory_count = db.session.query(Inventory.id).count()
        pastebin_count = db.session.query(Pastebin.id).count()
        
        db_status = "connected_and_tables_accessible"
        app.logger.info("Database connection and table access check successful.")
        return jsonify({
            "status": "ok", 
            "database": db_status,
            "inventory_count": inventory_count,
            "pastebin_count": pastebin_count
        }), 200
    except Exception as e:
        db_error = str(e)
        # Differentiate between general connection errors and table-specific errors
        if "no such table" in db_error.lower():
            db_status = "connected_table_missing"
            app.logger.error(f"Database connection okay, but table missing: {db_error}")
            app.logger.error(f"Health check failed - table missing: {db_error}")
        else:
            db_status = "connection_error"
            app.logger.error(f"Database connection check failed: {db_error}")
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

    log_func(f"[API LOG REQUEST] {message}")
    
    # Log to console as well for clarity
    app.logger.info(f"Log message created with level '{level}': {message}")
    
    return jsonify({
        "status": "logged", 
        "level": level, 
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "destination": "server_log"
    }), 200

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
    and returns the paste ID for retrieval.
    Expects JSON: { "text": "your text here" }
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]
    paste_id = uuid.uuid4().hex  # Generate a unique ID
    content_type = data.get("content_type", "text/plain")
    
    # Set expiry to 24 hours from now
    expiry = datetime.utcnow() + timedelta(hours=24)

    try:
        # Create a new Pastebin entry
        new_paste = Pastebin(
            id=paste_id,
            content=text,
            expires_at=expiry,
            content_type=content_type
        )
        
        db.session.add(new_paste)
        db.session.commit()
        
        # Construct the URL for the paste
        paste_url = f"{request.url_root}pastebin/{paste_id}"
        
        app.logger.info(f"Created new paste with ID: {paste_id}")
        return jsonify({
            "id": paste_id,
            "url": paste_url,
            "expires_at": expiry.isoformat() + "Z"
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating paste: {e}")
        return jsonify({"error": f"Failed to create paste: {str(e)}"}), 500

@app.route('/pastebin/<paste_id>', methods=['GET'])
def get_paste(paste_id):
    """
    Retrieves a paste by its ID.
    """
    try:
        # Query the paste from the database
        paste = Pastebin.query.get(paste_id)
        
        if not paste:
            app.logger.warning(f"Paste with ID {paste_id} not found")
            return jsonify({"error": "Paste not found"}), 404
            
        # Check if the paste has expired
        if paste.expires_at < datetime.utcnow():
            app.logger.info(f"Paste with ID {paste_id} has expired")
            # Clean up expired paste
            db.session.delete(paste)
            db.session.commit()
            return jsonify({"error": "Paste has expired"}), 404
            
        # Return the paste content with appropriate content type
        response = Response(paste.content, mimetype=paste.content_type)
        return response
        
    except Exception as e:
        app.logger.error(f"Error retrieving paste {paste_id}: {e}")
        return jsonify({"error": f"Failed to retrieve paste: {str(e)}"}), 500

@app.route('/pastebin/cleanup', methods=['POST'])
def cleanup_expired_pastes():
    """
    Removes all expired pastes from the database.
    This endpoint could be called periodically by a scheduled job.
    """
    try:
        # Find all expired pastes
        expired_pastes = Pastebin.query.filter(Pastebin.expires_at < datetime.utcnow()).all()
        count = len(expired_pastes)
        
        # Delete all expired pastes
        for paste in expired_pastes:
            db.session.delete(paste)
        
        db.session.commit()
        
        app.logger.info(f"Cleaned up {count} expired pastes")
        return jsonify({
            "message": f"Cleaned up {count} expired pastes",
            "count": count
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
  POST   /pastebin                 - Upload text to SQLite database with a 24h auto-delete policy.
  GET    /pastebin/<paste_id>      - Retrieve a paste by ID.
  POST   /pastebin/cleanup         - Remove all expired pastes from the database.
"""
    return Response(welcome_text, mimetype='text/plain')

# --- Application Runner ---
if __name__ == "__main__":
    app.logger.info("Starting Flask application...")
    db_path = os.path.join(instance_path, "database.db")
    app.logger.info(f"Database file expected at: {db_path}")
    if os.path.exists(db_path):
        app.logger.info("Database file exists.")
    else:
        app.logger.info("Database file does not exist yet, should be created by SQLAlchemy.")
    
    # Use the PORT environment variable, default to 5000 if not set
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
