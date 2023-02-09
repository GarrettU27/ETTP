# ETTP

This is the repository for the ECG Training Tool Project, or ETTP for short. It is a web application meant to train people in identifying various arrhythmias in ECGs. The backend is implemented using [FastAPI](https://fastapi.tiangolo.com/) with [pymongo]([pymongo · PyPI](https://pypi.org/project/pymongo/)) used to connect to an instance of [MongoDB](https://www.mongodb.com/). The frontend is implemented using [React](https://reactjs.org/).

# Setting Up the Project

1. Install [MongoDB Community Server](https://www.mongodb.com/try/download/community). Use the complete setup type. Keep the options default, but make sure you install MongoDB Compass 

2. Open MongoDB Compass and use the following uri to connect `mongodb://localhost:27017`

3. Install [Python 3.11.2](https://www.python.org/downloads/) (current latest installation of Python)

4. In the server folder, run 

```bash
pip install "fastapi[all]" "pymongo[srv]"
```

5. Then, run the following command to start the server

```bash
uvicorn main:app --reload
```

6. Install [Node 18.14.0](https://nodejs.org/en/) (current LTS version of NodeJS)

7. In the client folder, first run

```bash
npm install
```

8. Then, use the following command to start the client

```bash
npm run start
```

# Recommended Dev Tools

While these tools are not required, these are good tools to use in your development environment. Assuming you are a student of the University of Minnesota, all of these should be free through the school

- [WebStorm: The Smartest JavaScript IDE, by JetBrains](https://www.jetbrains.com/webstorm/) - this is a good IDE to used for the frontend

- [PyCharm: the Python IDE for Professional Developers by JetBrains](https://www.jetbrains.com/pycharm/) - this is a good IDE to use for the backend

- [Sublime Merge](https://www.sublimemerge.com/) - this is a good GUI to use with git

- [VS Code](https://code.visualstudio.com/) - If you cannot get your hands on a copy of WebStorm or PyCharm, VS Code is a nice replacement for those two, but you will have to spend some time installing plugins
