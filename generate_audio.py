#!/usr/bin/env python3
"""
Generate audio files for each scene using macOS say command or espeak on Linux
"""

import os
import subprocess
import time
import sys

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

# Detect OS and set TTS system
def detect_tts_system():
    """Detect available TTS system"""
    try:
        # Try macOS say command
        subprocess.run(['say', '--version'], capture_output=True, check=True)
        return 'macos'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    try:
        # Try espeak (Linux)
        subprocess.run(['espeak', '--version'], capture_output=True, check=True)
        return 'linux'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return None

tts_system = detect_tts_system()

if tts_system == 'macos':
    # macOS settings
    voice = 'Kyoko'  # Female Japanese voice
    rate = 225  # Speech rate (words per minute) - 1.5x faster than default 150
    print(f"Using macOS say command with voice: {voice}")
    print(f"Speech rate: {rate} words per minute\n")
elif tts_system == 'linux':
    print("Using Linux espeak for audio generation\n")
else:
    print("No suitable TTS system found. Please install:")
    print("- macOS: say command (built-in)")
    print("- Linux: sudo apt-get install espeak espeak-data-ja")
    sys.exit(1)

# Generate audio for each scene
for scene in scenes:
    output_file = f"audio/{scene['id']}_narration.aiff"
    mp3_file = f"audio/{scene['id']}_narration.mp3"

    print(f"Generating audio for {scene['id']}...")

    if tts_system == 'macos':
        # Create the say command
        cmd = [
            'say',
            '-v', voice,
            '-r', str(rate),
            '-o', output_file,
            scene['text']
        ]
    elif tts_system == 'linux':
        # Create the espeak command
        cmd = [
            'espeak',
            '-v', 'ja',  # Japanese voice
            '-s', '150',  # Speed (words per minute)
            '-w', output_file,  # Output to wav file
            scene['text']
        ]

    try:
        # Execute the command
        subprocess.run(cmd, check=True)
        print(f"  ✓ Saved to {output_file}")

        # Get file info
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / 1024 / 1024  # MB
            print(f"  File size: {file_size:.2f} MB")

    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error generating audio: {e}")
        continue
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        continue

print("\nConverting audio files to MP3...")

# Convert audio to MP3 for smaller file size
for scene in scenes:
    if tts_system == 'macos':
        input_file = f"audio/{scene['id']}_narration.aiff"
    else:
        input_file = f"audio/{scene['id']}_narration.wav"

    mp3_file = f"audio/{scene['id']}_narration.mp3"

    if os.path.exists(input_file):
        print(f"Converting {scene['id']}...")
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-acodec', 'mp3',
            '-ab', '128k',
            mp3_file,
            '-y'  # Overwrite output file
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✓ Converted to {mp3_file}")

            # Remove the original file
            os.remove(input_file)
            print(f"  ✓ Removed {input_file}")

        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error converting to MP3: {e}")
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")

print("\nAll audio files generated successfully!")

# Calculate duration of each audio file
print("\nAudio file durations:")
for scene in scenes:
    mp3_file = f"audio/{scene['id']}_narration.mp3"
    if os.path.exists(mp3_file):
        # Get duration using ffprobe
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
            print(f"  {scene['id']}: Unable to get duration")