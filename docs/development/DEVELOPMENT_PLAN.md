# Plan de desarrollo

## Estrategia
Desarrollo incremental por contratos. Cada componente debe tener schema, implementación, tests y documentación.

## Workstreams paralelos
A. Agent Definition + schemas.
B. Runtime/orchestration.
C. Tools + MCP adapters.
D. PC runtime.
E. Android runtime.
F. Memory/Memora adapter.
G. Git/GitHub integration.
H. GUI/Studio.
I. Evaluation/security.

## Regla de integración
Los workstreams se integran mediante interfaces versionadas. Ningún componente debe depender de detalles internos de otro workstream.

## Primera entrega funcional
Crear un agente local, asignarle un modelo Ollama, habilitar una tool, ejecutar una tarea, registrar trazas y guardar una versión reproducible.
