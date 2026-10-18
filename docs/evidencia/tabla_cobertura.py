"""Genera la tabla de cobertura "antes / después" por archivo y comprueba el objetivo del sprint.

Ejecutar desde la raíz del repositorio (con el entorno virtual activado):

    python docs/evidencia/tabla_cobertura.py

Hace tres cosas: ejecuta `coverage run -m pytest`, lee el resultado con `coverage json` y escribe
la tabla en la terminal y en `docs/evidencia/tabla_cobertura.md`. No modifica el código del juego.
"""
import json
import os
import subprocess
import sys

# Sube carpetas hasta encontrar la raíz del proyecto (donde está la carpeta pieces/)
_aqui = os.path.abspath(os.path.dirname(__file__))
while not os.path.isdir(os.path.join(_aqui, "pieces")):
    _padre = os.path.dirname(_aqui)
    if _padre == _aqui:
        raise RuntimeError("No se encontró la carpeta pieces/")
    _aqui = _padre
os.chdir(_aqui)

# Líneas del validate_move de cada pieza (según radon): el objetivo exige 100 % de ramas aquí
VALIDATE_MOVE = {
    "pieces/pawn.py": (10, 61), "pieces/king.py": (8, 25), "pieces/queen.py": (8, 28),
    "pieces/rook.py": (9, 26), "pieces/bishop.py": (8, 25), "pieces/knight.py": (8, 20),
}
OBJETIVO_RAMAS = 90.0

subprocess.run([sys.executable, "-m", "coverage", "run", "-m", "pytest", "-q"], check=False, stdout=subprocess.DEVNULL)
subprocess.run([sys.executable, "-m", "coverage", "json", "-o", "coverage.json", "-q"], check=True)
datos = json.load(open("coverage.json", encoding="utf-8"))
os.remove("coverage.json")


def pct(x):
    """100 % solo si es exactamente 100 (igual que coverage: 99.8 se muestra como 99.8 %, no como 100 %)."""
    return "100 %" if x >= 100 else f"{x:.1f} %"


def rangos(lineas):
    """[1,2,3,7,9,10] -> '1-3, 7, 9-10'"""
    if not lineas:
        return "—"
    lineas = sorted(lineas)
    salida, inicio, previo = [], lineas[0], lineas[0]
    for n in lineas[1:] + [None]:
        if n is not None and n == previo + 1:
            previo = n
            continue
        salida.append(str(inicio) if inicio == previo else f"{inicio}-{previo}")
        if n is not None:
            inicio = previo = n
    return ", ".join(salida)


filas = []
for ruta, d in sorted(datos["files"].items()):
    ruta = ruta.replace("\\", "/")
    if ruta.startswith("tests/") or ruta.endswith("__init__.py") and d["summary"]["num_statements"] == 0:
        continue
    s = d["summary"]
    ramas = s["num_branches"]
    cubiertas = s["covered_branches"]
    pct_ramas = (100.0 * cubiertas / ramas) if ramas else 100.0
    filas.append((ruta, s["num_statements"], s["num_branches"], s["percent_covered"], pct_ramas, rangos(d["missing_lines"]), d))

t = datos["totals"]
pct_ramas_total = 100.0 * t["covered_branches"] / t["num_branches"]

lineas = ["| Archivo | Sentencias | Ramas | % antes | % después | % ramas después | Líneas sin cubrir |", "|---|---|---|---|---|---|---|"]
for ruta, st, br, p, pr, falta, _ in filas:
    lineas.append(f"| {ruta} | {st} | {br} | 0 % | {pct(p)} | {pct(pr)} | {falta} |")
lineas.append(f"| **TOTAL** | **{t['num_statements']}** | **{t['num_branches']}** | **0 %** | **{pct(t['percent_covered'])}** | **{pct(pct_ramas_total)}** | |")
tabla = "\n".join(lineas)

# --- objetivo del sprint ---
res = [f"Objetivo 1: ≥ {OBJETIVO_RAMAS:.0f} % de ramas en total → {pct_ramas_total:.1f} % → {'CUMPLIDO' if pct_ramas_total >= OBJETIVO_RAMAS else 'NO CUMPLIDO'}"]
todo_ok = True
for ruta, (a, b) in VALIDATE_MOVE.items():
    d = datos["files"].get(ruta) or datos["files"].get(ruta.replace("/", "\\"))
    sin_lineas = [n for n in (d["missing_lines"] if d else range(a, b + 1)) if a <= n <= b]
    sin_ramas = [m for m in (d["missing_branches"] if d else [[a, 0]]) if a <= m[0] <= b]
    ok = not sin_lineas and not sin_ramas
    todo_ok &= ok
    res.append(f"Objetivo 2: {ruta} validate_move (L{a}–L{b}) al 100 % → {'CUMPLIDO' if ok else 'FALTA: líneas ' + rangos(sin_lineas) + (' y ramas ' + str(sin_ramas) if sin_ramas else '')}")
res.append(f"Objetivo 2 (los 6 validate_move): {'CUMPLIDO' if todo_ok else 'NO CUMPLIDO'}")

texto = tabla + "\n\n" + "\n".join(res)
print(texto)
with open("docs/evidencia/tabla_cobertura.md", "w", encoding="utf-8") as f:
    f.write("# Cobertura: antes y después por archivo\n\n" + texto + "\n")
print("\nTabla guardada en docs/evidencia/tabla_cobertura.md")
