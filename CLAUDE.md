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
├── script/               # Pythonスクリプト
│   └── extract_tables_from_pdf.py  # PDFテーブル抽出スクリプト
├── output/               # 抽出されたCSVファイル
├── for_claude/           # Claude用の作業ログ
│   └── log.txt          # セッション間の引継ぎ情報
├── .venv/                # Python仮想環境
├── CLAUDE.md            # プロジェクト固有設定（このファイル）
└── CLAUDE_GLOBAL.md     # グローバル設定
```

#### 使用ライブラリ

- **pdfplumber** (0.11.4): PDFから表を抽出
- **pandas** (2.2.3): データ処理とCSV出力
- **openpyxl** (3.1.5): Excel処理（将来の拡張用）

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

1. **表ヘッダーのNone値**
   - 問題: PDFから抽出した表のヘッダーにNone値が含まれることがある
   - 対処: `Column_{i}` 形式に自動変換

2. **列数の不一致**
   - 問題: 同じPDF内でも表ごとに列数が異なる場合がある
   - 対処: 全列名を収集し、不足列を空文字列で補完してから連結

3. **文字エンコーディング**
   - 問題: 多言語文字（タイ語、ミャンマー語、クメール語など）を扱う
   - 対処: UTF-8 BOM エンコーディングを使用

#### 進行状況

- [完了] Phase 1: PDFテーブル抽出スクリプト作成
- [完了] Phase 2: 8言語のPDFからCSV抽出
- [未実施] Phase 3: CSVデータの統合・加工（必要に応じて）
- [未実施] Phase 4: 多言語データベースの構築（必要に応じて）
