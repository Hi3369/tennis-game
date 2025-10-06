# 要求定義書 - ソースコード解説動画自動生成システム

## 1. プロジェクト概要

### 1.1 プロジェクト名
ソースコード解説動画自動生成システム

### 1.2 目的
任意のソースコードファイルから、そのコードの機能と実装内容を解説する高品質な動画を自動生成するシステムを構築する

### 1.3 背景
プログラミング教育やコードレビューにおいて、ソースコードの視覚的な解説動画は理解を深める効果的な手段である。しかし、手動での動画作成は時間がかかるため、自動化システムが求められている。

### 1.4 スコープ
- ソースコードの解析と適切なセクション分割
- コードのスクリーンショット生成（シンタックスハイライト付き）
- 解説文章の自動生成
- 日本語音声ナレーションの生成
- 動画の自動編集と出力

## 2. ステークホルダー

### 2.1 プロジェクトオーナー
システム利用者（開発者、教育者、学習者）

### 2.2 エンドユーザー
- プログラミング学習者
- コードレビュー参加者
- 技術ドキュメント利用者

### 2.3 その他関係者
- システム開発者
- コンテンツ作成者

## 3. 機能要求

### 3.1 必須機能

#### 3.1.1 ソースコード解析機能
- ソースコードを意味のある単位（関数、クラス、設定部分など）に自動分割
- 各セクションの行番号範囲を特定
- コードの論理的な流れに基づいた順序付け

#### 3.1.2 スクリーンショット生成機能
- **実装済みツール**: `code_to_image_simple.py`
- 各コードセクションの高品質スクリーンショット生成
- シンタックスハイライト（言語別対応）
- 日本語対応フォント使用
- 行番号表示
- ライト/ダークテーマ対応
- 出力解像度: 4倍スケール、600 DPI

#### 3.1.3 解説スクリプト生成機能
- 各セクションの機能を説明する日本語テキスト生成
- コードの目的、処理内容、使用技術の説明
- 読み上げ時間を考慮した適切な文章量

#### 3.1.4 音声生成機能（TTS）
- **使用技術**: macOS `say`コマンド（Kyokoボイス）
- 読み上げ速度: 225 words/minute（1.5倍速）
- 出力形式: MP3（128kbps）
- 各セクションごとに個別の音声ファイル生成

#### 3.1.5 画像前処理機能
- **実装済みツール**: `resize_screenshots.py`
- すべてのスクリーンショットを1920×1080に統一
- アスペクト比を維持しながら90%スケールでリサイズ
- ダークグレー背景（#2d2d2d）で中央配置
- 高品質リサンプリング（LANCZOS）使用

#### 3.1.6 動画生成機能
- **実装済みツール**: `create_video.py`
- 解像度: 1920×1080（フルHD）
- フレームレート: 30fps固定
- ビデオコーデック: H.264（libx264）
- オーディオコーデック: AAC（192kbps）
- シーン間に1秒の無音区間を挿入
- 出力形式: MP4

### 3.2 希望機能
- 複数プログラミング言語対応
- カスタマイズ可能なテーマ
- 字幕生成機能
- 複数の音声言語対応

## 4. 非機能要求

### 4.1 性能要求
- 100行のコード: 5分以内で動画生成完了
- 1000行のコード: 30分以内で動画生成完了
- メモリ使用量: 4GB以下

### 4.2 品質要求
- 音声の明瞭さ: 背景ノイズなし、自然な読み上げ
- 画像の鮮明さ: コードが読みやすい高解像度
- 動画の滑らかさ: フレームドロップなし
- 文字化け対策: 完全な日本語対応

### 4.3 互換性要求
- 動画: 主要な動画プレーヤーで再生可能
- デバイス: PC、スマートフォン、タブレット対応
- OS: macOS、Windows、Linux（音声生成は環境依存）

### 4.4 保守性要求
- モジュール化された設計
- 各機能の独立性確保
- エラーハンドリングの実装

## 5. システム構成

