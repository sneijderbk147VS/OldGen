import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Conexión con la base de datos PostgreSQL en Render
db_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo del Miembro
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default="Miembro")
    tier = db.Column(db.String(50), default="Netherite")
    country = db.Column(db.String(50), default="Perú")
    join_date = db.Column(db.String(20), default="")
    description = db.Column(db.Text, default="")

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# API: Obtener miembros
@app.route('/api/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'role': m.role,
        'tier': m.tier,
        'country': m.country,
        'joinDate': m.join_date,
        'description': m.description
    } for m in members])

# API: Agregar miembro
@app.route('/api/members', methods=['POST'])
def add_member():
    data = request.json
    new_member = Member(
        name=data.get('name'),
        role=data.get('role', 'Miembro'),
        tier=data.get('tier', 'Netherite'),
        country=data.get('country', 'Perú'),
        join_date=data.get('joinDate', ''),
        description=data.get('description', '')
    )
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Guardado con éxito', 'id': new_member.id}), 201

# API: Eliminar miembro
@app.route('/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = Member.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Eliminado'})
    return jsonify({'error': 'No encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)