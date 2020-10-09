"""
============================================================
                    Point Class
============================================================

Defines the Point3D class

"""

from numbers import Number


class Point3D:
    """
    A class for working with 3D points
    """

    def __init__(self, x, y=None, z=None):
        """
        :param x: Tuple of all the coords or just the x coord
        :param y: y coord of point
        :param z: z coord of point
        """

        if isinstance(x, (tuple, list)):
            assert len(x) == 3

            self.x = x[0]
            self.y = x[1]
            self.z = x[2]
        else:
            self.x = x
            self.y = y
            self.z = z

        if any(elem is None for elem in [self.x, self.y, self.z]):
            raise ValueError(f"Point does not accept None types")

    def get_coords(self):
        """
        :return: The coordinates stored in the Point
        """

        return self.x, self.y, self.z

    def dot(self, other):
        """
        Calcualte the dot product of the point and another point

        :param other: The other point
        :return: The dot product of the two points
        """

        assert type(other) == Point3D

        return self.x*other.x + self.y*other.y + self.z*other.z

    def cross(self, other):
        """
        Calcualte the cross product of the point and another point

        :param other: The other point
        :return: The cross product of the two points (a new point)
        """

        assert type(other) == Point3D

        c_x = self.y*other.z - self.z*other.y
        c_y = self.z*other.x - self.x*other.z
        c_z = self.x*other.y - self.y*other.x

        return Point3D(c_x, c_y, c_z)

    def __add__(self, other):
        """
        Add operator

        :param other: Other point to add
        :return: The addition of the point and another point
        """

        if isinstance(other, Point3D):
            c_x = self.x + other.x
            c_y = self.y + other.y
            c_z = self.z + other.z
        elif isinstance(other, (tuple, list)):
            assert len(other) == 3

            c_x = self.x + other[0]
            c_y = self.y + other[1]
            c_z = self.z + other[2]
        else:
            raise ValueError(f"Point3D can only add the following types: " \
                                 "Point3D, tuple, list")

        return Point3D(c_x, c_y, c_z)

    def __sub__(self, other):
        """
        Subtract operator

        :param other: Other point to subtract
        :return: The subtraction of the point and another point
        """

        if isinstance(other, Point3D):
            c_x = self.x - other.x
            c_y = self.y - other.y
            c_z = self.z - other.z
        elif isinstance(other, (tuple, list)):
            assert len(other) == 3

            c_x = self.x - other[0]
            c_y = self.y - other[1]
            c_z = self.z - other[2]
        else:
            raise ValueError(f"Point3D can only subtract the following types: "\
                             "Point3D, tuple, list")

        return Point3D(c_x, c_y, c_z)

    def __mul__(self, other):
        """
        Multiplication operator

        :param other: Other point to multiply
        :return: The product of the two points
        """

        if isinstance(other, Point3D):
            c_x = self.x*other.x
            c_y = self.y*other.y
            c_z = self.z*other.z
        elif isinstance(other, (tuple, list)):
            assert len(other) == 3

            c_x = self.x*other[0]
            c_y = self.y*other[1]
            c_z = self.z*other[2]
        elif isinstance(other, Number):
            c_x = self.x*other
            c_y = self.y*other
            c_z = self.z*other
        else:
            raise ValueError(f"Point3D can only be multiplied by the following types: "\
                             "Point3D, tuple, list, or Number")

        return Point3D(c_x, c_y, c_z)

    def __eq__(self, other):
        """
        Check if values are equal

        :param other: The other object (must be tuple, list, or
        :return: If the objects are equal
        """

        if isinstance(other, (tuple, list)):
            assert len(other) == 3

            return self.x == other[0] and self.y == other[1] and self.z == other[2]
        return (isinstance(other, Point3D) and self.x == other.x \
                and self.y == other.y and self.z == other.z)

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def __repr__(self):
        return "Point" + str(self)
