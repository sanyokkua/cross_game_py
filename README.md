# Cross Game Py (Tic Tac Toe or on ua: Хрестики-Нулики)
This is a simple implementation of the Tic Tac Toe game on python

## Main Idea
The idea to create this project is simple - learn Python.
The main aspects of Python language going to be learned/used inside this project.
For example:
- Working with python language types
- Working with python lists (collections)
- Working with python dictionaries (maps)
- Working with python OOP (class, inheritance, etc)
- Working with python lambdas and clousures
- Working with python modules

## Technologies
Also, this project is a place where will be tried different python frameworks/technologies such as:
- Tkinter (UI)
- PyQt (UI)
- Flask (Web-App)
- Django (Web-App)

## Parts
So, as result, this project will consist of next parts:
- Main module with the implementation of logic Tic Tac Toe game covered by unit tests
- Module that implements UI via Tkinter
- Module that implements UI via PyQt
- Module that implements Web-Application based on the Flask Framework
- Module that implements Web-Application based on the Django Framework

Also, here will be used build and distribution tools for packaging this project

## Structure
The current structure of the project:
- ./crossgame - Main module with all the logic and basic console app
- ./crossgameui - Module with the implementation of the simple Tkinter UI
- ./crossgameqt - Mpdule with the implementation of the simple QT6 UI
- ./resources - folder with any static resources that can be used in the app
- ./tests - unit tests (currently only for the Main module)
- ./pyproject.toml - all the meta information about project, including development dependencies
- ./setup.cfg - contains information about version, URL and where to find resources for the build
- ./.flake8 - config for linter
- ./create_venv.sh - helper script to create venv and activate it. Testend only on Mac OS

## How to build and install
Requires installed Python and Poetry.

1. Create Virtual Environment in order to install packages locally, without installing packages globally
```Shell
python3 -m venv .venv
```
1. Install Packages
```Shell
poetry install
```
3. Build the Project package
```Shell
poetry build
```
4. Run the game (from the root folder of the repository)
- Console App
```Shell
poetry run tictactoe  
```
- Tkinter App
```Shell
poetry run tictactoetk
```
- QT6 App
```Shell
poetry run tictactoeqt
```
8. If it is required, Project has unittests for the Game "Engine" (Base classes with the game logic)
```Shell
source .venv/bin/activate  # if it is not activated
python -m unittest discover tests -v
```
9. Make executable for your OS
TODO: Fix Loading of the Resources (--add-data 'resources/:./resources' or change a way of loading resources)
- Console App
```Shell
pyinstaller --onefile --windowed crossgame/main.py
```
- Tkinter App
```Shell
pyinstaller --onefile --windowed crossgameui/app.py
```
- QT6 App
For QT version was created a separate build spec file to define crucial properties to build it in correct way

To build spec file was used command (and if you want to just to build executable you should not use it again) and modified with custom properties:
> ```shell
> pyi-makespec --onefile --windowed crossgameqt/qtapp.py
> ```

And to build executables use this one instead:

```shell
pyinstaller qtapp.spec
```
