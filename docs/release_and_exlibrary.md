# ex-library 作成とリリース手順

このアドオンは依存ライブラリを `ex-library/` に同梱して配布する運用です。
単一配布で Blender 3.6 / 4.5 を両対応する場合は、Python バージョン別に同梱します。

## 前提
- 作業ディレクトリ: リポジトリルート
- Blender 4.5 LTS 同梱 Python: `3.11.x`
- `ex-library/` は `.gitignore` 対象（通常は Git 管理しない）

## 1. ex-library を作成/更新する（単一配布で複数 Blender 対応）
- Blender 3.6 用（Python 3.10）を生成:
  ```powershell
  .\venv2exlib.ps1 -BlenderPython "<blender3.6のpython.exe>"
  ```
- Blender 4.5 用（Python 3.11）を生成:
  ```powershell
  .\venv2exlib.ps1 -BlenderPython "<blender4.5のpython.exe>"
  ```
- 生成先は自動で `ex-library/py310` / `ex-library/py311` のように分かれます。
- `BLENDER_PYTHON` 環境変数を設定しておけば `-BlenderPython` は省略可能です（その場合は 1 実行で 1 バージョン分のみ生成）。
- バイナリ依存（例: Pillow）は Python バージョン互換が必要です。Blender 側 Python と一致する実行ファイルを必ず指定してください。

## 2. アドオン動作確認
- Blender でアドオンを有効化
- 依存不足ログ（`Missing dependencies`）が出ないことを確認

## 3. リリース zip を作成
`create_release.py` を実行すると、`releases/` に zip が生成されます。

```powershell
python create_release.py
```

このスクリプトは `ex-library/` を含めてコピーし、zip 化します。

## 4. 配布前チェック
- `__init__.py` の `bl_info["version"]` を更新済み
- README の更新履歴を更新済み
- 生成物: `releases/PSDTool_for_Blender_<version>.zip`
