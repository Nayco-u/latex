# Informe de Práctica II — BIFROST / DTS SpA

Plantilla UC (Práctica II) con el esqueleto del informe ya armado: secciones,
figuras, tablas, bibliografía en APA 7 y anexos generados desde el Excel.
Compilar con **XeLaTeX**.

## Cómo trabajar

Escribe solo en los lugares marcados `% ESCRIBIR AQUÍ`. Cada subsección trae
arriba un bloque de comentarios con:

- `[CONTENIDO]` — los puntos que el párrafo debe cubrir, mapeados al criterio
  exacto de la rúbrica que los evalúa.
- `[ESTRUCTURA]` — cómo encadenar los párrafos.
- `[EXTENSIÓN]` — presupuesto de palabras.
- `[EJEMPLO DE ARRANQUE]` — una o dos oraciones modelo para entrar al párrafo.

Borra el bloque de comentarios a medida que escribes cada subsección.

## Estructura de archivos

```text
├── main.tex                     // documento principal (no requiere cambios)
├── style.cls                    // estilos
├── readme.md                    // este documento
├── img/
│   ├── gantt.py                 // genera gantt.png desde 13-Carta Gantt.xlsx
│   ├── gantt.png                // Figura 1-1
│   ├── oeb_entidades_operacionales.jpg   // Figura 2-1
│   ├── sab_sistema_bifrost.jpg           // Figura 2-2
│   ├── lcbd_arquitectura_logica.jpg      // Figura 2-3
│   ├── pab_arquitectura_fisica.jpg       // Figura 2-4
│   ├── uplink.png                        // Figura 2-5
│   ├── downlink.png                      // Figura 3-1
│   ├── zoom_uplink.png                   // Figura 3-2
│   └── [ ... ] *.jpg            // diagramas Capella originales, sin usar
└── content/
    ├── abstract.tex             // ESCRIBIR (200-400 palabras, en inglés)
    ├── contenido.tex            // ESCRIBIR (cuerpo, máx. 20 planas)
    ├── bibliografia.tex         // 8 referencias APA 7 ya redactadas
    ├── anexos.tex               // ESCRIBIR (reflexión personal, 1ª persona)
    ├── tablas_anexos.tex        // GENERADO — no editar a mano
    ├── gen_tablas.py            // genera tablas_anexos.tex desde el Excel
    └── portada.pdf
```

Los nombres de archivo de las figuras se simplificaron porque `\includegraphics`
no acepta corchetes. Los diagramas originales de Capella siguen en `img/`.

## Regenerar tablas y figuras

Si cambias el Excel de requerimientos o la carta Gantt:

```shell
python3 content/gen_tablas.py   # Anexos A, B, C y D
python3 img/gantt.py            # Figura 1-1
```

Ambos scripts leen los archivos de la carpeta padre `PRACTICA2/`. Si mueves el
proyecto, ajusta la constante `XLSX` al inicio de cada script.

## Build

```shell
latexmk -xelatex -outdir=build main.tex
```

En Overleaf basta seleccionar XeLaTeX en las opciones del proyecto.

## Límites de la rúbrica

| Sección | Límite | Dónde se controla |
|---|---|---|
| Resumen ejecutivo (inglés) | 1 plana / 200–400 palabras | `abstract.tex` |
| Contextualización de la empresa | 1 plana | `contenido.tex` §1.1 |
| Informe técnico (secciones 1 a 3) | 20 planas | `contenido.tex` |
| Reflexión personal | 2 planas, primera persona | `anexos.tex` §5.1 |
| Referencias | mínimo 5, todas citadas en el texto | `bibliografia.tex` |

Formato exigido y ya configurado en `style.cls`: papel carta, Times New Roman
12 pt, márgenes de 2,5 cm, sangría de 1,27 cm, párrafos justificados,
numeración en la esquina superior derecha desde la portada, interlineado 1,5.

> **Nota sobre el interlineado.** El manual ING2001 (sección 8) pide interlineado
> doble, pero la rúbrica de corrección exige 1,5. La plantilla usa 1,5 porque es
> lo que marca el corrector. Si prefieres seguir el manual, cambia
> `\setstretch{1.5}` por `\setstretch{2}` en `style.cls` — ten en cuenta que eso
> aumenta el cuerpo en cerca de un tercio y te dejaría sobre las 20 planas.

## Cambio hecho a la plantilla original

`style.cls` ahora carga babel con `[british, spanish, es-noshorthands]` en vez de
solo `[spanish]`. Sin `british`, el `\selectlanguage{British}` del abstract falla
al compilar en instalaciones de LaTeX que no cargan el idioma automáticamente.
