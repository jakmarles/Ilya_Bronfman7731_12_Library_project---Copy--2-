from sqlalchemy.orm import sessionmaker

def db_load_example_data_customers(app, db,session):
    customer_details = session.query(db.Customers).first() # check if there are any customers in the db if no automaticly insert in when the app is launched 
    if customer_details:
        pass
    else:
        # The customer data that will be inserted into the db below
        custormer_01 = db.Customers(name="Ilya", city="TelAviv", age=22)
        custormer_02 = db.Customers(name="Jack", city="RoshHain", age=35)
        custormer_03 = db.Customers(name="Michael", city="Haifa", age=38)
        # loan_01 = db.Loans(customer_id="1", book_id="1", loan_date="2022-10-06", return_date="2022-10-08")

        with app.app_context():
            db.base.metadata.create_all(db.engine) # create db if doesnt already exist
            Session = sessionmaker(bind=db.engine)  # initialize sessionmaker
            session = Session()  # make Session object
            session.add_all([custormer_01, custormer_02,custormer_03]) # add the info to db
            # session.add_all([loan_01])
            session.commit() # commit the changes


def db_load_example_data_books(app, db,session):
    book_details = session.query(db.Books).first() # check if there are any books in the db if no automaticly insert in when the app is launched 
    if book_details:
        pass
    else:
        # The data that will be inserted into the db below
        book_01 = db.Books(name="The Teachings Of Don Juan: A Yaqui Way of Knowledge", author="Carlos Castaneda", year_published=1968, type=1)
        book_02 = db.Books(name="Journeys out of the body", author="Robert Monroe", year_published=1971, type=2)
        book_03 = db.Books(name="Lucid Dreaming The power of being aware and awake in your dreams", author="Stephen LaBerge", year_published=1985, type=3)
        


        with app.app_context():
            db.base.metadata.create_all(db.engine) # create db if doesnt already exist
            Session = sessionmaker(bind=db.engine)  # initialize sessionmaker
            session = Session()  # make Session object
            session.add_all([book_01, book_02,book_03]) # add the info to db
            session.commit() # commit the changes