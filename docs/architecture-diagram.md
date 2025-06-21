# 🏗️ Terraform Plan Parser - Visual Architecture

## 📊 System Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI[CLI Interface<br/>main.py]
        DEMO[Demo Script<br/>examples/demo.py]
    end
    
    subgraph "Core Processing Layer"
        PARSER[Core Parser<br/>parser.py]
        FORMATTER[Formatter Engine<br/>formatter.py]
    end
    
    subgraph "Data Models"
        PS[PlanSummary]
        RC[ResourceChange]
        CA[ChangeAction]
        IL[ImpactLevel]
    end
    
    subgraph "Input Sources"
        JSON[Plan JSON File]
        CONFIG[config.yaml]
        ARGS[CLI Arguments]
    end
    
    subgraph "Output Formats"
        TEXT[Text Format]
        NATURAL[Natural Language]
        NARRATIVE[Narrative Format]
        HUMAN[Human Format]
        JSON_OUT[JSON Format]
        TABLE[Table Format]
        RICH[Rich Format]
    end
    
    subgraph "Testing Layer"
        UT[Unit Tests]
        IT[Integration Tests]
        E2E[End-to-End Tests]
    end
    
    %% Input Flow
    JSON --> PARSER
    CONFIG --> PARSER
    ARGS --> CLI
    
    %% Processing Flow
    CLI --> PARSER
    DEMO --> PARSER
    PARSER --> PS
    PARSER --> RC
    PARSER --> CA
    PARSER --> IL
    
    %% Output Flow
    PS --> FORMATTER
    RC --> FORMATTER
    FORMATTER --> TEXT
    FORMATTER --> NATURAL
    FORMATTER --> NARRATIVE
    FORMATTER --> HUMAN
    FORMATTER --> JSON_OUT
    FORMATTER --> TABLE
    FORMATTER --> RICH
    
    %% Testing
    PARSER --> UT
    FORMATTER --> UT
    CLI --> E2E
    
    %% Styling
    classDef inputClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef processClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef dataClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef outputClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef testClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    
    class JSON,CONFIG,ARGS inputClass
    class CLI,DEMO,PARSER,FORMATTER processClass
    class PS,RC,CA,IL dataClass
    class TEXT,NATURAL,NARRATIVE,HUMAN,JSON_OUT,TABLE,RICH outputClass
    class UT,IT,E2E testClass
```

## 🔄 Data Flow Diagram

```mermaid
flowchart LR
    subgraph "Input Phase"
        A[Terraform Plan JSON] --> B[JSON Parser]
        B --> C[Data Validation]
    end
    
    subgraph "Processing Phase"
        C --> D[Change Extraction]
        D --> E[Action Analysis]
        E --> F[Impact Assessment]
        F --> G[Summary Building]
    end
    
    subgraph "Output Phase"
        G --> H[Format Selection]
        H --> I[Text Formatter]
        H --> J[Natural Language]
        H --> K[JSON Formatter]
        H --> L[Table Formatter]
        H --> M[Rich Formatter]
    end
    
    subgraph "Results"
        I --> N[Formatted Output]
        J --> N
        K --> N
        L --> N
        M --> N
    end
    
    style A fill:#e1f5fe
    style N fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fff3e0
    style F fill:#fff3e0
    style G fill:#fff3e0
```

## 🧩 Component Interaction Diagram

```mermaid
sequenceDiagram
    participant User
    participant CLI as CLI Interface
    participant Parser as Core Parser
    participant Formatter as Formatter Engine
    participant Output as Output Formats
    
    User->>CLI: Execute command with args
    CLI->>Parser: Parse plan file
    Parser->>Parser: Extract changes
    Parser->>Parser: Analyze actions
    Parser->>Parser: Assess impact
    Parser->>Parser: Build summary
    Parser->>Formatter: Send PlanSummary
    Formatter->>Formatter: Select format strategy
    Formatter->>Output: Generate formatted output
    Output->>CLI: Return formatted string
    CLI->>User: Display results
