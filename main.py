# Third party imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# Local module import
# from api_funcs.price_history import make_price_csv_high, make_price_csv_many
from resources.data_injestion_polygon import ingest_data
from strategy_funcs.process_data import process_train
from tech_ind_funcs.gen_features import gen_feat
from ml_funcs.recursive_pred import rec_pred




def main():
    # Arguments to get data and process data

    api_key="dKIwVG_a9asU1TzdfO6TC4PiBjmLyb_V"
    ticker ="C:EURUSD"
    start_date = "2021-10-01"
    end_date = "2023-10-01"
    # raw_data = ingest_data(api_key,ticker,start_date, end_date)

    

    lag_features = 20
    forecasts = 6

    # Graphing or using local xsv data
    graphing = True
    use_local = True

    # Make the data object
    print("a")
    raw_data = pd.read_csv('data_EUR_USD.csv')
    raw_data.set_index('time',inplace=True)

    # Process data - Generate the data features - Bollinger Bands, RSI and Lags
    print("b")
    data_processed = gen_feat(raw_data, lag_features, graphing)

    # Make features and run training, returning the trained model
    print("c")
    model, scaler_train_y, scaler_train_x = process_train(graphing, data_processed)

    # Make a copy of the raw data for testing and make recursive predictions
    print("d")
    data_backtest = raw_data.copy()
    data_backtest = data_backtest[::forecasts + 1]
    data_backtest=data_backtest[-41:]
    forecasted_data, pred_out = rec_pred(model, data_backtest, forecasts, lag_features, scaler_train_x, scaler_train_y, graphing=False)


    # #Forcasted list
    # fore_list = []
    # for x in range(len(data_backtest)//1.2, len(data_backtest)):
    #     print(x)
    #     data_row = data_backtest.iloc[:x]
    #     forecasted_data, pred_out = rec_pred(model, data_row, forecasts, lag_features, scaler_train_x, scaler_train_y, graphing=False)
    #     # [fore_list.append(item) for item in pred_out]
    #     # print(f"{x-len(data_backtest)//2} of {len(data_backtest)-len(data_backtest)//2}")

    print("Predicted_Values",pred_out)
    # print(len(fore_list))
    # print(len(raw_data[len(raw_data)//2:]))

    # # Display the forecasted data
    # plt.plot(fore_list)
    # plt.plot(raw_data["high"][len(raw_data)//2-forecasts:].reset_index(drop=True))
    # plt.legend(['Preds', 'Real'])
    # plt.show()


    tf.keras.models.save_model(model, 'trained_model.h5')
    print(f"Trained model saved ")





if __name__ == "__main__":
    main()
