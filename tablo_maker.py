from config import *


class Engine:
    _template = '\\begin{{mpost}}\n\npicture l;\n{}\n\\end{{mpost}}\n'
    _response = ''
    _dot = 'dotlabel.top(btex $$ etex, ({}, {}));\n'
    _line = 'draw ({}, {}) -- ({}, {});\n'
    _label = 'l := thelabel(btex ${}$ etex, ({}, {}));\ndraw l withcolor {};\n'
    _square = 'draw ({}, {})--({}, {})--({}, {})--({}, {})--cycle withcolor {};\n'

    @classmethod
    def draw(cls, file):
        s = cls._template.format(cls._response)
        with open(file, 'w') as f:
            f.write(s)

    @classmethod
    def line(cls, x_from, y_from, x_to, y_to):
        cls._response += cls._dot.format(x_from, y_from)
        cls._response += cls._line.format(x_from, y_from, x_to, y_to)
        cls._response += cls._dot.format(x_to, y_to)

    @classmethod
    def label(cls, x, y, text, color):
        if text != '':
            cls._response += cls._label.format(text, x, y, color)
        else:
            cls._response += cls._square.format(
                x - SQUARE_SIZE / 2, y - SQUARE_SIZE / 2,
                x + SQUARE_SIZE / 2, y - SQUARE_SIZE / 2,
                x + SQUARE_SIZE / 2, y + SQUARE_SIZE / 2,
                x - SQUARE_SIZE / 2, y + SQUARE_SIZE / 2,
                color
            )


class Vertex:

    def __init__(self, parent, x, y, text, spacing, color):
        self._parent = parent
        self._x = x
        self._y = y
        self._text = text
        self._color = color
        self._spacing = spacing
        self._successor = {}

    def __str__(self):
        if self._parent is not None:
            Engine.line(
                self._parent._x,
                self._parent._y - TEXT_HEIGHT / 2,
                self._x,
                self._y + TEXT_HEIGHT / 2
            )
        Engine.label(
            self._x,
            self._y,
            self._text,
            self._color
        )
        return self._text

    def get(self, *args):
        if len(args) > 0:
            if args[0] in self._successor.keys():
                return self._successor[args[0]].get(*args[1:])
            else:
                raise Exception(f'Wrong sequence in get, vertex does not have {args[0]} successor')
        else:
            return self
    
    def draw(self):
        _ = str(self)
        for succ in self._successor.values():
            succ.draw()
    
    def reproduce(self, left = None, under = None, right = None, decrement_spacing = True, color_left = 'black', color_under = 'black', color_right = 'black'):
        if decrement_spacing:
            new_spacing = self._spacing / 2
        else:
            new_spacing = self._spacing

        if left is not None:
            self._successor['<'] = Vertex(
                self,
                self._x - self._spacing * LINE_WIDTH,
                self._y - LINE_HEIGHT - TEXT_HEIGHT,
                left,
                new_spacing,
                color_left
            )
        if under is not None:
            self._successor['v'] = Vertex(
                self,
                self._x,
                self._y - LINE_HEIGHT - TEXT_HEIGHT,
                under,
                self._spacing,
                color_under
            )
        if right is not None:
            self._successor['>'] = Vertex(
                self,
                self._x + self._spacing * LINE_WIDTH,
                self._y - LINE_HEIGHT - TEXT_HEIGHT,
                right,
                new_spacing,
                color_right
            )


class Tree:
    
    def __init__(self, text, max_spacing = MAX_SPACING):
        self.root = Vertex(None, 0, 0, text, max_spacing, 'black')
    
    def get(self, *args):
        if len(args) > 0:
            return self.root.get(*(args[0].split(DELIMETER)))
        else:
            return self.root.get()
    
    def draw(self, file):
        self.root.draw()
        Engine.draw(file)
