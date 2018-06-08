# Learning Management System

A basic but scalable management system that can be used in a university

## Introduction

The system is made up of 3 major users: admin, instructors and students. Each user has different level of access or permissions.

### Prerequisites

[![Python Version](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://python.org) &nbsp;
[![Django Version](https://img.shields.io/badge/django-1.11-brightgreen.svg)](https://djangoproject.com) &nbsp;
[![Virtualenvwrapper](https://img.shields.io/badge/virtualenvwrapper-stable-brightgreen.svg)](http://virtualenvwrapper.readthedocs.io/en/latest/install.html)



### Running the project locally

First clone the repository to your local machine

```
$ git clone https://github.com/Akohrr/Learning-Management-System.git
```

Change your directory

```
$ cd lms
```

create a virtual environment

```
$ mkvirtualenv django-lms
```

To activate the virtual environment

```
$ workon django-lms
```

Install the dependencies

```
$ pip install -r requirements.txt
```

Finally, run the development server

```
$ python manage.py runserver
```

The project would be available at 127.0.0.1:8000

## Running the tests

Use the details below to login and access the different features and roles of the system

|   username   |  password   |       Role |
|:------------:|:-----------:|-----------:|
|  kdutchburn2 | randompass  |    Admin   |
|  bosheilds1u | randompass  |    Admin   |
| cschachter98 | randompass  |    Admin   |
| aashurst48   | randompass  | Instructor |
|   acolbyea   | randompass  | Instructor |
|   aedger6j   | randompass  | Instructor |
|   abasond5   | randompass  |   Student  |
|    aberny    | randompass  |   Student  |
|  adeverale8y | randompass  |   Student  |

login to the system using one of the login credentials in the table above
