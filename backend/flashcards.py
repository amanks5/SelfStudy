from database import *

def create_flashcard(app, owner, front, back):
    with app.app_context():
        card = UserFlashCard(
            owner=owner,
            front=front,
            back=back
        )
        try:
            db.session.add(card)
            db.session.commit()
        except:
            traceback.print_exc()
            return None
        return card.uuid

def fetch_all_flashcards(app, owner):
    with app.app_context():
        try:
            return [{'id': card.uuid, 'front_card': card.front, 'back_card': card.back}
                for card in db.session.execute(db.select(UserFlashCard).where(UserFlashCard.owner == owner).order_by(UserFlashCard.updated_at)).scalars()]
        except:
            traceback.print_exc()
            return None

def fetch_flashcard(app, uuid, owner):
    with app.app_context():
        try:
            card = db.session.execute(db.select(UserFlashCard).where(UserFlashCard.uuid == uuid and UserFlashCard.owner == owner)).scalar_one()
            return {'id': card.uuid, 'front_card': card.front, 'back_card': card.back} if card else None
        except:
            traceback.print_exc()
            return None
        
def update_flashcard(app, uuid, owner, front, back):
    with app.app_context():
        try:
            res = db.session.execute(db.update(UserFlashCard).where(UserFlashCard.uuid == uuid and UserFlashCard.owner == owner).values(
                front=front,
                back=back,
                updated_at=func.now()
            ))
            db.session.commit()
            return res.rowcount > 0
        except:
            traceback.print_exc()
            return False

def delete_flashcard(app, uuid, owner):
    with app.app_context():
        try:
            res = db.session.execute(db.delete(UserFlashCard).where(UserFlashCard.uuid == uuid and UserFlashCard.owner == owner))
            db.session.commit()
            return res.rowcount > 0
        except:
            traceback.print_exc()
            return False
