# Protocolo de Laboratorio — Caracterización del Galileoscope
### IEE 3873 — Astronomical Instrumentation Lab

**Objetivo:** medir magnificación (M) y campo de visión (FOV) en dos configuraciones ópticas del Galileoscope, y la resolución angular en una configuración, con estimación de error aleatorio y sistemático.

---

## 0. Elección de configuraciones y justificación

El Galileoscope permite tres configuraciones ópticas distintas. Para las dos mediciones de M y FOV se eligen las **dos configuraciones fundamentalmente diferentes**, porque conectan directamente con el objetivo del curso de entender "el significado práctico de la pupila":

| Config. | Óptica | M nominal | Imagen | Pupila de salida |
|---|---|---|---|---|
| **1. Ocular principal** | Kepleriano (ocular positivo) | 25x | Invertida | **Real** — proyectable |
| **2. Ocular Galileo** | Galileo verdadero (ocular negativo) | 17x | Derecha | **Virtual** — no proyectable |

Para la **resolución angular**, se usa la configuración de mayor magnificación disponible — **ocular principal + Barlow (50x)**. Esto es importante: a mayor M, la separación angular entre dos puntos se magnifica más antes de llegar al ojo/cámara, reduciendo la probabilidad de que la resolución medida esté limitada por el observador/detector en vez de por el instrumento (objetivo de 50 mm).

---

## 1. Materiales

- Galileoscope ensamblado (ver manual de armado)
- Trípode fotográfico (obligatorio — el manual advierte que a 25x-50x cualquier vibración arruina la observación)
- Cámara (smartphone o DSLR) con **enfoque y zoom manual bloqueables** durante cada serie de fotos
- Soporte/clamp para alinear el lente de la cámara con el ocular (acople afocal)
- Cinta métrica (para medir la distancia $L$ al blanco)
- Regla de 30 cm (como referencia de escala en las fotos, no para lectura directa)
- Blanco de prueba impreso (ver diseño abajo)
- Software para medir en píxeles: ImageJ, GIMP, o Python (`PIL`/`numpy`)
- Cuaderno de registro para las repeticiones

### Diseño de los blancos de prueba

- **Blanco para M y FOV:** cartulina blanca grande con 2-3 marcas negras gruesas y bien separadas (ej. franjas de 5 cm de ancho, separadas 20-30 cm entre centros). Marcas grandes = medibles con precisión en píxeles sin depender de resolver detalle fino.
- **Blanco para resolución angular:** hoja con varios pares de líneas negras paralelas, cada par con una separación distinta y conocida (ej. pares a 1, 2, 3, 5, 8, 12, 20 mm), impresos con buen contraste.

---

## 2. Método general: fotografía afocal (aplicable a ambas configuraciones)

Se usa el mismo método fotográfico para las dos configuraciones porque funciona sin importar si la pupila de salida es real o virtual — evita el problema de resolver marcas finas a simple vista.

**Pasos:**

1. Monta la cámara en trípode/soporte a distancia fija y medida $L$ del blanco. Registra $L$ (con su incertidumbre, ej. ±0.5 cm por la resolución de la cinta métrica).
2. **Foto de referencia (sin telescopio):** fotografía directa del blanco, foco y zoom fijos, anotados para no cambiarlos.
3. **Foto con telescopio:** acopla el lente de la cámara al ocular (alineado en el eje óptico), sin tocar el zoom, reenfocando solo si es necesario. Fotografía el mismo blanco.
4. Mide en píxeles la distancia entre las mismas dos marcas en ambas fotos: $d_{px,tel}$ y $d_{px,dir}$.
5. Calcula:
$$M = \frac{d_{px,tel}}{d_{px,dir}}$$
6. **Repite los pasos 3-5 un mínimo de 8 veces** por configuración (recentrando el acople cada vez), para tener estadística de error aleatorio.

