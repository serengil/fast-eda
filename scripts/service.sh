cd ../src

# production server
# uvicorn app:service --reload --host 0.0.0.0 --port 5000 # update the service whenever a code change is detected
uvicorn app:service --host 0.0.0.0 --port 5000 --workers 2