"""
==========================================================================
                                Piece Class
==========================================================================

Defines the Piece class and additional data for Pieces (colors and piece types)

"""

# Import necessary modules
from maths.points import Point3D
from maths.matrices import Matrix3D, IDENTITY_MATRIX, ROT_X_CC


# Colors on a Rubik's Cube
class RubiksColors:
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    WHITE = 'white'
    ORANGE = 'orange'
    BLANK = 'black'

    _VALS_ = [RED, BLUE, GREEN, YELLOW, WHITE, ORANGE, BLANK]


# Rubik's Piece Types
class PieceTypes:
    EDGE = 0
    CORNER = 1
    CENTER = 2

    _VALS_ = [EDGE, CORNER, CENTER]


class Piece:
    """
    Class for a piece (cubie) in a Rubik's cube

    Position is a 3D point relative to the center of the cube.
    Coordinates can be -1, 0, or 1 [EX: (-1, -1, 0)]

    Colors are a list of RubiksColors enum in a tuple.
    The first element corresponds to the X axis, the second the Y axis,
    and the third the Z axis.
    """

    def __init__(self, _pos, _colors):
        """
        :param _pos: The 3D position of the
        :param _colors: The colors on the piece
        """

        if isinstance(_pos, Point3D):
            self.pos = _pos
        elif isinstance(_pos, (tuple, list)):
            self.pos = Point3D(_pos)
        else:
            raise ValueError(f"Piece only accepts the following types for _pos: "\
                             "Point3D, tuple, list")

        if isinstance(_colors, list):
            if any(elem not in RubiksColors._VALS_ for elem in _colors):
                raise ValueError(f"Please use RubiksColors enum values for colors")

            assert len(_colors) == 3

            self.colors = _colors
        else:
            raise ValueError(f"Piece class only accepts lists for _color")

        self.type = self.__set_type__()

    def __set_type__(self):
        """
        Determines the type of piece

        :return: The determined piece type
        """

        if self.colors.count(RubiksColors.BLANK) == 2:
            return PieceTypes.CENTER
        elif self.colors.count(RubiksColors.BLANK) == 1:
            return PieceTypes.EDGE
        else:
            return PieceTypes.CORNER

    def __str__(self):
        return "Pos: " + str(self.pos) + ", Colors: {}".format(self.colors) + \
               ", Type: {}".format(self.type)

    def __repr__(self):
        return "Piece" + str(self)

    def get_piece_type(self):
        """
        :return: The piece type
        """

        return self.type

    def rotate(self, matrix):
        """
        Rotate the piece vector given a rotation matrix

        :param matrix: The matrix to rotate by
        :return: None
        """

        assert type(matrix) == Matrix3D
        
        before = self.pos
        self.pos = matrix * self.pos

        # Return if there was no rotation
        if self.pos == before:
            return

        # Get the vector representing the axis of rotation
        # Since it is a 90 degree rotation, we can just use the main diagonal of
        # The rotation matrix
        axis = matrix.diag()
        
        # Swap colors 
        i, j = (x for x, elem in enumerate(axis) if elem == 0)
        self.colors[i], self.colors[j] = self.colors[j], self.colors[i]

