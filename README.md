# Rubiks Cube Solver
This is a Python program to solve a 3x3x3 Rubik's Cube. It
uses a vector representation of the Pieces, which means rotations
are represented by simple matrix math. The algorithm used to solve
the cube is just the Layer-by-Layer approach.

## Dependencies

Below are the dependencies of the project:
* Python 3.7
* numpy
* matplotlib

## Project Structure

Below is the project structure:
* main.py : The entry point for the program
* maths : Folder for the maths modules
    - points.py : Module defining a point in 3D space
    - matrices.py : Module defining a 3x3 matrix
* rubiks : Folder for the Rubik's Cube
    - cube.py : Defines the Rubik's Cube
    - piece.py : Defines a piece (cubie) of the cube
    - solver.py : Defines a solver class for the cube
    - draw.py : Defines a drawing class for the cube