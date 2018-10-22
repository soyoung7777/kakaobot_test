import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
from operator import eq
import ast

bus_ars_id = {}

def get_bus_station(json_Data):
    #오디세이에서 버스 리스트 반환

    searchST = str(json_Data['result']['parameters']['any_bus_station'])
    print("searchST " + searchST)
    res = ""
    ACCESS = "rxJqZMHh6oQDUSfc7Kh42uCXZuHEhmj7dY7VWber2ryr9L5t2CFRy3z834JMR7RygMzaVby7ZQ3sW%2ByCZZn0Ig%3D%3D"
    my = "2Y3C1Vf5IqtpTOyTtlHh1zhP2SJSByC9xqsjCDo/4FQ"
    encMy = urllib.parse.quote_plus(my)
    encST = urllib.parse.quote_plus(searchST)

    odUrl = "https://api.odsay.com/v1/api/searchStation?lang=0&stationName="+encST+"&CID=1000&stationClass=1&apiKey="+encMy

    request = urllib.request.Request(odUrl)
    response = urllib.request.urlopen(request)

    json_rt = response.read().decode('utf-8')
    st = json.loads(json_rt)

    bus_station_dic = {}
    for i in range(0,len(st['result']['station'])):
        if st['result']['station'][i]['stationName'] not in bus_station_dic:
            bus_station_dic[st['result']['station'][i]['stationName'].replace(" ","")] = [str(st['result']['station'][i]['arsID']).replace("-","")]
        else :
            bus_station_dic[st['result']['station'][i]['stationName'].replace(" ","")].append(str(st['result']['station'][i]['arsID']).replace("-",""))

    if len(bus_station_dic.keys()) == 1 :
        return [1,res,list(bus_station_dic.keys()),bus_station_dic]

    else :
        res += "🤔 정류장을 선택해 주세요. 🤗" + "\n(올바른 숫자를 입력하는 센스!)\n\n"
        for i in range(0,len(bus_station_dic.keys())):
            res += str(i+1) +". " + list(bus_station_dic.keys())[i] + "\n"
        return [2,res,list(bus_station_dic.keys()),bus_station_dic]


def get_bus_pos(busnumber):

    res = ""
    ACCESS = "rxJqZMHh6oQDUSfc7Kh42uCXZuHEhmj7dY7VWber2ryr9L5t2CFRy3z834JMR7RygMzaVby7ZQ3sW%2ByCZZn0Ig%3D%3D"
    my = "2Y3C1Vf5IqtpTOyTtlHh1zhP2SJSByC9xqsjCDo/4FQ"
    encMy = urllib.parse.quote_plus(my)
    encNo = urllib.parse.quote_plus(busnumber)

    odUrl = "https://api.odsay.com/v1/api/searchBusLane?lang=0&busNo="+encNo+"&CID=1000&apiKey="+encMy

    request = urllib.request.Request(odUrl)
    response = urllib.request.urlopen(request)

    json_rt = response.read().decode('utf-8')
    st = json.loads(json_rt)

    odsay_bus_id = st['result']['lane'][0]['busID']
    local_bus_id = st['result']['lane'][0]['localBusID']

    print("busnumber : " + busnumber)
    print(str(odsay_bus_id) + " " + str(local_bus_id))

    odUrl = "https://api.odsay.com/v1/api/busLaneDetail?lang=0&busID="+str(odsay_bus_id)+"&apiKey="+encMy
    request = urllib.request.Request(odUrl)
    response = urllib.request.urlopen(request)
    json_rt = response.read().decode('utf-8')
    st = json.loads(json_rt)

    print(st['result']['station'][0])

    local_id_dic = {}
    find = False
    for i in st['result']['station']:
        local_id_dic[i['localStationID']] = i['stationName']
        if i['stationDirection'] == 2 and find == False:
            last_station = i['stationName']
            last_station_idx = i['idx']
            find = True


    ACCESS = "3wHizUCNd7ZmuKOs9bo3k%2FYfetwb18DzZH2xGCF6njHOYeKe5pB4RoO6AKAz3xKdeFUAVYFsf2yWa%2BhntbQJHw%3D%3D"
    oAPI = "http://ws.bus.go.kr/api/rest/buspos/getLowBusPosByRtid?serviceKey="+ACCESS+"&busRouteId="+str(local_bus_id)

    tree = ET.parse(urllib.request.urlopen(oAPI))
    root = tree.getroot()
    mbody = root.find("msgBody")

    bus_list = []

    for bus in mbody.iter("itemList"):
        tmp = []
        tmp.append(bus.find("sectOrd").text)
        tmp.append(bus.find("stopFlag").text)
        tmp.append(bus.find("lastStnId").text)
        tmp.append(bus.find("islastyn").text)

        bus_list.append(tmp)
    
    reverse = False

    res += "💌 "+busnumber + "의 위치 정보 💌" + "\n\n"
    res += "🚌 " + last_station + " 방향 🚌" + "\n"
    for i in bus_list:
        if int(tmp[0]) > last_station_idx and reverse == False:
            reverse = True
            res += "🚌 " + st['result']['station'][0]['stationName'] + " 방향 🚌" + "\n"

        if int(i[3])==1 :
            res += "‼️막차입니다‼️" + "\n"
        res += "👉🏿 현재정류장 : " + local_id_dic[i[2]]+"\n"  
        res += "👉 다음정류장 : " + st['result']['station'][int(i[0])]['stationName']+"\n"
        res += "\n"

    print(res)
    return res
    




   


