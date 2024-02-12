#------------------------------------------------------------
# Julian Peterson
# Final Project
# Change Log:
# January 21, 2024 - created script
#------------------------------------------------------------

from constants import *
import zmq

context = zmq.Context()




class Navigation:

    @staticmethod
    def main_menu():
        while True:
            print(MAIN_MENU)
            main_input = input().upper()
            if main_input in ('2', "EXIT"):
                quit()
            elif main_input in ('1', 'SELECT', 'SELECT A TEAM'):
                Navigation.select_team()
            else:
                print("Please try again")

    @staticmethod
    def select_team():
        while True:
            print(TEAMS)
            select_teams_input = input().upper()
            if select_teams_input == "HELP":
                print(SELECT_TEAM_HELP)
            elif select_teams_input in ("MAIN", "BACK"):
                return
            else:
                # connect to format_team_name socket
                socket = context.socket(zmq.REQ)
                socket.connect('tcp://localhost:5555')
                socket.send_string(select_teams_input)

                clean_team = str(socket.recv())[2:-1]
                if clean_team == "Error":
                    print("Input not understood. Please try again.")
                else:
                    return_value = Navigation.team_home(clean_team)
                    if return_value == "MAIN":
                        return
                    elif return_value == "BACK":
                        continue

    @staticmethod
    def team_home(team_name):
        if team_name == "NEW YORK YANKEES":
            print(YANKEES_LOGO)
        print(f"WELCOME TO THE HOME PAGE OF THE {team_name}!")
        print("""
Select an option:
1. View current 40-man roster (may need to scroll up to see the entire roster)
2. View upcoming schedule
3. View results of previous 5 games

BACK to select a different team
MAIN to return to main menu
""")
        while True:
            user_input = input().upper()
            if user_input == "BACK":
                return "BACK"
            elif user_input == "MAIN":
                return 'MAIN'
            elif user_input in ("1", "VIEW CURRENT 40-MAN ROSTER"):
                print("You selected view Current 40-man roster")
                print("")
                # connect to request_40_man socket
                socket = context.socket(zmq.REQ)
                socket.connect('tcp://localhost:4040')
                socket.send_string(team_name)

                # payload
                roster_json = socket.recv_json()

                # start formatting output string
                output_string_roster = "\n             PITCHERS\n\n"
                output_string_roster += "SELECT          JERSEY          NAME\n"
                select_number = 1

                # Find all pitchers, add to output string
                for player in roster_json:

                    if player['primary_position'] == '1':

                        buffer_1 = ""
                        if select_number < 10:
                            buffer_1 = " "
                        if len(player['jersey_number']) == 0:
                            buffer_2 = "  "
                        elif len(player['jersey_number']) == 1:
                            buffer_2 = " "
                        else:
                            buffer_2 = ""

                        output_string_roster += \
                            f"""{select_number}{buffer_1}              {player['jersey_number']}{buffer_2}              {player['name_display_first_last']}\n"""
                        select_number += 1

                # find all non-pitchers, add to output string
                output_string_roster += "\n\n\n             POSITION PLAYERS\n\n"
                output_string_roster += "SELECT          JERSEY          NAME\n"
                for player in roster_json:
                    if player['primary_position'] != '1':

                        buffer_1 = ""
                        if select_number < 10:
                            buffer_1 = " "
                        if len(player['jersey_number']) == 0:
                            buffer_2 = "  "
                        elif len(player['jersey_number']) == 1:
                            buffer_2 = " "
                        else:
                            buffer_2 = ""

                        output_string_roster += \
                            f"""{select_number}{buffer_1}              {player['jersey_number']}{buffer_2}              {player['name_display_first_last']}\n"""
                        select_number += 1

                print(output_string_roster)
                #print(roster_json)
                return_value = Navigation.select_player(roster_json=roster_json)
                if return_value == "BACK":
                    return "BACK"

            elif user_input in ("2", "VIEW UPCOMING SCHEDULE"):
                # TODO: get data from website (need new microservice)
                print("schedule!")
                continue
            elif user_input in ("3", "VIEW RESULTS OF PREVIOUS 5 GAMES"):
                # TODO: get data from website (need new microservice)
                print("prev 5 games!")
                continue

    @staticmethod
    def select_player(roster_json):
        while True:
            print('\nEnter a player\'s SELECT number to see more statistics about that player')
            print("BACK to go back. MAIN for main.")
            select_player_number = input().upper()
            if select_player_number == "BACK":
                return "BACK"
            elif select_player_number == "MAIN":
                return "MAIN"
            else:
                select_player_number = int(select_player_number)

            select_number = 1

            # iterate through pitchers
            for player in roster_json:
                if player['primary_position'] == '1':
                    if select_player_number == select_number:
                        for item in player:
                            print(f"{item}: {player[item]}")
                    select_number += 1

            # iterate through position players
            for player in roster_json:
                if player['primary_position'] != '1':
                    if select_player_number == select_number:
                        for item in player:
                            print(f"{item}: {player[item]}")
                    select_number += 1

            #socket = context.socket(zmq.REQ)
            #socket.connect('tcp://localhost:7843')
            #socket.send_string(player_id)

            # payload
            #stats_json = socket.recv_json()
            #print(stats_json)





Navigation.main_menu()
