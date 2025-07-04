"""
Terraform Plan Formatter Module

This module handles formatting and displaying Terraform plan summaries
in various output formats.
"""

import json
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from tabulate import tabulate

from parser import PlanSummary, ResourceChange, ChangeAction, ImpactLevel


class PlanFormatter:
    """Formatter class for Terraform plan summaries."""
    
    def __init__(self, use_color: bool = True):
        self.console = Console(color_system="auto" if use_color else None)
        self.use_color = use_color
    
    def format_summary(self, summary: PlanSummary, detailed: bool = False) -> str:
        """
        Format the plan summary for display.
        
        Args:
            summary: PlanSummary object to format
            detailed: Whether to show detailed information
            
        Returns:
            Formatted string representation
        """
        if detailed:
            return self._format_detailed_summary(summary)
        else:
            return self._format_basic_summary(summary)
    
    def _format_basic_summary(self, summary: PlanSummary) -> str:
        """Format a basic summary view."""
        output = []
        
        # Header
        output.append("📋 Terraform Plan Summary")
        output.append("=" * 40)
        output.append("")
        
        # Overview
        output.append("🔍 Overview:")
        output.append(f"  • Total Resources: {summary.total_resources}")
        output.append(f"  • To Create: {summary.resources_to_create}")
        output.append(f"  • To Update: {summary.resources_to_update}")
        output.append(f"  • To Delete: {summary.resources_to_delete}")
        output.append(f"  • No Changes: {summary.resources_no_change}")
        output.append("")
        
        # Resource Breakdown
        if summary.resource_breakdown:
            output.append("📊 Resource Breakdown:")
            for resource_type, counts in summary.resource_breakdown.items():
                actions = []
                if counts['create'] > 0:
                    actions.append(f"{counts['create']} create")
                if counts['update'] > 0:
                    actions.append(f"{counts['update']} update")
                if counts['delete'] > 0:
                    actions.append(f"{counts['delete']} delete")
                if counts['no-op'] > 0:
                    actions.append(f"{counts['no-op']} no-op")
                
                action_str = ", ".join(actions) if actions else "no changes"
                output.append(f"  • {resource_type}: {counts['total']} resources ({action_str})")
            output.append("")
        
        # Impact Analysis
        output.append("⚠️  Potential Impact:")
        output.append(f"  • High Impact: {summary.impact_analysis['high']} resources (deletions/replacements)")
        output.append(f"  • Medium Impact: {summary.impact_analysis['medium']} resources (updates)")
        output.append(f"  • Low Impact: {summary.impact_analysis['low']} resources (creations)")
        
        return "\n".join(output)
    
    def _format_detailed_summary(self, summary: PlanSummary) -> str:
        """Format a detailed summary view."""
        output = []
        
        # Basic summary first
        output.append(self._format_basic_summary(summary))
        output.append("")
        output.append("=" * 60)
        output.append("")
        
        # Detailed resource changes
        output.append("🔍 Detailed Resource Changes:")
        output.append("")
        
        # Group changes by action
        changes_by_action = {
            ChangeAction.CREATE: [],
            ChangeAction.UPDATE: [],
            ChangeAction.DELETE: [],
            ChangeAction.NO_OP: []
        }
        
        for change in summary.changes:
            changes_by_action[change.action].append(change)
        
        # Display each action type
        for action, changes in changes_by_action.items():
            if changes:
                action_emoji = {
                    ChangeAction.CREATE: "🟢",
                    ChangeAction.UPDATE: "🟡", 
                    ChangeAction.DELETE: "🔴",
                    ChangeAction.NO_OP: "⚪"
                }.get(action, "❓")
                
                output.append(f"{action_emoji} {action.value.upper()} ({len(changes)} resources):")
                for change in changes:
                    impact_emoji = {
                        ImpactLevel.HIGH: "🔴",
                        ImpactLevel.MEDIUM: "🟡",
                        ImpactLevel.LOW: "🟢"
                    }.get(change.impact_level, "⚪")
                    
                    output.append(f"  {impact_emoji} {change.address}")
                output.append("")
        
        return "\n".join(output)
    
    def format_json(self, summary: PlanSummary) -> str:
        """Format the summary as JSON."""
        # Convert summary to dictionary
        summary_dict = {
            "overview": {
                "total_resources": summary.total_resources,
                "resources_to_create": summary.resources_to_create,
                "resources_to_update": summary.resources_to_update,
                "resources_to_delete": summary.resources_to_delete,
                "resources_no_change": summary.resources_no_change
            },
            "resource_breakdown": summary.resource_breakdown,
            "impact_analysis": summary.impact_analysis,
            "changes": [
                {
                    "address": change.address,
                    "resource_type": change.resource_type,
                    "resource_name": change.resource_name,
                    "action": change.action.value,
                    "impact_level": change.impact_level.value
                }
                for change in summary.changes
            ]
        }
        
        return json.dumps(summary_dict, indent=2)
    
    def format_table(self, summary: PlanSummary) -> str:
        """Format the summary as a table."""
        # Create overview table
        overview_data = [
            ["Total Resources", summary.total_resources],
            ["To Create", summary.resources_to_create],
            ["To Update", summary.resources_to_update],
            ["To Delete", summary.resources_to_delete],
            ["No Changes", summary.resources_no_change]
        ]
        
        overview_table = tabulate(
            overview_data,
            headers=["Metric", "Count"],
            tablefmt="grid"
        )
        
        # Create resource breakdown table
        if summary.resource_breakdown:
            breakdown_data = []
            for resource_type, counts in summary.resource_breakdown.items():
                breakdown_data.append([
                    resource_type,
                    counts['total'],
                    counts['create'],
                    counts['update'],
                    counts['delete'],
                    counts['no-op']
                ])
            
            breakdown_table = tabulate(
                breakdown_data,
                headers=["Resource Type", "Total", "Create", "Update", "Delete", "No-op"],
                tablefmt="grid"
            )
        else:
            breakdown_table = "No resource changes found."
        
        # Create impact analysis table
        impact_data = [
            ["High Impact", summary.impact_analysis['high']],
            ["Medium Impact", summary.impact_analysis['medium']],
            ["Low Impact", summary.impact_analysis['low']]
        ]
        
        impact_table = tabulate(
            impact_data,
            headers=["Impact Level", "Count"],
            tablefmt="grid"
        )
        
        return f"""
Terraform Plan Summary
=====================

Overview:
{overview_table}

Resource Breakdown:
{breakdown_table}

Impact Analysis:
{impact_table}
"""
    
    def format_rich(self, summary: PlanSummary, detailed: bool = False) -> None:
        """Format and display using Rich library for enhanced terminal output."""
        # Create main panel
        title = Text("Terraform Plan Summary", style="bold blue")
        
        # Overview table
        overview_table = Table(title="Overview", box=box.ROUNDED)
        overview_table.add_column("Metric", style="cyan")
        overview_table.add_column("Count", style="magenta", justify="right")
        
        overview_table.add_row("Total Resources", str(summary.total_resources))
        overview_table.add_row("To Create", str(summary.resources_to_create))
        overview_table.add_row("To Update", str(summary.resources_to_update))
        overview_table.add_row("To Delete", str(summary.resources_to_delete))
        overview_table.add_row("No Changes", str(summary.resources_no_change))
        
        # Resource breakdown table
        breakdown_table = Table(title="Resource Breakdown", box=box.ROUNDED)
        breakdown_table.add_column("Resource Type", style="cyan")
        breakdown_table.add_column("Total", style="magenta", justify="right")
        breakdown_table.add_column("Create", style="green", justify="right")
        breakdown_table.add_column("Update", style="yellow", justify="right")
        breakdown_table.add_column("Delete", style="red", justify="right")
        breakdown_table.add_column("No-op", style="white", justify="right")
        
        for resource_type, counts in summary.resource_breakdown.items():
            breakdown_table.add_row(
                resource_type,
                str(counts['total']),
                str(counts['create']),
                str(counts['update']),
                str(counts['delete']),
                str(counts['no-op'])
            )
        
        # Impact analysis table
        impact_table = Table(title="Impact Analysis", box=box.ROUNDED)
        impact_table.add_column("Impact Level", style="cyan")
        impact_table.add_column("Count", style="magenta", justify="right")
        
        impact_table.add_row("High Impact", str(summary.impact_analysis['high']))
        impact_table.add_row("Medium Impact", str(summary.impact_analysis['medium']))
        impact_table.add_row("Low Impact", str(summary.impact_analysis['low']))
        
        # Display tables
        self.console.print(Panel(overview_table, title=title))
        self.console.print(breakdown_table)
        self.console.print(impact_table)
        
        if detailed:
            self._display_detailed_changes(summary)
    
    def _display_detailed_changes(self, summary: PlanSummary) -> None:
        """Display detailed changes using Rich."""
        # Group changes by action
        changes_by_action = {
            ChangeAction.CREATE: [],
            ChangeAction.UPDATE: [],
            ChangeAction.DELETE: [],
            ChangeAction.NO_OP: []
        }
        
        for change in summary.changes:
            changes_by_action[change.action].append(change)
        
        # Display each action type
        for action, changes in changes_by_action.items():
            if changes:
                action_colors = {
                    ChangeAction.CREATE: "green",
                    ChangeAction.UPDATE: "yellow",
                    ChangeAction.DELETE: "red",
                    ChangeAction.NO_OP: "white"
                }
                
                action_table = Table(
                    title=f"{action.value.upper()} ({len(changes)} resources)",
                    box=box.ROUNDED,
                    title_style=action_colors.get(action, "white")
                )
                action_table.add_column("Address", style="cyan")
                action_table.add_column("Resource Type", style="magenta")
                action_table.add_column("Impact", style="yellow")
                
                for change in changes:
                    impact_colors = {
                        ImpactLevel.HIGH: "red",
                        ImpactLevel.MEDIUM: "yellow",
                        ImpactLevel.LOW: "green"
                    }
                    
                    action_table.add_row(
                        change.address,
                        change.resource_type,
                        change.impact_level.value,
                        style=impact_colors.get(change.impact_level, "white")
                    )
                
                self.console.print(action_table)
    
    def format_natural_language(self, summary: PlanSummary, detailed: bool = False) -> str:
        """Format the summary in natural language."""
        output = []
        
        # Header
        output.append("What's Changing in Your Infrastructure")
        output.append("=" * 50)
        output.append("")
        
        # Overview in natural language
        output.append(self._generate_overview_narrative(summary))
        output.append("")
        
        # Resource breakdown in natural language
        if summary.resource_breakdown:
            output.append(self._generate_resource_breakdown_narrative(summary))
            output.append("")
        
        # Impact analysis in natural language
        output.append(self._generate_impact_narrative(summary))
        output.append("")
        
        # Detailed changes if requested
        if detailed:
            output.append(self._generate_detailed_changes_narrative(summary))
        
        return "\n".join(output)
    
    def _generate_overview_narrative(self, summary: PlanSummary) -> str:
        """Generate natural language overview of the plan."""
        total = summary.total_resources
        creates = summary.resources_to_create
        updates = summary.resources_to_update
        deletes = summary.resources_to_delete
        no_changes = summary.resources_no_change
        
        if total == 0:
            return "🎉 Great news! Everything looks good - no changes are needed. Your infrastructure is already exactly how it should be."
        
        narrative = []
        
        if creates > 0:
            if creates == 1:
                narrative.append("🎯 Terraform will be adding 1 new resource")
            else:
                narrative.append(f"🎯 Terraform will be adding {creates} new resources")
        
        if updates > 0:
            if updates == 1:
                narrative.append("🔧 Terraform will be modifying 1 existing resource")
            else:
                narrative.append(f"🔧 Terraform will be modifying {updates} existing resources")
        
        if deletes > 0:
            if deletes == 1:
                narrative.append("🔥 Terraform will be removing 1 resource")
            else:
                narrative.append(f"🔥 Terraform will be removing {deletes} resources")
        
        if no_changes > 0:
            if no_changes == 1:
                narrative.append("✅ 1 resource will stay exactly the same")
            else:
                narrative.append(f"✅ {no_changes} resources will stay exactly the same")
        
        # Join with appropriate conjunctions
        if len(narrative) == 1:
            return f"Here's what's happening: {narrative[0]}."
        elif len(narrative) == 2:
            return f"Here's what's happening: {narrative[0]} and {narrative[1]}."
        else:
            last_item = narrative.pop()
            return f"Here's what's happening: {', '.join(narrative)}, and {last_item}."
    
    def _generate_resource_breakdown_narrative(self, summary: PlanSummary) -> str:
        """Generate natural language breakdown of resources by type."""
        output = ["📊 Here's the breakdown by type:"]
        
        for resource_type, counts in summary.resource_breakdown.items():
            total = counts['total']
            actions = []
            
            if counts['create'] > 0:
                if counts['create'] == 1:
                    actions.append("🎯 adding 1")
                else:
                    actions.append(f"🎯 adding {counts['create']}")
            
            if counts['update'] > 0:
                if counts['update'] == 1:
                    actions.append("🔧 updating 1")
                else:
                    actions.append(f"🔧 updating {counts['update']}")
            
            if counts['delete'] > 0:
                if counts['delete'] == 1:
                    actions.append("🔥 removing 1")
                else:
                    actions.append(f"🔥 removing {counts['delete']}")
            
            if counts['no-op'] > 0:
                if counts['no-op'] == 1:
                    actions.append("✅ leaving 1 unchanged")
                else:
                    actions.append(f"✅ leaving {counts['no-op']} unchanged")
            
            action_str = ", ".join(actions) if actions else "no changes"
            
            if total == 1:
                output.append(f"  • {resource_type}: 1 total ({action_str})")
            else:
                output.append(f"  • {resource_type}: {total} total ({action_str})")
        
        return "\n".join(output)
    
    def _generate_impact_narrative(self, summary: PlanSummary) -> str:
        """Generate natural language impact analysis."""
        high = summary.impact_analysis['high']
        medium = summary.impact_analysis['medium']
        low = summary.impact_analysis['low']
        
        output = ["🎯 What this means for you:"]
        
        if high > 0:
            if high == 1:
                output.append("  • ⚠️ 1 resource will be completely replaced (this might cause a brief interruption)")
            else:
                output.append(f"  • ⚠️ {high} resources will be completely replaced (this might cause brief interruptions)")
        
        if medium > 0:
            if medium == 1:
                output.append("  • 🔄 1 resource will be modified (should be quick and smooth)")
            else:
                output.append(f"  • 🔄 {medium} resources will be modified (should be quick and smooth)")
        
        if low > 0:
            if low == 1:
                output.append("  • ✨ 1 new resource will be added (no impact on existing infrastructure)")
            else:
                output.append(f"  • ✨ {low} new resources will be added (no impact on existing infrastructure)")
        
        # Add friendly recommendations
        if high > 0:
            output.append("")
            output.append("💡 Quick heads up:")
            if high == 1:
                output.append("  • The resource being replaced might be briefly unavailable")
                output.append("  • If it has important data, you might want to back it up first")
            else:
                output.append(f"  • The {high} resources being replaced might be briefly unavailable")
                output.append("  • If any have important data, you might want to back them up first")
        
        return "\n".join(output)
    
    def _generate_detailed_changes_narrative(self, summary: PlanSummary) -> str:
        """Generate detailed natural language descriptions of each change."""
        output = ["📝 Here's exactly what's changing:"]
        output.append("=" * 30)
        output.append("")
        
        # Group changes by action
        changes_by_action = {
            ChangeAction.CREATE: [],
            ChangeAction.UPDATE: [],
            ChangeAction.DELETE: [],
            ChangeAction.NO_OP: []
        }
        
        for change in summary.changes:
            changes_by_action[change.action].append(change)
        
        # Describe each action type
        for action, changes in changes_by_action.items():
            if not changes:
                continue
            
            if action == ChangeAction.CREATE:
                output.append("🎯 Resources Terraform will be adding:")
                for change in changes:
                    output.append(f"  • {change.address}")
                    output.append(f"    This is a new {change.resource_type} - nothing to worry about!")
                    if change.changes:
                        output.append(f"    Configuration: {self._summarize_changes(change.changes)}")
            
            elif action == ChangeAction.UPDATE:
                output.append("🔧 Resources Terraform will be modifying:")
                for change in changes:
                    output.append(f"  • {change.address}")
                    output.append(f"    This {change.resource_type} will get some improvements.")
                    if change.before and change.after:
                        changes_summary = self._explain_changes(change.before, change.after)
                        if changes_summary:
                            output.append(f"    Reason: {changes_summary}")
            
            elif action == ChangeAction.DELETE:
                output.append("🔥 Resources Terraform will be removing:")
                for change in changes:
                    output.append(f"  • {change.address}")
                    output.append(f"    This {change.resource_type} will be gone for good.")
                    if change.before:
                        output.append(f"    Current state: {self._summarize_resource_state(change.before)}")
                    # Add reason for deletion
                    deletion_reason = self._explain_deletion(change)
                    if deletion_reason:
                        output.append(f"    Reason: {deletion_reason}")
            
            elif action == ChangeAction.NO_OP:
                output.append("✅ Resources staying the same:")
                for change in changes:
                    output.append(f"  • {change.address}")
                    output.append(f"    This {change.resource_type} is perfect as-is.")
            
            output.append("")
        
        return "\n".join(output)
    
    def _explain_changes(self, before: Dict[str, Any], after: Dict[str, Any]) -> str:
        """Explain why a resource is being changed based on before/after data."""
        if not before or not after:
            return "Configuration updated"
        
        # Find changed fields
        changed_fields = []
        for key in after:
            if key not in before or before[key] != after[key]:
                changed_fields.append(key)
        
        if not changed_fields:
            return "Configuration updated"
        
        # Provide human-readable explanations
        explanations = []
        for field in changed_fields[:3]:  # Limit to first 3 changes
            if field in ['name', 'tags', 'description']:
                explanations.append(f"{field} updated")
            elif field in ['size', 'capacity', 'count']:
                explanations.append(f"{field} changed")
            elif field in ['subnet_id', 'vpc_id', 'security_group_ids']:
                explanations.append(f"network configuration updated")
            else:
                explanations.append(f"{field} modified")
        
        if len(changed_fields) > 3:
            explanations.append(f"and {len(changed_fields) - 3} other changes")
        
        return ", ".join(explanations)
    
    def _summarize_changes(self, changes: Dict[str, Any]) -> str:
        """Summarize the configuration for new resources."""
        if not changes:
            return "Default configuration"
        
        # Extract key configuration details
        summary_parts = []
        if 'name' in changes:
            summary_parts.append(f"name: {changes['name']}")
        if 'tags' in changes:
            summary_parts.append("with tags")
        if 'subnet_id' in changes:
            summary_parts.append("network attached")
        
        if summary_parts:
            return ", ".join(summary_parts)
        return "Standard configuration"
    
    def _summarize_resource_state(self, state: Dict[str, Any]) -> str:
        """Summarize the current state of a resource being deleted."""
        if not state:
            return "Resource exists"
        
        summary_parts = []
        if 'name' in state:
            summary_parts.append(f"name: {state['name']}")
        if 'tags' in state:
            summary_parts.append("has tags")
        if 'subnet_id' in state:
            summary_parts.append("network attached")
        
        if summary_parts:
            return ", ".join(summary_parts)
        return "Resource exists"

    def _explain_deletion(self, change: ResourceChange) -> str:
        """Explain why a resource is being deleted."""
        # If this is a replacement, show which attributes are causing it
        if change.replace and len(change.replace) > 0:
            fields = ', '.join(change.replace)
            return f"Changing {fields} requires resource replacement"
        if not change.before:
            return "Resource no longer needed"
        
        # Check resource name for clues
        resource_name = change.resource_name.lower()
        if 'old' in resource_name:
            return "Legacy resource being replaced"
        elif 'temp' in resource_name or 'test' in resource_name:
            return "Temporary resource being cleaned up"
        elif 'backup' in resource_name:
            return "Backup resource being removed"
        elif 'staging' in resource_name:
            return "Staging resource being removed"
        
        # Check resource state for clues
        state = change.before
        if 'tags' in state and state.get('tags', {}).get('lifecycle') == 'temporary':
            return "Temporary resource being cleaned up"
        elif 'tags' in state and state.get('tags', {}).get('environment') == 'staging':
            return "Staging environment resource being removed"
        
        # Check if it's an orphaned resource
        if not state.get('tags') and not state.get('name'):
            return "Orphaned resource being cleaned up"
        
        return "Resource no longer needed in configuration" 