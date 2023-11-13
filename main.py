from api.views import app  # Import your FastAPI app instance from the views.py file
import uvicorn
import logging

## To run
#### uvicorn main:app --host 127.0.0.1 --port 8080 --reload


logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)