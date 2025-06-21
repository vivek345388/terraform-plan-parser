"""
Terraform Plan Parser Module

This module contains the core logic for parsing Terraform plan output
and analyzing the planned changes.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChangeAction(Enum):
    """Enumeration of possible Terraform change actions."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    NO_OP = "no-op"
    READ = "read"


class ImpactLevel(Enum):
    """Enumeration of impact levels for changes."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ResourceChange:
    """Data class representing a single resource change."""
    address: str
    resource_type: str
    resource_name: str
    action: ChangeAction
    impact_level: ImpactLevel
    changes: Dict[str, Any]
    before: Optional[Dict[str, Any]] = None
    after: Optional[Dict[str, Any]] = None


@dataclass
class PlanSummary:
    """Data class representing the overall plan summary."""
    total_resources: int
    resources_to_create: int
    resources_to_update: int
    resources_to_delete: int
    resources_no_change: int
    resource_breakdown: Dict[str, Dict[str, int]]
    impact_analysis: Dict[str, int]
    changes: List[ResourceChange]


class TerraformPlanParser:
    """Main parser class for Terraform plan output."""
    
    def __init__(self):
        self.plan_data: Optional[Dict[str, Any]] = None
        self.summary: Optional[PlanSummary] = None
    
    def parse_file(self, file_path: str) -> PlanSummary:
        """
        Parse a Terraform plan JSON file.
        
        Args:
            file_path: Path to the JSON plan file
            
        Returns:
            PlanSummary object containing parsed data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.plan_data = json.load(f)
            
            return self._analyze_plan()
        except FileNotFoundError:
            raise FileNotFoundError(f"Plan file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in plan file: {e}")
        except Exception as e:
            raise RuntimeError(f"Error parsing plan file: {e}")
    
    def parse_json(self, json_data: str) -> PlanSummary:
        """
        Parse Terraform plan JSON data from string.
        
        Args:
            json_data: JSON string containing plan data
            
        Returns:
            PlanSummary object containing parsed data
        """
        try:
            self.plan_data = json.loads(json_data)
            return self._analyze_plan()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")
        except Exception as e:
            raise RuntimeError(f"Error parsing JSON data: {e}")
    
    def _analyze_plan(self) -> PlanSummary:
        """Analyze the parsed plan data and create a summary."""
        if not self.plan_data:
            raise ValueError("No plan data to analyze")
        
        changes = self._extract_changes()
        summary = self._create_summary(changes)
        self.summary = summary
        return summary
    
    def _extract_changes(self) -> List[ResourceChange]:
        """Extract resource changes from the plan data."""
        changes = []
        
        # Navigate through the plan structure
        resource_changes = self.plan_data.get('resource_changes', [])
        
        for change in resource_changes:
            address = change.get('address', '')
            change_type = change.get('change', {})
            actions = change_type.get('actions', [])
            
            # Determine the primary action
            action = self._determine_action(actions)
            
            # Extract resource type and name from address
            resource_type, resource_name = self._parse_address(address)
            
            # Determine impact level
            impact_level = self._determine_impact_level(action, change_type)
            
            # Create ResourceChange object
            resource_change = ResourceChange(
                address=address,
                resource_type=resource_type,
                resource_name=resource_name,
                action=action,
                impact_level=impact_level,
                changes=change_type.get('after', {}),
                before=change_type.get('before'),
                after=change_type.get('after')
            )
            
            changes.append(resource_change)
        
        return changes
    
    def _determine_action(self, actions: List[str]) -> ChangeAction:
        """Determine the primary action from a list of actions."""
        if not actions:
            return ChangeAction.NO_OP
        
        # Terraform actions priority: delete > create > update > read
        if 'delete' in actions:
            return ChangeAction.DELETE
        elif 'create' in actions:
            return ChangeAction.CREATE
        elif 'update' in actions:
            return ChangeAction.UPDATE
        elif 'read' in actions:
            return ChangeAction.READ
        else:
            return ChangeAction.NO_OP
    
    def _parse_address(self, address: str) -> Tuple[str, str]:
        """Parse resource address to extract type and name."""
        parts = address.split('.')
        if len(parts) >= 2:
            resource_type = parts[0]
            resource_name = '.'.join(parts[1:])
            return resource_type, resource_name
        return address, address
    
    def _determine_impact_level(self, action: ChangeAction, change_type: Dict) -> ImpactLevel:
        """Determine the impact level of a change."""
        if action == ChangeAction.DELETE:
            return ImpactLevel.HIGH
        elif action == ChangeAction.UPDATE:
            # Check if it's a replacement
            if change_type.get('actions') and 'replace' in change_type.get('actions', []):
                return ImpactLevel.HIGH
            return ImpactLevel.MEDIUM
        elif action == ChangeAction.CREATE:
            return ImpactLevel.LOW
        else:
            return ImpactLevel.LOW
    
    def _create_summary(self, changes: List[ResourceChange]) -> PlanSummary:
        """Create a summary from the list of changes."""
        total_resources = len(changes)
        resources_to_create = len([c for c in changes if c.action == ChangeAction.CREATE])
        resources_to_update = len([c for c in changes if c.action == ChangeAction.UPDATE])
        resources_to_delete = len([c for c in changes if c.action == ChangeAction.DELETE])
        resources_no_change = len([c for c in changes if c.action == ChangeAction.NO_OP])
        
        # Create resource breakdown
        resource_breakdown = {}
        for change in changes:
            resource_type = change.resource_type
            if resource_type not in resource_breakdown:
                resource_breakdown[resource_type] = {
                    'total': 0,
                    'create': 0,
                    'update': 0,
                    'delete': 0,
                    'no-op': 0
                }
            
            resource_breakdown[resource_type]['total'] += 1
            resource_breakdown[resource_type][change.action.value] += 1
        
        # Create impact analysis
        impact_analysis = {
            'high': len([c for c in changes if c.impact_level == ImpactLevel.HIGH]),
            'medium': len([c for c in changes if c.impact_level == ImpactLevel.MEDIUM]),
            'low': len([c for c in changes if c.impact_level == ImpactLevel.LOW])
        }
        
        return PlanSummary(
            total_resources=total_resources,
            resources_to_create=resources_to_create,
            resources_to_update=resources_to_update,
            resources_to_delete=resources_to_delete,
            resources_no_change=resources_no_change,
            resource_breakdown=resource_breakdown,
            impact_analysis=impact_analysis,
            changes=changes
        )
    
    def get_changes_by_type(self, resource_type: str) -> List[ResourceChange]:
        """Get all changes for a specific resource type."""
        if not self.summary:
            raise ValueError("No plan has been parsed yet")
        
        return [change for change in self.summary.changes if change.resource_type == resource_type]
    
    def get_changes_by_action(self, action: ChangeAction) -> List[ResourceChange]:
        """Get all changes for a specific action."""
        if not self.summary:
            raise ValueError("No plan has been parsed yet")
        
        return [change for change in self.summary.changes if change.action == action]
    
    def get_changes_by_impact(self, impact_level: ImpactLevel) -> List[ResourceChange]:
        """Get all changes for a specific impact level."""
        if not self.summary:
            raise ValueError("No plan has been parsed yet")
        
        return [change for change in self.summary.changes if change.impact_level == impact_level] 