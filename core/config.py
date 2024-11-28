from typing import List

#PSDTOOLで使用する画像の名付け用
def make_name_for_psdtool(kindID: int=0, objectID: int=0, frame: int=0, layer_index: List[int]=[0,0,0,0,0]):
    name = "PSDTOOL_"
    if kindID == 0:#レイヤー画像用ネーミング
        layer_name = ""
        for layer_length in layer_index:
            str_layer_length = str(layer_length).zfill(3)
            layer_name += str_layer_length
        name += str(objectID) + "_layer_" + layer_name
    elif kindID == 1:#フレームごとのテクスチャ画像ネーミング
        name += str(objectID) + "_frame_" + str(frame).zfill(7)
    elif kindID == 2:#meshデータネーミング
        name += str(objectID) + "_mesh"
    else:
        print("naming error")
    return name