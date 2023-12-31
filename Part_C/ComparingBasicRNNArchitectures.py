# -*- coding: utf-8 -*-
"""ComparingBasicRNNArchitectures.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vekA9IzQI3DckScf1k2vGY3xdeE9uZ98

**Deep learning Project**,
**Part C**

**Student: Kaftantzis Savvas, aivc22007**
"""

#Libraries
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, LSTM, GRU, Dense, Dropout, Bidirectional
from tensorflow.keras.losses import MeanSquaredError, mean_absolute_error
from sklearn.metrics import mean_squared_error, mean_absolute_error, max_error
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# Mount Google Drive to access the dataset files.
from google.colab import drive
drive.mount('/content/drive')

# Load the dataset files using NumPy.
CoffeeMachinemaxAgg = np.loadtxt('/content/drive/MyDrive/WaterHeater/WaterHeatermaxAgg.txt')
# maximum consumption value observed in electrical panel of the house
CoffeeMachinemaxApp = np.loadtxt('/content/drive/MyDrive/WaterHeater/WaterHeatermaxApp.txt')
# It includes the maximum consumption value observed in the coffee machine
Input_Data = np.loadtxt('/content/drive/MyDrive/WaterHeater/Input_Data.txt'
, delimiter=',')
# The prices refer to the total consumption at home, during this period
Output_Data = np.loadtxt('/content/drive/MyDrive/WaterHeater/Output_Data.txt'
, delimiter=',')
# The prices refer to the consumption of the specific device, in this space.

# (specifying the delimiter as a comma ',' to correctly parse the values)

# The two txts(CoffeeMachinemaxAgg, CoffeeMachinemaxApp) contain values ​​in Watts.
# We need to convert them to kW, as are the values ​​of the 2 variables
MaxAgg = (CoffeeMachinemaxAgg/1000)
MaxApp = (CoffeeMachinemaxApp/1000)
print('CoffeeMachinemaxAgg after conversion: ', MaxAgg)
print('CoffeeMachinemaxApp after conversion: ', MaxApp)

# Normalize input and output data
X = Input_Data / MaxAgg
y = Output_Data / MaxApp

# Generate random indices to select random periods of time, for the plots
num_periods = Input_Data.shape[0]
random_indices = np.random.choice(num_periods, size=3, replace=False)

# Plotting the random periods and saving each plot separately
for i, index in enumerate(random_indices):
    # Get the data for the selected random period
    total_consumption = X[index]
    coffee_maker_consumption = y[index]

    # Create a new figure and axes
    fig, ax1 = plt.subplots(figsize=(8, 4))

    # Plot total consumption on the primary y-axis
    ax1.plot(total_consumption, color='blue', label='Total Consumption')
    ax1.set_ylabel('Total Consumption (kW)')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a secondary y-axis for coffee maker consumption
    ax2 = ax1.twinx()

    # Plot coffee maker consumption on the secondary y-axis
    ax2.plot(coffee_maker_consumption, color='red', label='Coffee Maker Consumption')
    ax2.set_ylabel('Coffee Maker Consumption (kW)')
    ax2.tick_params(axis='y', labelcolor='red')

    # Combine the legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines = lines1 + lines2
    labels = labels1 + labels2
    ax1.legend(lines, labels, loc='upper left')

    # Set the x-axis label
    ax1.set_xlabel('Time')

    # Set the plot title
    ax1.set_title(f'Random Period {i+1}')

    # Adjust layout to accommodate the legends
    fig.tight_layout()

    # Save the plot as an image file
    fig.savefig(f'plot{i+1}.png')

    # Display the plot
    plt.show()
    # Close the figure to release memory
    plt.close(fig)

X.shape , y.shape

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print('X_train shape:', X_train.shape)
print('X_test  shape:', X_test.shape)
print('y_train shape:', y_train.shape)
print('y_test  shape:', y_test.shape)

# Define model architecture and compile
# LSTM
model_lstm = Sequential()
model_lstm.add(LSTM(128, input_shape=(120, 1), return_sequences=True))
model_lstm.add(Dense(1))
model_lstm.compile(optimizer=Adam(), loss=MeanSquaredError())

# RNN
model_rnn = Sequential()
model_rnn.add(SimpleRNN(128, input_shape=(120, 1), return_sequences=True))
model_rnn.add(Dense(1))
model_rnn.compile(optimizer=Adam(), loss=MeanSquaredError())

# GRU
model_gru = Sequential()
model_gru.add(GRU(128, input_shape=(120, 1), return_sequences=True))
model_gru.add(Dense(1))
model_gru.compile(optimizer=Adam(), loss=MeanSquaredError())

# Define the callbacks for early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5)

# Train the models
epochs = 37
history_lstm = model_lstm.fit(X_train, y_train, \
                              epochs=epochs, validation_split=0.2, callbacks=[early_stopping])

