# Incident Postmortem Generator

## Architecture Comparison

### LangChain Implementation
```mermaid
graph TD
    A[Input Data] --> B[Generate Postmortem]
    B --> C[Extract Action Items]
    C --> D[Create Tracker]

graph TD
    A[Input Data] --> B[State]
    B --> C[Generate Postmortem Node]
    C --> D[Extract Actions Node]
    D --> E[Create Tracker Node]
    E --> F[Final State]


---
### 4. Architecture Diagrams

**LangChain Flow** (Sequential):
```mermaid
graph LR
    A[Input] --> B[Postmortem]
    B --> C[Action Items]
    C --> D[Tracker]

graph TB
    S[State] --> N1[Postmortem Node]
    S --> N2[Action Items Node]
    S --> N3[Tracker Node]
    N1 --> U[Update State]
    N2 --> U
    N3 --> U
    U --> F[Final Output]