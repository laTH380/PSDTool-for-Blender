from psd_tools import PSDImage
from PIL import Image

def main():
    # PSDファイルの読み込み
    psd = PSDImage.open('./test/小春六花ver1.1_めじろーす_im11070159.psd')

    psd_list = []

    # psd_list作成
    for index,layer in enumerate(psd):
        if layer.is_group():# レイヤーがグループの場合、その中のレイヤーも処理
            sublayer_list = []
            for sublayer in layer:
                layer_info = [sublayer.left, sublayer.top, sublayer.visible]
                sublayer_list.append(layer_info)
            psd_list.append(sublayer_list)
        else:# レイヤーが単独のレイヤーの場合
            psd_list.append([[layer.left, layer.top, layer.visible]])

    combined_image = Image.new('RGBA', psd.size)
    for group_index,item in enumerate(psd_list):
        if len(item) == 1:
            if item[0][2]:
                layer_image = psd[group_index].composite()
                combined_image.paste(layer_image, (item[0][0], item[0][1]), layer_image)
        else:# グループレイヤーの場合
            for layer_index, layer_info in enumerate(item):
                if layer_info[2]:
                    layer_image = psd[group_index][layer_index].composite()
                    combined_image.paste(layer_image, (layer_info[0], layer_info[1]), layer_image)
    combined_image.show()

if __name__ == "__main__":
    main()