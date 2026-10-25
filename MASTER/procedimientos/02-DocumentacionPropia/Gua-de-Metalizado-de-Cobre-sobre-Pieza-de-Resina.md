# Guía de Metalizado de Cobre sobre Pieza de Resina

## 0\. Lista de materiales

**Preparación de superficie**

- Lija de grano 1200
- Alcohol isopropílico \(IPA\), alcohol metílico y acetona
- Pistola de aire comprimido
- Guantes de nitrilo, gafas de seguridad

**Pintura conductiva**

- Pintura conductiva de grafito coloidal
- Aerógrafo
- Alcohol isopropílico para dilución
- Paño para pulir
- Multímetro \(continuidad/resistencia superficial\)

**Montaje eléctrico**

- Alambre de cobre delgado o clips tipo caimán
- Puntos de contacto mecánico hacia la capa de grafito

**Baño electrolítico \(cobre ácido, 20 L\)**

- Sulfato de cobre pentahidratado \(CuSO₄·5H₂O\)
- Ácido sulfúrico 98% \(ρ ≈ 1\.84 g/cm³\)
- Trazas de cloruro \(sal ionizada o ácido muriático\)
- Agua destilada o desionizada
- Recipiente/tanque de plástico resistente a ácidos \(20 L\)
- Ánodos de cobre de alta pureza \(99\.9%, libre de oxígeno\)
- Fuente de poder DC / rectificador con corriente ajustable
- Multímetro
- Termómetro
- Agitador magnético \+ barra magnética
- Filtro o tela para colar el electrolito

**Seguridad**

- Guantes resistentes a químicos \(nitrilo grueso\), gafas, delantal
- Ventilación adecuada o extracción de vapores

## Paso 1: Preparación de la superficie

1. Lijar las piezas impresas en resina con grano **1200**, con presión ligera y pasadas parejas\.
2. Limpiar y desengrasar:
    1. **IPA** con paño\.
    2. **Metanol** con paño\.
    3. **Acetona** con paño\. \(Poca aplicación\)

## Paso 2: Aplicación de la pintura conductiva de grafito

1. Agitar el envase enérgicamente al menos 30 segundos, hasta escuchar la bolilla metálica moviéndose libremente\.
2. Verificar que la superficie esté limpia, seca y libre de polvo\.
3. Diluir la pintura con IPA en proporción aproximada **1:2** \(una parte de pintura por dos de IPA\) para cargarla en el aerógrafo\.
4. Aplicar una **primera capa fina y pareja** con el aerógrafo sobre toda la pieza impresa en resina\.
5. Dejar secar al aire entre 5 y 15 minutos, hasta que la superficie tenga brillo mate uniforme y no transfiera pigmento al tacto\.
6. Aplicar una **segunda capa** fina repitiendo los pasos 4 y 5\.
7. Aplicar una **tercera capa** fina del mismo modo\.
8. Con la última capa seca, **pulir la superficie con el paño para pulir** hasta eliminar el polvo de grafito y obtener un acabado grafito brillante\.
9. Verificar la continuidad eléctrica con el multímetro entre puntos distantes\. \(Resistencia baja y consistente a lo largo de la pieza\)

## Paso 3: Montaje eléctrico

1. Conectar el cable/clip conductor a la capa de grafito mediante un **contacto mecánico firme**\.
2. Usar **varios puntos de contacto** distribuidos en distintas zonas de la pieza\.

## Paso 4: Preparación del mezcla electrolítica \(10 L\)

### 4\.1 Composición

*[Vista de Tabla](https://miro.com/app/board/uXjVJSvtWQM=/?moveToWidget=3458764682954959808&cot=14)*

| Componente | Cantidad \(10 L\) |
| --- | --- |
| Sulfato de cobre pentahidratado \(CuSO₄·5H₂O\) | 0\.750 kg |
| Ácido sulfúrico 98% \(ρ ≈ 1\.84 g/cm³\) | ≈ 0\.70 L |
| Cloruro de sodio \(NaCl\) | 0\.9 g |
| Agua destilada/desionizada | completar hasta 10 L |

### 4\.2 Solución electrolítica

1. Disolver el **sulfato de cobre** en ~7 L de agua tibia \(~49 °C\) sobre el agitador magnético, hasta disolución completa\.
2. Deja enfriar la solución a temperatura ambiente\.
3. Agregar el **ácido sulfúrico 98% muy lentamente, siempre ácido sobre solución acuosa**, agitando y dejando disipar el calor entre adiciones\.
4. Agregar el **cloruro** \(NaCl\)\.
5. Completar con agua hasta **10 L totales** y deja estabilizar a temperatura ambiente\.

### 4\.3 Tanque, ánodos y agitación

1. Usar un recipiente de plástico de polietileno de alta densidad\.
2. Colocar la **barra magnética** en el fondo del recipiente y ajustar el agitador 500 rpm y constante\.
3. Colocar los **ánodos de cobre** a distancia de 20\-30 cm entre sí\. 
4. Colocar la pieza impresa en resina entre los ánodos\. Asegurar que ni la pieza, ni los ánodos interfieren con la barra\.

## Paso 5: Electrodeposición

1. Iniciar a densidad de corriente baja, **0\.2–0\.5 A/dm²**, durante los primeros minutos, hasta ver una película de cobre continua y uniforme sobre toda la superficie\.
2. Subir a **1–3 A/dm²**, baño entre 20 y 45 °C, agitación magnética constante\.

> **Corriente total** = densidad de corriente x área a metalizar \(dm²\)\. Ejemplo: área ≈ 1\.5 dm² a 2 A/dm² → ≈ 3 A totales\.

### 5\.1 Tiempo según espesor

*[Vista de Tabla](https://miro.com/app/board/uXjVJSvtWQM=/?moveToWidget=3458764682954959809&cot=14)*

| Densidad de corriente | Tasa aproximada |
| --- | --- |
| 1 A/dm² | ~13 µm/hora |
| 2 A/dm² | ~25 µm/hora |
| 3 A/dm² | ~38 µm/hora |

**Espesor objetivo: 25–35 µm** de cobre\. A 2 A/dm² ≈ 1–1\.5 horas de deposición principal, después del golpe inicial\.

## Paso 6: Enjuague, secado e inspección

1. Retirar la pieza y **enjuagar** abundantemente con agua limpia\.
2. **Secar** completamente\.

