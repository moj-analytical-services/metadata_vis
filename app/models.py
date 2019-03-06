from main import db

class Database(db.Model):
    __tablename__ = "databases"
    db_id = db.Column(db.Integer, primary_key=True)
    db_name = db.Column(db.String(64), index=True, unique=True)
    db_desc = db.Column(db.String(120), index=True)

    tables = db.relationship('Table', backref='databases', lazy='dynamic')

    def __repr__(self):
        return '<Name {}>'.format(self.name)

class Table(db.Model):
    __tablename__ = "tables"
    tbl_id = db.Column(db.Integer, primary_key=True)
    tbl_name = db.Column(db.String(64), index=True, unique=True)
    tbl_desc = db.Column(db.String(120), index=True)
    db_id = db.Column(db.Integer, db.ForeignKey('databases.db_id'))

    fields = db.relationship('Column', backref='tables', lazy='dynamic')

    def __repr__(self):
        return '<Table name {}>'.format(self.tbl_name)

class Column(db.Model):
    __tablename__ = "columns"
    clm_id = db.Column(db.Integer, primary_key=True)
    clm_name = db.Column(db.String(64), index=True)
    clm_desc = db.Column(db.String(120), index=True)
    tbl_id = db.Column(db.Integer, db.ForeignKey('tables.tbl_id'))

    def __repr__(self):
        return '<Column name {}>'.format(self.name)