"""
Genera el GeoJSON con scores de la dimension Educacion por comuna.
Ejecutar en Colab o local para obtener el archivo descargable.

Uso:
    uv run scripts/generar_geojson_educacion.py
"""
import os
import sys
import zipfile
import pandas as pd
import numpy as np
import geopandas as gpd

# ============================================================
# CONFIGURACION DE RUTAS
# ============================================================
IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    REPO_DIR = '/content/Observatorio_de_Educacion'
    if not os.path.exists(REPO_DIR):
        os.system('git clone https://github.com/j0rg3c45/Observatorio_de_Educacion.git ' + REPO_DIR)
    os.chdir(REPO_DIR)
    DATA_PATH = 'data/Fuentes de datos'
    OUTPUT_PATH = 'outputs'
else:
    # Detectar si se ejecuta desde scripts/ o desde raiz
    if os.path.basename(os.getcwd()) == 'scripts':
        DATA_PATH = '../data/Fuentes de datos'
        OUTPUT_PATH = '../outputs'
    else:
        DATA_PATH = 'data/Fuentes de datos'
        OUTPUT_PATH = 'outputs'

os.makedirs(OUTPUT_PATH, exist_ok=True)
print(f'Datos: {DATA_PATH}')
print(f'Output: {OUTPUT_PATH}')

# ============================================================
# REFERENCIAS FIJAS - DIMENSION EDUCACION
# ============================================================
REFS = {
    'matricula':      (5000, 30000, False),
    'repitencia':     (1.0,  15.0,  True),
    'est_por_docente':(15.0, 40.0,  True),
    'est_por_equipo': (1.0,  20.0,  True),
}


def score_ref(valor, ref_min, ref_max, inverso):
    """Normaliza un valor con umbrales fijos."""
    if ref_max == ref_min:
        return 100.0
    raw = np.clip((valor - ref_min) / (ref_max - ref_min) * 100, 0, 100)
    return 100 - raw if inverso else raw


def clasificar(score):
    if score < 40: return 'Nivel 1 - Critico'
    elif score < 60: return 'Nivel 2 - En desarrollo'
    elif score < 80: return 'Nivel 3 - Adecuado'
    else: return 'Nivel 4 - Optimo'


# ============================================================
# 1. CARGAR MATRICULA POR COMUNA
# ============================================================
print('\n[1/5] Cargando matricula por comuna...')
ruta_mat = os.path.join(DATA_PATH, 'Reporte de matr\u00edcula', '01_Matricula_2026.xlsx')
if not os.path.exists(ruta_mat):
    ruta_mat = os.path.join(DATA_PATH, 'Reporte de matricula', '01_Matricula_2026.xlsx')

df_comuna = pd.read_excel(ruta_mat, sheet_name='Por comuna')
df_cu = df_comuna[df_comuna['comuna'].str.contains('Comuna', na=False)].copy()
df_cu['num_comuna'] = df_cu['comuna'].str.extract(r'(\d+)').astype(int)
df_cu = df_cu.sort_values('num_comuna').reset_index(drop=True)
print(f'  Comunas: {len(df_cu)}, Matricula total: {df_cu["Total"].sum():,}')

# ============================================================
# 2. CARGAR DETALLE POR SEDE Y ASIGNAR COMUNA
# ============================================================
print('[2/5] Cargando sedes y asignando comuna...')
ruta_doc = os.path.join(DATA_PATH, 'Indicadores de docentes y equipos de computo',
                        '03_Estudiantes_por_docente_y_equipo_2026.xlsx')
df_sede = pd.read_excel(ruta_doc, sheet_name='Detalle por sede')

ruta_geo = os.path.join(DATA_PATH, 'Informaci\u00f3n geogr\u00e1fica sedes.xlsx')
if not os.path.exists(ruta_geo):
    ruta_geo = os.path.join(DATA_PATH, 'info_geografica',
                            'Informaci\u00f3n geogr\u00e1fica_sedes_Educativas.xlsx')
df_geo = pd.read_excel(ruta_geo)

df_geo_min = df_geo[['EeCodDane', 'EEComCor']].copy()
df_geo_min['EeCodDane'] = df_geo_min['EeCodDane'].astype(str).str.strip()
df_sede['cod_dane_sede'] = df_sede['cod_dane_sede'].astype(str).str.strip()

df_sc = df_sede.merge(df_geo_min, left_on='cod_dane_sede', right_on='EeCodDane', how='left')
df_sc = df_sc[df_sc['EEComCor'].between(1, 22)].copy()
df_sc['num_comuna'] = df_sc['EEComCor'].astype(int)

agg = df_sc.groupby('num_comuna').agg(
    matricula_oficial=('matricula', 'sum'),
    equipos_total=('equipos', 'sum'),
    est_equipo_prom=('estudiantes_por_equipo', 'mean'),
).reset_index()

print(f'  Sedes mapeadas: {len(df_sc)}')

# ============================================================
# 3. CALCULAR SCORES
# ============================================================
print('[3/5] Calculando scores...')
df_edu = df_cu[['num_comuna', 'comuna', 'Total']].merge(agg, on='num_comuna', how='left')
df_edu.rename(columns={'Total': 'matricula_total'}, inplace=True)
df_edu['repitencia'] = 6.82
df_edu['est_por_docente'] = 24.64

