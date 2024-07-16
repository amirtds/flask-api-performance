# init_db.py
from app import db, User, app

with app.app_context():
    # Create the database and the database table
    db.create_all()

    # Insert initial data
    user1 = User(name='John Doe', email='john@example.com')
    user2 = User(name='Jane Doe', email='jane@example.com')

    # Add the records to the session
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes to the database
    db.session.commit()
