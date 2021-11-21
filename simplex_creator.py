import numpy as np
import diode
import dionysus


data = np.loadtxt("County_Location.csv", delimiter=',', usecols=range(1,3))
lst = [1e-1] * 50
lst2 = [1e-1] * 50
lst0 = np.append(lst, lst2)

lst1 = [1] * 100
data_3D = np.column_stack((data,lst0))
print(data_3D)

simplices = diode.fill_alpha_shapes(data_3D)
print(simplices)

data_3D_weighted = np.column_stack((data_3D,lst1))
print(data_3D_weighted)
# simplices = diode.fill_weighted_alpha_shapes(data_3D)
# print(simplices)

f = dionysus.Filtration(simplices)
print(f)
