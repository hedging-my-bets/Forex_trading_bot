import pandas as pd
from polygon import RESTClient
import time

def ingest_data(api_key, ticker, start_date, end_date):
    aggs = []

    # Define the initial start date and step size (e.g., 6 months)
    current_date = pd.to_datetime(start_date)
    step_size = pd.DateOffset(months=6)

    # Create the RESTClient
    client = RESTClient(api_key)

    # Loop to fetch data in chunks of 6 months
    while current_date < pd.to_datetime(end_date):
        # Calculate the end date for this chunk (6 months later)
        chunk_end_date = current_date + step_size
        if chunk_end_date > pd.to_datetime(end_date):
            chunk_end_date = pd.to_datetime(end_date)

        # Fetch data for the current chunk
        for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="hour",
                                  from_=current_date.strftime("%Y-%m-%d"),
                                  to=chunk_end_date.strftime("%Y-%m-%d"), limit=50000):
            aggs.append(a)

        # Move to the next chunk
        current_date = chunk_end_date + pd.DateOffset(days=1)

        # Pause for rate limiting (wait for 12 seconds to make 5 API calls per minute)
        time.sleep(60)

    # Create a DataFrame from the collected data
    data = pd.DataFrame(aggs)
    data['Date'] = data['timestamp'].apply(lambda x: pd.to_datetime(x * 1000000))
    data = data[['Date', 'open', 'high', 'low', 'close', 'volume']]
    data.rename_axis('time', inplace=True)
    
    # Save the data to a CSV file
    data.to_csv('test_data_.csv', index=False)
    
    return data


