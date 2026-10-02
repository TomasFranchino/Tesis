#!/usr/bin/env bash
# Compila la memoria (tesis/*.md en orden) a Word y, si hay motor LaTeX, a PDF.
# Requiere pandoc. Opcionales: bibliografia/apa.csl y plantilla/referencia.docx (estilos de la facultad).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p salida
ARCHIVOS=$(ls tesis/*.md | sort)
OPC=(--citeproc --bibliography=bibliografia/referencias.bib --toc --number-sections -M lang=es-AR)
[ -f bibliografia/apa.csl ] && OPC+=(--csl=bibliografia/apa.csl)
REF=(); [ -f plantilla/referencia.docx ] && REF=(--reference-doc=plantilla/referencia.docx)
pendientes=$(cat $ARCHIVOS | grep -o '\[\[' | wc -l | tr -d ' ')
echo "Marcadores [[...]] sin resolver: $pendientes"
pandoc "${OPC[@]}" "${REF[@]}" $ARCHIVOS -o salida/tesis.docx && echo "OK salida/tesis.docx"
if command -v xelatex >/dev/null; then
  pandoc "${OPC[@]}" --pdf-engine=xelatex $ARCHIVOS -o salida/tesis.pdf && echo "OK salida/tesis.pdf" \
    || echo "PDF no generado (revisar la instalación de LaTeX); el .docx sí se generó"
fi
