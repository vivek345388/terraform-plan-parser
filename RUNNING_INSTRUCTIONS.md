# 🚀 Running Instructions for Terraform Plan Parser

This guide will help you get started with the Terraform Plan Parser project, including the new **Natural Language** output feature.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Terraform (optional, for generating plans)

## 🛠️ Installation

### Option 1: Quick Installation Script
```bash
python install.py
```

### Option 2: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Option 3: Using Makefile
```bash
# Install everything including development tools
make install-dev

# Or just install the package
make install
```

## 🎯 Quick Start

### 1. Run the Demo
```bash
python examples/demo.py
```
This will show you all the different output formats including the new natural language format.

### 2. Parse the Sample Plan
```bash
# Basic text output
python -m src.main parse examples/sample_plan.json

# Natural language output
python -m src.main parse examples/sample_plan.json --output-format natural

# Natural language with detailed information
python -m src.main parse examples/sample_plan.json --output-format natural --detailed

# Narrative format
python -m src.main parse examples/sample_plan.json --output-format narrative

# Human format
python -m src.main parse examples/sample_plan.json --output-format human
```

### Short Aliases

For convenience, you can use these short aliases:

```bash
# Short aliases for output format
python -m src.main parse examples/sample_plan.json -f natural    # --output-format natural
python -m src.main parse examples/sample_plan.json -fmt json     # --output-format json

# Short aliases for other options
python -m src.main parse examples/sample_plan.json -d            # --detailed
python -m src.main parse examples/sample_plan.json -o summary.txt # --output-file summary.txt
```

## 📊 Available Output Formats

The tool now supports **6 different output formats**:

### 1. Text Format (Default)
```bash
python -m src.main parse examples/sample_plan.json
```
- Standard formatted output with emojis and structure
- Good for quick overview

### 2. Natural Language Format ⭐ NEW!
```bash
python -m src.main parse examples/sample_plan.json --output-format natural
```
- Human-readable descriptions of changes
- Perfect for stakeholders and non-technical users
- Includes recommendations for high-impact changes

### 3. Narrative Format ⭐ NEW!
```bash
python -m src.main parse examples/sample_plan.json --output-format narrative
```
- Story-like explanations of changes (same as natural)
- Great for presentations and reports

### 4. Human Format ⭐ NEW!
```bash
python -m src.main parse examples/sample_plan.json --output-format human
```
- Human-readable format (same as natural)
- Clear and direct naming

### 5. JSON Format
```bash
python -m src.main parse examples/sample_plan.json --output-format json
```
- Machine-readable format
- Good for automation and scripting

### 6. Table Format
```bash
python -m src.main parse examples/sample_plan.json --output-format table
```
- Tabular representation
- Good for reports and documentation

### 7. Rich Format
```bash
python -m src.main parse examples/sample_plan.json --output-format rich
```
- Enhanced terminal output with colors
- Best for interactive use

### 8. Detailed View
```bash
python -m src.main parse examples/sample_plan.json --detailed
```
- Comprehensive breakdown of all resources
- Works with any output format

## 🎮 Using the Makefile

The Makefile provides convenient shortcuts:

```bash
# Show all available commands
make help

# Run examples with different formats
make run-example                    # Text format
make run-example-detailed           # Text format with details
make run-example-json               # JSON format
make run-example-table              # Table format
make run-example-natural            # Natural language format ⭐
make run-example-narrative          # Narrative format ⭐
make run-example-human              # Human format ⭐
make run-example-natural-detailed   # Natural language with details ⭐
make run-example-narrative-detailed # Narrative with details ⭐
make run-example-human-detailed     # Human format with details ⭐

# Development commands
make test                           # Run tests
make format                         # Format code
make lint                           # Lint code
make clean                          # Clean build artifacts
```

## 🗣️ Natural Language Output Examples

### Basic Natural Language Output
```
Terraform Plan Summary
==================================================

In total, 2 new resources will be created, 1 existing resource will be modified, and 1 resource will be destroyed.

Resource Changes by Type:
  • aws_instance: 2 resources (1 creation, 1 deletion)
  • aws_security_group: 1 resource (1 update)

Impact Assessment:
  • High Impact: 1 resource will be destroyed or replaced
  • Medium Impact: 1 resource will be modified
  • Low Impact: 2 new resources will be created

⚠️  Recommendations:
  • Review the resource that will be destroyed to ensure no data loss
  • Consider backing up any important data before applying
```

### Detailed Natural Language Output
```
Terraform Plan Summary
==================================================

In total, 2 new resources will be created, 1 existing resource will be modified, and 1 resource will be destroyed.

Resource Changes by Type:
  • aws_instance: 2 resources (1 creation, 1 deletion)
  • aws_security_group: 1 resource (1 update)

Impact Assessment:
  • High Impact: 1 resource will be destroyed or replaced
  • Medium Impact: 1 resource will be modified
  • Low Impact: 2 new resources will be created

⚠️  Recommendations:
  • Review the resource that will be destroyed to ensure no data loss
  • Consider backing up any important data before applying

Detailed Changes:
==============================

Resources to be Created:
  • aws_instance.web (aws_instance)
    This will create a new aws_instance resource.

Resources to be Modified:
  • aws_security_group.web_sg (aws_security_group)
    This will update the existing aws_security_group resource.

Resources to be Destroyed:
  • aws_instance.old (aws_instance)
    This will permanently delete the aws_instance resource.
```

## 🔧 Working with Your Own Terraform Plans

### 1. Generate a Terraform Plan
```bash
# In your Terraform directory
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
```

### 2. Parse Your Plan
```bash
# Parse with natural language output
python -m src.main parse plan.json --output-format natural

# Parse with detailed natural language
python -m src.main parse plan.json --output-format natural --detailed

# Save output to file
python -m src.main parse plan.json --output-format natural --output-file summary.txt
```

### 3. Generate and Parse Automatically
```bash
# Generate plan and parse it automatically
python -m src.main generate --auto-parse --output-format natural
```

## 🧪 Testing

### Run All Tests
```bash
make test
# or
python -m pytest tests/ -v
```

### Run Specific Test Files
```bash
# Test parser functionality
python -m pytest tests/test_parser.py -v

# Test formatter functionality (including natural language)
python -m pytest tests/test_formatter.py -v
```

## 📝 Configuration

You can customize the output by editing `config.yaml`:

```yaml
output:
  show_summary: true
  show_details: false
  color_output: true
  max_line_length: 80
  default_format: "natural"  # Set natural language as default

filters:
  exclude_resource_types: []
  include_resource_types: []
  min_impact_level: "low"
```

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Make sure you've installed the package with `pip install -e .`

2. **Missing dependencies**: Run `pip install -r requirements.txt`

3. **Python version**: Ensure you're using Python 3.8+

4. **Permission errors**: Use `python -m src.main` instead of direct script execution

### Getting Help
```bash
# Show CLI help
python -m src.main --help

# Show version
python -m src.main --version

# Show Makefile help
make help
```

## 🎉 What's New in This Version

- ✅ **Natural Language Output**: Human-readable descriptions of Terraform changes
- ✅ **Smart Recommendations**: Automatic suggestions for high-impact changes
- ✅ **Detailed Narratives**: Comprehensive explanations of each resource change
- ✅ **Enhanced Testing**: Complete test coverage for all output formats
- ✅ **Better Documentation**: Updated README and examples

The natural language output makes it much easier to:
- Explain changes to non-technical stakeholders
- Generate reports for management
- Understand the impact of changes quickly
- Get recommendations for safe deployments

Enjoy using the enhanced Terraform Plan Parser! 🚀 