### 5.1 ディレクトリ構造
```
プロジェクトルート/
├── ソースコードファイル（入力）
├── code_to_image_simple.py（スクリーンショット生成）
├── generate_screenshots.py（バッチ処理）
├── generate_audio.py（音声生成）
├── resize_screenshots.py（画像前処理）
├── create_video.py（動画生成）
├── script.txt（解説スクリプト）
├── pic/（オリジナルスクリーンショット）
├── pic_resized/（リサイズ済み画像）
├── audio/（音声ファイル）
└── 出力動画.mp4
```

### 5.2 処理フロー
1. **コード解析**: ソースコードを論理的なセクションに分割
2. **スクリプト作成**: 各セクションの解説文を含むscript.txt生成
3. **スクリーンショット生成**: 各セクションの画像をpicフォルダに生成
4. **音声生成**: 解説文からMP3ファイルをaudioフォルダに生成
5. **画像前処理**: 1920×1080にリサイズしてpic_resizedフォルダに保存
6. **動画生成**: ffmpegで画像と音声を結合してMP4生成

## 6. 技術仕様

### 6.1 必要なソフトウェア
- Python 3.x
- Pillow (PIL)
- ffmpeg
- macOS（sayコマンド用）またはTTS代替手段

### 6.2 スクリプトファイル仕様
```
# セクションタイトル（行番号範囲）
[実際の表示時間: XX.X秒]
[表示行: 開始行-終了行]
[画像ファイル: pic/ファイル名.png]
[音声ファイル: audio/ファイル名.mp3]

解説文章（日本語）
```

### 6.3 コマンド実行順序
```bash
# 1. スクリーンショット生成
python generate_screenshots.py

# 2. 音声ファイル生成
python generate_audio.py

# 3. 画像リサイズ
python resize_screenshots.py

# 4. 動画生成
python create_video_resized.py
```

## 7. 制約事項

### 7.1 技術的制約
- 音声生成はmacOS環境依存（代替: gTTS等のクロスプラットフォームTTS）
- 日本語フォントのインストールが必要
- ffmpegのインストールが必要

### 7.2 コンテンツ制約
- 1シーンあたりの推奨時間: 5-40秒
- 総動画時間: 10分以内を推奨
- コードの可読性を考慮したセクション分割

## 8. 成果物

### 8.1 生成物
1. 解説動画ファイル（MP4形式、1920×1080、30fps）
2. 動画スクリプト（script.txt）
3. 各セクションのスクリーンショット（PNG形式）
4. 各セクションの音声ファイル（MP3形式）

### 8.2 中間成果物
1. オリジナルスクリーンショット（picフォルダ）
2. リサイズ済みスクリーンショット（pic_resizedフォルダ）
3. 音声ファイル（audioフォルダ）
4. 一時動画ファイル（処理後削除）

## 9. 品質保証

### 9.1 チェックポイント
1. スクリプト内容の確認（動画生成前）
2. スクリーンショットの視認性確認
3. 音声の聞き取りやすさ確認
4. 動画の再生確認

### 9.2 エラー処理
- 画像生成失敗時の通知
- 音声生成失敗時の代替処理
- 動画生成失敗時のログ出力

## 10. 拡張性

### 10.1 将来的な拡張
- Web APIとしての提供
- 複数言語のソースコード対応
- AIによる解説文自動生成
- インタラクティブな動画機能
- クラウドベースの処理

### 10.2 カスタマイズポイント
- テーマカラーの変更
- フォントの選択
- 音声の種類と速度
- 動画の品質設定

---

## 改訂履歴
| 版数 | 日付 | 変更内容 | 変更者 |
|------|------|----------|--------|
| 1.0  | 2025/05/30 | 初版作成 | Claude Code |
| 1.1  | 2025/05/30 | ソースコード付録を追加 | Claude Code |

---

# 付録：ソースコード

## 付録A: code_to_image_simple.py

