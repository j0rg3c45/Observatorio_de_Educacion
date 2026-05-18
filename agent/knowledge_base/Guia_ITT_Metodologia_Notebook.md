# Metodología Índice de Calidad Educativa Territorial (ICET) — Observatorio de Educación

## Guía técnica para cálculo, calibración y análisis de indicadores educativos por sede/institución

**Versión:** 1.0  
**Última actualización:** Mayo 2026  
**Fuente base:** Metodología ITT · Adaptación para dimensión educativa con datos SED Cali  
**Propósito:** Documento de referencia para un agente de IA que asista en la construcción, análisis y seguimiento de indicadores educativos territoriales.

---

## 1. Definición del ICET

El Índice de Calidad Educativa Territorial (ICET) es una medición compuesta que cuantifica las condiciones del servicio educativo en sedes e instituciones del municipio de Santiago de Cali.

Opera en una escala de **0 a 100** donde valores más altos indican mejores condiciones educativas. Mide acceso, eficiencia, recursos y condiciones de infraestructura.

### Clasificación

| Rango | Nivel | Descripción |
|-------|-------|-------------|
| 0 – 40 | Nivel 1 · Crítico | Condiciones deficientes. Requiere intervención prioritaria |
| 40 – 60 | Nivel 2 · En desarrollo | Avances parciales con brechas significativas |
| 60 – 80 | Nivel 3 · Adecuado | Condiciones aceptables con oportunidades de mejora |
| 80 – 100 | Nivel 4 · Óptimo | Condiciones robustas y sostenibles |

---

## 2. Dimensiones y ponderaciones

| Dimensión | Peso | Tipo general | Indicadores base |
|-----------|------|-------------|-----------------|
| Cobertura y Acceso | 30% | Positivo/Inverso | Matrícula total, Tasa de cobertura bruta, Tasa de cobertura neta |
| Eficiencia Interna | 25% | Inverso/Positivo | Deserción, Repitencia, Tasa de aprobación, Tasa de reprobación |
| Recursos Pedagógicos | 20% | Inverso/Positivo | Estudiantes por docente, Estudiantes por equipo de cómputo |
| Infraestructura | 15% | Positivo | Intervenciones realizadas, Estado de sedes, Inversión ejecutada |
| Dotación Tecnológica | 10% | Positivo | Equipos de cómputo disponibles, Ratio equipos/estudiantes |

**La suma de los pesos debe ser siempre 1.0 (100%).**

Los pesos reflejan la prioridad estratégica del Plan de Desarrollo para educación. Cobertura tiene el mayor peso (30%) por ser la condición habilitante del derecho a la educación.

---

## 3. Fórmula de cálculo — 3 pasos

### Paso 1 — Normalización por indicador con ref_min / ref_max

Cada indicador se transforma a una escala común de 0 a 100 mediante umbrales de referencia fijos.

**Fórmula base:**

```
score_raw = clamp( (valor - ref_min) / (ref_max - ref_min) × 100,  0, 100 )
```

**Para indicadores inversos** (menor valor = mejor resultado: deserción, repitencia, estudiantes/docente):

```
score = 100 - score_raw
```

**Para indicadores positivos** (mayor valor = mejor resultado: matrícula, cobertura, aprobación):

```
score = score_raw
```

El uso de `clamp(resultado, 0, 100)` garantiza que el score final permanezca dentro del rango 0-100.

### Paso 2 — Score de dimensión (promedio simple)

Cada dimensión agrega sus indicadores con igual peso entre ellos:

```
Score_dim = (Score_ind1 + Score_ind2 + ... + Score_indN) / N
```

Ejemplos:
- Score_Cobertura = (Score_Matricula + Score_Cobertura_Bruta + Score_Cobertura_Neta) / 3
- Score_Eficiencia = (Score_Desercion + Score_Repitencia + Score_Aprobacion + Score_Reprobacion) / 4
- Score_Recursos = (Score_Estudiantes_Docente + Score_Estudiantes_Equipo) / 2

### Paso 3 — Índice compuesto ICET (suma ponderada)

