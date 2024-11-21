from psd_tools import PSDImage
from PIL import Image
import os

import bpy
import utils

# import os
# import sys
# # PYTHONPATHにzipファイルを追加
# basepath = os.path.split(os.path.realpath(__file__))[0]
# print(os.path.join(basepath, 'ex-library'))
# sys.path.insert(0, os.path.join(basepath, 'ex-library'))
# # PILモジュールのロード
# import PIL
# from PIL import Image
# from psd_tools import PSDImage

#Blenderオペレータから呼ばれる関数
def make_psd_data(psd_path):
    psd = PSDImage.open(psd_path)
    psd_info, layer_images, layer_nums = _first_process_psd(psd)
    first_image = _make_image(psd,psd_info)
    name = os.path.basename(psd_path)
    return first_image, layer_images, psd_info, name, layer_nums

max_depth = 0
def _first_process_psd(psd):
    psd_info = []
    layer_images = []#psd_infoと同じ構造でレイヤーごとの画像データが入っている
    layer_nums = []#psd_infoと同じ構造でレイヤーの数が入っている[0,0,0,1...]0はグループでない場合、それ以外はサブレイヤーの数
    layer_struct = []
    for index,layer in enumerate(psd):
        layer_struct_item,_ = _recur_make_psd_struct(layer)
        layer_struct.append(layer_struct_item)
        psd_info.append({"x":layer.left, "y":layer.top, "visible":layer.visible, "name":layer.name})
        if layer.is_group():# レイヤーがグループの場合、その中のレイヤーも処理
            layer_nums.append(len(layer))
            sublayer_info = []
            sublayer_images = []
            for sublayer in layer:
                layer_info = {"x":sublayer.left, "y":sublayer.top, "visible":sublayer.visible, "name":sublayer.name, "sublayer":None}
                sublayer_info.append(layer_info)
                sublayer_images.append(sublayer.composite())
            psd_info[index]["sublayer"] = sublayer_info
            layer_images.append(sublayer_images)
        else:
            layer_nums.append(0)
            psd_info[index]["sublayer"] = None
            layer_images.append([layer.composite()])
    utils.save_json_file(layer_struct, "./layer_struct.json")
    print(max_depth)
    return psd_info, layer_images, layer_nums

def _recur_make_psd_struct(layer, depth=0):
    depth = depth
    global max_depth
    if max_depth < depth:
        max_depth = depth
    if layer.is_group():
        sublayer_struct = []
        for sublayer in layer:
            subsublayer_struct,depth = _recur_make_psd_struct(sublayer, depth+1)
            sublayer_struct.append(subsublayer_struct)
        layer_struct = _psd_layer_to_dict(layer.left, layer.top, layer.visible, layer.name, sublayer_struct)
        return layer_struct, depth-1
    else:
        layer_struct = _psd_layer_to_dict(layer.left, layer.top, layer.visible, layer.name)
        return layer_struct, depth-1

def _psd_layer_to_dict(x, y, visible, name, sublayer=None):
    result = {}
    result["x"] = x
    result["y"] = y
    result["visible"] = visible
    result["name"] = name
    result["sublayer"] = sublayer
    return result


def _make_image(psd,psd_info):
    combined_image = Image.new('RGBA', psd.size)
    for group_index,item in enumerate(psd_info):
        if item["visible"]:
            if item["sublayer"] is None:# グループレイヤーでない場合
                layer_image = psd[group_index].composite()
                combined_image.paste(layer_image, (item["x"], item["y"]), layer_image)
            else:
                for layer_index, layer_info in enumerate(item["sublayer"]):
                    if layer_info["visible"]:
                        layer_image = psd[group_index][layer_index].composite()
                        combined_image.paste(layer_image, (layer_info["x"], layer_info["y"]), layer_image)
    # combined_image.show()
    return combined_image

if __name__ == "__main__":
    make_psd_data("./test/小春六花ver1.1_めじろーす_im11070159.psd")