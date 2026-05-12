import email

from chapter06.model import engine, Users, Faces, Checkin
from sqlmodel import Session, text, select, join

with Session(engine) as session:
    user = select(Users, Faces.facecode).join(Faces, isouter=True)
    result = session.execute(user).all()
    print(result)