def get_bus_direction(stationName):
    global bus_ars_id
    print("stationName : " + stationName)
    res = ""

    ACCESS = "rxJqZMHh6oQDUSfc7Kh42uCXZuHEhmj7dY7VWber2ryr9L5t2CFRy3z834JMR7RygMzaVby7ZQ3sW%2ByCZZn0Ig%3D%3D"
    my = "2Y3C1Vf5IqtpTOyTtlHh1zhP2SJSByC9xqsjCDo/4FQ"

    encMy = urllib.parse.quote_plus(my)


    for i in range(0,len(bus_ars_id[stationName])):
        st_ars = bus_ars_id[stationName][i].replace("-","")
        encArs = urllib.parse.quote_plus(st_ars)
        print("error")
        oAPI = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey="+ACCESS+"&arsId="+encArs
        tree = ET.parse(urllib.request.urlopen(oAPI))
        root = tree.getroot()
        mbody = root.find("msgBody").find("itemList")[20].text
        res += str(i+1) + ". " + mbody + "방향("+bus_ars_id[stationName][i]+")" + "\n"

    print(res)
    return [bus_ars_id[stationName],res]



def get_bus_station_information(busData):
    text = ""
    bus_station = busData[0]
    bus_station = bus_station.replace("'","")
    bus_arsid = json.loads(json.dumps(ast.literal_eval(busData[1])))

    ACCESS = "rxJqZMHh6oQDUSfc7Kh42uCXZuHEhmj7dY7VWber2ryr9L5t2CFRy3z834JMR7RygMzaVby7ZQ3sW%2ByCZZn0Ig%3D%3D"
    my = "2Y3C1Vf5IqtpTOyTtlHh1zhP2SJSByC9xqsjCDo/4FQ"
    encMy = urllib.parse.quote_plus(my)

    print("STation : " + bus_station)
    for i in range(0,len(bus_arsid[bus_station])) :
        #encArs = urllib.parse.quote_plus(bus_arsid[bus_station][i])
        oAPI = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey="+ACCESS+"&arsId="+bus_arsid[bus_station][i]
        tree = ET.parse(urllib.request.urlopen(oAPI))

        root = tree.getroot()
        mbody = root.find("msgBody")

        busList = {}
        bcnt = 0
        for bus in mbody.iter("itemList"):
            msg1 = "msg1_c"+str(bcnt)
            msg2 = "msg2_c"+str(bcnt)
            adr = "adr_c"+str(bcnt)
            busNo = "busNo_c"+str(bcnt)
            busNxt = "busNtext_c" + str(bcnt)
            busList[msg1] =  bus.find("arrmsg1").text
            busList[msg2] =  bus.find("arrmsg2").text
            busList[adr] =  bus.find("adirection").text
            busList[busNo] =  bus.find("rtNm").text
            busList[busNxt] = bus.find("nxtStn").text
            bcnt = bcnt+1

        text += "💌[ "+bus_station+"("+bus_arsid[bus_station][i] + ", " +busList[adr]+"방향) "+"]💌\n"
        for i in range(0, bcnt):
            bus_msg1 = "msg1_c"+str(i)
            bus_msg2 = "msg2_c"+str(i)
            bus_adr = "adr_c"+str(i)
            bus_No = "busNo_c"+str(i)
            text += "🚌 " + busList[bus_No] + " 👉🏿 "+busList[bus_msg1]+"\n"
        text += "\n"


    return text


