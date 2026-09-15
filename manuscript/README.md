# Manuscript package

## Compile

```bash
xelatex -interaction=nonstopmode main.tex
biber main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

The manuscript uses `biblatex` with APA style and Biber. It was compile-tested with XeLaTeX and Biber before packaging.

## Contents

- `main.tex` — complete manuscript source
- `references.bib` — 80-reference bibliography database
- `compile.sh` — deterministic compile script

## Reproducibility

Code and executable validation artifact:
https://github.com/Arithmetic-Power-Geometry/Underdetermination-Lab
