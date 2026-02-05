# Requirements template

| Columna        | Tipo lógico   | Obligatoria | Descripción                        |
| -------------- | ------------- | ----------- | ---------------------------------- |
| requirement_id | string        | Sí          | Identificador del requerimiento    |
| description    | string        | Sí          | Necesidad expresada por el usuario |
| category       | string        | No          | Categoría esperada                 |
| constraints    | string (JSON) | No          | Restricciones técnicas             |
| quantity       | number        | No          | Cantidad requerida                 |
| unit           | string        | No          | Unidad esperada                    |
| priority       | integer       | No          | 1 (alta) – 5 (baja)                |
