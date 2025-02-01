from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/spareorders'  # Update with your DB credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class DummyTest(db.Model):
    __tablename__ = 'api'
    Sku = db.Column(db.Text, primary_key=True)
    Brand = db.Column(db.Text)
    Name = db.Column(db.Text)
    Descrption = db.Column(db.Text)
    MRP = db.Column(db.Text)
    Make = db.Column(db.Text)
    Model = db.Column(db.Text)
    Year = db.Column(db.Text)
    Engine = db.Column(db.Text)
    row_key = db.Column(db.Text)
    variant_key = db.Column(db.Text)
@app.route('/part_name1', methods=['POST'])
def get_part_name():
    data = request.get_json()
    if not data or 'Brand' not in data:
        return jsonify({"error": "Missing 'Brand' in request body"}), 400
    brand = data['Brand']
    results = DummyTest.query.filter(func.trim(DummyTest.Brand) == brand).all()
    if not results:
        return jsonify({"message": "No data found"}), 404
    response = [
        {
            "Sku": result.Sku,
            "Name": result.Name,
            "Brand": result.Brand,
            "Descrption": result.Descrption,
            "MRP": result.MRP,
            "Make": result.Make,
            "Model": result.Model,
            "Year": result.Year,
            "Engine": result.Engine,
            "row_key": result.row_key,
            "variant_key": result.variant_key
        }
        for result in results
    ]
    return jsonify(response), 200
@app.route('/filter_by_brand', methods=['POST'])
def filter_by_brand():
    data = request.get_json()
    if not data or 'Brand' not in data:
        return jsonify({"error": "Missing 'Brand' in request body"}), 400

    brand = data['Brand']

    try:
        results = DummyTest.query.filter(DummyTest.Brand.ilike(f"%{brand}%")).all()  # Case-insensitive match
        if not results:
            return jsonify({"message": "No data found"}), 404
        response = [
            {
                "Sku": result.Sku,
                "Name": result.Name,
                "Brand": result.Brand,
                "Descrption": result.Descrption,
                "MRP": result.MRP,
                "Make": result.Make,
                "Model": result.Model,
                "Year": result.Year,
                "Engine": result.Engine,
                "row_key": result.row_key,
                "variant_key": result.variant_key
            }
            for result in results
        ]
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/part_name', methods=['PUT'])
def insert_part_name():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        new_entry = DummyTest(
            Sku=data.get('Sku'),
            Brand=data.get('Brand'),
            Name=data.get('Name'),
            Descrption=data.get('Descrption'),
            MRP=data.get('MRP'),
            Make=data.get('Make'),
            Model=data.get('Model'),
            Year=data.get('Year'),
            Engine=data.get('Engine'),
            row_key=data.get('row_key'),
            variant_key=data.get('variant_key')
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5020)
