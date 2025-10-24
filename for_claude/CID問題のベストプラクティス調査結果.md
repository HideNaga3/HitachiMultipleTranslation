# CIDコード問題のベストプラクティス調査結果

## 調査日
2025-10-24

## 調査元
- Stack Overflow（複数のCID関連質問）
- PyMuPDF公式ドキュメント
- 日本語技術ブログ（golden-lucky.hatenablog.com）
- GitHub Issue（pdfplumber, PyMuPDF）
- 2024-2025年のPDFライブラリ比較記事

---

## 問題の本質

### CIDコードとは

**CID (Character ID)** は、PDFフォント内部で使用される文字の識別番号です。

```
例：
元の文字: ា（クメール語の母音記号）
CIDコード: (cid:640)
```

### なぜCIDコードが発生するのか

1. **ToUnicode CMapの欠如または不完全**
   - PDFフォントには、CID→Unicodeのマッピング情報（ToUnicode CMap）が埋め込まれるべき
   - しかし、このマップが存在しない、または不完全な場合がある
   - 特に、ダイアクリティカルマーク（発音記号）などの特殊文字で発生しやすい

2. **フォントのサブセット化**
   - PDFファイルサイズ削減のため、使用された文字のみがフォントに含まれる
   - この過程でマッピング情報が失われることがある

3. **ライブラリの制限**
   - pdfplumberはPDFの内部構造を完全に解釈できない場合がある
   - 特に複雑なフォントエンコーディング（Identity-H、Type0など）で問題発生

---

## ベストプラクティス

### 1. ライブラリの選択

#### 📊 2024-2025年の評価

| ライブラリ | CID処理 | 速度 | 表構造抽出 | 推奨用途 |
|-----------|---------|------|-----------|----------|
| **PyMuPDF** | ⭐⭐⭐⭐⭐ | 最速 | ⭐⭐⭐ | CID問題がある文書 |
| **pdfplumber** | ⭐⭐ | 中速 | ⭐⭐⭐⭐⭐ | 表データ抽出 |
| **PyPDF2** | ⭐⭐⭐ | 高速 | ⭐⭐ | 破損したPDF |
| **pdfminer.six** | ⭐⭐⭐ | 低速 | ⭐⭐⭐ | 細粒度制御が必要 |

#### 🎯 選択基準

**PyMuPDFを選ぶべき場合：**
- ✅ CIDコードが多発する文書
- ✅ 処理速度が重要
- ✅ 複雑なフォントエンコーディング（Identity-H、CIDFont）
- ✅ テキスト抽出がメイン

**pdfplumberを選ぶべき場合：**
- ✅ 表データ抽出が必要
- ✅ レイアウト情報の保持が重要
- ✅ 座標ベースの抽出が必要
- ✅ CIDコードが少ない（<5%）

### 2. CID問題への対処法

#### アプローチA：PyMuPDFへの切り替え（推奨度：⭐⭐⭐⭐）

**メリット：**
- CID→Unicode変換を内部で自動処理
- ToUnicode CMapが不完全でも、埋め込みフォントのcmapテーブルを参照
- 処理速度が速い

**デメリット：**
- 出力されるUnicodeが不正確な場合がある（今回のケースで確認済み）
- 表構造の抽出がpdfplumberより弱い

**コード例：**
```python
import fitz  # PyMuPDF

doc = fitz.open('document.pdf')
for page in doc:
    text = page.get_text()  # CID自動変換
    print(text)
doc.close()
```

#### アプローチB：ToUnicode CMMapの手動抽出（推奨度：⭐⭐⭐⭐⭐）

**メリット：**
- 最も正確なマッピングを取得可能
- PDF作成時の意図を尊重
- 一度マッピングを作成すれば再利用可能

**デメリット：**
- 実装が複雑
- 全てのCIDがマップに含まれているとは限らない

**手順：**

1. **PyMuPDFでToUnicode CMapを抽出**
```python
import fitz
doc = fitz.open('document.pdf')
page = doc[0]

# フォント情報を取得
fonts = page.get_fonts(full=True)
for font in fonts:
    xref = font[0]

    # フォントオブジェクトを取得
    obj = doc.xref_object(xref)

    # ToUnicodeストリームを抽出
    if 'ToUnicode' in obj:
        tounicode_xref = # xrefを抽出
        cmap_stream = doc.xref_stream(tounicode_xref)
        # CMAPを解析
```

2. **CMAPからCID→Unicodeマッピングを作成**
```python
import re

# beginbfcharセクションを探す
bfchar_pattern = r'beginbfchar\s+(.*?)\s+endbfchar'
bfchar_matches = re.findall(bfchar_pattern, cmap_text, re.DOTALL)

mappings = {}
for section in bfchar_matches:
    pairs = re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', section)
    for cid_hex, unicode_hex in pairs:
        cid = int(cid_hex, 16)
        # 結合文字の処理（4桁ずつ分割）
        unicode_chars = []
        for i in range(0, len(unicode_hex), 4):
            char_hex = unicode_hex[i:i+4]
            unicode_chars.append(chr(int(char_hex, 16)))
        mappings[cid] = ''.join(unicode_chars)
```

3. **CIDコードを置換**
```python
def replace_cids(text, mappings):
    def replace_cid(match):
        cid_num = int(match.group(1))
        return mappings.get(cid_num, match.group(0))

    return re.sub(r'\(cid:(\d+)\)', replace_cid, text)
```

