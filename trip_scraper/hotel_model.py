from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(String, unique=True)
    hotel_name = Column(String)
    hotel_url = Column(String)
    hotel_location = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float)
    image_url = Column(String)
    price = Column(Float)
    city = Column(String)
    section = Column(String)

# Replace with your actual PostgreSQL connection details
engine = create_engine(DATABASE_URL)

# Create the table
Base.metadata.create_all(engine)
