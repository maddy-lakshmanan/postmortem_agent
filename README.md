# Incident Postmortem Generator

## Architecture Comparison

### LangChain Implementation (Sequential)

```mermaid
graph TD
    A[Input Data] --> B[Generate Postmortem]
    B --> C[Extract Action Items]
    C --> D[Create Tracker]

    %% Second graph begins
    subgraph Action Items Flow
        S[Initial State] --> N1[Postmortem Node]
        N1 --> U[Updated State]
        U --> N2[Action Items Node]
        N2 --> U2[Updated State]
        U2 --> N3[Tracker Node]
        N3 --> F[Final Output]
    end