df_edu['score_matricula'] = df_edu['matricula_total'].apply(
    lambda v: score_ref(v, *REFS['matricula']))
df_edu['score_repitencia'] = df_edu['repitencia'].apply(
    lambda v: score_ref(v, *REFS['repitencia']))
df_edu['score_est_docente'] = df_edu['est_por_docente'].apply(
    lambda v: score_ref(v, *REFS['est_por_docente']))
df_edu['score_est_equipo'] = df_edu['est_equipo_prom'].apply(
    lambda v: score_ref(v, *REFS['est_por_equipo']))

df_edu['score_educacion'] = (
    df_edu['score_matricula'] + df_edu['score_repitencia'] +
    df_edu['score_est_docente'] + df_edu['score_est_equipo']
) / 4

df_edu['nivel'] = df_edu['score_educacion'].apply(clasificar)
print(f'  Score promedio: {df_edu["score_educacion"].mean():.1f}')

# ============================================================
# 4. CARGAR POLIGONOS DE COMUNAS
# ============================================================
print('[4/5] Cargando poligonos de comunas...')
ruta_comunas_zip = os.path.join(DATA_PATH, 'info_geografica', 'Comunas.zip')
carpeta_comunas = os.path.join(DATA_PATH, 'info_geografica', 'Comunas')

if not os.path.exists(carpeta_comunas):
    with zipfile.ZipFile(ruta_comunas_zip, 'r') as z:
        z.extractall(os.path.join(DATA_PATH, 'info_geografica'))
    print('  Comunas.zip descomprimido')

# Buscar shapefile o geojson
archivos_comunas = []
for root, dirs, files in os.walk(os.path.join(DATA_PATH, 'info_geografica')):
    for f in files:
        if 'omuna' in f.lower() and f.endswith(('.shp', '.geojson', '.json')):
            archivos_comunas.append(os.path.join(root, f))

gdf_comunas = gpd.read_file(archivos_comunas[0])
print(f'  Archivo: {archivos_comunas[0]}')
print(f'  Poligonos: {len(gdf_comunas)}, CRS: {gdf_comunas.crs}')

# Identificar columna de comuna
col_comuna = None
for col in gdf_comunas.columns:
    if col == 'geometry':
        continue
    if 'comuna' in col.lower() or 'com' in col.lower():
        col_comuna = col
        break

if col_comuna is None:
    for col in gdf_comunas.columns:
        if col == 'geometry':
            continue
        try:
            vals = pd.to_numeric(gdf_comunas[col], errors='coerce').dropna()
            if vals.between(1, 22).all() and len(vals) >= 20:
                col_comuna = col
                break
        except:
            pass

gdf_comunas['num_comuna'] = pd.to_numeric(gdf_comunas[col_comuna], errors='coerce').astype('Int64')
gdf_urb = gdf_comunas[gdf_comunas['num_comuna'].between(1, 22)].copy()

# Merge con scores
gdf_edu = gdf_urb.merge(
    df_edu[['num_comuna', 'comuna', 'matricula_total', 'matricula_oficial',
            'equipos_total', 'est_equipo_prom', 'repitencia', 'est_por_docente',
            'score_matricula', 'score_repitencia', 'score_est_docente',
            'score_est_equipo', 'score_educacion', 'nivel']],
    on='num_comuna', how='left'
)

# Reproyectar a WGS84
gdf_edu = gdf_edu.to_crs(epsg=4326)
print(f'  Comunas con score: {gdf_edu["score_educacion"].notna().sum()}')

# ============================================================
# 5. EXPORTAR GEOJSON
# ============================================================
print('[5/5] Exportando GeoJSON...')
geojson_dir = os.path.join(OUTPUT_PATH, 'geojson_educacion')
os.makedirs(geojson_dir, exist_ok=True)

# Seleccionar y limpiar columnas
cols_final = ['num_comuna', 'comuna', 'matricula_total', 'matricula_oficial',
              'equipos_total', 'est_equipo_prom', 'repitencia', 'est_por_docente',
              'score_matricula', 'score_repitencia', 'score_est_docente',
              'score_est_equipo', 'score_educacion', 'nivel', 'geometry']
cols_final = [c for c in cols_final if c in gdf_edu.columns]
gdf_final = gdf_edu[cols_final].copy()

# Redondear
for col in gdf_final.select_dtypes(include=[np.number]).columns:
    gdf_final[col] = gdf_final[col].round(2)

ruta_salida = os.path.join(geojson_dir, 'score_educacion_por_comuna_2026.geojson')
gdf_final.to_file(ruta_salida, driver='GeoJSON')

print(f'\n  Archivo generado: {ruta_salida}')
print(f'  Tamano: {os.path.getsize(ruta_salida) / 1024:.1f} KB')
print(f'  Comunas: {len(gdf_final)}')
print(f'  CRS: EPSG:4326 (WGS84)')

# Descargar en Colab
if IN_COLAB:
    from google.colab import files
    files.download(ruta_salida)
    print('\n  Descarga iniciada en Colab...')
else:
    print(f'\n  Ruta completa: {os.path.abspath(ruta_salida)}')

print('\nListo.')
