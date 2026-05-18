# Unidades de analisis - Observatorio de Educacion

## Nivel municipal

- Cobertura: Total Cali, 304,291 estudiantes (2026).
- Indicadores disponibles: Cobertura bruta (75.78%), neta (68.87%), repitencia (6.82%).
- Limitacion: Muchos indicadores solo estan a este nivel.

## Nivel comuna (22 comunas urbanas)

- Indicadores disponibles por comuna:
  - Matricula total, oficial, no oficial (fuente: 01_Matricula_2026, hoja Por comuna)
  - Sedes oficiales (cruce con info geografica)
  - Equipos de computo (agregacion de detalle por sede)
  - Estudiantes por equipo (agregacion de detalle por sede)
- Indicadores NO disponibles por comuna:
  - Cobertura bruta/neta (requiere poblacion DANE por comuna)
  - Repitencia/desercion (solo nivel municipal)
- Comunas con mayor matricula: C14 (25,902), C21 (23,489), C13 (22,107)
- Comunas con mayor % no oficial: C22 (99%), C21 (89%), C2 (75%)
- Comunas con mayor % oficial: C10 (83%), C16 (72%), C11 (69%)

## Nivel sede (337 sedes oficiales)

- Datos disponibles por sede:
  - Codigo DANE, nombre, matricula, equipos, estudiantes por equipo
  - Comuna asignada via info geografica (campo EEComCor)
- Rango de matricula por sede: 7 a 2,299 estudiantes
- Rango de equipos por sede: 2 a 695
- Rango est/equipo: 0.15 a 112.0 (mediana: 6.52)

## Corregimientos (16)

- Datos de matricula disponibles (solo sector oficial en la mayoria).
- No se incluyen en el analisis urbano del ICET.
- Pueden analizarse por separado con refs diferenciados (rural).

## Viabilidad del ICET por nivel

| Nivel | Dimensiones calculables | Viabilidad |
|-------|------------------------|------------|
| Municipal | 5 de 5 | Completa (pero sin comparacion interna) |
| Comuna | 3 de 5 | Parcial (Cobertura, Recursos, Dotacion) |
| Sede | 2 de 5 | Limitada (Recursos, Dotacion) |
