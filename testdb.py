from app.database import engine
from sqlalchemy import inspect

print(engine.url)
inspector = inspect(engine)
print("Tables in database:", inspector.get_table_names())