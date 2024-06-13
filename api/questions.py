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
        

        # Default amount of questions to 20 or get from the query, capped at 50
        max_questions = 50
        amount = my_dic.get('amount', '20')  # Get 'amount' from query or default to '20'
        
        if not amount.isdigit():
            amount = 20  # If the amount isn't a valid integer, default to 20
        else:
            amount = int(amount)
        
        if amount > max_questions:
            amount = max_questions  # Cap the amount to 50

        # Making the API request with the calculated amount
        url = f'https://opentdb.com/api.php?amount={amount}'
        
        req = requests.get(url)
        
        if req.status_code == 200:
            # Process the successful API response
            rec_question = req.json()

            # Prepare the output in plain text format
            output = ""
            counter = 0
            for item in rec_question["results"]:
                question = item["question"]
                correct_answer = item["correct_answer"]
                category = item["category"]
                counter +=1
                output += f"Question {counter}: {question}\nAnswer: {correct_answer}\nCategory: {category}\n\n\n\n"

            # Send HTTP status 200 (OK)
            self.send_response(200)

            # Set the Content-type to 'text/plain' to match the output format
            self.send_header("Content-type", "text/plain")

            # End headers
            self.end_headers()

            # Write the output to the response
            self.wfile.write(output.encode())
    

