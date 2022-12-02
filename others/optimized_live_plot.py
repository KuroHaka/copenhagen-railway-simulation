# importing libraries
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
# creating initial data values
# of x and y

# to run GUI event loop
plt.ion()

# here we are creating sub plots
figure, ax = plt.subplots(figsize=(5, 4))
ax.axis(xmin=-15,xmax=80,ymax=40,ymin=-3)
dot, = ax.plot(0, 0)

# setting title
plt.title("moving point", fontsize=20)

# setting x-axis label and y-axis label
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

speed_list = [
        0.000,
        0.000,
        0.000,
        0.000,
        1.500,
        3.000,
        4.500,
        6.000,
        7.500,
        9.000,
        10.500,
        12.000,
        13.500,
        15.000,
        16.500,
        18.000,
        19.500,
        21.000,
        22.500,
        24.000,
        25.500,
        27.000,
        28.500,
        30.000,
        31.500,
        33.000,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        33.330,
        31.930,
        30.530,
        29.130,
        27.730,
        26.330,
        24.930,
        23.530,
        22.130,
        20.730,
        19.330,
        17.930,
        16.530,
        15.130,
        13.730,
        12.330,
        10.930,
        9.530,
        8.130,
        6.730,
        5.330,
        3.930,
        2.530,
        1.340,
        0.329,
        0,
        0,
        0
    ]
x = list(range(-3,len(speed_list)-3))
# Loop
back = True
while True:
    if back:
        dot._marker = MarkerStyle('o')
    else:
        dot._marker = MarkerStyle('o',fillstyle='none')
    back = not back
    for i in range(len(x)):
        # changing value
        new_y = speed_list[i]
        new_x = x[i]

        # updating data values
        dot.set_xdata(new_x)
        dot.set_ydata(new_y)

        # drawing updated values
        figure.canvas.draw()

        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        figure.canvas.flush_events()

    x.reverse()
    speed_list.reverse()
