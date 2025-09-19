from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio

SSE_URL = "http://127.0.0.1:8001/sse"   # matches mcp_server.py run()

async def run():
    async with sse_client(url=SSE_URL) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            # --- discover what's available (optional) ---
            toolsets = await session.list_toolsets()
            print("Toolsets:", toolsets)

            # --- 1) call your MongoDB tool: list_recent ---
            recent = await session.call_tool(
                "list_recent",
                {
                    "db_name": "modq",                    # from your Compass
                    "collection_name": "crm_processed_records",
                    "limit": 5
                }
            )
            print("Recent docs:", recent)

            # --- 2) (optional) call find_by_userid if/when you have a value ---
            # record = await session.call_tool(
            #     "find_by_userid",
            #     {
            #         "db_name": "modq",
            #         "collection_name": "crm_processed_records",
            #         "user_id": "PUT-A-REAL-USERID-HERE"
            #     }
            # )
            # print("Record by user_id:", record)

            # --- 3) prompts still work as before (your current code) ---
            prompts = await session.list_prompts()
            print("Prompts:", prompts)

            prompt = await session.get_prompt(
                "review_code",
                arguments={"code": 'print("Hello world!")'}
            )
            print("Prompt (review_code):", prompt)

            # You can also test the other prompt:
            # debug = await session.get_prompt("debug_error", arguments={"error": "KeyError: 'access_token'"})
            # print("Prompt (debug_error):", debug)

if __name__ == "__main__":
    asyncio.run(run())
# mcp_client.py
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

SSE_URL = "http://127.0.0.1:8001/sse"  # must match mcp_server.py

async def run():
    async with sse_client(url=SSE_URL) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            # 1) list what's available (optional)
            toolsets = await session.list_toolsets()
            print("Toolsets:", toolsets)

            # 2) list_recent (no user_id needed)
            recent = await session.call_tool(
                "list_recent",
                {"db_name": "modq", "collection_name": "crm_processed_records", "limit": 3}
            )
            print("Recent:", recent)

            # 3) generic query by Type
            docs = await session.call_tool(
                "find_many",
                {
                    "db_name": "modq",
                    "collection_name": "crm_processed_records",
                    "filter": {"Type": "AccountInsight"},
                    "sort": [["UpdatedTimestamp", -1]],
                    "limit": 3
                }
            )
            print("By Type=AccountInsight:", docs)

            # 4) optional prompt (unchanged)
            prompt = await session.get_prompt("review_code", arguments={"code": 'print("Hello")'})
            print("Prompt:", prompt)

if __name__ == "__main__":
    asyncio.run(run())
