# Agent - Notas del entorno

## Repositorio

- URL: https://github.com/j0rg3c45/Observatorio_de_Educacion.git
- Rama: main

## Herramientas disponibles en este PC

- **uv** — Gestor de paquetes y entornos Python (instalado y disponible en PATH)
- **Ambiente Conda** — Existe un ambiente conda configurado con todas las dependencias
- **Python 3.12** — Version instalada en el sistema

## Entorno de ejecucion

- Local: Windows, uv + conda disponibles, ejecutar directamente con `uv run` o `python`

## Dependencias instaladas

- pandas, openpyxl (lectura de datos)
- numpy (calculo numerico)
- matplotlib, seaborn (visualizacion)
- geopandas, folium (analisis geoespacial)
- scikit-learn (analisis estadistico)

## Convenciones del proyecto

- Sin emojis ni caracteres especiales en el codigo
- Formato abreviado en ejes de graficos (1K, 1M, 1B)
- Reportes de texto plano (.txt) en outputs/
- Exportacion de graficos (.png) en outputs/

## Git - Regla obligatoria

Despues de cualquier modificacion (crear, editar o eliminar archivos), ejecutar:

```bash
git add .
git commit -m "descripcion breve del cambio"
git push
```

- Repositorio: https://github.com/j0rg3c45/Observatorio_de_Educacion.git
- Rama: main
- No esperar a que el usuario lo pida. Hacerlo automaticamente.

## Actualizacion de contexto - Regla obligatoria

Cada cambio en el proyecto DEBE desencadenar la actualizacion de los archivos relacionados:

| Si cambias... | Actualiza tambien... |
|---------------|---------------------|
| Codigo (.py, .ipynb) | README.md, reportes en outputs/ |
| Datos o estructura de datos | agent/context/contexto_proyecto.md |
| Indicadores o metricas | outputs/, agent/knowledge_base/ |
| Metodologia | agent/knowledge_base/, agent/context/glosario.md |
| Dependencias o entorno | requirements.txt, agent/README.md |

Mantener SIEMPRE la coherencia entre codigo, documentacion y contexto del agente.
