# プログラム構成
- __init__.py : アドオンのコア。ほかのファイルからインポートし、登録や削除機能など
- io_import_psd_as_planes.py : このアドオンの中核機能を持つオペレータ作成ファイル
- main_operator.py : 使われていないオペレータが置いたるファイル
- process_psd.py : psdファイルの処理
- control_property.py : カスタムプロパティとそのアクセッサの定義