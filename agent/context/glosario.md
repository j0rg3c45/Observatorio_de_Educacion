# Glosario - Observatorio de Educacion

## Terminos generales

| Termino | Definicion |
|---|---|
| ICET | Indice de Calidad Educativa Territorial (0-100) |
| ITT | Indice de Transformacion Territorial (indice padre) |
| SED | Secretaria de Educacion Municipal de Cali |
| MEN | Ministerio de Educacion Nacional |
| SIMAT | Sistema Integrado de Matricula (fuente de datos oficial) |
| DANE | Departamento Administrativo Nacional de Estadistica |
| IE | Institucion Educativa (agrupa varias sedes) |
| Sede | Unidad fisica donde se presta el servicio educativo |
| Codigo DANE | Identificador unico de cada sede educativa |
| EEComCor | Campo de info geografica que indica comuna o corregimiento |
| Matricula | Estudiantes matriculados en el sistema educativo (matricula = estudiantes matriculados) |

## Indicadores de linea base (por comuna)

| Indicador | Definicion | Fuente | Variacion por comuna |
|---|---|---|---|
| matricula_total | Total de estudiantes matriculados (oficial + no oficial) | 01_Matricula_2026 | SI |
| matricula_oficial | Estudiantes en sector oficial (publico) | 01_Matricula_2026 | SI |
| matricula_no_oficial | Estudiantes en sector no oficial (privado/contratado) | 01_Matricula_2026 | SI |
| pct_oficial | Porcentaje de matricula en sector oficial | Calculado | SI |
| sedes_oficiales | Cantidad de sedes educativas oficiales en la comuna | 03_Estudiantes_2026 + info geo | SI |
| instituciones_educativas | Cantidad de IE unicas en la comuna | Info geografica | SI |
| equipos_computo | Total de equipos de computo en sedes oficiales | 03_Estudiantes_2026 | SI |
| est_por_equipo | Promedio de estudiantes por equipo de computo | 03_Estudiantes_2026 (por sede) | SI |
| matricula_por_sede | Promedio de estudiantes por sede oficial | Calculado | SI |
| equipos_por_sede | Promedio de equipos por sede oficial | Calculado | SI |
| obras_2020_2025 | Obras de infraestructura ejecutadas (acumulado 6 anos) | HISTORICO OBRAS | SI |
| sedes_intervenidas | Sedes unicas que recibieron al menos 1 obra | HISTORICO OBRAS | SI |
| inversion_acumulada_M | Inversion total en infraestructura (millones COP) | HISTORICO OBRAS | SI |
| repitencia_pct | Tasa de repitencia (%) | 02_Indicadores_2026 | NO (constante 6.82%) |
| est_por_docente | Ratio estudiantes por docente | 03_Estudiantes_2026 | NO (constante 24.64) |
| cobertura_bruta_pct | Matricula total / Poblacion en edad escolar x 100 | 02_Indicadores_2026 | NO (constante 75.78%) |
| cobertura_neta_pct | Matricula en edad adecuada / Poblacion en edad escolar x 100 | 02_Indicadores_2026 | NO (constante 68.87%) |

## Indicadores derivados (scores)

| Indicador | Definicion | Formula |
|---|---|---|
| score_matricula | Score normalizado de matricula (0-100) | score_ref(matricula_total, 5000, 30000, positivo) |
| score_repitencia | Score normalizado de repitencia (0-100) | score_ref(6.82, 1.0, 15.0, inverso) |
| score_est_docente | Score normalizado de est/docente (0-100) | score_ref(24.64, 15.0, 40.0, inverso) |
| score_est_equipo | Score normalizado de est/equipo (0-100) | score_ref(est_por_equipo, 1.0, 20.0, inverso) |
| score_educacion | Score dimension Educacion (promedio de 4 scores) | (score_mat + score_rep + score_doc + score_eq) / 4 |
| score_obras | Score de obras acumuladas (0-100) | score_ref(obras_total, 1, 35, positivo) |
| score_inversion | Score de inversion acumulada (0-100) | score_ref(inversion_M, 100, 9000, positivo) |
| score_infraestructura | Score dimension Infraestructura (promedio) | (score_obras + score_inversion) / 2 |
| icet_parcial | ICET con 2 dimensiones (Educacion 75% + Infra 25%) | 0.75 * score_educacion + 0.25 * score_infraestructura |

## Metodologia

| Termino | Definicion |
|---|---|
| Score | Valor normalizado de 0 a 100 |
| ref_min | Umbral inferior de normalizacion (mejor resultado razonable) |
| ref_max | Umbral superior de normalizacion (peor resultado tolerable) |
| clamp | Funcion que acota un valor al rango [0, 100] |
| Indicador inverso | Indicador donde menor valor = mejor resultado (desercion, repitencia, est/equipo) |
| Indicador positivo | Indicador donde mayor valor = mejor resultado (matricula, obras) |
| Score parcial | Calculo del indice con indicadores disponibles (algunos constantes) |
| Constante municipal | Indicador sin desglose por comuna, mismo valor para todas |
| Linea base | Conjunto de indicadores con valores unicos por comuna al corte 2026 |
| Reponderacion | Ajuste de pesos para que sumen 100% cuando faltan dimensiones |

## Clasificacion del score

| Rango | Nivel | Descripcion |
|---|---|---|
| 0 - 40 | Nivel 1 - Critico | Condiciones deficientes |
| 40 - 60 | Nivel 2 - En desarrollo | Avances parciales |
| 60 - 80 | Nivel 3 - Adecuado | Condiciones aceptables |
| 80 - 100 | Nivel 4 - Optimo | Condiciones robustas |

## Terminos espaciales

| Termino | Definicion |
|---|---|
| Spatial join | Cruce espacial entre puntos y poligonos |
| CRS | Sistema de referencia de coordenadas |
| MAGNA-SIRGAS | Marco Geocentrico Nacional de Referencia de Colombia |
| EPSG:4326 | Sistema WGS84 (latitud/longitud) usado en mapas web |
| GeoJSON | Formato de archivo geoespacial basado en JSON |
| Coropletico | Mapa donde cada poligono se colorea segun un valor numerico |

## Fuentes de datos

| Termino | Definicion |
|---|---|
| SIMAT Anexo 6a | Reporte de matricula sector oficial (Marzo 2026) |
| SIMAT Anexo 5a | Reporte de matricula sector no oficial (Marzo 2026) |
| Sector oficial | Instituciones educativas publicas |
| Sector no oficial | Instituciones educativas privadas o contratadas |
| SGP Defensa | Sector de educacion militar |
| Emprestito | Credito publico para inversion en infraestructura educativa |
