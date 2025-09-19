# mcp_server.py
from fastmcp import FastMCP
from pymongo import MongoClient
from bson import ObjectId
from typing import Any, Dict, List, Tuple, Optional

mcp = FastMCP("MongoDB-MCP")

# ---- Use your Compass URL as-is (no user/pass), e.g. replica set with TLS ----
# Example: "mongodb://host1:29000,host2:29000,host3:29000/?replicaSet=rs0&ssl=true"
MONGO_URI = "<PASTE_YOUR_COMPASS_URL>"
client = MongoClient(MONGO_URI)


# ---- helpers ----
def _stringify_ids(doc: Dict[str, Any]) -> Dict[str, Any]:
    d = dict(doc)
    if "_id" in d and isinstance(d["_id"], ObjectId):
        d["_id"] = str(d["_id"])
    return d


# ---- TOOLS ----

@mcp.tool()
def list_recent(db_name: str, collection_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    List the most recent N docs sorted by UpdatedTimestamp descending.
    """
    db = client[db_name]
    coll = db[collection_name]
    cursor = coll.find().sort("UpdatedTimestamp", -1).limit(limit)
    return [_stringify_ids(doc) for doc in cursor]


@mcp.tool()
def find_many(
    db_name: str,
    collection_name: str,
    filter: Dict[str, Any],
    limit: int = 10,
    sort: Optional[List[Tuple[str, int]]] = None,
) -> List[Dict[str, Any]]:
    """
    Run an arbitrary MongoDB query filter and return up to N docs.
    sort format: [["UpdatedTimestamp", -1]]  or  [["ExtId", 1]]
    """
    db = client[db_name]
    coll = db[collection_name]
    cur = coll.find(filter)
    if sort:
        cur = cur.sort(sort)
    if limit:
        cur = cur.limit(limit)
    return [_stringify_ids(doc) for doc in cur]


@mcp.tool()
def find_one(db_name: str, collection_name: str, filter: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find a single doc by any filter. If _id is a string, server handles it.
    """
    db = client[db_name]
    coll = db[collection_name]
    # if user passed _id as string, try to coerce to ObjectId
    f = dict(filter)
    if "_id" in f and isinstance(f["_id"], str):
        try:
            f["_id"] = ObjectId(f["_id"])
        except Exception:
            pass
    doc = coll.find_one(f)
    return _stringify_ids(doc) if doc else {}


# ---- (optional) prompts you already had ----
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"

@mcp.prompt()
def debug_error(error: str):
    return [
        ("User", "I'm seeing this error:"),
        ("user", error),
        ("assistant", "I'll help debug that. What have you tried so far?"),
    ]


if __name__ == "__main__":
    # SSE transport on 8001 so ADK web can connect locally
    mcp.run(host="127.0.0.1", port=8001, transport="sse")
