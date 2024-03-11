import matplotlib.pyplot as plt
import numpy as np

# Sample data points
x = np.random.rand(50) * 10
y = np.random.rand(50) * 10
z = np.random.rand(50) * 10

# Create a new figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plotting the data points
ax.scatter(x, y, z, c='g', marker='o', s=50)  # Using green color with 'o' marker

# Adding labels
ax.text(2, 2, 2, 'Wolf')
ax.text(4, 4, 4, 'Dog')
ax.text(6, 6, 6, 'Cat')
ax.text(8, 8, 8, 'Banana')
ax.text(9, 9, 9, 'Apple')
ax.text(3, 4, 4, 'Query: Puppy', color='blue')  # Highlighting the 'Query: Kitten' label

# Setting the axis labels
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# Display the plot
plt.show()
