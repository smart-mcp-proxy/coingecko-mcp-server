#!/usr/bin/env python3
"""Universal MCP Server for OpenAPI specifications."""

import os
import httpx
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType


def main():
    """Main entry point."""
    # CoinGecko configuration
    config = {
        "name": "CoinGecko API",
        "base_url": "https://api.coingecko.com/api/v3",
        "oas_url": "https://raw.githubusercontent.com/coingecko/coingecko-api-oas/refs/heads/main/coingecko-public-api-v3.json"
    }
    
    # Download OpenAPI spec
    openapi_spec = httpx.get(config["oas_url"]).json()
    
    # Setup headers
    headers = {}
    api_key = os.getenv("COINGECKO_API_KEY")
    if api_key:
        headers["x-cg-demo-api-key"] = api_key
    
    # Create HTTP client
    client = httpx.AsyncClient(
        base_url=config["base_url"],
        headers=headers if headers else None
    )
    
    # Create MCP server
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name=config["name"],
        route_maps=[RouteMap(mcp_type=MCPType.TOOL)]
    )
    
    mcp.run()


if __name__ == "__main__":
    main()
