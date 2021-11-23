import numpy as np
import gudhi as gd
import gudhi.representations
import matplotlib.pyplot as plt


num_pts = 1000
r       = 3.5

X = np.empty([num_pts,2])
x, y = np.random.uniform(), np.random.uniform()
for i in range(num_pts):
    X[i,:] = [x, y]
    x = (X[i,0] + r * X[i,1] * (1-X[i,1])) % 1.
    y = (X[i,1] + r * x * (1-x)) % 1.


plt.scatter(X[:,0], X[:,1], s=3)
plt.show()

acX = gd.AlphaComplex(points=X).create_simplex_tree()
dgmX = acX.persistence()

# gd.plot_persistence_diagram(dgmX)

LS = gd.representations.Landscape(resolution=1000)
L = LS.fit_transform([acX.persistence_intervals_in_dimension(1)])

plt.plot(L[0][:1000])
plt.plot(L[0][1000:2000])
plt.plot(L[0][2000:3000])
plt.title("Landscape")
plt.show()

SH = gd.representations.Silhouette(resolution=1000, weight=lambda x: np.power(x[1]-x[0],1))
sh = SH.fit_transform([acX.persistence_intervals_in_dimension(1)])
plt.plot(sh[0])
plt.title("Silhouette")
plt.show()

PI = gd.representations.PersistenceImage(bandwidth=1e-4, weight=lambda x: x[1]**2, \
                                         im_range=[0,.004,0,.004], resolution=[100,100])
pi = PI.fit_transform([acX.persistence_intervals_in_dimension(1)])

plt.imshow(np.flip(np.reshape(pi[0], [100,100]), 0))
plt.title("Persistence Image")
plt.show()