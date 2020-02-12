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

def time_transform():
    sql = """ with 
                    new_date as (
                            select extract(year from datetime) as year,
                                    extract(month from datetime) as month,
                                    extract(day from datetime) as day,
                                    case 
                                        when extract(hour from datetime) <= 3 then 3
                                        when extract(hour from datetime) <= 6 then 6
                                        when extract(hour from datetime) <= 9 then 9
                                        when extract(hour from datetime) <= 12 then 12
                                        when extract(hour from datetime) <= 15 then 15
                                        when extract(hour from datetime) <= 18 then 18
                                        when extract(hour from datetime) <= 21 then 21
                                        when extract(hour from datetime) <= 24 then 24
                                    end as hour
                            from "COLLECTOR"
                        group by 1,2,3,4	
                    ),
                    
                    missing_date_month as (
                                        select nd.year, nd.month, null::Integer as day, null::Integer as hour
                                        from new_date nd
                                        left join "TIME" t on t.year = nd.year and t.month = nd.month
                                        where t.id is null
                                        group by 1,2,3,4

                                    ),
                                    
                    missing_date_day as (
                                    select nd.year, nd.month, nd.day, null::Integer as hour
                                    from new_date nd
                                    left join "TIME" t on t.year = nd.year and t.month = nd.month and t.day = nd.day
                                    where t.id is null
                                    group by 1,2,3,4

                                ),
                                
                    missing_date_hour as (
                                    select nd.year, nd.month, nd.day, nd.hour as hour
                                    from new_date nd
                                    left join "TIME" t on t.year = nd.year and t.month = nd.month and t.day = nd.day and t.hour = nd.hour
                                    where t.id is null
                                    group by 1,2,3,4

                                ),
                                
                    missing_date as (
                                        select year, month, day, hour from missing_date_month
                                        union
                                        select year, month, day, hour from  missing_date_day
                                        union
                                        select year, month, day, hour from  missing_date_hour	
                    )
                    
                    
                    INSERT into "TIME" (id, year, month, day, hour) select nextval('time_sequence') as id, year, month, day, hour from missing_date
                            
        """
    db.session.execute(sql)
    db.session.commit()


def fact_transform():
    sql = """with 
                    collect_daily_not_repetead_data as (select cast(id_station as varchar) as code,
                                                    extract(year from datetime) as year,
                                                    extract(month from datetime) as month,
                                                    extract(day from datetime) as day,
                                                    extract(hour from datetime) as real_hour,
                                                    case 
                                                            when extract(hour from datetime) <= 3 then 3
                                                            when extract(hour from datetime) <= 6 then 6
                                                            when extract(hour from datetime) <= 9 then 9
                                                            when extract(hour from datetime) <= 12 then 12
                                                            when extract(hour from datetime) <= 15 then 15
                                                            when extract(hour from datetime) <= 18 then 18
                                                            when extract(hour from datetime) <= 21 then 21
                                                            when extract(hour from datetime) <= 24 then 24
                                                    end as hour,
                                                    max(rain) as rain,
                                                    max(max_temperature) as max_temperature
                                                from "COLLECTOR" c 
                                                group by 1, 2, 3, 4, 5, 6
                                            ),
                                            
                month_transformation as (
                    select code,
                            month,
                            year,
                            sum(rain) as total_rainfall,
                            avg(max_temperature) as mean_max_temperature
                        from collect_daily_not_repetead_data  
                        group by 1,2,3
                ),
                
                day_transformation as (
                    select code,
                            month,
                            year,
                            day,
                            sum(rain) as total_rainfall,
                            avg(max_temperature) as mean_max_temperature
                        from collect_daily_not_repetead_data  
                        group by 1,2,3,4
                ),
                
                hour_transformation as (
                    select code,
                            month,
                            year,
                            day,
                            hour,
                            sum(rain) as total_rainfall,
                            avg(max_temperature) as mean_max_temperature
                        from collect_daily_not_repetead_data  
                        group by 1,2,3,4,5
                ),
                
                data_fact_month as (
                                    select nextval('fact_sequence') as id,
                                        s.id as id_station,
                                        t.id as id_time,
                                        total_rainfall,
                                        mean_max_temperature      
                                from month_transformation m
                                join "TIME" t on t.year = m.year and t.month = m.month and t.day is null and t.hour is null
                                join "STATION" s on s.code = m.code 
                ),
                
                data_fact_day as (
                                    select nextval('fact_sequence') as id,
                                        s.id as id_station,
                                        t.id as id_time,
                                        total_rainfall,
                                        mean_max_temperature      
                                from day_transformation d
                                join "TIME" t on t.year = d.year and t.month = d.month and t.day = d.day and t.hour is null
                                join "STATION" s on s.code = d.code 
                ),
                
                data_fact_hour as (
                                    select nextval('fact_sequence') as id,
                                        s.id as id_station,
                                        t.id as id_time,
                                        total_rainfall,
                                        mean_max_temperature      
                                from hour_transformation h
                                join "TIME" t on t.year = h.year and t.month = h.month and t.day = h.day and t.hour = h.hour
                                join "STATION" s on s.code = h.code 
                ),
                
                data_fact as (
                                    select * from data_fact_month
                                    union 
                                    select * from data_fact_day
                                    union
                                    select * from data_fact_hour				
                )
                
                insert into "FACT" select * from data_fact
    """
    db.session.execute(sql)
    db.session.commit()