```
ICET = 0.30 × Cobertura + 0.25 × Eficiencia + 0.20 × Recursos + 0.15 × Infraestructura + 0.10 × Dotación
```

---

## 4. Umbrales ref_min / ref_max — Indicadores Educativos

Los umbrales ref_min y ref_max son determinantes en la sensibilidad del score. Se definen con base en estándares nacionales (MEN), metas del Plan de Desarrollo y datos históricos de Cali.

### 4.1 Indicadores de Cobertura y Acceso

| Indicador | ref_min | ref_max | Tipo | Sustento |
|-----------|---------|---------|------|----------|
| Tasa de cobertura bruta (%) | 80 | 120 | Positivo | Meta MEN: cobertura universal. >100% indica extraedad |
| Tasa de cobertura neta (%) | 60 | 100 | Positivo | Meta ideal: 100% de población en edad escolar |
| Matrícula por sede | Varía por nivel | Varía por nivel | Positivo | Depende de capacidad instalada |

### 4.2 Indicadores de Eficiencia Interna

| Indicador | ref_min | ref_max | Tipo | Sustento |
|-----------|---------|---------|------|----------|
| Tasa de deserción (%) | 0.5 | 12.0 | Inverso | Meta Plan Desarrollo <3%. Máx histórico ~10% |
| Tasa de repitencia (%) | 0.5 | 15.0 | Inverso | Meta <5%. Máx observado ~12% |
| Tasa de aprobación (%) | 70 | 100 | Positivo | Meta >90%. Mín aceptable 70% |
| Tasa de reprobación (%) | 0 | 30 | Inverso | Meta <5%. Máx observado ~25% |

### 4.3 Indicadores de Recursos Pedagógicos

| Indicador | ref_min | ref_max | Tipo | Sustento |
|-----------|---------|---------|------|----------|
| Estudiantes por docente | 15 | 45 | Inverso | Estándar MEN: 32 (urbano), 22 (rural). Ideal <25 |
| Estudiantes por equipo de cómputo | 1 | 20 | Inverso | Meta Plan Desarrollo: 1 equipo por cada 5 estudiantes |

### 4.4 Indicadores de Infraestructura

| Indicador | ref_min | ref_max | Tipo | Sustento |
|-----------|---------|---------|------|----------|
| Intervenciones ejecutadas (por sede) | 0 | 5 | Positivo | Histórico de obras 2020-2025 |
| Inversión ejecutada (millones COP) | 0 | 5,000 | Positivo | Rango de inversión por sede según empréstito |

### 4.5 Indicadores de Dotación Tecnológica

| Indicador | ref_min | ref_max | Tipo | Sustento |
|-----------|---------|---------|------|----------|
| Equipos de cómputo por sede | 5 | 100 | Positivo | Rango observado en inventario SED |
| Ratio equipos/estudiantes | 0.05 | 0.50 | Positivo | Meta: 1 equipo cada 5 estudiantes (0.20) |

---

## 5. Fuentes de datos disponibles — Observatorio de Educación

### 5.1 Inventario de archivos

| Archivo | Carpeta | Contenido | Periodicidad |
|---------|---------|-----------|-------------|
| 01_Matricula_2026.xlsx | Reporte de matrícula | Matrícula por sede, nivel, grado, jornada | Anual (corte 2026) |
| 02_Indicadores_2026.xlsx | Indicadores de eficiencia y cobertura | Tasas de deserción, repitencia, aprobación, cobertura | Anual (corte 2026) |
| 03_Estudiantes_por_docente_y_equipo_2026.xlsx | Indicadores de docentes y equipos | Ratio estudiantes/docente y estudiantes/equipo | Anual (corte 2026) |
| Información geográfica sedes.xlsx | Fuentes de datos | Coordenadas y ubicación de sedes educativas | Estático |
| REPORTE DE INVENTARIO DE EQUIPOS DE COMPUTO SEDES EDUCATIVAS.xlsx | Fuentes de datos | Inventario detallado de equipos por sede | Corte único |
| 22 SEDES.xlsx | Intervenciones de infraestructura | 22 sedes con intervención | Corte único |
| 49 sedes Empréstito - Valores 2026 y 2027.xlsx | Intervenciones de infraestructura | Inversiones programadas empréstito | Proyección 2026-2027 |
| HISTORICO OBRAS 2020-2025.xlsx | Intervenciones de infraestructura | Histórico de obras ejecutadas | Serie 2020-2025 |

