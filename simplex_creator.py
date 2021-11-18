import numpy as np
import diode
import dionysus


# data = np.loadtxt("County_Location.csv", delimiter=',', usecols=range(1,3))

# simplices = diode.fill_alpha_shapes(data)

# f = dionysus.Filtration(simplices)
# print(f)

t = np.linspace(0, 2 * np.pi, 40)
x = np.sin(t)
y = np.sin(t) * np.cos(t)
data = np.column_stack((x,y))
simplices = diode.fill_alpha_shapes(data)

print(simplices)
f = dionysus.Filtration(simplices)
print(f)
