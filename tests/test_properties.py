"""Pruebas basadas en propiedades (Hypothesis).

Complementan a las pruebas por caminos: en vez de elegir a mano las casillas,
Hypothesis genera cientos de combinaciones y comprueba una regla que debe cumplirse siempre.
"""
from hypothesis import given, strategies as st
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn

FILES = "abcdefgh"
RANKS = "12345678"
DIRECCIONES = [(df, dr) for df in (-1, 0, 1) for dr in (-1, 0, 1) if (df, dr) != (0, 0)]

square = st.builds(lambda f, r: f"{f}{r}", st.sampled_from(FILES), st.sampled_from(RANKS))


def empty_board():
    return {f"{f}{r}": None for f in FILES for r in RANKS}


def pasos_maximos(start, df, dr):
    """Cuántos pasos se puede avanzar desde start en la dirección (df, dr) sin salir del tablero."""
    f0, r0 = FILES.index(start[0]), int(start[1])
    n = 0
    while 0 <= f0 + df * (n + 1) <= 7 and 1 <= r0 + dr * (n + 1) <= 8:
        n += 1
    return n


@st.composite
def aligned_pair(draw):
    """Casilla de inicio, dirección y número de pasos (≥ 1) que no se salen del tablero."""
    start = draw(square)
    posibles = [d for d in DIRECCIONES if pasos_maximos(start, *d) >= 1]
    df, dr = draw(st.sampled_from(posibles))
    steps = draw(st.integers(min_value=1, max_value=pasos_maximos(start, df, dr)))
    f0, r0 = FILES.index(start[0]), int(start[1])
    end = f"{FILES[f0 + df * steps]}{r0 + dr * steps}"
    return start, end, (df, dr), steps


@given(aligned_pair())
def test_get_path_propiedades(par):
    start, end, (df, dr), steps = par
    path = Pawn(True).get_path(start, end)
    assert len(path) == steps
    assert path[-1] == end
    assert path[0] == f"{FILES[FILES.index(start[0]) + df]}{int(start[1]) + dr}"


@given(square, square)
def test_caballo_en_tablero_vacio_solo_mueve_en_L(a, b):
    df = abs(FILES.index(a[0]) - FILES.index(b[0]))
    dr = abs(int(a[1]) - int(b[1]))
    esperado = (df, dr) in ((1, 2), (2, 1))
    assert Knight(True).validate_move(a, b, empty_board()) is esperado


@given(square, square)
def test_rey_en_tablero_vacio_solo_mueve_una_casilla(a, b):
    df = abs(FILES.index(a[0]) - FILES.index(b[0]))
    dr = abs(int(a[1]) - int(b[1]))
    esperado = max(df, dr) == 1
    assert King(True).validate_move(a, b, empty_board()) is esperado