```python
#!/usr/bin/env python3
"""
Simple Code to Image Converter
Converts Python source code to a screenshot-like image without external syntax highlighting libraries.
Only requires Pillow (PIL).

Requirements:
    pip install pillow
"""

import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow library is not installed.")
    print("Please install it using: pip install pillow")
    sys.exit(1)

import os
import re


class SimpleCodeImageGenerator:
    """Generates screenshot-like images from source code with basic syntax highlighting."""
    
    # Theme configurations
    THEMES = {
        'dark': {
            'background': '#1e1e1e',
            'line_number_bg': '#2d2d2d',
            'line_number_fg': '#858585',
            'default_text': '#d4d4d4',
            'keyword': '#569cd6',
            'string': '#ce9178',
            'comment': '#6a9955',
            'function': '#dcdcaa',
            'number': '#b5cea8',
            'decorator': '#d7ba7d'
        },
        'light': {
            'background': '#ffffff',
            'line_number_bg': '#f5f5f5',
            'line_number_fg': '#999999',
            'default_text': '#333333',
            'keyword': '#0000ff',
            'string': '#a31515',
            'comment': '#008000',
            'function': '#795e26',
            'number': '#098658',
            'decorator': '#af00db'
        }
    }
    
    # Python keywords
    KEYWORDS = {
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
        'while', 'with', 'yield', 'self'
    }
    
    # Built-in functions
    BUILTINS = {
        'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
        'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr',
        'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter',
        'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
        'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
        'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min',
        'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property',
        'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
        'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type',
        'vars', 'zip'
    }
    
    def __init__(self, theme='dark', font_size=14, line_height_ratio=1.5):
        """Initialize the code image generator."""
        self.theme = self.THEMES.get(theme, self.THEMES['dark'])
        self.font_size = font_size
        self.line_height = int(font_size * line_height_ratio)
        
        # Try to load a monospace font
        self.font = self._load_font()
        
        # Margins and padding
        self.padding = 30
        self.line_number_padding = 15
        self.line_number_width = 50
        
    def _load_font(self):
        """Load a suitable monospace font."""
        return self._load_font_with_size(self.font_size)
    
    def _load_font_with_size(self, size):
        """Load a suitable monospace font with specific size."""
        font_candidates = [
            # macOS - Japanese fonts first
            '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
            '/System/Library/Fonts/Hiragino Sans GB.ttc',
            '/Library/Fonts/Arial Unicode.ttf',
            '/System/Library/Fonts/PingFang.ttc',
            # macOS - English monospace fonts
            '/System/Library/Fonts/Monaco.dfont',
            '/Library/Fonts/Courier New.ttf',
            '/System/Library/Fonts/Menlo.ttc',
            # Linux - Japanese fonts
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
            # Linux - English fonts
            '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
            # Windows - Japanese fonts
            'C:\\Windows\\Fonts\\msgothic.ttc',
            'C:\\Windows\\Fonts\\YuGothM.ttc',
            # Windows - English fonts
            'C:\\Windows\\Fonts\\consola.ttf',
            'C:\\Windows\\Fonts\\cour.ttf',
        ]
        
        for font_path in font_candidates:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        
        # Fallback to default font
        try:
            return ImageFont.load_default()
        except:
            print("Warning: Could not load font, using PIL default")
            return ImageFont.load_default()
    
    def _get_text_size(self, text):
        """Get the size of text when rendered."""
        bbox = self.font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    def _tokenize_line(self, line):
        """Simple tokenizer for Python code."""
        tokens = []
        
        # Handle empty lines
        if not line.strip():
            return [(line, 'default')]
        
        # Check if entire line is a comment
        if line.strip().startswith('#'):
            return [(line, 'comment')]
        
        # Regular expressions for different token types
        patterns = [
            (r'#.*$', 'comment'),  # Comments
            (r'@\w+', 'decorator'),  # Decorators
            (r'""".*?"""|\'\'\'.*?\'\'\'', 'string'),  # Triple quotes
            (r'"[^"]*"|\'[^\']*\'', 'string'),  # Strings
            (r'\b\d+\.?\d*\b', 'number'),  # Numbers
            (r'\b(?:' + '|'.join(self.KEYWORDS) + r')\b', 'keyword'),  # Keywords
            (r'\b(?:' + '|'.join(self.BUILTINS) + r')\b', 'function'),  # Built-ins
            (r'\b\w+(?=\s*\()', 'function'),  # Function calls
        ]
        
        # Tokenize the line
        position = 0
        while position < len(line):
            matched = False
            
            for pattern, token_type in patterns:
                regex = re.compile(pattern)
                match = regex.match(line, position)
                if match:
                    # Add any text before the match as default
                    if match.start() > position:
                        tokens.append((line[position:match.start()], 'default'))
                    
                    # Add the matched token
                    tokens.append((match.group(), token_type))
                    position = match.end()
                    matched = True
                    break
            
            if not matched:
                # No pattern matched, add one character as default
                tokens.append((line[position], 'default'))
                position += 1
        
        return tokens
    
    def generate_image(self, code, output_path, title=None):
        """Generate an image from source code."""
        # Split code into lines
        lines = code.split('\n')
        num_lines = len(lines)
        
        # Calculate image dimensions
        max_line_length = max(len(line) for line in lines) if lines else 0
        char_width, _ = self._get_text_size('M')
        
        content_width = (max_line_length * char_width) + self.line_number_width + (self.line_number_padding * 2)
        content_height = num_lines * self.line_height
        
        img_width = content_width + (self.padding * 2)
        img_height = content_height + (self.padding * 2)
        
        if title:
            img_height += self.line_height + 10
        
        # Create image with higher resolution for better quality
        scale = 4  # Scale factor for higher resolution (increased from 2 to 4)
        img = Image.new('RGB', (img_width * scale, img_height * scale), self.theme['background'])
        draw = ImageDraw.Draw(img)
        
        # Create scaled font
        scaled_font = self._load_font_with_size(self.font_size * scale)
        
        # Draw title if provided
        y_offset = self.padding * scale
        if title:
            title_color = self.theme['default_text']
            draw.text((self.padding * scale, y_offset), title, fill=title_color, font=scaled_font)
            y_offset += (self.line_height + 10) * scale
        
        # Draw line numbers background
        line_num_bg_x1 = self.padding * scale
        line_num_bg_x2 = (self.padding + self.line_number_width) * scale
        draw.rectangle(
            [line_num_bg_x1, y_offset, line_num_bg_x2, y_offset + (content_height * scale)],
            fill=self.theme['line_number_bg']
        )
        
        # Process each line
        for i, line in enumerate(lines):
            line_y = y_offset + (i * self.line_height * scale)
            
            # Draw line number
            line_num = str(i + 1).rjust(3)
            draw.text(
                ((self.padding + 5) * scale, line_y),
                line_num,
                fill=self.theme['line_number_fg'],
                font=scaled_font
            )
            
            # Draw code line with syntax highlighting
            x_offset = (self.padding + self.line_number_width + self.line_number_padding) * scale
            
            # Tokenize and draw the line
            tokens = self._tokenize_line(line)
            for token_text, token_type in tokens:
                color = self.theme.get(token_type, self.theme['default_text'])
                draw.text(
                    (x_offset, line_y),
                    token_text,
                    fill=color,
                    font=scaled_font
                )
                text_width = scaled_font.getbbox(token_text)[2]
                x_offset += text_width
        
        # Add a subtle border
        border_color = '#333333' if 'dark' in self.theme else '#cccccc'
        draw.rectangle(
            [0, 0, (img_width * scale) - 1, (img_height * scale) - 1],
            outline=border_color,
            width=scale
        )
        
        # Add subtle shadow/gradient effect at edges
        for i in range(10):
            alpha = 255 - (i * 20)
            shadow_color = (0, 0, 0, alpha) if 'dark' in self.theme else (200, 200, 200, alpha)
            # Top shadow
            draw.line([(i, i), ((img_width * scale) - i, i)], fill=shadow_color, width=1)
            # Left shadow
            draw.line([(i, i), (i, (img_height * scale) - i)], fill=shadow_color, width=1)
        
        # Resize back to target resolution with antialiasing
        img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)
        
        # Save image with higher quality
        img.save(output_path, quality=100, dpi=(600, 600))
        print(f"Image saved to: {output_path}")


def main():
    """Main function to convert Python files to images."""
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'rbeta.py'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print("\nUsage:")
        print("  python code_to_image_simple.py [filename]")
        print("\nExample:")
        print("  python code_to_image_simple.py rbeta.py")
        print("  python code_to_image_simple.py mycode.py")
        print("\nNote: This script only requires the Pillow library.")
        print("Install it with: pip install pillow")
        sys.exit(1)
    
    # Read source code
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Generate images with both themes
    generator_dark = SimpleCodeImageGenerator(theme='dark', font_size=14)
    generator_light = SimpleCodeImageGenerator(theme='light', font_size=14)
    
    # Generate dark theme image
    output_dark = f'{base_name}_dark_simple.png'
    generator_dark.generate_image(
        code,
        output_dark,
        title=f'{os.path.basename(input_file)} - Dark Theme'
    )
    
    # Generate light theme image
    output_light = f'{base_name}_light_simple.png'
    generator_light.generate_image(
        code,
        output_light,
        title=f'{os.path.basename(input_file)} - Light Theme'
    )
    
    print(f"\nSuccessfully generated:")
    print(f"  - Dark theme: {output_dark}")
    print(f"  - Light theme: {output_light}")


if __name__ == '__main__':
    main()
```

