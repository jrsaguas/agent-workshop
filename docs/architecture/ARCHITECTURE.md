# Arquitectura

```
Agent Studio
    |
Agent Registry ---- Tool/MCP Registry
    |
Agent Runtime / Praxis
    |---- Model Providers
    |---- Memory / Memora
    |---- PC Runtime
    |---- Android Runtime
    |---- Web Runtime
    |
Execution -> Evaluation -> Experience -> Versioning
```

## Capas
1. Presentation: editor, graph, execution console.
2. Definition: schemas y configuración declarativa.
3. Orchestration: planificación, delegación y ciclo de ejecución.
4. Tooling: tools, MCP, APIs y agentes como tools.
5. Runtime: PC, Android, web y sandbox.
6. Memory: memoria de trabajo y persistente.
7. Governance: permisos, aprobación, auditoría y versionado.

## Regla arquitectónica
MCP es una extensión, no el núcleo completo. El runtime debe abstraer herramientas independientemente de su transporte.
