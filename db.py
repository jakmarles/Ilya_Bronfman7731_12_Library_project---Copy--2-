# import statements
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# create engine
engine = create_engine('sqlite:///library.sqlite', echo=True,
                       connect_args={'check_same_thread': False})
base = declarative_base()

# Books Table


class Books(base):

    __tablename__ = 'Books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    year_published = Column(String)
    type = Column(Integer)

    def __init__(self, name, author, year_published, type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.type = int(type)

# Customers Table


class Customers(base):
    __tablename__ = 'Customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    age = Column(Integer)

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = int(age)

# Loans Table


class Loans(base):
    __tablename__ = 'Loans'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(
        "Customers.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey(
        "Books.id", ondelete="CASCADE"), nullable=False)
    loan_date = Column(String)
    return_date = Column(String)

    def __init__(self, customer_id, book_id, loan_date, return_date):
        self.customer_id = int(customer_id)
        self.book_id = int(book_id)
        self.loan_date = loan_date
        self.return_date = return_date