## 付録B: generate_screenshots.py

```python
#!/usr/bin/env python3
"""
Generate screenshot images for each scene of rbeta.py
"""

import os
import sys
from code_to_image_simple import SimpleCodeImageGenerator

# Read the source code
with open('rbeta.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Define scenes with their line ranges and output filenames
scenes = [
    {'name': 'scene01_import', 'start': 1, 'end': 3},
    {'name': 'scene02_settings', 'start': 5, 'end': 10},
    {'name': 'scene03_calculate_resize', 'start': 13, 'end': 41},
    {'name': 'scene04_resize_image', 'start': 44, 'end': 56},
    {'name': 'scene05_validation', 'start': 59, 'end': 75},
    {'name': 'scene06_output_folder', 'start': 77, 'end': 83},
    {'name': 'scene07_main_loop_start', 'start': 85, 'end': 100},
    {'name': 'scene08_image_processing', 'start': 102, 'end': 134},
    {'name': 'scene09_error_handling', 'start': 136, 'end': 141},
    {'name': 'scene10_summary', 'start': 143, 'end': 148}
]

# Create image generator (using light theme for better visibility)
generator = SimpleCodeImageGenerator(theme='light', font_size=16)

# Generate screenshots for each scene
for scene in scenes:
    # Extract the relevant lines (adjusting for 0-based indexing)
    scene_lines = lines[scene['start']-1:scene['end']]
    scene_code = ''.join(scene_lines)
    
    # Generate the image
    output_path = f"pic/{scene['name']}.png"
    title = f"rbeta.py - Lines {scene['start']}-{scene['end']}"
    
    print(f"Generating {output_path}...")
    generator.generate_image(scene_code, output_path, title=title)

print("\nAll screenshots generated successfully!")
```

