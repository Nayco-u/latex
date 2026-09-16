# Informe de Práctica II — BIFROST / DTS SpA — versión 3

Nicolás Esteban Seguel Ardiles · Ingeniería Civil Eléctrica · neseguel@uc.cl

Esta carpeta es la **v3**. Sale de la v2 y recoge la revisión final del
23 de agosto de 2026. La v2 queda intacta en `../00-Informe de practica v2/`
por si hay que volver a algo.

---

## Cómo compilar

```
latexmk -pdf -outdir=build main.tex
```

Requiere **biber** (biblatex, estilo APA 7). En Overleaf basta con seleccionar
XeLaTeX o pdfLaTeX; biber corre solo. El PDF queda en `build/main.pdf`.

Si cambia el Excel de trazabilidad:

```
python3 content/gen_tablas.py
```

Regenera `content/05-anexos-tablas.tex` (Anexos A a D). **No editar ese archivo
a mano**, se sobrescribe.

---

## Estructura

| Archivo | Contenido |
|---|---|
| `main.tex` | Ordena los `\input` y arma el documento |
| `style.cls` | Formato: márgenes, fuente, interlineado, numeración |
| `content/00-abstract.tex` | Resumen ejecutivo en inglés (354 palabras, 1 plana) |
| `content/01-identificacion.tex` | 1. Identificación y Contextualización |
| `content/02-generacion.tex` | 2. Generación y Justificación |
| `content/03-evaluacion.tex` | 3. Evaluación y Conclusiones |
| `content/04-referencias.tex` | 4. Referencias (biblatex) |
| `content/05-anexos.tex` | 5. Anexos: reflexión personal |
| `content/05-anexos-tablas.tex` | Anexos A a D (**generado**, no editar) |
| `content/gen_tablas.py` | Generador de los anexos desde el Excel |
| `content/referencias.bib` | 8 fuentes, todas citadas |

---

## Extensión, medida sobre el PDF de esta versión

| Sección | Planas del PDF | Límite | Estado |
|---|---|---|---|
| Resumen ejecutivo | 2 | 1 plana | cumple |
| Cuerpo (secciones 1 a 3) | 6 a 23 (**18 planas**) | 20 planas | cumple, con 2 de holgura |
| Contextualización de la empresa (1.1) | solo plana 6 | 1 plana | cumple |
| Reflexión personal | 25 y 26 | 2 planas | cumple |

**Chequeo rápido después de editar:** el título "4. Referencias bibliográficas"
tiene que caer en la plana 24 del PDF o antes. Si se pasa, el cuerpo superó las
20 planas.

---

## Formato exigido por el manual ING2001, punto 8

- Hoja carta, márgenes de 2,5 cm por los cuatro lados.
- Times New Roman 12 (`mathptmx`); tamaño reducido en anexos, tablas y figuras.
- Interlineado 1,5. **El manual pide doble, pero la rúbrica de corrección
  exige 1,5. Manda la rúbrica.**
- Sangría de 1,27 cm en la primera línea de cada párrafo, párrafos justificados.
- Numeración arábiga en la esquina superior derecha, desde la portada.
- Títulos numerados; tablas y figuras numeradas por capítulo con separador
  punto (`Tabla 2.1`, `Figura 3.2`), según el punto 9.2 del manual.
- Cursiva reservada a palabras de otro idioma.

---

## Pendientes que quedan fuera de LaTeX

1. **Arreglar el Excel.** `07-TraceabilityRequirimentsMatrix.xlsx`, hoja `RISK`,
   columna "Mitigación Propuesta" del bloque de SR: está corrida desde SR-08
   hacia abajo. `gen_tablas.py` la corrige con el diccionario `MIT_OVERRIDE`,
   pero es un parche. Arreglado el Excel, ese diccionario se puede borrar.
   Lo mismo con la lista `ERRATAS`, que corrige faltas de ortografía del Excel.
2. **SR-07 sigue diciendo "Transponder Banda S"**, cuando el diseño migró a UHF
   propio. El Anexo B lleva una nota que lo explica, pero el requerimiento
   debería actualizarse formalmente en la CDR.
3. **SR-02 aparece como riesgo Alto en la hoja `SR` y Medio en la hoja `RISK`.**
   El informe usa la hoja `SR` y por eso el conteo de doce requerimientos de
   riesgo alto es consistente. Conviene alinear ambas hojas.
4. **Los tres diagramas de Capella (Figuras 2.1, 2.2 y 2.3) son poco legibles
   al tamaño impreso.** Se dejaron así por decisión propia. Si el corrector lo
   objeta, la salida es ponerlos en plana apaisada con `\begin{landscape}`.
5. **El título dentro de los gráficos del simulador dice "24 HORAS" y el eje
   llega a 42 horas.** Está adentro de la imagen y solo se arregla
   regenerándola desde el simulador.
