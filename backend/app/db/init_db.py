from app.db.models import Base
from app.db.session import engine

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("✅ Done.")
