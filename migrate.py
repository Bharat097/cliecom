# from models import Base
from base import engine, Base

Base.metadata.create_all(engine)