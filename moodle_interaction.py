from datetime import datetime
import requests
from bs4 import BeautifulSoup
import credentials
from days import day


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


def get_activities(session, dayParam = day.HOJE):
    calendar_url = "https://moodle.sptech.school/calendar/view.php?view=upcoming"
    response = session.get(calendar_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    events_list = []
    # a_tag = soup.find('div', {'data-day': str(day)}, string=day)
    elementos_eventos = soup.find_all('div', {'data-type': 'event'})
    for elemento in elementos_eventos:
        # print(elemento.prettify())
        description_element = elemento.find('div', class_={'description', 'card-body'})
        rows_inside_description = description_element.find_all('div', class_="row")
        last_row = rows_inside_description[-1]
        last_column = last_row.find_all('div')[-1]
        course = last_column.find('a').text[8:-7]
        if (elemento.find('a', string='Hoje') and dayParam == day.HOJE) or (elemento.find('a', string='Amanhã') and dayParam == day.AMANHA):
            activity_name = elemento.find('h3', class_={'name'}).text
            if activity_name.endswith(" está marcado(a) para esta data"):
                activity_name = activity_name[:-31]
            date = elemento.find('div', class_={'col-11'})
            events_list.append({"activity": activity_name, "course": course, "date": date.text})
            
    return events_list

def get_all_activities(session):
    calendar_url = "https://moodle.sptech.school/calendar/view.php?view=upcoming"
    response = session.get(calendar_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    events_list = []
    # a_tag = soup.find('div', {'data-day': str(day)}, string=day)
    elementos_eventos = soup.find_all('div', {'data-type': 'event'})
    for elemento in elementos_eventos:
        # print(elemento.prettify())
        description_element = elemento.find('div', class_={'description', 'card-body'})
        rows_inside_description = description_element.find_all('div', class_="row")
        last_row = rows_inside_description[-1]
        last_column = last_row.find_all('div')[-1]

        course = last_column.find('a').text[8:-7]
        activity_name = elemento.find('h3', class_={'name'}).text
        if activity_name.endswith(" está marcado(a) para esta data"):
            activity_name = activity_name[:-31]

        date = elemento.find('div', class_={'col-11'})
        events_list.append({"activity": activity_name, "course": course, "date": date.text})
            
    return events_list


# Exemplo
# username = credentials.USERNAME
# password = credentials.PASSWORD
# session = login_moodle(username, password)
# activities = get_activities(session)
# if activities:
#     print("Atenção!! As seguintes atividades serão fechadas hoje:")
#     for activity in activities:
#         print(activity)
# else:
#     print("Nenhuma atividade será fechada hoje :)")

# username = credentials.USERNAME
# password = credentials.PASSWORD
# session = login_moodle(username, password)
# get_activities(session)
# print(get_all_activities(session))
