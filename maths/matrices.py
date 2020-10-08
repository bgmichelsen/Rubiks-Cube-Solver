"""
===============================================================
                        Matrix class
===============================================================

Defines the Matrix3D class

"""

from maths.points import Point3D
from numbers import Number


class Matrix3D:
    """
    A class for working with 3x3x3 matrices
    """

    def __init__(self, *args):
        """
        :param args: Args for entering the data into the matrix
                     must be numeric and must have 9 elements
        """

        self.data = None

        if len(args) == 9:
            # Args entered: 1, 2, 3, 4, 5, 6, 7, 8, 9
            self.data = list(args)
        elif len(args) == 3:
            # Args entered: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            self.data = [elem for sub in args for elem in sub]
        else:
            # Args entered: [1, 2, 3, 4, 5, 6, 7, 8, 9]
            self.data = args[0]

        if len(self.data) != 9:
            raise ValueError(f"Matrix3D must have 9 elements, received {args}")

        if any(elem is None for elem in self.data):
            raise ValueError(f"Matrix3D does not accept None type")

    def rows(self):
        """
        Get the rows in the matrix

        :return: The rows in the matrix
        """

        yield self.data[0:3]
        yield self.data[3:6]
        yield self.data[6:9]

    def cols(self):
        """
        Get the columns in the matrix

        :return: The columns in the matrix
        """

        yield self.data[0:9:3]
        yield self.data[1:9:3]
        yield self.data[2:9:3]

    def det(self):
        """
        Find the determinant of the matrix

        :return: The determinant
        """

        a = self.data[0]*(self.data[4]*self.data[8] - self.data[5]*self.data[7])
        b = self.data[1]*(self.data[3]*self.data[8] - self.data[5]*self.data[6])
        c = self.data[2]*(self.data[3]*self.data[7] - self.data[4]*self.data[6])

        return a - b + c

    def __add__(self, other):
        """
        Add operator

        :param other: The other component to add
        :return: A matrix of the sum
        """

        assert type(other) == Matrix3D

        return Matrix3D(a + b for a, b in zip(self.vals, other.vals))

    def __sub__(self, other):
        """
        Subtraction operator

        :param other: The other component to subtract
        :return: A matrix of the sum
        """

        assert type(other) == Matrix3D

        return Matrix3D(a - b for a, b in zip(self.vals, other.vals))

    def __mul__(self, other):
        """
        Multiplication operator

        :param other: The other component to multiply
        :return:
        """

        if isinstance(other, Point3D):
            return Point3D(other.dot(Point3D(row)) for row in self.rows())
        elif isinstance(other, Matrix3D):
            return Matrix3D(Point3D(row).dot(Point3D(col)) for row in self.rows \
                            for col in self.cols())
        elif isinstance(other, Number):
            return Matrix3D(a*other for a in self.data)
        else:
            raise ValueError(f"Matrix3D can only multiply the following types: "\
                             "Point3D, Matrix3D, Number")

    def __str__(self):
        return "[{}, {}, {}\n"\
                "{}, {}, {}\n"\
                "{}, {}, {}]".format(*self.data)

    def __repr__(self):
        return "Matrix3D" + str(self)


# Identity matrix
IDENTITY_MATRIX = Matrix3D((1, 0, 0),
                           (0, 1, 0),
                           (0, 0, 1))

"""
90 Degree Rotation Matrices

CW is Clockwise and CC is Counter Clockwise
"""

ROT_X_CW = Matrix3D(((1, 0, 0),
                     (0, 0, 1),
                     (0, -1, 0)))
ROT_X_CC = Matrix3D(((1, 0, 0),
                     (0, 0, -1),
                     (0, 1, 0)))

ROT_Y_CW = Matrix3D((0, 0, -1),
                    (0, 1, 0),
                    (1, 0, 0))
ROT_Y_CC = Matrix3D((0, 0, 1),
                    (0, 1, 0),
                    (-1, 0, 0))

ROT_Z_CW = Matrix3D((0, 1, 0),
                    (-1, 0, 0),
                    (0, 0, 1))
ROT_Z_CC = Matrix3D((0, -1, 0),
                    (1, 0, 0),
                    (0, 0, 1))
