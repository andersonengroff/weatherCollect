# Spark Networks Python test

Simple Docker + Python + Flask + Postgres API

## Requirements

A [docker](https://www.docker.com/products/docker-desktop) installed 

## Installation
Unzip sparknet.zip file or git clone https://github.com/andersonengroff/weatherCollect.git


run
```bash
cd to/sparknet/unzip/folder
./dev_init.sh
```

## Usage
```
curl -H "Content-Type: application/json" -X POST http://localhost:5000/forecast/collect/7284876
curl -H "Content-Type: application/json" -X POST http://localhost:5000/forecast/collect/2640729
curl -H "Content-Type: application/json" -X POST http://localhost:5000/transformation/fact
```
## Data Retrieve

connect to postgres via jdbc using:

host: 0.0.0.0

port: 6432

database: sparknet_dev

user: sparknet

password: sparknet

```
-- sql example				  
select t.year,
       t.month,
       t.day,
       t.hour,
       s.code,
       s.name,
       total_rainfall,
       mean_max_temperature 
  from "FACT" f
  join "TIME" t on t.id = f.id_time 
  join "STATION" s on s.id = f.id_station 
where t.day = 12
   and t.month = 2
   and t.year = 2020
```
