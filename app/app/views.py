import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
#
# Example Consumer
# 

callback_url = 'http://127.0.0.1:8899/callback/'
client_id = 'MP1vVTHa7Fn2StMRJiSmGgFCUdKfil6qr7PDQWck'
client_secret = 'kkMjYmhyZqvvBSI4SL4v5446Ed2YUWVbqQMM4BMH6StIIs91FrQCFR7YSNYKYAGrMXAE57yyc3Www6hjPAfIKw4ygIrydA3fwOvqHWSZsp6qEgiFtmDCzXUoByAa8itp'
_GRANT_URL = "http://localhost:8000/o/authorize/?client_id={}&response_type=code&state=random_state_string".format(client_id)

def callback(request):
    if 'code' in request.GET:
        code = request.GET.get('code')
        response = json.loads(get_token(code).text)
        context = {'grant': request.GET, 'code': response}
        request.session['access_token'] = response['access_token']
        return HttpResponseRedirect('/consume/')

def consume(request):
    access_token = request.session.get('access_token', None)
    if access_token == None:
        return HttpResponseRedirect(_GRANT_URL)
    else:
        res = get_person_info(request)
        academic = get_academic_info(request)
        library = get_library_info(request)
        context = {'username': res['user']}
        context['academic'] = academic
        context['library'] = library
        return render(request, 'inform.html', context)


def get_token(code):
    response = requests.post(
        'http://localhost:8000/o/token/',
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': callback_url
        })
    return response

def get_academic_info(request):
    access_token = request.session['access_token']
    response = requests.get(
        'http://localhost:8000/api/academic/student/',
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
        }
    )
    return response.json()

def get_library_info(request):
    access_token = request.session['access_token']
    response = requests.get(
        'http://localhost:8000/api/library/patron/',
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
        }
    )
    return response.json()
    
def get_person_info(request):
    access_token = request.session['access_token']
    response = requests.get(
        'http://localhost:8000/api/hello',
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
        }
    )
    return response.json()
