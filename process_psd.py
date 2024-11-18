from psd_tools import PSDImage
from PIL import Image
import os

import bpy

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
    psd_info, layer_images = _first_process_psd(psd)
    first_image = _make_image(psd,psd_info)
    name = os.path.basename(psd_path)
    return first_image, layer_images, psd_info, name


def _first_process_psd(psd):
    psd_info = []
    layer_images = []#psd_infoと同じ構造でレイヤーごとの画像データが入っている
    for index,layer in enumerate(psd):
        psd_info.append({"x":layer.left, "y":layer.top, "visible":layer.visible, "name":layer.name})
        if layer.is_group():# レイヤーがグループの場合、その中のレイヤーも処理
            sublayer_info = []
            sublayer_images = []
            for sublayer in layer:
                layer_info = {"x":sublayer.left, "y":sublayer.top, "visible":sublayer.visible, "name":sublayer.name, "sublayer":None}
                sublayer_info.append(layer_info)
                sublayer_images.append(sublayer.composite())
            psd_info[index]["sublayer"] = sublayer_info
            layer_images.append(sublayer_images)
        else:
            psd_info[index]["sublayer"] = None
            layer_images.append([layer.composite()])
    return psd_info, layer_images

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
    combined_image.show()
    return combined_image

if __name__ == "__main__":
    make_psd_data("./test/小春六花ver1.1_めじろーす_im11070159.psd")