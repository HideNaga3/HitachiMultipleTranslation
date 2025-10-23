# エラーログ - 日立様多言語翻訳プロジェクト

このファイルには、プロジェクト中に発生したエラーとその対処法を記録します。

---

## エラーログ形式

各エラーは以下の形式で記録：

```
### [YYYY-MM-DD] エラー名

**発生状況**:
- スクリプト: `ファイル名`
- コマンド: `実行コマンド`

**エラー内容**:
```
エラーメッセージ
```

**原因**:
エラーの原因

**対処法**:
解決方法

**ステータス**: [解決済み/未解決/回避済み]

---
```

---

## エラーログ一覧

### [2025-10-23] UnicodeEncodeError - PowerShellでの多言語文字表示エラー

**発生状況**:
- スクリプト: `scripts/check_words_in_categories.py`
- コマンド: `powershell -Command ".venv\Scripts\python.exe scripts\check_words_in_categories.py"`

**エラー内容**:
```
UnicodeEncodeError: 'cp932' codec can't encode character '\u1780' in position 72: illegal multibyte sequence
```

**原因**:
- PowerShellのデフォルト出力エンコーディングがCP932（Shift-JIS）
- カンボジア語（クメール文字: \u1780）、タイ語、ミャンマー語などの文字がCP932では表現できない
- `print(df.head())`で多言語を含むDataFrameを表示しようとした

**対処法**:

1. **ファイル出力にリダイレクト（UTF-8）**:
```powershell
powershell -Command ".venv\Scripts\python.exe script.py > output.txt 2>&1"
```

2. **表示内容を日本語列のみに限定**:
```python
# 修正前
print(df.head())

# 修正後
print(df[['ja']].head())
```

3. **Python内でUTF-8を強制**:
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

4. **ファイルに書き出してから確認**:
```python
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(str(df.head()))
```

**ステータス**: 解決済み

---

### [2025-10-23] TypeError - JSON serialization error (int64)

**発生状況**:
- スクリプト: `scripts/analyze_translation_data.py`
- コマンド: `powershell -Command ".venv\Scripts\python.exe scripts\analyze_translation_data.py"`

**エラー内容**:
```
TypeError: Object of type int64 is not JSON serializable
```

**原因**:
- pandasのint64型はPythonのJSON encoderが直接シリアライズできない
- `language_stats`辞書内にpandasのint64型の値が含まれていた

**対処法**:

1. **int型に変換**:
```python
# 修正前
language_stats[col] = {
    'total': len(df),
    'filled': non_empty_count,
    'empty': empty_count,
    'coverage': coverage
}

# 修正後
language_stats[col] = {
    'total': int(len(df)),
    'filled': int(non_empty_count),
    'empty': int(empty_count),
    'coverage': float(coverage)
}
```

2. **JSONの代わりにテキストファイルで出力**:
```python
# JSON出力を避けてテキストファイルに変更
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(f"総数: {len(df)} 語\n")
```

**ステータス**: 解決済み

---

### [2025-10-23] PowerShellパス解釈エラー - 仮想環境Python実行

**発生状況**:
- スクリプト: `scripts_google_translation/scripts/check_api.py`
- コマンド: `powershell -Command ".venv\Scripts\python.exe scripts_google_translation\scripts\check_api.py"`

**エラー内容**:
```
.venv\Scripts\python.exe : 用語 '.venv' を読み込むことができませんでした。
```

**原因**:
- PowerShellが`.venv\Scripts\python.exe`をモジュール読み込みと解釈
- `powershell -Command`内でのパス解釈の問題

**対処法**:

1. **呼び出し演算子`&`を使用**:
```powershell
powershell -Command "& .\.venv\Scripts\python.exe script.py"
```

2. **フルパスを使用**:
```powershell
powershell -Command "C:\path\to\.venv\Scripts\python.exe script.py"
```

3. **CLAUDE_GLOBAL.mdの推奨方法を使用**:
```powershell
powershell -Command ".venv\Scripts\python.exe -m pip install pandas"
```

**ステータス**: 回避済み（別の方法で実行）

---

## よくあるエラーパターン

### 1. 文字エンコーディング関連
- **症状**: UnicodeEncodeError, UnicodeDecodeError
- **原因**: CP932とUTF-8の混在、多言語文字の扱い
- **予防**: 常にUTF-8を明示、ファイル出力にリダイレクト

### 2. Pandas型とJSON
- **症状**: TypeError: Object of type int64/float64 is not JSON serializable
- **原因**: PandasのNumPy型がJSON非対応
- **予防**: `int()`, `float()`で明示的に変換

### 3. PowerShellパス問題
- **症状**: 用語を読み込むことができませんでした
- **原因**: `.`で始まるパスの解釈問題
- **予防**: `& .\`を使用、またはフルパス指定

### 4. 仮想環境の不在
- **症状**: ModuleNotFoundError
- **原因**: `.venv`が存在しない、または有効化されていない
- **予防**: プロジェクト開始時に`.venv`の存在確認

---

## エラー記録のルール

1. **即座に記録**: エラー発生時は解決後すぐに記録する
2. **詳細に記録**: エラーメッセージ全文、発生状況を詳しく
3. **対処法を明記**: 将来の自分や他の開発者が参照できるように
4. **ステータス更新**: 解決したら必ずステータスを更新

---

最終更新: 2025-10-23