#### アプローチC：正規表現でCID→ASCII変換（推奨度：⭐）

**⚠️ 注意：この方法は信頼性が低い**

Stack Overflowで提案されている方法ですが、**CID番号は必ずしもUnicode値と一致しない**ため、誤変換が発生します。

```python
import re

def prune_text(text):
    def replace_cid(match):
        ascii_num = int(match.group(1))
        try:
            return chr(ascii_num)  # ⚠️ 誤変換の可能性
        except:
            return ''

    cid_pattern = re.compile(r'\(cid:(\d+)\)')
    return re.sub(cid_pattern, replace_cid, text)
```

**問題点：**
- CID 640 ≠ Unicode U+0640
- クメール語の場合、CID 640 → U+17C0（正しいマッピング）

#### アプローチD：OCR（光学文字認識）（推奨度：⭐⭐）

**メリット：**
- フォント情報に依存しない
- 画像化されたPDFにも対応

**デメリット：**
- 精度が100%ではない
- 処理時間がかかる
- 追加ライブラリのインストールが必要（Tesseract）

**適用場面：**
- ToUnicode CMMapが完全に欠如している
- 他の方法で解決できない場合の最終手段

#### アプローチE：手動修正（推奨度：⭐⭐⭐⭐⭐）

**メリット：**
- 最も確実
- 元のPDFから正しい文字を直接コピー

**デメリット：**
- 手作業が必要
- 時間がかかる

**適用場面：**
- CIDコードが少数（<30件）
- データの正確性が最重要
- 他の自動化手法が失敗した場合

---

## 今回のプロジェクトへの適用

### 現状分析

| 項目 | 値 |
|------|-----|
| 総データ数 | 524行 |
| CID含有データ | 22行（4.3%） |
| ユニークCIDコード | 32種類 |
| CID出現総数 | 71回 |

### 試した方法と結果

#### ✅ 方法1：pdfplumber（現状）
- **結果**: CIDコード発生するが、意味的には正確
- **逆翻訳精度**: スキルトレーニング ✓（技能実習に近い）

#### ❌ 方法2：PyMuPDF
- **結果**: CIDコード発生しないが、Unicode文字コードが誤り
- **逆翻訳精度**: 意味不明 ✗
- **例**: `ករា ហវឹ្កហវឺ្នជំនញា`（ガベージ）

#### ⭐ 方法3：ToUnicode CMap抽出
- **結果**: 32個中10個のCIDマッピングを発見
- **発見率**: 31.25%
- **残り**: 22個（全49ページを調査すれば発見可能性あり）

### 推奨アプローチ

#### 🎯 最適解：ハイブリッドアプローチ

**ステップ1: 全ページToUnicode CMap統合調査**
- 全49ページのフォントCMapを抽出
- 32個のCIDマッピングを可能な限り収集
- 推定成功率：60-80%

**ステップ2: 発見されたマッピングで自動置換**
- 発見されたCID→Unicodeマッピングを適用
- 残りのCIDのみ手動修正

**ステップ3: 残りを手動修正**
- 元のPDFから正しい文字をコピー
- 推定作業量：10-15件（約30分）

**期待される結果：**
- ✅ 70-80%を自動処理
- ✅ 20-30%を手動修正
- ✅ 最終的なデータ精度：100%

---

## 参考文献

### 技術記事
1. **Stack Overflow - How to solve (cid:x) pdfplumber**
   - https://stackoverflow.com/questions/74416930/

2. **PDFから「使える」テキストを取り出す**
   - https://golden-lucky.hatenablog.com/entry/2019/12/05/171340
   - ToUnicode CMapの重要性とcmapテーブル参照方法

3. **PyMuPDF vs pdfplumber 比較（2024-2025）**
   - PyMuPDF: CID処理に優れる、速度最速
   - pdfplumber: 表抽出に優れる、レイアウト保持

### GitHub
- **pdf-rm-tuc**: ToUnicode CMap削除ツール
  - https://github.com/trueroad/pdf-rm-tuc

- **pdfplumber Issue #29**: CID問題の議論
  - https://github.com/jsvine/pdfplumber/issues/29

---

## まとめ

### ✅ やるべきこと

1. **pdfplumberを継続使用**
   - 理由：意味的に正確、表抽出が優秀
   - 欠点：CIDコード発生

2. **ToUnicode CMapから自動抽出**
   - 全49ページを調査
   - 60-80%のCIDを自動解決

3. **残りを手動修正**
   - 元のPDFから正しい文字をコピー
   - 推定10-15件

### ❌ 避けるべきこと

1. **PyMuPDFへの完全移行**
   - Unicode文字コードが不正確
   - 表構造が崩れる

2. **CID→ASCII単純変換**
   - `chr(cid_num)`は信頼性が低い
   - 誤変換が発生

3. **OCR**
   - 精度不安定
   - 処理時間長い
   - 最終手段のみ

---

## 次のステップ

### 提案1: 全ページCMap統合調査（推奨）
```python
# 全49ページのフォントCMapを抽出
# 32個のCIDマッピングを収集
# 自動置換スクリプト作成
```

### 提案2: 部分的自動置換 + 手動修正
```python
# 発見された10個のマッピングで置換
# 残り22個を手動修正
```

### 提案3: 現状のまま使用
```python
# CIDコードを許容
# 必要に応じて後から手動修正
```

**推奨：提案1（全ページCMap統合調査）**

理由：
- 自動化率が最も高い
- 今後の類似PDFにも再利用可能
- 学習価値が高い