## 付録C: generate_audio.py

```python
#!/usr/bin/env python3
"""
Generate audio files for each scene using macOS say command
"""

import os
import subprocess
import time

# Define the narration text for each scene
scenes = [
    {
        'id': 'scene01',
        'text': '''このプログラムは、PILライブラリを使用した画像リサイズツールです。
必要なライブラリとして、PILのImageモジュール、osモジュール、sysモジュールをインポートしています。'''
    },
    {
        'id': 'scene02',
        'text': '''設定項目では、プログラムの動作をカスタマイズできます。
sourceFolderで入力画像のフォルダを指定し、outputFolderで出力先を設定します。
outputExtentionでは、pngまたはjpg形式を選択できます。
sizeは、リサイズ時の基準となるピクセル数で、デフォルトは700ピクセルです。
modeでは、リサイズするか元のサイズを維持するかを選択できます。'''
    },
    {
        'id': 'scene03',
        'text': '''calculate_resize_dimensions関数は、画像の縦横比を維持しながら適切なリサイズサイズを計算します。
リサイズモードの場合、横長画像は幅を基準に、縦長画像は高さを基準にサイズを調整します。
これにより、画像の変形を防ぎながら、指定されたサイズに収まるように処理します。
オリジナルモードでは、元の画像サイズをそのまま返します。'''
    },
    {
        'id': 'scene04',
        'text': '''resize_image関数は、実際に画像をリサイズする処理を行います。
PILのresize メソッドを使用して、指定された幅と高さに画像を変更します。
この関数はシンプルですが、プログラムの中核となる処理です。'''
    },
    {
        'id': 'scene05',
        'text': '''プログラムの安全性を確保するため、設定値の検証を行います。
出力形式がpngまたはjpgであることを確認し、
処理モードがresizeまたはoriginalであることをチェックします。
サイズが正の整数であることも検証し、
入力フォルダが存在することを確認します。
エラーがある場合は、分かりやすいメッセージを表示して終了します。'''
    },
    {
        'id': 'scene06',
        'text': '''出力フォルダが存在しない場合は、自動的に作成します。
エラーハンドリングにより、フォルダ作成に失敗した場合も適切に処理します。'''
    },
    {
        'id': 'scene07',
        'text': '''処理した画像数とエラー数をカウントする変数を初期化します。
入力フォルダ内のファイルリストを取得し、
jpg、jpeg、png、bmp、gif形式の画像ファイルのみを処理対象とします。'''
    },
    {
        'id': 'scene08',
        'text': '''各画像ファイルに対して以下の処理を実行します。
まず、画像を読み込み、CMYK形式の場合はRGB形式に変換します。
ファイル名から拡張子を除去し、処理中であることを表示します。
calculate_resize_dimensions関数でリサイズ後のサイズを計算し、
resize_image関数で実際にリサイズを実行します。
最後に、指定された形式で画像を保存し、品質は90に設定しています。'''
    },
    {
        'id': 'scene09',
        'text': '''画像処理中に発生する可能性のあるエラーを適切に処理します。
IOErrorは画像の読み込みや保存に関するエラーを、
その他の例外は予期しないエラーをキャッチします。
エラーが発生しても、他の画像の処理は継続されます。'''
    },
    {
        'id': 'scene10',
        'text': '''すべての処理が完了したら、結果のサマリーを表示します。
処理に成功した画像数と、エラーが発生した画像数を報告し、
ユーザーが処理結果を一目で確認できるようにしています。'''
    }
]

# Japanese voice options for macOS say command
# Available voices: Kyoko, Otoya
voice = 'Kyoko'  # Female Japanese voice
rate = 225  # Speech rate (words per minute) - 1.5x faster than default 150

print(f"Using voice: {voice}")
print(f"Speech rate: {rate} words per minute\n")

# Generate audio for each scene
for scene in scenes:
    output_file = f"audio/{scene['id']}_narration.aiff"
    
    print(f"Generating audio for {scene['id']}...")
    
    # Create the say command
    cmd = [
        'say',
        '-v', voice,
        '-r', str(rate),
        '-o', output_file,
        scene['text']
    ]
    
    try:
        # Execute the command
        subprocess.run(cmd, check=True)
        print(f"  ✓ Saved to {output_file}")
        
        # Get file info
        file_size = os.path.getsize(output_file) / 1024 / 1024  # MB
        print(f"  File size: {file_size:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error generating audio: {e}")
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")

print("\nConverting AIFF files to MP3...")

# Convert AIFF to MP3 for smaller file size
for scene in scenes:
    aiff_file = f"audio/{scene['id']}_narration.aiff"
    mp3_file = f"audio/{scene['id']}_narration.mp3"
    
    if os.path.exists(aiff_file):
        print(f"Converting {scene['id']}...")
        cmd = [
            'ffmpeg',
            '-i', aiff_file,
            '-acodec', 'mp3',
            '-ab', '128k',
            mp3_file,
            '-y'  # Overwrite output file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✓ Converted to {mp3_file}")
            
            # Remove the original AIFF file
            os.remove(aiff_file)
            print(f"  ✓ Removed {aiff_file}")
            
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
```