def get_bus_station_and_number_information(busData) :
    text = ""
    bus_station = busData[0]
    bus_station = bus_station.replace("'","")
    bus_arsid = json.loads(json.dumps(ast.literal_eval(busData[1])))
    bus_number = busData[2]
    bus_number = bus_number.replace("'","")

    ACCESS = "rxJqZMHh6oQDUSfc7Kh42uCXZuHEhmj7dY7VWber2ryr9L5t2CFRy3z834JMR7RygMzaVby7ZQ3sW%2ByCZZn0Ig%3D%3D"
    my = "2Y3C1Vf5IqtpTOyTtlHh1zhP2SJSByC9xqsjCDo/4FQ"
    encMy = urllib.parse.quote_plus(my)

    print("STation : " + bus_station)
    for i in range(0,len(bus_arsid[bus_station])) :
        #encArs = urllib.parse.quote_plus(bus_arsid[bus_station][i])
        oAPI = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey="+ACCESS+"&arsId="+bus_arsid[bus_station][i]
        res_tree = ET.parse(urllib.request.urlopen(oAPI))

        root = res_tree.getroot()
        mbody = root.find("msgBody")

        busList = {}
        tmp = {}
        text += "💌[ "+bus_station+" 🚏 "+ bus_number +"번 도착정보 ]💌\n"
        for bus in mbody.iter("itemList"):
            tmp['msg1'] =  bus.find("arrmsg1").text
            tmp['msg2'] =  bus.find("arrmsg2").text
            tmp['adr'] =  bus.find("adirection").text
            tmp['nxtStn'] = bus.find("nxtStn").text
            stNm1 = bus.find("stationNm1")
            stNm2 = bus.find("stationNm2")
            if stNm1 is None:
                tmp['stNm1'] = bus.find("stNm").text
            else:
                tmp['stNm1'] = stNm1.text
            if stNm2 is None:
                tmp['stNm2'] = bus.find("stNm").text
            else:
                tmp['stNm2'] = stNm2.text
            busNo = bus.find("rtNm").text
            busList[busNo] = tmp


            if eq(busNo,bus_number) :

                text += "🚌 " + busList[busNo]['adr'] + "방향 🚌\n"
                text += "👉🏿 " + busList[busNo]['msg1'] + " " + busList[busNo]['stNm1'] + "\n"
                text += "👉🏿 " + busList[busNo]['msg2'] + " " + busList[busNo]['stNm2'] + "\n"
                text += "\n"


    return text
            #busList[busNo]['congetion1'] = bus.find("congetion1").text
            #busList[busNo]['congetion2'] = bus.find("congetion2").text
            #print(busList[stationNm1]+ " " + busList[stationNm2])






    ###버스 정보

    # if not eq(bus_number,""):
    #     text = ""
    #     direction = ""

    #     my = "f/WM8od4VAXdGg4Q5ZaWSlJ8tIbSpw+nJ4WQ4AFRpsM"
    #     encMy = urllib.parse.quote_plus(my)

    #     Bus_Info_URL = "https://api.odsay.com/v1/api/searchBusLane?lang=0&busNo="+bus_number+"&apiKey="+encMy+"&CID=1000"
    #     bus_info_request = urllib.request.Request(Bus_Info_URL)
    #     bus_info_res = urllib.request.urlopen(bus_info_request)

    #     json_data = json.loads(bus_info_res.read().decode('utf-8'))

    #     busID = json_data['result']['lane'][0]['busID']
    #     Line_URL = "https://api.odsay.com/v1/api/busLaneDetail?lang=0&busID="+str(busID)+"&apiKey="+encMy

    #     request = urllib.request.Request(Line_URL)
    #     response = urllib.request.urlopen(request)

    #     json_rt = response.read().decode('utf-8')
    #     data = json.loads(json_rt)

    #     startStation = data['result']['busStartPoint']
    #     endStation = data['result']['busEndPoint']

    #     print(startStation)
    #     print(endStation)

    #     station_idx_res = {}
    #     idx_station_res = {}
    #     bus_number_list_res = []

    #     for i in data['result']['station']:
    #         idx_station_res[i['idx']] = i['stationName']
    #         bus_number_list_res.append(i['stationName'])

    #     arrival_busstation = []
    #     kk = ""
    #     for i in range(0, bcnt):
    #         bus_key = "busNo_c"+str(i)
    #         if(busList[bus_key] == bus_number):
    #             arrival_first = busList["msg1_c"+str(i)]
    #             arrival_second = busList["msg2_c"+str(i)]

    #             if eq(startStation,busList["adr_c"+str(i)]) :
    #                 direction = "-"
    #             elif eq(endStation,busList["adr_c"+str(i)]) :
    #                 direction = "+"

    #             break

    #     print("direction : "+ direction)
    #     print("@@@@@@")
    #     print(bus_number_list_res)


