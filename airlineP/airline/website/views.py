import datetime
from django.http import HttpResponse
from django.template import loader
from django.template.loader import get_template
from .models import Flightt
from django.shortcuts import render
from django.template.response import TemplateResponse
from operator import itemgetter
import math
import pandas as pd
import calendar
import time
import datetime
from django.template.loader import get_template

from datetime import timedelta


def home(request):
    if request.method == "POST":
        Adresse_depart = request.POST['Adresse_depart']
        Adresse_arrivée = request.POST['Adresse_arrivée']
        Date = request.POST['Date']
        Heure = request.POST['Heure']
        Compagnie = request.POST['Compagnie']

        # return render(request, 'flights.html', {'Adresse_depart': Adresse_depart, 'Adresse_arrivée': Adresse_arrivée, 'Date': Date, 'Heure': Heure, 'Compagnie': Compagnie})
        return render(request, 'home.html', {'Adresse_depart': Adresse_depart, 'Adresse_arrivée': Adresse_arrivée, 'Date': Date, 'Heure': Heure, 'Compagnie': Compagnie})

    else:
        return render(request, 'home.html', {})


def all_flights(request):
    template = loader.get_template('flights.html')
    flights_list = Flightt.objects.all()
    context = {'flights_list': flights_list}
    return HttpResponse(template.render(context, request))


"""
def all_flights(request):
    return TemplateResponse(request, 'flights.html', {'flights_list': Flightt.objects.all()})
"""


