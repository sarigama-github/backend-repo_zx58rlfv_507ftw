from __future__ import annotations
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# Environment variables are injected by the platform. Fallbacks provided for local dev.
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "aigle_jurassien")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

async def list_collections() -> List[str]:
    db = await get_db()
    names = []
    async for name in db.list_collection_names():
        names.append(name)
    return names

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    to_insert = {**data, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    result = await db[collection_name].insert_one(to_insert)
    to_insert["_id"] = str(result.inserted_id)
    return to_insert

async def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    docs: List[Dict[str, Any]] = []
    async for doc in cursor:
        doc["_id"] = str(doc.get("_id"))
        docs.append(doc)
    return docs
