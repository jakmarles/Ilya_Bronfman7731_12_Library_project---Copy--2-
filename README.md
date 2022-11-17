
![Logo](https://cdn.discordapp.com/attachments/592142768453845022/1032280516549947473/unknown.png)


# Library Management System

A simple system to manage books library
A Python Flask based Library Management System. 
This Flask app has all the features of a Library Management System like adding,removing, and loaning books.

## Deployment

Create Virtual Environment.

```bash
pip install virtualenv 
py  -m virtualenv myenv
Activate: myenv\Scripts\activate

```
Install dependencies.

```bash
pip install -r .\requirements.txt

```

Run the application.

```bash
py .\app.py

```
Navigate to http://127.0.0.1:5000/

## Features

- Add a new customer
- Add a new book
- Loan a book
- Return a book
- Display all books
- Display all customers
- Display all loans
- Display late loans
- Find book by name
- Find customer by name
- Remove book
- Remover customer
- Automaticly populate the database if it's empty



## Authors

- [@jakmarles](https://github.com/jakmarles) - Ilya Bronfman

![Credits](https://img.shields.io/badge/Credits-Ilya%20Bronfman-green)


## Note to Eyal
- In order to make the testing of late loans easier for you head to init_db.py and remove the # from lines 12 and 19 and remove the Database file (library.sqlite)
normaly i wouldnt include it but since its a test its there for you.
 