"""
クリーンアップされたCSVを統合するスクリプト

目的：
1. 各言語のクリーンアップCSVを読み込む
2. 列を日本語に統一してマッピング
3. 全言語統合CSVを出力
"""

import pandas as pd
from pathlib import Path

# 設定
INPUT_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\output_cleaned")
OUTPUT_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\output_cleaned")
OUTPUT_FILE = "全言語統合_v2.csv"

# 出力ディレクトリ作成
OUTPUT_DIR.mkdir(exist_ok=True)

# 言語別のCSVファイルマッピング
LANGUAGE_FILES = {
    '英語': '【全課統合版】英語_げんばのことば_建設関連職種_cleaned.csv',
    'タガログ語': '【全課統合版】タガログ語_げんばのことば_建設関連職種_cleaned.csv',
    'カンボジア語': '【全課統合版】カンボジア語_げんばのことば_建設関連職種_cleaned.csv',
    '中国語': '【全課統合版】中国語_げんばのことば_建設関連職種_cleaned.csv',
    'インドネシア語': '【全課統合版】インドネシア語_げんばのことば_建設関連職種_cleaned.csv',
    'ミャンマー語': '【全課統合版】ミャンマー語_げんばのことば_建設関連職種_cleaned.csv',
    'タイ語': '【全課統合版】タイ語_げんばのことば_建設関連職種_cleaned.csv',
    'ベトナム語': '【全課統合版】ベトナム語_げんばのことば_建設関連職種_cleaned.csv',
}

# 各言語の列マッピング（クリーンアップ後の実際の列名 → 日本語列名）
COLUMN_MAPPINGS = {
    '英語': {
        'No.': '番号',
        'Word/Phrase': '単語',
        'How to read (Hiragana)': '読み方（ひらがな）',
        'Translation': '翻訳',
        'Note': '備考',
        'Example': '例文',
    },
    'タガログ語': {
        'No.': '番号',
        'Talasalitaan': '単語',
        'Paano Magbasa': '読み方（ひらがな）',
        'Pagsasalin': '翻訳',
        'Annotasyon': '備考',
        'Halimbawa': '例文',
    },
    'カンボジア語': {
        'No.': '番号',
        'វាក្យសព្ទ': '単語',
        ' មបៀបអាន': '読み方（ひらがな）',
        'កា បក្ប្រប': '翻訳',
        'ចំណា ព្នយល់': '備考',
        'ឧទាហ ណ៍': '例文',
    },
    '中国語': {
        'No.': '番号',
        '词汇': '単語',
        '读音 （假名）': '読み方（ひらがな）',
        '中文词意': '翻訳',
        '注解': '備考',
        '例句': '例文',
    },
    'インドネシア語': {
        'No.': '番号',
        'Kosakata': '単語',
        'Cara membaca (Hiragana)': '読み方（ひらがな）',
        'Terjemahan': '翻訳',
        'Anotasi': '備考',
        'Contoh': '例文',
    },
    'ミャンマー語': {
        'No.': '番号',
        'ခ ေါဟာရ': '単語',
        'စာဖတ နည ်း': '読み方（ひらがな）',
        'ဘာသာ ြန ဆို  ခင ်း': '翻訳',
        'ဥြမာ': '例文',
    },
    'タイ語': {
        'No.': '番号',
        'ศัพท์': '単語',
        'อ่านว่า': '読み方（ひらがな）',
        'ค าแปล': '翻訳',
        'หมายเหตุ': '備考',
        'ตัวอย่าง': '例文',
    },
    'ベトナム語': {
        'Số': '番号',
        'Từ vựng': '単語',
        'Cách đọc (Hiragana)': '読み方（ひらがな）',
        'Dịch': '翻訳',
        'Chú thích': '備考',
        'Ví dụ câu': '例文',
    },
}


