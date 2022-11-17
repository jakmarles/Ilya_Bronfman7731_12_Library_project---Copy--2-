# import statements
from sqlalchemy import and_
import init_db
from flask import Flask, redirect, render_template, request
import db
from sqlalchemy.orm import sessionmaker
import datetime

# Flask constructor
app = Flask(__name__)
session = Session()

@app.route('/')
def home():
    """
    When client click on the home button the server will run this method
    :return:
    """
    return render_template("home.html")


@app.route("/display/<cat>/")
def display(cat):
    """
    When client click on the display method the server will run this function and this function will return the
    relevant data to be displayed
    :param cat:
    cat = Category 
    :return:
    """
    # if user wants to display books 
    if cat == "book":
        book_names = session.query(db.Books.name).all()
        return render_template("display.html", cat=cat, book_names=book_names)
    # if user wants to display customers
    elif cat == "customer":
        customer_names = session.query(db.Customers.name).all()
        return render_template("display.html", cat=cat, customer_names=customer_names)

    # if user wants to display loans
    elif cat == "loan":
        customers = []
        books = []
        loan_dates = []
        return_dates = []
        for loan in session.query(db.Loans).all():
            customer = session.query(db.Customers.name).filter(
                db.Customers.id == loan.customer_id).first()
            book = session.query(db.Books.name).filter(
                db.Books.id == loan.book_id).first()
            customers.append(customer)
            books.append(book)
            loan_dates.append(loan.loan_date)
            return_dates.append(loan.return_date)
        return render_template("display.html", cat=cat, customers=customers, books=books, loan_dates=loan_dates, return_dates=return_dates)

    # if user wants to display late loans
    elif cat == "lateloan":
        customers = []
        books = []
        loan_dates = []
        return_dates = []
        late_days = []
        currentDate = datetime.datetime.now()
        for loan in session.query(db.Loans).all():
            if datetime.datetime.strptime(loan.return_date, "%Y-%m-%d") < currentDate:
                customer = session.query(db.Customers.name).filter(
                    db.Customers.id == loan.customer_id).first()
                book = session.query(db.Books.name).filter(
                    db.Books.id == loan.book_id).first()
                customers.append(customer)
                books.append(book)
                loan_dates.append(loan.loan_date)
                return_dates.append(loan.return_date)
                late_days.append((currentDate.date(
                ) - datetime.datetime.strptime(loan.return_date, "%Y-%m-%d").date()).days)

        return render_template("display.html", cat=cat, customers=customers, books=books, loan_dates=loan_dates, return_dates=return_dates, late_days=late_days)


@app.route("/return/", methods=["POST", "GET"])
def returnloan():
    """
    This method will be used for the return loan functionality
    :return:
    """

    book_details = session.query(db.Books.id, db.Books.name).all()
    customer_details = session.query(db.Customers.id, db.Customers.name).all()

    if request.method == "POST":
        book_id = int(request.form["book"])
        customer_id = int(request.form["customer"])
        loan_details = session.query(db.Loans).filter(and_(db.Loans.customer_id.like(customer_id),
                                                           db.Loans.book_id.like(book_id))).first()
        if loan_details:
            session.delete(loan_details)
            session.commit()
            return render_template("return.html", returned=True, book_details=book_details,
                                   customer_details=customer_details)
        else:
            return render_template("return.html", returned=False, book_details=book_details,
                                   customer_details=customer_details)
    else:
        return render_template("return.html", book_details=book_details, customer_details=customer_details)


