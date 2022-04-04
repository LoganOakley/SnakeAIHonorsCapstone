import matplotlib.pyplot as plt

import pandas

df = pandas.read_csv('SavedFitnesses/Fitnesses_3',names=['Gen', 'Median','Max'])
print(df)

df.plot(x='Gen', y=['Median','Max'], kind = 'line')
plt.show()