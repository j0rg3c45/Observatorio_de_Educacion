# Contexto del Proyecto - Observatorio de Educacion

## Repositorio

- URL: https://github.com/j0rg3c45/Observatorio_de_Educacion.git
- Rama: main
- Equipo: ITT Cali Inteligente - Gobierno de Datos

## Objetivo del proyecto

Construir un Observatorio de Educacion territorial a partir de datos de la Secretaria
de Educacion Municipal (SED) de Cali, que permita medir y comparar las condiciones
del servicio educativo por sede, institucion y comuna, y hacer seguimiento en el tiempo
como insumo para el Indice de Transformacion Territorial (ITT).

## Relacion con el ITT

Este proyecto alimenta la **dimension de Educacion y Desarrollo** del ITT.
Los indicadores derivados son:
- Matricula escolar por zona de intervencion
- Tasa de desercion por zona
- Tasa de repitencia por zona
- Ratio estudiantes por docente por zona
- Cobertura educativa (bruta y neta)

## Indice propio: ICET

El proyecto construye el Indice de Calidad Educativa Territorial (ICET) con 5 dimensiones:
- Cobertura y Acceso (30%)
- Eficiencia Interna (25%)
- Recursos Pedagogicos (20%)
- Infraestructura (15%)
- Dotacion Tecnologica (10%)

## Datos disponibles

### Matricula 2026
- Archivo: `data/Fuentes de datos/Reporte de matricula/01_Matricula_2026.xlsx`
- Periodo: Corte 2026
- Hojas: Por sector, Por nivel, Por comuna, Por sexo, Comuna x sector x nivel x sexo, Notas tecnicas
- Datos clave: 304,291 estudiantes totales, 143,747 oficiales, 159,469 no oficiales
- Desglose por comuna: 22 comunas urbanas + 16 corregimientos
- Desglose por nivel: Prejardin, Transicion, Primaria, Secundaria, Media, Aceleracion, Adultos, PFC

### Indicadores de eficiencia y cobertura 2026
- Archivo: `data/Fuentes de datos/Indicadores de eficiencia y de cobertura/02_Indicadores_2026.xlsx`
- Periodo: Corte 2026
- Hojas: Repitencia por sector, Repitencia por nivel, Cobertura bruta, Cobertura neta, Notas tecnicas
- Datos clave: Tasa repitencia municipal 6.82%, Cobertura bruta 75.78%, Cobertura neta 68.87%
- Limitacion: Solo nivel municipal, NO desglose por comuna

### Estudiantes por docente y equipo 2026
- Archivo: `data/Fuentes de datos/Indicadores de docentes y equipos de computo/03_Estudiantes_por_docente_y_equipo_2026.xlsx`
- Periodo: Corte 2026
- Hojas: Resumen municipio, Detalle por sede (337 sedes), Nota tecnica
- Datos clave: 24.64 est/docente, 4.88 est/equipo, 5,835 docentes, 29,432 equipos
- Desglose: Por sede (cod_dane_sede, nombre, matricula, equipos, ratio)

### Informacion geografica de sedes
- Archivo: `data/Fuentes de datos/Informacion geografica sedes.xlsx`
- Contenido: 356 sedes con codigo DANE, nombre IE, sede, comuna/corregimiento (EEComCor), barrio, geometria
- Campo clave para cruce: EeCodDane (codigo DANE de sede), EEComCor (numero de comuna)
- CRS: MAGNA-SIRGAS (coordenadas proyectadas)

### Inventario de equipos de computo
- Archivo: `data/Fuentes de datos/REPORTE DE INVENTARIO DE EQUIPOS DE COMPUTO SEDES EDUCATIVAS.xlsx`
- Contenido: Inventario detallado de equipos por sede

### Intervenciones de infraestructura
- Archivos:
  - `data/Fuentes de datos/Intervenciones de infraestructura/22 SEDES.xlsx`
  - `data/Fuentes de datos/Intervenciones de infraestructura/49 sedes Emprestito - Valores 2026 y 2027.xlsx`
  - `data/Fuentes de datos/Intervenciones de infraestructura/HISTORICO OBRAS 2020-2025.xlsx`
- Contenido: Obras ejecutadas, inversiones programadas, historico

## Entorno de ejecucion

- Local: Windows, uv + conda disponibles
- Python: 3.12
- Dependencias: pandas, openpyxl, numpy, matplotlib, seaborn, geopandas, folium

## Reglas del agente

1. SIEMPRE analizamos los datos entregados: cantidad de nulos, vacios, repetidos y unicos.
2. No inventes datos.
3. Si un resultado no esta disponible, indicalo claramente.
4. Diferencia entre datos reales, datos provisionales y scores de referencia.
5. Despues de cada cambio realizado en el proyecto, SIEMPRE hacer commit y push:
   - git add .
   - git commit -m "descripcion breve del cambio"
   - git push
6. Cada cambio DEBE desencadenar la actualizacion de archivos .md y .txt relacionados.
7. Sin emojis en codigo.
8. Formato abreviado en ejes (1K, 1M, 1B).
9. Reportes en texto plano (.txt) en outputs/.
10. Ademas de tablas y reportes, SIEMPRE generar graficos sencillos y faciles de entender:
    - Barras horizontales para comparar cantidades entre categorias.
    - Tortas para distribuciones porcentuales simples.
    - Histogramas para distribuciones de variables numericas.
    - Heatmaps para matrices de calidad o correlacion.
    - Usar paleta Set2 de seaborn y estilo limpio (whitegrid).
    - Incluir etiquetas de valor en las barras para facilitar lectura.
