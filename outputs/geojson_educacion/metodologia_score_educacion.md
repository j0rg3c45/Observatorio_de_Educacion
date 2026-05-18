# Metodologia de Calculo - Score Dimension Educacion ITT

## Contexto del archivo GeoJSON

**Archivo:** `score_educacion_por_comuna_2026.geojson`
**Fecha de generacion:** Mayo 2026
**Proyecto:** Observatorio de Educacion - Santiago de Cali
**Equipo:** ITT Cali Inteligente - Gobierno de Datos

---

## 1. Que es el Score de Educacion

El score de la dimension Educacion y Desarrollo es un componente del Indice de
Transformacion Territorial (ITT). Mide las condiciones del servicio educativo
en cada comuna de Cali en una escala de 0 a 100.

Este score reemplaza el referente provisional de Pulmon de Oriente (54.9) que
se usaba anteriormente, con un calculo basado en datos reales 2026.

---

## 2. Fuentes de datos utilizadas

| Fuente | Archivo | Dato extraido |
|--------|---------|---------------|
| Matricula 2026 | 01_Matricula_2026.xlsx (hoja Por comuna) | Matricula total por comuna |
| Docentes y equipos | 03_Estudiantes_por_docente_y_equipo_2026.xlsx (hoja Detalle por sede) | Equipos y ratio est/equipo por sede |
| Info geografica | Informacion geografica sedes.xlsx | Asignacion de comuna a cada sede (campo EEComCor) |
| Poligonos comunas | info_geografica/Comunas.zip | Geometria de las 22 comunas urbanas |

Todas las fuentes provienen de la Secretaria de Educacion Municipal (SED) de Cali.
Datos SIMAT Anexo 6a y 5a, corte Marzo 2026.

---

## 3. Indicadores utilizados

| Indicador | Valor | Tipo | Variacion por comuna |
|-----------|-------|------|---------------------|
| Matricula total | 5,313 - 25,902 | Positivo | SI (dato real por comuna) |
| Tasa de repitencia | 6.82% | Inverso | NO (constante municipal) |
| Estudiantes por docente | 24.64 | Inverso | NO (constante municipal) |
| Estudiantes por equipo | Variable por comuna | Inverso | SI (agregado de sedes) |

---

## 4. Referencias fijas (ref_min / ref_max)

| Indicador | ref_min | ref_max | Sustento |
|-----------|---------|---------|----------|
| Matricula | 5,000 | 30,000 | Rango observado en 22 comunas (5,313 - 25,902) |
| Repitencia (%) | 1.0 | 15.0 | Meta Plan Desarrollo <5%, max historico ~12% |
| Est/Docente | 15 | 40 | Estandar MEN: 32 urbano, ideal <25 |
| Est/Equipo | 1 | 20 | Meta Plan Desarrollo: 1 equipo cada 5 estudiantes |

---

## 5. Formula de calculo

### Paso 1 - Normalizacion por indicador

Cada indicador se transforma a escala 0-100:

```
score_raw = clamp( (valor - ref_min) / (ref_max - ref_min) * 100,  0, 100 )
```

Para indicadores inversos (menor = mejor): `score = 100 - score_raw`
Para indicadores positivos (mayor = mejor): `score = score_raw`

### Paso 2 - Score de dimension (promedio simple)

```
Score_Educacion = (score_matricula + score_repitencia + score_est_docente + score_est_equipo) / 4
```

Los 4 indicadores tienen igual peso dentro de la dimension.

### Paso 3 - Clasificacion

| Rango | Nivel | Descripcion |
|-------|-------|-------------|
| 0 - 40 | Nivel 1 - Critico | Condiciones deficientes |
| 40 - 60 | Nivel 2 - En desarrollo | Avances parciales |
| 60 - 80 | Nivel 3 - Adecuado | Condiciones aceptables |
| 80 - 100 | Nivel 4 - Optimo | Condiciones robustas |

---

## 6. Proceso de cruce territorial

1. Se carga la matricula por comuna directamente (hoja "Por comuna" del archivo 01).
2. Se carga el detalle de 337 sedes oficiales con equipos de computo.
3. Se cruza cada sede con su comuna usando el campo `EeCodDane` de la info geografica.
4. Se agrega el ratio estudiantes/equipo por comuna (promedio de las sedes).
5. Se aplican los indicadores municipales constantes (repitencia, est/docente).
6. Se normalizan los 4 indicadores con refs fijos.
7. Se calcula el score promedio.
8. Se hace merge con los poligonos de comunas y se exporta como GeoJSON en WGS84.

---

## 7. Campos del GeoJSON

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| num_comuna | int | Numero de comuna (1-22) |
| comuna | string | Nombre (ej: "Comuna 14") |
| matricula_total | float | Matricula total de la comuna (oficial + no oficial) |
| matricula_oficial | float | Matricula solo sector oficial |
| equipos_total | float | Total equipos de computo en sedes oficiales |
| est_equipo_prom | float | Promedio de estudiantes por equipo en la comuna |
| repitencia | float | Tasa de repitencia (%) - valor municipal |
| est_por_docente | float | Ratio estudiantes/docente - valor municipal |
| score_matricula | float | Score normalizado de matricula (0-100) |
| score_repitencia | float | Score normalizado de repitencia (0-100) |
| score_est_docente | float | Score normalizado de est/docente (0-100) |
| score_est_equipo | float | Score normalizado de est/equipo (0-100) |
| score_educacion | float | Score final de la dimension (0-100) |
| nivel | string | Clasificacion (Critico/En desarrollo/Adecuado/Optimo) |
| geometry | Polygon | Poligono de la comuna en EPSG:4326 |

---

## 8. Limitaciones

- Repitencia y Est/Docente son constantes municipales. No varian entre comunas.
- La variacion real del score entre comunas se explica solo por Matricula y Est/Equipo.
- No se incluye desercion (dato no disponible en fuentes actuales).
- No se incluye cobertura bruta/neta por comuna (requiere poblacion DANE por comuna).
- Cuando se consiga desglose por comuna de repitencia y docentes, el score sera mas preciso.

---

## 9. Como reproducir

Ejecutar el script:

```bash
uv run scripts/generar_geojson_educacion.py
```

O en Google Colab:

```python
!python scripts/generar_geojson_educacion.py
```

El notebook completo con graficos esta en:
`notebooks/03_dimension_educacion_itt.ipynb`

---

## 10. Uso del GeoJSON

El archivo se puede abrir en:
- QGIS (arrastrar y soltar)
- ArcGIS (agregar capa)
- Kepler.gl (importar archivo)
- geojson.io (pegar contenido)
- Cualquier libreria geoespacial (geopandas, leaflet, mapbox)