history_rnn = model_rnn.fit(X_train, y_train,\
                              epochs=epochs, validation_split=0.2, callbacks=[early_stopping])

history_gru = model_gru.fit(X_train, y_train,\
                              epochs=epochs, validation_split=0.2, callbacks=[early_stopping])

# plot the history performance scores
plt.figure(figsize=(8,5))
plt.plot(history_rnn.history[list(history_rnn.history.keys())[0]])
plt.plot(history_rnn.history[list(history_rnn.history.keys())[1]])
plt.title('RNN model')
plt.ylabel(list(history_rnn.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

plt.figure(figsize=(8,5))
plt.plot(history_gru.history[list(history_gru.history.keys())[0]])
plt.plot(history_gru.history[list(history_gru.history.keys())[1]])
plt.title('GRU model')
plt.ylabel(list(history_gru.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

plt.figure(figsize=(8,5))
plt.plot(history_lstm.history[list(history_lstm.history.keys())[0]])
plt.plot(history_lstm.history[list(history_lstm.history.keys())[1]])
plt.title('LSTM model')
plt.ylabel(list(history_lstm.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

# Evaluate the models
train_loss_gru = history_gru.history['loss'][-1]
val_loss_gru   = history_gru.history['val_loss'][-1]

print(f"GRU training loss: {train_loss_gru}")
print(f"GRU validation loss: {val_loss_gru}")

train_loss_rnn = history_rnn.history['loss'][-1]
val_loss_rnn  = history_rnn.history['val_loss'][-1]

print(f"\nRNN training loss: {train_loss_rnn}")
print(f"RNN validation loss: {val_loss_rnn}")

train_loss_lstm = history_lstm.history['loss'][-1]
val_loss_lstm = history_lstm.history['val_loss'][-1]

print(f"\nLSTM training loss: {train_loss_lstm}")
print(f"LSTM validation loss: {val_loss_lstm}")

# Predict using the models
lstm_train_predictions = model_lstm.predict(X_train)
lstm_test_predictions = model_lstm.predict(X_test)

rnn_train_predictions = model_rnn.predict(X_train)
rnn_test_predictions = model_rnn.predict(X_test)

gru_train_predictions = model_gru.predict(X_train)
gru_test_predictions = model_gru.predict(X_test)

# Reshape LSTM predictions
lstm_train_predictions = np.reshape(lstm_train_predictions, (lstm_train_predictions.shape[0], -1))
lstm_test_predictions = np.reshape(lstm_test_predictions, (lstm_test_predictions.shape[0], -1))

# Reshape RNN predictions
rnn_train_predictions = np.reshape(rnn_train_predictions, (rnn_train_predictions.shape[0], -1))
rnn_test_predictions = np.reshape(rnn_test_predictions, (rnn_test_predictions.shape[0], -1))

# Reshape GRU predictions
gru_train_predictions = np.reshape(gru_train_predictions, (gru_train_predictions.shape[0], -1))
gru_test_predictions = np.reshape(gru_test_predictions, (gru_test_predictions.shape[0], -1))

# Denormalize the predictions
denorm_lstm_train_predictions = (lstm_train_predictions * MaxApp)
denorm_lstm_test_predictions = (lstm_test_predictions * MaxApp)

denorm_rnn_train_predictions = (rnn_train_predictions * MaxApp)
denorm_rnn_test_predictions = (rnn_test_predictions * MaxApp)

denorm_gru_train_predictions = (gru_train_predictions * MaxApp)
denorm_gru_test_predictions = (gru_test_predictions * MaxApp)

# Calculate RMSE for each model (LSTM, RNN, GRU) on training set
rmse_train_lstm = np.sqrt(mean_squared_error(y_train, denorm_lstm_train_predictions))
rmse_train_rnn = np.sqrt(mean_squared_error(y_train, denorm_rnn_train_predictions))
rmse_train_gru = np.sqrt(mean_squared_error(y_train, denorm_gru_train_predictions))

# Calculate RMSE for each model (LSTM, RNN, GRU) on test set
rmse_test_lstm = np.sqrt(mean_squared_error(y_test, denorm_lstm_test_predictions))
rmse_test_rnn = np.sqrt(mean_squared_error(y_test, denorm_rnn_test_predictions))
rmse_test_gru = np.sqrt(mean_squared_error(y_test, denorm_gru_test_predictions))

# Calculate MAE for each model (LSTM, RNN, GRU) on training set
mae_train_lstm = mean_absolute_error(y_train, denorm_lstm_train_predictions)
mae_train_rnn = mean_absolute_error(y_train, denorm_rnn_train_predictions)
mae_train_gru = mean_absolute_error(y_train, denorm_gru_train_predictions)

# Calculate MAE for each model (LSTM, RNN, GRU) on test set
mae_test_lstm = mean_absolute_error(y_test, denorm_lstm_test_predictions)
mae_test_rnn = mean_absolute_error(y_test, denorm_rnn_test_predictions)
mae_test_gru = mean_absolute_error(y_test, denorm_gru_test_predictions)

# Calculate maximum error for each model (LSTM, RNN, GRU) on training set
max_error_train_lstm = np.max(np.abs(y_train - denorm_lstm_train_predictions), axis=0)
max_error_train_rnn = np.max(np.abs(y_train - denorm_rnn_train_predictions), axis=0)
max_error_train_gru = np.max(np.abs(y_train - denorm_gru_train_predictions), axis=0)

# Calculate maximum error for each model (LSTM, RNN, GRU) on test set
max_error_test_lstm = np.max(np.abs(y_test - denorm_lstm_test_predictions), axis=0)
max_error_test_rnn = np.max(np.abs(y_test - denorm_rnn_test_predictions), axis=0)
max_error_test_gru = np.max(np.abs(y_test - denorm_gru_test_predictions), axis=0)

# Convert maximum error to a single value per output
max_error_train_lstm = np.max(max_error_train_lstm)
max_error_train_rnn = np.max(max_error_train_rnn)
max_error_train_gru = np.max(max_error_train_gru)
max_error_test_lstm = np.max(max_error_test_lstm)
max_error_test_rnn = np.max(max_error_test_rnn)
max_error_test_gru = np.max(max_error_test_gru)

# Define model names for plotting
model_names = ['LSTM', 'RNN', 'GRU']

# Collect RMSE values for training and test sets
rmse_train = [rmse_train_lstm, rmse_train_rnn, rmse_train_gru]
rmse_test = [rmse_test_lstm, rmse_test_rnn, rmse_test_gru]

# Collect MAE values for training and test sets
mae_train = [mae_train_lstm, mae_train_rnn, mae_train_gru]
mae_test = [mae_test_lstm, mae_test_rnn, mae_test_gru]

# Collect Max Error values for training and test sets
max_error_train = [max_error_train_lstm, max_error_train_rnn, max_error_train_gru]
max_error_test = [max_error_test_lstm, max_error_test_rnn, max_error_test_gru]

# Plot RMSE
plt.figure(figsize=(7, 5))
plt.plot(model_names, rmse_train, marker='o', label='Train')
plt.plot(model_names, rmse_test, marker='o', label='Test')
plt.xlabel('Model')
plt.ylabel('RMSE')
plt.title('RMSE for Each Model')
plt.legend()
plt.savefig('rmse_figure.png')
plt.show()

# Plot MAE
plt.figure(figsize=(7, 5))
plt.plot(model_names, mae_train, marker='o', label='Train')
plt.plot(model_names, mae_test, marker='o', label='Test')
plt.xlabel('Model')
plt.ylabel('MAE')
plt.title('MAE for Each Model')
plt.legend()
plt.savefig('mae_figure.png')
plt.show()

# Plot Max Error
plt.figure(figsize=(7,5))
plt.plot(model_names, max_error_train, marker='o', label='Train')
plt.plot(model_names, max_error_test, marker='o', label='Test')
plt.xlabel('Model')
plt.ylabel('Max Error')
plt.title('Max Error for Each Model')
plt.legend()
plt.savefig('max_error_figure.png')
plt.show()

# Select four lines from the test data
working_lines = [0, 1]  # Indices of lines when the device was working
off_lines = [2, 3]  # Indices of lines when the device was off

# Plot actual consumption and predictions for working lines and save/show the plots
for line_idx in working_lines:
    plt.figure(figsize=(7, 5))
    plt.plot(X_test[line_idx], label='Actual')
    plt.plot(lstm_test_predictions[line_idx], label='LSTM')
    plt.plot(rnn_test_predictions[line_idx], label='RNN')
    plt.plot(gru_test_predictions[line_idx], label='GRU')
    plt.xlabel('Time')
    plt.ylabel('Consumption')
    plt.title(f'Working Line {line_idx + 1}')
    plt.legend()
    plt.savefig(f'figure_working_line_{line_idx + 1}.png')
    plt.show()

# Plot actual consumption and predictions for off lines and save/show the plots
for line_idx in off_lines:
    plt.figure(figsize=(7, 5))
    plt.plot(X_test[line_idx], label='Actual')
    plt.plot(lstm_test_predictions[line_idx], label='LSTM')
    plt.plot(rnn_test_predictions[line_idx], label='RNN')
    plt.plot(gru_test_predictions[line_idx], label='GRU')
    plt.xlabel('Time')
    plt.ylabel('Consumption')
    plt.title(f'Off Line {line_idx + 1}')
    plt.legend()
    plt.savefig(f'figure_off_line_{line_idx + 1}.png')
    plt.show()

















