CITIES = ["The Hague", "Rotterdam", "Leiden", "Amsterdam",
          "Delft", "Utrecht", "Arnhem", "Haarlem", "Den Bosch", "Zwolle"]
GENDERS = ["Male", "Female", "Other"]
ROLES = ["consultant", "admin", "super_admin"]


def CITY(i): return CITIES[int(i.decode())-1].encode('utf-8')
def GENDER(i): return GENDERS[int(i.decode())-1].encode('utf-8')
def ROLE(i): return ROLES[int(i.decode())-1].encode('utf-8')
