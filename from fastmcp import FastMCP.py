from fastmcp import FastMCP
from pymongo import MongoClient

# Create MCP Server
mcp = FastMCP("MongoDB-MCP")

# --- MongoDB Connection ---
# Use the same full URL you use in Compass (with hosts, ports, replicaSet, ssl, etc.)
MONGO_URI = "m"

client = MongoClient(MONGO_URI)


# --- MCP Tools ---

@mcp.tool()
def find_by_userid(db_name: str, collection_name: str, user_id: str) -> dict:
    """Find a record in MongoDB by UserId from any DB + collection"""
    db = client[db_name]
    collection = db[collection_name]
    record = collection.find_one({"UserId": user_id})
    if record:
        record["_id"] = str(record["_id"])
        return record
    return {"error": f"No record found for UserId={user_id} in {db_name}.{collection_name}"}


@mcp.tool()
def list_recent(db_name: str, collection_name: str, limit: int = 5) -> list:
    """List the most recent N records from any DB + collection"""
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find().sort("UpdatedTimestamp", -1).limit(limit)
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results


# Example Prompt (still available)
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Reviewing your code:\n{code}"
