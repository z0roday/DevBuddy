"""
Example plugin for DevBuddy.
Shows how to create custom commands.
"""

import click
import os
import platform
import subprocess
import sys

def get_system_info():
    """Get basic system information."""
    info = {
        "System": platform.system(),
        "Node": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Python": platform.python_version(),
    }
    return info

def register_commands(cli_group):
    """Register commands with the CLI."""
    
    @cli_group.command()
    def system_info():
        """Display system information."""
        info = get_system_info()
        
        click.echo("System Information:")
        click.echo("------------------")
        
        for key, value in info.items():
            click.echo(f"{key}: {value}")
            
    @cli_group.command()
    @click.argument('file_path', type=click.Path(exists=True))
    def count_lines(file_path):
        """Count lines in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            total_lines = len(lines)
            code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
            
            click.echo(f"File: {os.path.basename(file_path)}")
            click.echo(f"Total lines: {total_lines}")
            click.echo(f"Code lines: {code_lines}")
            click.echo(f"Comment/empty lines: {total_lines - code_lines}")
        except Exception as e:
            click.echo(f"Error reading file: {e}")

    # Return the commands if you want other plugins to extend them
    return {
        "system_info": system_info,
        "count_lines": count_lines
    } 