# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 重要 / Important

**このファイルを読み込む際は、必ず `CLAUDE_GLOBAL.md` も一緒に読み込んでください。**

`CLAUDE_GLOBAL.md` には、すべてのプロジェクトに共通するグローバル設定が記載されています。

**When reading this file, always read `CLAUDE_GLOBAL.md` together.**

`CLAUDE_GLOBAL.md` contains global settings that apply to all projects.

---

## 【プロジェクト設定】Project Settings

このセクションには、このプロジェクト固有の設定を記載します。

### 概要

このドキュメントは、Claude Code が多言語翻訳プロジェクトで作業する際のガイドラインを提供します。

### プロジェクト固有のルール

#### プロジェクト概要

**プロジェクト名**: 三菱様_多言語翻訳_202510

**目的**: 建設関連職種の多言語辞書PDFから表データを抽出し、CSV形式で保存・加工

**対象データ**:
- 「げんばのことば」建設関連職種用語集
- 言語: 日本語を基準に、英語、タガログ語、カンボジア語、中国語、インドネシア語、ミャンマー語、タイ語、ベトナム語の8言語
- PDFファイルの場所: `建設関連PDF/` フォルダ

#### ファイル構成

```
三菱様_多言語翻訳_202510/
├── 建設関連PDF/          # 入力PDFファイル（8言語）
├── scripts/              # Pythonスクリプト
│   └── extract_tables_from_pdf.py  # PDFテーブル抽出スクリプト
├── output/               # 抽出されたCSVファイル
├── for_claude/           # Claude用の作業ログ
│   └── log.txt          # セッション間の引継ぎ情報
├── .venv/                # Python仮想環境
├── CLAUDE.md            # プロジェクト固有設定（このファイル）
└── CLAUDE_GLOBAL.md     # グローバル設定
```

#### 使用ライブラリ

- **PyMuPDF (fitz)** (1.26.5): PDFから表を抽出（推奨 - CIDコード問題なし）
- **pdfplumber** (0.11.7): PDFから表を抽出（CIDコード問題あり - 非推奨）
- **pandas** (2.3.3): データ処理とCSV出力
- **openpyxl** (3.1.5): Excel処理

#### 重要な技術仕様

- **エンコーディング**: CSV出力は UTF-8 BOM 形式
- **ファイル命名規則**: `{PDFファイル名}_{列数}cols.csv`
- **データ構造**: 各PDFの表構造は異なる（列数が26～50列まで様々）
- **表の内容**:
  - ページ番号 (Page)
  - 表番号 (Table)
  - 番号 (No.)
  - 単語/フレーズ
  - 読み方（ひらがな）
  - 翻訳
  - 備考
  - 例文
  - その他の列（言語によって異なる）

#### 既知の問題と対処方法

**詳細なエラー対処法は `for_claude/エラー対処法.md` を参照してください。**

1. **CIDコード問題（重要）**
   - 問題: pdfplumberがクメール語・タイ語のダイアクリティカルマークをCIDコードとして出力
   - 例: `(cid:688)បព័ន(cid:640)`
   - 対処: **PyMuPDFを使用（推奨）** - CIDコード問題が発生しない
   - 詳細: `for_claude/エラー対処法.md` の「5. CIDコード問題」参照

2. **UnicodeEncodeError (頻発)**
   - 問題: `'cp932' codec can't encode character` エラー
   - 対処: スクリプト先頭に以下を追加
     ```python
     import sys, io
     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
     ```
   - 詳細: `for_claude/エラー対処法.md` の「1. UnicodeEncodeError」参照

3. **表ヘッダーのNone値**
   - 問題: PDFから抽出した表のヘッダーにNone値が含まれる
   - 対処: `Column_{i}` 形式に自動変換

4. **列数の不一致**
   - 問題: 同じPDF内でも表ごとに列数が異なる
   - 対処: 最大列数に揃えて空文字列で補完
   - 詳細: `for_claude/エラー対処法.md` の「3. ValueError」参照

5. **PyMuPDF API変更**
   - 問題: `TypeError: object of type 'TableFinder' has no len()`
   - 対処: `table_finder = page.find_tables(); tables = table_finder.tables`
   - 詳細: `for_claude/エラー対処法.md` の「2. TypeError」参照

#### 進行状況

- [完了] Phase 1: PDFテーブル抽出スクリプト作成
- [完了] Phase 2: 8言語のPDFからCSV抽出
- [完了] Phase 3: CSVデータの統合・加工（全言語統合CSVを作成、4,146行、翻訳充足率99.4%）
- [完了] Phase 4: Google Translation APIプロジェクトとの統合（翻訳品質チェック機能）
- [未実施] Phase 5: 多言語データベースの構築（必要に応じて）

