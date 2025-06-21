"""
Terraform Plan Parser CLI

Main command-line interface for parsing and displaying Terraform plan summaries.
"""

import sys
import os
import click
from pathlib import Path
from typing import Optional

from .parser import TerraformPlanParser
from .formatter import PlanFormatter


@click.command()
@click.argument('plan_file', type=click.Path(exists=True, path_type=Path))
@click.option('--detailed', '-d', is_flag=True, help='Show detailed resource changes')
@click.option('--output-format', '-f', '-fmt',
              type=click.Choice(['text', 'json', 'table', 'rich', 'natural', 'narrative', 'human'], case_sensitive=False),
              default='text', help='Output format')
@click.option('--output-file', '-o', type=click.Path(path_type=Path), 
              help='Save output to file')
@click.option('--no-color', is_flag=True, help='Disable colored output')
@click.option('--version', is_flag=True, help='Show version information')
def main(plan_file: Path, detailed: bool, output_format: str, 
         output_file: Optional[Path], no_color: bool, version: bool):
    """
    Parse Terraform plan output and provide a summary of planned changes.
    
    PLAN_FILE: Path to the Terraform plan JSON file
    """
    if version:
        from . import __version__
        click.echo(f"Terraform Plan Parser v{__version__}")
        return
    
    try:
        # Parse the plan file
        parser = TerraformPlanParser()
        summary = parser.parse_file(str(plan_file))
        
        # Create formatter
        formatter = PlanFormatter(use_color=not no_color)
        
        # Generate output based on format
        if output_format == 'json':
            output = formatter.format_json(summary)
        elif output_format == 'table':
            output = formatter.format_table(summary)
        elif output_format == 'rich':
            # Rich format prints directly to console
            formatter.format_rich(summary, detailed=detailed)
            return
        elif output_format in ['natural', 'narrative', 'human']:
            output = formatter.format_natural_language(summary, detailed=detailed)
        else:  # text format
            output = formatter.format_summary(summary, detailed=detailed)
        
        # Output the result
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            click.echo(f"Output saved to {output_file}")
        else:
            click.echo(output)
            
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


@click.command()
@click.option('--terraform-dir', '-d', type=click.Path(exists=True, path_type=Path),
              default='.', help='Terraform working directory')
@click.option('--plan-file', '-p', type=click.Path(path_type=Path),
              default='plan.json', help='Output plan file name')
@click.option('--auto-parse', is_flag=True, help='Automatically parse the plan after generation')
@click.option('--detailed', is_flag=True, help='Show detailed output when auto-parsing')
def generate_plan(terraform_dir: Path, plan_file: Path, auto_parse: bool, detailed: bool):
    """
    Generate a Terraform plan and optionally parse it.
    """
    try:
        # Change to terraform directory
        original_dir = Path.cwd()
        os.chdir(terraform_dir)
        
        # Generate plan
        click.echo(f"Generating Terraform plan in {terraform_dir}...")
        
        # Run terraform plan
        import subprocess
        result = subprocess.run(['terraform', 'plan', '-out=plan.tfplan'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            click.echo(f"Error generating plan: {result.stderr}", err=True)
            sys.exit(1)
        
        # Convert to JSON
        click.echo("Converting plan to JSON...")
        result = subprocess.run(['terraform', 'show', '-json', 'plan.tfplan'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            click.echo(f"Error converting plan to JSON: {result.stderr}", err=True)
            sys.exit(1)
        
        # Save JSON plan
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        
        click.echo(f"Plan saved to {plan_file}")
        
        # Auto-parse if requested
        if auto_parse:
            click.echo("\nParsing plan...")
            parser = TerraformPlanParser()
            summary = parser.parse_file(str(plan_file))
            
            formatter = PlanFormatter()
            output = formatter.format_summary(summary, detailed=detailed)
            click.echo(output)
        
        # Clean up temporary plan file
        if (terraform_dir / 'plan.tfplan').exists():
            (terraform_dir / 'plan.tfplan').unlink()
        
        # Return to original directory
        os.chdir(original_dir)
        
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running Terraform command: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


@click.group()
def cli():
    """Terraform Plan Parser - Parse and summarize Terraform plan output."""
    pass


cli.add_command(main, name='parse')
cli.add_command(generate_plan, name='generate')


if __name__ == '__main__':
    cli() 