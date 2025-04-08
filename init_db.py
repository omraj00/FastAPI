from sqlalchemy.orm import Session
from app.db import engine, Base, SessionLocal
from app.models import Tenant

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    # Check if we already have tenants
    existing_tenants = db.query(Tenant).all()
    if not existing_tenants:
        # Add sample tenants
        sample_tenants = [
            Tenant(name="Tech Blog", domain="tech.localhost"),
            Tenant(name="Food Blog", domain="food.localhost"),
            Tenant(name="Travel Blog", domain="travel.localhost"),
            Tenant(name="Default Blog", domain="localhost")
        ]
        db.add_all(sample_tenants)
        db.commit()
        print("Added sample tenants to the database.")
    else:
        print(f"Database already contains {len(existing_tenants)} tenants.")
    
    db.close()

if __name__ == "__main__":
    print("Initializing the database...")
    init_db()
    print("Database initialization completed.")
