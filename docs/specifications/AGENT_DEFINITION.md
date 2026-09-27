# Agent Definition

Un agente debe poder describirse sin depender de una interfaz gráfica.

Campos mínimos:
- id, name, version, description.
- model.
- instructions.
- capabilities.
- tools.
- mcp.
- skills.
- memory.
- permissions.
- runtime.
- subagents.
- evaluation.

## Distinciones
Capability = qué puede intentar hacer.
Permission = qué tiene autorizado hacer.
Tool = operación ejecutable.
Skill = conocimiento/procedimiento reutilizable.
Runtime = entorno que ejecuta la operación.
Model = componente que genera decisiones/respuestas.
