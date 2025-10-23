"""
統合CSVのNO・日本語・翻訳のフィルター条件を確認
パターン1: NO空欄 AND 日本語空欄 AND 翻訳空欄
パターン2: NO空欄 AND 日本語空欄 AND 翻訳あり
パターン3: NO空欄 AND 日本語あり AND 翻訳空欄
パターン4: NO空欄 AND 日本語あり AND 翻訳あり
パターン5: NOあり AND 日本語空欄 AND 翻訳空欄
パターン6: NOあり AND 日本語空欄 AND 翻訳あり ★ これが対象
パターン7: NOあり AND 日本語あり AND 翻訳空欄
パターン8: NOあり AND 日本語あり AND 翻訳あり（正常）
"""
import pandas as pd
import os

def is_empty_value(value):
    """値が空かどうか判定（trim/clean後）"""
    if pd.isna(value):
        return True
    if isinstance(value, str):
        cleaned = str(value).strip()
        return cleaned == '' or cleaned.lower() == 'nan'
    return False

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
csv_path = os.path.join(output_dir, '全言語統合_比較用.csv')

print("=" * 80)
print("統合CSV フィルター条件確認")
print("=" * 80)
print()

# CSVを読み込み
df = pd.read_csv(csv_path, encoding='utf-8-sig')
print(f"総行数: {len(df)}行")
print()

# パターン別に分類
patterns = {
    'パターン1: NO空 & 日本語空 & 翻訳空': [],
    'パターン2: NO空 & 日本語空 & 翻訳あり': [],
    'パターン3: NO空 & 日本語あり & 翻訳空': [],
    'パターン4: NO空 & 日本語あり & 翻訳あり': [],
    'パターン5: NOあり & 日本語空 & 翻訳空': [],
    'パターン6: NOあり & 日本語空 & 翻訳あり ★対象': [],
    'パターン7: NOあり & 日本語あり & 翻訳空': [],
    'パターン8: NOあり & 日本語あり & 翻訳あり（正常）': [],
}

for idx, row in df.iterrows():
    no = row['番号']
    jp = row['日本語']
    translated = row['翻訳']

    no_empty = is_empty_value(no)
    jp_empty = is_empty_value(jp)
    tr_empty = is_empty_value(translated)

    if no_empty and jp_empty and tr_empty:
        patterns['パターン1: NO空 & 日本語空 & 翻訳空'].append(idx)
    elif no_empty and jp_empty and not tr_empty:
        patterns['パターン2: NO空 & 日本語空 & 翻訳あり'].append(idx)
    elif no_empty and not jp_empty and tr_empty:
        patterns['パターン3: NO空 & 日本語あり & 翻訳空'].append(idx)
    elif no_empty and not jp_empty and not tr_empty:
        patterns['パターン4: NO空 & 日本語あり & 翻訳あり'].append(idx)
    elif not no_empty and jp_empty and tr_empty:
        patterns['パターン5: NOあり & 日本語空 & 翻訳空'].append(idx)
    elif not no_empty and jp_empty and not tr_empty:
        patterns['パターン6: NOあり & 日本語空 & 翻訳あり ★対象'].append(idx)
    elif not no_empty and not jp_empty and tr_empty:
        patterns['パターン7: NOあり & 日本語あり & 翻訳空'].append(idx)
    else:
        patterns['パターン8: NOあり & 日本語あり & 翻訳あり（正常）'].append(idx)

# 結果表示
print("=" * 80)
print("パターン別集計")
print("=" * 80)
print()

for pattern_name, indices in patterns.items():
    print(f"{pattern_name}: {len(indices)}行")

print()

# パターン6（対象）の詳細を表示
target_indices = patterns['パターン6: NOあり & 日本語空 & 翻訳あり ★対象']

if target_indices:
    print("=" * 80)
    print(f"パターン6の詳細（最初の20行）")
    print("=" * 80)
    print()

    for i, idx in enumerate(target_indices[:20], 1):
        row = df.iloc[idx]
        print(f"{i}. 行ID={row['行ID']}, 言語={row['言語']}, Page={row['ページ']}, NO={row['番号']}")
        print(f"   日本語=空欄")
        print(f"   翻訳={str(row['翻訳'])[:50]}...")
        print()

    if len(target_indices) > 20:
        print(f"... 他 {len(target_indices) - 20}行")
        print()

print("=" * 80)
print("確認完了")
print("=" * 80)
