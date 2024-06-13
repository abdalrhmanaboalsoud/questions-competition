from http.server import BaseHTTPRequestHandler
import requests
from urllib import parse

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse the URL and query string
        s = self.path
        url_component = parse.urlsplit(s)
        query_string_list = parse.parse_qsl(url_component.query)
        my_dic = dict(query_string_list)
        
        # Get the category from query parameters or default to '9' (General Knowledge)
        category = int(my_dic.get('category', '9'))

        # Get the amount of questions to retrieve, default to 10
        amount = my_dic.get('amount', '10')
        if not amount.isdigit() or int(amount) > 50:
            amount = '50'  # Default to 50 if not a valid number or if more than 50 is requested
        
        valid_category_range = range(9, 33)  # Categories 9 to 32 inclusive

        if category not in valid_category_range:
            # If the category is out of the valid range, respond with an error
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            error_message = "Invalid category. Please choose a category ID between 9 and 32."
            self.wfile.write(error_message.encode())
            return

        # Making the API request with the category and amount parameters
        url = f'https://opentdb.com/api.php?amount={amount}&category={category}'
        
        req = requests.get(url)
        
        if req.status_code == 200:
            # Process the successful API response
            rec_question = req.json()

            # Prepare the output in plain text format
            output = ""
            counter = 0
            for item in rec_question.get("results", []):
                question = item["question"]
                correct_answer = item["correct_answer"]
                category_name = item["category"]
                counter += 1
                output += f"Question {counter}: {question}\nAnswer: {correct_answer}\nCategory: {category_name}\n\n"

            # Send HTTP status 200 (OK)
            self.send_response(200)

            # Set the Content-type to 'text/plain' to match the output format
            self.send_header("Content-type", "text/plain")

            # End headers
            self.end_headers()

            # Write the output to the response
            self.wfile.write(output.encode())
        
        else:
            # Handle the case where the API request fails
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            error_message = f"Failed to retrieve data: Status Code {req.status_code}"
            self.wfile.write(error_message.encode())
