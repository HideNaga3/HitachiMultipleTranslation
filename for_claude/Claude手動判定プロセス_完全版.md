# Claude AI 手動判定プロセス - 完全版

## 📋 概要

Google Translation APIによる逆翻訳（日本語→外国語→日本語）の品質評価において、difflib（文字列一致）では正確に評価できない同義語ペアを、Claude AIが意味的に判定するプロセス。

### 成果
- **difflib平均**: 52.3%
- **Claude AI平均**: 96.7%
- **改善**: +44.4ポイント
- **処理対象**: 1,297行（869ユニークペア）

---

## 🎯 なぜこの手法が必要か

### 問題点
difflibは文字列の一致度しか見ないため、以下のような同義語ペアを正しく評価できない：

| 元の単語 | 再翻訳 | difflib | 正しい評価 |
|---------|--------|---------|-----------|
| 清掃 | クリーニング | 0% | 100% (完全同義) |
| 給料 | 賃金 | 0% | 100% (完全同義) |
| 指導員 | インストラクター | 0% | 100% (完全同義) |
| 救急箱 | 救急キット | 14% | 95% (ほぼ同義) |
| 技能実習 | 技能訓練 | 50% | 100% (同義) |

### 解決策
Claude AIによる意味的判定を行うことで、専門用語や建設業界用語の同義語を正確に評価できる。

---

## 📊 処理フロー

```
1. 入力データ準備
   ↓
2. ユニークペア抽出（1,297行 → 869ユニークペア）
   ↓
3. バッチ分割（200件ずつ、トークン節約のため）
   ↓
4. Claude AI手動判定（バッチ1-5）
   ↓
5. 全バッチ統合
   ↓
6. 元の1,297行にマッピング
   ↓
7. 最終CSV出力
```

---

## 🔧 詳細手順

### Step 1: 入力データ準備

**入力ファイル**: `比較_AI判定_全行.csv`
- 行数: 1,297行
- 列: アドレス、言語、単語、再翻訳、翻訳、一致、類似度_difflib、分類、類似度_ai

### Step 2: ユニークペア抽出

```python
# スクリプト例
df_all = pd.read_csv('比較_AI判定_全行.csv', encoding='utf-8-sig')
unique_pairs = df_all[['単語', '再翻訳']].drop_duplicates().reset_index(drop=True)
# 結果: 869ユニークペア
```

### Step 3: バッチ分割

トークン使用量を管理するため、200件ずつに分割：

| バッチ | インデックス | 件数 | スクリプト |
|--------|-------------|------|-----------|
| 1 | 0-99 | 100 | `claude_judgment_batch1.py` |
| 2 | 100-299 | 200 | `claude_judgment_batch2.py` |
| 3 | 300-499 | 200 | `claude_judgment_batch3.py` |
| 4 | 500-699 | 200 | `claude_judgment_batch4_manual.py` |
| 5 | 700-868 | 169 | `claude_judgment_batch5_manual.py` |

### Step 4: Claude AI手動判定

#### 4-1. 判定基準

**100点（完全同義）**:
- 意味が完全に同じ
- 例: 清掃/クリーニング、給料/賃金、指導員/インストラクター

**90-99点（ほぼ同義）**:
- 意味がほぼ同じだが、ニュアンスに若干の違い
- 例: 救急箱/救急キット (95点)、技能実習/技能訓練 (95点)

**80-89点（類義語）**:
- 同じカテゴリーで意味が近い
- 例: 労働基準法/雇用基本条件法 (80点)

**50-79点（関連あり）**:
- 意味は異なるが関連性がある
- 例: 火事/やけど (50点)

**0-49点（誤訳・無関連）**:
- 明らかな誤訳または意味が全く異なる
- 例: 支柱/ポーランド人 (0点)、硬さ/暴力 (0点)

#### 4-2. スクリプト構造

