import matplotlib.pyplot as plt

import KerasNetwork
import pandas

import tensorflow as tf

df = pandas.read_csv('SavedFitnesses/Fitnesses_3',names=['Gen', 'Median','Max'])
print(df)

df.plot(x='Gen', y=['Median','Max'], kind = 'line')
plt.grid()
plt.ylabel('Fitness')
plt.locator_params ('x', nbins = 40)
plt.show()

