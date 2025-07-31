from sqlalchemy import create_engine, inspect
from app.core.config import settings

engine = create_engine(settings.database_url)
inspector = inspect(engine)

print("Tables found in database:")
print(inspector.get_table_names())