```python
"""
Claude AI 手動判定（バッチN: インデックス X-Y）
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd

# Claude AI手動判定結果
claude_judgments = {
    0: 80,   # 翻訳サイネージ / 多言語翻訳システム
    1: 100,  # 技能実習 / 技能実習
    2: 100,  # 技能実習生 / 技能実習生
    # ... 全ペアを手動判定
}

csv_path = r'C:\...\比較_AI判定_全行.csv'
df_all = pd.read_csv(csv_path, encoding='utf-8-sig')
unique_pairs = df_all[['単語', '再翻訳']].drop_duplicates().reset_index(drop=True)
batch = unique_pairs.iloc[START:END].copy()

batch['類似度_claude'] = batch.index.map(lambda idx: f'{claude_judgments.get(idx, 50)}%')
batch['スコア'] = batch.index.map(lambda idx: claude_judgments.get(idx, 50))

output_csv = r'C:\...\ユニークペア_batchN_claude判定.csv'
batch.to_csv(output_csv, index=True, encoding='utf-8-sig')
```

#### 4-3. 実行

```bash
.venv/Scripts/python.exe scripts/claude_judgment_batch1.py
.venv/Scripts/python.exe scripts/claude_judgment_batch2.py
.venv/Scripts/python.exe scripts/claude_judgment_batch3.py
.venv/Scripts/python.exe scripts/claude_judgment_batch4_manual.py
.venv/Scripts/python.exe scripts/claude_judgment_batch5_manual.py
```

### Step 5: 全バッチ統合

**スクリプト**: `merge_all_batches_manual.py`

#### 5-1. 各バッチを読み込み

```python
batches = []
batch_info = [
    (1, 0, 100, 'ユニークペア_batch1_claude判定.csv'),
    (2, 100, 300, 'ユニークペア_batch2_claude判定.csv'),
    (3, 300, 500, 'ユニークペア_batch3_claude判定.csv'),
    (4, 500, 700, 'ユニークペア_batch4_claude判定.csv'),
    (5, 700, 869, 'ユニークペア_batch5_claude判定.csv'),
]

for batch_num, start, end, filename in batch_info:
    df = pd.read_csv(f'output/{filename}', encoding='utf-8-sig', index_col=0)

    # 列数で判定（batch1-3は3列、batch4-5は4列）
    if len(df.columns) >= 4:
        score_data = df.iloc[:, -1]  # 整数
    else:
        score_data = df.iloc[:, -1].str.replace('%', '').astype(int)  # "80%"→80

    df['score'] = score_data
    batches.append(df)
```

#### 5-2. マッピング辞書作成

```python
all_unique = pd.concat(batches, ignore_index=False).sort_index()

mapping = {}
for idx, row in all_unique.iterrows():
    word_col = all_unique.columns[0]
    retrans_col = all_unique.columns[1]
    key = (str(row[word_col]).strip(), str(row[retrans_col]).strip())
    mapping[key] = row['score']

# 結果: 869エントリー
```

#### 5-3. 元データに適用

```python
df_all = pd.read_csv('比較_AI判定_全行.csv', encoding='utf-8-sig')

def get_claude_score(row):
    key = (str(row[word_col_name]).strip(), str(row[retrans_col_name]).strip())
    return mapping.get(key, 50)

df_all['類似度_claude'] = df_all.apply(get_claude_score, axis=1)
```

#### 5-4. 実行

```bash
.venv/Scripts/python.exe scripts/merge_all_batches_manual.py
```

### Step 6: 結果確認

**出力ファイル**: `比較_Claude手動判定_全1297行.csv`

---

## 📈 最終結果

### バッチ別スコア

| バッチ | インデックス | 件数 | 平均スコア | 100%件数 |
|--------|-------------|------|-----------|---------|
| 1 | 0-99 | 100 | 97.3% | 83 (83.0%) |
| 2 | 100-299 | 200 | 98.5% | 184 (92.0%) |
| 3 | 300-499 | 200 | 99.2% | 192 (96.0%) |
| 4 | 500-699 | 200 | 97.4% | 172 (86.0%) |
| 5 | 700-868 | 169 | 87.8% | 108 (63.9%) |
| **合計** | **0-868** | **869** | **96.2%** | **739 (85.0%)** |

