#!/usr/bin/env python3
"""
音声ファイル生成スクリプト（Google Text-to-Speech使用）

各シーン用の日本語音声ナレーションファイルを自動生成します。
システムレベルのTTSインストールが不要で、インターネット経由で
Google TTSサービスを利用します。

出力:
    audio/フォルダに scene01_narration.mp3 から scene12_narration.mp3 まで12個のMP3ファイル
"""

import os          # ディレクトリ作成とファイル操作用
import subprocess  # 外部コマンド実行（pip install、ffprobe）用
import time        # 時間操作用（将来の拡張用）
import sys         # システム操作とpipインストール用

# Google Text-to-Speechライブラリのインポートと自動インストール
# gTTSが利用できない場合は自動的にインストールを試行
try:
    from gtts import gTTS    # Google Text-to-Speech メインクラス
    import tempfile          # 一時ファイル処理用
    print("gTTS (Google Text-to-Speech) を使用します")
except ImportError:
    # gTTSがインストールされていない場合の自動インストール
    print("gTTS が見つかりません。インストールを開始...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages', 'gtts'], check=True)
    from gtts import gTTS
    import tempfile
    print("gTTS のインストールが完了し、使用準備ができました")

# Define the narration text for each scene
scenes = [
    {
        'id': 'scene01',
        'text': '''このテニスゲームは、HTML5のCanvasを使用したクラシックなPongスタイルのゲームです。
HTMLの基本構造では、meta要素でビューポートとエンコーディングを設定し、
日本語タイトル「クラシックテニスゲーム」を表示します。
CSSスタイルで全体のレイアウトとデザインを定義しています。'''
    },
    {
        'id': 'scene02',
        'text': '''CSSでは、ダークテーマのデザインを採用しています。
bodyは黒背景に設定し、Flexboxレイアウトでゲームをページ中央に配置します。
gameCanvasには白いボーダーを付け、スコア表示には等幅フォント「Courier New」を使用しています。
ボタンとセレクトボックスには統一されたスタイルを適用し、ホバー効果も実装しています。'''
    },
    {
        'id': 'scene03',
        'text': '''HTML本体部分では、スコア表示、800×400ピクセルのCanvas要素、
操作説明、難易度選択、ゲーム開始ボタンを配置しています。
プレイヤーは矢印キーの上下でパドルを操作し、
AIが自動でコンピューターのパドルを制御します。'''
    },
    {
        'id': 'scene04',
        'text': '''JavaScriptでは、まずHTML要素への参照を取得します。
canvas、コンテキスト、スコア表示、開始ボタン、難易度選択の要素を取得し、
ゲームの基本設定を定義するgameオブジェクトを作成します。
ボール速度、パドル速度、AI設定などの重要なパラメーターを管理しています。'''
    },
    {
        'id': 'scene05',
        'text': '''プレイヤー、AI、ボールの各オブジェクトを定義します。
プレイヤーは画面右側、AIは左側に配置し、それぞれ位置、サイズ、スコアを管理します。
ボールオブジェクトには、位置、速度、軌跡表示用の配列を含めています。
これらのオブジェクトがゲームの状態を管理する中核となります。'''
    },
    {
        'id': 'scene06',
        'text': '''描画関数群では、ゲーム画面の各要素を描画します。
drawPaddle関数でパドルを白い矩形として描画し、
drawBall関数ではボールの軌跡効果も含めて円を描画します。
drawNet関数は、画面中央に点線のネットを描画し、
クラシックなPongゲームの見た目を再現しています。'''
    },
    {
        'id': 'scene07',
        'text': '''AI制御システムは、非常に高度な予測システムを実装しています。
ボールがAI側に向かっているとき、ボールの軌道を予測計算し、
エラー率を加えることで人間らしい不完全性を再現しています。
AIの反応距離や速度は難易度設定によって調整され、
リアルな対戦相手としての体験を提供します。'''
    },
    {
        'id': 'scene08',
        'text': '''プレイヤー制御では、矢印キーの入力に基づいてパドルを移動させます。
ボール物理システムでは、軌跡効果、壁での反射、パドルとの衝突判定を処理します。
パドル衝突時には、衝突位置に応じてボールの角度が変化し、
速度も1.05倍に増加することで、ゲームの緊張感を高めています。
ボールが画面端を通り抜けると、対応するプレイヤーのスコアが増加します。'''
    },
    {
        'id': 'scene09',
        'text': '''resetBall関数は、得点後にボールを画面中央にリセットし、
ランダムな方向と角度で新しいラウンドを開始します。
updateScore関数では、スコア表示を更新し、
11点に達したプレイヤーが勝利となります。
勝利時には日本語でメッセージを表示し、ゲームをリセットします。'''
    },
    {
        'id': 'scene10',
        'text': '''draw関数は、半透明な黒い矩形で軌跡効果を作り、
その上にネット、パドル、ボールを順序良く描画します。
gameLoop関数は、ゲームが実行中の間、
プレイヤー更新、AI更新、ボール更新、描画を順次実行し、
requestAnimationFrameで滑らかなアニメーションを実現します。'''
    },
    {
        'id': 'scene11',
        'text': '''キーボード入力処理では、keydownとkeyupイベントリスナーを設定しています。
矢印キーの上下でプレイヤーパドルの動作フラグを制御し、
preventDefaultでデフォルトのスクロール動作を防止します。
この仕組みにより、滑らかで応答性の良いパドル操作を実現しています。'''
    },
    {
        'id': 'scene12',
        'text': '''難易度設定システムでは、「かんたん」「ふつう」「むずかしい」の3段階を用意しています。
各難易度でAIの速度、反応距離、エラー率が変化し、
プレイヤーのスキルレベルに応じた挑戦を提供します。
ゲーム開始ボタンをクリックすると、設定を適用してゲームループを開始し、
UI要素を非表示にしてゲームに集中できる環境を作ります。'''
    }
]

# Create audio directory if it doesn't exist
os.makedirs('audio', exist_ok=True)

print("Generating audio files using gTTS...")
print("Language: Japanese (ja)")
print("Output format: MP3 (via gTTS)\n")

# Generate audio for each scene
for scene in scenes:
    mp3_file = f"audio/{scene['id']}_narration.mp3"

    print(f"Generating audio for {scene['id']}...")

    try:
        # Create gTTS object
        tts = gTTS(text=scene['text'], lang='ja', slow=False)

        # Save to file
        tts.save(mp3_file)
        print(f"  ✓ Saved to {mp3_file}")

        # Get file info
        if os.path.exists(mp3_file):
            file_size = os.path.getsize(mp3_file) / 1024 / 1024  # MB
            print(f"  File size: {file_size:.2f} MB")

    except Exception as e:
        print(f"  ✗ Error generating audio: {e}")
        continue

# メイン処理完了メッセージ
print("\n全ての音声ファイルが正常に生成されました！")

# Calculate duration of each audio file
print("\nAudio file durations:")
for scene in scenes:
    mp3_file = f"audio/{scene['id']}_narration.mp3"
    if os.path.exists(mp3_file):
        # Get duration using ffprobe if available
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            mp3_file
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            duration = float(result.stdout.strip())
            print(f"  {scene['id']}: {duration:.1f} seconds")
        except:
            print(f"  {scene['id']}: Duration unknown (ffprobe not available)")