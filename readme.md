# Run locally

## Install requirements
```
pip install fastapi uvicorn motor
```

## Run Qdrant
```
docker pull qdrant/qdrant
docker run -d -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant
```

Access at this link: http://127.0.0.1:6333/dashboard

## Download Ollama and pull model
```
ollama pull llama3.2:1b
```

## Run mongodb as container
```
docker pull mongodb/mongodb-community-server:latest
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

To view data, use Mongodb Compass
Access at this link: mongodb://localhost:27017


### Start FASTAPI
```
uvicorn main:app --reload
```