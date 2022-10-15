#library
import matplotlib.pyplot as plt
from pandas_datareader import data as web
from datetime import datetime
from sklearn import preprocessing
import numpy as np
from finta import TA
import keras
import tensorflow as tf
from keras.models import Model
from keras.layers import Dense, Dropout, LSTM, Input, Activation, concatenate
from keras import optimizers
from keras.callbacks import History 
from sklearn.metrics import mean_squared_error
import pandas as pd
#create balance volume
def on_balance_volume_creation(df):
    new_df = pd.DataFrame({})
    new_df = df[['Adj Close']].copy()
    new_balance_volume = [0]
    tally = 0

    for i in range(1, len(new_df)):
        if (df['Adj Close'][i] > df['Adj Close'][i - 1]):
            tally += df['Volume'][i]
        elif (df['Adj Close'][i] < df['Adj Close'][i - 1]):
            tally -= df['Volume'][i]
        new_balance_volume.append(tally)

    new_df['On_Balance_Volume'] = new_balance_volume
    minimum = min(new_df['On_Balance_Volume'])
    new_df['On_Balance_Volume'] = new_df['On_Balance_Volume'] - minimum
    new_df['On_Balance_Volume'] = (new_df['On_Balance_Volume']+1).transform(np.log)
    return new_df
#indicators
def add_technical_indicators(new_df):
    data = pd.DataFrame()
    data['open'] = df['Open']
    data['high'] = df['High']
    data['low'] = df['Low']
    data['close'] = df['Close']
    data['volume'] = df['Volume']
    data.head()
    ema = TA.EMA(data)
    bb = TA.BBANDS(data)
    new_df['Exponential_moving_average'] = ema.copy()
    new_df = pd.concat([new_df, bb], axis = 1)
    for i in range(19):
        new_df['BB_MIDDLE'][i] = new_df.loc[i, 'Exponential_moving_average']
        if i != 0:
            higher = new_df.loc[i, 'BB_MIDDLE'] + 2 * new_df['Adj Close'].rolling(i + 1).std()[i]
            lower = new_df.loc[i, 'BB_MIDDLE'] - 2 * new_df['Adj Close'].rolling(i + 1).std()[i]
            new_df['BB_UPPER'][i] = higher
            new_df['BB_LOWER'][i] = lower
        else:
            new_df['BB_UPPER'][i] = new_df.loc[i, 'BB_MIDDLE']
            new_df['BB_LOWER'][i] = new_df.loc[i, 'BB_MIDDLE']
    return new_df

 #Preparation of train test set.
def train_test_split_preparation(new_df, train_split):
    train_indices = int(new_df.shape[0] * train_split)
    train_data = new_df[:train_indices]
    test_data = new_df[train_indices:]
    test_data = test_data.reset_index()
    test_data = test_data.drop(columns = ['index'])
    normaliser = preprocessing.MinMaxScaler()
    train_normalised_data = normaliser.fit_transform(train_data)
    test_normalised_data = normaliser.transform(test_data)
    X_train = np.array([train_normalised_data[:,0:][i : i + history_points].copy() for i in range(len(train_normalised_data) - history_points)])
    y_train = np.array([train_normalised_data[:,0][i + history_points].copy() for i in range(len(train_normalised_data) - history_points)])
    y_train = np.expand_dims(y_train, -1)
    y_normaliser = preprocessing.MinMaxScaler()
    next_day_close_values = np.array([train_data['Adj Close'][i + history_points].copy() for i in range(len(train_data) - history_points)])
    next_day_close_values = np.expand_dims(next_day_close_values, -1)

#normalize
    y_normaliser.fit(next_day_close_values)
    X_test = np.array([test_normalised_data[:,0:][i  : i + history_points].copy() for i in range(len(test_normalised_data) - history_points)])
    y_test = np.array([test_data['Adj Close'][i + history_points].copy() for i in range(len(test_data) - history_points)])    
    y_test = np.expand_dims(y_test, -1)
    return X_train, y_train, X_test, y_test, y_normaliser

#lstm model train
def lstm_model(X_train, y_train, history_points):
    tf.random.set_seed(20)
    np.random.seed(10)
    lstm_input = Input(shape=(history_points, 6), name='lstm_input')
    inputs = LSTM(21, name='first_layer')(lstm_input)
    inputs = Dense(1, name='dense_layer')(inputs)
    output = Activation('linear', name='output')(inputs)
    model = Model(inputs=lstm_input, outputs=output)
    adam = optimizers.Adam(lr = 0.0008)
    model.compile(optimizer=adam, loss='mse')
    model.fit(x=X_train, y=y_train, batch_size=25, epochs=50, shuffle=True, validation_split = 0.1)
    return model

#main function
if __name__ == "__main__":
    start_date = datetime(2017, 10, 10)
    end_date = datetime(2022, 10, 10)

    #pulling of BTC data from yahoofincance file
    df = pd.read_csv('../data/BTC-USD.csv')   
    train_split = 0.7
    history_points = 21
    data = on_balance_volume_creation(df)
    data = add_technical_indicators(data)
    X_train, y_train, X_test, y_test, y_reverse_normaliser = train_test_split_preparation(data, train_split)
    model = lstm_model(X_train, y_train, history_points)
    y_pred = model.predict(X_test)
    y_pred = y_reverse_normaliser.inverse_transform(y_pred)

#plots Actual value
    real = plt.plot(y_test, label='Trade Actual Price')
    pred = plt.plot(y_pred, label='Trade Predicted Price')
    plt.gcf().set_size_inches(12, 8, forward=True)
    plt.title('The real price and predicted price')
    plt.xlabel('Number of days')
    plt.ylabel('Adjusted Close Price($)')
    plt.legend(['Trade actual Price', 'Trade predicted Price'])
    print(mean_squared_error(y_test, y_pred))
    plt.show()  
  #show  