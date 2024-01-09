from django.shortcuts import render
from bs4 import BeautifulSoup
import os
import json
import base64


os.sep = '/'
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
        with open((os.path.join(LIBRARY_ROOT["path"], node["folder"], 'document.xml')), encoding='UTF-8') as f:
            soup = BeautifulSoup(f, features='xml')
            page = soup.find('body')
            images = page.find_all("img")
            codes = page.find_all("code")
            consoles = page.find_all("console")
            outputs = page.find_all("output")
            if images:
                for image in images:
                    with open(os.path.join(LIBRARY_ROOT["path"], node["folder"], "image", image.attrs["src"]), 'rb') as f:
                        img_data = f.read()
                    encoded_image = base64.b64encode(img_data).decode('UTF-8')
                    image["src"] = f"data:image/png;base64,{encoded_image}"
            if codes:
                for code in codes:
                    with open(os.path.join(LIBRARY_ROOT["path"], node["folder"], "code", code.attrs["src"]), encoding="UTF-8") as f:
                        text = f.read()
                        code.insert(0, text)
            if consoles:
                for console in consoles:
                    with open(os.path.join(LIBRARY_ROOT["path"], node["folder"], "console", console.attrs["src"]), encoding="UTF-8") as f:
                        text = f.read()
                        console.insert(0, text)
            if outputs:
                for output in outputs:
                    with open(os.path.join(LIBRARY_ROOT["path"], node["folder"], "output", output.attrs["src"]), encoding="UTF-8") as f:
                        text = f.read()
                        output.insert(0, text)
            body = str(page)
            print(node["folder"])
            context = {"body" : body}
        return render(request, 'reader_app/display_file.html', context)
    context = {"node": node["path"]}
    return render(request, 'reader_app/other.html', context)


def tree_processing(path):
    path_keys = path.split('/')
    node = TREE_JSON
    for key in path_keys:
        node = node["path"]
        node = node[key]
    return node