# backend/init_db.py

from app.db.session import engine
from app.db.models import Base

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
