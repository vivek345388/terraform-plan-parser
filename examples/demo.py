#!/usr/bin/env python3
"""
Demo script for Terraform Plan Parser

This script demonstrates how to use the Terraform plan parser
to analyze and display plan summaries.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from parser import TerraformPlanParser, ChangeAction, ImpactLevel
from formatter import PlanFormatter


def main():
    """Main demonstration function."""
    print("🚀 Terraform Plan Parser Demo")
    print("=" * 40)
    
    # Path to the sample plan file
    sample_plan_path = Path(__file__).parent / "sample_plan.json"
    
    if not sample_plan_path.exists():
        print(f"❌ Sample plan file not found: {sample_plan_path}")
        return
    
    try:
        # Create parser and parse the plan
        print(f"📄 Parsing plan file: {sample_plan_path}")
        parser = TerraformPlanParser()
        summary = parser.parse_file(str(sample_plan_path))
        
        print("✅ Plan parsed successfully!")
        print()
        
        # Create formatter
        formatter = PlanFormatter(use_color=True)
        
        # Display different output formats
        print("📋 Basic Summary:")
        print("-" * 20)
        basic_output = formatter.format_summary(summary, detailed=False)
        print(basic_output)
        print()
        
        print("📊 Table Format:")
        print("-" * 20)
        table_output = formatter.format_table(summary)
        print(table_output)
        print()
        
        print("🔍 Detailed Summary:")
        print("-" * 20)
        detailed_output = formatter.format_summary(summary, detailed=True)
        print(detailed_output)
        print()
        
        print("📄 JSON Format (first 500 chars):")
        print("-" * 20)
        json_output = formatter.format_json(summary)
        print(json_output[:500] + "..." if len(json_output) > 500 else json_output)
        print()
        
        print("🗣️  Natural Language Format:")
        print("-" * 20)
        natural_output = formatter.format_natural_language(summary, detailed=False)
        print(natural_output)
        print()
        
        print("🗣️  Natural Language Format (Detailed):")
        print("-" * 20)
        natural_detailed_output = formatter.format_natural_language(summary, detailed=True)
        print(natural_detailed_output[:800] + "..." if len(natural_detailed_output) > 800 else natural_detailed_output)
        print()
        
        # Demonstrate filtering capabilities
        print("🎯 Filtering Examples:")
        print("-" * 20)
        
        # Filter by resource type
        aws_instances = parser.get_changes_by_type("aws_instance")
        print(f"• AWS Instances: {len(aws_instances)} resources")
        for change in aws_instances:
            print(f"  - {change.address} ({change.action.value})")
        
        # Filter by action
        create_changes = parser.get_changes_by_action(ChangeAction.CREATE)
        print(f"• Resources to create: {len(create_changes)}")
        
        delete_changes = parser.get_changes_by_action(ChangeAction.DELETE)
        print(f"• Resources to delete: {len(delete_changes)}")
        
        # Filter by impact
        high_impact = parser.get_changes_by_impact(ImpactLevel.HIGH)
        print(f"• High impact changes: {len(high_impact)}")
        
        print()
        print("🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 