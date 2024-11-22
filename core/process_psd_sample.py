from psd_tools import PSDImage

def main():
    # PSDファイルの読み込み
    psd = PSDImage.open('./test/小春六花ver1.1_めじろーす_im11070159.psd')

    # PSDファイルの情報を表示
    print(f'Number of layers: {len(psd)}')

    # レイヤーを反復処理
    for layer in psd:
        print(f'Layer name: {layer.name}')
        print(f'Layer size: {layer.size}')

        # レイヤーを画像として保存する場合
        if layer.is_group():
            # レイヤーがグループの場合、その中のレイヤーも処理
            for sublayer in layer:
                sublayer_image = sublayer.composite()
                sublayer_image.save(f'{sublayer.name}.png')
        else:
            # レイヤーが単独のレイヤーの場合
            layer_image = layer.composite()
            layer_image.save(f'{layer.name}.png')

    # PSD全体を画像として保存
    psd.composite().save('output.png')


if __name__ == "__main__":
    main()