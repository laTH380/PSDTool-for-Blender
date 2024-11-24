import os
import utils
from psd_tools import PSDImage
from PIL import Image

#################
# psdファイル空のデータ抽出およびpsdデータ空の画像生成
#################

max_depth = 0

def make_psd_data_from_psd(psd_path):
    psd = PSDImage.open(psd_path)
    psd_info, layer_images, layer_struct, max_depth = _first_process_psd(psd)
    first_image = _make_image_from_psd_data(psd_info, layer_struct, layer_images)
    psd_info["name"] = os.path.basename(psd_path)
    return psd_info, first_image, layer_images, layer_struct, max_depth #psd_info = {name, size}

def _first_process_psd(psd):
    layer_struct = []
    layer_images = []#psdと同じ構造でレイヤーごとの画像データが入っている
    psd_info = {"size":psd.size}
    for index, layer in enumerate(psd):
        layer_struct_item, _ = _recur_make_psd_struct(layer, layer_images)
        layer_struct.append(layer_struct_item)
    utils.save_json_file(layer_struct, "./layer_struct.json")
    return psd_info, layer_images, layer_struct, max_depth

def _recur_make_psd_struct(layer, layer_images, depth=0):
    depth = depth
    global max_depth
    if max_depth < depth:
        max_depth = depth
    if layer.is_group():
        sublayer_struct = []
        layer_images.append([])
        for sublayer in layer:
            subsublayer_struct,depth = _recur_make_psd_struct(sublayer, layer_images[-1], depth+1)
            sublayer_struct.append(subsublayer_struct)
        layer_struct = _psd_layer_to_dict(layer.left, layer.top, layer.visible, layer.name, sublayer_struct)
        return layer_struct, depth-1
    else:
        layer_struct = _psd_layer_to_dict(layer.left, layer.top, layer.visible, layer.name)
        layer_images.append([layer.composite()])
        return layer_struct, depth-1

def _psd_layer_to_dict(x, y, visible, name, sublayer=None):
    result = {}
    result["x"] = x
    result["y"] = y
    result["visible"] = visible
    result["name"] = name
    result["sublayer"] = sublayer
    return result


def _make_image_from_psd_data(psd_info, layer_struct, layer_images):
    print(layer_images)
    combined_image = Image.new('RGBA', psd_info["size"])
    for layer_index, layer in enumerate(layer_struct):
        _recur_make_image_psd_data(layer, combined_image, layer_images[layer_index])
    combined_image.show()
    return combined_image

def _recur_make_image_psd_data(layer, combined_image, layer_images):
    combined_image = combined_image
    if layer["visible"]:
        if layer["sublayer"] is None:
            layer_image = layer_images[0]
            combined_image.paste(layer_image, (layer["x"], layer["y"]), layer_image)
        else:
            for sublayer_index, sublayer in enumerate(layer["sublayer"]):
                combined_image = _recur_make_image_psd_data(sublayer, combined_image, layer_images[sublayer_index])
    return combined_image

def make_image(size):
    return Image.new('RGBA', size)

def merge_image(base_image, merged_image, x, y):
    return merged_image.paste(base_image, (x, y), base_image)


if __name__ == "__main__":
    make_psd_data_from_psd("./test/小春六花ver1.1_めじろーす_im11070159.psd")



