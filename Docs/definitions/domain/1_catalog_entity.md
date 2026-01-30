# Catalog
Gestionar un catálogo consistente de ítems que representa la oferta disponible del sistema

## Propiedades
- items: Lista de CatalogItem
- version: int
- last_updated: datetime
- source: Enum("manual", "csv", "xlsx") u otros.

## Reglas generales
- Un duplicado se define como un ítem cuya fila de origen (por ejemplo CSV) es exactamente igual a otra ya existente.
- Los ítems internos no se exponen ni se modifican desde fuera de Catalog.
- Todo cambio de estado de un ítem es orquestado exclusivamente por Catalog.

## Comportamiento
- create_item(name, category, subcategory, description, attributes, unit, provider)
  * Crea nuevos items.
  * Evita duplicados (fila exactamente igual a otra existente).
  * Aplica reglas.
- deactivate_item(item_id)
  * no borrar, desactivar
  * contains(item_id)
  * consulta interna
- activate_item(item_id)
  * verificar que exista contains(item_id)
- update_item_attributes(item_id, attributes)
  * verifica existencia del item
  * delega la actualización al CatalogItem
  * no permite modificar identidad
- update_item_description(item_id, description)
  * verifica existencia del item
  * delega la actualización al CatalogItem

## Entidad interna
### CatalogItem
Entidad interna, no accesible ni manipulable directamente desde el exterior del Catalog.

#### Propiedades
- item_id: str-> ID del item.
- name: nombre del item.
- category: Categoría del item.
- subcategory (opcional): subcategoría del item.
- description: Descripción del item.
- attributes: diccionario de atributos del item.
- unit (opcional): unidad de medida
- provider (opcional): proveedor del item.
- active: estado que representa si hay disponibilidad o no.

#### Comportamiento
- validate: Se debe validar a sí mismo durante su creación y mutaciones internas.
  * item_id válido no vacío.
  * name no vacío
  * category no vacío
  * description no vacía
  * attributes debe ser un diccionario cuando exista.
- activate
  * activa el item si se encuentra inactivo.
- deactivate
  * desactiva el item si este se encuentra activo.
- update_attributes: actualizar el diccionario.
  * solo actualiza attributes
  * valida claves / tipos
  * no toca identidad
- update_description: cambiar descripción.
  * Cambia texto.
  * validación vacíos.
