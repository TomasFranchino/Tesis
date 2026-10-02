#!/usr/bin/env python3
"""Reorganiza el repositorio de la tesis en carpetas con roles claros (tarea T-001).

Por defecto solo MUESTRA lo que haría. Con --aplicar ejecuta `git mv` (el historial se conserva).
Tolera nombres con espacios, guiones bajos o puntos ("Plan de validacion.md" = "Plan_de_validacion.md").
Uso:  python scripts/reorganizar_repo.py            (simulación)
      python scripts/reorganizar_repo.py --aplicar
"""
import pathlib, re, subprocess, sys, unicodedata

DESTINOS = {
    "insumos": ["Contribucion y alcance", "Objetivos", "Requisitos", "Arquitectura", "Plan de validacion",
                "Estado del arte comparativo", "1.1 Antecedentes de investigacion", "Definicion de problema",
                "Justificacion de tesis"],
    "guias":   ["Estructura del trabajo final", "Estrategia", "Errores comunes", "Preguntas"],
    "archivo": ["Ideas", "Idea seleccionada", "Entregable quincenal de avances profesor", "Entrega 1 Tesis"],
}
CARPETAS_NUEVAS = ["tesis", "insumos", "guias", "archivo", "bibliografia/fichas", "evidencia/datos",
                   "evidencia/resultados", "gestion/revisiones", "scripts/analisis", "salida"]

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[\s_.\-]+", "", s)

def main():
    aplicar = "--aplicar" in sys.argv
    raiz = pathlib.Path(".")
    presentes = {norm(p.stem): p for p in raiz.iterdir() if p.is_file() and p.suffix in (".md", ".docx")}
    movs, faltan = [], []
    for carpeta, nombres in DESTINOS.items():
        for n in nombres:
            p = presentes.pop(norm(n), None)
            (movs.append((p, pathlib.Path(carpeta) / p.name)) if p else faltan.append(f"{carpeta}/{n}"))
    for p, d in movs:
        print(f"git mv '{p}' '{d}'")
    for c in CARPETAS_NUEVAS:
        print(f"mkdir -p {c}")
    if faltan:
        print("\nNo encontrados (revisar nombre):", *faltan, sep="\n  - ")
    sobran = [str(p) for k, p in presentes.items() if p.name not in ("CLAUDE.md", "README.md")]
    if sobran:
        print("\nSin destino asignado (quedan en la raíz):", *sobran, sep="\n  - ")
    if not aplicar:
        print("\nSimulación. Para ejecutar: python scripts/reorganizar_repo.py --aplicar")
        return
    for c in CARPETAS_NUEVAS:
        (raiz / c).mkdir(parents=True, exist_ok=True)
        (raiz / c / ".gitkeep").touch()
    for p, d in movs:
        subprocess.run(["git", "mv", str(p), str(d)], check=True)
    print("\nListo. Revisá con `git status` y commiteá: [T-001][orquestador] reorganización del repositorio")

if __name__ == "__main__":
    main()