---

## サブプロジェクト: Google Translation APIプロジェクト

**場所**: `scripts_google_translation/`

### 概要
Google Cloud Translation API v2を使用した往復翻訳システム。抽出した翻訳データの品質検証や、欠損データの補完に使用可能。

### 主要機能

#### 1. 単一ファイル翻訳
- **translate_from_csv()**: CSVファイルからの一括翻訳
- **translate_from_excel()**: Excelファイルからの一括翻訳
- 列インデックス指定機能（0始まり）
- シート名指定機能（Excel）

#### 2. 複数ファイル一括翻訳
- **translate_from_multiple_csv()**: 複数CSVの一括翻訳
- **translate_from_multiple_excel()**: 複数Excelの一括翻訳
- 列構造チェック機能
- 全ファイルを1つのCSVに統合出力
- ファイル名列で元ファイルを識別

#### 3. 往復翻訳機能
- **round_trip_translate()**: 日本語→他言語→日本語の往復翻訳
- **round_trip_translate_batch()**: 複数テキストの往復翻訳
- 完全一致判定機能（is_perfect_match）
- 翻訳品質の自動評価

#### 4. サポート機能
- サポート言語一覧取得（193言語）
- API接続確認とIP制限エラー検出
- 列構造チェック（check_csv_structure, check_excel_structure）

### 技術仕様

- **API**: Google Cloud Translation API v2（REST API）
- **認証**: APIキー認証（.env管理）
- **言語コード**: ISO 639-1形式（en, ja, zh-CN, ko, など）
- **対応言語数**: 193言語
- **HTTPライブラリ**: requests
- **Excelライブラリ**: openpyxl
- **データ処理**: pandas 2.3.3
- **出力形式**: CSV（UTF-8 BOM）、JSON（UTF-8）

### ファイル構成

```
scripts_google_translation/
├── scripts/
│   ├── translator.py                    # 翻訳機能の中核
│   ├── batch_translator.py              # CSV/Excel一括処理
│   ├── check_api.py                     # API接続確認
│   ├── test_translation.py              # 翻訳テスト
│   ├── test_round_trip.py               # 往復翻訳テスト
│   ├── test_batch_translation.py        # 総合テスト
│   ├── test_multiple_files.py           # 複数ファイル処理テスト
│   ├── get_supported_languages.py       # サポート言語取得
│   ├── create_test_files.py             # テストファイル自動生成
│   ├── create_multiple_test_files.py    # 複数テストファイル生成
│   ├── run_multiple_csv_test.py         # CSV一括翻訳テスト
│   └── run_multiple_excel_test.py       # Excel一括翻訳テスト
├── for_claude/
│   ├── log.txt                          # Google Translation API作業ログ
│   └── supported_languages.json         # サポート言語一覧
├── test_data/                           # テストデータ
├── output/                              # 翻訳結果出力
├── .env                                 # APIキー（Git除外）
├── requirements.txt                     # Python依存パッケージ
└── CLAUDE.md                            # プロジェクト設定
```

### 使用例

```python
from scripts_google_translation.scripts.batch_translator import translate_from_csv, translate_from_multiple_csv

# 単一CSVファイルの翻訳
result = translate_from_csv('input.csv', column_index=0, intermediate_lang='en')
print(f"完全一致率: {result['perfect_match_rate']:.1f}%")

# 複数CSVファイルを1つに統合して翻訳
files = ['file1.csv', 'file2.csv', 'file3.csv']
result = translate_from_multiple_csv(
    file_paths=files,
    column_index=0,
    intermediate_lang='en',
    check_structure=True
)
print(f"出力ファイル: {result['output_file']}")
print(f"総翻訳件数: {result['total_count']}")
print(f"完全一致率: {result['perfect_match_rate']:.1f}%")
```

### テスト結果

- **CSV翻訳テスト**: 88.9%完全一致率（18件中16件）
- **Excel翻訳テスト**: 100.0%完全一致率（18件中18件）
- **API接続**: 正常動作中（IP制限なし）

### 統合活用案

1. **PDF抽出データの翻訳品質チェック**
   - `output/全言語統合_pdfplumber_最終版.csv`に対して往復翻訳を実行
   - 翻訳の正確性を検証（完全一致率の計算）

2. **空欄翻訳の補完**
   - 翻訳が空欄のデータ（0.6%、約24行）を自動翻訳

3. **言語間の整合性チェック**
   - 8言語間で翻訳の整合性を検証
