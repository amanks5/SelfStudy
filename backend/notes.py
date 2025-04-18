from database import *
import traceback

def create_note(app, owner, title, content):
    with app.app_context():
        note = UserNote(
            owner=owner,
            title=title,
            content=content
        )
        try:
            db.session.add(note)
            db.session.commit()
        except:
            traceback.print_exc()
            return None
        return note.uuid

def fetch_all_notes(app, owner):
    with app.app_context():
        try:
            return [{'id': note.uuid, 'title': note.title, 'content': note.content}
                for note in db.session.execute(db.select(UserNote).where(UserNote.owner == owner).order_by(UserNote.updated_at)).scalars()]
        except:
            traceback.print_exc()
            return None

def fetch_note(app, uuid, owner):
    with app.app_context():
        try:
            note = db.session.execute(db.select(UserNote).where(UserNote.uuid == uuid and UserNote.owner == owner)).scalar_one()
            return {'id': note.uuid, 'title': note.title, 'content': note.content} if note else None
        except:
            traceback.print_exc()
            return None

def edit_note(app, uuid, owner, title, content):
    with app.app_context():
        try:
            res = db.session.execute(db.update(UserNote).where(UserNote.uuid == uuid and UserNote.owner == owner).values(
                title=title,
                content=content,
                updated_at=func.now()
            ))
            db.session.commit()
            return res.rowcount > 0
        except:
            traceback.print_exc()
            return False

def delete_note(app, uuid, owner):
    with app.app_context():
        try:
            res = db.session.execute(db.delete(UserNote).where(UserNote.uuid == uuid and UserNote.owner == owner))
            db.session.commit()
            return res.rowcount > 0
        except:
            traceback.print_exc()
            return False
