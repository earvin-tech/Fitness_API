from init import db, ma

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    f_name = db.Column(db.String(100), nullable=False)
    l_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id","f_name", "l_name", "dob", "email")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
