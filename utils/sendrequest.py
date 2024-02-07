import requests

def fun_post(url,header,data):
     try:
        response = requests.post(url,json=data,headers=header).json()
     except:
         response = requests.post(url,json=data,headers=header)
     return response


def fun_get(url,headder,params):
    try:
        response = requests.get(url,headers=headder,params=params).json()
    except:
        response = requests.get(url,headers=headder)

    return response
