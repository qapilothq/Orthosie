from utils import encode_image, extract_clickable
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from prompts import suggestion_prompt, tetscase_prompt, suggestionWithText_prompt
from init_llm import initialize_llm
from typing import Optional
from dotenv import load_dotenv
import os
import json 


load_dotenv()
app = FastAPI()

class suggestionRequest(BaseModel):
    image: Optional[str] = None
    userinput: Optional[str] = None
    
class testcaseRequest(BaseModel):
    xml: Optional[str] = None
    scenario: Optional[str] = None

@app.post("/invoke/suggestions")
async def suggestions(request: suggestionRequest):
    llm_key = os.getenv("OPENAI_API_KEY")

    if not llm_key:
        raise HTTPException(status_code=500, detail="API key not found. Please check your environment variables.")
    llm = initialize_llm(llm_key)

    try:
        if (request.userinput and request.image):
            base64image = encode_image(request.image)
            print("userinoputted scenarios")
            message = [
                    (
                    "system",
                    suggestionWithText_prompt,
                    ),
                    ("human", [
                        {"type": "text", "text": f"This is the userinputted natural language scenario: {request.userinput}"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64image}"},
                        },
                    ]),
                ]
        elif request.image:
            base64image = encode_image(request.image)
            message = [
                    (
                    "system",
                    suggestion_prompt,
                    ),
                    ("human", [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64image}"},
                        },
                    ]),
                ]
        else:
            raise HTTPException(status_code=400, detail="Image must be provided.")

        bdd_test_case = llm.invoke(message)
        output = bdd_test_case.content.strip("```json\n").strip("\n```")
        return {"status": "success", "agent_response": json.loads(output)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/invoke/teststeps")
async def teststeps(request: testcaseRequest):
    try:
        llm_key = os.getenv("OPENAI_API_KEY")
        if not llm_key:
            raise HTTPException(status_code=500, detail="API key not found. Please check your environment variables.")
        llm = initialize_llm(llm_key)
        
        if request.xml and request.scenario:
            parsed_xml = extract_clickable(request.xml)
            message = [
                    (
                        "system",
                        tetscase_prompt,
                    ),
                    (
                        "human", 
                        f"this is the required test scenario json: {request.scenario}"
                    ),
                    (
                        "human", 
                        f"this is the required test XML: {parsed_xml}"
                    ),
                ]
        else:
            raise HTTPException(status_code=400, detail="XML and testcase scenario must be provided.")

        test_steps = llm.invoke(message)
        output = test_steps.content.strip("```json\n").strip("\n```")
        return {"status": "success", "agent_response": json.loads(output)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "APP is healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
