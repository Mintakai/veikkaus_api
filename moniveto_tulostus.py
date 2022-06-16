import datetime
import json
import requests
import yaml

SPORTIDS = {
    1: "Jalkapallo",
    2: "Pesäpallo"
}


def get_creds(usr):
    with open(r'creds.yaml') as creds_file:
        creds = yaml.load(creds_file, Loader=yaml.FullLoader)
        if usr:
            return creds["username"]
        elif not usr:
            return creds["password"]


USR = get_creds(True)
PW = get_creds(False)

# Vaaditut otsikkotietueet
headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'X-ESA-API-Key': 'ROBOT'
}


# Sisäänkirjautuminen Veikkauksen tilille palauttaa sessio-objektin
def login(username, password):
    s = requests.Session()
    login_req = {"type": "STANDARD_LOGIN", "login": username, "password": password}
    r = s.post("https://www.veikkaus.fi/api/bff/v1/sessions", data=json.dumps(login_req), headers=headers)
    if r.status_code == 200:
        return s
    else:
        raise Exception("Connection or login failure!", r.status_code)


# Main-funktio.
# 1. Kirjautuu sisään
# 2. Hakee Monivedon tulevat kohteet (kirjautuneena käyttäjänä)
# 3. Tulostaa vastauksen
def main():
    s = login(USR, PW)
    r = s.get('https://www.veikkaus.fi/api/sport-open-games/v1/games/MULTISCORE/draws', headers=headers).json()
    for x in range(len(r)):
        sport_id = int(r[x]["rows"][0]["sportId"])
        try:
            print(f"\n---{SPORTIDS[sport_id]}---")
        except ValueError:
            print(f"Tunnistamaton laji... sport_id: {sport_id}")
        close_time = datetime.datetime.fromtimestamp(int(r[x]["closeTime"] / 1000))
        print(f"Closes at {close_time:%Y-%m-%d %H:%M:%S}")
        print("---games---")
        for y in range(len(r[x]["rows"])):
            print(r[x]["rows"][y]["name"])


main()