## 付録D: resize_screenshots.py

```python
#!/usr/bin/env python3
"""
Resize all screenshots to 1920x1080 with proper scaling and centering
"""

from PIL import Image
import os

# Target resolution
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080

# Background color (dark gray to match code theme)
BACKGROUND_COLOR = '#2d2d2d'

# Create output directory
output_dir = "pic_resized"
os.makedirs(output_dir, exist_ok=True)

print(f"Resizing screenshots to {TARGET_WIDTH}x{TARGET_HEIGHT}...")

# Process all PNG files in pic directory
pic_files = [f for f in os.listdir('pic') if f.endswith('.png')]

for filename in pic_files:
    input_path = os.path.join('pic', filename)
    output_path = os.path.join(output_dir, filename)
    
    print(f"\nProcessing {filename}...")
    
    # Open the original image
    img = Image.open(input_path)
    original_width, original_height = img.size
    print(f"  Original size: {original_width}x{original_height}")
    
    # Calculate scaling factor to fit within target resolution while maintaining aspect ratio
    scale_x = TARGET_WIDTH / original_width
    scale_y = TARGET_HEIGHT / original_height
    scale = min(scale_x, scale_y) * 0.9  # Use 90% to leave some padding
    
    # Calculate new dimensions
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    
    # Resize the image with high quality
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create a new image with target resolution and background color
    final_img = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHT), BACKGROUND_COLOR)
    
    # Calculate position to center the resized image
    x_offset = (TARGET_WIDTH - new_width) // 2
    y_offset = (TARGET_HEIGHT - new_height) // 2
    
    # Paste the resized image onto the background
    final_img.paste(resized_img, (x_offset, y_offset))
    
    # Save the final image
    final_img.save(output_path, quality=95, dpi=(300, 300))
    print(f"  ✓ Saved to {output_path}")
    print(f"  Resized to: {new_width}x{new_height} (scale: {scale:.2f})")
    print(f"  Centered at: ({x_offset}, {y_offset})")

print(f"\n✓ All screenshots resized and saved to '{output_dir}' directory")

# Update create_video.py to use resized images
print("\nUpdating video creation script to use resized images...")

# Read the current create_video.py
with open('create_video.py', 'r') as f:
    content = f.read()

# Replace pic/ with pic_resized/
updated_content = content.replace('pic/', 'pic_resized/')

# Write the updated content
with open('create_video_resized.py', 'w') as f:
    f.write(updated_content)

print("✓ Created 'create_video_resized.py' that uses resized images")
```

