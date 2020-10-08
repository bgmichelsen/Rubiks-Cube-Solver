"""

=========================================================================================
                        Drawing class for the cube
=========================================================================================

Dependencies:
- Python 3.7
- matplotlib
- numpy

"""

# Import external necessary modules
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D # Registers 3D projection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection # For drawing the cuboids

# Import internal necessary modules
from rubiks.cube import Cube


class Drawing:
    """
    Class for handling drawing of the cube.
    """

    def __init__(self, _cube, _grid=False, _axes=False, _sizes=(1, 1, 1)):
        """
        :param _cube: The cube to draw
        :param _grid: Boolean for if the grid should be displayed
        :param _axes: Boolean for if the axes should be displayed
        :param _sizes: Tuple of sizes in the X, Y, Z directions
        """

        assert _cube is not None
        assert type(_cube) is Cube

        assert type(_sizes) == tuple
        assert len(_sizes) == 3

        self.cube = _cube
        self.grid = _grid
        self.axes = _axes
        self.size = _sizes

        self.context = None
        self.CONTEXT_OPEN = False

    def init_context(self):
        """
        Create an initialize the window

        :return: None
        """

        self.__create_context__()
        self.CONTEXT_OPEN = True

    def draw(self):
        """
        Updates the graph with new data

        :return: None
        """

        positions = [
            # Bottom back edge
            (-1, -1, -1),
            (-1, 0, -1),
            (-1, 1, -1),

            # Bottom middle
            (0, -1, -1),
            (0, 0, -1),
            (0, 1, -1),

            # Bottom front edge
            (1, -1, -1),
            (1, 0, -1),
            (1, 1, -1),

            # Middle back
            (-1, -1, 0),
            (-1, 0, 0),
            (-1, 1, 0),

            # Middle middle
            (0, -1, 0),
            (0, 1, 0),

            # Middle front
            (1, -1, 0),
            (1, 0, 0),
            (1, 1, 0),

            # Top back
            (-1, -1, 1),
            (-1, 0, 1),
            (-1, 1, 1),

            # Top middle
            (0, -1, 1),
            (0, 0, 1),
            (0, 1, 1),

            # Top front
            (1, -1, 1),
            (1, 0, 1),
            (1, 1, 1)
        ]

        colors = [
            # Bottom back
            ('red', 'blue', 'white'),
            ('red', 'black', 'white'),
            ('red', 'green', 'white'),

            # Bottom middle
            ('red', 'blue', 'black'),
            ('red', 'black', 'black'),
            ('red', 'green', 'black'),

            # Bottom front
            ('red', 'blue', 'yellow'),
            ('red', 'black', 'yellow'),
            ('red', 'green', 'yellow'),

            # Middle back
            ('black', 'blue', 'white'),
            ('black', 'black', 'white'),
            ('black', 'green', 'white'),

            # Middle middle
            ('black', 'blue', 'black'),
            ('black', 'green', 'black'),

            # Middle front
            ('black', 'blue', 'yellow'),
            ('black', 'black', 'yellow'),
            ('black', 'green', 'yellow'),

            # Top back
            ('orange', 'blue', 'white'),
            ('orange', 'black', 'white'),
            ('orange', 'green', 'white'),

            # Top middle
            ('orange', 'blue', 'black'),
            ('orange', 'black', 'black'),
            ('orange', 'green', 'black'),

            # Top front
            ('orange', 'blue', 'yellow'),
            ('orange', 'black', 'yellow'),
            ('orange', 'green', 'yellow')
        ]

        # Create the voxels
        for p, c in zip(positions, colors):
            voxel = self.__create_voxel__(self.__create_cuboid__(p, c))
            self.context.add_collection3d(voxel)

    def update(self, _pause=0.001):
        # Redraw the plot with new data if window is still open
        self.draw()
        if plt.get_fignums():
            plt.draw()
            plt.pause(_pause)
            self.context.cla()
            self.__set_context__()
        else:
            self.CONTEXT_OPEN = False

    def keep_open(self):
        """
        Keeps the window open after completion

        :return: None
        """

        if self.CONTEXT_OPEN and plt.get_fignums():
            self.draw()
            plt.show()

    def context_opened(self):
        return self.CONTEXT_OPEN

    def __create_context__(self):
        """
        Create the drawing context

        :return: Context of the plot
        """

        fig = plt.figure("Rubik's Cube")
        self.context = fig.gca(projection='3d')
        self.__set_context__()

    def __set_context__(self):
        """"
        Updates the context of the plot

        :return: None
        """

        assert self.context is not None

        self.context.set_xlabel('X')
        self.context.set_ylabel('Y')
        self.context.set_zlabel('Z')
        self.context.set_xbound(-1, 1)
        self.context.set_ybound(-1, 1)
        self.context.set_zbound(-1, 1)
        self.context._axis3don = self.axes
        self.context.grid(self.grid)

    def __cubify__(self, coords):
        """
        Create a list of vertices to draw cuboids

        :param coords: Coordinates of cuboids
        :return: List of vertices to draw the cuboid
        """

        assert coords is not None

        # Unit cube for determining the shape of the cuboid
        unit_cube = [
            [[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],  # Bottom Face
            [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],  # Left Face
            [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],  # Front Face
            [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],  # Back Face
            [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],  # Right Face
            [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]  # Top Face
        ]
        unit_cube = np.array(unit_cube).astype(float)

        # Resize cube based on given size and add coords
        for i in range(len(self.size)):
            unit_cube[:, :, i] *= self.size[i]

        # Resize the coords based on the size factor
        resized_coords = (coords[0] * self.size[0], coords[1] * self.size[1], coords[2] * self.size[2])

        # Add the coords
        cubie = unit_cube + np.array(resized_coords)
        return cubie

    def __create_cuboid__(self, coords, colors):
        """
        Create a cuboid with the given coordinates and colors

        :param coords: coordinates of the cuboid (tuple)
        :param colors: colors of the cuboid (string)
        :return: Tuple of vertices and colors
        """

        assert coords is not None
        assert type(coords) is tuple and len(coords) == 3

        assert colors is not None
        assert type(colors) is tuple and len(colors) == 3

        # Create the cubified position data
        vertices = self.__cubify__(coords)

        # We only want to color the three outside pieces of a cuboid
        full_colors = [colors[0], colors[1], colors[2], 'black', 'black', 'black']

        if coords[1] > 0:
            full_colors[1], full_colors[4] = full_colors[4], full_colors[1]
        if coords[0] < 0:
            full_colors[2], full_colors[3] = full_colors[3], full_colors[2]
        if coords[2] > 0:
            full_colors[0], full_colors[5] = full_colors[5], full_colors[0]

        return vertices, full_colors

    def __create_voxel__(self, cuboids):
        """
        Create voxels out of a list of cuboids

        :param cuboids: The cuboids to be drawn
        :return: Poly3DCollection to represent a voxel
        """

        assert cuboids is not None

        return Poly3DCollection(np.array(cuboids[0]), facecolors=np.array(cuboids[1]), edgecolors='k')

