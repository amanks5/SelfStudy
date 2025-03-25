from database import *


def create_flashcard(front_card, back_card):
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO user_flashcards (front_card, back_card)
    VALUES (%s, %s)
    RETURNING id;
    ''', (front_card, back_card))
    flashcard_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    return flashcard_id


def fetch_all_flashcards():
    cursor = connection.cursor()
    cursor.execute('''
    SELECT id, front_card, back_card FROM user_flashcards;
    ''')
    cards = cursor.fetchall()
    cursor.close()
    return [{'id': row[0], 'front_card': row[1], 'back_card': row[2]} for row in cards]


def fetch_flashcard(flashcard_id):
    cursor = connection.cursor()
    cursor.execute('''
    SELECT id, front_card, back_card FROM user_flashcards WHERE id = %s;
    ''', (flashcard_id,))
    card = cursor.fetchone()
    cursor.close()
    return {'id': card[0], 'front_card': card[1], 'back_card': card[2]} if card else None


def update_flashcard(flashcard_id, front_card, back_card):
    cursor = connection.cursor()
    cursor.execute('''
    UPDATE user_flashcards SET front_card = %s, back_card = %s
    WHERE id = %s RETURNING id;
    ''', (front_card, back_card, flashcard_id))
    updated = cursor.fetchone()
    connection.commit()
    cursor.close()
    return updated is not None


def delete_flashcard(flashcard_id):
    cursor = connection.cursor()
    cursor.execute('''
    DELETE FROM user_flashcards WHERE id = %s RETURNING id
    ''', (flashcard_id,))
    deleted = cursor.fetchone()
    connection.commit()
    cursor.close()
    return deleted is not None
