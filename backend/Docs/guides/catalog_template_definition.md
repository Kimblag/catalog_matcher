# Catalog template definition

| Columna         | Tipo lógico   | Obligatoria | Descripción                                           |
| --------------- | ------------- | ----------- | ----------------------------------------------------- |
| catalog_item_id | string        | Sí          | Identificador único interno del producto/servicio     |
| name            | string        | Sí          | Nombre corto del ítem                                 |
| category        | string        | Sí          | Categoría principal (ej: válvula, servicio, software) |
| subcategory     | string        | No          | Subcategoría más específica                           |
| description     | string        | Sí          | Descripción técnica clara                             |
| attributes      | string (JSON) | No          | Atributos clave estructurados                         |
| unit            | string        | No          | Unidad de medida (kg, mm, licencia, etc.)             |
| provider        | string        | No          | Proveedor o fabricante                                |
| active          | boolean       | Sí          | true / false                                          |
