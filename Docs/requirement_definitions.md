# Requerimiento del sistema

**Sistema de matching automático contra un catálogo persistente**

---

## 1. Gestión del catálogo

### RF-01 – Carga inicial del catálogo

El sistema debe permitir cargar un archivo CSV de catálogo inicial.

* El archivo debe seguir una **plantilla estricta** de columnas y tipos.
* No se aceptan columnas extra ni faltantes.
* El catálogo se considera **estado interno del sistema**.

---

### RF-02 – Extensión del catálogo

El sistema debe permitir extender el catálogo existente mediante nuevos archivos CSV.

* Los nuevos registros se agregan al catálogo actual.
* El sistema debe **evitar duplicados**, utilizando reglas claras (por ejemplo, combinación de campos clave).
* La deduplicación se realiza usando Pandas.

---

### RF-03 – Validación del catálogo

El sistema debe validar el archivo de catálogo antes de procesarlo.

Validaciones mínimas:

* Estructura de columnas
* Tipos de datos
* Valores obligatorios
* Valores inválidos o nulos

Si falla la validación, el catálogo **no se modifica**.

---

### RF-04 – Persistencia del catálogo

El sistema debe persistir el catálogo validado en un archivo interno.

* El archivo persistido es la única fuente de verdad.
* En esta versión, la persistencia se realiza en CSV.
* El diseño debe permitir reemplazar esta persistencia por una base de datos en el futuro sin cambiar la lógica de negocio.

---

### RF-05 – Plantilla de catálogo

El sistema debe proporcionar al usuario una plantilla oficial del catálogo.

* La plantilla define columnas, tipos y ejemplos.
* Puede descargarse mediante un endpoint.

---

## 2. Gestión de requerimientos

### RF-06 – Carga de requerimientos en archivo

El sistema debe permitir cargar un archivo de requerimientos en CSV o Excel.

* El archivo debe seguir una **plantilla estricta**.
* No se aceptan formatos libres.
* Está pensado para procesamiento masivo.

---

### RF-07 – Validación de requerimientos

El sistema debe validar el archivo de requerimientos antes de procesarlo.

Validaciones mínimas:

* Estructura de columnas
* Tipos de datos
* Valores requeridos

Si falla la validación, el procesamiento se detiene.

---

### RF-08 – Plantilla de requerimientos

El sistema debe proporcionar una plantilla oficial de requerimientos.

* Define columnas, tipos y ejemplos.
* Disponible para descarga.

---

## 3. Matching automático

### RF-09 – Generación de matches

El sistema debe generar matches entre los requerimientos y el catálogo persistido.

* Para cada requerimiento:

  * Se deben devolver **hasta N matches** (N configurable, por defecto 5).
  * Si existen menos de N coincidencias, se devuelven las disponibles.
  * Si no hay coincidencias, se indica explícitamente.

---

### RF-10 – Uso de IA en el matching

La IA debe utilizarse exclusivamente para:

* Interpretar equivalencias semánticas
* Sugerir alternativas compatibles

Las reglas determinísticas (filtros, límites, validaciones) **son controladas por el código**, no por la IA.

---

### RF-11 – Justificación de resultados

Cada match o alternativa debe incluir una justificación clara y legible para humanos.

---

## 4. Requerimientos en lenguaje natural (flujo alternativo)

### RF-12 – Requerimientos rápidos en lenguaje natural

El sistema debe permitir ingresar requerimientos en lenguaje natural sin archivo.

* Pensado para pocos requerimientos.
* No reemplaza el flujo masivo por CSV.
* El sistema debe convertir el texto a una estructura equivalente a un requerimiento válido antes de procesarlo.

Este flujo reutiliza:

* la lógica de matching
* el catálogo persistido

Pero **no** la validación de archivos.
