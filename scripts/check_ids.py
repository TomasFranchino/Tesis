#!/usr/bin/env python3
"""Verificador determinista de identificadores de la tesis (sin LLM, costo cero).

Detecta:
  1. IDs usados que nunca se definen (referencias rotas).
  2. IDs definidos en más de un archivo (colisiones o duplicaciones).
  3. IDs definidos que nadie referencia fuera de su definición (posible huérfano).

Uso:  python scripts/check_ids.py [raiz] [--salida gestion/revisiones/ids.md]
Excluye archivo/, guias/, gestion/, bibliografia/, .git/ y .claude/ (solo audita insumos/ y tesis/).
"""
import re, sys, pathlib, collections, argparse

FAMILIAS = {
    "RF": r"RF-\d{2}", "RNF": r"RNF-\d{2}", "OE": r"OE\d", "SP": r"SP\d",
    "ADR": r"ADR-\d{2}", "Escenario": r"E\d{2}", "Validación": r"V\d",
    "Núcleo": r"N\d", "Aporte/Antecedente": r"A\d", "Detección(B)": r"B\d",
    "Criterio(K)": r"K\d", "Stack(S)": r"S\d", "Criterio(G/D/X)": r"[GDX]\d",
}
EXCLUIR = {"archivo", ".git", "node_modules", ".claude", "gestion", "bibliografia", "guias"}

RANGO = re.compile(r"\b(RNF-|RF-|ADR-|OE|SP|E|V|N|A|B|K|S)(\d{1,2})\s*(?:–|-|a)\s*(?:\1)?(\d{1,2})\b")

def expandir_rangos(linea):
    """RF-17–20 -> RF-17 RF-18 RF-19 RF-20 ; SP1–SP4 -> SP1 SP2 SP3 SP4 ; RF-03 a RF-07 -> ..."""
    def rep(m):
        pre, a, b = m.group(1), m.group(2), m.group(3)
        ini, fin = int(a), int(b)
        if not (0 < fin - ini < 30):
            return m.group(0)
        ancho = len(a)
        return " ".join(f"{pre}{str(k).zfill(ancho)}" for k in range(ini, fin + 1))
    return RANGO.sub(rep, linea)

def patrones_definicion(idre):
    # Definición = primera celda de una fila de tabla con >= 3 columnas (las tablas de
    # trazabilidad de 2 columnas no cuentan), un título, o un ítem en negrita al inicio.
    return [
        re.compile(rf"^\|\s*\**({idre})\**\s*\|(?:[^|]*\|){{2,}}"),
        re.compile(rf"^#+\s*({idre})\b"),
        re.compile(rf"^\s*(?:[-*]\s*)?\*\*({idre})[\.:\s\*]"),
    ]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raiz", nargs="?", default=".")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    raiz = pathlib.Path(a.raiz)
    archivos = [p for p in raiz.rglob("*.md") if not (set(p.relative_to(raiz).parts) & EXCLUIR)]

    defs = collections.defaultdict(list)
    usos = collections.defaultdict(list)
    for p in archivos:
        rel = str(p.relative_to(raiz))
        for n, linea in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for idre in FAMILIAS.values():
                pos_def = set()
                for pat in patrones_definicion(idre):
                    m = pat.match(linea)
                    if m:
                        defs[m.group(1)].append((rel, n, linea.strip()[:90]))
                        pos_def.add(m.start(1))
                for m in re.finditer(rf"(?<![\w-])({idre})(?![\w])", expandir_rangos(linea)):
                    if m.start(1) not in pos_def:
                        usos[m.group(1)].append((rel, n))

    out = ["# Verificación de identificadores", ""]
    rotas = sorted(set(usos) - set(defs))
    out += ["## 1. Usados pero nunca definidos", ""]
    out += [f"- `{i}` → " + ", ".join(sorted({f'{f}:{l}' for f, l in usos[i]})[:6]) for i in rotas] or ["- Ninguno."]
    out += ["", "## 2. Definidos en más de un archivo (revisar si significan lo mismo)", ""]
    col = {i: d for i, d in defs.items() if len({f for f, _, _ in d}) > 1}
    for i in sorted(col):
        out.append(f"- `{i}`:")
        out += [f"  - {f}:{l} — {t}" for f, l, t in col[i]]
    if not col:
        out.append("- Ninguno.")
    out += ["", "## 3. Definidos y nunca referenciados en otro lugar (informativo)", ""]
    huer = [i for i in sorted(defs) if not usos.get(i)]
    out += [f"- `{i}` ({defs[i][0][0]}:{defs[i][0][1]})" for i in huer] or ["- Ninguno."]
    texto = "\n".join(out) + "\n"
    if a.salida:
        pathlib.Path(a.salida).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.salida).write_text(texto, encoding="utf-8")
    print(texto)
    sys.exit(1 if rotas else 0)

if __name__ == "__main__":
    main()