**Para el FOV**, en la misma foto con telescopio:
- Identifica el borde del círculo de campo visible (donde la imagen se corta o vigneta).
- Mide su ancho en píxeles, $W_{px}$.
- Calibra la escala px→cm usando la regla de 30 cm incluida en el mismo cuadro, a la misma distancia $L$ que el blanco.
- Convierte a longitud real $W$ y calcula:
$$\text{FOV} = 2\arctan\left(\frac{W}{2L}\right)$$
- Repite igual que para M (≥8 veces).

---

## 3. Configuración 1 — Ocular principal (Kepleriano, 25x)

Además del método fotográfico (obligatorio), esta configuración permite un **método de verificación independiente**, porque su pupila de salida es real:

1. Ilumina el telescopio con luz difusa (cielo, pared blanca) y coloca una hoja de papel detrás del ocular.
2. Desliza la hoja hasta encontrar el punto donde el disco de luz proyectado tiene diámetro mínimo y bordes más nítidos — esa es la pupila de salida.
3. Mide su diámetro $D_{salida}$ con calibrador. Repite ≥5 veces variando ligeramente la posición para confirmar el mínimo.
4. Mide el diámetro del objetivo $D_{obj}$ (dato de fábrica: 50 mm, pero verifícalo con calibrador).
5. Calcula:
$$M_{proyección} = \frac{D_{obj}}{D_{salida}}$$
6. **Compara** $M_{proyección}$ contra $M_{fotográfico}$ (sección 2) y contra el valor nominal de fábrica (25x, según el manual). Esta comparación entre dos métodos independientes es evidencia fuerte de la validez de tu medición — inclúyela en el informe.

---

## 4. Configuración 2 — Ocular Galileo (17x, imagen derecha)

Aquí **no se puede proyectar la pupila de salida** porque es virtual (se forma dentro del tubo, del lado del objetivo — solo una de las dos pupilas de un sistema afocal puede ser real, y en el Galileo la real es la de entrada).

1. Aplica **únicamente el método fotográfico** de la sección 2 para M y FOV.
2. Como dato derivado (no como medición independiente de verificación), puedes calcular:
$$D_{salida,virtual} = \frac{D_{obj}}{M_{fotográfico}}$$
y discutir en el informe por qué este valor no puede confirmarse por proyección directa — esto conecta con el objetivo del curso sobre el "significado práctico de la pupila".
3. Compara tu $M_{fotográfico}$ contra el valor nominal de fábrica (17x).

---

## 5. Resolución angular (una configuración: principal + Barlow, 50x)

**Fundamento:** el límite de resolución teórico de un telescopio (criterio de Rayleigh) depende del diámetro del objetivo, no del ocular:
$$\theta_R = 1.22\,\frac{\lambda}{D_{obj}}$$
Con $\lambda \approx 550$ nm (luz visible) y $D_{obj}=50$ mm: $\theta_R \approx 1.34\times10^{-5}$ rad $\approx 2.8$ arcsegundos.

**Aviso realista:** es muy probable que tu resolución *medida* sea mucho peor que este límite teórico, porque en la práctica dominan otros factores (calidad de impresión del blanco, resolución de la cámara, turbulencia atmosférica si mides a distancia larga al aire libre, aberraciones del sistema). Esto **no es un error del experimento** — es un resultado válido y esperado que debes discutir: tu medición te dice cuál es el factor limitante real del sistema, no necesariamente el límite de difracción del objetivo.

**Procedimiento:**

1. Coloca el blanco de pares de líneas (sección 1) a una distancia $L$ conocida — usa la mayor distancia práctica disponible (pasillo largo, patio) para maximizar la resolución angular alcanzable.
2. Fotografía el blanco a través del telescopio (acople afocal, mismo método que antes), asegurando que se vean varios pares de líneas dentro del campo.
3. Con Python (`numpy`/`scipy`, que ya usas en tu pipeline de reflectancia), extrae el perfil de intensidad a lo largo de una línea perpendicular a los pares de líneas, para cada par.
4. Determina el par de **menor separación** cuyo perfil de intensidad todavía muestra un mínimo local claro entre los dos picos (líneas resueltas) — el siguiente par más junto que ya no muestra ese mínimo (se funden en un solo pico) marca tu límite práctico.
5. Convierte la separación física $s_{mín}$ de ese par límite a resolución angular:
$$\theta_{exp} = \frac{s_{mín}}{L}$$
6. Repite con nuevas fotos (≥5) para estimar el error aleatorio del umbral de "líneas resueltas".
7. Compara $\theta_{exp}$ contra $\theta_R$ teórico y discute la brecha.

