"""
Tests for the Terraform Plan Parser module
"""

import json
import pytest
from unittest.mock import Mock, patch

from src.parser import (
    TerraformPlanParser, 
    PlanSummary, 
    ResourceChange, 
    ChangeAction, 
    ImpactLevel
)


class TestTerraformPlanParser:
    """Test cases for TerraformPlanParser class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = TerraformPlanParser()
        
        # Sample plan data
        self.sample_plan = {
            "resource_changes": [
                {
                    "address": "aws_instance.web",
                    "change": {
                        "actions": ["create"],
                        "after": {"instance_type": "t3.micro"},
                        "before": None
                    }
                },
                {
                    "address": "aws_security_group.web_sg",
                    "change": {
                        "actions": ["update"],
                        "after": {"name": "web-sg"},
                        "before": {"name": "old-sg"}
                    }
                },
                {
                    "address": "aws_instance.old",
                    "change": {
                        "actions": ["delete"],
                        "after": None,
                        "before": {"instance_type": "t2.micro"}
                    }
                }
            ]
        }
    
    def test_parse_json(self):
        """Test parsing JSON data."""
        json_data = json.dumps(self.sample_plan)
        summary = self.parser.parse_json(json_data)
        
        assert isinstance(summary, PlanSummary)
        assert summary.total_resources == 3
        assert summary.resources_to_create == 1
        assert summary.resources_to_update == 1
        assert summary.resources_to_delete == 1
    
    def test_parse_file(self, tmp_path):
        """Test parsing from file."""
        plan_file = tmp_path / "plan.json"
        with open(plan_file, 'w') as f:
            json.dump(self.sample_plan, f)
        
        summary = self.parser.parse_file(str(plan_file))
        
        assert isinstance(summary, PlanSummary)
        assert summary.total_resources == 3
    
    def test_parse_file_not_found(self):
        """Test parsing non-existent file."""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_file("nonexistent.json")
    
    def test_parse_invalid_json(self):
        """Test parsing invalid JSON."""
        with pytest.raises(ValueError):
            self.parser.parse_json("invalid json")
    
    def test_determine_action(self):
        """Test action determination logic."""
        assert self.parser._determine_action(["delete"]) == ChangeAction.DELETE
        assert self.parser._determine_action(["create"]) == ChangeAction.CREATE
        assert self.parser._determine_action(["update"]) == ChangeAction.UPDATE
        assert self.parser._determine_action(["read"]) == ChangeAction.READ
        assert self.parser._determine_action([]) == ChangeAction.NO_OP
        
        # Test priority (delete > create > update)
        assert self.parser._determine_action(["create", "delete"]) == ChangeAction.DELETE
        assert self.parser._determine_action(["update", "create"]) == ChangeAction.CREATE
    
    def test_parse_address(self):
        """Test address parsing."""
        resource_type, resource_name = self.parser._parse_address("aws_instance.web")
        assert resource_type == "aws_instance"
        assert resource_name == "web"
        
        resource_type, resource_name = self.parser._parse_address("aws_subnet.private.0")
        assert resource_type == "aws_subnet"
        assert resource_name == "private.0"
        
        # Test invalid address
        resource_type, resource_name = self.parser._parse_address("invalid")
        assert resource_type == "invalid"
        assert resource_name == "invalid"
    
    def test_determine_impact_level(self):
        """Test impact level determination."""
        # Delete should be high impact
        change_type = {"actions": ["delete"]}
        impact = self.parser._determine_impact_level(ChangeAction.DELETE, change_type)
        assert impact == ImpactLevel.HIGH
        
        # Create should be low impact
        change_type = {"actions": ["create"]}
        impact = self.parser._determine_impact_level(ChangeAction.CREATE, change_type)
        assert impact == ImpactLevel.LOW
        
        # Update should be medium impact
        change_type = {"actions": ["update"]}
        impact = self.parser._determine_impact_level(ChangeAction.UPDATE, change_type)
        assert impact == ImpactLevel.MEDIUM
        
        # Update with replace should be high impact
        change_type = {"actions": ["update", "replace"]}
        impact = self.parser._determine_impact_level(ChangeAction.UPDATE, change_type)
        assert impact == ImpactLevel.HIGH
    
    def test_get_changes_by_type(self):
        """Test filtering changes by resource type."""
        self.parser.parse_json(json.dumps(self.sample_plan))
        
        aws_instance_changes = self.parser.get_changes_by_type("aws_instance")
        assert len(aws_instance_changes) == 2
        
        aws_security_group_changes = self.parser.get_changes_by_type("aws_security_group")
        assert len(aws_security_group_changes) == 1
    
    def test_get_changes_by_action(self):
        """Test filtering changes by action."""
        self.parser.parse_json(json.dumps(self.sample_plan))
        
        create_changes = self.parser.get_changes_by_action(ChangeAction.CREATE)
        assert len(create_changes) == 1
        assert create_changes[0].address == "aws_instance.web"
        
        delete_changes = self.parser.get_changes_by_action(ChangeAction.DELETE)
        assert len(delete_changes) == 1
        assert delete_changes[0].address == "aws_instance.old"
    
    def test_get_changes_by_impact(self):
        """Test filtering changes by impact level."""
        self.parser.parse_json(json.dumps(self.sample_plan))
        
        high_impact = self.parser.get_changes_by_impact(ImpactLevel.HIGH)
        assert len(high_impact) == 1  # Only delete action
        
        low_impact = self.parser.get_changes_by_impact(ImpactLevel.LOW)
        assert len(low_impact) == 1  # Only create action
        
        medium_impact = self.parser.get_changes_by_impact(ImpactLevel.MEDIUM)
        assert len(medium_impact) == 1  # Only update action
    
    def test_empty_plan(self):
        """Test parsing empty plan."""
        empty_plan = {"resource_changes": []}
        summary = self.parser.parse_json(json.dumps(empty_plan))
        
        assert summary.total_resources == 0
        assert summary.resources_to_create == 0
        assert summary.resources_to_update == 0
        assert summary.resources_to_delete == 0
    
    def test_no_changes_plan(self):
        """Test parsing plan with no-op changes."""
        no_change_plan = {
            "resource_changes": [
                {
                    "address": "aws_instance.existing",
                    "change": {
                        "actions": ["no-op"],
                        "after": {"instance_type": "t3.micro"},
                        "before": {"instance_type": "t3.micro"}
                    }
                }
            ]
        }
        
        summary = self.parser.parse_json(json.dumps(no_change_plan))
        assert summary.resources_no_change == 1
        assert summary.total_resources == 1


class TestPlanSummary:
    """Test cases for PlanSummary dataclass."""
    
    def test_plan_summary_creation(self):
        """Test creating a PlanSummary instance."""
        summary = PlanSummary(
            total_resources=5,
            resources_to_create=2,
            resources_to_update=2,
            resources_to_delete=1,
            resources_no_change=0,
            resource_breakdown={},
            impact_analysis={"high": 1, "medium": 2, "low": 2},
            changes=[]
        )
        
        assert summary.total_resources == 5
        assert summary.resources_to_create == 2
        assert summary.resources_to_update == 2
        assert summary.resources_to_delete == 1
        assert summary.resources_no_change == 0


class TestResourceChange:
    """Test cases for ResourceChange dataclass."""
    
    def test_resource_change_creation(self):
        """Test creating a ResourceChange instance."""
        change = ResourceChange(
            address="aws_instance.test",
            resource_type="aws_instance",
            resource_name="test",
            action=ChangeAction.CREATE,
            impact_level=ImpactLevel.LOW,
            changes={"instance_type": "t3.micro"},
            before=None,
            after={"instance_type": "t3.micro"}
        )
        
        assert change.address == "aws_instance.test"
        assert change.resource_type == "aws_instance"
        assert change.resource_name == "test"
        assert change.action == ChangeAction.CREATE
        assert change.impact_level == ImpactLevel.LOW 