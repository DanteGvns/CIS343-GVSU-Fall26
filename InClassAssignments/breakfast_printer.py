"""Student exercise: printing a breakfast syntax tree.

Implement __str__ in Crispiness, Cooked, Bacon, Sausage, Eggs, Bread, and
Breakfast so that print(breakfast) produces the menu text described by the
grammar. Return strings from these methods; do not print inside them.
Leave Node.__str__ as the base-class placeholder.

Run your completed solution with: python3 breakfast_printer.py
The example should print:
really really crispy bacon with scrambled eggs with toast on the side on the side
"""

from typing import Literal


class Node:
    """A syntax-tree node whose string is the menu text it represents."""

    def __str__(self):
        raise NotImplementedError


class Crispiness(Node):
    def __init__(self, more = None):
        self.more = more

    def __str__(self):
        if self.more:
            return f"really {self.more}"
        else:
            return "really "


class Cooked(Node):
    def __init__(self, style: Literal["scrambled", "poached", "fried"]):
        self.style = style

    def __str__(self):
        # TODO: Implement this method using the breakfast grammar.
        return self.style


class Protein(Node):
    """Base class for the three protein productions."""


class Bacon(Protein):
    def __init__(self, crispiness):
        self.crispiness = crispiness

    def __str__(self):
        return self.crispiness.__str__() + "crispy bacon"


class Sausage(Protein):
    def __str__(self):
        # TODO: Implement this method using the breakfast grammar.
        return " sausage"


class Eggs(Protein):
    def __init__(self, cooked):
        self.cooked = cooked

    def __str__(self):
        # TODO: Implement this method using the breakfast grammar.
        return self.cooked.__str__() + " eggs"


class Bread(Node):
    def __init__(self, kind: Literal["toast", "biscuits", "English muffin"]):
        self.kind = kind

    def __str__(self):
        # TODO: Implement this method using the breakfast grammar.
        return self.kind.__str__()


class Breakfast(Node):
    def __init__(self, main, side = None):
        self.main = main
        self.side = side
        if self.side is not None and not isinstance(self.main, Protein):
            raise ValueError("Only a protein can have a breakfast on the side.")

    def __str__(self):
        # TODO: Implement this method using the breakfast grammar.
        if not self.side:
            return str(self.main)
        else:
            return f"{self.main} with {self.side} on the side" 

if __name__ == "__main__":
    breakfast = Breakfast(
        main=Bacon(Crispiness(Crispiness())),
        side=Breakfast(
            main=Eggs(Cooked("scrambled")),
            side=Breakfast(Bread("toast")),
        ),
    )
    print(breakfast)