@app.route("/loan/", methods=["POST", "GET"])
def loan():
    """
    this method will be used for taking loan functionality
    :return:
    """
    book_details = session.query(db.Books.id, db.Books.name, db.Books.type).all()
    loan_details = session.query(db.Loans.book_id).all()
    to_remove = []
    for book in book_details:
        if (book[0],) in loan_details:
            to_remove.append(book)
    for item in to_remove:
        book_details.remove(item)
    customer_details = session.query(db.Customers.id, db.Customers.name).all()
    if request.method == "POST":
        book_id = int(request.form["book"])
        customer_id = int(request.form["customer"])
        loan_date = str(request.form["loan_date"])
        return_date = str(request.form["return_date"])
        tr = db.Loans(book_id, customer_id, loan_date, return_date)
        session.add(tr)
        session.commit()
        return redirect ("/display/loan/")
    else:
        return render_template("loan.html", book_details=book_details, customer_details=customer_details)


@app.route('/remove/<cat>/', methods=["POST", "GET"])
def remove(cat):
    """
    this method will be used if user wants to remove any book or customer
    cat = Category
    :param cat:
    :return:
    """
    if request.method == "POST":
        if cat == "book":
            book_name = request.form["book_name"]
            book_details = session.query(db.Books).filter(
                db.Books.name == book_name).first()
            
            if book_details:
                session.delete(book_details)
                session.commit()
                return render_template("remove.html", cat=cat, book_deleted=True)
            else:
                return render_template("remove.html", cat=cat, book_deleted=False)

        else:
            customer_name = request.form["customer_name"]
            customer_details = session.query(db.Customers).filter(
                db.Customers.name == customer_name).first()
            if customer_details:
                session.delete(customer_details)
                session.commit()
                return render_template("remove.html", cat=cat, customer_deleted=True)
            else:
                return render_template("remove.html", cat=cat, customer_deleted=False)

    else:
        return render_template("remove.html", cat=cat)


@app.route('/find/<cat>/', methods=["POST", "GET"])
def find(cat):
    """
    this method will be used if the user wants to find any book or customer
    :param cat:
    cat = Category
    :return:
    """
    if request.method == "POST":
        if cat == "book":
            book_name = request.form["book_name"]
            book_details = session.query(db.Books).filter(
                db.Books.name == book_name).first()
            if book_details:

                return render_template("find.html", cat=cat, book_details=True, id=book_details.id,
                                       name=book_details.name, author=book_details.author,
                                       year=book_details.year_published, type=book_details.type)
            else:
                return render_template("find.html", cat=cat, book_details=False)
        else:
            customer_name = request.form["customer_name"]
            customer_details = session.query(db.Customers).filter(
                db.Customers.name == customer_name).first()
            if customer_details:

                return render_template("find.html", cat=cat, customer_details=True, id=customer_details.id,
                                       name=customer_details.name, city=customer_details.city,
                                       age=customer_details.age)
            else:
                return render_template("find.html", cat=cat, customer_details=False)

    else:
        return render_template("find.html", cat=cat)


@app.route('/add/<cat>/', methods=["POST", "GET"])
def add(cat):
    """
    this method will be used to add customer or book to the database
    :param cat:
    cat = Category
    :return:
    """
    if request.method == "POST":
        if cat == "book":
            book_name = request.form["book_name"]
            author_name = request.form["author_name"]
            published_date = request.form["year"]
            type = request.form["type"]

            tr = db.Books(book_name, author_name, published_date, type)
            session.add(tr)
            session.commit()

            return render_template("add.html", cat=cat)

        else:
            customer_name = request.form["customer_name"]
            city = request.form["city"]
            age = request.form["age"]

            tr = db.Customers(customer_name, city, age)
            session.add(tr)
            session.commit()

            return render_template("add.html", cat=cat)
    else:
        return render_template("add.html", cat=cat)


if __name__ == '__main__':
    db.base.metadata.create_all(db.engine)  # create database
    Session = sessionmaker(bind=db.engine)  # initialize sessionmaker
    session = Session() # make Session object
    init_db.db_load_example_data_customers(app, db, session) # runs the init db if the customer database is empty
    init_db.db_load_example_data_books(app, db, session) # runs the init db if the book database is empty
    app.run(debug=True)  # run flask app
