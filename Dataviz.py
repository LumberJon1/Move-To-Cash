import matplotlib as mpl
import matplotlib.pyplot as plt
# import Main

# chart_data = Main.generate_chart_data()

test_data = [
    ['Jul 05, 2017', '$100017.57'],
    ['Jul 06, 2017', '$99480.29'],
    ['Jul 07, 2017', '$99707.28'],
    ['Jul 10, 2017', '$99790.19'],
    ['Jul 11, 2017', '$99873.65'],
    ['Jul 12, 2017', '$100472.82'],
    ['Jul 13, 2017', '$100591.43'],
    ['Jul 14, 2017', '$100979.24'],
    ['Jul 17, 2017', '$100997.13'],
    ['Jul 18, 2017', '$101138.55']
]

# Define the arrays to hold balances and dates
balances = []
dates = []

for pair in test_data:
    balances.append(pair[1])
    dates.append(pair[0])

print(test_data)

plt.plot(test_data)
plt.ylabel("Account Balance")
plt.xlabel("Date")
plt.show()
