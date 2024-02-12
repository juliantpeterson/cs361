import requests
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:7843")

while True:
    # wait for message from client
    player_id_string = str(socket.recv()).upper()[2:-1]
    print(player_id_string)

    # create url and GET request to search for team number
    host = "http://lookup-service-prod.mlb.com"
    path = f"/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='2023'&player_id='{player_id_string}'"
    url = host + path
    print(url)
    response = requests.get(url)
    print(response)
    print(response.json())
    socket.send_json(response.json())




