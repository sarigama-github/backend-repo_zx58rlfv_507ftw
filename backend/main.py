from __future__ import annotations
from typing import List, Dict, Any
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import Testimonial, Service, Course, Product, AuditRequest
from database import create_document, get_documents, list_collections, DATABASE_URL, DATABASE_NAME

app = FastAPI(title="Aigle Jurassien API", version="1.0.0")

# CORS - allow all origins for dev; frontend will call using provided URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Aigle Jurassien backend running"}

@app.get("/test")
async def test_connection() -> Dict[str, Any]:
    try:
        collections = await list_collections()
        return {
            "backend": "ok",
            "database": "mongo",
            "database_url": DATABASE_URL,
            "database_name": DATABASE_NAME,
            "connection_status": "connected",
            "collections": collections,
        }
    except Exception as e:
        return {
            "backend": "ok",
            "database": "mongo",
            "database_url": DATABASE_URL,
            "database_name": DATABASE_NAME,
            "connection_status": f"error: {e}",
        }

# Services
@app.get("/services", response_model=List[Service])
async def list_services() -> List[Service]:
    docs = await get_documents("service")
    return [Service(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/services", response_model=Service)
async def add_service(payload: Service) -> Service:
    doc = await create_document("service", payload.model_dump())
    return Service(**{k: v for k, v in doc.items() if k != "_id"})

# Academy Courses
@app.get("/courses", response_model=List[Course])
async def list_courses() -> List[Course]:
    docs = await get_documents("course")
    return [Course(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/courses", response_model=Course)
async def add_course(payload: Course) -> Course:
    doc = await create_document("course", payload.model_dump())
    return Course(**{k: v for k, v in doc.items() if k != "_id"})

# Shop Products
@app.get("/products", response_model=List[Product])
async def list_products() -> List[Product]:
    docs = await get_documents("product")
    return [Product(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/products", response_model=Product)
async def add_product(payload: Product) -> Product:
    doc = await create_document("product", payload.model_dump())
    return Product(**{k: v for k, v in doc.items() if k != "_id"})

# Testimonials
@app.get("/testimonials", response_model=List[Testimonial])
async def list_testimonials() -> List[Testimonial]:
    docs = await get_documents("testimonial")
    return [Testimonial(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/testimonials", response_model=Testimonial)
async def add_testimonial(payload: Testimonial) -> Testimonial:
    doc = await create_document("testimonial", payload.model_dump())
    return Testimonial(**{k: v for k, v in doc.items() if k != "_id"})

# Audit request
@app.post("/audit")
async def request_audit(payload: AuditRequest) -> Dict[str, Any]:
    doc = await create_document("auditrequest", payload.model_dump())
    return {"status": "received", "id": doc.get("_id")}
