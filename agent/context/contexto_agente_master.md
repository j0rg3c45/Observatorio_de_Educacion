# Contexto Maestro para Agente

Este archivo resume el contexto mas importante del repo para que otro agente pueda trabajar con buen criterio metodologico y operativo desde el inicio.

## 1. Objetivo del proyecto

El repositorio construye el **Observatorio de Educacion** de Santiago de Cali, Colombia.

El proyecto mide y compara las condiciones del servicio educativo por sede, institucion educativa y comuna, usando datos de la Secretaria de Educacion Municipal (SED).

El indice propio del proyecto es el **ICET** (Indice de Calidad Educativa Territorial), que opera en escala `0-100` y alimenta la dimension de Educacion y Desarrollo del ITT general.

## 2. Regla metodologica principal

La metodologia vigente del proyecto exige:

- Usar `ref_min/ref_max` fijos por indicador.
- No usar min-max relativo calculado desde la propia muestra.
- Diferenciar entre datos reales y scores calculados.
- SIEMPRE analizar datos entregados: nulos, vacios, repetidos y unicos.

La fuente metodologica principal y prioritaria es:

- `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`

## 3. Dimensiones y pesos oficiales del ICET

El ICET usa 5 dimensiones:

- Cobertura y Acceso: `0.30`
- Eficiencia Interna: `0.25`
- Recursos Pedagogicos: `0.20`
- Infraestructura: `0.15`
- Dotacion Tecnologica: `0.10`

La suma de los pesos debe ser `1.0`.

## 4. Estado real de notebooks

### Notebook 01 - Carga y analisis de datos

- `notebooks/01_carga_y_analisis_datos.ipynb`

Estado:

- Creado y funcional.
- Carga las 8 fuentes de datos del Observatorio.
- Ejecuta analisis de calidad por cada fuente (nulos, vacios, duplicados, unicos, estadisticas).
- Genera graficos sencillos por cada fuente: barras de nulos, torta de tipos, histogramas de numericas.
- Genera visualizaciones consolidadas: registros por fuente, % nulos, duplicados, heatmap de calidad.
- Genera resumen consolidado de calidad en tabla.
- Detecta automaticamente si esta en Colab o local.

### Notebook 02 - Analisis por comuna, correlacion y viabilidad del ICET

- `notebooks/02_analisis_espacial_correlacion.ipynb`

Estado:

- Creado y funcional.
- Cruza matricula por comuna (22 comunas urbanas) con detalle por sede (337 sedes).
- Asigna comuna a cada sede usando info geografica (campo EEComCor).
- Agrega indicadores por comuna: sedes, matricula oficial, equipos, est/equipo.
- Genera graficos: barras de matricula, composicion sectorial, est/equipo, equipos, sedes.
- Calcula matriz de correlacion entre indicadores y genera heatmap.
- Genera scatter plots de relaciones clave.
- Evalua viabilidad del ICET por comuna.

Hallazgos clave del notebook 02:

- Matricula total urbana 2026: 304,291 estudiantes en 22 comunas.
- 337 sedes oficiales con datos de equipos de computo.
- Ratio promedio municipal: 4.88 estudiantes por equipo (meta cumplida a nivel agregado).
- Comunas con mayor matricula: C13, C14, C21, C15, C18.
- Comunas con mayor % no oficial: C22, C21, C2.

Viabilidad del ICET:

- 3 de 5 dimensiones son calculables hoy por comuna: Cobertura, Recursos, Dotacion.
- Eficiencia (repitencia/desercion) solo disponible a nivel municipal.
- Infraestructura requiere cruce adicional de obras con sedes.
- Recomendacion: calcular ICET parcial con 3 dimensiones y reponderar pesos.

## 5. Fuentes de datos disponibles

| Archivo | Dimension ICET | Estado |
|---------|---------------|--------|
| 01_Matricula_2026.xlsx | Cobertura y Acceso | Disponible |
| 02_Indicadores_2026.xlsx | Eficiencia Interna, Cobertura | Disponible |
| 03_Estudiantes_por_docente_y_equipo_2026.xlsx | Recursos Pedagogicos | Disponible |
| Informacion geografica sedes.xlsx | Georreferenciacion | Disponible |
| REPORTE DE INVENTARIO DE EQUIPOS DE COMPUTO.xlsx | Dotacion Tecnologica | Disponible |
| 22 SEDES.xlsx | Infraestructura | Disponible |
| 49 sedes Emprestito - Valores 2026 y 2027.xlsx | Infraestructura | Disponible |
| HISTORICO OBRAS 2020-2025.xlsx | Infraestructura | Disponible |

Todos los datos estan versionados en el repositorio dentro de `data/Fuentes de datos/`.

## 6. Unidades de analisis

| Nivel | Descripcion |
|-------|-------------|
| Sede | Unidad fisica individual (codigo DANE) |
| Institucion Educativa (IE) | Agrupacion de sedes |
| Comuna | Agregacion territorial |
| Municipal | Totalidad de Cali |

## 7. Donde vive el conocimiento

Para responder bien sobre este repo, un agente debe leer en este orden:

1. `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`
2. `agent/context/contexto_proyecto.md`
3. `agent/context/contexto_agente_master.md`
4. `agent/context/glosario.md`
5. `notebooks/01_carga_y_analisis_datos.ipynb`
6. `notebooks/02_analisis_espacial_correlacion.ipynb`

## 8. Precauciones para otro agente

- No inventar datos. Si un resultado no esta disponible, indicarlo.
- Distinguir siempre entre dato observado real y score normalizado.
- No asumir que `outputs/` ya contiene resultados.
- El notebook 01 esta creado pero pendiente de ejecucion en Colab.
- Tratar con cuidado textos con problemas de codificacion (tildes, caracteres especiales).

## 9. Reglas operativas obligatorias

1. Despues de cada cambio: `git add .` + `git commit` + `git push`
2. Cada cambio debe actualizar los archivos .md y .txt relacionados.
3. Repositorio: https://github.com/j0rg3c45/Observatorio_de_Educacion.git
4. Rama: main

## 10. Resumen ejecutivo para handoff rapido

Este repo construye el Observatorio de Educacion de Cali. La metodologia usa `ref_min/ref_max` fijos y esta documentada en `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`. El notebook 01 carga y analiza las 8 fuentes de datos de la SED. El notebook 02 cruza datos por comuna, calcula correlaciones y evalua la viabilidad del ICET. Hallazgo principal: 3 de 5 dimensiones del ICET son calculables hoy por comuna (Cobertura, Recursos, Dotacion). Eficiencia solo esta a nivel municipal y requiere desglose. Todas las fuentes estan en `data/Fuentes de datos/`. El indice ICET tiene 5 dimensiones: Cobertura (30%), Eficiencia (25%), Recursos (20%), Infraestructura (15%) y Dotacion (10%).

## 11. Prompt sugerido para otro agente

> Este repo construye el Observatorio de Educacion de Cali. La metodologia vigente exige `ref_min/ref_max` fijos por indicador y esta documentada en `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`. El notebook 01 carga y analiza 8 fuentes de datos de la SED. El notebook 02 cruza datos por comuna (22 comunas, 337 sedes), calcula correlaciones y evalua viabilidad del ICET. Hallazgo: 3 de 5 dimensiones son calculables hoy (Cobertura, Recursos, Dotacion). Eficiencia solo a nivel municipal. El ICET usa 5 dimensiones: Cobertura (30%), Eficiencia (25%), Recursos (20%), Infraestructura (15%), Dotacion (10%). Despues de cada cambio haz commit+push y actualiza los .md y .txt relacionados. No inventes datos ni outputs.
