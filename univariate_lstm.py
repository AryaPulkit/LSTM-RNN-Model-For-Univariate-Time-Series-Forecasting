# -*- coding: utf-8 -*-
"""Univariate_LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rWyqLIoJQv63sTWtn5I3-IUgF1D8lcKq

#kaggle dataset
#https://www.kaggle.com/rakannimer/air-passengers?select=AirPassengers.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

data = pd.read_csv('AirPassengers.csv')
data

data.tail()

data.info()

data['Month'] = pd.to_datetime(data['Month'])
data.info()

data.set_index('Month', inplace=True) #set date as index

plt.xlabel("Month")
plt.ylabel("Passengers")
plt.title("Passengers Travelled")
plt.plot(data['#Passengers'],)

#data_Scaling
data['#Passengers']

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))
data=scaler.fit_transform(data)

data

data.shape

#Creating train and test partition
train = int(len(data)*0.75)
test = len(data)-train

train

test

train_data,test_data=data[0:train,:],data[train:len(data),:1]

train_data

test_data

# converting an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-time_step-1):
		a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3
		dataX.append(a)
		dataY.append(dataset[i + time_step, 0])
	return np.array(dataX), np.array(dataY)

# reshape into X=t,t+1,t+2,t+3 and Y=t+4
time_step = 4
X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)

y_train

X_train.shape, y_train.shape

# reshape input to be [sample, time steps, features] which is required for LSTM
X_train =X_train.reshape(X_train.shape[0], 4, 1)
X_test = X_test.reshape(X_test.shape[0], 4, 1)

X_train.shape

### Create the LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(4,1)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')
model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=100,batch_size=1,verbose=1)

#Model Prediction
train_predict=model.predict(X_train)
test_predict=model.predict(X_test)

test_predict

#Transforming data back to original form
train_predict=scaler.inverse_transform(train_predict)
test_predict=scaler.inverse_transform(test_predict)

test_predict

### Calculate RMSE performance metrics
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(y_train,train_predict))

### Test Data RMSE
math.sqrt(mean_squared_error(ytest,test_predict))

### Plotting 
# shift train predictions for plotting
lookback=4
trainPredictPlot = np.empty_like(data)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(train_predict)+look_back, :] = train_predict
# shift test predictions for plotting
testPredictPlot = np.empty_like(data)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(train_predict)+(look_back*2)+1:len(data)-1, :] = test_predict
# plot baseline and predictions
plt.xlabel("Month")
plt.ylabel("Passengers")
plt.title("Passengers Travelled")
plt.plot(scaler.inverse_transform(data)) #original data
plt.plot(trainPredictPlot) #train prediction
plt.plot(testPredictPlot) #test prediction
plt.show()