##baisakhi's code
def plot_sphere(ax):
    x_abs_center = x[0]
    y_abs_center = y[0]
    z_abs_center = z[0]

    N = 500
    radius = trust/200
    stride = 1
    u = np.linspace(0, 2*np.pi, N)
    v = np.linspace(0, np.pi, N)
    x = np.outer(np.cos(u), np.sin(v)) * radius + x_abs_center
    y = np.outer(np.sin(u), np.sin(v)) * radius + y_abs_center
    z = np.outer(np.ones(np.size(u)), np.cos(v)) * radius + z_abs_center
    ax.plot_wireframe(x, y, z, alpha=0.1)