def exemple(request):

    if request.method == "POST":

        Adresse_depart = request.POST['Adresse_depart']
        # print(Adresse_depart)
        Adresse_arrivée = request.POST['Adresse_arrivée']
        # print(Adresse_arrivée)

        Date = request.POST['Date']
        # print(Date)

        Heure = request.POST['Heure']
        # print(Heure)

        Compagnie = request.POST['Compagnie']
        # print(Compagnie)

        df = pd.read_csv('C:/Users/Genius/Desktop/projet/ProjetAnouar/Vol/airlineP/airline/test_reyada.csv', delimiter=';')
        Dheurf = df[(df.Date == Date) & (df.Heurelocale >= Heure)]

        ff = Dheurf.filter(["depart_x", "depart_y", "départ_IATA"])
        fi = ff.drop_duplicates()
        # stock the resukt of filter in list ( depart , destination iata)
        lff = [list(row) for row in fi.values]

        # print(lff)

        def zoneCalcul(Adresse_depart, Adresse_arrivée, lff):
            x_depart = 0
            y_depart = 0
            x_destination = 0
            y_destination = 0
            for i in range(len(lff)):
                for j in range(len([i])):

                    if(lff[i][j+2] == Adresse_depart):

                        x_depart = (lff[i][j])
                        y_depart = (lff[i][j+1])

                if(lff[i][j+2] == Adresse_arrivée):

                    x_destination = (lff[i][j])
                    y_destination = (lff[i][j+1])

            e = 1.5

            xm = (x_depart+x_destination) // 2
            ym = (y_depart+y_destination) // 2

            r = ((math.sqrt(pow(x_destination-x_depart, 2) +
                 pow(y_destination-y_depart, 2)))*e)/2

            InZone = []
            OutZone = []

            for i in range(len(lff)):
                for j in range(len([i])):
                    c = (pow(lff[i][j]-xm, 2)) + (lff[i][j+1]-ym)**2
                    if c <= (pow(r, 2)*e):

                        InZone.append(lff[i][j+2])

                    else:

                        OutZone.append(lff[i][j+2])

            return OutZone

        def filterZone(listD, OutZoneList):
            for i in range(len(listD)):
                for j in range(len([i])):

                    if ((listD[i][j]) in OutZoneList):
                        del listD[i][j]
                        del listD[i][0]

                    elif (listD[i][j+1] in OutZoneList):
                        del listD[i][j+1]
                        del listD[i][0]

            listA = list(filter(lambda x: x, listD))
            return(listA)

        # filter the data of date filtred by depart and destination iata

        FD = Dheurf.filter(["départ_IATA", "destination_IATA"])

        listD = [list(row) for row in FD.values]

        OutZoneList = zoneCalcul(Adresse_depart, Adresse_arrivée, lff)

        listB = filterZone(listD, OutZoneList)

        # print(listA)
        routes = listB

        start = Adresse_depart
        end = Adresse_arrivée

        def reverse(routes, start, end):

            graph = {}
            for start, end in routes:
                if start in graph:
                    graph[start].add(end)
                else:
                    graph[start] = {end}
                if end in graph:
                    graph[end].add(start)
                else:
                    graph[end] = {start}
            return graph

        graph = reverse(routes, start, end)

        def bfs_paths(graph, start, goal):
            queue = [(start, [start])]
            while queue:
                (vertex, path) = queue.pop(0)
                if graph:
                    for next in graph[vertex]-set(path):
                        # if ( len(path)  <4 ):  les paths qui sont connecter directement avec la destination [2 ,3]
                        if (len(path) < 3):
                            if next == goal:

                                yield path + [next]

                            else:

                                queue.append((next, path + [next]))

        list(bfs_paths(graph, Adresse_depart, Adresse_arrivée))

        p1 = list(bfs_paths(graph, Adresse_depart, Adresse_arrivée))
        p2 = []
        p3 = []

        # prendre que les path de 3
        for i in range(len(p1)):
            for j in range(2 < len(p1[i]) < 4):
                p2.append(p1[i])

        for k in range(len(p2)):
            for n in range(len([k])):
                p3.append(p2[k][n+1])

        IA = Adresse_depart

        for j in range(len(lff)):
            for k in range(len([j])):
                if (lff[j][k+2] == IA):  # if (lff[j][k+1] == IA):
                    del lff[j][k+2]  # del lff[j][k+1]
        # supprimer le point de depart qui est dejà visiter

        # vider les coord de depart
        lof = list(filter(lambda x: (len(x) > 2), lff))

        p = []
        # faire une zone pour chaque points ( qui sont relier avec le point de depart : list p3)
        for i in range(len(p3)):
            # Adresse_depart=p3[i]
            OutZoneList = zoneCalcul(p3[i], Adresse_arrivée, lof)
            # return les points qui sont out of zone et on ajout le point de depart
            OutZoneList.append(IA)
            FD2 = Dheurf.filter(["départ_IATA", "destination_IATA"])

            listC = [list(row) for row in FD2.values]

            listK = filterZone(listC, OutZoneList)

            routes = listK

            if routes:

                start = p3[i]
                end = Adresse_arrivée

            graph = reverse(routes, start, end)

            a = list(bfs_paths(graph, p3[i], Adresse_arrivée))
            p = p+a

        for k in range(len(p)):
            p[k].insert(0, Adresse_depart)

        p.append([Adresse_depart, Adresse_arrivée])
        # if p:
        p
        # DISPLAY PATH

        pa = []
        # Direct
        if 'Direct' in request.POST:
            Direct = request.POST['Direct']

            # print("hello")
            directt = Dheurf[(Dheurf.départ_IATA == Adresse_depart) & (
                Dheurf.destination_IATA == Adresse_arrivée) & (Dheurf.Compagnie == Compagnie)]
            cff = directt.filter(["Heurelocale", "départ_IATA", "destination_IATA",
                                  "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
            #print("cff", cff)
            lc = [list(row) for row in cff.values]
            #print("lc", lc)
            if lc:
                for z in range(len(lc)):
                    #   print(" Direct  Path::", lc[z], " , HeureDepart: ", lc[z][0], " , départ_IATA: ", lc[z][1], " , destination_IATA: ", lc[z]
                    # [2], " , HeureArrivé: ", lc[z][3], " , Coût: ", lc[z][4], "£ , Durée: ", lc[z][5], " , Compagnie: ", lc[z][6])

                    t1 = datetime.datetime.strptime(lc[z][0], '%H:%M')
                    t2 = datetime.datetime.strptime(lc[z][3], '%H:%M')
                    c = 0
                    if (t1 > t2):
                        c = 1
                    # print("hi")
                    a = round(float(lc[z][4]), 3)
                    pa.append([a, lc[z][0], lc[z][1], lc[z]
                               [2], lc[z][3], lc[z][5], lc[z][6], c])
                    # print(pa)
                    # lc[z][4]

                    pa.sort()
                    # pa
                    # sorted(pa, key=lambda x: x[5])
                    # if ( lc[z][0] )
                    # return render(request, 'flights.html', {'HeureDepart ', lc[z][0], ' départ_IATA', lc[z][1], 'destination_IATA', lc[z][2], 'HeureArrivé', lc[z][3], 'Coût', lc[z][4], 'Durée', lc[z][5], 'Compagnie', lc[z][6]})
                # return render(request, 'flightsDirect.html', {'pa': pa, 'Adresse_depart': Adresse_depart, 'Adresse_arrivée': Adresse_arrivée, 'Compagnie': Compagnie, 'nouv': nouv, 'air': air, 'bri': bri, 'tur': tur})
            return render(request, 'flightsDirect.html', {'pa': pa, 'Adresse_depart': Adresse_depart, 'Adresse_arrivée': Adresse_arrivée})
        # stop1

        elif 'stop1' in request.POST:
            stop1 = request.POST['stop1']
            er1 = True

            p2 = []
            # print("hello1")

            for i in range(len(p)):
                for j in range(2 < len(p[i]) < 4):
                    # print(p[i])
                    p2.append(p[i])
            # print(p2)
            # print("hello2")

            for i in range(len(p2)):
                for j in range(len([i])):

                    c1 = Dheurf[(Dheurf.départ_IATA == p2[i][j]) & (
                        Dheurf.destination_IATA == p2[i][j+1])]
                    cf1 = c1.filter(["Heurelocale", "départ_IATA", "destination_IATA",
                                    "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
            # print(cf1)
            # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                    l1 = [list(row) for row in cf1.values]
                   
                    # print(l1)
                    if l1:

                        for k in range(len(l1)):
                            # print("ggg",l1[k])

                            td1 = datetime.datetime.strptime(l1[k][3], '%H:%M')
                            td2 = timedelta(hours=2)
                            td = td1+td2
                            # print("td", td)
                            m3 = td.strftime('%H:%M')
                            # print('m3', m3)

                            c2 = Dheurf[(Dheurf.départ_IATA == p2[i][j+1]) & (
                                Dheurf.destination_IATA == p2[i][j+2]) & (Dheurf.Heurelocale >= m3)]
                            # print("c2:", c2)
                            cf2 = c2.filter(["Heurelocale", "départ_IATA", "destination_IATA",
                                            "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])

                            l2 = [list(row) for row in cf2.values]
                            
                            # print(l2)
                            if l2:

                                for n in range(len(l2)):

                                    s1 = l1[k][0]
                                    # print("s1", s1)
                                    s2 = l2[n][3]  # for example
                                    # print("s2", s2)
                                    FMT = '%H:%M'
                                    x33 = datetime.datetime.strptime(
                                        s2, FMT) - datetime.datetime.strptime(s1, FMT)

                                    def strfdelta(tdelta, fmt):
                                        d = {"days": tdelta.days}
                                        d["hours"], rem = divmod(
                                            tdelta.seconds, 3600)
                                        d["minutes"], d["seconds"] = divmod(
                                            rem, 60)
                                        return fmt.format(**d)
                                    x3 = strfdelta(
                                        x33, "{hours}:{minutes}")

                                    k1 = datetime.datetime.strptime(
                                        x3, FMT)
                                    # print("k1", k1)
                                    k2 = datetime.datetime.strptime(
                                        "16:00", FMT)
                                    # print("k2", k2)

                                    # print(
                                    #   "     ---------------------------------------------------------------------------------------------------------------------------------------------------")
                                    if (l1[k][6] == Compagnie or l2[n][6] == Compagnie) :

                                        # print(l1[k][1])
                                        # print(l1[k][2])

                                       # print(l1[k][4])
                                        # print(float(l1[k][4]))
                                       # print(float(l2[n][4]))
                                        b = float(l1[k][4])+float(l2[n][4])

                                        # print(b)
                                        a = round(float(b), 3)

                                        # print(a)
                                       # print("   Stop1   Path::", l1[k],  "-> Escale-> ", l2[n], ", HeureDepart: ", l1[k][0], " , départ_IATA: ", l1[k][1], " , destination_IATA: ", l2[n][2],
                                        #      " , HeureArrivé: ", l2[n][3], " , Escale: ", l2[n][1], " , Coût: ", a, "£ , Durée: ", x3, " , Compagnie: ", l1[k][6], "+", l2[n][6])
                                       # print(
                                        #   "       -----------------------------------------------------------------------------------------------------------------------------------------------")

                                        t1 = datetime.datetime.strptime(
                                            l1[k][0], '%H:%M')
                                        t2 = datetime.datetime.strptime(
                                            l2[n][3], '%H:%M')
                                        c = 0
                                        if (t1 > t2):
                                            c = 1

                                        pa.append([a, l1[k], l2[n], l1[k][0], l1[k][1], l2[n][2], l2[n]
                                                  [3], l2[n][1], x3, l1[k][6], l2[n][6], c])
                                        pa.sort()
                                        # sorted(pa, key=lambda x: x[8])

                                        #print("pa:", pa)
                                       # print("hi")
            return render(request, 'flightsStop1.html', {'pa': pa, 'Adresse_depart': Adresse_depart, 'Adresse_arrivée': Adresse_arrivée, 'Compagnie': Compagnie})

        # stop2
        elif 'stop2' in request.POST:
            stop2 = request.POST['stop2']
            er2 = True
            p3 = []
            for i in range(len(p)):
                for j in range(3 < len(p[i]) <= 5):
                    # print(p1[i])
                    p3.append(p[i])
            # print(p3)

            for i in range(len(p3)):
                for j in range(len([i])):

                    c1 = Dheurf[(Dheurf.départ_IATA == p3[i][j]) & (
                        Dheurf.destination_IATA == p3[i][j+1])]
                    cf1 = c1.filter(["Heurelocale", "départ_IATA", "destination_IATA",
                                    "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
                    # print("cf1",cf1)
                    # print("**********************")

                    l1 = [list(row) for row in cf1.values]
                    l1.insert(0, cf1.columns.to_list())

                    l1.remove(["Heurelocale", "départ_IATA", "destination_IATA",
                               "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
                    if l1:

                        for k in range(len(l1)):
                            # print("ggg",l1[k])

                            td1 = datetime.datetime.strptime(l1[k][3], '%H:%M')
                            td2 = timedelta(hours=1)
                            td = td1+td2
                            m3 = td.strftime('%H:%M')

                            c2 = Dheurf[(Dheurf.départ_IATA == p3[i][j+1]) & (
                                Dheurf.destination_IATA == p3[i][j+2]) & (Dheurf.Heurelocale > m3)]
                            cf2 = c2.filter(["Heurelocale", "départ_IATA", "destination_IATA",
                                            "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
                            # print(cf2)
                            # print("++++++++++++++++++++++++++++++++++++++")
                            l2 = [list(row) for row in cf2.values]
                            l2.insert(0, cf2.columns.to_list())

                            l2.remove(["Heurelocale", "départ_IATA", "destination_IATA",
                                       "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
                            if l2:
                                # print(l2)
                                # print(l1[0][3])
                                for n in range(len(l2)):
                                    # print("g",l2[n])

                                    td1 = datetime.datetime.strptime(
                                        l2[n][3], '%H:%M')

                                    td2 = timedelta(hours=1)
                                    td = td1+td2
                                    t3 = td.strftime('%H:%M')

                                    c3 = Dheurf[(Dheurf.départ_IATA == p3[i][j+2]) & (
                                        Dheurf.destination_IATA == p3[i][j+3]) & (Dheurf.Heurelocale > t3)]
                                    cf3 = c3.filter(["Heurelocale", "départ_IATA", "destination_IATA",
                                                    "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
                                    l3 = [list(row) for row in cf3.values]
                            
                                    if l3:
                                        for m in range(len(l3)):

                                            s1 = l1[k][0]
                                            s2 = l3[m][3]  # for example
                                            FMT = '%H:%M'
                                            x44 = datetime.datetime.strptime(
                                                s2, FMT) - datetime.datetime.strptime(s1, FMT)

                                            def strfdelta(tdelta, fmt):
                                                d = {"days": tdelta.days}
                                                d["hours"], rem = divmod(
                                                    tdelta.seconds, 3600)
                                                d["minutes"], d["seconds"] = divmod(
                                                    rem, 60)
                                                return fmt.format(**d)
                                            x4 = strfdelta(
                                                x44, "{hours}:{minutes}")

                                            k1 = datetime.datetime.strptime(
                                                x4, FMT)
                                            # print("k1", k1)
                                            k2 = datetime.datetime.strptime(
                                                "16:00", FMT)
                                    # print("k2", k2)
                                            # print("  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                                            if (l1[k][6] == Compagnie or l2[n][6] == Compagnie or l3[m][6] == Compagnie) and (k1 < k2):
                                                b = float(
                                                    l1[k][4])+float(l2[n][4])+float(l3[m][4])

                                                a = round(float(b), 3)

                                                # print("   Path ::", l1[k], " -> Escale 1 -> ", l2[n], "->Escale 2-> ", l3[m], ", HeureDepart: ", l1[k][0], " , départ_IATA: ", l1[k][1], " , destination_IATA: ", l3[m][2], " , HeureArrivé: ",
                                                #      l3[m][3], " , Escale1: ", l2[n][1], " , Escale2: ", l3[m][1],  ", Coût :", a, "£ , Durée: ", x4, " , Compagnie: ", l1[k][6], "+", l2[n][6], "+", l3[m][6])
                                                # print(
                                                #    "   -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                                                t1 = datetime.datetime.strptime(
                                                    l1[k][0], '%H:%M')
                                                t2 = datetime.datetime.strptime(
                                                    l3[m][3], '%H:%M')
                                                c = 0
                                                if (t1 > t2):
                                                    c = 1

                                                pa.append([a, l1[k], l2[n], l3[m], l1[k][0], l1[k][1], l3[m][2], l3[m][3], l2[n]
                                                           [1], l3[m][1],  x4, l1[k][6], l2[n][6], l3[m][6], c])
                                                pa.sort()
                                                # sorted(pa, key=lambda x: x[10])

                                                # print(pa)
            return render(request, 'flightsStop2.html', {'pa': pa, 'Adresse_depart': Adresse_depart, 'Adresse_arrivée': Adresse_arrivée, 'Compagnie': Compagnie})

        """def dirc():
            directt = df[(df.départ_IATA == Adresse_depart) & (
                df.destination_IATA == Adresse_arrivée) & (df.Compagnie == Compagnie)]
            cff = directt.filter(["Heurelocale", "départ_IATA", "destination_IATA",
                                  "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
            lc = [list(row) for row in cff.values]
            lc.insert(0, cff.columns.to_list())
            lc.remove(["Heurelocale", "départ_IATA", "destination_IATA",
                       "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
            for z in range(len(lc)):
                print(" Direct  Path::", lc[z], " , HeureDepart: ", lc[z][0], " , départ_IATA: ", lc[z][1], " , destination_IATA: ", lc[z]
                      [2], " , HeureArrivé: ", lc[z][3], " , Coût: ", lc[z][4], "£ , Durée: ", lc[z][5], " , Compagnie: ", lc[z][6])
                pa.append([lc[z][0], lc[z][1], lc[z]
                           [2], lc[z][3], lc[z][4], lc[z][5], lc[z][6]])
            d = []
            dur = []

            for i in range(len(pa)):
                for j in range(len([i])):
                    d.append(pa[i][j+5])

            for i in range(len(d)):
                for j in range(len([i])):
                    mini = min(d)
                    # print(ma)
                    if mini in pa[i]:
                        pa[i]

            for i in range(len(dur)):
                for j in range(len([i])):
                    mini = min(dur)
                    ma = time.strftime("%H:%M", time.localtime(mini))
                    # print(ma)

                    if ma in pa[i]:
                        pa[i]
            return pa
"""
    return render(request, 'home.html', {'pa': pa, 'Adresse_depart': Adresse_depart, 'Adresse_arrivée': Adresse_arrivée, 'Compagnie': Compagnie})


"""def directPath(request):
    if request.method == "POST":
        Adresse_depart = request.POST['Adresse_depart']
        Adresse_arrivée = request.POST['Adresse_arrivée']
        Date = request.POST['Date']
        Heure = request.POST['Heure']
        Compagnie = request.POST['Compagnie']

        df = pd.read_csv('flightt.csv', delimiter=',')
        Dheurf = df[(df.Date == Date) & (df.Heurelocale >= Heure)]

        ff = Dheurf.filter(["depart_x", "depart_y", "départ_IATA"])
        fi = ff.drop_duplicates()
        # stock the resukt of filter in list ( depart , destination iata)
        lff = [list(row) for row in fi.values]
        lff.insert(0, fi.columns.to_list())
        lff.remove(['depart_x', 'depart_y', 'départ_IATA'])

        # print(lff)
        x_depart = 0
        y_depart = 0
        x_destination = 0
        y_destination = 0

        def zoneCalcul(Adresse_depart, Adresse_arrivée, lff):

            for i in range(len(lff)):
                for j in range(len([i])):

                    if(lff[i][j+2] == Adresse_depart):

                        x_depart = (lff[i][j])
                        y_depart = (lff[i][j+1])

                if(lff[i][j+2] == Adresse_arrivée):

                    x_destination = (lff[i][j])
                    y_destination = (lff[i][j+1])

            e = 1.5

            xm = (x_depart+x_destination) // 2
            ym = (y_depart+y_destination) // 2

            r = ((math.sqrt(pow(x_destination-x_depart, 2) +
                 pow(y_destination-y_depart, 2)))*e)/2

            InZone = []
            OutZone = []

            for i in range(len(lff)):
                for j in range(len([i])):
                    c = (pow(lff[i][j]-xm, 2)) + (lff[i][j+1]-ym)**2
                    if c <= (pow(r, 2)):

                        InZone.append(lff[i][j+2])

                    else:

                        OutZone.append(lff[i][j+2])

            return OutZone

        def filterZone(listD, OutZoneList):
            for i in range(len(listD)):
                for j in range(len([i])):

                    if ((listD[i][j]) in OutZoneList):
                        del listD[i][j]
                        del listD[i][0]

                    elif (listD[i][j+1] in OutZoneList):
                        del listD[i][j+1]
                        del listD[i][0]

            listA = list(filter(lambda x: x, listD))
            return(listA)

        # filter the data of date filtred by depart and destination iata

        FD = Dheurf.filter(["départ_IATA", "destination_IATA"])

        listD = [list(row) for row in FD.values]
        listD.insert(0, FD.columns.to_list())
        listD.remove(['départ_IATA', 'destination_IATA'])

        OutZoneList = zoneCalcul(Adresse_depart, Adresse_arrivée, lff)

        listB = filterZone(listD, OutZoneList)

        # print(listA)
        routes = listB

        start = Adresse_depart
        end = Adresse_arrivée

        def reverse(routes, start, end):

            graph = {}
            for start, end in routes:
                if start in graph:
                    graph[start].add(end)
                else:
                    graph[start] = {end}
                if end in graph:
                    graph[end].add(start)
                else:
                    graph[end] = {start}
            return graph

        graph = reverse(routes, start, end)

        def bfs_paths(graph, start, goal):

            queue = [(start, [start])]

            while queue:
                (vertex, path) = queue.pop(0)
                if graph:
                    for next in graph[vertex]-set(path):
                        # if ( len(path)  <4 ):  les paths qui sont connecter directement avec la destination [2 ,3]
                        if (len(path) < 3):
                            if next == goal:

                                yield path + [next]

                            else:

                                queue.append((next, path + [next]))

        list(bfs_paths(graph, Adresse_depart, Adresse_arrivée))

        p1 = list(bfs_paths(graph, Adresse_depart, Adresse_arrivée))
        p2 = []
        p3 = []

        # prendre que les path de 3
        for i in range(len(p1)):
            for j in range(2 < len(p1[i]) < 4):
                p2.append(p1[i])

        for k in range(len(p2)):
            for n in range(len([k])):
                p3.append(p2[k][n+1])

        IA = Adresse_depart

        for j in range(len(lff)):
            for k in range(len([j])):
                if (lff[j][k+2] == IA):  # if (lff[j][k+1] == IA):
                    del lff[j][k+2]  # del lff[j][k+1]
        # supprimer le point de depart qui est dejà visiter

        # vider les coord de depart
        lof = list(filter(lambda x: (len(x) > 2), lff))

        p = []
        # faire une zone pour chaque points ( qui sont relier avec le point de depart : list p3)
        for i in range(len(p3)):
            # Adresse_depart=p3[i]
            OutZoneList = zoneCalcul(p3[i], Adresse_arrivée, lof)
            # return les points qui sont out of zone et on ajout le point de depart
            OutZoneList.append(IA)
            FD2 = Dheurf.filter(["départ_IATA", "destination_IATA"])

            listC = [list(row) for row in FD2.values]
            listC.insert(0, FD2.columns.to_list())
            listC.remove(['départ_IATA', 'destination_IATA'])

            listK = filterZone(listC, OutZoneList)

            routes = listK
            if routes:
                start = p3[i]
                end = Adresse_arrivée

            graph = reverse(routes, start, end)
            a = list(bfs_paths(graph, p3[i], Adresse_arrivée))
            p = p+a

        for k in range(len(p)):
            p[k].insert(0, Adresse_depart)

        p.append([Adresse_depart, Adresse_arrivée])
        p
        # DISPLAY PATH

        pDir = []

        # Direct
        if request.POST.get('stop2', False):

            directt = df[(df.départ_IATA == Adresse_depart) & (
                df.destination_IATA == Adresse_arrivée) & (df.Compagnie == Compagnie)]
            cff = directt.filter(["Heurelocale", "départ_IATA", "destination_IATA",
                                  "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
            lc = [list(row) for row in cff.values]
            lc.insert(0, cff.columns.to_list())
            lc.remove(["Heurelocale", "départ_IATA", "destination_IATA",
                       "HeureArrivé", "Prix_Camp1", "Durée_trajet", "Compagnie"])
            for z in range(len(lc)):
                print(" Direct  Path::", lc[z], " , HeureDepart: ", lc[z][0], " , départ_IATA: ", lc[z][1], " , destination_IATA: ", lc[z]
                      [2], " , HeureArrivé: ", lc[z][3], " , Coût: ", lc[z][4], "£ , Durée: ", lc[z][5], " , Compagnie: ", lc[z][6])
                pDir.append([lc[z][0], lc[z][1], lc[z]
                             [2], lc[z][3], lc[z][4], lc[z][5], lc[z][6]])
    return render(request, 'flights.html', {'pa': pDir, 'Adresse_depart': Adresse_depart, 'Adresse_arrivée': Adresse_arrivée})
"""
