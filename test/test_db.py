from sqlalchemy import inspect
from backend.database.db import engine

inspector = inspect(engine)

table_name = "users"
columns = inspector.get_columns(table_name)

print(f"Structure of table '{table_name}':")
for column in columns:
    print(f"Name: {column['name']}, Type: {column['type']}, Nullable: {column['nullable']}, Default: {column.get('default')}")
