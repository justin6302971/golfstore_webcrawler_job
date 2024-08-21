from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime,types


from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


class GolfStoreDb:
    def __init__(self):
        # sqlalchemy_database_uri = 'postgresql://tempuser_local:temppassword_local@127.0.0.1:9908/exampledb_local'
        sqlalchemy_database_uri = 'postgresql://tempuser_local:temppassword_local@postgresqldb/exampledb_local'

        self.engine = create_engine(
            sqlalchemy_database_uri, echo=True, future=True)

        self.sessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        
        Base.metadata.create_all(self.engine)

    def get_db(self):
        db = self.sessionLocal()
        try:
            yield db
        finally:
            db.close()


class Base(DeclarativeBase):
    pass

class GolfStoreInfo(Base):
    __tablename__ = 'golf_store_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200), nullable=False)
    data = Column(JSONB, nullable=True)
    created_at = Column(types.DateTime(timezone=True), default=datetime.utcnow)
    modified_at = Column(types.DateTime(timezone=True), default=datetime.utcnow)
    