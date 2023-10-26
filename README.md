# Django APP

## Getting started

> All of the following commands need to be executed from the project's root directory

To install all the requirments needed for the backend, run:

```bash
pip install -r /ecommerce_project/requirements.txt
```

To install all the requirments needed for the GUI, run:

```bash
pip install -r requirementsGUI.txt
```

## Backend server

To use the backend server make sure to perform all of the database migrations, via:

```bash
python /ecommerce_project/manage.py migrate
```

Afterwards, You can start the server:

```bash
python /ecommerce_project/manage.py runserver
```

## GUI

To start the GUI run:

```bash
python GUI.py
```
