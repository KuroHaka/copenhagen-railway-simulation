import matplotlib.pyplot as plt
import csv

train = []
with open('others\plotters\data\distances_train.txt','r') as f:
    for l in f:
        train.append(float(l.rstrip('\n')))
carrier = []
with open('others\plotters\data\distances_carrier.txt','r') as f:
    for l in f:
        carrier.append(float(l.rstrip('\n')))

x = list(range(0,len(train)*2,2))
train_reach = train.index(max(train))*2
train_max = max(train)
carrier_reach = carrier.index(max(carrier))*2
carrier_max = max(carrier)
fig, ax = plt.subplots(dpi=100)
ax.grid(color='black', linestyle='-', linewidth=0.1)
ax.plot(x, train, color ='red', linewidth=1, label="train")
ax.plot(x, carrier, color ='green', linewidth=1, label="carrier")
ax.vlines(train_reach, 0, train_max, linestyles ="dashed", colors ="red")
ax.vlines(carrier_reach, 0, carrier_max, linestyles ="dashed", colors ="green")
ax.set_title("Commuting time over 3 stations")
ax.set_xlabel("time(s)")
ax.set_ylabel("distance(m)")
leg = ax.legend()
for legobj in leg.legendHandles:
    legobj.set_linewidth(3.0)
plt.show()