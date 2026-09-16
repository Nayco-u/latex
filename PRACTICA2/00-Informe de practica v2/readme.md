# Informe de Práctica II — BIFROST / DTS SpA

Plantilla UC (Práctica II) con el informe modularizado: una sección por archivo,
bibliografía en BibTeX con estilo APA 7, y anexos generados desde el Excel.
Compilar con **XeLaTeX**.

## Estado

| Sección | Estado |
|---|---|
| Resumen ejecutivo (inglés) | por escribir |
| 1. Identificación y Contextualización | **redactada** |
| 2. Generación y Justificación | esqueleto con guía |
| 3. Evaluación y Conclusiones | esqueleto con guía |
| 4. Referencias bibliográficas | automática desde `referencias.bib` |
| 5. Anexos — reflexión personal | por escribir |
| 5. Anexos A–D — tablas | generadas desde el Excel |

## Cómo trabajar

Escribe solo en los lugares marcados `% ESCRIBIR AQUÍ`. Cada subsección trae
arriba un bloque de comentarios con:

- `[CONTENIDO]` — los puntos que el párrafo debe cubrir, mapeados al criterio
  exacto de la rúbrica que los evalúa.
- `[ESTRUCTURA]` — cómo encadenar los párrafos.
- `[EXTENSIÓN]` — presupuesto de palabras.
- `[EJEMPLO DE ARRANQUE]` — una o dos oraciones modelo para entrar al párrafo.

Borra el bloque de comentarios a medida que cierras cada subsección.

## Estructura de archivos

```text
├── main.tex                          // documento principal, ordena los \input
├── style.cls                         // estilos
├── readme.md                         // este documento
├── content/
│   ├── 00-abstract.tex               // resumen ejecutivo en inglés
│   ├── 01-identificacion.tex         // sección 1  (REDACTADA)
│   ├── 02-generacion.tex             // sección 2
│   ├── 03-evaluacion.tex             // sección 3
│   ├── 04-referencias.tex            // imprime la bibliografía
│   ├── 05-anexos.tex                 // reflexión personal + \input de tablas
│   ├── 05-anexos-tablas.tex          // GENERADO — no editar a mano
│   ├── referencias.bib               // base bibliográfica
│   ├── gen_tablas.py                 // genera 05-anexos-tablas.tex
│   └── portada.pdf
└── img/
    ├── gantt.py                      // genera gantt.png
    ├── gantt.png                     // Figura 1-1
    ├── oeb_entidades_operacionales.jpg   // Figura 2-1
    ├── sab_sistema_bifrost.jpg           // Figura 2-2
    ├── lcbd_arquitectura_logica.jpg      // Figura 2-3
    ├── pab_arquitectura_fisica.jpg       // Figura 2-4
    ├── crop_uplink.png                   // Figura 2-5
    ├── crop_downlink.png                 // Figura 3-1
    ├── crop_zoom_uplink.png              // Figura 3-2
    └── [ ... ] *.jpg                 // diagramas Capella originales, sin usar
```

Los nombres de archivo de las figuras se simplificaron porque `\includegraphics`
no acepta corchetes. Las tres figuras de simulación son recortes de las capturas
originales (`uplink.png`, `downlink.png`, `zoom_uplink.png`), que también siguen
en `img/`: se dejó solo el gráfico y la barra de estado, lo que ahorra cerca de
una plana y media y las hace legibles.

## Citar

La bibliografía usa **biblatex + biber** con estilo APA 7. Para citar:

```latex
\parencite{roques}             % (Roques, 2018)
\textcite{roques}              % Roques (2018)
\parencite[p.~45]{roques}      % (Roques, 2018, p. 45)
\parencites{alenspace}{roques} % (Alén Space, s.f.; Roques, 2018)
```

Solo aparecen en la bibliografía las entradas efectivamente citadas; la rúbrica
exige un mínimo de 5. Para agregar una fuente, añade la entrada en
`content/referencias.bib` y cítala en el texto.

## Regenerar tablas y figuras

Desde la raíz del proyecto, si cambias el Excel de requerimientos o la Gantt:

```shell
python3 content/gen_tablas.py   # Anexos A, B, C y D
python3 img/gantt.py            # Figura 1-1
```

Ambos scripts buscan los Excel en la carpeta padre (`PRACTICA2/`).

## Build

```shell
latexmk -xelatex -outdir=build main.tex
```

`latexmk` corre biber automáticamente entre pasadas. En Overleaf basta
seleccionar XeLaTeX en las opciones del proyecto.

## Límites de la rúbrica

| Sección | Límite | Dónde se controla |
|---|---|---|
| Resumen ejecutivo (inglés) | 1 plana / 200–400 palabras | `00-abstract.tex` |
| Contextualización de la empresa | 1 plana | `01-identificacion.tex` §1.1 |
| Informe técnico (secciones 1 a 3) | 20 planas | secciones 01 a 03 |
| Reflexión personal | 2 planas, primera persona | `05-anexos.tex` §5.1 |
| Referencias | mínimo 5, todas citadas en el texto | `referencias.bib` |

Formato exigido y ya configurado en `style.cls`: papel carta, Times New Roman
12 pt, márgenes de 2,5 cm, sangría de 1,27 cm, párrafos justificados,
numeración en la esquina superior derecha desde la portada, interlineado 1,5.

**Control de extensión.** Con la sección 1 escrita y las secciones 2 y 3 aún
vacías, el cuerpo ocupa 13 planas. Quedan unas 7 planas (≈2.500 palabras) para
el texto de las secciones 2 y 3. Compila cada cierto tiempo y revisa dónde cae
el título "4. Referencias bibliográficas": debe quedar en la plana 25 del PDF o
antes, porque la portada, el abstract y los tres índices ocupan 5 planas previas
al cuerpo.

> **Nota sobre el interlineado.** El manual ING2001 (sección 8) pide interlineado
> doble, pero la rúbrica de corrección exige 1,5. La plantilla usa 1,5 porque es
> lo que marca el corrector. Si prefieres seguir el manual, cambia
> `\setstretch{1.5}` por `\setstretch{2}` en `style.cls` — ten en cuenta que eso
> aumenta el cuerpo en cerca de un tercio y te dejaría muy por sobre las 20 planas.

## Cambios hechos a la plantilla original

Todos en `style.cls`:

1. `babel` se carga con `[british, spanish, es-noshorthands]` en vez de solo
   `[spanish]`. Sin `british`, el `\selectlanguage{British}` del abstract falla
   al compilar en instalaciones que no cargan el idioma automáticamente.
2. `apacite` (que sigue APA 6) se reemplazó por `biblatex` con estilo `apa` y
   backend `biber`, más `\DeclareLanguageMapping{spanish}{spanish-apa}` para que
   las referencias salgan en español. Se agregó `csquotes`, que biblatex exige
   cuando hay babel.
3. `ulem` se carga con la opción `[normalem]`. Sin ella, `ulem` redefine `\emph`
   como subrayado y los títulos de la bibliografía salían subrayados en vez de
   en cursiva.
4. `hyperref` recibió `citecolor=black`, para que las citas no salgan en verde.
