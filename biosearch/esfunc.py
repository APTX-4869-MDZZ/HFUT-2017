# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
import chardet
import json
es = Elasticsearch()
fields = ["attribution","background","description","design","human_practice","modeling","notebook","protocol","result","safety","keywords"]
def getdetailbyid(_id):
    _query = {
        "size": 1,
        "query": {
            "match": {
                "_id":_id
            }
        }
    }
    _searched = es.search(index='team_wiki', doc_type='wiki',body=_query)
    # _increment = {
    #     "script": {
    #         "inline": "ctx._source.hits++",
    #         "lang": "painless"
    #     },
    #     "query": {
    #         "term": {
    #             "_id": _id
    #         }
    #     }
    # }
    # _s = {
    #     "script": {
    #         "inline": "ctx._source.hits += params.count",
    #         "lang": "painless",
    #         "params": {
    #             "count": 1
    #         }
    #     }
    # }
    # # es.update(index='bio_search_index', doc_type='bio_search',id=_id,body=_s)
    # es.update_by_query(index='bio_search_index', doc_type='bio_search',body=_increment)
    return _searched['hits']['hits']

def getanswer(_keyword,_track1):

    _query = {
        "size": 5000,
        "query": {
            "bool":{
                "filter":[{
                    "terms": {
                        "track": _track1
                    }
                }],
                "must":[{
                        "multi_match":{
                            "query": _keyword,
                            "fields": [
                                "attribution",
                                "background",
                                "description",
                                "design",
                                "human_practice",
                                "modeling",
                                "notebook",
                                "protocol",
                                "result",
                                "safety",
                                "keywords"
                            ],
                            "fuzziness" : "AUTO"
                        }
                    }
                ]
            }
        },
        "sort": [{
            "_score": {"order": "desc"}
        },{
            "calScore": {"order": "desc"}
        },{
            "year": {"order": "desc"}
        }],
        "highlight": {
            "pre_tags" : ["<font color='#f35762'><b>"],
            "post_tags" : ["</b></font>"],
            "fragment_size" : 80,
            "fields": {
                "attribution":{},
                "background":{},
                "description":{},
                "design":{},
                "human_practice":{},
                "modeling":{},
                "notebook":{},
                "protocol":{},
                "result":{},
                "safety":{},
                "keywords":{}
            }
        }
    }
    _searched = es.search(index='team_wiki', doc_type='wiki',body=_query)
    file = open("1.json","w",encoding="utf-8")
    file.write(json.dumps(_searched))
    file.close()
    # searchsort = biosort(_searched)
    searchfilter = filter(searchsort)
    return searchfilter

def filter(searchsort):
    teamList = list()
    groupDict = dict()
    for i in searchsort:
        # print (i)
        abstract = ""
        if i['_source']['description']!="":
            abstract = i['_source']['description']
        elif i['_source']['design']!="":
            abstract = i['_source']['design']
        elif i['_source']['background']!="":
            abstract = i['_source']['background']
        elif i['_source']['attribution']!="":
            abstract = i['_source']['attribution']
        abstract = abstract[:500]
        highlight = list()
        if len(i['highlight'])>0:
            for field in i['highlight'].keys():
                highlight.append(i['highlight'][field][0])
        tmp = {
            'id':i['_id'],
            'title':i['_source']['year']+'-'+i['_source']['team_name'],
            'keywords':i['_source']['keywords'],
            'award': i['_source']['award'],
            'type': i['_source']['type'],
            'abstract':abstract,
            'highlight': highlight
        }
        groupDict = json.loads(i['_source']['group'])
        for field in group.keys():
            if (groupDict.get(field) < group.get(field)):
                groupDict[field] = group.get[field]
        groups = list()
        for (key, value) in groupDict.items():
            groups.append([key, value])
        # print (tmp)
        teamList.append(tmp)
    groups.sort(key = lambda x:x[1], reverse=True)
    groups = groups[:8]
    return {
        teamList: teamList,
        groups: groups
    }

# def biosort(groups):
    # search = searched['hits']['hits']
    # #score 重新计算并排序
    # search.sort(key = lambda x:x['_score']+x['_source']['hits'],reverse=True)
    # return search
    

def getPart(keyword):
    query = {
        "from" : 0,
        "size" : 10,
        "query" : {
            "multi_match" : {
                "fields" : ["part_name", "part_type", "short_desc"],
                "query" : keyword,
                "fuzziness" : "AUTO",
            }
        }
    }
    _searched = es.search(index="biodesigners", doc_type="parts", body=query)
    return _searched["hits"]["hits"]

def getTeamWiki(teamIds):
    query = {
        "size": 1,
        "query": {
            "bool": {
                "filter": {
                    "terms": {
                        "_id": teamIds
                    }
                }
            }
        }
    }

    _searched = es.search(index='team_wiki', doc_type='wiki',body=query)
    teams = filter(_searched)
    return teams