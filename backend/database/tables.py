from backend.database.db import engine, Base
from backend.database import models


Base.metadata.create_all(bind=engine)
print("tables created")