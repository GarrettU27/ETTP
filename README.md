# ETTP

This is the repository for the ECG Training Tool Project, or ETTP for short. It is a desktop application written
in [Python](https://www.python.org/) meant to train people in identifying various arrhythmias in ECGs. It uses
a [SQLite](https://www.sqlite.org/index.html) database for storing the data and
a [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) frontend. [ecg-plot](https://pypi.org/project/ecg-plot/),
with modifications, is used to produce the ECG graphics and [neurokit2](https://pypi.org/project/neurokit2/) is used to
process the ECGs for annotations.

[This tutorial](https://docs.python.org/3/library/sqlite3.html) from the Python documentation was used to setup
the `sqlite3` module in Python to connect to SQLite

# Setting Up the Project

1. Install [Python 3.11.2](https://www.python.org/downloads/) (current latest installation of Python)

2. To help make the management of dependencies easier, we use [Pipenv](https://pipenv.pypa.io/en/latest/). This library
   handles creating the proper virtual environment, tracking dependencies, and resolving dependency issues. To use it,
   first run this command
   
   ```bash
   pip install --user pipenv
   ```
   
   Note: `pipenv` sets the requirement of the project to use a specific version of python. If you install the proper
   version of `pyenv` for your OS, `pipenv` will handle installing the right version of python. If you're on Mac,
   install [pyenv](https://github.com/pyenv/pyenv). On Windows,
   install [pyenv-win](https://github.com/pyenv-win/pyenv-win).

3. After that, we want to install the current set of dependnecies required by the project. Navigate your terminal so
   that the current directory is the project root directory and run the following command
   
   ```bash
   python -m pipenv sync
   ```

4. To run the application, you need to run the python file in such a way that it uses the `pipenv` dependencies. One way
   is to access the `pipenv` shell and then run the app normally. The other method is to run the following command
   
   ```bash
   python -m pipenv run python main.py
   ```

5. Before seeding the database, you'll need to download the ECG data from
   PhysioNet: [A large scale 12-lead electrocardiogram database for arrhythmia study v1.0.0](https://physionet.org/content/ecg-arrhythmia/1.0.0/).
   Save the folder that you downloaded (that should be
   named `a-large-scale-12-lead-electrocardiogram-database-for-arrhythmia-study-1.0.0`) into the root directory of the
   project

6. To seed the database, the same principle holds. But, just run the following command
   
   ```bash
   python -m pipenv run python seed.py
   ```

7. Before you can use the database in the app, however, you need to remove entries that won't work with the annotations.
   You do that by running the `cull_database` script
   
   ```bash
   python -m pipenv run python cull_database.py
   ```

8. To compile the application into an executable, you need to run `pyinstaller` on the proper `spec` file for your OS. On Windows, this is `windows.spec`. On Mac, this is `mac.spec`. This file is the compilation settings. To use it, run the following command (for Windows, on Mac, switch out the spec file name)
   
   ```bash
   python -m pipenv run pyinstaller windows.spec
   ```

9. To run the application, find the app's executable, which will `dist/main/main.exe`

# Adding Libraries

If you add libraries to the project, you will want to install them using `pipenv` to ensure the newly installed
libraries are tracked. To install a library with `pipenv`, simply run

```bash
python -m pipenv install <library_name>
```

# Improvements for Future Maintainers

A software project is never really done, and there's always more to do. While this project is functional, and we are
proud of the result, there certainly are areas that could be cleaned up/improved. If you are someone taking on the task
of improving, modifying or maintaining this repository, here are some places that could use your attention.

- *Add CI/CD pipeline.* I was unfamiliar with Python when starting this project and was unable to properly add CI/CD.
  This would be a good thing to add to the repo. It's generally useful across the board

- *Cleaning up the messy code*. While we did our best to maintain coding best practices throughout this project, we
  still ended up having some messier parts to our code when all was said and done. In particular, `annotations.py` was
  written to be heavily extensible, but was not necessarily written to be readable or to follow best practices. It
  worked for what we needed, and it allowed us to get many annotations done for this project, but that file could use
  some reworking, and, in general, there are certain areas of the code that are not written particularly nicely and
  could do with some cleaning

- *Combining `cull_database` and `seed`*. Our project originally just had a `seed.py` script to seed the database.
  Towards the end, though, we realized we needed to remove ECGs that couldn't be properly annotated by our annotation
  script. Further, our database was somewhere around 6 GB with all the data we had collected, and that was far too large
  to distribute in a desktop app. So, we wrote `cull_database` to limit the size of the database and to remove entries
  that couldn't be annotated. However, it would probably make more sense for the logic in `cull_database` to be
  integrated into `seed`, so a developer simply has to seed the database

- *Add more arrhythmias*. This app can provide annotations for 8 arrhythmias, but the PhysioNet database we used has
  enough ECGs to support at least 14 arrhythmias. If you're a future maintainer, you may want to consider implementing
  the logic to support even more arrhythmias.

- *Fine tune annotations*. The annotations we created are certainly functional, but they don't get into much detail.
  Future maintainers could look into making the annotations more detailed by highlighting more sections and putting
  textual descriptions on them.

- *Improve responsive styling*. None of us were familiar with PyQt or desktop applications before we started this
  project, and I'm sad to say it probably shows. There are parts of the application where font sizes are constant even
  if the application is resized to be very large, because we couldn't fix the bugs that came with resizing fonts
  within `QScrollArea`. A future maintainer may be interested in making the responsive styling of the app more
  responsive

- *Improve `cull_database`'s speed*. To cull the database, `cull_database` needs to check if our annotation script can
  properly annotate the ECG, which requires it to call `plot_12_ecgs` from the annotation script. This is slow, and
  causes `cull_database` to take a large amount of time to run. Consider changing how `cull_database` checks if an ECG
  will be annotated properly

- *Improve `seed`'s speed*. `seed.py` currently takes somwhere in the realm of 15 to 20 minutes to run, which is very
  long. Consider trying to speed this up. There are two main things we think could potentially do that. First, we save
  the ECG data, which is a 5000x12 array, as a string into the database. It may be possible to save this array as binary
  data or something similar to improve the speed at which entries can be added to the database. Secondly, `seed.py` can
  probably be multi-threaded. Potentially, you could create a thread for each sub-folder `seed.py` pulls data from and
  have each thread find database entries. This would probably improve `seed`'s speed as well

# Recommended Dev Tools

While these tools are not required, these are good tools to use in your development environment. Assuming you are a
student of the University of Minnesota, all of these should be free through the school

- [PyCharm: the Python IDE for Professional Developers by JetBrains](https://www.jetbrains.com/pycharm/) - this is a
  good IDE to use for Python

- [Sublime Merge](https://www.sublimemerge.com/) - this is a good GUI to use with git

- [VS Code](https://code.visualstudio.com/) - If you cannot get your hands on a copy of WebStorm or PyCharm, VS Code is
  a nice replacement for those two, but you will have to spend some time installing plugins