### 最終統計（全1,297行）

| 評価基準 | 件数 | 割合 |
|---------|------|------|
| 100%（完全一致） | 1,105 | 85.2% |
| 90%以上 | 1,188 | 91.6% |
| 80%以上 | 1,251 | 96.5% |
| 50%以上 | 1,275 | 98.3% |
| 50%未満 | 22 | 1.7% |

### 改善効果

- **difflib平均**: 52.3%
- **Claude AI平均**: 96.7%
- **改善**: **+44.4ポイント** 🎉

---

## 🔍 重要な判定例

### 完全同義（100点）

| 単語 | 再翻訳 | 理由 |
|------|--------|------|
| 清掃 | クリーニング | 完全に同じ意味 |
| 給料 | 賃金 | 労働法用語として同義 |
| 指導員 | インストラクター | 完全に同じ職種 |
| 整備（する） | メンテナンス/サービス | 技術用語として同義 |
| 清掃 | クリーン | 動詞・名詞の違いのみ |

### 高類似度（90-99点）

| 単語 | 再翻訳 | スコア | 理由 |
|------|--------|--------|------|
| 救急箱 | 救急キット | 95 | ほぼ同じだが表現が異なる |
| 技能実習 | 技能訓練 | 95 | 同じ制度を指す |
| 一輪車 | 手押し車 | 95 | 建設現場で同じ道具 |

### 誤訳例（0-30点）

| 単語 | 再翻訳 | スコア | 理由 |
|------|--------|--------|------|
| 支柱 | ポーランド人 | 0 | pole（柱）とPole（ポーランド人）の誤訳 |
| 硬さ | 暴力 | 0 | hardness（硬さ）とviolence（暴力）の誤訳 |
| 標識 | 星座 / 牡羊座管 | 0 | sign（標識）とsign（星座）の誤訳 |
| 調子 | 州 | 0 | 全く無関係 |
| 縛る | ネクタイ | 30 | tie（縛る）とtie（ネクタイ）の誤訳 |

---

## 📁 関連ファイル

### 入力ファイル
- `output/比較_AI判定_全行.csv` - 元データ（1,297行）

### 判定スクリプト
- `scripts/claude_judgment_batch1.py` - バッチ1判定（0-99）
- `scripts/claude_judgment_batch2.py` - バッチ2判定（100-299）
- `scripts/claude_judgment_batch3.py` - バッチ3判定（300-499）
- `scripts/claude_judgment_batch4_manual.py` - バッチ4判定（500-699）
- `scripts/claude_judgment_batch5_manual.py` - バッチ5判定（700-868）

### 統合スクリプト
- `scripts/merge_all_batches_manual.py` - 全バッチ統合

### 中間ファイル
- `output/ユニークペア_batch1_claude判定.csv` - バッチ1結果
- `output/ユニークペア_batch2_claude判定.csv` - バッチ2結果
- `output/ユニークペア_batch3_claude判定.csv` - バッチ3結果
- `output/ユニークペア_batch4_claude判定.csv` - バッチ4結果
- `output/ユニークペア_batch5_claude判定.csv` - バッチ5結果

### 出力ファイル
- `output/比較_Claude手動判定_全1297行.csv` - **最終結果**

---

## ⚠️ トラブルシューティング

### エラー1: UnicodeEncodeError

**エラー**: `'cp932' codec can't encode character`

**解決策**:
```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### エラー2: KeyError（列名の文字化け）

**原因**: Windowsコンソールでの日本語列名の文字化け

**解決策**:
- 列インデックスを使用（`df.iloc[:, -1]`）
- または英語列名で統一（`df['score']`）

### エラー3: TypeError（文字列を数値として計算）

**原因**: "80%"という文字列を平均計算しようとした

**解決策**:
```python
score_data = df.iloc[:, -1].str.replace('%', '').astype(int)
```

### エラー4: 列数の不一致

**原因**: バッチ1-3は3列、バッチ4-5は4列

**解決策**:
```python
if len(df.columns) >= 4:
    score_data = df.iloc[:, -1]  # 整数列
