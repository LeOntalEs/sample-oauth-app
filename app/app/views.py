import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
#
# Example Consumer
# 
AUTH_SERVER = "api.tu.ac.th"
callback_url = 'http://127.0.0.1:8899/callback/'
client_id = 'MP1vVTHa7Fn2StMRJiSmGgFCUdKfil6qr7PDQWck'
client_secret = 'kkMjYmhyZqvvBSI4SL4v5446Ed2YUWVbqQMM4BMH6StIIs91FrQCFR7YSNYKYAGrMXAE57yyc3Www6hjPAfIKw4ygIrydA3fwOvqHWSZsp6qEgiFtmDCzXUoByAa8itp'

_GRANT_URL = "https://{}/o/authorize/?client_id={}&response_type=code&state=random_state_string".format(AUTH_SERVER, client_id)
_TOKEN_URL = 'https://{}/o/token/'.format(AUTH_SERVER)
_STUDENT_API = 'https://{}/api/student/'.format(AUTH_SERVER)
_LIB_API = 'https://{}/api/library-patron/'.format(AUTH_SERVER)
_ME_URL = 'https://{}/api/me/'.format(AUTH_SERVER)

def callback(request):
    print request.GET
    if 'code' in request.GET:
        code = request.GET.get('code')
        print 'code: ', code
        print
        response = json.loads(get_token(code).text)
        context = {'grant': request.GET, 'code': response}
        request.session['access_token'] = response['access_token']
        return HttpResponseRedirect('/consume/')
    if 'error' in request.GET:
        return HttpResponse(status=404)


def consume(request):
    access_token = request.session.get('access_token', None)
    if access_token == None:
        return HttpResponseRedirect(_GRANT_URL)
    else:
        res = get_person_info(request)
        academic = get_academic_info(request)
        library = get_library_info(request)
        context = dict()
        context = {'username': res['username']}
        context['academic'] = academic
        context['library'] = library
        return render(request, 'inform.html', context)


def get_token(code):
    response = requests.post(
        _TOKEN_URL,
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': callback_url
        })
    print 'get_token: ', response
    print response.text
    print
    return response

def get_academic_info(request):
    access_token = request.session['access_token']
    response = requests.get(
        _STUDENT_API,
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
        }
    )
    print response
    return response.json()

def get_library_info(request):
    access_token = request.session['access_token']
    response = requests.get(
        _LIB_API,
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
        }
    )
    print response
    return response.json()
    
def get_person_info(request):
    access_token = request.session['access_token']
    print '- me -'
    print access_token
    response = requests.get(
        _ME_URL,
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
        }
    )
    print response
    print response.json()
    return response.json()
