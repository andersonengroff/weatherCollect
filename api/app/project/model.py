from project import db

class Station(db.Model):
    __tablename__ = "STATION"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
 

    def __init__(self, 
                 name,
                 code
                 ):

        self.name = name
        self.code = code

class Time(db.Model):
    __tablename__ = "TIME"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=True)
    hour = db.Column(db.Integer, nullable=True)
 

    def __init__(self, 
                 year,
                 month,
                 day,
                 hour
                ):

        self.year = year
        self.month = month
        self.day = day
        self.hour = hour

class Fact(db.Model):
    __tablename__ = "FACT"

    id = db.Column(db.Integer, primary_key=True)
    id_station = db.Column(db.Integer, nullable=False)
    id_time = db.Column(db.Integer, nullable=False)
    total_rainfall = db.Column(db.Float, nullable=False)
    mean_max_temperature = db.Column(db.Float, nullable=False)
 

    def __init__(self, 
                 id_station,
                 id_time,
                 total_rainfall,
                 mean_max_temperature
                 ):

        self.id_station = id_station
        self.id_time = id_time
        self.total_rainfall = total_rainfall
        self.mean_max_temperature = mean_max_temperature

class Collector(db.Model):
    __tablename__ = "COLLECTOR"

    id = db.Column(db.Integer, primary_key=True)
    id_station = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    rain = db.Column(db.Float, nullable=False)
    max_temperature = db.Column(db.Float, nullable=False)
    origin = db.Column(db.String, nullable=False)
 

    def __init__(self, 
                 id_station,
                 datetime,
                 rain,
                 max_temperature,
                 origin
                 ):

        self.id_station = id_station
        self.datetime = datetime
        self.rain = rain
        self.max_temperature = max_temperature
        self.origin = origin





