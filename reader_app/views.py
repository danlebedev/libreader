from django.shortcuts import render
import os
import json


LIBRARY_ROOT_JSON = os.path.join(os.path.abspath(os.curdir), 'reader_app', 'services', 'library_root.json')
with open(LIBRARY_ROOT_JSON, 'r') as f:
    LIBRARY_ROOT = json.load(f)
LIBRARY_STRUCTURE_TREE_JSON = os.path.join(LIBRARY_ROOT["path"], "_structure", "tree.json")
with open(LIBRARY_STRUCTURE_TREE_JSON) as f:
    TREE_JSON = json.load(f)


def index(request):
    context = {"tree_root": TREE_JSON["path"]}
    return render(request, 'reader_app/index.html', context)
