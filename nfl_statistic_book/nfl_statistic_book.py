#Next Steps:
# - Get roster in a formatted kind of way
# - View players stats


from team import Team
import base64
import requests
import os
import sys


def get_credentials():
    """
    Gets username and password as credentials to acccess the API - Hidden ;)

    """
    with open('secret.txt') as f:
        lines = f.readlines()
        return lines


def generate_teams():
    """
    Accesses the API to get a team (City + Name) and pairs that with the team's
    abbreviation in a dictionary

    """
    try:
        response = requests.get(
            url='https://api.mysportsfeeds.com/v1.2/pull/nfl/2018-regular/'
                'conference_team_standings.json?teamstats=W,L,T,PF,PA',
            params={
            },
            headers={
                'Authorization': 'Basic ' + base64.b64encode
                ('{}:{}'.format(user_name,passw).encode('utf-8')).decode('ascii')
            }
        )
        data = response.json()
        for j in range(0, 2):
            for i in range(0, 16):
                team = (data['conferenceteamstandings']['conference'][j]
                ['teamentry'][i]['team']['City']) + ' '
                team += (data['conferenceteamstandings']['conference'][j]
                ['teamentry'][i]['team']['Name'])
                abbreviation = (data['conferenceteamstandings']['conference'][j]
                ['teamentry'][i]['team']['Abbreviation'])
                allTeams[team] = abbreviation

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def print_welcome(opening = True, team_selected = False):
    """"
    Prints the welcome when the program is first started, also gives user
    options at other times during execution

    Paramters
    ---------
    opening : bool
        whether or not the opening message should be displayed
    team_selected : bool
        whether or not a team has already been selected so that the option to
        stay with the current team is available

    """
    if opening:
        print('############ Welcome to the NFL Statistic Book ############ \n\n')
    if team_selected is True:
        print('(0) Stay with current team')

    print('(1) Search for a specific team')
    print('(2) Get a list of teams to choose from')
    print('(3) Quit')
    return get_selection()


def get_selection():
    """
    Gets user selection after input options displayed

    """
    choice = input('\nSelection: ')
    return choice


def exec_input(selection, current_team, to_clear = True, team_selected = False):
    """
    Gets input from user based on previous selection

    Parameters
    ----------
    selection : string
        input from user when given previous options
    created_team :

    """
    if selection is '1':
        if to_clear:
           clear()
           team_name = input('Please enter team name: ')
        else:
            team_name = input('\nPlease enter team name: ')
        if is_team(team_name):
            current_team = team_name
            create_team(get_abbreviation(team_name))

        else:
            exec_input('1', current_team, False)

    elif selection is '0' and team_selected is True:
        create_team(current_team)

    elif selection is '2':
        clear()
        print('Available teams: \n')
        print_teams()
        exec_input('1', current_team, to_clear=False)

    elif selection is '3':
        clear()
        sys.exit('Have a great day')

    else:
        exec_input(get_selection(), current_team)


def create_team(team_abbreviation):
    """
    Creates a team in the team class

    Paramters
    ---------
    team_abbreviation : string
        abbreviation for the team to locate it in API
    """
    t = Team(team_abbreviation)
    get_team_options(t)


def clear():
    """
    Clears window

    """
    os.system( 'clear' )


def print_teams():
    """
    Prints all teams available for user to choose from

    """
    count = 0
    team_string = ''
    for key in allTeams:
        count = count + 1
        team_string += key + ' ' * (25 - len(key))
        if count % 5 == 0:
            team_string += '\n'
    print(team_string)


def is_team(team_name):
    """
    Determines whether or not team entered by user is actually real

    Paramters
    ---------
    team_name : string
        name of team entered by user

    Notes
    -----
    User does not need to enter entire name for team, function is meant to
    recognize both cities and actual team names
    """
    for key in allTeams:
        if team_name.lower() in key.lower() and len(team_name) >= 4:
            return True
    return False


def get_abbreviation(team_name):
    """
    Gets abbreviation for corresponding team name

    Parameters
    ----------
    team_name : string
        team_name searched for corresponding abbreviation

    """
    for key in allTeams:
        if team_name.lower() in key.lower() and len(team_name) >= 4:
            return allTeams[key]


def get_team_options(team, printWelcome=True):
    """
    Display user options once a team has been selected

    Parameters
    ----------
    team : Team
        Team object that is created once verified to be real, all options given
        correspond to specific team

    """
    clear()
    if printWelcome:
        print(f'TEAM SELECTED: {team.get_name()} \n\n(1) Get 2018-2019 Schedule\n(2)'
          f' Get Roster\n(3) Search for player\n(4) Choose another team ')
    choice = input('\n Selection: ')

    if choice is '4':
        clear()
        print('\n')
        exec_input('1', current_team=team.name)

    elif choice is '1':
        clear()
        team.get_schedule(user_name, passw)
        print('\n')
        exec_input(print_welcome(opening=False, team_selected=True),
                   current_team=team.name, to_clear=True, team_selected=True)

    elif choice is '2':
        clear()
        team.get_roster(user_name, passw)
        print('\n')
        exec_input(print_welcome(opening=False, team_selected=True),
                   current_team=team.name, to_clear=True, team_selected=True)

    elif choice is '3':
        clear()
        player_name = input("Please enter <first_name> <last_name>: ")
        try:
            first_name = player_name.split()[0]
            last_name = player_name.split()[1]
            team.get_player_stats(first_name, last_name, user_name, passw)
        except:
            print("Not valid player name!")
            get_team_options(team)
    else:
        print("invalid input. ")
        get_team_options(team, False)


if __name__ == '__main__':
    user_name = get_credentials()[0].strip()
    passw = get_credentials()[1].strip()
    allTeams = {}
    team_selected = 'Bengals'
    generate_teams()
    selection = print_welcome()
    exec_input(selection, team_selected, to_clear=False)