## 付録E: create_video.py

```python
#!/usr/bin/env python3
"""
Create video from screenshots and audio narration using ffmpeg
"""

import subprocess
import os

# Video settings
output_video = "rbeta_tutorial.mp4"
resolution = "1920x1080"
fps = 30
video_codec = "libx264"
audio_codec = "aac"

# Define scenes with their durations (including 1 second gap after each scene)
scenes = [
    {'id': 'scene01', 'duration': 7.4, 'gap': 1.0},
    {'id': 'scene02', 'duration': 17.7, 'gap': 1.0},
    {'id': 'scene03', 'duration': 16.5, 'gap': 1.0},
    {'id': 'scene04', 'duration': 9.9, 'gap': 1.0},
    {'id': 'scene05', 'duration': 16.6, 'gap': 1.0},
    {'id': 'scene06', 'duration': 6.6, 'gap': 1.0},
    {'id': 'scene07', 'duration': 9.6, 'gap': 1.0},
    {'id': 'scene08', 'duration': 19.8, 'gap': 1.0},
    {'id': 'scene09', 'duration': 10.7, 'gap': 1.0},
    {'id': 'scene10', 'duration': 8.7, 'gap': 0.0},  # No gap after last scene
]

# Create a temporary directory for intermediate files
temp_dir = "temp_video_files"
os.makedirs(temp_dir, exist_ok=True)

print("Creating video segments for each scene...")

# Process each scene
for i, scene in enumerate(scenes):
    scene_id = scene['id']
    duration = scene['duration']
    gap = scene['gap']
    total_duration = duration + gap
    
    print(f"\nProcessing {scene_id}...")
    
    # Create video from image
    image_file = f"pic/{scene_id}_import.png" if scene_id == 'scene01' else f"pic/{scene_id}_{scene_id.replace('scene', '').replace('0', '')}.png"
    
    # Check for correct image filename
    possible_image_files = [
        f"pic/{scene_id}_import.png",
        f"pic/{scene_id}_settings.png",
        f"pic/{scene_id}_calculate_resize.png",
        f"pic/{scene_id}_resize_image.png",
        f"pic/{scene_id}_validation.png",
        f"pic/{scene_id}_output_folder.png",
        f"pic/{scene_id}_main_loop_start.png",
        f"pic/{scene_id}_image_processing.png",
        f"pic/{scene_id}_error_handling.png",
        f"pic/{scene_id}_summary.png"
    ]
    
    image_file = None
    for possible_file in possible_image_files:
        if os.path.exists(possible_file):
            image_file = possible_file
            break
    
    if not image_file:
        print(f"  ✗ Error: Image file for {scene_id} not found")
        continue
    
    audio_file = f"audio/{scene_id}_narration.mp3"
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

print("\nConcatenating all video segments...")

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
```

