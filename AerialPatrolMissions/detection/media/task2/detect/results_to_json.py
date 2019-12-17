# 自己写的转所需json文件的代码
import json
import os

def det2json(dataset, results):
    json_dict = {'images':[]}
    print('the num of images is %d' %len(dataset))
    for idx in range(len(dataset)):
        img_name = dataset.img_infos[idx]['file_name']
        height = dataset.img_infos[idx]['height']
        width = dataset.img_infos[idx]['width']

        result = results[idx]  # all box of single image
        one_img_ann = []
        for label in range(len(result)):
            bboxes = result[label]
            for i in range(bboxes.shape[0]):
                ann = dict()
                ann['bbox'] = xyxy2xywh(bboxes[i])
                ann['score'] = float(bboxes[i][4])
                ann['category_id'] = dataset.cat_ids[label]
                one_img_ann.append(ann)
        image_info={'file_name':img_name,'height':height,'width':width,'annotations':one_img_ann}
        json_dict['images'].append(image_info)
    return json_dict

def xyxy2xywh(bbox):
    _bbox = bbox.tolist()
    return [
        _bbox[0],
        _bbox[1],
        _bbox[2] - _bbox[0] + 1,
        _bbox[3] - _bbox[1] + 1,
    ]

def resultstojson(dataset, results, out_file):
    print("\n"+out_file)
    if isinstance(results[0], list):
        json_dict = det2json(dataset, results)
        path = out_file+'.json'
        with open(path, 'w') as f:
            json.dump(json_dict, f)
    else:
        raise TypeError('invalid type of results')