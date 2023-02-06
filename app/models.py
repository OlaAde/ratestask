from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    parent_slug = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Port %r>' % self.name


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orig_code = db.Column(db.String(80), nullable=False)
    dest_code = db.Column(db.String(80), nullable=False)
    day = db.Column(db.Date(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return '<Price %r>' % self.title


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    parent_slug = db.Column(db.String(80))

    def __repr__(self):
        return '<Region %r>' % self.title
