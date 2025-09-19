# Query a collection
record = await session.call_tool(
    "find_by_userid",
    {
        "db_name": "modq",
        "collection_name": "crm_processed_records",
        "user_id": "ebb08033-10bd-454d-833c-840199e013a9"
    }
)
print("Record:", record)

# Get recent documents
records = await session.call_tool(
    "list_recent",
    {"db_name": "modq", "collection_name": "crm_processed_records", "limit": 3}
)
print("Recent Records:", records)
