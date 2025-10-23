"""
Excelファイルから直接読み込んで統合するスクリプト

目的：
1. 各言語のExcelファイルを直接読み込む
2. 列を日本語に統一してマッピング
3. 全言語統合CSVを出力
"""

import pandas as pd
from pathlib import Path

# 設定
EXCEL_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\建設関係Excel")
OUTPUT_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\output_cleaned")
OUTPUT_FILE = "全言語統合_最終版.csv"

# 出力ディレクトリ作成
OUTPUT_DIR.mkdir(exist_ok=True)

# 言語別のExcelファイルマッピング
LANGUAGE_FILES = {
    '英語': '【全課統合版】英語_げんばのことば_建設関連職種.xlsx',
    'タガログ語': '【全課統合版】タガログ語_げんばのことば_建設関連職種.xlsx',
    'カンボジア語': '【全課統合版】カンボジア語_げんばのことば_建設関連職種.xlsx',
    '中国語': '【全課統合版】中国語_げんばのことば_建設関連職種.xlsx',
    'インドネシア語': '【全課統合版】インドネシア語_げんばのことば_建設関連職種.xlsx',
    'ミャンマー語': '【全課統合版】ミャンマー語_げんばのことば_建設関連職種.xlsx',
    'タイ語': '【全課統合版】タイ語_げんばのことば_建設関連職種.xlsx',
    'ベトナム語': '【全課統合版】ベトナム語_げんばのことば_建設関連職種.xlsx',
}

# 各言語の列マッピング（実際の列名 → 日本語列名）
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
        'មបៀបអាន': '読み方（ひらがな）',
        'កា បក្ប្រប': '翻訳',
        'ចំណាព្នយល់': '備考',
        'ឧទាហណ៍': '例文',
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
        'ခေါဟာရ': '単語',
        'စာဖတ်နည်း': '読み方（ひらがな）',
        'ဘာသာ ြန ဆို  ခင ်း': '翻訳',
        'ဥပမာ': '例文',
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


def load_language_excel(language, filename):
    """
    言語別Excelを読み込み、列を日本語に変換

    Args:
        language: 言語名
        filename: Excelファイル名

    Returns:
        DataFrame: 日本語列名に変換されたDataFrame
    """
    filepath = EXCEL_DIR / filename
    print(f"\n{'='*80}")
    print(f"読込中: {language} - {filename}")
    print(f"{'='*80}")

    # Excelを読み込み（3行目をヘッダーとして、header=2で指定）
    df = pd.read_excel(filepath, sheet_name=0, header=2)

    print(f"元の行数: {len(df)}")
    print(f"元の列数: {len(df.columns)}")

    # 列名の空白を除去・正規化
    df.columns = [str(col).strip() if col is not None else '' for col in df.columns]

    # Excel行番号を保存（header=2なので、実際の行番号は index + 3）
    df['Excel行'] = df.index + 3

    # 列マッピングを取得
    column_mapping = COLUMN_MAPPINGS.get(language, {})

    # 列マッピングの空白も正規化
    column_mapping_normalized = {k.strip(): v for k, v in column_mapping.items()}

    # 列名を日本語に変換
    df_renamed = df.rename(columns=column_mapping_normalized)

    # 必要な列名リスト（ユーザー指定の5列）
    required_columns = ['番号', '単語', '翻訳']

    # 存在しない列を空列として追加
    for col in required_columns:
        if col not in df_renamed.columns:
            df_renamed[col] = ''

    # 言語列を追加
    df_renamed['言語'] = language

    # 必要な列のみを選択
    df_final = df_renamed[['言語', 'Excel行', '番号', '単語', '翻訳']].copy()

    # 番号列がNaNの行を除外
    df_final = df_final[df_final['番号'].notna()].copy()

    # 番号が数字の行のみを残す
    def is_number(val):
        """値が数字かどうかをチェック"""
        if pd.isna(val):
            return False
        try:
            # 文字列に変換して数値に変換できるかチェック
            float(str(val).strip())
            return True
        except (ValueError, TypeError):
            return False

    df_final = df_final[df_final['番号'].apply(is_number)].copy()

    # 翻訳列のデータ充足率を計算
    translation_fill = (df_final['翻訳'].notna() & (df_final['翻訳'].astype(str).str.strip() != '')).sum()
    translation_rate = translation_fill / len(df_final) * 100 if len(df_final) > 0 else 0

    print(f"変換後の行数: {len(df_final)}")
    print(f"変換後の列数: {len(df_final.columns)}")
    print(f"翻訳データあり: {translation_fill}/{len(df_final)} ({translation_rate:.1f}%)")

    # サンプル表示
    print(f"\nサンプルデータ（最初の3行）:")
    try:
        print(df_final[['言語', 'Excel行', '番号', '単語', '翻訳']].head(3).to_string())
    except Exception as e:
        print(f"  サンプル表示エラー: {e}")

    return df_final


def main():
    """メイン処理"""
    print(f"{'='*80}")
    print("Excelファイル直接統合処理開始")
    print(f"{'='*80}")

    all_data = []

    # 各言語のExcelを読み込み
    for language, filename in LANGUAGE_FILES.items():
        try:
            df = load_language_excel(language, filename)
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