#        if eq(arrival_first,"곧 도착") != True:
#            for i in range(0,len(arrival_first)):
#                if eq(arrival_first[i],"["):
#                    arrival_busstation.append(arrival_first[i+1])
#        else :
#            print("00000")
#            arrival_busstation.append("0")

#        print(arrival_second)
#        if eq(arrival_second,"곧 도착") != True:
#            for i in range(0,len(arrival_second)):
#                if eq(arrival_second[i],"["):
#                    arrival_busstation.append(arrival_second[i+1])
#                    if(int(arrival_busstation[i+2]))

        # current = 0
        # for i in bus_number_list_res:
        #     if i  == bus_station :
        #         break
        #     else :
        #         current += 1

        # print("current : " + bus_number_list_res[current])

        # if eq(direction,"+") :
        #     for i in range(5,-1,-1):
        #         print(bus_number_list_res[current+i])





#        for i in range(0,len(arrival_busstation)):
#            path_res.append(res[current+int(arrival_busstation[i])])

        # for i in range(0,len(path_res)):
        #     print("path_res " + path_res[i])

        # text += "💌["+bus_number+"번 버스에 대한 정보]💌\n"
        # if direction == "+":
        #     for i in range(5,-1,-1):
        #         checked = False
        #         for j in range(0,len(path_res)):
        #             if eq(path_res[j],res[current+i]) :
        #                 text += "💛"+res[current+i]+" 🚌\n"
        #                 print(res[current+i] + "***")
        #                 checked = True
        #                 break
        #         if checked == False:
        #             text += "💛"+res[current+i]+"\n"
        #             print(res[current+i])
        #         if i != 0 :
        #             text += "       ↓↓↓   \n"

        # text += "\n"
        # text+= "👉🏿 " + arrival_first + "\n"
        # text+= "👉🏿 " + arrival_second

    #return text
