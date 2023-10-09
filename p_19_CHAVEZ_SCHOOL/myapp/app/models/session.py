from app.database import db

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    #session_data = db.Column(db.String, nullable=True)
    canvas_data = db.Column(db.JSON, nullable=True)  # the Excalidraw canvas data
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    tutor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tutor = relationship('User', foreign_keys=[tutor_id], uselist = False)

    tutee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tutor = relationship('User', foreign_keys=[tutee_id], uselist = False)

#without the end_datetime
#class Session(db.Model):
#    __tablename__ = 'sessions'
#    id = db.Column(db.Integer, primary_key=True)
#    start_datetime = db.Column(db.DateTime, nullable=False)
#    canvas_data = db.Column(db.JSON, nullable=True)  # the Excalidraw canvas data
#    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
