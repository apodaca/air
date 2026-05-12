from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("AirQualityServer")

@mcp.tool()
def get_status() -> str:
    """
    Dummy tool to verify the framework and MCP scaffolding.
    """
    return "Air Quality MCP Server is running and operational."

if __name__ == "__main__":
    mcp.run()
