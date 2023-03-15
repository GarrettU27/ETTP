# ETTP

This is the repository for the ECG Training Tool Project, or ETTP for short. It is a desktop application written in [Python](https://www.python.org/) meant to train people in identifying various arrhythmias in ECGs. It uses a [SQLite](https://www.sqlite.org/index.html) database for storing the data and a [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) frontend. [ecg-plot](https://pypi.org/project/ecg-plot/), with modifications, is used to produce the ECG graphics and [neurokit2](https://pypi.org/project/neurokit2/) is used to process the ECGs for annotations.

[This tutorial](https://docs.python.org/3/library/sqlite3.html) from the Python documentation was used to setup the `sqlite3` module in Python to connect to SQLite

# Setting Up the Project

1. Install [Python 3.11.2](https://www.python.org/downloads/) (current latest installation of Python)

2. For installing the Python libraries, I heavily recommend creating a virtual environment first. First, you will create a virtual environment with the following command
   
   ```bash
   python -m venv venv
   ```
   
   After that, you run the script you generated to activate your virtual environment. On Windows, that would look like the following
   
   ```bash
   .\venv\Scripts\activate
   ```
   
   Note that you might need to enable the ability to run scripts on your system

3. Then, run the following command
   
   ```bash
   pip install numpy matplotlib scipy neurokit2 PyQt6 qtawesome
   ```

4. To run the application, run the following command
   
   ```bash
   python main.py
   ```

5. To seed the database, run the following command
   
   ```bash
   python seed.py
   ```

6. To compile the application into an executable, first install the `pyinstaller` library like so
   
   ```bash
   pip install -U pyinstaller
   ```

7. Then, simply compile using the `spec` file in the root directory. In other words, run the following command
   
   ```bash
   pyinstaller main.spec
   ```

8. To run the application, find the app's executable, which will  `dist/main/main.exe`

# Recommended Dev Tools

While these tools are not required, these are good tools to use in your development environment. Assuming you are a student of the University of Minnesota, all of these should be free through the school

- [PyCharm: the Python IDE for Professional Developers by JetBrains](https://www.jetbrains.com/pycharm/) - this is a good IDE to use for Python

- [Sublime Merge](https://www.sublimemerge.com/) - this is a good GUI to use with git

- [VS Code](https://code.visualstudio.com/) - If you cannot get your hands on a copy of WebStorm or PyCharm, VS Code is a nice replacement for those two, but you will have to spend some time installing plugins
