from datetime import datetime
import requests
from bs4 import BeautifulSoup
import credentials

def login_moodle(username, password):
    login_url = "https://moodle.sptech.school/login/index.php"
    session = requests.Session()
    
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    logintoken = soup.find('input', {'name': 'logintoken'}).get('value')
    
    login_data = {
        'anchor': '',
        'logintoken': logintoken,
        'username': username,
        'password': password
    }
    response = session.post(login_url, data=login_data)
    
    if "Invalid login" in response.text:
        raise ValueError("Invalid login credentials")
    return session


def get_activities_today(session):
    
    today = datetime.today().day
    
    calendar_url = "https://moodle.sptech.school/calendar/view.php?view=month"
    response = session.get(calendar_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    a_tag = soup.find('a', {'data-day': str(today)})
    div_parent = a_tag.parent
    elementos_eventos = div_parent.find_all('span', {'class': 'eventname'})
    events_list = []
    for evento in elementos_eventos:
        events_list.append(evento.text)

    for i in range(len(events_list)):
        events_list[i] = events_list[i][:-31]

    return events_list


# Exemplo
username = credentials.USERNAME
password = credentials.PASSWORD
session = login_moodle(username, password)
activities = get_activities_today(session)
if activities:
    print("Atenção!! As seguintes atividades serão fechadas hoje:")
    for activity in activities:
        print(activity)
else:
    print("Nenhuma atividade será fechada hoje :)")
