import os
import subprocess
import json  # Add JSON parsing
from mcp.server.fastmcp import FastMCP  # Keep your original import

mcp = FastMCP("My MCP Server")

DEFAULT_WORKSPACE = os.getcwd()

@mcp.tool()
async def run_command(command: str) -> str:  # Keep async for official SDK
    """
    Run a terminal command inside the workspace directory.
    """
    try:
        # NEW: Parse JSON to extract the actual command
        if command.startswith('{'):
            command_data = json.loads(command)
            actual_command = command_data.get('command', '')
        else:
            actual_command = command
            
        result = subprocess.run(actual_command, shell=True, cwd=DEFAULT_WORKSPACE, capture_output=True, text=True)
        return result.stdout or result.stderr
    
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    mcp.run(transport='stdio')