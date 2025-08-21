# Energy forecasting for a Refrigerator using the consumption values of 1 month.

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import seaborn as sns
register_matplotlib_converters()
from datetime import datetime, timedelta
import pandas as pd
from deep_model import DeepModelTS

d = pd.read_csv("D:\Forecast - Fridge\Fridge - 1Month.csv")   # Reading the data from the .csv file - need to give the exact location
d['Datetime'] = [datetime.strptime(x,'%Y-%m-%d %H:%M') for x in d['Datetime']]
d = d.groupby('Datetime', as_index=False)['Energy_kW'].mean()
d.sort_values('Datetime', inplace=True)

from matplotlib import style
fig = plt.figure()
ax1 = plt.subplot2grid((1,1), (0,0))
style.use('ggplot')
sns.lineplot(x=d["Datetime"], y=d["Energy_kW"], data=d)
sns.set(rc={'figure.figsize':(15,6)})
plt.xlabel("Date")
plt.ylabel("Energy in MW")
plt.grid(True)

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(90)
plt.title("Energy Consumption")
plt.show()
sns.distplot(d["Energy_kW"])
plt.title("Energy Distribution")
plt.grid(True)
plt.show()

deep_learner = DeepModelTS(
    data=d,
    Y_var='Energy_kW',
    lag=20,
    LSTM_layer_depth=64,
    epochs=10,
    train_test_split=0.15
)

model = deep_learner.LSTModel()
prediction_list = deep_learner.predict()

if len(prediction_list) > 0:
    fc = d.tail(len(prediction_list)).copy()
    fc.reset_index(inplace=True)
    fc['Forecast'] = prediction_list

    plt.figure(figsize=(12, 8))
    for dtype in ['Energy_kW', 'Forecast']:
        plt.plot(
            'Datetime',
            dtype,
            data=fc,
            label=dtype,
            alpha=0.8
        )
    plt.legend()
    plt.title("Time Series Forecasting")
    plt.grid(True)
    plt.show()

deep_learner = DeepModelTS(
    data=d,
    Y_var='Energy_kW',
    lag=20,
    LSTM_layer_depth=64,
    epochs=10,
    train_test_split=0
)

deep_learner.LSTModel()
n = 70
prediction_list = deep_learner.forecast(n)
prediction_list = [y[0][0] for y in prediction_list]
Prediction = prediction_list
print("")
print("Prediction Values =")
print(Prediction)

fc = d.tail(400).copy()
fc['type'] = 'Actual Energy'
last_date = max(fc['Datetime'])
hat_frame = pd.DataFrame({
    'Datetime': [last_date + timedelta(hours=x + 1) for x in range(n)],
    'Energy_kW': prediction_list,
    'type': 'Forecast'
})

fc = fc.append(hat_frame)
fc.reset_index(inplace=True, drop=True)
plt.figure(figsize=(12, 8))
for col_type in ['Actual Energy', 'Forecast']:
    plt.plot(
        'Datetime',
        'Energy_kW',
        data=fc[fc['type'] == col_type],
        label=col_type
    )
plt.legend()
plt.title("Future Forecasting")
plt.grid(True)
plt.show()