import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter

csv_file = sys.argv[1]
cpu_data = pd.read_csv(csv_file)
cpu_data['timestamp'] = pd.to_datetime(cpu_data['timestamp'])

plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5, label='Temperature data')

frac_value = 0.025 
loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'], frac=frac_value)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-', label='LOESS smoothing line')

kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
kalman_data = kalman_data.to_numpy()

initial_state = kalman_data[0]

observation_covariance = np.diag([10, 10, 10, 10]) ** 2
transition_covariance = np.diag([1, 1, 1, 1]) ** 2
transition = [[0.94, 0.5, 0.2, -0.001],
              [0.1, 0.4, 2.1, 0],
              [0, 0, 0.94, 0],
              [0, 0, 0, 1]]

kf = KalmanFilter(transition_matrices=transition, 
                  observation_covariance=observation_covariance,
                  transition_covariance=transition_covariance, 
                  initial_state_mean=initial_state)

mean_states, _ = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], mean_states[:, 0], 'g-', label='Kalman Smoothing Line')

plt.legend()
plt.savefig('cpu.svg')