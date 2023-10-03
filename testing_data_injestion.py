from resources.data_injestion_polygon import ingest_data

api_key="dKIwVG_a9asU1TzdfO6TC4PiBjmLyb_V"
ticker ="C:EURUSD"
start_date = "2023-09-01"
end_date = "2023-10-01"

data = ingest_data(api_key,ticker,start_date, end_date)
print(data.head())
print(data.tail)