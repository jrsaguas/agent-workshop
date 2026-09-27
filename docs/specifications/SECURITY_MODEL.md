# Modelo de seguridad

## Principios
- Deny-by-default para operaciones sensibles.
- Permisos por recurso, no solo por categoría.
- Aprobación humana para acciones destructivas o irreversibles.
- Auditoría de cada tool call.
- Separación entre planificación y ejecución.
- Secretos fuera de AgentDefinition.

## PC
Permisos por rutas, comandos y capacidades.

## GitHub
Separar lectura, escritura, push, merge y acciones administrativas.

## Android
Separar lectura de pantalla, interacción, shell y operaciones destructivas.

## Ejecución
Cada ejecución debe producir un execution_id y un registro auditable.
