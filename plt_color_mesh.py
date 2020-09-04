import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

from data_process import get_interval, get_xy_size, plt_color_mesh_process


def plt_color_mesh(filename, title='max_color_mesh'):
    ideal_x_arr, ideal_y_arr, x_index_arr, y_index_arr, max_offset_arr = plt_color_mesh_process(filename)
    x_interval = get_interval(ideal_x_arr)
    y_interval = get_interval(ideal_y_arr)
    x_min, x_max, y_min, y_max = get_xy_size(ideal_x_arr, ideal_y_arr)
    x_tap_num = int(round(x_max/x_interval) + 1)
    y_tap_num = int(round(y_max/y_interval) + 1)
    linspace_x = np.linspace(- x_interval/2, x_max + x_interval/2, x_tap_num + 1)
    linspace_y = np.linspace(- y_interval/2, y_max + y_interval/2, y_tap_num + 1)
    meshgrid_x, meshgrid_y= np.meshgrid(linspace_x, linspace_y)
    # shape of C is printed in (rows, cols) order, whereas X represents columns and Y rows
    meshgrid_z = np.full((len(linspace_y), len(linspace_x)), np.inf)
    for i, max_offset in enumerate(max_offset_arr):
        meshgrid_z[y_index_arr[i]][x_index_arr[i]] = max_offset
    bounds = np.linspace(0.0, 4.5, 10)
    norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
    fig, ax = plt.subplots(figsize=(8,6))
    fig.canvas.set_window_title(title)
    ax.set_title(title)
    ax.set_xlabel('Width(mm)')
    ax.set_ylabel('Length(mm)')
    ax.invert_yaxis()
    mesh = ax.pcolormesh(meshgrid_x, meshgrid_y, meshgrid_z, norm=norm, cmap='jet', color=(0,0,0))
    plt.colorbar(mesh, ax=ax, extend = 'max', orientation = 'vertical')
    fig.tight_layout()
    # plt.show()
    return fig, ax
    # fig.savefig(filename[:-18] + title + '.png')
        # bounds = numpy.linspace(0.0, 4.5, 10)
        # norm = colors.BoundaryNorm(boundaries = bounds, ncolors = 256)
        # pcm = plt.pcolormesh(x - xPace/2, y - yPace/2, z, norm = norm, cmap = 'jet', color =(0, 0, 0))
        # cb = fig.colorbar(pcm, ax = ax, extend = 'max', orientation = 'vertical')
        # cb.set_label('Accuracy(mm)', labelpad = -70)
