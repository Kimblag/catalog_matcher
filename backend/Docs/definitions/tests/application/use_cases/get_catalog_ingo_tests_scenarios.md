# Escenarios de tests - GetCatalogInfo

| Caso de test                                 | Escenario                  | Setup (mocks)                   | Entrada | Comportamiento esperado                     | Resultado esperado                          |
| ------------------------------------------- | -------------------------- | -------------------------------- | ------- | ------------------------------------------- | ------------------------------------------- |
| get_catalog_info_happy_path                  | Catálogo existente         | Repo retorna catálogo válido     | —       | Obtiene metadata del catálogo               | Tuple (last_updated, source, version)       |
| get_catalog_info_calls_repo_get_once         | Orquestación correcta      | Mock CatalogRepository           | —       | Llama a get una sola vez                    | get() called once                           |
| get_catalog_info_propagates_repo_exception   | Error en repositorio       | Repo.get lanza excepción         | —       | No captura la excepción                     | Excepción propagada                         |
