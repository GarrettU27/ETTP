# ETTP

This is the repository for the ECG Training Tool Project, or ETTP for short. It is a web application designed with a [MERN Stack](https://www.mongodb.com/mern-stack)



# Setting Up the Project

1. Install [MongoDB Community Server](https://www.mongodb.com/try/download/community). Use the complete setup type. Keep the options default, but make sure you install MongoDB Compass 

2. Open MongoDB Compass and use the following uri to connect `mongodb://localhost:27017`

3. In the server folder, run 

```bash
pip install "fastapi[all]" "pymongo[srv]"
```

4. Then, run the following command to start the server

```bash
uvicorn main:app --reload
```

5. In the client folder, first run

```bash
npm install
```

6. Then, use the following command to start the client

```bash
npm run start
```
