from main import db

class Database(db.Model):
    __tablename__ = "databases"
    db_id = db.Column(db.Integer, primary_key=True)
    db_name = db.Column(db.String(64), index=True, unique=True)
    db_desc = db.Column(db.String(120), index=True)
    db_loc = db.Column(db.String(120))
    db_s3bucket = db.Column(db.String(120))
    db_metaloc = db.Column(db.String(120))

    tables = db.relationship('Table', backref='databases', lazy='dynamic')
    enums = db.relationship('AccessRight', backref='databases', lazy='dynamic')

    def __repr__(self):
        return '<Name {}>'.format(self.db_name)

class Table(db.Model):
    __tablename__ = "tables"
    tbl_id = db.Column(db.Integer, primary_key=True)
    tbl_name = db.Column(db.String(64), index=True)
    tbl_desc = db.Column(db.String(120), index=True)
    tbl_loc = db.Column(db.String(120))
    tbl_metaloc = db.Column(db.String(120))
    tbl_datatype = db.Column(db.String(120))
    tbl_partitions = db.Column(db.String(120))

    db_id = db.Column(db.Integer, db.ForeignKey('databases.db_id'))

    columns = db.relationship('Column', backref='tables', lazy='dynamic')

    def __repr__(self):
        return '<Table name {}>'.format(self.tbl_name)

class Column(db.Model):
    __tablename__ = "columns"
    clm_id = db.Column(db.Integer, primary_key=True)
    clm_name = db.Column(db.String(64), index=True)
    clm_desc = db.Column(db.String(120), index=True)
    clm_pattern = db.Column(db.String(120))
    clm_enum = db.Column(db.String(120))
    clm_datatype = db.Column(db.String(120))
    clm_is_partition = db.Column(db.Boolean)


    tbl_id = db.Column(db.Integer, db.ForeignKey('tables.tbl_id'))

    enums = db.relationship('Enum', backref='columns', lazy='dynamic')

    def __repr__(self):
        return '<Column name {}>'.format(self.clm_name)


class Enum(db.Model):
    __tablename__ = "enums"
    enum_id = db.Column(db.Integer, primary_key=True)
    enum_value = db.Column(db.String(120))

    clm_id = db.Column(db.Integer, db.ForeignKey('columns.clm_id'))

    def __repr__(self):
        return '<Enum value {}>'.format(self.enum_value)

class AccessRight(db.Model):
    __tablename__ = "accessrights"
    ar_id = db.Column(db.Integer, primary_key=True)
    ar_s3bucket = db.Column(db.String(120))
    ar_git_username = db.Column(db.String(120))
    ar_email = db.Column(db.String(120))
    ar_is_admin = db.Column(db.Boolean)

    db_id = db.Column(db.Integer, db.ForeignKey('databases.db_id'))

    def __repr__(self):
        return '<Access rights value {}>'.format(self.ar_s3bucket)
