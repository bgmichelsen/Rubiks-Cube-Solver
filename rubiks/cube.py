"""
============================================================
                    Cube Class
============================================================

Defines the Cube class and helper data.

"""

# Import necessary modules
from rubiks.piece import Piece, RubiksColors as Colors
from maths.points import Point3D
from maths.matrices import Matrix3D, ROT_X_CC, ROT_X_CW, ROT_Y_CC, ROT_Y_CW, ROT_Z_CC, ROT_Z_CW

# Helper Points for representing the different pieces
FRONT   = Point3D((1, 0, 0))
BACK    = Point3D((-1, 0, 0))
LEFT    = Point3D((0, -1, 0))
RIGHT   = Point3D((0, 1, 0))
UP      = Point3D((0, 0, 1))
DOWN    = Point3D((0, 0, -1))

# Helper str for valid move symbols
VALID_NOTATION = 'L Li R Ri F Fi B Bi U Ui D Di'


class Cube:
    """
    A class defining a 3x3x3 Rubik's Cube

    The cube is made out of a tuple of Piece types. Each Piece can be an EDGE, CORNER, or CENTER,
    depending on how many colors the piece has. Each piece also has a position associated with it.
    The positions are set up in a 3D coordinate system, where the center of the cube is the origin.
    The axes go from -1 to 1, so a piece can have a -1, 0, or 1 for each coordinate [EX: (-1, 0, 1)].
    the cube is printed in the following way:

          U U U
          U U U
          U U U
    L L L F F F R R R B B B
    L L L F F F R R R B B B
    L L L F F F R R R B B B
          D D D
          D D D

    Where:
        - T = Top Face
        - F = Front Face
        - B = Bottom Face
        - L = Left Face
        - R = Right Face
    """

    def __init__(self):
        """
        Just need to set up the pieces
        """

        self.faces = (
            Piece(_pos=FRONT, _colors=[Colors.YELLOW, Colors.BLANK, Colors.BLANK]),
            Piece(_pos=BACK, _colors=[Colors.WHITE, Colors.BLANK, Colors.BLANK]),
            Piece(_pos=LEFT, _colors=[Colors.BLANK, Colors.BLUE, Colors.BLANK]),
            Piece(_pos=RIGHT, _colors=[Colors.BLANK, Colors.GREEN, Colors.BLANK]),
            Piece(_pos=UP, _colors=[Colors.BLANK, Colors.BLANK, Colors.ORANGE]),
            Piece(_pos=DOWN, _colors=[Colors.BLANK, Colors.BLANK, Colors.RED])
        )

        self.edges = (
            Piece(_pos=FRONT+LEFT, _colors=[Colors.YELLOW, Colors.BLUE, Colors.BLANK]),
            Piece(_pos=FRONT+RIGHT, _colors=[Colors.YELLOW, Colors.GREEN, Colors.BLANK]),
            Piece(_pos=FRONT+UP, _colors=[Colors.YELLOW, Colors.BLANK, Colors.ORANGE]),
            Piece(_pos=FRONT+DOWN, _colors=[Colors.YELLOW, Colors.BLANK, Colors.RED]),
            Piece(_pos=BACK+LEFT, _colors=[Colors.WHITE, Colors.BLUE, Colors.BLANK]),
            Piece(_pos=BACK+RIGHT, _colors=[Colors.WHITE, Colors.GREEN, Colors.BLANK]),
            Piece(_pos=BACK+UP, _colors=[Colors.WHITE, Colors.BLANK, Colors.ORANGE]),
            Piece(_pos=BACK+DOWN, _colors=[Colors.WHITE, Colors.BLANK, Colors.RED]),
            Piece(_pos=LEFT+UP, _colors=[Colors.BLANK, Colors.BLUE, Colors.ORANGE]),
            Piece(_pos=LEFT+DOWN, _colors=[Colors.BLANK, Colors.BLUE, Colors.RED]),
            Piece(_pos=RIGHT+UP, _colors=[Colors.BLANK, Colors.GREEN, Colors.ORANGE]),
            Piece(_pos=RIGHT+DOWN, _colors=[Colors.BLANK, Colors.GREEN, Colors.RED])
        )

        self.corners = (
            Piece(_pos=FRONT+LEFT+UP, _colors=[Colors.YELLOW, Colors.BLUE, Colors.ORANGE]),
            Piece(_pos=FRONT+LEFT+DOWN, _colors=[Colors.YELLOW, Colors.BLUE, Colors.RED]),
            Piece(_pos=FRONT+RIGHT+UP, _colors=[Colors.YELLOW, Colors.GREEN, Colors.ORANGE]),
            Piece(_pos=FRONT+RIGHT+DOWN, _colors=[Colors.YELLOW, Colors.GREEN, Colors.RED]),
            Piece(_pos=BACK+LEFT+UP, _colors=[Colors.WHITE, Colors.BLUE, Colors.ORANGE]),
            Piece(_pos=BACK+LEFT+DOWN, _colors=[Colors.WHITE, Colors.BLUE, Colors.RED]),
            Piece(_pos=BACK+RIGHT+UP, _colors=[Colors.WHITE, Colors.GREEN, Colors.ORANGE]),
            Piece(_pos=BACK+RIGHT+DOWN, _colors=[Colors.WHITE, Colors.GREEN, Colors.RED])
        )

        self.pieces = self.faces + self.edges + self.corners

    def _get_face(self, axis):
        """
        Find a face given a unit vector representing the axis

        :return: A list of the pieces on the face
        """

        assert type(axis) == Point3D
        assert len([elem for elem in axis if elem == 0]) == 2

        return [p for p in self.pieces if p.pos.dot(axis) > 0]

    def _rotate_face(self, axis, matrix):
        """
        Rotate a given face by the given matrix

        :param axis: The axis to rotate about
        :param matrix: The matrix to rotate by
        :return: None
        """

        assert type(matrix) is Matrix3D

        self._rotate_pieces(self._get_face(axis), matrix)

    def _rotate_pieces(self, face, matrix):
        """
        Rotate all the pieces in a face

        :param face: The face to rotate
        :param matrix: The rotation matrix
        :return: None
        """

        for p in face:
            p.rotate(matrix)

    def is_solved(self):
        """
        Check if the cube is solved

        :return: Bool indicating if cube is solved
        """

        def check(colors):
            """
            Internal helper function to check each face

            :param colors: Colors to check (list)
            :return: Bool if all the colors match
            """
            assert len(colors) == 9
            return all(c == colors[0] for c in colors)

        return (check(p.colors[0] for p in self._get_face(FRONT)) and
                check(p.colors[0] for p in self._get_face(BACK)) and
                check(p.colors[1] for p in self._get_face(LEFT)) and
                check(p.colors[1] for p in self._get_face(RIGHT)) and
                check(p.colors[2] for p in self._get_face(UP)) and
                check(p.colors[2] for p in self._get_face(DOWN)))

    def find_piece(self, colors):
        """
        Find a piece given a color list

        :param colors: The list of colors to search for
        :return: Piece that matches color list
        """

        assert isinstance(colors, (tuple, list)) and len(colors) == 3

        for p in self.pieces:
            if all(c in p.colors for c in colors):
                return p

    def sequence(self, move_str):
        """
        Sequence through a list of rotations given in Rubik's notation

        :param move_str: The sequence to move by
        :return: None
        """

        assert type(move_str) == str
        assert all(s in VALID_NOTATION.split() for s in move_str.split())

        # Find all the functions in this class that match the symbols in the move string
        moves = [getattr(self, sym) for sym in move_str.split()]

        # Sequence the given moves
        for move in moves:
            move()

    def face_colors(self, axis):
        """
        Find all the colors on a face relating to the given axis

        :param axis: The axis of the face
        :return: A list of all the colors
        """

        face = self._get_face(axis)
        i = [j for j, x in enumerate(axis) if x == 1 or x == -1][0]

        return [p.colors[i] for p in face]

    def F(self): self._rotate_face(FRONT, ROT_X_CW)
    def Fi(self): self._rotate_face(FRONT, ROT_X_CC)
    def B(self): self._rotate_face(BACK, ROT_X_CC)
    def Bi(self): self._rotate_face(BACK, ROT_X_CW)
    def L(self): self._rotate_face(LEFT, ROT_Y_CW)
    def Li(self): self._rotate_face(LEFT, ROT_Y_CC)
    def R(self): self._rotate_face(RIGHT, ROT_Y_CC)
    def Ri(self): self._rotate_face(RIGHT, ROT_Y_CW)
    def U(self): self._rotate_face(UP, ROT_Z_CW)
    def Ui(self): self._rotate_face(UP, ROT_Z_CC)
    def D(self): self._rotate_face(DOWN, ROT_Z_CC)
    def Di(self): self._rotate_face(DOWN, ROT_Z_CW)

    def __eq__(self, other):
        """
        Equal to operator

        :param other: Compare object
        :return: Bool for if the objects are equal
        """

        assert type(other) == Cube

        return Cube.pieces == other.pieces

    def __ne__(self, other):
        return not self == other

    def __str__(self):

        template = ("         {} {} {}\n"
                    "         {} {} {}\n"
                    "         {} {} {}\n"
                    "{} {} {} {} {} {} {} {} {} {} {} {}\n"
                    "{} {} {} {} {} {} {} {} {} {} {} {}\n"
                    "{} {} {} {} {} {} {} {} {} {} {} {}\n"
                    "         {} {} {}\n"
                    "         {} {} {}\n"
                    "         {} {} {}\n")


        full_str = template.format(*(self.face_colors(UP) + self.face_colors(LEFT) + self.face_colors(FRONT) +
                                     self.face_colors(RIGHT) + self.face_colors(BACK) + self.face_colors(DOWN)))

        return full_str

