from app.models.user import User

def create_user(db, external_id: str) -> User:
    user = User(external_id=external_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_or_create_user_by_external_id(db, external_id: str) -> User:
    user = db.query(User).filter(User.external_id == external_id).first()
    if user:
        return user
    return create_user(db, external_id)