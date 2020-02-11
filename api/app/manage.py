from flask.cli import FlaskGroup

from project import app, db
import csv

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.engine.execute(
        """CREATE TABLE TMP_SEED (
            id serial NOT NULL,
            station varchar(20) NOT NULL,
            year int4 NOT NULL,
            month int4 NOT NULL,
            tmax float8 NOT NULL,
            tmin float8 NOT NULL,
            rain float8 NOT NULL,
            CONSTRAINT seed_pkey PRIMARY KEY (id)
        )"""
    )

    db.engine.execute(
        """INSERT INTO "STATION" (name, code) 
            VALUES ('Heathrow','7284876'), 
            ('Oxford','2640729'),
            ('Cardiff','2653822'),
            ('Shawbury','2638111'),
            ('Leuchars','2644581')
        """
    )

    with open('./weather_history.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        for row in reader:
            db.engine.execute(
                "INSERT INTO TMP_SEED VALUES (%s, %s, %s, %s, %s,%s, %s)",
                row
            )
        db.session.commit()

    db.engine.execute(
        """INSERT into "TIME"  
                select row_number() over (order by year, month) as row_number,
                    year,
                    month
                from (select year, month
                        from tmp_seed
                        group by 1,2
                    ) s 
        """
    )

    db.engine.execute(
        """INSERT into "FACT" 
                select row_number() over (order by ts.year, ts.month) as row_number,
                    s.id,
                    t.id,
                    ts.rain,
                    ts.tmax 
                from tmp_seed ts 
                join "STATION" s on s."name" = ts.station 
                join "TIME" t on t."year" = ts."year" and t."month" = ts."month" 
        """
    )

    db.engine.execute(
        "DROP TABLE TMP_SEED"
    )



if __name__ == "__main__":
    cli()
