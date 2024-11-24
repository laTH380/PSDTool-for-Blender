from typing import List

#PSDToolKitで使用する画像の名付け用
def make_name_for_psdtool(kindID: int=0, frame: int=0, layer_index: List[int]=[0,0,0,0,0]):
    objectID = 0
    ID1 = 0
    ID2 = 0
    name = "PSDToolKit_"
    if kindID == 0:#レイヤー画像用ネーミング
        layer_name = ""
        for layer_length in layer_index:
            str_layer_length = str(layer_length).zfill(3)
            layer_name += str_layer_length
        name += "_layer_" + layer_name
    elif kindID == 1:#テクスチャ画像ネーミング
        name += "_frame_" + str(frame).zfill(7)
    elif kindID == 2:#オブジェクトデータネーミング
        name += str(objectID) + "_mesh"
    else:
        print("naming error")
    return name