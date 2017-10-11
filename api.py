import json
import re


def load(data):
    with open(data) as json_file:
        json_lst = json.load(json_file)
    sorted_json_lst = sorted(json_lst, key = lambda k: k['project_id'])
    #sorted_json_lst = [i['project_name'] for i in sorted_json_lst]
    return sorted_json_lst


def get_project_count(lst):
    count = len(lst)
    print(count)


def get_project(lst, project_id):
    project_dict = [i for i in lst if i['project_id'] == project_id]
    return project_dict[0]


def search(lst, sort_by='start_date', sort_order='desc',
                techniques=None, search=None, search_fields=None):
    if techniques == []:
        techniques = None
    slist = []
    if search_fields == []:
        search_fields = None
    for i in lst:
        key_list = list(i.keys())
        if search_fields == None:
            if search is None:
                slist.append(i)
            else:
                for j in key_list:
                    if re.search(str(search), str(i[j])) != None:
                        slist.append(i)
                        break
        else:
            for j in search_fields:
                if j in key_list:
                    if re.search(str(search), str(i[j])) != None:
                        slist.append(i)
    if len(slist) != 0:
        if techniques is not None:
            slist = [i for i in slist
                          if set(i['techniques_used']).isdisjoint(techniques)
                          is not True]
        if sort_order == 'asc':
            slist = sorted(slist, key = lambda k: k[sort_by])
        elif sort_order == 'desc':
            slist = sorted(slist, key = lambda k: k[sort_by], reverse=True)
    return slist

def mini_list(lst, selected_keys_list):
    selected_list = []
    for i in lst:
        d = {k:v for k, v in i.items() if k in selected_keys_list}
        selected_list.append(d)
            
    return selected_list


def get_techniques(lst):
    techniques = [i['techniques_used'] for i in lst]
    techniques = sorted(set(t for i in techniques for t in i))
    return techniques


def get_technique_stats(lst):
    techniques = get_techniques(lst)
    x_dict = {}
    for x in techniques:
        y_lst = []
        x_dict[x] = y_lst
        for y in lst: 
            if x in lst[lst.index(y)]['techniques_used']: 
                idx = {k:v for k, v in y.items()
                       if k in ('project_id', 'project_name')}
                y_lst.append(idx)
    return x_dict

selected_keys_list = ['small_image', 'project_name', 'project_id', 'course_name', 'start_date', 'end_date',  'short_description', 'techniques']
