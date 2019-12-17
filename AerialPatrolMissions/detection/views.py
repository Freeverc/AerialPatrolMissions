from django.shortcuts import render
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import JsonResponse
from django.conf import settings

from .models import Image, Mission
import os
import json
# Create your views here.

STATIC_ROOT = settings.STATIC_ROOT
MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
# COCO_ROOT = settings.COCO_ROOT
# DETECT_ROOT = settings.DETECT_ROOT
# SEG_ROOT = settings.SEG_ROOT
# Create your views here.
DETECT_SCRIPT_PATH = '/home/file/mmdetection/tools/server_test.py'
SEG_SCRIPT_PATH = ''

ROOT_NODE = ''


def profile_demo(request):
    return render(request, 'index.html')


def upload_demo(request, upload_page_id):
    upload_path = os.path.join(MEDIA_ROOT, 'img')
    upload_name = ''
    # if request.method == 'POST':
    image_list = request.FILES.getlist('img')
    print(len(image_list))
    for image_file in image_list:
        destination = open(os.path.join(upload_path, image_file.name), 'wb')
        for chunk in image_file.chunks():
            destination.write(chunk)
        destination.close()

    app_functions = ['单类别目标检测', '多类别目标检测']
    class_names = [["工程车辆"], ["挖掘机", "推土机", "运输车"]]
    return render(request, 'upload_demo.html',
                  {
                      'upload_page_id': upload_page_id,
                      'app_function': app_functions[upload_page_id],
                      'class_names': class_names[upload_page_id],
                      'upload_path': upload_path,
                      'upload_name': upload_name
                  })


def get_all_missions(request):
    root_node = Mission.objects.all()[0]
    ROOT_NODE = root_node
    json_tree_str = json.dumps(serializable_object(root_node))
    print(json_tree_str)
    json_tree = json.loads(json_tree_str)
    children = json_tree['children']
    # for key, value in items:
    #     print(str(key) + '=' + str(value))
    # for child in children:

    response = JsonResponse(
        {
            'success': 'true',
            'tasks': children
        }
    )
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    print(response.content)

    return response
    # return render(request, 'index.html')


def create_mission(request):
    # name = request.POST.get('name')
    # info = request.POST.get('info')
    # parent_id = request.POST.get('parent_id')

    # parent = request.POST.get('parent')
    # children = request.POST.get('children')
    name = 'name'
    info = 'info'
    # parent = ROOT_NODE
    parent_id = 1
    # children = []
    # children_id = 8
    print("name: ", name)

    new_mission = Mission(
        name=name,
        info=info,
        # parent=parent,
        parent_id=parent_id,
        # children=children, # can not assign a value
        # image_path=os.path.join(parent.image_path, name),
        parent_mission_id=parent_id
    )
    new_mission.image_path = os.path.join(new_mission.parent.image_path, new_mission.name)
    new_mission.detect_path = os.path.join(new_mission.image_path, 'detect')
    if not os.path.exists(new_mission.image_path):
        os.mkdir(new_mission.image_path)
    if not os.path.exists(new_mission.detect_path):
        os.mkdir(new_mission.detect_path)

    new_mission.save()

    return get_all_missions(request)
    # return render(request, 'index.html')


def rename_mission(request):
    mission_id = request.POST.get('id')
    mission_new_name = request.POST.get('name')
    # mission_id = 4
    cur_mission = Mission.objects.get(id=mission_id)
    cur_mission.name = mission_new_name
    return get_all_missions(request)


