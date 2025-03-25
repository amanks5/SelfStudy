from database import *

# creates a table in postgresql with an auto incrementing id when new notes are added and title content sections
def create_table():
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_notes (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL
        );''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_flashcards (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        front_card TEXT NOT NULL,
        back_card TEXT NOT NULL
    );
    ''')
    connection.commit()
    cursor.close()
