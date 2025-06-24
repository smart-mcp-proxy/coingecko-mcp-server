# CoinGecko MCP Server

An MCP (Model Context Protocol) server that provides access to the CoinGecko API.

## Installation & Usage

### Using uvx (recommended)

```bash
uvx git+https://github.com/smart-mcp-proxy/coingecko-mcp-server
```

### Using pip

```bash
pip install git+https://github.com/smart-mcp-proxy/coingecko-mcp-server
coingecko-mcp-server
```

### Development

```bash
git clone https://github.com/smart-mcp-proxy/coingecko-mcp-server
cd coingecko-mcp-server
pip install -e .
python main.py
```

## Configuration

### API Key (Optional)

For higher rate limits, set your CoinGecko API key:

```bash
export COINGECKO_API_KEY="your-api-key-here"
```

The server will automatically load the OpenAPI specification and make all endpoints available as MCP tools.

## Available Endpoints

This server exposes all CoinGecko API endpoints as MCP tools. The exact number of available endpoints is displayed when the server starts.

## License

MIT
