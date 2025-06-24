#!/usr/bin/env python3
"""Universal MCP Server for OpenAPI specifications."""

import json
import os
import sys
from pathlib import Path
import httpx
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType


def count_endpoints(openapi_spec: dict) -> int:
    """Count total number of endpoints (paths + HTTP methods) in OpenAPI spec."""
    paths = openapi_spec.get("paths", {})
    total_endpoints = 0
    
    for _, path_obj in paths.items():
        # Count HTTP methods for this path
        http_methods = ["get", "post", "put", "delete", "patch", "head", "options", "trace"]
        for method in http_methods:
            if method in path_obj:
                total_endpoints += 1
    
    return total_endpoints


def load_config() -> dict:
    """Load configuration from config.json file."""
    config_path = Path(__file__).parent / "config.json"
    
    if not config_path.exists():
        print(f"Error: config.json not found at {config_path}")
        sys.exit(1)
    
    with open(config_path, "r") as f:
        return json.load(f)


def load_openapi_spec(spec_path: str) -> dict:
    """Load OpenAPI specification from file."""
    spec_file = Path(__file__).parent / spec_path
    
    if not spec_file.exists():
        print(f"Error: OpenAPI spec not found at {spec_file}")
        sys.exit(1)
    
    with open(spec_file, "r") as f:
        return json.load(f)


def create_mcp_server(config: dict) -> FastMCP:
    """Create and configure the MCP server."""
    # Load OpenAPI specification
    openapi_spec = load_openapi_spec(config["openapi_spec_path"])
    
    # Create HTTP client with configuration
    client_config = {"base_url": config["base_url"]}
    
    if "headers" in config and config["headers"]:
        client_config["headers"] = config["headers"]
    
    # Override headers with environment variables if they exist
    if "env_headers" in config:
        env_headers = {}
        for key, env_var in config["env_headers"].items():
            env_value = os.getenv(env_var)
            if env_value:
                env_headers[key] = env_value
        
        if env_headers:
            if "headers" not in client_config:
                client_config["headers"] = {}
            client_config["headers"].update(env_headers)
    
    client = httpx.AsyncClient(**client_config)
    
    # Configure route mappings
    route_maps = config.get("route_maps", [RouteMap(mcp_type=MCPType.TOOL)])
    if isinstance(route_maps, list) and route_maps:
        # Convert dict route maps to RouteMap objects if needed
        converted_maps = []
        for route_map in route_maps:
            if isinstance(route_map, dict):
                converted_maps.append(RouteMap(mcp_type=MCPType.TOOL))
            else:
                converted_maps.append(route_map)
        route_maps = converted_maps
    else:
        route_maps = [RouteMap(mcp_type=MCPType.TOOL)]
    
    # Create the MCP server
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name=config["name"],
        route_maps=route_maps,
    )
    
    # Count and display endpoints
    endpoint_count = count_endpoints(openapi_spec)
    print(f"[{config['name']}] Total number of endpoints: {endpoint_count}")
    
    return mcp


def main():
    """Main entry point."""
    try:
        config = load_config()
        mcp = create_mcp_server(config)
        mcp.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 