### 5.2 Relación fuentes-dimensiones

| Dimensión | Fuentes principales | Estado |
|-----------|-------------------|--------|
| Cobertura y Acceso | 01_Matricula_2026.xlsx, 02_Indicadores_2026.xlsx | Datos reales disponibles |
| Eficiencia Interna | 02_Indicadores_2026.xlsx | Datos reales disponibles |
| Recursos Pedagógicos | 03_Estudiantes_por_docente_y_equipo_2026.xlsx | Datos reales disponibles |
| Infraestructura | HISTORICO OBRAS 2020-2025.xlsx, 22 SEDES.xlsx, 49 sedes Empréstito | Datos reales disponibles |
| Dotación Tecnológica | REPORTE DE INVENTARIO DE EQUIPOS DE COMPUTO.xlsx | Datos reales disponibles |

### 5.3 Información geográfica

- Archivo: `Información geográfica sedes.xlsx`
- Contenido: Coordenadas de sedes educativas oficiales
- Uso: Georreferenciación para análisis territorial (por comuna, barrio, zona)
- CRS esperado: EPSG:4326 (WGS84) o MAGNA-SIRGAS

---

## 6. Unidades de análisis

El Observatorio de Educación permite análisis a múltiples niveles de agregación:

| Nivel | Descripción | Uso principal |
|-------|-------------|---------------|
| Sede | Unidad física individual | Diagnóstico puntual, priorización de intervenciones |
| Institución Educativa (IE) | Agrupación de sedes bajo una misma dirección | Gestión administrativa, comparación entre IE |
| Comuna | Agregación territorial | Análisis de brechas territoriales |
| Zona (urbana/rural) | Clasificación geográfica | Políticas diferenciadas |
| Municipal | Totalidad del municipio | Indicadores agregados, metas Plan de Desarrollo |

---

## 7. Cómo calibrar ref_min / ref_max para indicadores educativos

### 7.1 Principios generales

1. **ref_min** = mejor resultado razonable (meta aspiracional o estándar MEN)
2. **ref_max** = peor resultado tolerable o máximo observado con margen
3. Los refs deben ser **fijos y documentados** — no calculados dinámicamente
4. Usar estándares nacionales (MEN) como referencia principal cuando existan

### 7.2 Fuentes para definir refs en educación

| Fuente | Aplicación |
|--------|-----------|
| Estándares MEN | Ratios estudiantes/docente, metas de cobertura |
| Plan de Desarrollo Municipal | Metas de deserción, cobertura, dotación |
| Datos históricos SED Cali | Rangos observados en años anteriores |
| Benchmarks nacionales | Promedios departamentales y nacionales |

### 7.3 Reglas prácticas de calibración

| Regla | Descripción |
|-------|-------------|
| No usar min-max relativo | Nunca calcular ref_min/ref_max a partir de los propios datos. Esto infla scores |
| Documentar siempre | Cada ref debe tener justificación (estándar MEN, meta PD, histórico) |
| Diferenciar urbano/rural | Los estándares MEN difieren por zona; aplicar refs diferenciados |
| Sensibilidad | Probar el ICET con +/-20% en refs para evaluar estabilidad |
| Consistencia temporal | Mantener los mismos refs entre cortes anuales para comparabilidad |

### 7.4 Errores comunes a evitar

| Error | Consecuencia | Corrección |
|-------|-------------|-----------|
| Usar min-max relativo de la muestra | Scores extremos con muestras pequeñas | Usar refs fijos basados en estándares |
| ref_min = ref_max | División por cero | Asegurar que siempre ref_max > ref_min |
| No diferenciar niveles educativos | Comparar preescolar con media sin ajuste | Aplicar refs por nivel cuando corresponda |
| No invertir indicadores negativos | Más deserción = mejor score (absurdo) | Verificar flag inverso por indicador |
| Mezclar sedes con IE | Doble conteo o promedios incorrectos | Definir unidad de análisis antes de calcular |

