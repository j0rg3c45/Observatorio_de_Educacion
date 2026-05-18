# Proceso para calcular la Linea Base de Educacion por Comuna

## Para replicar en el ITT general

**Repositorio:** https://github.com/j0rg3c45/Observatorio_de_Educacion.git
**Notebook:** `notebooks/03_dimension_educacion_itt.ipynb`
**Seccion de referencia:** 15. Indicadores de linea base - Valores unicos por comuna

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/j0rg3c45/Observatorio_de_Educacion.git
cd Observatorio_de_Educacion
```

En Colab:
```python
import os
REPO_DIR = '/content/Observatorio_de_Educacion'
if not os.path.exists(REPO_DIR):
    os.system('git clone https://github.com/j0rg3c45/Observatorio_de_Educacion.git ' + REPO_DIR)
os.chdir(REPO_DIR)
DATA_PATH = 'data/Fuentes de datos'
```

---

## 2. Archivos de entrada

| Archivo | Ruta | Dato que aporta |
|---------|------|-----------------|
| Matricula 2026 | `data/Fuentes de datos/Reporte de matricula/01_Matricula_2026.xlsx` | Matricula por comuna (hoja "Por comuna") |
| Docentes y equipos | `data/Fuentes de datos/Indicadores de docentes y equipos de computo/03_Estudiantes_por_docente_y_equipo_2026.xlsx` | Sedes, equipos, est/equipo (hoja "Detalle por sede") |
| Info geografica | `data/Fuentes de datos/Informacion geografica sedes.xlsx` | Asignacion de comuna a cada sede (campo EEComCor) |
| Historico obras | `data/Fuentes de datos/Intervenciones de infraestructura/HISTORICO OBRAS 2020-2025.xlsx` | Obras, inversion, sedes intervenidas por comuna |
| Indicadores 2026 | `data/Fuentes de datos/Indicadores de eficiencia y de cobertura/02_Indicadores_2026.xlsx` | Repitencia, cobertura (nivel municipal) |

---

## 3. Proceso paso a paso

### Paso 3.1 - Cargar matricula por comuna

```python
df_comuna = pd.read_excel(ruta_mat, sheet_name='Por comuna')
df_cu = df_comuna[df_comuna['comuna'].str.contains('Comuna', na=False)].copy()
df_cu['num_comuna'] = df_cu['comuna'].str.extract(r'(\d+)').astype(int)
df_cu = df_cu.sort_values('num_comuna').reset_index(drop=True)
```

Resultado: 22 comunas urbanas con columnas `Oficial`, `No oficial`, `Total`.

### Paso 3.2 - Cargar detalle por sede y asignar comuna

```python
# Cargar sedes
df_sede = pd.read_excel(ruta_doc, sheet_name='Detalle por sede')

# Cargar info geografica
df_geo = pd.read_excel(ruta_geo)

# Cruzar sede con comuna usando codigo DANE
df_geo_min = df_geo[['EeCodDane', 'EEComCor']].copy()
df_geo_min['EeCodDane'] = df_geo_min['EeCodDane'].astype(str).str.strip()
df_sede['cod_dane_sede'] = df_sede['cod_dane_sede'].astype(str).str.strip()

df_sc = df_sede.merge(df_geo_min, left_on='cod_dane_sede', right_on='EeCodDane', how='left')
df_sc = df_sc[df_sc['EEComCor'].between(1, 22)].copy()
df_sc['num_comuna'] = df_sc['EEComCor'].astype(int)
```

Resultado: 337 sedes con comuna asignada.

### Paso 3.3 - Agregar equipos por comuna

```python
equipo_comuna = df_sc.groupby('num_comuna').agg(
    sedes_oficiales=('cod_dane_sede', 'nunique'),
    equipos_computo=('equipos', 'sum'),
    est_por_equipo=('estudiantes_por_equipo', 'mean')
).reset_index()
```

Resultado: Un valor unico por comuna de sedes, equipos y ratio.

### Paso 3.4 - Cargar historico de obras

```python
df_obras = pd.read_excel(ruta_obras, header=None, skiprows=2)
df_obras.columns = ['Num', 'Ano', 'IEO', 'Sede', 'Com', 'Estudiantes', 'Comuna',
                    'Proyecto', 'Valor_obra', 'Valor_interventoria', 'Valor_estudios',
                    'Inversion', ...]

# Limpiar
df_obras['Ano'] = pd.to_numeric(df_obras['Ano'], errors='coerce')
df_obras = df_obras[df_obras['Ano'].notna()].copy()
df_obras['Com_num'] = pd.to_numeric(df_obras['Com'], errors='coerce')
df_obras['Inversion_num'] = pd.to_numeric(df_obras['Inversion'], errors='coerce')
df_obras_urb = df_obras[df_obras['Com_num'].between(1, 22)].copy()
```

### Paso 3.5 - Agregar infraestructura por comuna

```python
infra_comuna = df_obras_urb.groupby('Com_num').agg(
    obras_2020_2025=('Num', 'count'),
    sedes_intervenidas=('Sede', 'nunique'),
    inversion_acumulada_M=('Inversion_num', 'sum')
).reset_index()
infra_comuna['inversion_acumulada_M'] = infra_comuna['inversion_acumulada_M'] / 1e6
infra_comuna.rename(columns={'Com_num': 'num_comuna'}, inplace=True)
```

### Paso 3.6 - Contar IE por comuna

```python
ie_count = df_geo[['EeNomIns', 'EEComCor']].copy()
ie_count['EEComCor'] = pd.to_numeric(ie_count['EEComCor'], errors='coerce')
ie_count = ie_count[ie_count['EEComCor'].between(1, 22)]
ie_count = ie_count.groupby('EEComCor')['EeNomIns'].nunique().reset_index()
ie_count.columns = ['num_comuna', 'instituciones_educativas']
```

### Paso 3.7 - Construir tabla maestra (merge)

```python
linea_base = df_cu[['num_comuna', 'comuna', 'Oficial', 'No oficial', 'Total']].copy()
linea_base.columns = ['num_comuna', 'comuna', 'matricula_oficial',
                      'matricula_no_oficial', 'matricula_total']

