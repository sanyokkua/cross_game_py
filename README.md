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
1) Install Virtual Environment in order to install it locally, without installing package and dependencies globally
```Shell
python3 -m venv .venv
```
2) Activate in the current console session Virtual Environment
```Shell
source .venv/bin/activate
```
3) Install Build Package
```Shell
pip install build
```
4) Install All the development Packages if it is reqiured
```Shell
pip install -e ".[development]"
```
5) Build the Project
```Shell
python -m build
```
6) Install package
```Shell
pip install dist/crossgame-0.0.1-py3-none-any.whl
```
7) Run the game
- Console App
- Tkinter App
- QT6 App
8) If it is required, Project has unittests for the Game "Engine" (Base classes with the game logic)
```Shell
python -m unittest discover tests -v
```
