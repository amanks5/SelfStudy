from database import *

# separate file to make app.py a little cleaner
def create_note(title, content):
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO user_notes (title, content)
    VALUES (%s, %s)
    RETURNING id''', (title, content))
    note_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    return note_id


def edit_note(note_id, title, content):
    cursor = connection.cursor()
    cursor.execute('''
    UPDATE user_notes SET title = %s, content = %s
    WHERE id = %s
    RETURNING id''', (title, content, note_id))
    updated = cursor.fetchone()
    connection.commit
    cursor.close()
    return updated is not None


def delete_note(note_id):
    cursor = connection.cursor()
    cursor.execute('''
    DELETE FROM user_notes WHERE id = %s 
    RETURNING id''', (note_id,))
    deleted = cursor.fetchone()
    connection.commit()
    cursor.close()
    return deleted is not None


def fetch_all_notes():
    cursor = connection.cursor()
    cursor.execute('''
    SELECT id, title, content FROM user_notes''')
    notes = cursor.fetchall()
    cursor.close()
    return [{'id': row[0], 'title': row[1], 'content': row[2]} for row in notes]


def fetch_note(note_id):
    cursor = connection.cursor()
    cursor.execute('''
    SELECT id, title, content FROM user_notes WHERE id = %s''', (note_id,))
    note = cursor.fetchone()
    cursor.close()
    return {'id': note[0], 'title': note[1], 'content': note[2]} if note else None
