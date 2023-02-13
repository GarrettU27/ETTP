# ETTP

This is the repository for the ECG Training Tool Project, or ETTP for short. It is a web application meant to train people in identifying various arrhythmias in ECGs. The backend is implemented using [FastAPI](https://fastapi.tiangolo.com/) with [pymongo]([pymongo · PyPI](https://pypi.org/project/pymongo/)) used to connect to an instance of [MongoDB](https://www.mongodb.com/). The frontend is implemented using [React](https://reactjs.org/).

[PyMongo Tutorial: MongoDB And Python | MongoDB](https://www.mongodb.com/languages/python/pymongo-tutorial) served as a good basis for the project, and helped with setting up many of the features

# Setting Up the Project

1. Install [MongoDB Community Server](https://www.mongodb.com/try/download/community). Use the complete setup type. Keep the options default, but make sure you install MongoDB Compass 

2. Open MongoDB Compass and use the following uri to connect `mongodb://localhost:27017`

3. Install [Python 3.11.2](https://www.python.org/downloads/) (current latest installation of Python)

4. For installing the Python libraries, I heavily recommend creating a virtual environment first. First, you will create a virtual environment in the server folder with the following command
   
   ```bash
   python -m venv venv
   ```
   
   After that, you run the script you generated to activate your virtual environment. On Windows, that would look like the following
   
   ```bash
   .\venv\Scripts\activate
   ```
   
   Note that you might need to enable the ability to run scripts on your system

5. Then, in the server folder, run the following command
   
   ```bash
   pip install numpy matplotlib scipy neurokit2 
   ```

6. Then, run the following command to start the server
   
   ```bash
   uvicorn main:app --reload
   ```

7. Install [Node 18.14.0](https://nodejs.org/en/) (current LTS version of NodeJS)

8. In the client folder, first run
   
   ```bash
   npm install
   ```

9. Then, use the following command to start the client
   
   ```bash
   npm run start
   ```

# Server Links

After starting up the development server, there are a handful of useful things you can view in your browser if you go the following links

- http://127.0.0.1:8000/docs# - provides documentation on all the available routes the server provides. It also gives you the option to execute the corresponding requests these routes accept

- http://127.0.0.1:8000/redoc - provides all responses the server has given and the specific errors they may have had

- http://127.0.0.1:8000/ - this is the root route, which is currently a basic get request saying "Hello World". You can make sure you get a page saying "Hello World" with this link to ensure the server is running

# Frontend Links

There is not much for links here, just the one that connects you to the client, which should open by default

- http://localhost:3000/

# Recommended Dev Tools

While these tools are not required, these are good tools to use in your development environment. Assuming you are a student of the University of Minnesota, all of these should be free through the school

- [WebStorm: The Smartest JavaScript IDE, by JetBrains](https://www.jetbrains.com/webstorm/) - this is a good IDE to used for the frontend

- [PyCharm: the Python IDE for Professional Developers by JetBrains](https://www.jetbrains.com/pycharm/) - this is a good IDE to use for the backend

- [Sublime Merge](https://www.sublimemerge.com/) - this is a good GUI to use with git

- [VS Code](https://code.visualstudio.com/) - If you cannot get your hands on a copy of WebStorm or PyCharm, VS Code is a nice replacement for those two, but you will have to spend some time installing plugins
