#!/usr/bin/env python3
"""
PSDTool for Blender リリース用自動化スクリプト
リリース用zipファイルを自動生成します。
"""

import os
import shutil
import zipfile
import re
from pathlib import Path

def get_version_from_init():
    """__init__.pyからバージョン情報を取得"""
    init_file = Path("__init__.py")
    if not init_file.exists():
        raise FileNotFoundError("__init__.py が見つかりません")
    
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # "version" : (1, 2, 0) の形式を検索
    version_match = re.search(r'"version"\s*:\s*\((\d+),\s*(\d+),\s*(\d+)\)', content)
    if not version_match:
        raise ValueError("バージョン情報が見つかりません")
    
    major, minor, patch = version_match.groups()
    return f"{major}.{minor}.{patch}"

def create_release_directory(version):
    """リリース用ディレクトリを作成"""
    release_name = f"PSDTool_for_Blender_{version}"
    release_dir = Path("releases") / "src" / release_name
    
    # 既存のディレクトリがあれば削除
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir(parents=True, exist_ok=True)
    return release_dir

def copy_release_files(release_dir):
    """リリースに必要なファイルをコピー"""
    # コピー対象のファイル・フォルダ
    files_to_copy = [
        "__init__.py",
        "utils.py", 
        "license",
        "README.md",
        "readme2.png"
    ]
    
    folders_to_copy = [
        "core",
        "operators", 
        "panels",
        "properties",
        "ex-library"
    ]
    
    # ファイルをコピー
    for file_name in files_to_copy:
        src = Path(file_name)
        if src.exists():
            dst = release_dir / file_name
            shutil.copy2(src, dst)
            print(f"✅ コピー完了: {file_name}")
        else:
            print(f"⚠️  ファイルが見つかりません: {file_name}")
    
    # フォルダを再帰的にコピー
    for folder_name in folders_to_copy:
        src = Path(folder_name)
        if src.exists():
            dst = release_dir / folder_name
            shutil.copytree(src, dst)
            print(f"✅ フォルダコピー完了: {folder_name}")
        else:
            print(f"⚠️  フォルダが見つかりません: {folder_name}")

def clean_pycache(release_dir):
    """__pycache__フォルダを削除"""
    for pycache_dir in release_dir.rglob("__pycache__"):
        shutil.rmtree(pycache_dir)
        print(f"🗑️  削除: {pycache_dir}")

def create_zip(release_dir, version):
    """zipファイルを作成"""
    zip_name = f"PSDTool_for_Blender_{version}.zip"
    zip_path = Path("releases") / zip_name
    
    # 既存のzipがあれば削除
    if zip_path.exists():
        os.remove(zip_path)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = Path(root) / file
                # releases/src/PSDTool_for_Blender_{version}/ からの相対パスを計算
                arcname = file_path.relative_to(release_dir.parent.parent) 
                zipf.write(file_path, arcname)
                print(f"📦 zip追加: {arcname}")
    
    return zip_path

def main():
    """メイン処理"""
    print("🚀 PSDTool for Blender リリース用zip作成を開始...")
    
    try:
        # カレントディレクトリの確認
        if not Path("__init__.py").exists():
            raise FileNotFoundError("PSDTool-for-Blenderのルートディレクトリで実行してください")
        
        # バージョン取得
        version = get_version_from_init()
        print(f"📋 検出されたバージョン: {version}")
        
        # リリースディレクトリ作成
        release_dir = create_release_directory(version)
        print(f"📁 リリースディレクトリ作成: {release_dir}")
        
        # ファイルコピー
        print("📄 ファイルをコピー中...")
        copy_release_files(release_dir)
        
        # クリーンアップ
        print("🧹 __pycache__を削除中...")
        clean_pycache(release_dir)
        
        # zip作成
        print("📦 zipファイルを作成中...")
        zip_path = create_zip(release_dir, version)
        
        print(f"\n✅ リリース完了!")
        print(f"📦 作成されたzip: {zip_path}")
        print(f"📏 ファイルサイズ: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        # 次のステップの案内
        print(f"\n📝 次のステップ:")
        print(f"1. README.mdの更新")
        print(f"2. mainブランチへのマージ")
        print(f"3. GitHubでのリリース作成 (v{version})")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