linea_base = linea_base.merge(equipo_comuna, on='num_comuna', how='left')
linea_base = linea_base.merge(infra_comuna, on='num_comuna', how='left').fillna(0)
linea_base = linea_base.merge(ie_count, on='num_comuna', how='left')
```

### Paso 3.8 - Calcular indicadores derivados

```python
linea_base['pct_oficial'] = (linea_base['matricula_oficial'] / linea_base['matricula_total'] * 100).round(1)
linea_base['matricula_por_sede'] = (linea_base['matricula_oficial'] / linea_base['sedes_oficiales']).round(0)
linea_base['equipos_por_sede'] = (linea_base['equipos_computo'] / linea_base['sedes_oficiales']).round(0)
```

### Paso 3.9 - Agregar constantes municipales

```python
linea_base['repitencia_pct'] = 6.82
linea_base['est_por_docente'] = 24.64
linea_base['cobertura_bruta_pct'] = 75.78
linea_base['cobertura_neta_pct'] = 68.87
```

---

## 4. Resultado: Tabla de linea base

22 filas (una por comuna) con estos indicadores unicos:

| Indicador | Tipo | Varia por comuna |
|-----------|------|-----------------|
| matricula_total | Real | SI |
| matricula_oficial | Real | SI |
| matricula_no_oficial | Real | SI |
| pct_oficial | Derivado | SI |
| sedes_oficiales | Real | SI |
| instituciones_educativas | Real | SI |
| equipos_computo | Real | SI |
| est_por_equipo | Real | SI |
| matricula_por_sede | Derivado | SI |
| equipos_por_sede | Derivado | SI |
| obras_2020_2025 | Real (acumulado) | SI |
| sedes_intervenidas | Real (acumulado) | SI |
| inversion_acumulada_M | Real (acumulado) | SI |
| repitencia_pct | Constante | NO |
| est_por_docente | Constante | NO |
| cobertura_bruta_pct | Constante | NO |
| cobertura_neta_pct | Constante | NO |

---

## 5. Normalizacion (para calcular scores)

```python
def score_ref(valor, ref_min, ref_max, inverso):
    """Normaliza un valor con umbrales fijos ref_min/ref_max."""
    if ref_max == ref_min:
        return 100.0
    raw = np.clip((valor - ref_min) / (ref_max - ref_min) * 100, 0, 100)
    return 100 - raw if inverso else raw
```

### Referencias fijas usadas:

| Indicador | ref_min | ref_max | Tipo | Sustento |
|-----------|---------|---------|------|----------|
| Matricula | 5,000 | 30,000 | Positivo | Rango observado 22 comunas |
| Repitencia (%) | 1.0 | 15.0 | Inverso | Meta PD <5%, max historico ~12% |
| Est/Docente | 15 | 40 | Inverso | Estandar MEN: 32 urbano |
| Est/Equipo | 1 | 20 | Inverso | Meta PD: 1 equipo cada 5 est |
| Obras acumuladas | 1 | 35 | Positivo | Rango observado |
| Inversion (M) | 100 | 9,000 | Positivo | Rango observado |

---

## 6. Calculo del score

```python
# Score Educacion (promedio de 4 indicadores)
score_educacion = (score_matricula + score_repitencia + score_est_docente + score_est_equipo) / 4

# Score Infraestructura (promedio de 2 indicadores)
score_infraestructura = (score_obras + score_inversion) / 2

# ICET parcial (2 dimensiones)
icet_parcial = 0.75 * score_educacion + 0.25 * score_infraestructura
```

---

## 7. Para integrar en el ITT general

El score de Educacion calculado aqui reemplaza el referente provisional (54.9).
Para usarlo en el ITT de una zona especifica:

1. Identificar las comunas que componen la zona de intervencion.
2. Filtrar la tabla `linea_base` por esas comunas.
3. Promediar el `score_educacion` de las comunas de la zona.
4. Usar ese valor como la dimension "Educacion y Desarrollo" del ITT.

Ejemplo para Barrio Obrero (Comuna 9):
```python
score_edu_c9 = linea_base[linea_base['num_comuna'] == 9]['score_educacion']
# Usar este valor en vez de REF_EDUC_DES = 54.9
```

---

## 8. Ejecucion rapida

```bash
# Local
uv run scripts/generar_geojson_educacion.py

# Colab
!python scripts/generar_geojson_educacion.py
```

Genera: `outputs/geojson_educacion/score_educacion_por_comuna_2026.geojson`
