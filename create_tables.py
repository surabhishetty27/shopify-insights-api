from database import Base, engine
from models import db_models

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
