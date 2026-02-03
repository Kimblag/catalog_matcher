# CatalogMatcher

CatalogMatcher es un servicio backend que automatiza la comparación de requerimientos contra un catálogo persistente, combinando **reglas determinísticas** con interpretación semántica mediante IA.

El objetivo del sistema es reducir el trabajo manual necesario para analizar requerimientos técnicos o funcionales y encontrar coincidencias válidas dentro de un catálogo propio del sistema.

---

## Problema

En muchos procesos operativos, los equipos reciben requerimientos en formato libre o semi-estructurado que deben compararse manualmente contra un catálogo de opciones existentes.

Este proceso suele ser:

* Repetitivo
* Lento
* Propenso a errores
* Dependiente del criterio humano
* Difícil de escalar cuando el catálogo crece

CatalogMatcher busca automatizar este flujo, manteniendo el control de las reglas de negocio y utilizando IA únicamente **para generar embeddings y medir similitud semántica**.

---

## Alcance del sistema

El sistema permite:

* Cargar y mantener un catálogo persistente a partir de archivos CSV
* Validar estrictamente la estructura y los tipos de datos del catálogo
* Evitar duplicados al extender el catálogo
* Recibir requerimientos en formato CSV para procesamiento masivo
* Generar hasta N coincidencias por requerimiento (configurable)
* Proveer justificaciones claras para cada coincidencia
* Persistir embeddings y catálogos localmente usando FAISS

> Nota: La IA se usa solo para embeddings y búsqueda semántica; las reglas de negocio son determinísticas y controladas por código.

---

## Qué NO hace el sistema

* No expone interfaz gráfica
* No gestiona usuarios ni autenticación
* No aprende automáticamente con el uso
* No toma decisiones finales críticas

Estas decisiones son intencionales para mantener el alcance controlado y el sistema simple.

---

## Arquitectura

El proyecto sigue una **arquitectura limpia**, separando responsabilidades sin sobreingeniería.

```
app/
├─ api/               # Endpoints HTTP (FastAPI)
├─ application/       # Casos de uso, interfaces (ports)
├─ domain/            # Modelos y reglas de negocio
├─ infrastructure/    # Implementaciones externas (FAISS, OpenAI, CSV)
└─ data/              # Archivos persistentes (catálogo, embeddings)
```

---

## Stack tecnológico

* Python 3.13.7
* FastAPI
* Pydantic v2
* Pandas
* FAISS (vector store local)
* OpenAI API (solo embeddings)
* Pytest

---

## Uso de IA

La IA se utiliza exclusivamente para:

* Generar embeddings de texto para medir similitud semántica
* Detectar equivalencias entre requerimientos y catálogo

Todo lo demás (validaciones, reglas, límites) es **determinístico** y controlado por el código.

---

## Estado del proyecto

Este proyecto fue desarrollado como ejercicio técnico enfocado en:

* Automatización de procesos
* Diseño de sistemas backend
* Uso responsable de IA
* Claridad arquitectónica

---

## Posibles extensiones futuras

* Migrar de archivos CSV a una base de datos estructurada
* Versionado del catálogo
* Persistencia de ejecuciones y resultados
* Interfaz web
* Cache de resultados

Estas extensiones **no forman parte del alcance actual**.
