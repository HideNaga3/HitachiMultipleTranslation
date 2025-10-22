# 統合CSVファイルで翻訳列が空の行をチェックするスクリプト
import pandas as pd

# CSVファイルを読み込み
input_file = 'output_cleaned/全言語統合.csv'
df = pd.read_csv(input_file, encoding='utf-8-sig')

print(f"総行数: {len(df)}")
print(f"列数: {len(df.columns)}")
print(f"\n列名:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

# 翻訳列が空の行を確認
if '翻訳' in df.columns:
    # 翻訳列がNaN、空文字列、またはスペースのみの行を検出
    empty_translation = df[
        df['翻訳'].isna() |
        (df['翻訳'].astype(str).str.strip() == '') |
        (df['翻訳'].astype(str).str.strip() == 'nan')
    ]

    print(f"\n翻訳列が空の行数: {len(empty_translation)}")

    if len(empty_translation) > 0:
        print("\n翻訳が空の行（最初の20件）:")
        print("="*80)
        for idx, row in empty_translation.head(20).iterrows():
            lang = row.get('言語', 'N/A')
            page = row.get('PDFページ番号', 'N/A')
            no = row.get('番号', 'N/A')
            word = row.get('単語', 'N/A')
            translation = row.get('翻訳', 'N/A')

            print(f"行番号: {idx+2}")  # +2はヘッダー行とインデックスのずれを調整
            print(f"  言語: {lang}")
            print(f"  PDFページ番号: {page}")
            print(f"  番号: {no}")
            print(f"  単語: {word}")
            print(f"  翻訳: '{translation}'")
            print("-"*80)

        # 言語別の翻訳が空の行数をカウント
        print("\n言語別の翻訳が空の行数:")
        if '言語' in df.columns:
            lang_counts = empty_translation['言語'].value_counts()
            for lang, count in lang_counts.items():
                total = len(df[df['言語'] == lang])
                print(f"  {lang}: {count}行 / {total}行 ({count/total*100:.1f}%)")
else:
    print("\nエラー: '翻訳'列が見つかりません")
