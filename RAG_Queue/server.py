from fastapi import FastAPI,Query
from Worker.worker_function import process_query
from queue_rag.queue_rag import queue

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/enqueue")
def enqueue(query :str = Query(..., description="The query to be processed")):
    job = queue.enqueue(process_query, query)

    return {"job_id": job.get_id(), "status": "enqueued"}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    job = queue.fetch_job(job_id)

    if job is None:
        return {"error": "Job not found"}

    return {"job_id": job.get_id(), "status": job.get_status(), "result": job.result}