else:
    score_data = df.iloc[:, -1].str.replace('%', '').astype(int)  # "%"列
```

---

## 💡 ベストプラクティス

### 1. バッチサイズの決定

- **推奨**: 100-200ペア/バッチ
- **理由**: トークン使用量とのバランス
- **Claude Code Max プラン**: 約200,000トークン/セッション

### 2. 判定時の注意点

**意味を重視する**:
- 文字列の一致ではなく、意味の同一性を判断
- 専門用語の同義語を正しく認識

**コンテキストを考慮する**:
- 建設業界用語の特性を理解
- 労働法用語の正確性を重視

**一貫性を保つ**:
- 同じ基準で全ペアを判定
- 類似したペアは同じスコアに

### 3. マッピング辞書の活用

ユニークペア（869）を判定し、全行（1,297）にマッピングすることで：
- **効率化**: 重複判定を避ける
- **一貫性**: 同じペアは必ず同じスコア
- **トークン節約**: 約30%削減

### 4. ファイル名規則

- バッチファイル: `ユニークペア_batch{N}_claude判定.csv`
- 最終ファイル: `比較_Claude手動判定_全{行数}行.csv`
- エンコーディング: 常に `utf-8-sig`

---

## 🔄 次回実行時の手順

### 準備

1. 新しい比較データCSVを準備
2. ユニークペア数を確認
3. バッチ数を決定（200件/バッチが目安）

### 実行

```bash
# Step 1: バッチ判定スクリプトを作成（このドキュメントを参照）
# Step 2: 各バッチを実行
.venv/Scripts/python.exe scripts/claude_judgment_batch1.py
.venv/Scripts/python.exe scripts/claude_judgment_batch2.py
# ... 以下同様

# Step 3: 統合実行
.venv/Scripts/python.exe scripts/merge_all_batches_manual.py
```

### 確認

1. 各バッチの平均スコアを確認
2. 異常に低いスコアのバッチをチェック
3. 最終統計を確認（平均90%以上が目安）
4. difflib との改善ポイントを確認

---

## 📊 活用方法

### 翻訳品質レポート

このデータを使用して：
1. 言語別の翻訳精度を評価
2. 誤訳パターンを分析
3. 改善が必要な用語を特定

### データベース構築

高スコアのペアを使用して：
1. 建設業界用語の同義語辞書を構築
2. 多言語翻訳システムの精度向上
3. 翻訳APIの選定基準として活用

### 継続的改善

1. 低スコアペアの原因分析
2. Google Translate以外のAPIとの比較
3. 専門用語辞書の充実

---

## ✅ チェックリスト

次回実行時の確認項目：

- [ ] 入力CSVファイルの列構成を確認
- [ ] ユニークペア数を確認
- [ ] バッチサイズを決定（100-200が目安）
- [ ] 各バッチ判定スクリプトを作成
- [ ] UTF-8エンコーディングを設定
- [ ] 判定基準を統一（同義語=100%）
- [ ] 各バッチを実行
- [ ] 統合スクリプトを実行
- [ ] 最終統計を確認（90%以上が目標）
- [ ] 出力CSVの内容を確認

---

## 📝 まとめ

この手法により、機械的な文字列一致（difflib: 52.3%）から、意味を考慮した評価（Claude AI: 96.7%）へと**+44.4ポイント**の改善を達成しました。

特に建設業界用語や労働法用語のような専門用語において、同義語を正確に認識できることが、この手法の最大の利点です。

**次回も同じ手順で実行可能です。**

---

**作成日**: 2025-01-24
**プロジェクト**: 三菱様_多言語翻訳_202510
**処理対象**: インドネシア語逆翻訳データ（1,297行、869ユニークペア）
