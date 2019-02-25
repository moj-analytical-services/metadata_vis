from app import db

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_name = db.Column(db.String(64), index=True, unique=True)
    db_desc = db.Column(db.String(120), index=True, unique=True)

    tables = db.relationship('Table', backref='database', lazy='dynamic')

    def __repr__(self):
        return '<Name {}>'.format(self.name)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tbl_name = db.Column(db.String(64), index=True, unique=True)
    tbl_desc = db.Column(db.String(120), index=True, unique=True)
    database_id = db.Column(db.Integer, db.ForeignKey('database.id'))

    fields = db.relationship('Column', backref='table', lazy='dynamic')

    def __repr__(self):
        return '<Table name {}>'.format(self.tbl_name)

class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clm_name = db.Column(db.String(64), index=True)
    clm_desc = db.Column(db.String(120), index=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))

    def __repr__(self):
        return '<Column name {}>'.format(self.name)