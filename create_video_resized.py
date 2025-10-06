#!/usr/bin/env python3
"""
動画生成スクリプト

スクリーンショットと音声ファイルを組み合わせて、
テニスゲームの解説動画を自動生成します。

機能:
- 各シーンごとの動画セグメント作成
- 音声同期での静止画表示
- 高品質H.264エンコーディング
- 全セグメントの結合
"""

import subprocess  # ffmpegコマンド実行用
import os          # ファイル操作とディレクトリ管理用

# 動画出力設定
output_video = "tennis_game_tutorial.mp4"  # 最終出力ファイル名
resolution = "1920x1080"                    # フルHD解像度
fps = 30                                    # フレームレート（秒間30フレーム）
video_codec = "libx264"                     # H.264ビデオコーデック
audio_codec = "aac"                         # AACオーディオコーデック

# シーン定義：各セクションの表示時間設定
# ナレーション音声の長さに基づいて推定された表示時間
# duration: メイン表示時間（秒）, gap: シーン間の無音間隔（秒）
scenes = [
    {'id': 'scene01', 'duration': 12.0, 'gap': 1.0},  # HTML構造とメタデータ
    {'id': 'scene02', 'duration': 15.0, 'gap': 1.0},  # CSSスタイル
    {'id': 'scene03', 'duration': 10.0, 'gap': 1.0},  # HTML本体
    {'id': 'scene04', 'duration': 12.0, 'gap': 1.0},  # JavaScript初期設定
    {'id': 'scene05', 'duration': 18.0, 'gap': 1.0},  # ゲームオブジェクト
    {'id': 'scene06', 'duration': 15.0, 'gap': 1.0},  # 描画関数
    {'id': 'scene07', 'duration': 20.0, 'gap': 1.0},  # AI制御システム
    {'id': 'scene08', 'duration': 25.0, 'gap': 1.0},  # プレイヤー制御とボール物理
    {'id': 'scene09', 'duration': 15.0, 'gap': 1.0},  # スコア管理
    {'id': 'scene10', 'duration': 12.0, 'gap': 1.0},  # メインループと描画
    {'id': 'scene11', 'duration': 12.0, 'gap': 1.0},  # キーボード入力処理
    {'id': 'scene12', 'duration': 18.0, 'gap': 0.0},  # 難易度設定（最後なので無音なし）
]

# Scene name mapping
scene_names = {
    'scene01': 'html_structure',
    'scene02': 'css_styles',
    'scene03': 'html_body',
    'scene04': 'js_initialization',
    'scene05': 'game_objects',
    'scene06': 'drawing_functions',
    'scene07': 'ai_system',
    'scene08': 'player_ball_physics',
    'scene09': 'score_management',
    'scene10': 'main_loop',
    'scene11': 'keyboard_input',
    'scene12': 'difficulty_start'
}

# Create a temporary directory for intermediate files
temp_dir = "temp_video_files"
os.makedirs(temp_dir, exist_ok=True)

print("Creating video segments for each scene...")
print(f"Target resolution: {resolution}")
print(f"Frame rate: {fps} fps")
print(f"Video codec: {video_codec}")
print(f"Audio codec: {audio_codec}")

# Process each scene
for i, scene in enumerate(scenes):
    scene_id = scene['id']
    duration = scene['duration']
    gap = scene['gap']
    total_duration = duration + gap

    print(f"\nProcessing {scene_id}...")

    # Find the correct image file
    scene_name = scene_names.get(scene_id, 'unknown')
    image_file = f"pic_resized/{scene_id}_{scene_name}.png"

    # Check if image file exists
    if not os.path.exists(image_file):
        print(f"  ✗ Error: Image file {image_file} not found")
        continue

    audio_file = f"audio/{scene_id}_narration.mp3"

    # Check if audio file exists
    if not os.path.exists(audio_file):
        print(f"  ✗ Error: Audio file {audio_file} not found")
        continue

    video_segment = f"{temp_dir}/{scene_id}_video.mp4"

    # Create video segment with audio
    cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', image_file,
        '-i', audio_file,
        '-c:v', video_codec,
        '-tune', 'stillimage',
        '-c:a', audio_codec,
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-s', resolution,
        '-r', str(fps),
        '-t', str(total_duration),
        '-shortest',
        video_segment,
        '-y'
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✓ Created video segment: {video_segment}")
        print(f"  Duration: {total_duration:.1f}s (content: {duration:.1f}s, gap: {gap:.1f}s)")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error creating video segment: {e}")
        print(f"    stderr: {e.stderr.decode()}")
        continue

# Create concat file
concat_file = f"{temp_dir}/concat.txt"
with open(concat_file, 'w') as f:
    for scene in scenes:
        video_file = f"{temp_dir}/{scene['id']}_video.mp4"
        if os.path.exists(video_file):
            f.write(f"file '{os.path.abspath(video_file)}'\n")

print(f"\nConcatenating all video segments...")

# Concatenate all videos
concat_cmd = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', concat_file,
    '-c', 'copy',
    output_video,
    '-y'
]

try:
    subprocess.run(concat_cmd, check=True, capture_output=True)
    print(f"\n✓ Successfully created video: {output_video}")

    # Get video info
    probe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,r_frame_rate,duration',
        '-of', 'default=noprint_wrappers=1',
        output_video
    ]

    try:
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        print(f"\nVideo info:")
        print(result.stdout)
    except:
        pass

    # Get file size
    file_size = os.path.getsize(output_video) / (1024 * 1024)  # MB
    print(f"File size: {file_size:.2f} MB")

except subprocess.CalledProcessError as e:
    print(f"\n✗ Error concatenating videos: {e}")
    print(f"  stderr: {e.stderr.decode()}")

# Clean up temporary files
print("\nCleaning up temporary files...")
for file in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, file))
os.rmdir(temp_dir)
print("✓ Cleanup complete")

print(f"\nVideo creation complete! Output file: {output_video}")
print("\nTo update durations based on actual audio length, run:")
print("python generate_audio.py")
print("Then check the reported durations and update the 'scenes' list in this script.")