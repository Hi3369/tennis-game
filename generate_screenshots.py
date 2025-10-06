#!/usr/bin/env python3
"""
テニスゲームのスクリーンショット画像生成スクリプト

index.htmlファイルを12のセクションに分割し、各セクションの
コードスクリーンショットを自動生成します。

出力:
    pic/フォルダに scene01_xxx.png から scene12_xxx.png まで12枚の画像
"""

import os    # ディレクトリ作成とファイル操作用
import sys   # システム操作用
from code_to_image_simple import SimpleCodeImageGenerator  # 画像生成クラス

# ソースコードファイル（index.html）の読み込み
# UTF-8エンコーディングで行ごとにリストとして読み込み
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# シーン定義：各セクションの行番号範囲と出力ファイル名
# テニスゲームのコードを12の論理的なセクションに分割
scenes = [
    {'name': 'scene01_html_structure', 'start': 1, 'end': 66},
    {'name': 'scene02_css_styles', 'start': 7, 'end': 65},
    {'name': 'scene03_html_body', 'start': 67, 'end': 82},
    {'name': 'scene04_js_initialization', 'start': 84, 'end': 99},
    {'name': 'scene05_game_objects', 'start': 90, 'end': 128},
    {'name': 'scene06_drawing_functions', 'start': 129, 'end': 157},
    {'name': 'scene07_ai_system', 'start': 159, 'end': 178},
    {'name': 'scene08_player_ball_physics', 'start': 180, 'end': 233},
    {'name': 'scene09_score_management', 'start': 235, 'end': 258},
    {'name': 'scene10_main_loop', 'start': 260, 'end': 279},
    {'name': 'scene11_keyboard_input', 'start': 281, 'end': 303},
    {'name': 'scene12_difficulty_start', 'start': 305, 'end': 338}
]

# 出力ディレクトリ 'pic' の作成（既存の場合は何もしない）
os.makedirs('pic', exist_ok=True)

# 画像生成器のインスタンス作成
# ライトテーマを使用（印刷時やプレゼンテーションでの視認性向上のため）
# フォントサイズは16px（デフォルトの14pxより大きくして読みやすく）
generator = SimpleCodeImageGenerator(theme='light', font_size=16)

print("テニスゲームのスクリーンショット生成を開始...")

# 各シーンのスクリーンショット生成ループ
for scene in scenes:
    # 対象行の抽出（Pythonのインデックスは0から始まるため-1）
    scene_lines = lines[scene['start']-1:scene['end']]
    # リストの行を結合して文字列に変換
    scene_code = ''.join(scene_lines)

    # 出力ファイルパスとタイトルの生成
    output_path = f"pic/{scene['name']}.png"
    title = f"index.html - Lines {scene['start']}-{scene['end']}"

    # 進行状況の表示
    print(f"Generating {output_path}...")
    # 実際の画像生成処理を実行
    generator.generate_image(scene_code, output_path, title=title)

# 処理完了メッセージ
print(f"\n✓ 全{len(scenes)}枚のスクリーンショットが正常に生成されました！")
print("スクリーンショットは 'pic' ディレクトリに保存されています。")