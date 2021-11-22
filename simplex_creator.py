import numpy as np
import diode
import dionysus as d
import json

def sample_points(data):

    return

def calculate_total_homology(points):
    simplices = diode.fill_alpha_shapes(points)
    f = d.Filtration(simplices)
    m = d.homology_persistence(f)
    # for i,c in enumerate(m):
    #     print(i, c)

    dgms = d.init_diagrams(m, f)
    print(dgms)
    zero_total_homology = 0
    first_total_homology = 0
    for i, dgm in enumerate(dgms):
        for pt in dgm:
            if i==0 and not pt.death == float("inf"):
                zero_total_homology+= ((pt.birth-pt.death)**2)
            if i==1:
                first_total_homology+= ((pt.birth-pt.death)**2)
            print(i, pt.birth, pt.death)
    print(zero_total_homology)
    print(first_total_homology)
    
    return zero_total_homology, first_total_homology

data = np.loadtxt("County_Location.csv", delimiter=',', usecols=range(1,3))
calculate_total_homology(data)

with open('County_Cases.json') as f:
    data = json.load(f)
    print(data)

# lst = [1e-1] * 50
# lst2 = [1e-2] * 50
# lst0 = np.append(lst, lst2)

# lst1 = [1] * 100
# data_3D = np.column_stack((data,lst0))
# print(data_3D)

# simplices = diode.fill_alpha_shapes(data_3D)
# simplices = diode.fill_alpha_shapes(data)
# print(simplices)

# data_3D_weighted = np.column_stack((data_3D,lst1))
# print(data_3D_weighted)
# simplices = diode.fill_weighted_alpha_shapes(data_3D)
# print(simplices)

# f = d.Filtration(simplices)
# print(f)