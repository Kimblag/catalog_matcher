# Escenarios de tests - DeactivateCatalogItem

| Caso de test                              | Escenario                            | Setup (mocks)                          | Entrada        | Comportamiento esperado                | Resultado esperado                         |
| ---------------------------------------- | ------------------------------------ | -------------------------------------- | -------------- | -------------------------------------- | ------------------------------------------ |
| deactivate_item_happy_path                | Item existente y activo              | Repo retorna catálogo con item activo  | item_id válido | Desactiva el item y persiste catálogo  | save(catalog) llamado una vez               |
| deactivate_item_not_found                | Item inexistente                     | Repo retorna catálogo sin item         | item_id invál | Propaga error de dominio               | ItemNotFoundException                      |
| deactivate_item_calls_repo_get_once       | Obtención de catálogo                | Mock CatalogRepository                 | item_id válido | Obtiene catálogo una sola vez          | get() called once                          |
| deactivate_item_calls_repo_save_once      | Persistencia                         | Mock CatalogRepository                 | item_id válido | Persiste una sola vez                  | save() called once                         |