---

## 8. Tratamiento de datos nulos y ausentes

Los datos ausentes se manejan en dos niveles:

1. **Sedes sin reporte:** Sedes que no reportan matrícula o indicadores se excluyen del cálculo pero se documentan como brecha de información.

2. **Ceros legítimos:** Sedes nuevas o sin matrícula en un nivel específico reciben valor cero, que refleja ausencia real del servicio.

3. **Datos incompletos por dimensión:** Si una sede no tiene datos para una dimensión completa, esa dimensión se excluye y se recalculan los pesos proporcionalmente.

En ningún caso se inventan o estiman datos faltantes. No se realiza imputación estadística.

---

## 9. Implementación en Python (estructura del notebook)

### Función de normalización con refs fijos

```python
def score_ref(valor, ref_min, ref_max, inverso):
    """Normaliza un valor con umbrales fijos ref_min/ref_max."""
    if ref_max == ref_min:
        return 100.0
    raw = np.clip((valor - ref_min) / (ref_max - ref_min) * 100, 0, 100)
    return 100 - raw if inverso else raw
```

### Definición de refs en el notebook (editables)

```python
REFS = {
    #                        ref_min  ref_max  inverso  descripcion
    'desercion':            (0.5,    12.0,    True,    'Tasa de desercion (%)'),
    'repitencia':           (0.5,    15.0,    True,    'Tasa de repitencia (%)'),
    'aprobacion':           (70.0,   100.0,   False,   'Tasa de aprobacion (%)'),
    'reprobacion':          (0.0,    30.0,    True,    'Tasa de reprobacion (%)'),
    'est_por_docente':      (15.0,   45.0,    True,    'Estudiantes por docente'),
    'est_por_equipo':       (1.0,    20.0,    True,    'Estudiantes por equipo computo'),
    'cobertura_bruta':      (80.0,   120.0,   False,   'Tasa cobertura bruta (%)'),
    'cobertura_neta':       (60.0,   100.0,   False,   'Tasa cobertura neta (%)'),
    'equipos_sede':         (5.0,    100.0,   False,   'Equipos de computo por sede'),
    'ratio_equipos_est':    (0.05,   0.50,    False,   'Ratio equipos/estudiantes'),
}
```

### Pesos por dimensión

```python
PESOS = {
    'cobertura':       0.30,
    'eficiencia':      0.25,
    'recursos':        0.20,
    'infraestructura': 0.15,
    'dotacion':        0.10,
}
```

### Cálculo del ICET

```python
# Normalizar indicadores
for ind, (rmin, rmax, inv, desc) in REFS.items():
    df[f'score_{ind}'] = df[ind].apply(lambda v: score_ref(v, rmin, rmax, inv))

# Scores por dimension
df['score_cobertura'] = (
    df['score_cobertura_bruta'] + df['score_cobertura_neta']
) / 2

df['score_eficiencia'] = (
    df['score_desercion'] + df['score_repitencia'] +
    df['score_aprobacion'] + df['score_reprobacion']
) / 4

df['score_recursos'] = (
    df['score_est_por_docente'] + df['score_est_por_equipo']
) / 2

df['score_dotacion'] = (
    df['score_equipos_sede'] + df['score_ratio_equipos_est']
) / 2

# ICET compuesto
df['ICET'] = (
    PESOS['cobertura'] * df['score_cobertura'] +
    PESOS['eficiencia'] * df['score_eficiencia'] +
    PESOS['recursos'] * df['score_recursos'] +
    PESOS['infraestructura'] * df['score_infraestructura'] +
    PESOS['dotacion'] * df['score_dotacion']
)
```

---

## 10. Flujo de trabajo para el Observatorio de Educación

### Paso 1 — Carga y exploración de datos
Cargar cada archivo Excel. Verificar estructura, columnas, nulos, duplicados y tipos de datos.

