# CatalogMatcher

CatalogMatcher es un servicio backend que automatiza la comparación de requerimientos contra un catálogo persistente, combinando reglas determinísticas con interpretación semántica mediante IA.

El objetivo del sistema es reducir el trabajo manual necesario para analizar requerimientos técnicos o funcionales y encontrar coincidencias válidas dentro de un catálogo propio del sistema.

---

## Problema

En muchos procesos operativos, los equipos reciben requerimientos en formato libre o semi-estructurado que deben compararse manualmente contra un catálogo de opciones existentes.

Este proceso suele ser:
- repetitivo
- lento
- propenso a errores
- dependiente del criterio humano
- difícil de escalar cuando el catálogo crece

CatalogMatcher busca automatizar este flujo, manteniendo el control de las reglas de negocio y utilizando IA únicamente como apoyo para la interpretación semántica.

---

## Alcance del sistema

El sistema permite:

- Cargar y mantener un catálogo persistente a partir de archivos CSV
- Validar estrictamente la estructura y los tipos de datos del catálogo
- Extender el catálogo evitando duplicados
- Recibir requerimientos en formato CSV/Excel para procesamiento masivo
- Recibir requerimientos en lenguaje natural para consultas rápidas
- Generar hasta N coincidencias por requerimiento (configurable)
- Proveer justificaciones claras para cada coincidencia
- Exportar los resultados en formato Excel

---

## Qué NO hace el sistema

- No utiliza base de datos (en esta versión)
- No expone interfaz gráfica
- No gestiona usuarios
- No aprende automáticamente con el uso
- No toma decisiones finales críticas

Estas decisiones son intencionales para mantener el alcance controlado y el sistema simple.

---

## Arquitectura

El proyecto sigue una arquitectura limpia liviana, separando responsabilidades sin introducir sobreingeniería.

```

app/
├─ api/               # Endpoints HTTP
├─ application/       # Casos de uso y servicios
├─ domain/            # Modelos y reglas del dominio
├─ infrastructure/    # Detalles externos (OpenAI, CSV, Excel)
└─ data/              # Catálogo persistido

```

---

## Stack tecnológico

- Python 3.13.7
- FastAPI
- Pydantic v2
- Pandas
- OpenAI API
- Pytest (tests mínimos)
- Exportación a Excel

---

## Uso de IA

La IA se utiliza exclusivamente para:

- Interpretar requerimientos en lenguaje natural
- Detectar equivalencias semánticas
- Proponer alternativas compatibles

Las validaciones, reglas y límites del sistema son controlados por código determinístico.

---

## Estado del proyecto

Este proyecto fue desarrollado como ejercicio técnico enfocado en:
- automatización de procesos
- diseño de sistemas backend
- uso responsable de IA
- claridad arquitectónica

---

## Posibles extensiones futuras

- Reemplazo del CSV por una base de datos
- Versionado del catálogo
- Persistencia de ejecuciones
- Interfaz web
- Cache de resultados

Estas extensiones no forman parte del alcance actual.