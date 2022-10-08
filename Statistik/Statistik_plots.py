import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# python modules needed: tkinter, pandas and matplotlib

data1 = {'Person': ['Willi', 'Penelope', 'Brigitte'],
         'party_fun_value': [100, 200, 50]
         }
df1 = DataFrame(data1, columns=['Person', 'party_fun_value'])

data2 = {'Person': ['Willi', 'Penelope', 'Brigitte'],
         'party_fun_value': [100, 200, 50]
         }
df2 = DataFrame(data2, columns=['Person', 'party_fun_value'])

data3 = {'Person': ['Willi', 'Penelope', 'Brigitte'],
         'party_fun_value': [100, 200, 50]
         }
df3 = DataFrame(data3, columns=['Person', 'party_fun_value'])

root = tk.Tk()

# Balkendiagramm
figure1 = plt.Figure(figsize=(6, 5), dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df1 = df1[['Person', 'party_fun_value']].groupby('Person').sum()
df1.plot(kind='bar', legend=True, ax=ax1)
ax1.set_title('Personen Behagen')

# Liniendiagramm
figure2 = plt.Figure(figsize=(5, 4), dpi=100)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df2 = df2[['Person', 'party_fun_value']].groupby('Person').sum()
df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
ax2.set_title('Personen Behagen')

# Punktediagramm
figure3 = plt.Figure(figsize=(5, 4), dpi=100)
ax3 = figure3.add_subplot(111)
ax3.scatter(df3['Person'], df3['party_fun_value'], color='g')
scatter3 = FigureCanvasTkAgg(figure3, root)
scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
ax3.legend(['party_fun_value'])
ax3.set_xlabel('Person')
ax3.set_title('Personen Behagen')

root.mainloop()
