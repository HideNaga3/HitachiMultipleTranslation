"""
フィルター条件をPython df形式で表示
"""
import pandas as pd
import os

def is_empty_value(value):
    """値が空かどうか判定"""
    if pd.isna(value):
        return True
    if isinstance(value, str):
        cleaned = str(value).strip()
        return cleaned == '' or cleaned.lower() == 'nan'
    return False

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
csv_path = os.path.join(output_dir, '全言語統合_比較用.csv')

# CSVを読み込み
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("フィルター条件（Python df形式）")
print("=" * 80)
print()

# 空欄判定用のカラムを追加
df['NO空欄'] = df['番号'].apply(is_empty_value)
df['日本語空欄'] = df['日本語'].apply(is_empty_value)
df['翻訳空欄'] = df['翻訳'].apply(is_empty_value)

print("各パターンのフィルター条件:")
print()

patterns = {
    'パターン1: NO空 & 日本語空 & 翻訳空':
        "(df['NO空欄']) & (df['日本語空欄']) & (df['翻訳空欄'])",

    'パターン2: NO空 & 日本語空 & 翻訳あり':
        "(df['NO空欄']) & (df['日本語空欄']) & (~df['翻訳空欄'])",

    'パターン3: NO空 & 日本語あり & 翻訳空':
        "(df['NO空欄']) & (~df['日本語空欄']) & (df['翻訳空欄'])",

    'パターン4: NO空 & 日本語あり & 翻訳あり':
        "(df['NO空欄']) & (~df['日本語空欄']) & (~df['翻訳空欄'])",

    'パターン5: NOあり & 日本語空 & 翻訳空':
        "(~df['NO空欄']) & (df['日本語空欄']) & (df['翻訳空欄'])",

    'パターン6: NOあり & 日本語空 & 翻訳あり ★対象':
        "(~df['NO空欄']) & (df['日本語空欄']) & (~df['翻訳空欄'])",

    'パターン7: NOあり & 日本語あり & 翻訳空':
        "(~df['NO空欄']) & (~df['日本語空欄']) & (df['翻訳空欄'])",

    'パターン8: NOあり & 日本語あり & 翻訳あり（正常）':
        "(~df['NO空欄']) & (~df['日本語空欄']) & (~df['翻訳空欄'])",
}

for pattern_name, condition in patterns.items():
    # 条件を評価
    filtered = df[eval(condition)]
    count = len(filtered)

    print(f"{pattern_name}: {count}行")
    print(f"  条件式: {condition}")
    print()

print("=" * 80)
print("簡易版（pandasの標準記法）")
print("=" * 80)
print()

# パターン6の例
print("パターン6（対象）の抽出:")
print("  filtered_df = df[(~df['NO空欄']) & (df['日本語空欄']) & (~df['翻訳空欄'])]")
print()

filtered_pattern6 = df[(~df['NO空欄']) & (df['日本語空欄']) & (~df['翻訳空欄'])]
print(f"  結果: {len(filtered_pattern6)}行")
print()

if len(filtered_pattern6) > 0:
    print("  サンプル:")
    print(filtered_pattern6[['行ID', '言語', 'ページ', '番号', '日本語', '翻訳']].head(10))
else:
    print("  該当データなし")

print()

# パターン2の例（NO空 & 日本語空 & 翻訳あり）
print("-" * 80)
print("パターン2（NO空 & 日本語空 & 翻訳あり）の抽出:")
print("  filtered_df = df[(df['NO空欄']) & (df['日本語空欄']) & (~df['翻訳空欄'])]")
print()

filtered_pattern2 = df[(df['NO空欄']) & (df['日本語空欄']) & (~df['翻訳空欄'])]
print(f"  結果: {len(filtered_pattern2)}行")
print()

if len(filtered_pattern2) > 0:
    print("  サンプル:")
    for idx in range(min(5, len(filtered_pattern2))):
        row = filtered_pattern2.iloc[idx]
        print(f"  {idx+1}. 行ID={row['行ID']}, 言語={row['言語']}, Page={row['ページ']}, 翻訳={str(row['翻訳'])[:40]}...")

print()
print("=" * 80)
