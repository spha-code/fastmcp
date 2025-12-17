#!/usr/bin/env python3
import sys, json, asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("coingecko-mcp")

@app.list_tools()
async def list_tools():
    return [Tool(name="get_price",
                 description="Live price from CoinGecko",
                 inputSchema={"type":"object",
                              "properties":{
                                 "ids":{"type":"string"},
                                 "vs_currencies":{"type":"string"}
                              },
                              "required":["ids","vs_currencies"]})]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    import httpx, json
    r = httpx.get("https://api.coingecko.com/api/v3/simple/price",
                  params={"ids": arguments["ids"],
                          "vs_currencies": arguments["vs_currencies"]})
    return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]

async def main():
    # ----  CRITICAL:  log that we started  ----
    async with stdio_server() as (reader, writer):
        await app.run(reader, writer, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())