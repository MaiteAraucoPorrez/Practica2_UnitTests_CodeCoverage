"""Reproduce en la terminal los 3 defectos encontrados (BUG-01, BUG-02 y BUG-03).

Ejecutar desde la raíz del repositorio (con el entorno virtual activado):

    python docs/evidencia/reproducir_defectos.py

No modifica nada: solo llama al código del juego y muestra "esperado" vs "obtenido".
"""
import contextlib
import io
import os
import sys

# Sube carpetas hasta encontrar la raíz del proyecto (donde está la carpeta pieces/)
_aqui = os.path.abspath(os.path.dirname(__file__))
while not os.path.isdir(os.path.join(_aqui, "pieces")):
    _padre = os.path.dirname(_aqui)
    if _padre == _aqui:
        raise RuntimeError("No se encontró la carpeta pieces/")
    _aqui = _padre
sys.path.insert(0, _aqui)

from board import Board
from pieces.bishop import Bishop
from pieces.king import King
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.space import Space


def tablero_vacio():
    return {f"{f}{r}": None for f in "abcdefgh" for r in "12345678"}


def llamar(funcion, *args):
    """Devuelve (resultado, lo que la función imprimió)."""
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        resultado = funcion(*args)
    return resultado, salida.getvalue().strip()


print("=" * 72)
print("BUG-01 · el rey, la reina, la torre y el alfil no pueden capturar")
print("=" * 72)
casos = [("King", King(True), "e4", "e5"), ("Queen", Queen(True), "d4", "d7"),
         ("Rook", Rook(True), "a1", "a4"), ("Bishop", Bishop(True), "c1", "f4")]
for nombre, pieza, inicio, fin in casos:
    tablero = tablero_vacio()
    tablero[fin] = Pawn(False)                      # peón enemigo en el destino
    resultado, mensaje = llamar(pieza.validate_move, inicio, fin, tablero)
    print(f"{nombre}: {inicio}->{fin} con un peón enemigo en {fin}")
    print(f"   esperado (reglas del ajedrez): True  (capturar es legal)")
    print(f"   obtenido: {resultado}   mensaje: {mensaje}")

print()
print("=" * 72)
print("BUG-02 · el peón queda marcado is_en_passentable aunque su avance fue rechazado")
print("=" * 72)
tablero = tablero_vacio()
tablero["e3"] = Rook(False)                         # e3 ocupada: el avance de 2 casillas está bloqueado
peon = Pawn(True)
resultado, mensaje = llamar(peon.validate_move, "e2", "e4", tablero)
print("Peón blanco e2->e4 con una torre en e3")
print(f"   validate_move: {resultado}   mensaje: {mensaje}   (correcto: el avance está bloqueado)")
print("   esperado: is_en_passentable = False  (el peón no se movió)")
print(f"   obtenido: is_en_passentable = {peon.is_en_passentable}")

print()
print("=" * 72)
print("BUG-03 · el mensaje al elegir una casilla vacía depende del color de la casilla")
print("=" * 72)
for color, nombre in ((True, "blanca"), (False, "negra")):
    tablero_juego = Board()
    tablero_juego.board["e4"] = Space(color)
    resultado, mensaje = llamar(tablero_juego.validate_piece, True, "e4")
    print(f"Turno de blanco; e4 es una casilla vacía {nombre}")
    print("   esperado: No piece selected. Please select a piece to move")
    print(f"   obtenido: {mensaje}")
