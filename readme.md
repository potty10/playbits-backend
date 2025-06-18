# Setup backend repo locally
1. Git clone  [backend repository](https://github.com/potty10/playbits-backend) to your desired folder.
```
git clone https://github.com/potty10/playbits-backend.git
```

2. Install necessary Python dependencies.
```
pip install -r requirements.txt
```

3. Create a .env file in the root repository with the following information. To create the MongoDB URI, you can head to MongoDB Atlas (Cloud) to set up your own cluster and obtain the URI, or use `mongodb://localhost:27017` if you use MongoDB locally in Docker (below).
```
OPENAI_API_KEY = <Your OpenAI key here>
MONGO_URI=<Your MongoDB URI here> 
DATABASE_NAME=db_local
```

4. Ensure that you have Docker downloaded.


5. Run MongoDB as container.
```
docker pull mongodb/mongodb-community-server:latest
docker run --name mongodb -p 27017:27017 -d mongodb mongodb-community-server:latest
```

6. Start running API via FastAPI
```
uvicorn main:app --reload
```