## 付録F: create_video_resized.py

```python
#!/usr/bin/env python3
"""
Create video from screenshots and audio narration using ffmpeg
"""

import subprocess
import os

# Video settings
output_video = "rbeta_tutorial.mp4"
resolution = "1920x1080"
fps = 30
video_codec = "libx264"
audio_codec = "aac"

# Define scenes with their durations (including 1 second gap after each scene)
scenes = [
    {'id': 'scene01', 'duration': 7.4, 'gap': 1.0},
    {'id': 'scene02', 'duration': 17.7, 'gap': 1.0},
    {'id': 'scene03', 'duration': 16.5, 'gap': 1.0},
    {'id': 'scene04', 'duration': 9.9, 'gap': 1.0},
    {'id': 'scene05', 'duration': 16.6, 'gap': 1.0},
    {'id': 'scene06', 'duration': 6.6, 'gap': 1.0},
    {'id': 'scene07', 'duration': 9.6, 'gap': 1.0},
    {'id': 'scene08', 'duration': 19.8, 'gap': 1.0},
    {'id': 'scene09', 'duration': 10.7, 'gap': 1.0},
    {'id': 'scene10', 'duration': 8.7, 'gap': 0.0},  # No gap after last scene
]

# Create a temporary directory for intermediate files
temp_dir = "temp_video_files"
os.makedirs(temp_dir, exist_ok=True)

print("Creating video segments for each scene...")

# Process each scene
for i, scene in enumerate(scenes):
    scene_id = scene['id']
    duration = scene['duration']
    gap = scene['gap']
    total_duration = duration + gap
    
    print(f"\nProcessing {scene_id}...")
    
    # Create video from image
    image_file = f"pic_resized/{scene_id}_import.png" if scene_id == 'scene01' else f"pic_resized/{scene_id}_{scene_id.replace('scene', '').replace('0', '')}.png"
    
    # Check for correct image filename
    possible_image_files = [
        f"pic_resized/{scene_id}_import.png",
        f"pic_resized/{scene_id}_settings.png",
        f"pic_resized/{scene_id}_calculate_resize.png",
        f"pic_resized/{scene_id}_resize_image.png",
        f"pic_resized/{scene_id}_validation.png",
        f"pic_resized/{scene_id}_output_folder.png",
        f"pic_resized/{scene_id}_main_loop_start.png",
        f"pic_resized/{scene_id}_image_processing.png",
        f"pic_resized/{scene_id}_error_handling.png",
        f"pic_resized/{scene_id}_summary.png"
    ]
    
    image_file = None
    for possible_file in possible_image_files:
        if os.path.exists(possible_file):
            image_file = possible_file
            break
    
    if not image_file:
        print(f"  ✗ Error: Image file for {scene_id} not found")
        continue
    
    audio_file = f"audio/{scene_id}_narration.mp3"
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

print("\nConcatenating all video segments...")

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
```