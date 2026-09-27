# Estado del proyecto

## Implementado
- [x] Estructura local y documentación base.
- [x] Repositorio GitHub y rama main sincronizada.
- [x] AgentDefinition + schema JSON.
- [x] Agent Registry filesystem-backed.
- [x] CLI inicial para listar agentes.
- [x] CI inicial con Python 3.11/3.12.
- [x] ModelDefinition + schema + Model Registry.
- [x] ToolDefinition + schema + Tool Registry.
- [x] MCPServerDefinition + schema + MCP Registry.
- [x] Ejemplos YAML para Ollama, Python, filesystem y GitHub MCP.
- [x] Pruebas automatizadas de los tres registros.
- [x] CLI para listar models/tools/mcp.

## Verificado
- [x] Suite local: 3 tests pasando.
- [x] Working tree inspeccionado antes de cambios.
- [x] main estaba sincronizada con origin/main antes de este bloque.

## Pendiente
- [ ] Permission Policy engine y validación deny-by-default.
- [ ] Model provider adapters y ejecución real de inferencia.
- [ ] Tool execution contract.
- [ ] MCP discovery/connection runtime.
- [ ] Runtime mínimo de ejecución de agentes.
- [ ] Human approval y audit log.
- [ ] Agent-as-tool y Agent Graph.
- [ ] GUI/Studio.

## Próximo bloque técnico
Conectar AgentDefinition con los registros mediante referencias estables (model, tools, mcp) y añadir el primer contrato de ejecución, manteniendo separadas capacidades, permisos y transporte MCP.
