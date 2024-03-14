from socket import *


nameServer = "127.0.0.1"
portNumber = 4569
server = socket(AF_INET, SOCK_STREAM)
server.bind((nameServer, portNumber))
server.listen(1)
champ_array = [
    "ARIZONA DIAMONDBACKS","World Series Championships: [2001 ]",
    "ATLANTA BRAVES", "World Series Championships: [1914,1957,1995,2021]",
    "BALTIMORE ORIOLES","World Series Championships: [1966,1970,1983 ]",
    "BOSTON RED SOX","World Series Championships: [1903,1912,1915,1916,1918,2004,2007,2013,2018]",
    "CHICAGO WHITE SOX", "World Series Championships: [1906,1917,2005]",
    "CHICAGO CUBS","World Series Championships: [1907,1908,2016 ]",
    "CINCINNATI REDS","World Series Championships: [1919,1940,1975,1976,1990,]",
    "CLEVELAND GUARDIANS","World Series Championships: [1920,1948, ]",
    "COLORADO ROCKIES","World Series Championships: [n/a]",
    "DETROIT TIGERS","World Series Championships: [1935,1945,1968,1984]",
    "HOUSTON ASTROS","World Series Championships: [2017,2022 ]",
    "KANSAS CITY ROYALS","World Series Championships: [1985,2015 ]",
    "LOS ANGELES ANGELS","World Series Championships: [2002]",
    "LOS ANGELES DODGERS","World Series Championships: [1955,1959,1963,1965,1981,1988,2020]",
    "MIAMI MARLINS","World Series Championships: [1997,2003]",
    "MILWAUKEE BREWERS","World Series Championships: [n/a]",
    "MINNESOTA TWINS","World Series Championships: [1924,1987,1991]",
    "NEW YORK METS","World Series Championships: [1969,1986,]",
    "NEW YORK YANKEES",
    "World Series Championships: [19: 05,23,27,28,32,36,37,38,39,41,43,47,49,50,",
    "51,52,53,56,58,61,62,77,78,96,98,99,2000,2009]",
    "OAKLAND ATHLETICS","World Series Championships: [1910,1911,1913,1929,1930,1972,1973,1974,1989,]",
    "PHILADELPHIA PHILLIES","World Series Championships: [1980,2008]",
    "PITTSBURGH PIRATES","World Series Championships: [1909,1925,1960,1971,1979,]",
    "SAN DIEGO PADRES","World Series Championships: [n/a]",
    "SAN FRANCISCO GIANTS","World Series Championships: [1921,1922,1933,1954,2010,2012,2014]",
    "SEATTLE MARINERS","World Series Championships: [n/a]",
    "ST. LOUIS CARDINALS","World Series Championships: [1926,1931,1934,1942,1944,1946,1964,1967,1982,2006,2011]",
    "TAMPA BAY RAYS","World Series Championships: [n/a]",
    "TEXAS RANGERS","World Series Championships: [2023]",
    "TORONTO BLUE JAYS","World Series Championships: [1992,1993 ]",
    "WASHINGTON NATIONALS","World Series Championships: [2019 ]"
]

while True:

    connectedSocket, addr = server.accept()
    response = connectedSocket.recv(1024).decode("utf-8")
    print("REQUEST RECEIVED")
    j = 0
    team_not_found = 0
    for i in champ_array:
        if i == response:
            j += 1
            team_not_found = 1
            responded = champ_array[j]
            connectedSocket.send(responded.encode("utf-8"))
            print("RESPONSE SENT")
            break
        j += 1

    if team_not_found == 0:
        error_message = "Team not found: check input"
        connectedSocket.send(error_message.encode("utf-8"))
    connectedSocket.close()
