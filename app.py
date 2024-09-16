from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from llm_utils import generate_response  # Import the function from llm_utils.py
import sqlite3

app = Flask(__name__)
swagger = Swagger(app)

def fetch_sales_data(query):
    # Function to fetch sales data from the database
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/chat', methods=['POST'])
@swag_from({
    'tags': ['Chat'],
    'description': 'Chat with the chatbot',
    'parameters': [
        {
            'name': 'user_input',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'query': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Chatbot response',
            'schema': {
                'type': 'object',
                'properties': {
                    'response': {'type': 'string'}
                }
            }
        }
    }
})
def chat():
    user_query = request.json.get('query')
    llm_response = generate_response(user_query)

    # Example logic to augment the LLM's response with database data
    if "top-selling products this month" in user_query:
        query = '''
        SELECT product_name, SUM(sale_amount) AS total_sales
        FROM sales
        WHERE sale_date BETWEEN date('now', 'start of month') AND date('now')
        GROUP BY product_name
        ORDER BY total_sales DESC
        LIMIT 5
        '''
        sales_data = fetch_sales_data(query)
        sales_info = "\n".join([f"{row[0]}: ${row[1]:.2f}" for row in sales_data])
        response = f"{llm_response}\n\nTop-selling products this month:\n{sales_info}"
    else:
        response = llm_response

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)