### Paso 2 — Limpieza y estandarización
Estandarizar nombres de sedes/IE. Cruzar con información geográfica. Validar consistencia entre fuentes.

### Paso 3 — Cálculo de indicadores base
Calcular tasas, ratios y métricas por sede/IE/comuna según la unidad de análisis definida.

### Paso 4 — Normalización con ref_min/ref_max
Aplicar la función de normalización con los refs definidos. Verificar que no haya scores extremos injustificados.

### Paso 5 — Agregación por dimensión y cálculo del ICET
Promediar indicadores por dimensión. Aplicar pesos. Calcular índice compuesto.

### Paso 6 — Análisis territorial
Cruzar con información geográfica. Generar mapas por comuna. Identificar brechas territoriales.

### Paso 7 — Validación y reporte
Verificar resultados con expertos de la SED. Generar reportes y visualizaciones.

---

## 11. Relación con el ITT general

El Observatorio de Educación alimenta la **dimensión de Educación y Desarrollo** del Índice de Transformación Territorial (ITT). Los indicadores derivados que se exportan al ITT son:

- Matrícula escolar por zona de intervención
- Tasa de deserción por zona
- Tasa de repitencia por zona
- Ratio estudiantes por docente por zona
- Cobertura deportiva/recreativa (cuando aplique)

El ICET es un índice más granular y específico que permite:
1. Diagnóstico detallado a nivel de sede/IE
2. Priorización de intervenciones educativas
3. Seguimiento de metas del Plan de Desarrollo en educación
4. Alimentar con datos consolidados la dimensión educativa del ITT

---

## 12. Observaciones metodológicas finales

- Las referencias mínimas y máximas son determinantes en la sensibilidad del score. Cambios en estos límites modifican directamente la posición relativa de cada indicador.
- El índice final es comparable entre sedes porque todos los indicadores fueron llevados a una escala homogénea de 0 a 100 antes de la agregación ponderada.
- Las dimensiones con menor puntaje deben interpretarse como frentes prioritarios de intervención.
- Diferenciar siempre entre niveles educativos (preescolar, básica primaria, básica secundaria, media) cuando los indicadores lo permitan.
- Los datos de infraestructura (obras, empréstito) son complementarios y no deben confundirse con indicadores de resultado educativo.
- El ICET es un índice de seguimiento operativo, no un modelo econométrico. Su valor está en la comparabilidad y el seguimiento temporal.
- La lectura correcta prioriza los indicadores con datos completos y reconoce las limitaciones de los indicadores con un solo corte.

---

## 13. Glosario

| Término | Definición |
|---------|-----------|
| ICET | Índice de Calidad Educativa Territorial |
| ITT | Índice de Transformación Territorial (índice padre) |
| SED | Secretaría de Educación Municipal |
| MEN | Ministerio de Educación Nacional |
| IE | Institución Educativa (agrupa varias sedes) |
| Sede | Unidad física donde se presta el servicio educativo |
| Score | Valor normalizado 0-100 de un indicador o dimensión |
| ref_min | Umbral inferior de normalización (mejor resultado razonable) |
| ref_max | Umbral superior de normalización (peor resultado tolerable) |
| clamp | Función que acota un valor al rango [0, 100] |
| Indicador inverso | Indicador donde menor valor = mejor resultado (deserción, repitencia) |
| Indicador positivo | Indicador donde mayor valor = mejor resultado (matrícula, cobertura) |
| Tasa de cobertura bruta | Matrícula total / Población en edad escolar × 100 |
| Tasa de cobertura neta | Matrícula en edad adecuada / Población en edad escolar × 100 |
| Tasa de deserción | Estudiantes que abandonan / Matrícula inicial × 100 |
| Tasa de repitencia | Estudiantes que repiten / Matrícula total × 100 |
| Ratio estudiantes/docente | Total estudiantes / Total docentes en la sede |
| Ratio estudiantes/equipo | Total estudiantes / Total equipos de cómputo |
| Empréstito | Crédito público para inversión en infraestructura educativa |
| DANE | Código único de identificación de sedes educativas |
| Jornada | Turno de operación de la sede (mañana, tarde, completa, nocturna) |
