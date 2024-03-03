from riddle_solvers import riddle_solvers
import requests
import numpy as np
import json

api_base_url = "http://3.70.97.142:5000"

team_id = 'ds42W0d'


# from LSBSteg import encode


def init_fox(team_id, use_cache):
    '''
    In this function you need to hit to the endpoint to start the game as a fox with your team id.
    If a successful response is returned, you will receive back the message that you can break into chunks
    and the carrier image that you will encode the chunk in it.
    '''

    cache_file = "game.json"

    if use_cache:
        data = None
        with open(cache_file, 'r') as f:
            data = json.loads(f.read())
        return data

    # Define the endpoint URL and team ID
    endpoint = "http://3.70.97.142:5000/fox/start"

    # Construct the request body
    payload = {
        "teamId": team_id
    }

    # Send the POST request
    response = requests.post(endpoint, json=payload)

    # Check if the request was successful
    if response.status_code == 200 or response.status_code == 201:
        # Extract data from the response
        data = response.json()
        # secret_message = data["msg"]
        # carrier_image = data["carrier_image"]
        with open(cache_file, "w") as f:
            json.dump(data, f)
        # Convert carrier image to NumPy array if needed
        # numpy_carrier_image = np.array(carrier_image)

        return data
    else:
        print(f"Request failed with status code {response.status_code}")


def generate_message_array(message, image_carrier):
    '''
    In this function you will need to create your own startegy. That includes:
        1. How you are going to split the real message into chunkcs
        2. Include any fake chunks
        3. Decide what 3 chuncks you will send in each turn in the 3 channels & what is their entities (F,R,E)
        4. Encode each chunck in the image carrier  
    '''
    pass


def get_riddle(team_id, riddle_id, use_cache):
    '''
    In this function you will hit the api end point that requests the type of riddle you want to solve.
    use the riddle id to request the specific riddle.
    Note that: 
        1. Once you requested a riddle you cannot request it again per game. 
        2. Each riddle has a timeout if you didnot reply with your answer it will be considered as a wrong answer.
        3. You cannot request several riddles at a time, so requesting a new riddle without answering the old one
          will allow you to answer only the new riddle and you will have no access again to the old riddle. 
    '''

    cache_file = "test_case.json"

    if use_cache:
        data = None
        with open(cache_file, 'r') as f:
            data = json.loads(f.read())
        return data

    endpoint = "http://3.70.97.142:5000/fox/get-riddle"
    payload = {
        "teamId": team_id,
        "riddleId": riddle_id
    }

    # Send the POST request
    response = requests.post(endpoint, json=payload)

    # Check if the request was successful
    if response.status_code == 200 or response.status_code == 201:
        # Extract data from the response
        data = response.json()
        with open(cache_file, "w") as f:
            json.dump(data, f)
        return data
    else:
        print("Error while getting a riddle:", response.status_code)


def solve_riddle(team_id, solution, use_cache):
    '''
    In this function you will solve the riddle that you have requested. 
    You will hit the API end point that submits your answer.
    Use te riddle_solvers.py to implement the logic of each riddle.
    '''
    
    cache_file = "solve_riddle.json"
    
    if use_cache:
        data = None
        with open(cache_file, 'r') as f:
            data = json.loads(f.read())
        return data

    endpoint = "http://3.70.97.142:5000/fox/solve-riddle"

    # Construct the request body
    payload = {
        "teamId": team_id,
        "solution": str(solution)
    }

    # Send the POST request
    response = requests.post(endpoint, json=payload)

    # Check if the request was successful
    if response.status_code == 200 or response.status_code == 201:
        # Extract data from the response
        data = response.json()
        with open(cache_file, "w") as f:
            json.dump(data, f)
        return data
    else:
        print("Error:", response.status_code)


def send_message(team_id, messages, message_entities=['F', 'E', 'R']):
    '''
    Use this function to call the api end point to send one chunk of the message. 
    You will need to send the message (images) in each of the 3 channels along with their entites.
    Refer to the API documentation to know more about what needs to be send in this api call. 
    '''
    pass


def end_fox(team_id):
    '''
    Use this function to call the api end point of ending the fox game.
    Note that:
    1. Not calling this fucntion will cost you in the scoring function
    2. Calling it without sending all the real messages will also affect your scoring fucntion
      (Like failing to submit the entire message within the timelimit of the game).
    '''
    pass


def submit_fox_attempt(team_id):
    '''
     Call this function to start playing as a fox. 
     You should submit with your own team id that was sent to you in the email.
     Remeber you have up to 15 Submissions as a Fox In phase1.
     In this function you should:
        1. Initialize the game as fox 
        2. Solve riddles 
        3. Make your own Strategy of sending the messages in the 3 channels
        4. Make your own Strategy of splitting the message into chunks
        5. Send the messages 
        6. End the Game
    Note that:
        1. You HAVE to start and end the game on your own. The time between the starting and ending the game is taken into the scoring function
        2. You can send in the 3 channels any combination of F(Fake),R(Real),E(Empty) under the conditions that
            2.a. At most one real message is sent
            2.b. You cannot send 3 E(Empty) messages, there should be atleast R(Real)/F(Fake)
        3. Refer To the documentation to know more about the API handling 
    '''
    init_fox(team_id, True)
    test_case = get_riddle(team_id, "problem_solving_easy", True)['test_case']
    solution = riddle_solvers['problem_solving_easy'](test_case)
    solve_riddle(team_id, solution, False)


submit_fox_attempt(team_id)