def get_mission_info(request):
    # mission_id = request.POST.get('id')
    mission_id = 4
    cur_mission = Mission.objects.get(id=mission_id)
    cur_image_path = cur_mission.image_path
    cur_detect_path = cur_mission.detect_path
    # cur_mission_name = cur_mission.name
    if not os.path.exists(cur_image_path):
        os.mkdir(cur_image_path)
    if not os.path.exists(cur_detect_path):
        os.mkdir(cur_detect_path)

    images = []
    urls = []
    for root, dirs, files in os.walk(cur_detect_path):
        for file in files:
            if os.path.splitext(file)[1] in ['.JPG', '.jpg', '.png', '.bmp']:
                # url = os.path.join('127.0.0.1:8080', 'media', cur_image_path[len(settings.MEDIA_ROOT)+1:], file)
                url = os.path.join('47.99.180.225:8080', 'media', cur_image_path[len(settings.MEDIA_ROOT)+1:], file)
                # url = os.path.join('127.0.0.1:8080', 'media', cur_detect_path[len(settings.MEDIA_ROOT)+1:], file)
                images.append(file)
                urls.append(url)

    print('urls:  ', urls)
    print('images:', images)
    # detect_result = json.load(open(os.path.join(cur_detect_path, 'detect_result.json')))
    detect_result_path = os.path.join(cur_detect_path, 'detect_result.json')
    if os.path.exists(detect_result_path):
        detect_result = json.load(open(detect_result_path))
    else:
        detect_result = {'results': []}
        print(detect_result)
        with open(detect_result_path, 'w') as f:
            json.dump(detect_result, f)

    response = JsonResponse(
        {
            'success': 'true',
            'urls': urls,
            'images': images,
            'detect_result': detect_result,
        }
    )
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    print(response.content)
    return response
    # return render(request, 'index.html')


def upload(request):
    # mission_id = request.POST.get('id')
    mission_id = 4

    cur_mission = Mission.objects.get(id=mission_id)
    cur_image_path = cur_mission.image_path
    cur_detect_path = cur_mission.detect_path
    # cur_mission_name = cur_mission.name

    print("cur_image_path:     ", cur_image_path)
    if not os.path.exists(cur_image_path):
        os.mkdir(cur_image_path)
    if not os.path.exists(cur_detect_path):
        os.mkdir(cur_detect_path)
        print("mkdir done")
    print("cur_detect_path:     ", cur_detect_path)

    # file_list = request.POST.get('file_list').split(',')
    # print(file_list)
    image_list = request.FILES.getlist('img')
    print(len(image_list))
    for image_file in image_list:
        destination = open(os.path.join(cur_image_path, image_file.name), 'wb')
        for chunk in image_file.chunks():
            destination.write(chunk)
        destination.close()
        # cur_mission.image_list.append(image_file)

    # print("detecting")
    image_detection(cur_image_path, cur_detect_path)

    cur_result = json.load(open(os.path.join(cur_detect_path, 'alert_result.json')))
    print(cur_result)

    detect_result_path = os.path.join(cur_detect_path, 'detect_result.json')
    if os.path.exists(detect_result_path):
        detect_result = json.load(open(detect_result_path))
        detect_result['results'] += cur_result['results']
        with open(detect_result_path, 'w') as f:
            json.dump(detect_result, f)
    else:
        detect_result = cur_result
        with open(detect_result_path, 'w') as f:
            json.dump(detect_result, f)

    return get_mission_info(request)
    # get_mission_info(request)
    # upload_page_id = 0
    # app_functions = ['单类别目标检测', '多类别目标检测']
    # class_names = [["工程车辆"], ["挖掘机", "推土机", "运输车"]]
    # return render(request, 'upload_demo.html',
    #                   {
    #                       'upload_page_id': upload_page_id,
    #                       'app_function': app_functions[upload_page_id],
    #                       'class_names': class_names[upload_page_id],
    #                       'upload_path': cur_image_path,
    #                       # 'upload_name': upload_name
    #                   })


def image_detection(src_image_path, detect_path):
    print("image detecting...")
    os.system("python " + DETECT_SCRIPT_PATH + " --test_image_path== " + src_image_path + "  --result_path== " +detect_path)
    print("detection finished!")


def serializable_object(node):
    obj = {'name': node.name, 'id': node.id, 'image_path': node.image_path, 'detect_path': node.detect_path, 'children': [],}
    for child in node.get_children():
        obj['children'].append(serializable_object(child))
    return obj

