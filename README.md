# Terraform Plan Parser

This project takes a Terraform plan output file as input and provides a summary of the planned changes.
It helps in understanding what resources Terraform is planning to create, update, or delete.

## Features

- Parse Terraform plan output in JSON format
- Provide detailed summaries of planned changes
- Categorize changes by resource type and action
- Display resource counts and impact analysis
- Support for both human-readable and machine-readable output formats
- Color-coded output for better readability

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd terraform-plan-parser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Usage

### Basic Usage

```bash
# Parse a Terraform plan file
python -m src.main parse <plan.json> [OPTIONS]

# Parse with detailed output
python -m src.main parse <plan.json> --detailed

# Output to JSON format
python -m src.main parse <plan.json> --output-format json

# Output to natural language format
python -m src.main parse <plan.json> --output-format natural

# Output to narrative format (alternative to natural)
python -m src.main parse <plan.json> --output-format narrative

# Output to human-readable format (alternative to natural)
python -m src.main parse <plan.json> --output-format human

# Save output to file
python -m src.main parse <plan.json> --output-file summary.txt
```

### Short Aliases

For convenience, you can use these short aliases:

```bash
# Short aliases for output format
python -m src.main parse <plan.json> -f natural    # --output-format natural
python -m src.main parse <plan.json> -fmt json     # --output-format json

# Short aliases for other options
python -m src.main parse <plan.json> -d            # --detailed
python -m src.main parse <plan.json> -o summary.txt # --output-file summary.txt
```

### Generating Terraform Plan

To generate a Terraform plan file that can be parsed by this tool:

```bash
# Generate plan in JSON format
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
```

## Output Formats

The tool provides several output formats:

1. **Text Format**: Standard formatted output with emojis and structure
2. **Natural Language**: Human-readable descriptions of changes
3. **Narrative Format**: Story-like explanations of changes (same as natural)
4. **Human Format**: Human-readable format (same as natural)
5. **Detailed View**: Comprehensive breakdown of all resources
6. **JSON Output**: Machine-readable format for automation
7. **Table Format**: Tabular representation of changes
8. **Rich Format**: Enhanced terminal output with colors and formatting

### Example Output

#### Text Format
```
📋 Terraform Plan Summary
========================

🔍 Overview:
  • Total Resources: 15
  • To Create: 8
  • To Update: 4
  • To Delete: 3
  • No Changes: 0

📊 Resource Breakdown:
  • aws_instance: 5 resources (3 create, 2 update)
  • aws_security_group: 3 resources (2 create, 1 delete)
  • aws_subnet: 4 resources (2 create, 2 update)
  • aws_vpc: 1 resource (1 create)
  • aws_route_table: 2 resources (1 create, 1 delete)

⚠️  Potential Impact:
  • High Impact: 3 resources (deletions)
  • Medium Impact: 4 resources (updates)
  • Low Impact: 8 resources (creations)
```

#### Natural Language Format
```
Terraform Plan Summary
==================================================

In total, 8 new resources will be created, 4 existing resources will be modified, and 3 resources will be destroyed.

Resource Changes by Type:
  • aws_instance: 5 resources (3 creations, 2 updates)
  • aws_security_group: 3 resources (2 creations, 1 deletion)
  • aws_subnet: 4 resources (2 creations, 2 updates)
  • aws_vpc: 1 resource (1 creation)
  • aws_route_table: 2 resources (1 creation, 1 deletion)

Impact Assessment:
  • High Impact: 3 resources will be destroyed or replaced
  • Medium Impact: 4 resources will be modified
  • Low Impact: 8 new resources will be created

⚠️  Recommendations:
  • Review the 3 resources that will be destroyed to ensure no data loss
  • Consider backing up any important data before applying
```

## Configuration

Create a `config.yaml` file to customize the output:

```yaml
output:
  show_summary: true
  show_details: false
  color_output: true
  max_line_length: 80

filters:
  exclude_resource_types: []
  include_resource_types: []
  min_impact_level: "low"
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

## 🏗️ Architecture

For detailed information about the system architecture, design patterns, and component interactions, see:

- [Architecture Documentation](docs/architecture.md) - Comprehensive architecture overview
- [Visual Architecture Diagrams](docs/architecture-diagram.md) - Mermaid diagrams for visual understanding

The project follows a modular architecture with clear separation of concerns:
- **CLI Interface** (`main.py`) - Command-line interface and argument handling
- **Core Parser** (`parser.py`) - Terraform plan parsing and analysis
- **Formatter Engine** (`formatter.py`) - Multiple output format generation
- **Data Models** - Structured data representation
- **Testing Suite** - Comprehensive test coverage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.