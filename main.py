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

if __name__ == '__main__':
    app.run(debug=True)