```

## 📁 Project Structure Diagram

```mermaid
graph TD
    subgraph "terraform-plan-parser"
        subgraph "src/"
            MAIN[main.py]
            PARSER[parser.py]
            FORMATTER[formatter.py]
            INIT[__init__.py]
        end
        
        subgraph "tests/"
            TEST_PARSER[test_parser.py]
            TEST_FORMATTER[test_formatter.py]
            TEST_INIT[__init__.py]
        end
        
        subgraph "examples/"
            DEMO[demo.py]
            SAMPLE[sample_plan.json]
            SIMPLE[sample_plan_simple.json]
        end
        
        subgraph "docs/"
            ARCH[architecture.md]
            DIAGRAM[architecture-diagram.md]
        end
        
        subgraph "Root Files"
            README[README.md]
            REQUIREMENTS[requirements.txt]
            SETUP[setup.py]
            MAKEFILE[Makefile]
            INSTALL[install.py]
            CONFIG[config.yaml]
            LICENSE[LICENSE]
        end
    end
    
    MAIN --> PARSER
    MAIN --> FORMATTER
    DEMO --> PARSER
    DEMO --> FORMATTER
    TEST_PARSER --> PARSER
    TEST_FORMATTER --> FORMATTER
    
    classDef srcClass fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef testClass fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef exampleClass fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef docClass fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef rootClass fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class MAIN,PARSER,FORMATTER,INIT srcClass
    class TEST_PARSER,TEST_FORMATTER,TEST_INIT testClass
    class DEMO,SAMPLE,SIMPLE exampleClass
    class ARCH,DIAGRAM docClass
    class README,REQUIREMENTS,SETUP,MAKEFILE,INSTALL,CONFIG,LICENSE rootClass
```

## 🎯 Design Patterns Diagram

```mermaid
graph TB
    subgraph "Factory Pattern"
        F1[Format Factory]
        F2[Text Formatter]
        F3[Natural Formatter]
        F4[JSON Formatter]
        F5[Table Formatter]
        F6[Rich Formatter]
        
        F1 --> F2
        F1 --> F3
        F1 --> F4
        F1 --> F5
        F1 --> F6
    end
    
    subgraph "Strategy Pattern"
        S1[Format Strategy]
        S2[Text Strategy]
        S3[Natural Strategy]
        S4[JSON Strategy]
        
        S1 --> S2
        S1 --> S3
        S1 --> S4
    end
    
    subgraph "Builder Pattern"
        B1[Summary Builder]
        B2[Change Builder]
        B3[Impact Builder]
        
        B1 --> B2
        B1 --> B3
    end
    
    subgraph "Command Pattern"
        C1[CLI Commands]
        C2[Parse Command]
        C3[Generate Command]
        
        C1 --> C2
        C1 --> C3
    end
    
    classDef patternClass fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    class F1,F2,F3,F4,F5,F6,S1,S2,S3,S4,B1,B2,B3,C1,C2,C3 patternClass
```

## 🔒 Error Handling Flow

```mermaid
flowchart TD
    A[User Input] --> B{Input Valid?}
    B -->|No| C[Input Error]
    B -->|Yes| D[JSON Processing]
    D --> E{JSON Valid?}
    E -->|No| F[JSON Error]
    E -->|Yes| G[Data Processing]
    G --> H{Data Valid?}
    H -->|No| I[Data Error]
    H -->|Yes| J[Output Generation]
    J --> K{Output Success?}
    K -->|No| L[Output Error]
    K -->|Yes| M[Success]
    
    C --> N[User-Friendly Error]
    F --> N
    I --> N
    L --> N
    
    style A fill:#e8f5e8
    style M fill:#e8f5e8
    style C fill:#ffebee
    style F fill:#ffebee
    style I fill:#ffebee
    style L fill:#ffebee
    style N fill:#fff3e0
```

## 🚀 Performance Architecture

```mermaid
graph TB
    subgraph "Memory Management"
        M1[Streaming JSON Parser]
        M2[Lazy Loading]
        M3[Efficient Data Structures]
    end
    
    subgraph "Processing Optimization"
        P1[Optimized Algorithms]
        P2[Cached Calculations]
        P3[Parallel Processing]
    end
    
    subgraph "Scalability"
        S1[Modular Architecture]
        S2[Plugin System]
        S3[Configuration Driven]
    end
    
    M1 --> P1
    M2 --> P2
    M3 --> P3
    P1 --> S1
    P2 --> S2
    P3 --> S3
    
    classDef perfClass fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    class M1,M2,M3,P1,P2,P3,S1,S2,S3 perfClass
```

These diagrams provide a comprehensive visual representation of the Terraform Plan Parser architecture, making it easy to understand the system's structure, data flow, and design patterns. 🏗️ 