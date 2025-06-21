# 🏗️ Terraform Plan Parser - Architecture

This document describes the architecture of the Terraform Plan Parser project, including system components, data flow, and design decisions.

## 📊 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Terraform Plan Parser                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   CLI Interface │    │   Core Parser   │    │    Formatter Engine     │  │
│  │   (main.py)     │    │   (parser.py)   │    │    (formatter.py)       │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
│           │                       │                       │                  │
│           │                       │                       │                  │
│           ▼                       ▼                       ▼                  │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   Input Layer   │    │  Data Models    │    │   Output Formats        │  │
│  │ • JSON Files    │    │ • PlanSummary   │    │ • Text (Default)        │  │
│  │ • CLI Args      │    │ • ResourceChange│    │ • Natural Language      │  │
│  │ • Config Files  │    │ • Enums         │    │ • JSON                  │  │
│  └─────────────────┘    └─────────────────┘    │ • Table                 │  │
│                                                │ • Rich                  │  │
│                                                └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Terraform   │    │   Parser    │    │  Formatter  │    │   Output    │
│ Plan JSON   │───▶│   Engine    │───▶│   Engine    │───▶│   Formats   │
│             │    │             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Raw JSON    │    │ Structured  │    │ Formatted   │    │ Text/JSON/  │
│ Data        │    │ Data Models │    │ Strings     │    │ Natural     │
│             │    │             │    │             │    │ Language    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 🧩 Component Architecture

### 1. CLI Interface Layer (`main.py`)

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLI Interface                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Parse Command │  │ Generate Command│  │   Help System   │  │
│  │                 │  │                 │  │                 │  │
│  │ • File Input    │  │ • Terraform     │  │ • Usage Info    │  │
│  │ • Format Args   │  │   Integration   │  │ • Examples      │  │
│  │ • Output Args   │  │ • Auto-parsing  │  │ • Version Info  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Core Parser Layer (`parser.py`)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Core Parser                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  JSON Parser    │  │  Change Analyzer│  │  Impact Assessor│  │
│  │                 │  │                 │  │                 │  │
│  │ • File Reading  │  │ • Action Detect │  │ • Risk Analysis │  │
│  │ • JSON Validate │  │ • Resource Type │  │ • Priority Calc │  │
│  │ • Error Handle  │  │ • Address Parse │  │ • Recs Generate │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Data Models    │  │  Filter Engine  │  │  Summary Builder│  │
│  │                 │  │                 │  │                 │  │
│  │ • PlanSummary   │  │ • Type Filter   │  │ • Stats Calc    │  │
│  │ • ResourceChange│  │ • Action Filter │  │ • Breakdown Gen │  │
│  │ • Enums         │  │ • Impact Filter │  │ • Analysis Gen  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Formatter Engine (`formatter.py`)

```
┌─────────────────────────────────────────────────────────────────┐
│                      Formatter Engine                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Text Formatter │  │ Natural Language│  │  JSON Formatter │  │
│  │                 │  │   Generator     │  │                 │  │
│  │ • Emoji Output  │  │                 │  │ • Structured    │  │
│  │ • Structured    │  │ • Narrative Gen │  │   Output        │  │
│  │ • Color Support │  │ • Impact Desc   │  │ • API Ready     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ Table Formatter │  │  Rich Formatter │  │  Output Router  │  │
│  │                 │  │                 │  │                 │  │
│  │ • Tabulate Lib  │  │ • Rich Library  │  │ • Format Select │  │
│  │ • Grid Layout   │  │ • Color Output  │  │ • File Output   │  │
│  │ • CSV Ready     │  │ • Interactive   │  │ • Console Output│  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure Architecture

```
terraform-plan-parser/
├── 📁 src/                          # Core source code
│   ├── __init__.py                  # Package initialization
│   ├── main.py                      # CLI interface & entry point
│   ├── parser.py                    # Core parsing logic
│   └── formatter.py                 # Output formatting engine
│
├── 📁 tests/                        # Test suite
│   ├── __init__.py                  # Test package init
│   ├── test_parser.py               # Parser unit tests
│   └── test_formatter.py            # Formatter unit tests
│
├── 📁 examples/                     # Examples & demos
│   ├── demo.py                      # Interactive demo script
│   ├── sample_plan.json             # Sample Terraform plan
│   └── sample_plan_simple.json      # Simple test plan
│
├── 📁 docs/                         # Documentation
│   └── architecture.md              # This file
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 setup.py                      # Package configuration
├── 📄 README.md                     # Project documentation
├── 📄 Makefile                      # Build & development tasks
├── 📄 install.py                    # Installation script
├── 📄 config.yaml                   # Configuration file
└── 📄 LICENSE                       # MIT license
```

## 🔧 Data Model Architecture

### Core Data Models

```python
# Plan Summary - Top-level container
PlanSummary:
├── total_resources: int
├── resources_to_create: int
├── resources_to_update: int
├── resources_to_delete: int
├── resources_no_change: int
├── resource_breakdown: Dict[str, Dict[str, int]]
├── impact_analysis: Dict[str, int]
└── changes: List[ResourceChange]

