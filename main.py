"""

=========================================================================
                        Rubik's Cube Solver Program
=========================================================================

A Python program to solve a 3x3x3 Rubik's Cubes. Draws the cube using MATPLOTLIB. Uses the
Layer-by-Layer approach to solve the cube.

Dependencies:
- Python 3.7
- matplotlib
- numpy

Directories and Files:
- maths
    * matrices.py : file that defines a Matrix class and its functions
    * points.py : file that defines a Point class and its functions
- rubiks
    * cube.py : file that defines the Cube class
    * piece.py : file that defines the Piece class and its functions
    * solver.py : file that defines the Solver class and its functions
    * draw.py : file that defines the Drawing class and functions
- main.py (this file) : defines the entry function for the program

"""
# TODO: Convert rubiks.draw to OOP
# TODO: Create the other classes
# TODO: Implement main program

# Import necessary internal modules
from rubiks.draw import Drawing
from rubiks.cube import Cube

def main():
    """
    Main function to run the program

    :return: None
    """

    cube = Cube()

    window = Drawing(cube, _sizes=(0.25, 0.25, 0.25))
    window.init_context()

    i = 0
    while i <= 1000 and window.context_opened():
        window.update()
        i += 1
    window.keep_open()


if __name__ == "__main__":
    main()