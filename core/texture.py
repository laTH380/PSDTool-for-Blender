import os
import bpy
import tempfile
from core import config

def get_packed_image_by_name(image_name):
    image = bpy.data.images.get(image_name)
    if image and image.packed_file:
        return image
    else:
        print(f"Image '{image_name}' が見つからないか、パックされていません。")
        return None
    
def paccking_merged_image_to_blender(image):
    name = config.make_name_for_psdtool(kindID=1, frame=bpy.context.scene.frame_current)
    paccking_image_to_blender(image, name)
    return name
    
#　paccking image object to .blend file
def paccking_image_to_blender(image, name):
    # Blenderの一時ディレクトリを取得
    temp_dir = tempfile.mkdtemp(prefix='blender_temp_')
    # 仮の画像ファイルパスを作成
    temp_image_path = os.path.join(temp_dir, name + ".png")
    # 仮の画像データを一時ファイルに保存
    image.save(temp_image_path, format="PNG")
    # 画像をBlenderにロード,パック
    loaded_image = bpy.data.images.load(temp_image_path)
    loaded_image.name = name
    loaded_image.pack()
    # パックが成功したかどうかを確認
    if loaded_image.packed_file:
        print(f"Image '{loaded_image.name}' is packed into the .blend file.")
    else:
        print(f"Failed to pack image '{loaded_image.name}' into the .blend file.")
    # 一時ファイルを削除する
    os.remove(temp_image_path)