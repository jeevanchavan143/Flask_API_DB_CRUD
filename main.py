from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Adjust your MySQL connection URI here
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@hostname/database_name'
db = SQLAlchemy(app)

@app.route('/read_table/<schemaname>/<table_name>', methods=['GET'])
def read_table(table_name):
    # Execute SQL query to select all data from the table
    result = db.engine.execute(f"SELECT * FROM {schema_name}.{table_name}").fetchall()

    # Convert result into a list of dictionaries
    table_data = [dict(row) for row in result]

    return jsonify(table_data)

@app.route('/create_record', methods=['POST'])
def create_record():
    request_data = request.get_json()

    if not isinstance(request_data, dict) or 'table_name' not in request_data or 'data' not in request_data:
        return jsonify({'error': 'Invalid request. Please provide table_name and data in the request body.'}), 400

    table_name = request_data['table_name']
    data = request_data['data']

    if isinstance(data, list):
        for record in data:
            if not isinstance(record, dict):
                return jsonify({'error': 'Invalid request. Data should be a dictionary or a list of dictionaries.'}), 400
    else:
        data = [data]  # Convert single record to list of records

    try:
        cnx = connect_to_db()
        cur = cnx.cursor()

        for record in data:
            columns = ', '.join(record.keys())
            placeholders = ', '.join(['%s'] * len(record))
            values = tuple(record.values())

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cur.execute(query, values)

        cnx.commit()
        cur.close()
        cnx.close()

        return jsonify({'message': f'{len(data)} records inserted successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
