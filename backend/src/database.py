from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect as sqlalchemy_inspect # Rename to avoid conflict
# Import the specific exception type
from sqlalchemy.exc import OperationalError

# Initialize SQLAlchemy without an app object initially
db = SQLAlchemy()

# --- Model Definition ---
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price
        }

def init_db(app):
    """Initializes the database and creates tables if they don't exist."""
    db.init_app(app)
    with app.app_context():
        print("Checking and creating database tables if they don't exist...")
        try:
            # Call create_all on the metadata object, passing the engine and checkfirst
            db.metadata.create_all(bind=db.engine, checkfirst=True)
            print("Database tables checked/created successfully.")
            # Optional: Verify table existence
            inspector = sqlalchemy_inspect(db.engine)
            if 'inventory' in inspector.get_table_names():
                print("Verified 'inventory' table exists.")
            else:
                print("Warning: 'inventory' table not found after create_all().")
        except OperationalError as e:
            # Check if the error is specifically about the table already existing
            if "table inventory already exists" in str(e).lower():
                print("Info: Table 'inventory' already exists, skipping creation.")
            else:
                # Log other OperationalErrors as actual errors
                print(f"Error during database initialization: {e}")
                app.logger.error(f"Error during database initialization: {e}")
        except Exception as e:
            # Catch any other unexpected errors during initialization
            print(f"Unexpected error during database initialization: {e}")
            app.logger.error(f"Unexpected error during database initialization: {e}")