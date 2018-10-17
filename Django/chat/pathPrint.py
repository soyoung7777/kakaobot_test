import json
import urllib.request
import urllib.parse
from operator import eq
import ast

def subway(swPath):
	sText = ""
	sText += "💜"+swPath['startName']+"역에서\n"
	sText += swPath['lane'][0]['name']+"을 탑승\n"
	sText += "("+swPath['passStopList']['stations'][1]['stationName']+"방면)\n"
	sText += "💜"+swPath['endName']+"역에서 하차\n"
	sText += "("+str(swPath['stationCount'])+"개 정류장 이동)\n"

	return sText


def bus(busPath):
	bText = ""
	bText += "💛"+busPath['startName']+"정류장에서\n"
	bText += busPath['lane'][0]['busNo']+"번 버스 탑승\n"
	bText += "💛"+busPath['endName']+"정류장에서 하차\n"
	bText += "("+str(busPath['stationCount'])+"개 정류장 이동)\n"

	return bText

def get_result(start, end, tsType, pNum):

	geoUrl = "https://maps.googleapis.com/maps/api/geocode/json?&sensor=false&language=ko&address="

	sUrl = geoUrl+urllib.parse.quote_plus(start)
	eUrl = geoUrl+urllib.parse.quote_plus(end)

	s_request = urllib.request.Request(sUrl+'&key=AIzaSyBZNZ54ytcVVd6JZMCsEJ55pasegJRAIt8')
	e_request = urllib.request.Request(eUrl+'&key=AIzaSyBZNZ54ytcVVd6JZMCsEJ55pasegJRAIt8')

	s_response = urllib.request.urlopen(s_request)
	e_response = urllib.request.urlopen(e_request)

	s_json = json.loads(s_response.read().decode('utf-8'))
	e_json = json.loads(e_response.read().decode('utf-8'))

	s_status = str(s_json['status'])
	if eq(s_status,"OK") :
		#(x, 경도, longtitude) , (y, 위도, latitude)
		sx = str(s_json['results'][0]['geometry']['location']['lng'])
		sy = str(s_json['results'][0]['geometry']['location']['lat'])
		ex = str(e_json['results'][0]['geometry']['location']['lng'])
		ey = str(e_json['results'][0]['geometry']['location']['lat'])


		my = "2Y3C1Vf5IqtpTOyTtlHh1zhP2SJSByC9xqsjCDo/4FQ"
		encMy = urllib.parse.quote_plus(my)

		if eq(tsType, "지하철"):
			SPT = "&SearchPathType=1"
		elif eq(tsType, "버스"):
			SPT = "&SearchPathType=2"
		else:
			SPT = "&SearchPathType=0"

		odUrl = "https://api.odsay.com/v1/api/searchPubTransPath?SX="+sx+"&SY="+sy+"&EX="+ex+"&EY="+ey+SPT+"&apiKey="+encMy

		request = urllib.request.Request(odUrl)
		response = urllib.request.urlopen(request)

		json_rt = response.read().decode('utf-8')
		data = json.loads(json_rt)

		try:
			path_data = data['result']['path']
			txt = start+"에서 "+end+"까지 가는 길 알려드릴게요!\n\n\n"
			detail_txt = detail_get_pathFind(path_data)
		except KeyError:
			txt = "문제가 생겼어요😂잠시 후 다시 이용해주시겠어요?"
		path_len = len(path_data)

		if pNum < path_len:
			pType = path_data[pNum]['pathType']
			subPath = path_data[pNum]['subPath']

			count = len(subPath)
			print(count)

			if pType == 1:
				# txt += "[지하철로 이동 🚋🚋]\n"
				for i in range(0, count):
					tType = subPath[i]['trafficType']
					if tType == 1:
						txt += subway(subPath[i])
			elif pType == 2:
				# txt += "[버스로 이동 🚌🚌]\n"
				for i in range(0, count):
					tType = subPath[i]['trafficType']
					if tType == 2:
						txt += bus(subPath[i])
			else:
				# txt += "💌[지하철+버스로 이동하세요]💌\n"
				for i in range(0, count):
					tType = subPath[i]['trafficType']
					if tType == 1 :
						# txt += "\n[지하철로 이동 🚋🚋]\n"
						txt += subway(subPath[i])
						if i < count:
							txt += "\n⬇\n"
					elif tType == 2:
						# txt += "\n[버스로 이동 🚌🚌]\n"
						txt += bus(subPath[i])
						if i < count:
							txt += "\n⬇\n"


			txt +=  "\n\n다른경로를 원하시나요?\n원하시면 10초내로 'Y/ㅇ/응/어' 중 응답해주세요!"
		else:
			txt = "더 이상 경로가 없어요!!\n"
			detail_txt = ""

	elif eq(s_status,"ZERO_RESULTS"):
		txt = "존재하지 않는 주소입니다"
	elif eq(s_status,"OVER_QUERY_LIMIT") :
		txt = "할당량 초과"
	elif eq(s_status,"REQUEST_DENIED"):
		txt = "요청거부"
	elif eq(s_status,"INVALID_REQUEST"):
		txt = "출발지 정보 누락"
	elif eq(s_status,"UNKNOWN_ERROR"):
		txt = "서버오류"

	return txt, detail_txt


def detail_get_pathFind(data):
	detail = "가나다라마바사"

# 	<!DOCTYPE html>
# <html>
# <head>
#     <meta charset="UTF-8">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
#     <title>간단한 지도 표시하기</title>
#     <script type="text/javascript" src="https://openapi.map.naver.com/openapi/v3/maps.js?clientId=YOUR_CLIENT_ID"></script>
# </head>
# <body>
# <div id="map" style="width:100%;height:400px;"></div>
#
# <script>
# var mapOptions = {
#     center: new naver.maps.LatLng(37.3595704, 127.105399),
#     zoom: 10
# };
#
# var map = new naver.maps.Map('map', mapOptions);
# </script>
# </body>
# </html


	return detail
