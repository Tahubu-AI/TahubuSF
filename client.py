from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def run():
    async with streamable_http_client(url="http://localhost:5000/mcp") as streams:
        async with ClientSession(*streams) as session:
            # Call the function you want to run
            await session.initialize()
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"Tool: {tool.name}")
                print(f"Description: {tool.description}")
            print()
            result = await session.call_tool("getNews")
            print(result.content[0].text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())