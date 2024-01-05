from django.shortcuts import render, HttpResponse
from django.urls import reverse
import os
import json


LIBRARY_ROOT_JSON = os.path.join(os.path.abspath(os.curdir), 'reader_app', 'services', 'library_root.json')
with open(LIBRARY_ROOT_JSON, 'r') as f:
    LIBRARY_ROOT = json.load(f)
LIBRARY_STRUCTURE_TREE_JSON = os.path.join(LIBRARY_ROOT["path"], "_structure", "tree.json")
with open(LIBRARY_STRUCTURE_TREE_JSON) as f:
    TREE_JSON = json.load(f)


def sort_dict(dict_node, key=''):
    sorted_dict = {}
    for k, v in dict_node.items():
        if isinstance(v, dict):
            if k.isnumeric():
                dct = dict_node[k]
                dct["route"] = key + '/' + k
                sorted_dict[k] = sort_dict(v, key + '/' + k)
            else:
                sorted_dict[k] = sort_dict(v, key)
        else:
            sorted_dict[k] = v
    return sorted_dict

NEW_DICT = sort_dict(TREE_JSON)


def index(request):
    context = {"tree_root": NEW_DICT["path"]}
    return render(request, 'reader_app/index.html', context)


def other(request, path):
    node = tree_processing(path)
    if node.get("folder"):
        with open((os.path.join(LIBRARY_ROOT["path"], node["folder"], 'document.xml'))) as f:
            page = f.read()
        return HttpResponse(page)
    context = {"node": node["path"]}
    return render(request, 'reader_app/other.html', context)


def tree_processing(path):
    path_keys = path.split('/')
    node = TREE_JSON
    for key in path_keys:
        node = node["path"]
        node = node[key]
    return node