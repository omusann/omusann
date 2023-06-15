import matplotlib.pyplot as plt

# Data for the x-axis (time)
x = [1, 2, 3, 4, 5]

# Data for the y-axis (values)
y = [5, 3, 8, 4, 6]

# Create the line graph
plt.plot(x, y)

# Add labels and title
plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Line Graph')

# Display the graph
plt.show()
