import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import random
import time

# Initialize FastAPI app
app = FastAPI(title="Text Analysis Backend")

# Data model for the input
class UserInput(BaseModel):
    text_input_1: str
    text_input_2: str
    # You can add more fields here in the future
    # extra_param: str = None 

# Dummy function to simulate complex processing
def process_data(text1: str, text2: str) -> List[Dict[str, Any]]:
    """
    Placeholder for your actual business logic.
    Returns a list of dicts which converts easily to a DataFrame.
    """
    # Simulate processing delay
    time.sleep(1)
    
    # Mock response data based on inputs
    # In a real app, you'd use ML models or DB queries here
    results = []
    
    # Generating some dummy rows
    for i in range(5):
        results.append({
            "ID": i + 1,
            "Source": "Input 1" if i % 2 == 0 else "Input 2",
            "Extracted_Entity": f"Entity_{random.randint(100, 999)}",
            "Confidence_Score": round(random.uniform(0.7, 0.99), 2),
            "Context_Snippet": text1[:20] + "..." if i % 2 == 0 else text2[:20] + "...",
            "Status": random.choice(["Verified", "Pending", "Flagged"])
        })
        
    return results

@app.get("/")
def read_root():
    return {"status": "Backend is running"}

@app.post("/analyze")
def analyze_text(payload: UserInput):
    try:
        # Call the dummy processing function
        data = process_data(payload.text_input_1, payload.text_input_2)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

