# Escenarios de tests CatalogItem

| Método / Comportamiento | Escenario                    | Entrada                  | Salida esperada / Assert principal              | Notas                            |
| ----------------------- | ---------------------------- | ------------------------ | ----------------------------------------------- | -------------------------------- |
| `__init__`              | Crear item válido            | Todos los campos válidos | Item creado correctamente, `active=True`        |                                  |
| `__init__`              | Crear item con item_id vacío | `item_id=""`             | Lanza `InvalidCatalogItemException`             |                                  |
| `__init__`              | Crear item con name vacío    | `name=""`                | Lanza excepción                                 |                                  |
| `activate`              | Activar item inactivo        | item con `active=False`  | Devuelve un **nuevo item** con `active=True`    | Inmutable                        |
| `activate`              | Activar item ya activo       | item con `active=True`   | Devuelve item igual (no cambia)                 | Inmutable                        |
| `deactivate`            | Desactivar item activo       | item con `active=True`   | Nuevo item con `active=False`                   | Inmutable                        |
| `update_name`           | Cambiar nombre válido        | `"Nuevo Nombre"`         | Nuevo item con `name="Nuevo Nombre"`            | Inmutable                        |
| `update_name`           | Cambiar nombre a vacío       | `""`                     | Lanza `InvalidCatalogItemException`             | Inmutable                        |
| `update_attributes`     | Actualizar atributos         | `{"color":"rojo"}`       | Nuevo item con atributos actualizados           | Overwrite o merge según decisión |
| `update_description`    | Cambiar descripción válida   | `"Descripción nueva"`    | Nuevo item con `description` actualizado        |                                  |
| `update_category`       | Cambiar categoría válida     | `"Nuevo Cat"`            | Nuevo item con `category` actualizado           |                                  |
| `update_unit`           | Cambiar unidad válida        | `"ml"`                   | Nuevo item con `unit="ml"`                      |                                  |
| `update_provider`       | Cambiar proveedor válido     | `"Proveedor X"`          | Nuevo item con `provider="Proveedor X"`         |                                  |
| `update_subcategory`    | Cambiar subcategoría válida  | `"SubCat"`               | Nuevo item con `subcategory="SubCat"`           |                                  |
| Inmutabilidad general   | Llamar `update_*`            | Cualquier actualización  | Original no cambia, se devuelve un nuevo objeto | Fundamental                      |
