"""
Tests for the Terraform Plan Formatter module
"""

import pytest
from unittest.mock import Mock

from src.formatter import PlanFormatter
from src.parser import PlanSummary, ResourceChange, ChangeAction, ImpactLevel


class TestPlanFormatter:
    """Test cases for PlanFormatter class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = PlanFormatter(use_color=False)
        
        # Create a sample summary for testing
        self.sample_changes = [
            ResourceChange(
                address="aws_instance.web",
                resource_type="aws_instance",
                resource_name="web",
                action=ChangeAction.CREATE,
                impact_level=ImpactLevel.LOW,
                changes={"instance_type": "t3.micro"},
                before=None,
                after={"instance_type": "t3.micro"}
            ),
            ResourceChange(
                address="aws_security_group.web_sg",
                resource_type="aws_security_group",
                resource_name="web_sg",
                action=ChangeAction.UPDATE,
                impact_level=ImpactLevel.MEDIUM,
                changes={"name": "web-sg"},
                before={"name": "old-sg"},
                after={"name": "web-sg"}
            ),
            ResourceChange(
                address="aws_instance.old",
                resource_type="aws_instance",
                resource_name="old",
                action=ChangeAction.DELETE,
                impact_level=ImpactLevel.HIGH,
                changes={},
                before={"instance_type": "t2.micro"},
                after=None
            )
        ]
        
        self.sample_summary = PlanSummary(
            total_resources=3,
            resources_to_create=1,
            resources_to_update=1,
            resources_to_delete=1,
            resources_no_change=0,
            resource_breakdown={
                "aws_instance": {
                    "total": 2,
                    "create": 1,
                    "update": 0,
                    "delete": 1,
                    "no-op": 0
                },
                "aws_security_group": {
                    "total": 1,
                    "create": 0,
                    "update": 1,
                    "delete": 0,
                    "no-op": 0
                }
            },
            impact_analysis={
                "high": 1,
                "medium": 1,
                "low": 1
            },
            changes=self.sample_changes
        )
    
    def test_format_summary_basic(self):
        """Test basic summary formatting."""
        output = self.formatter.format_summary(self.sample_summary, detailed=False)
        
        assert "Terraform Plan Summary" in output
        assert "Total Resources: 3" in output
        assert "To Create: 1" in output
        assert "To Update: 1" in output
        assert "To Delete: 1" in output
    
    def test_format_summary_detailed(self):
        """Test detailed summary formatting."""
        output = self.formatter.format_summary(self.sample_summary, detailed=True)
        
        assert "Terraform Plan Summary" in output
        assert "Detailed Resource Changes:" in output
        assert "aws_instance.web" in output
        assert "aws_security_group.web_sg" in output
        assert "aws_instance.old" in output
    
    def test_format_json(self):
        """Test JSON formatting."""
        output = self.formatter.format_json(self.sample_summary)
        
        # Should be valid JSON
        import json
        parsed = json.loads(output)
        
        assert "overview" in parsed
        assert "resource_breakdown" in parsed
        assert "impact_analysis" in parsed
        assert "changes" in parsed
        
        assert parsed["overview"]["total_resources"] == 3
        assert parsed["overview"]["resources_to_create"] == 1
        assert parsed["overview"]["resources_to_update"] == 1
        assert parsed["overview"]["resources_to_delete"] == 1
    
    def test_format_table(self):
        """Test table formatting."""
        output = self.formatter.format_table(self.sample_summary)
        
        assert "Terraform Plan Summary" in output
        assert "Overview:" in output
        assert "Resource Breakdown:" in output
        assert "Impact Analysis:" in output
        assert "Total Resources" in output
        assert "To Create" in output
        assert "To Update" in output
        assert "To Delete" in output
    
    def test_format_natural_language_basic(self):
        """Test natural language formatting (basic)."""
        output = self.formatter.format_natural_language(self.sample_summary, detailed=False)
        
        assert "Terraform Plan Summary" in output
        assert "In total," in output
        assert "1 new resource will be created" in output
        assert "1 existing resource will be modified" in output
        assert "1 resource will be destroyed" in output
        assert "Resource Changes by Type:" in output
        assert "Impact Assessment:" in output
    
    def test_format_natural_language_detailed(self):
        """Test natural language formatting (detailed)."""
        output = self.formatter.format_natural_language(self.sample_summary, detailed=True)
        
        assert "Terraform Plan Summary" in output
        assert "Detailed Changes:" in output
        assert "Resources to be Created:" in output
        assert "Resources to be Modified:" in output
        assert "Resources to be Destroyed:" in output
        assert "aws_instance.web" in output
        assert "aws_security_group.web_sg" in output
        assert "aws_instance.old" in output
    
    def test_natural_language_overview_narrative(self):
        """Test natural language overview generation."""
        narrative = self.formatter._generate_overview_narrative(self.sample_summary)
        
        assert "1 new resource will be created" in narrative
        assert "1 existing resource will be modified" in narrative
        assert "1 resource will be destroyed" in narrative
    
    def test_natural_language_overview_single_action(self):
        """Test natural language overview with single action type."""
        # Create summary with only creates
        create_only_summary = PlanSummary(
            total_resources=2,
            resources_to_create=2,
            resources_to_update=0,
            resources_to_delete=0,
            resources_no_change=0,
            resource_breakdown={},
            impact_analysis={"high": 0, "medium": 0, "low": 2},
            changes=[]
        )
        
        narrative = self.formatter._generate_overview_narrative(create_only_summary)
        assert "2 new resources will be created" in narrative
    
    def test_natural_language_overview_no_changes(self):
        """Test natural language overview with no changes."""
        no_changes_summary = PlanSummary(
            total_resources=0,
            resources_to_create=0,
            resources_to_update=0,
            resources_to_delete=0,
            resources_no_change=0,
            resource_breakdown={},
            impact_analysis={"high": 0, "medium": 0, "low": 0},
            changes=[]
        )
        
        narrative = self.formatter._generate_overview_narrative(no_changes_summary)
        assert "No changes are planned" in narrative
    
    def test_natural_language_resource_breakdown(self):
        """Test natural language resource breakdown."""
        breakdown = self.formatter._generate_resource_breakdown_narrative(self.sample_summary)
        
        assert "Resource Changes by Type:" in breakdown
        assert "aws_instance: 2 resources" in breakdown
        assert "aws_security_group: 1 resource" in breakdown
        assert "1 creation" in breakdown
        assert "1 update" in breakdown
        assert "1 deletion" in breakdown
    
    def test_natural_language_impact_narrative(self):
        """Test natural language impact analysis."""
        impact = self.formatter._generate_impact_narrative(self.sample_summary)
        
        assert "Impact Assessment:" in impact
        assert "High Impact: 1 resource will be destroyed or replaced" in impact
        assert "Medium Impact: 1 resource will be modified" in impact
        assert "Low Impact: 1 new resource will be created" in impact
        assert "⚠️  Recommendations:" in impact
        assert "Review the resource that will be destroyed" in impact
    
    def test_natural_language_impact_no_high_impact(self):
        """Test natural language impact analysis with no high impact."""
        no_high_impact_summary = PlanSummary(
            total_resources=2,
            resources_to_create=1,
            resources_to_update=1,
            resources_to_delete=0,
            resources_no_change=0,
            resource_breakdown={},
            impact_analysis={"high": 0, "medium": 1, "low": 1},
            changes=[]
        )
        
        impact = self.formatter._generate_impact_narrative(no_high_impact_summary)
        
        assert "Impact Assessment:" in impact
        assert "High Impact:" not in impact
        assert "⚠️  Recommendations:" not in impact
    
    def test_natural_language_detailed_changes(self):
        """Test natural language detailed changes."""
        detailed = self.formatter._generate_detailed_changes_narrative(self.sample_summary)
        
        assert "Detailed Changes:" in detailed
        assert "Resources to be Created:" in detailed
        assert "Resources to be Modified:" in detailed
        assert "Resources to be Destroyed:" in detailed
        assert "aws_instance.web" in detailed
        assert "aws_security_group.web_sg" in detailed
        assert "aws_instance.old" in detailed
    
    def test_formatter_with_color(self):
        """Test formatter with color enabled."""
        color_formatter = PlanFormatter(use_color=True)
        output = color_formatter.format_summary(self.sample_summary, detailed=False)
        
        assert "Terraform Plan Summary" in output
        assert "Total Resources: 3" in output
    
    def test_empty_summary(self):
        """Test formatting with empty summary."""
        empty_summary = PlanSummary(
            total_resources=0,
            resources_to_create=0,
            resources_to_update=0,
            resources_to_delete=0,
            resources_no_change=0,
            resource_breakdown={},
            impact_analysis={"high": 0, "medium": 0, "low": 0},
            changes=[]
        )
        
        # Test all formats with empty summary
        text_output = self.formatter.format_summary(empty_summary, detailed=False)
        json_output = self.formatter.format_json(empty_summary)
        table_output = self.formatter.format_table(empty_summary)
        natural_output = self.formatter.format_natural_language(empty_summary, detailed=False)
        
        assert "Total Resources: 0" in text_output
        assert "total_resources" in json_output
        assert "Total Resources" in table_output
        assert "No changes are planned" in natural_output 