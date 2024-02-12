import requests
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:4040")

while True:
    # wait for message from client
    team_string = str(socket.recv()).upper()[2:-1]

    # format name for searching in list
    # cover edge cases for teams with two-word names:
    if team_string == 'TORONTO BLUE JAYS':
        name = "Blue Jays"
    elif team_string == 'CHICAGO WHITE SOX':
        name = 'White Sox'
    elif team_string == 'BOSTON RED SOX':
        name = 'Red Sox'
    else:
        name = team_string.split()[-1].lower().capitalize()

    # create url and GET request to search for team number
    host = "http://lookup-service-prod.mlb.com"
    path = "/json/named.team_all_season.bam?sport_code='mlb'&season='2024'"
    url = host + path
    response = requests.get(url)
    teams = response.json()['team_all_season']['queryResults']['row']

    for team in teams:
        if name == team['name']:
            team_id = team['team_id']

    # create url to team roster
    path = f"/json/named.roster_40.bam?team_id='{team_id}'"
    url = host + path


    # A GET request to the API to get roster
    response = requests.get(url)
    #print(response)
    #print(response.content)

    # send the response json
    response_json = response.json()
    players = response_json['roster_40']['queryResults']['row']
    socket.send_json(players)


