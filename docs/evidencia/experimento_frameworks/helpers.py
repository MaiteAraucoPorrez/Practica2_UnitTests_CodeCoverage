import os, sys

_aqui = os.path.abspath(os.path.dirname(__file__))
while not os.path.isdir(os.path.join(_aqui, "pieces")):
    _padre = os.path.dirname(_aqui)
    if _padre == _aqui:
        raise RuntimeError("No se encontró la carpeta pieces/")
    _aqui = _padre
sys.path.insert(0, _aqui)

from pieces.pawn import Pawn


def empty():
    return {f"{f}{r}": None for f in "abcdefgh" for r in "12345678"}
