import numpy as np
import plotille

# Generate data
X = np.sort(np.random.normal(size=1000))

# Create the plot
fig = plotille.Figure()
fig.width = 60
fig.height = 30
fig.set_x_limits(min_=-3, max_=3)
fig.set_y_limits(min_=-1, max_=1)
fig.color_mode = 'byte'
fig.plot([-0.5, 1], [-1, 1], lc=25, label='First line')
fig.scatter(X, np.sin(X), lc=100, label='sin')
fig.plot(X, (X+2)**2 , lc=200, label='square')

# Save the plot to a text file
with open("plot_output.txt", "w") as f:
    f.write(fig.show(legend=True))
