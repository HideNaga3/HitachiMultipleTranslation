"""
「雇用保険」の全言語データを確認
"""
import pandas as pd
import os

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
unified_csv = os.path.join(output_dir, '全言語統合_比較用.csv')

print("=" * 80)
print("「雇用保険」の全言語データ確認")
print("=" * 80)
print()

# CSVを読み込み
df = pd.read_csv(unified_csv, encoding='utf-8-sig')

# 「雇用保険」の行を抽出
employment_insurance_rows = df[df['日本語'] == '雇用保険']

print(f"「雇用保険」の行数: {len(employment_insurance_rows)}行")
print()

if len(employment_insurance_rows) > 0:
    print("各言語のデータ:")
    print()

    for idx, row in employment_insurance_rows.iterrows():
        lang = row['言語']
        translated = row['翻訳']
        page = row['ページ']
        number = row['番号']

        # 翻訳があるかチェック
        has_translation = pd.notna(translated) and str(translated).strip() != ''

        status = "[O]" if has_translation else "[X]"

        print(f"{status} {lang:15s}: 翻訳={'あり' if has_translation else '空欄':4s} - Page={page}, No={number}")
        print()

else:
    print("[情報] 「雇用保険」の行が見つかりませんでした")

print("=" * 80)
print("確認完了")
print("=" * 80)
