import time
import pandas as pd
import numpy as np
from implementations import all_implementations

start_time = time.time()
max_time = 60  # Maximum allowable time in seconds
data = []

num_repeats = 100  # Initial guess
array_size = 1000

while True:
    elapsed_time = time.time() - start_time
    if elapsed_time >= max_time:
        break

    for sort in all_implementations:
        if time.time() - start_time >= max_time:
            break

        for i in range(num_repeats):
            if time.time() - start_time >= max_time:
                break

            random_array = np.random.randint(0, 100000, size=array_size)
            st = time.time()
            res = sort(random_array)
            en = time.time()

            data.append({
                'sort_type': sort.__name__,
                'time': en - st,
                'random_state': i,
            })

data_df = pd.DataFrame(data)

data_df.to_csv('data.csv', index=False)
