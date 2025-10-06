#!/usr/bin/env python3
"""
動画生成パイプライン統合実行スクリプト

テニスゲームのソースコード解説動画を自動生成する全工程を
ワンクリックで実行するメインスクリプトです。

処理フロー:
1. 必要なツール・ライブラリの確認
2. コードスクリーンショット生成
3. 音声ファイル生成
4. 画像リサイズ処理
5. 動画の編集・出力

このスクリプトを実行するだけで、完全な解説動画が自動生成されます。
"""

import os          # ファイルシステム操作用
import sys         # システム操作とプロセス制御用
import subprocess  # 外部スクリプト実行用

def check_requirements():
    """
    必要なツールとライブラリの存在確認

    動画生成に必要な全ての依存関係をチェックし、
    不足している場合は具体的なインストール方法を案内します。

    Returns:
        bool: 全ての要件が満たされている場合True
    """
    print("動作要件をチェック中...")

    # PIL/Pillow（画像処理ライブラリ）の確認
    try:
        import PIL
        print("✓ PIL/Pillow が利用可能です")
    except ImportError:
        print("✗ PIL/Pillow が見つかりません")
        return False

    # gTTS（Google Text-to-Speech）の確認
    try:
        import gtts
        print("✓ gTTS が利用可能です")
    except ImportError:
        print("✗ gTTS が見つかりません")
        return False

    # ffmpeg（動画編集ツール）の確認
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ ffmpeg が利用可能です")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ ffmpeg が見つかりません - 動画生成ができません")
        print("  インストール方法: sudo apt-get install ffmpeg")
        return False

    return True

def run_pipeline():
    """
    動画生成パイプラインの実行

    全ての工程を順次実行して、最終的な解説動画を生成します。
    各ステップでエラーが発生した場合は処理を中断し、エラー内容を報告します。

    Returns:
        bool: 全ての処理が成功した場合True
    """
    print("\n" + "="*60)
    print("テニスゲーム コード解説動画 自動生成システム")
    print("="*60)

    # Check if we have all files
    required_files = [
        'index.html',
        'code_to_image_simple.py',
        'generate_screenshots.py',
        'generate_audio_gtts.py',
        'resize_screenshots.py',
        'create_video_resized.py'
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"Missing files: {missing_files}")
        return False

    print("\nAll required files present ✓")

    # Step 1: Generate screenshots
    print("\n1. Generating screenshots...")
    try:
        subprocess.run([sys.executable, 'generate_screenshots.py'], check=True)
        print("✓ Screenshots generated")
    except subprocess.CalledProcessError as e:
        print(f"✗ Screenshot generation failed: {e}")
        return False

    # Step 2: Generate audio
    print("\n2. Generating audio files...")
    try:
        subprocess.run([sys.executable, 'generate_audio_gtts.py'], check=True)
        print("✓ Audio files generated")
    except subprocess.CalledProcessError as e:
        print(f"✗ Audio generation failed: {e}")
        return False

    # Step 3: Resize screenshots
    print("\n3. Resizing screenshots...")
    try:
        subprocess.run([sys.executable, 'resize_screenshots.py'], check=True)
        print("✓ Screenshots resized")
    except subprocess.CalledProcessError as e:
        print(f"✗ Screenshot resizing failed: {e}")
        return False

    # Step 4: Create video (if ffmpeg available)
    print("\n4. Creating video...")
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        subprocess.run([sys.executable, 'create_video_resized.py'], check=True)
        print("✓ Video created successfully!")

        # Show final video info
        if os.path.exists('tennis_game_tutorial.mp4'):
            size = os.path.getsize('tennis_game_tutorial.mp4') / (1024 * 1024)
            print(f"  Final video: tennis_game_tutorial.mp4 ({size:.2f} MB)")

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Video creation skipped - ffmpeg not available")
        print("  Install ffmpeg to complete video generation")
        return False

    return True

def show_summary():
    """Show summary of generated files"""
    print("\n" + "="*60)
    print("GENERATED FILES SUMMARY")
    print("="*60)

    # Screenshots
    if os.path.exists('pic'):
        screenshots = [f for f in os.listdir('pic') if f.endswith('.png')]
        print(f"\n📸 Screenshots (pic/): {len(screenshots)} files")
        for f in sorted(screenshots)[:3]:
            print(f"   - {f}")
        if len(screenshots) > 3:
            print(f"   ... and {len(screenshots) - 3} more")

    # Resized screenshots
    if os.path.exists('pic_resized'):
        resized = [f for f in os.listdir('pic_resized') if f.endswith('.png')]
        print(f"\n🖼️  Resized screenshots (pic_resized/): {len(resized)} files")

    # Audio files
    if os.path.exists('audio'):
        audio_files = [f for f in os.listdir('audio') if f.endswith('.mp3')]
        print(f"\n🔊 Audio files (audio/): {len(audio_files)} files")
        total_size = sum(os.path.getsize(f'audio/{f}') for f in audio_files)
        print(f"   Total audio size: {total_size / (1024 * 1024):.2f} MB")

    # Final video
    if os.path.exists('tennis_game_tutorial.mp4'):
        size = os.path.getsize('tennis_game_tutorial.mp4') / (1024 * 1024)
        print(f"\n🎥 Final video: tennis_game_tutorial.mp4 ({size:.2f} MB)")

    print("\n" + "="*60)
    print("VIDEO GENERATION COMPLETE!")
    print("="*60)

    # Instructions
    print("\nTo view the video:")
    print("  Open tennis_game_tutorial.mp4 with any video player")

    print("\nTo customize:")
    print("  - Edit script.txt to modify narration")
    print("  - Run generate_audio_gtts.py to regenerate audio")
    print("  - Run create_video_resized.py to regenerate video")

if __name__ == '__main__':
    if not check_requirements():
        print("\nPlease install missing requirements and try again.")
        sys.exit(1)

    if run_pipeline():
        show_summary()
    else:
        print("\nPipeline completed with some errors. Check the output above.")
        show_summary()