def load_language_csv(language, filename):
    """
    言語別CSVを読み込み、列を日本語に変換

    Args:
        language: 言語名
        filename: CSVファイル名

    Returns:
        DataFrame: 日本語列名に変換されたDataFrame
    """
    filepath = INPUT_DIR / filename
    print(f"\n{'='*80}")
    print(f"読込中: {language} - {filename}")
    print(f"{'='*80}")

    # CSVを読み込み（4行目をヘッダーとして、header=3で指定）
    df = pd.read_csv(filepath, encoding='utf-8-sig', header=3)

    print(f"元の行数: {len(df)}")
    print(f"元の列数: {len(df.columns)}")
    print(f"元の列名: {list(df.columns)}")

    # 列名の空白を除去（前後の空白、複数の空白を1つに）
    df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]

    # 列マッピングを取得
    column_mapping = COLUMN_MAPPINGS.get(language, {})

    # 列名を日本語に変換
    df_renamed = df.rename(columns=column_mapping)

    # 標準列名リスト
    standard_columns = ['番号', '単語', '読み方（ひらがな）', '翻訳', '備考', '例文']

    # 存在しない列を空列として追加
    for col in standard_columns:
        if col not in df_renamed.columns:
            df_renamed[col] = ''

    # 標準列のみを選択
    df_final = df_renamed[standard_columns].copy()

    # 言語列を追加
    df_final['言語'] = language

    # 翻訳列のデータ充足率を計算
    translation_fill = (df_final['翻訳'].notna() & (df_final['翻訳'].astype(str).str.strip() != '')).sum()
    translation_rate = translation_fill / len(df_final) * 100 if len(df_final) > 0 else 0

    print(f"変換後の行数: {len(df_final)}")
    print(f"変換後の列数: {len(df_final.columns)}")
    print(f"翻訳データあり: {translation_fill}/{len(df_final)} ({translation_rate:.1f}%)")

    # サンプル表示
    print(f"\nサンプルデータ（最初の3行）:")
    print(df_final[['番号', '単語', '翻訳', '言語']].head(3))

    return df_final


def main():
    """メイン処理"""
    print(f"{'='*80}")
    print("クリーンアップCSV統合処理開始")
    print(f"{'='*80}")

    all_data = []

    # 各言語のCSVを読み込み
    for language, filename in LANGUAGE_FILES.items():
        try:
            df = load_language_csv(language, filename)
            all_data.append(df)
        except Exception as e:
            print(f"\nエラー: {language} の処理中にエラーが発生しました")
            print(f"  {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

    # 全言語を統合
    if all_data:
        print(f"\n{'='*80}")
        print("全言語データ統合中")
        print(f"{'='*80}")

        df_combined = pd.concat(all_data, ignore_index=True)

        print(f"統合後の総行数: {len(df_combined)}")
        print(f"統合後の総列数: {len(df_combined.columns)}")

        # 言語別の行数を表示
        print(f"\n言語別行数:")
        language_counts = df_combined['言語'].value_counts()
        for lang, count in language_counts.items():
            print(f"  {lang}: {count}行")

        # 翻訳列の全体充足率を計算
        translation_fill = (df_combined['翻訳'].notna() & (df_combined['翻訳'].astype(str).str.strip() != '')).sum()
        translation_rate = translation_fill / len(df_combined) * 100 if len(df_combined) > 0 else 0

        print(f"\n全体の翻訳充足率: {translation_fill}/{len(df_combined)} ({translation_rate:.1f}%)")

        # CSV出力
        output_path = OUTPUT_DIR / OUTPUT_FILE
        df_combined.to_csv(output_path, index=False, encoding='utf-8-sig')

        print(f"\n{'='*80}")
        print(f"統合完了!")
        print(f"{'='*80}")
        print(f"出力ファイル: {output_path}")
        print(f"総行数: {len(df_combined)}")
        print(f"総列数: {len(df_combined.columns)}")
        print(f"列名: {list(df_combined.columns)}")

    else:
        print("\nエラー: 処理できるデータがありません")


if __name__ == '__main__':
    main()
