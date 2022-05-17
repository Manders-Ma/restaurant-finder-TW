import googlemaps
from sqlalchemy.ext.declarative import declarative_base
from google.cloud.sql.connector import Connector
import sqlalchemy as sa
import pg8000
import os

class Environment:
    def __init__(self) -> None:
        self.GOOGLE_APPLICATION_CREDENTIALS = "D:/DabaseDesignProject/key/database-project-348308-2e88dd61cf17.json"
        self.POSTGRES_CONNECTION_NAME = "database-project-348308:asia-east1:database-project"
        self.POSTGRES_USER = "postgres"
        self.POSTGRES_PASS = "881626"
        self.POSTGRES_DB = "restaurant"
        self.ip = "34.81.1.117"

# Set environemnt - CREDENTIALS
environ = Environment()


def init_connection_engine() -> sa.engine.Engine:
    def getconn() -> pg8000.dbapi.Connection:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = environ.GOOGLE_APPLICATION_CREDENTIALS
        connector = Connector()
        conn: pg8000.dbapi.Connection = connector.connect(
            environ.POSTGRES_CONNECTION_NAME,
            "pg8000",
            user=environ.POSTGRES_USER,
            password=environ.POSTGRES_PASS,
            db=environ.POSTGRES_DB,
        )
        return conn

    engine = sa.create_engine(
        "postgresql+pg8000://{}:{}@{}/{}".format(
            environ.POSTGRES_USER,
            environ.POSTGRES_PASS,
            environ.ip,
            environ.POSTGRES_DB
        ),
        creator=getconn,
    )
    engine.dialect.description_encoding = None
    return engine


BASE = declarative_base()


class Location(BASE):
    __tablename__ = 'location'
    Region = sa.Column(sa.String(10))
    Town = sa.Column(sa.String(10))
    location_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    rests = sa.orm.relationship('Restaurant')

    def __str__(self) -> str:
        return 'Region:{}, Town:{}'.format(self.Region, self.Town)


class Restaurant(BASE):

    __tablename__ = 'restaurant'
    Name = sa.Column(sa.String(100), primary_key=True)
    Description = sa.Column(sa.String(400))
    Add = sa.Column(sa.String(60))
    Region = sa.Column(sa.String(10))
    Town = sa.Column(sa.String(10))
    Opentime = sa.Column(sa.String(500))
    Parkinginfo = sa.Column(sa.String(100))
    Tel = sa.Column(sa.String(40))
    url = sa.Column(sa.String(200))

    fk_location_id = sa.Column(
        sa.Integer, sa.ForeignKey('location.location_id'))


engine = init_connection_engine()
Session = sa.orm.sessionmaker(bind=engine)

if __name__ == '__main__':
    s = Session()
    # BASE.metadata.create_all(engine)
    # msg = """UPDATE public.restaurant
    # SET fk_location_id=public.location.location_id
    # FROM public.location
    # WHERE public.restaurant."Region"=public.location."Region"
    # AND public.restaurant."Town"=public.location."Town";
    # """
    # s.execute(msg)
    s.commit()
    s.close()
