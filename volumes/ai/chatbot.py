#!/usr/bin/env python3
"""
Chat service using Hugging Face Transformers
FastAPI API with support for ChatML-formatted messages
"""

import os
import uuid
import logging
from typing import List, Dict, Optional
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline,
    set_seed
)

# ------------------------------------------------------------
# Models
# ------------------------------------------------------------

class ChatMessage(BaseModel):
    role: str  # "system", "user", "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    conversation_id: Optional[str] = None
    max_length: Optional[int] = None
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    model_used: str
    device: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    device: str
    model_name: str

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables d'environnement
MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "2048"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Display variables
print(f"MODEL_NAME: {MODEL_NAME}")
print(f"DEVICE: {DEVICE}")
print(f"MAX_LENGTH: {MAX_LENGTH}")
print(f"TEMPERATURE: {TEMPERATURE}")
print(f"torch.cuda.is_available(): {torch.cuda.is_available()}")


# ------------------------------------------------------------
# Variables globales
# ------------------------------------------------------------

model = None
tokenizer = None
pipe = None


def load_model():
    global model, tokenizer, pipe

    # Set seed for reproducibility
    torch.random.manual_seed(0) # for reproducibility

    model = AutoModelForCausalLM.from_pretrained( 
        "microsoft/Phi-3-mini-4k-instruct",  
        device_map=DEVICE if DEVICE == "cuda" else "auto",  
        torch_dtype="auto",  
        trust_remote_code=True,  
    ) 

    tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct") 

    pipe = pipeline( 
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
    ) 

def generate_response(messages: List[ChatMessage], max_length: int = None, temperature: float = None) -> str:
    global pipe
    try:
        generation_args = { 
            "max_new_tokens": MAX_LENGTH, 
            "return_full_text": False, 
            "temperature": TEMPERATURE, 
            "do_sample": False, 
        } 
        messages_dict = [{"role": msg.role, "content": msg.content} for msg in messages]

        output = pipe(messages_dict, **generation_args) 
        return output[0]['generated_text']
    except Exception as e:
        logger.error(f"Erreur lors de la génération: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")

# ------------------------------------------------------------
# FastAPI
# ------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    # Démarrage
    logger.info("Démarrage du service de chat...")
    load_model()
    yield
    # Arrêt
    logger.info("Arrêt du service de chat...")

# Créer l'application FastAPI
app = FastAPI(
    title="Deven Chat Service",
    description="Service de chat utilisant Transformers",
    version="1.0.0",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Vérification de l'état du service"""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        device=DEVICE,
        model_name=MODEL_NAME
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal pour le chat"""
    try:
        # Générer un ID de conversation si non fourni
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Générer la réponse
        response = generate_response(
            request.messages,
            request.max_length,
            request.temperature
        )
        
        return ChatResponse(
            response=response,
            conversation_id=conversation_id,
            model_used=MODEL_NAME,
            device=DEVICE
        )
        
    except Exception as e:
        logger.error(f"Erreur dans l'endpoint chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Page d'accueil"""
    return {
        "message": "Deven Chat Service",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "chatbot:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