---

## 6. Estimación de error aleatorio (aplica a M, FOV y resolución)

Para cada cantidad medida repetidamente ($N\geq5$-8 repeticiones):

- Calcula media $\bar{x}$ y desviación estándar muestral $s$.
- Reporta el error de la media:
$$\sigma_{\bar{x}} = \frac{s}{\sqrt{N}}$$

Para cantidades derivadas, propaga el error con derivadas parciales. Ejemplos:

**M por proyección** ($M = D_{obj}/D_{salida}$):
$$\frac{\sigma_M}{M} = \sqrt{\left(\frac{\sigma_{D_{obj}}}{D_{obj}}\right)^2 + \left(\frac{\sigma_{D_{salida}}}{D_{salida}}\right)^2}$$

**FOV** ($= 2\arctan(W/2L)$):
$$\sigma_{FOV} = \frac{2}{1+(W/2L)^2}\sqrt{\left(\frac{\sigma_W}{2L}\right)^2 + \left(\frac{W\sigma_L}{2L^2}\right)^2}$$

**Resolución** ($\theta_{exp} = s_{mín}/L$):
$$\frac{\sigma_{\theta}}{\theta_{exp}} = \sqrt{\left(\frac{\sigma_{s}}{s_{mín}}\right)^2 + \left(\frac{\sigma_L}{L}\right)^2}$$

---

## 7. Fuentes de error sistemático a documentar

- **Desalineación del acople afocal**: el eje del lente de la cámara no coincide exactamente con el eje óptico del telescopio → viñeteo asimétrico, subestimación de M y del FOV.
- **Distorsión geométrica de la cámara** (barril/cojín): afecta más la medición del FOV (zona periférica del cuadro) que la de M (si mides cerca del centro).
- **Diferencia de enfoque entre fotos** (con/sin telescopio): si el foco no es exactamente el mismo, la escala angular de la cámara puede variar levemente ("focus breathing" en algunos lentes).
- **Borde de campo mal definido (viñeteo gradual, no abrupto)**: introduce sesgo dependiente del criterio subjetivo de "dónde termina el campo" — documenta el criterio exacto que usaste (ej. 50% de brillo respecto al centro).
- **No perpendicularidad** del blanco respecto al eje óptico → error de escorzo, subestima $W$.
- **Calibración de la cinta métrica y de la regla de referencia.**
- **Para la resolución:** calidad de impresión del blanco (líneas no perfectamente nítidas), turbulencia atmosférica si se mide al aire libre a distancia larga, resolución/muestreo de píxeles de la cámara (si el "mínimo local" del perfil de intensidad está limitado por el tamaño de píxel más que por la óptica del telescopio).
- **Aberraciones ópticas** (esférica, cromática): pueden hacer que M no sea perfectamente constante en todo el campo, y que la resolución varíe entre el centro y el borde de la imagen.

---

## 8. Estructura sugerida del informe

1. Introducción y objetivos (según guía del curso)
2. Marco teórico: telescopio Kepleriano vs. Galileo, pupila de entrada/salida, criterio de Rayleigh
3. Metodología (resumen de este protocolo, con fotos del montaje)
4. Resultados:
   - Tabla comparativa: M y FOV medidos vs. nominales, para ambas configuraciones
   - Resolución angular medida vs. teórica
   - Todas las incertidumbres reportadas como $\bar{x} \pm \sigma_{\bar{x}}$
5. Análisis de errores (aleatorio + sistemático, según secciones 6-7)
6. Discusión: ¿por qué la pupila de salida del ocular Galileo no pudo verificarse por proyección? ¿Qué factor limitó la resolución medida?
7. Conclusiones