import openai
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

openai.api_key = "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"

@app.get("/openai")
async def generate_story(prompt: str, length: str = Query(None, title='Story Length', description='The length of the story (short, medium, long)'), 
genre: str = Query(None, title='Story Genre', description='The genre of the story (fantasy, horror, mystery, romance, sci-fi, thriller)')):
    try:
        if length:
            if "short" in length:
                length = ", 50-100 words, "
            elif "medium" in length:
                length = ", 100-150 words, "
            elif "long" in length:
                length = ", 150-200 words, "
            else:
                length = ", 100 words, "
            # f-string allows you to embed expressions inside string literals
            prompt = f"{prompt} {length}"
        if genre:
            prompt = f"{prompt} {genre}"

        print(prompt)
            
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        print(response)
        return response
    except openai.OpenAIError as e:
        raise HTTPException(status_code=400, detail=str(e))

# uvicorn main:app --reload
# This will start the service on http://localhost:8000
# Test the service by sending a GET request to http://localhost:8000/openai?prompt=What is the weather today?