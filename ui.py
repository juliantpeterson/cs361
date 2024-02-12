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
                roster_json = socket.recv_json()
                output_string_roster = "\n             PITCHERS\n\n"
                output_string_roster += "SELECT          JERSEY          NAME\n"
                select_number = 1

                # Find all pitchers
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

                # find all non-pitchers
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
                print(roster_json)

            elif user_input in ("2", "VIEW UPCOMING SCHEDULE"):
                # TODO: get data from website (need new microservice)
                print("schedule!")
                continue
            elif user_input in ("3", "VIEW RESULTS OF PREVIOUS 5 GAMES"):
                # TODO: get data from website (need new microservice)
                print("prev 5 games!")
                continue


Navigation.main_menu()