# Individual Resource Change
ResourceChange:
├── address: str
├── resource_type: str
├── resource_name: str
├── action: ChangeAction (CREATE|UPDATE|DELETE|NO_OP|READ)
├── impact_level: ImpactLevel (LOW|MEDIUM|HIGH)
├── changes: Dict[str, Any]
├── before: Optional[Dict[str, Any]]
└── after: Optional[Dict[str, Any]]
```

## 🔄 Process Flow Architecture

### 1. Input Processing Flow

```
User Input
    │
    ▼
┌─────────────┐
│ CLI Parser  │ ← Click framework
└─────────────┘
    │
    ▼
┌─────────────┐
│ File Reader │ ← JSON validation
└─────────────┘
    │
    ▼
┌─────────────┐
│ JSON Parser │ ← Error handling
└─────────────┘
    │
    ▼
┌─────────────┐
│ Data Models │ ← Structured data
└─────────────┘
```

### 2. Analysis Flow

```
Structured Data
    │
    ▼
┌─────────────┐
│ Change      │ ← Extract resource changes
│ Extractor   │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Action      │ ← Determine primary action
│ Analyzer    │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Impact      │ ← Assess risk level
│ Assessor    │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Summary     │ ← Build comprehensive summary
│ Builder     │
└─────────────┘
```

### 3. Output Generation Flow

```
Plan Summary
    │
    ▼
┌─────────────┐
│ Format      │ ← Route to appropriate formatter
│ Router      │
└─────────────┘
    │
    ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Text        │  │ Natural     │  │ JSON        │
│ Formatter   │  │ Language    │  │ Formatter   │
└─────────────┘  └─────────────┘  └─────────────┘
    │              │              │
    ▼              ▼              ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Formatted   │  │ Narrative   │  │ Structured  │
│ Text        │  │ Output      │  │ JSON        │
└─────────────┘  └─────────────┘  └─────────────┘
```

## 🎯 Design Patterns Used

### 1. **Factory Pattern**
- Formatter selection based on output format type
- Dynamic formatter creation

### 2. **Strategy Pattern**
- Different formatting strategies for each output type
- Pluggable formatter implementations

### 3. **Builder Pattern**
- PlanSummary construction from raw data
- Step-by-step summary building

### 4. **Observer Pattern**
- CLI progress reporting
- Error handling and logging

### 5. **Command Pattern**
- CLI command structure with Click
- Subcommand organization

## 🔒 Error Handling Architecture

```
┌─────────────┐
│ User Input  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Input       │ ← File validation
│ Validation  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ JSON        │ ← JSON parsing errors
│ Processing  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Data        │ ← Data structure validation
│ Validation  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Output      │ ← Format-specific errors
│ Generation  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Error       │ ← User-friendly error messages
│ Reporting   │
└─────────────┘
```

## 🚀 Performance Considerations

### 1. **Memory Efficiency**
- Streaming JSON parsing for large plans
- Lazy loading of detailed information
- Efficient data structures

### 2. **Processing Speed**
- Optimized change detection algorithms
- Cached impact calculations
- Parallel processing for large datasets

### 3. **Scalability**
- Modular architecture for easy extension
- Plugin system for custom formatters
- Configuration-driven behavior

## 🔧 Configuration Architecture

```
┌─────────────┐
│ config.yaml │ ← User configuration
└─────────────┘
    │
    ▼
┌─────────────┐
│ Config      │ ← Configuration loader
│ Manager     │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Defaults    │ ← Default values
└─────────────┘
    │
    ▼
┌─────────────┐
│ Runtime     │ ← Runtime configuration
│ Config      │
└─────────────┘
```

## 🧪 Testing Architecture

```
┌─────────────┐
│ Unit Tests  │ ← Individual component tests
└─────────────┘
    │
    ▼
┌─────────────┐
│ Integration │ ← Component interaction tests
│ Tests       │
└─────────────┘
    │
    ▼
┌─────────────┐
│ End-to-End  │ ← Full workflow tests
│ Tests       │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Performance │ ← Performance benchmarks
│ Tests       │
└─────────────┘
```

This architecture provides a solid foundation for the Terraform Plan Parser, ensuring maintainability, extensibility, and reliability. 🏗️ 