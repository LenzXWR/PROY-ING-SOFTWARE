from base import db

class ResponsableEstablecimiento(db.Model):
    __tablename__ = 'RESPONSABLE_DE_ESTABLECIMIENTO'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class ActividadTuristica(db.Model):
    __tablename__ = 'ACTIVIDAD_TURISTICA'
    id = db.Column(db.Integer, primary_key=True)
    responsable_id = db.Column(db.Integer, db.ForeignKey('RESPONSABLE_DE_ESTABLECIMIENTO.id'))
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.Date, nullable=True)
    responsable = db.relationship('ResponsableEstablecimiento', backref='actividades')
