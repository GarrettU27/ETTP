# ETTP

This is the repository for the ECG Training Tool Project, or ETTP for short. It is a desktop application written in [Python](https://www.python.org/) meant to train people in identifying various arrhythmias in ECGs. It uses a [SQLite](https://www.sqlite.org/index.html) database for storing the data and a [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) frontend. [ecg-plot](https://pypi.org/project/ecg-plot/), with modifications, is used to produce the ECG graphics and [neurokit2](https://pypi.org/project/neurokit2/) is used to process the ECGs for annotations.

[This tutorial](https://docs.python.org/3/library/sqlite3.html) from the Python documentation was used to setup the `sqlite3` module in Python to connect to SQLite

# Setting Up the Project

1. Install [Python 3.11.2](https://www.python.org/downloads/) (current latest installation of Python)

2. To help make the management of dependencies easier, we use [Pipenv](https://pipenv.pypa.io/en/latest/). This library handles creating the proper virtual environment, tracking dependencies, and resolving dependency issues. To use it, first run this command
   
   ```bash
   pip install --user pipenv
   ```
   
   Note: `pipenv` sets the requirement of the project to use a specific version of python. If you're on mac, you can simply install [pyenv](https://github.com/pyenv/pyenv) and let `pipenv` handle installing the right version. On windows, you'll have to install the right version yourself, but you can use the windows version of `pyenv`: [pyenv-win](https://github.com/pyenv-win/pyenv-win) (though, I don't know whether `pipenv` will use it to set python versions for you automatically)

3. After that, we want to install the current set of dependnecies required by the project. Navigate your terminal so that the current directory is the project root directory and run the following command
   
   ```bash
   python -m pipenv sync
   ```

4. To run the application, you need to run the python file in such a way that it uses the `pipenv` dependencies. One way is to access the `pipenv` shell and then run the app normally. The other method is to run the following command
   
   ```bash
   python -m pipenv run python main.py
   ```

5. To seed the database, the same principle holds. But, just run the following command
   
   ```bash
   python -m pipenv run python seed.py
   ```

6. To compile the application into an executable, you need to run `pyinstaller` on the `main.spec`, which are the compilation settings. To do that, run the following command
   
   ```bash
   python -m pipenv run pyinstaller main.spec
   ```

7. To run the application, find the app's executable, which will `dist/main/main.exe`

# Adding Libraries

If you add libraries to the project, you will want to install them using `pipenv` to ensure the newly installed libraries are tracked. To install a library with `pipenv`, simply run

```bash
python -m pipenv install <library_name>
```

# Recommended Dev Tools

While these tools are not required, these are good tools to use in your development environment. Assuming you are a student of the University of Minnesota, all of these should be free through the school

- [PyCharm: the Python IDE for Professional Developers by JetBrains](https://www.jetbrains.com/pycharm/) - this is a good IDE to use for Python

- [Sublime Merge](https://www.sublimemerge.com/) - this is a good GUI to use with git

- [VS Code](https://code.visualstudio.com/) - If you cannot get your hands on a copy of WebStorm or PyCharm, VS Code is a nice replacement for those two, but you will have to spend some time installing plugins
