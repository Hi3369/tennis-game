#!/usr/bin/env python3
"""
Simple Code to Image Converter
ソースコードを画像に変換するツール

HTML/CSS/JavaScriptのソースコードを、シンタックスハイライト付きの
高品質なスクリーンショット画像に変換します。
外部のシンタックスハイライトライブラリは使用せず、PILのみで実現。

Requirements:
    pip install pillow
"""

import sys

# PIL（Pillow）ライブラリのインポートを試行
# 画像の生成・編集・保存に必要なモジュール
try:
    from PIL import Image, ImageDraw, ImageFont  # 画像処理の核となるモジュール
except ImportError:
    # Pillowがインストールされていない場合のエラーメッセージ
    print("Error: Pillow library is not installed.")
    print("Please install it using: pip install pillow")
    sys.exit(1)

import os    # ファイルパス操作とファイル存在確認用
import re    # 正規表現によるコードのトークン解析用


class SimpleCodeImageGenerator:
    """
    ソースコードから画像を生成するクラス

    シンタックスハイライト機能付きでコードのスクリーンショット風画像を生成。
    ダークテーマとライトテーマに対応し、行番号表示や高解像度出力をサポート。
    """

    # テーマ設定：ダークテーマとライトテーマの色定義
    THEMES = {
        'dark': {
            # ダークテーマ：黒背景に明るい文字色（VS Code風）
            'background': '#1e1e1e',        # 背景色（濃いグレー）
            'line_number_bg': '#2d2d2d',    # 行番号領域の背景色
            'line_number_fg': '#858585',    # 行番号の文字色
            'default_text': '#d4d4d4',      # 通常のテキスト色
            'keyword': '#569cd6',           # キーワード色（青系）
            'string': '#ce9178',            # 文字列色（オレンジ系）
            'comment': '#6a9955',           # コメント色（緑系）
            'function': '#dcdcaa',          # 関数名色（黄系）
            'number': '#b5cea8',            # 数値色（薄緑）
            'decorator': '#d7ba7d',         # デコレータ色（薄オレンジ）
            'tag': '#569cd6',               # HTMLタグ色（青系）
            'attribute': '#92c5f8',         # 属性色（水色）
            'css_property': '#9cdcfe',      # CSSプロパティ色（水色）
            'css_value': '#ce9178'          # CSS値色（オレンジ系）
        },
        'light': {
            # ライトテーマ：白背景に暗い文字色（Visual Studio風）
            'background': '#ffffff',        # 背景色（白）
            'line_number_bg': '#f5f5f5',    # 行番号領域の背景色（薄灰色）
            'line_number_fg': '#999999',    # 行番号の文字色（灰色）
            'default_text': '#333333',      # 通常のテキスト色（濃いグレー）
            'keyword': '#0000ff',           # キーワード色（青）
            'string': '#a31515',            # 文字列色（赤茶色）
            'comment': '#008000',           # コメント色（緑）
            'function': '#795e26',          # 関数名色（茶色）
            'number': '#098658',            # 数値色（濃い緑）
            'decorator': '#af00db',         # デコレータ色（紫）
            'tag': '#800000',               # HTMLタグ色（赤茶色）
            'attribute': '#0000ff',         # 属性色（青）
            'css_property': '#800080',      # CSSプロパティ色（紫）
            'css_value': '#a31515'          # CSS値色（赤茶色）
        }
    }

    # JavaScript予約語・キーワード定義
    # シンタックスハイライトでキーワード色を適用する単語のセット
    JS_KEYWORDS = {
        'function', 'var', 'let', 'const',          # 関数・変数宣言
        'if', 'else', 'for', 'while', 'do',         # 制御構文
        'switch', 'case', 'break', 'continue',      # 分岐・ループ制御
        'return', 'try', 'catch', 'finally',        # 関数・例外処理
        'throw', 'new', 'this', 'typeof',           # オブジェクト関連
        'instanceof', 'in', 'of',                   # 演算子
        'true', 'false', 'null', 'undefined',       # リテラル値
        'class', 'extends', 'import', 'export',     # ES6+ 機能
        'async', 'await'                            # 非同期処理
    }

    # CSSプロパティ定義
    # よく使われるCSSプロパティ名のセット
    CSS_KEYWORDS = {
        'margin', 'padding', 'border',              # ボックスモデル
        'width', 'height', 'color', 'background',   # サイズ・色
        'font-size', 'font-family', 'text-align',   # テキスト関連
        'display', 'position', 'top', 'left',       # レイアウト
        'right', 'bottom', 'flex', 'grid',          # レイアウト（続き）
        'justify-content', 'align-items'            # Flexbox/Grid
    }

    # JavaScript組み込み関数・オブジェクト定義
    # ブラウザAPIやDOM操作でよく使われる名前のセット
    BUILTINS = {
        'document', 'window', 'console',            # ブラウザオブジェクト
        'alert', 'setTimeout', 'setInterval',       # タイマー関数
        'addEventListener', 'getElementById',        # DOM操作
        'querySelector', 'Math', 'Date',            # セレクタ・組み込み
        'Array', 'Object', 'String', 'Number',      # データ型
        'Boolean', 'parseInt', 'parseFloat',        # 型変換
        'canvas', 'ctx', 'fillRect', 'strokeRect',  # Canvas API
        'arc', 'moveTo', 'lineTo'                   # Canvas描画
    }

    def __init__(self, theme='dark', font_size=14, line_height_ratio=1.5):
        """
        コードイメージジェネレーターの初期化

        Args:
            theme (str): テーマ名（'dark' または 'light'）
            font_size (int): フォントサイズ（ピクセル）
            line_height_ratio (float): 行の高さの倍率（フォントサイズに対する比率）
        """
        # 選択されたテーマの色設定を取得（存在しない場合はダークテーマ）
        self.theme = self.THEMES.get(theme, self.THEMES['dark'])
        self.font_size = font_size  # フォントサイズを保存
        # 行の高さを計算（フォントサイズ × 倍率）
        self.line_height = int(font_size * line_height_ratio)

        # 等幅フォントの読み込みを試行
        self.font = self._load_font()

        # 画像のマージンとパディング設定
        self.padding = 30               # 画像全体の余白
        self.line_number_padding = 15   # 行番号とコードの間隔
        self.line_number_width = 50     # 行番号領域の幅

    def _load_font(self):
        """
        等幅フォントの読み込み

        現在のフォントサイズで等幅フォントを読み込みます。

        Returns:
            ImageFont: 読み込まれたフォントオブジェクト
        """
        return self._load_font_with_size(self.font_size)

    def _load_font_with_size(self, size):
        """
        指定サイズの等幅フォントを読み込み

        OS別のフォントファイルパスを順次試行し、利用可能な等幅フォントを読み込みます。
        日本語対応フォントを優先して検索し、見つからない場合はデフォルトフォントを使用。

        Args:
            size (int): フォントサイズ（ピクセル）

        Returns:
            ImageFont: 読み込まれたフォントオブジェクト
        """
        # OS別のフォントパス候補リスト（優先順）
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
        """Simple tokenizer for HTML/CSS/JavaScript code."""
        tokens = []

        # Handle empty lines
        if not line.strip():
            return [(line, 'default')]

        # Check if entire line is a comment
        if line.strip().startswith('//') or line.strip().startswith('/*'):
            return [(line, 'comment')]

        # HTML comment
        if '<!--' in line:
            return [(line, 'comment')]

        # CSS rule detection
        in_css = False
        if '{' in line and (':' in line or 'px' in line or '#' in line):
            in_css = True

        # Regular expressions for different token types
        patterns = [
            (r'//.*$|/\*.*?\*/', 'comment'),  # Comments
            (r'<!--.*?-->', 'comment'),  # HTML comments
            (r'"[^"]*"|\'[^\']*\'', 'string'),  # Strings
            (r'\b\d+\.?\d*\b', 'number'),  # Numbers
            (r'</?[a-zA-Z][^>]*>', 'tag'),  # HTML tags
            (r'\b(?:' + '|'.join(self.JS_KEYWORDS) + r')\b', 'keyword'),  # JS Keywords
        ]

        if in_css:
            patterns.extend([
                (r'\b(?:' + '|'.join(self.CSS_KEYWORDS) + r')\b', 'css_property'),  # CSS properties
                (r'#[0-9a-fA-F]{3,6}', 'css_value'),  # Color values
                (r'\d+px|\d+%|\d+em', 'css_value'),  # CSS units
            ])
        else:
            patterns.extend([
                (r'\b(?:' + '|'.join(self.BUILTINS) + r')\b', 'function'),  # Built-ins
                (r'\b\w+(?=\s*\()', 'function'),  # Function calls
            ])

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
        """
        ソースコードから画像を生成

        指定されたソースコードをシンタックスハイライト付きの画像として生成し、
        高解像度（4倍スケール）で処理後、最終的に通常解像度で保存します。

        Args:
            code (str): 画像化するソースコード
            output_path (str): 出力画像ファイルのパス
            title (str, optional): 画像上部に表示するタイトル

        Returns:
            None（ファイルとして保存）
        """
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
        border_color = '#333333' if 'dark' in str(self.theme) else '#cccccc'
        draw.rectangle(
            [0, 0, (img_width * scale) - 1, (img_height * scale) - 1],
            outline=border_color,
            width=scale
        )

        # Resize back to target resolution with antialiasing
        img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)

        # Save image with higher quality
        img.save(output_path, quality=100, dpi=(600, 600))
        print(f"Image saved to: {output_path}")


def main():
    """Main function to convert HTML files to images."""

    # Parse command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'index.html'

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print("\nUsage:")
        print("  python code_to_image_simple.py [filename]")
        print("\nExample:")
        print("  python code_to_image_simple.py index.html")
        print("  python code_to_image_simple.py mycode.js")
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