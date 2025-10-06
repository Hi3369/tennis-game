# ソースコード解説動画自動生成システム

テニスゲームのソースコード（index.html）から解説動画を自動生成するシステムです。

## 🎯 概要

HTML/CSS/JavaScriptで作成されたテニスゲームのソースコードを12のセクションに分割し、各セクションの解説を含む動画を自動生成します。

## 📁 ファイル構成

### 核となるスクリプト
- `code_to_image_simple.py` - ソースコードのスクリーンショット生成
- `generate_screenshots.py` - 全セクションのスクリーンショットを一括生成
- `generate_audio_gtts.py` - Google Text-to-Speech を使用した音声生成
- `resize_screenshots.py` - 1920x1080解像度への画像リサイズ
- `create_video.py` - ffmpegを使用した動画生成
- `run_video_pipeline.py` - 全体のパイプライン実行

### 設定ファイル
- `script.txt` - セクション定義と解説テキスト

### 出力フォルダ
- `pic/` - オリジナルスクリーンショット
- `pic_resized/` - 1920x1080にリサイズされた画像
- `audio/` - MP3音声ファイル

## 🚀 使用方法

### 1. 必要な依存関係のインストール

```bash
# Python パッケージ
pip install --break-system-packages pillow gtts

# システムツール (Ubuntu/Debian)
sudo apt-get install ffmpeg
```

### 2. 動画生成の実行

#### 方法 A: 一括実行（推奨）
```bash
python3 run_video_pipeline.py
```

#### 方法 B: ステップごとの実行
```bash
# 1. スクリーンショット生成
python3 generate_screenshots.py

# 2. 音声ファイル生成
python3 generate_audio_gtts.py

# 3. 画像リサイズ
python3 resize_screenshots.py

# 4. 動画生成
python3 create_video_resized.py
```

### 3. 出力確認
生成された `tennis_game_tutorial.mp4` を任意の動画プレーヤーで再生

## 📋 生成される動画の内容

1. **HTML構造とメタデータ** (12秒) - 基本的なHTML構造とCSS設定
2. **CSSスタイル** (15秒) - ダークテーマとレイアウト設定
3. **HTML本体** (10秒) - Canvas要素とUI配置
4. **JavaScript初期設定** (12秒) - DOM参照取得とゲーム設定
5. **ゲームオブジェクト** (18秒) - プレイヤー、AI、ボールオブジェクト
6. **描画関数** (15秒) - パドル、ボール、ネットの描画
7. **AI制御システム** (20秒) - ボール軌道予測とAI動作
8. **プレイヤー制御とボール物理** (25秒) - 入力処理と衝突判定
9. **スコア管理** (15秒) - スコア更新とゲーム終了処理
10. **メインループと描画** (12秒) - ゲームループと描画処理
11. **キーボード入力処理** (12秒) - イベントリスナーの設定
12. **難易度設定とゲーム開始** (18秒) - 難易度調整とゲーム初期化

総動画時間: 約3分

## ⚙️ カスタマイズ

### 解説内容の変更
`script.txt` を編集して、各セクションの解説テキストを修正可能

### 画像テーマの変更
`code_to_image_simple.py` の以下の行を編集：
```python
generator = SimpleCodeImageGenerator(theme='light', font_size=16)  # 'dark' に変更可能
```

### 音声設定の変更
`generate_audio_gtts.py` でgTTSの設定を変更可能

### 動画設定の変更
`create_video.py` で解像度、フレームレート、品質を調整可能

## 🔧 技術仕様

- **画像解像度**: 4倍スケール → 1920x1080リサイズ
- **音声**: gTTS（Google Text-to-Speech）、日本語、MP3形式
- **動画**: H.264（libx264）、AAC（192kbps）、30fps
- **フォント**: システムの日本語対応等幅フォント

## 🐛 トラブルシューティング

### ffmpegが見つからない
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### PIL/Pillowエラー
```bash
pip install --break-system-packages pillow
```

### gTTSネットワークエラー
- インターネット接続を確認
- Google Text-to-Speech APIの利用制限を確認

### メモリ不足エラー
- 画像のスケール設定を下げる（`code_to_image_simple.py` の `scale = 4` を `scale = 2` に変更）

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 貢献

バグ報告や機能追加の提案は、GitHubのIssuesまでお願いします。