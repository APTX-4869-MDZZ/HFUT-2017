from django.shortcuts import render
import json
import math
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .esfunc import *
from .models import Wiki
from .suggestion import *

numOfEachPage = 5
cacheNum = 4

def randomPage(request):
    result = dict()
    try:
        data = json.loads(request.body)
        keyword = data.get('keyword')
        part = getPart(keyword)
        track = data.get('track')
        track.append('NotSpecified')
        page = data.get('page')
        suggestions = list()
        groups = list()
        if page == 1 :
            r = Retrieve()
            suggestions = r.retrieve(keyword)
            groups = getLdaResult(track)
        teamList = list()
        if len(part) == 0:
            teamList = getanswer(keyword, track, page)
        else:
            part_name = part[0]["part_name"]
            teamList = getPartTeam(part_name, track, page)
        request.session['answers'] = teamList
        result = {
            'successful': True,
            'data': {
                'groups': groups,
                'suggestions': suggestions,
                'content': teamList[0:numOfEachPage]
            }
        }
    except Exception as e:
        print(e)
        result = {
            'successful': False,
            'error': {
                'id': '1',
                'msg': e.value
            }
        }
    finally:
        return HttpResponse(json.dumps(result), content_type='application/json')


def turnPage(request):
    answers = []
    try:
        data = json.loads(request.body)
        page = data.get('page')
        answers = request.session.get('answers')
        answers = answers[(page-1)*numOfEachPage:page*numOfEachPage]
        result = {
            'successful': True,
            'data': {
                'content': answers
            }
        }
    except Exception as e:
        print(e)
        result = {
            'successful': False,
            'error': {
                'id': '1',
                'msg': e.value
            }
        }
    finally:
        return HttpResponse(json.dumps(result), content_type='application/json')

def getCache(request):
    result = dict()
    try:
        data = json.loads(request.body)
        page = data.get('page')
        keyword = data.get('keyword')
        track = data.get('track')
        track.append('NotSpecified')
        teamList = getanswer(keyword, track, page)
        request.session['answers'] = teamList
        result = {
            'successful': True
        }
    except Exception as e:
        print(e)
        result = {
            'successful': False,
            'error': {
                'id': '1',
                'msg': e.value
            }
        }
    finally:
        return HttpResponse(json.dumps(result), content_type='application/json')

def getDetail(request):
    data = None
    detail = None
    try:
        data = json.loads(request.body)
        id = data['_id']
        detail = getdetailbyid(id)
        detail = detail['_source']
        result = {
            'successful': True,
            'data': detail
        }
    except Exception as e:
        print(e)
    finally:
        return HttpResponse(json.dumps(result), content_type='application/json')


def classify(request):
    data = json.loads(request.body)
    keyword = data.get("keyword")
    classification = data["classification"]
    teamsIds = request.session.get('answers')
    # teams = getClassification(classification, keyword)
    result = {
        'successful': True,
        'data': {
            'pageSum':math.ceil(teams.__len__()/numOfEachPage),
            'content':teams[0:numOfEachPage]
        }
    }
    return HttpResponse(json.dumps(result), content_type='application/json')

def searchPart(request):
    data = json.loads(request.body)
    print(data)
    keyword = data["keyword"]
    part = getPart(keyword)
    return HttpResponse(json.dumps(part), content_type='application/json')