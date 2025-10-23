# タイ語CSVの列名をデバッグするスクリプト
import pandas as pd
import sys

# UTF-8で出力
output_file = 'for_claude/thai_columns_debug.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

# タイ語CSVを読み込み
csv_file = 'output/【全課統合版】タイ語_げんばのことば_建設関連職種_25cols.csv'
df = pd.read_csv(csv_file, encoding='utf-8-sig', nrows=5)

print(f"列数: {len(df.columns)}\n")

print("列名の詳細（バイト表現含む）:")
print("="*80)

for i, col in enumerate(df.columns, 1):
    print(f"\n列 {i}:")
    print(f"  列名: '{col}'")
    print(f"  長さ: {len(col)}")
    print(f"  Unicode: {[f'U+{ord(c):04X}' for c in col]}")
    print(f"  バイト（UTF-8）: {col.encode('utf-8')}")

    # サンプル値
    sample_value = ''
    for val in df[col]:
        if pd.notna(val) and str(val).strip() != '':
            sample_value = str(val).strip()
            if len(sample_value) > 50:
                sample_value = sample_value[:50] + "..."
            break
    print(f"  サンプル値: {sample_value}")

# 翻訳列候補を検出
print("\n" + "="*80)
print("翻訳データがありそうな列:")
print("="*80)

for col in df.columns:
    if any(df[col].notna() & (df[col].astype(str).str.contains('การ|ผู้|โรง', na=False))):
        print(f"\n列名: '{col}'")
        print("サンプルデータ:")
        for i, val in enumerate(df[col].head(5)):
            if pd.notna(val) and str(val).strip() != '':
                print(f"  行{i+1}: {val}")

sys.stdout.close()
