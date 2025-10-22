# 全言語のCSVファイルを統合するスクリプト（改善版v2）
import pandas as pd
from pathlib import Path
import os

# 各言語の列名マッピング（言語固有の列名 → 日本語の統一列名）
COLUMN_MAPPINGS = {
    '英語': {
        'No.': '番号',
        'Word/Phrase': '単語',
        'Translation': '翻訳',
        'How to read (Hiragana)': '読み方（ひらがな）',
        'Note': '備考',
        'Example': '例文',
        'Picture': '写真',
        'Sign': '標識',
    },
    'タガログ語': {
        'No.': '番号',
        'Talasalitaan': '単語',
        'Pagsasalin': '翻訳',
        'Paano Magbasa': '読み方（ひらがな）',
        'Annotasyon': '備考',
        'Halimbawa': '例文',
        'Larawan': '写真',
        'Palatandaan': '標識',
    },
    'カンボジア語': {
        'No.': '番号',
        'វាក្យសព្ទ': '単語',
        'កា បក្ប្រប': '翻訳',
        'មបៀបអាន': '読み方（ひらがな）',
        # 備考・説明の列（複数の表記ゆれがあるので全て統合）
        'ចាំណា ពនយល់': '備考',
        'ចំ(cid:622)រពន(cid:679)ល់': '備考',
        'ចំណា ពនយល់': '備考',
        'ចំណា ព្នយល់': '備考',
        'ច្ំណា ពនយល់': '備考',
        'ច្ំណា ព្នយល់': '備考',
        # 例文の列
        'ឧ(cid:637)ហរណ៍': '例文',
        'ឧទាហ ណ៍': '例文',
        'ឧទាហ ណ្៍': '例文',
        'ឧទាហ្ ណ៍': '例文',
        # 写真の列
        'រូបថត': '写真',
        'បូ ថត': '写真',
        'រេប(cid:827)ប(cid:738)ន': '読み方（ひらがな）',
        # 標識の列
        'សញ្ញា': '標識',
        # その他の単語列（表記ゆれ）
        'វាកយសពទ': '単語',
        'វាកយសព្ទ': '単語',
        'វាក្យសពទ': '単語',
        'វាក្យសព្ា': '単語',
        # その他の翻訳列（表記ゆれ）
        '(cid:535)របកែ(cid:688)ប': '翻訳',
        '(cid:700)ក(cid:679)សព(cid:635)': '単語',
        'កា បកដរប': '翻訳',
        'កា បកប្រប': '翻訳',
        'កា បក្ប្គ្ប': '翻訳',
        'កា បក្ប្្ប': '翻訳',
        'កា រក្ប្ប្រ': '翻訳',
        # 読み方の列（表記ゆれ）
        'មរៀរអាន': '読み方（ひらがな）',
    },
    '中国語': {
        'No.': '番号',
        '词汇': '単語',
        '中文词意': '翻訳',
        '读音 （假名）': '読み方（ひらがな）',
        '注解': '備考',
        '例句': '例文',
        '照片': '写真',
        '标识': '標識',
    },
    'インドネシア語': {
        'No.': '番号',
        'Kosakata': '単語',
        'Terjemahan': '翻訳',
        'Cara membaca (Hiragana)': '読み方（ひらがな）',
        'Anotasi': '備考',
        'Annotasyon': '備考',
        'Contoh': '例文',
        'Foto': '写真',
        'Tanda': '標識',
    },
    'ミャンマー語': {
        'No.': '番号',
        'ခ ေါဟာရ': '単語',
        'ဘာသာ ြန ဆ ို ခင်း': '翻訳',
        'စာဖတန ည်း': '読み方（ひらがな）',
        'မှတခ ျက': '備考',
        'ဥြမာ': '例文',
        'အမှတအ သာ်း/ဆငို ်း ဘတို': '標識',
    },
    'タイ語': {
        # PDF抽出版（タイ語列名）
        'No.': '番号',
        'ศพั ท์': '単語',
        'คา แปล': '翻訳',
        'อา่ นวา่': '読み方（ひらがな）',
        # 読み方の列（表記ゆれ）
        'วธิ ก ีารอา่ น': '読み方（ひらがな）',
        'วธิ ก ีำรอำ่ น': '読み方（ひらがな）',
        'วิธกีารอ่าน': '読み方（ひらがな）',
        # 備考の列（表記ゆれ）
        'ความคดิ เห็น': '備考',
        'ความคิดเห็น': '備考',
        'ควำมคดิ เห็น': '備考',
        'หมายเหตุ': '備考',
        'เหตผุ ล': '備考',
        'เหตุผล': '備考',
        # 例文の列（表記ゆれ）
        'ตว ัอย่าง': '例文',
        'ตวั อยา่ ง': '例文',
        'ตวัอย่าง': '例文',
        # 写真の列（表記ゆれ）
        'รปู ภาพ': '写真',
        'รูปภาพ': '写真',
        # 標識の列
        'เครอื่ งหมาย': '標識',
        # その他の単語列（表記ゆれ）
        'ศพ ัท์': '単語',
        'ศพัท์': '単語',
        # Excel抽出版（日本語列名）
        '番号': '番号',
        '単語': '単語',
        '読み方（ひらがな）': '読み方（ひらがな）',
        '翻訳': '翻訳',
        '備考': '備考',
        '例文': '例文',
        '写真': '写真',
        '標識': '標識',
    },
    'ベトナム語': {
        'Số': '番号',
        'Từ vựng': '単語',
        'Dịch': '翻訳',
        'Cách đọc (Hiragana)': '読み方（ひらがな）',
        'Chú thích': '備考',
        'Ví dụ câu': '例文',
        'Ảnh': '写真',
        'Biển báo': '標識',
    },
}


def detect_language_from_filename(filename):
    """ファイル名から言語を判定"""
    if '英語' in filename:
        return '英語'
    elif 'タガログ' in filename:
        return 'タガログ語'
    elif 'カンボジア' in filename:
        return 'カンボジア語'
    elif '中国語' in filename:
        return '中国語'
    elif 'インドネシア' in filename:
        return 'インドネシア語'
    elif 'ミャンマー' in filename:
        return 'ミャンマー語'
    elif 'タイ' in filename:
        return 'タイ語'
    elif 'ベトナム' in filename:
        return 'ベトナム語'
    else:
        return None


def merge_columns(df, mapping):
    """
    同じ日本語名にマッピングされる複数の列を統合する
    """
    # 日本語列名ごとにグループ化
    japanese_to_original = {}
    for orig_col, jp_col in mapping.items():
        if jp_col not in japanese_to_original:
            japanese_to_original[jp_col] = []
        japanese_to_original[jp_col].append(orig_col)

    merged_df = pd.DataFrame()

    for jp_col, orig_cols in japanese_to_original.items():
        # 存在する列のみを取得
        existing_cols = [col for col in orig_cols if col in df.columns]

        if len(existing_cols) == 0:
            # 該当する列がない場合は空列を作成
            merged_df[jp_col] = ''
        elif len(existing_cols) == 1:
            # 1列のみの場合はそのまま使用
            merged_df[jp_col] = df[existing_cols[0]]
        else:
            # 複数列がある場合は、空でない最初の値を使用
            merged_df[jp_col] = df[existing_cols].apply(
                lambda row: next((val for val in row if pd.notna(val) and str(val).strip() != ''), ''),
                axis=1
            )

    return merged_df


def main():
    """メイン処理"""
    output_folder = Path('output')
    output_cleaned_folder = Path('output_cleaned')

    # 出力フォルダが存在しない場合は作成
    os.makedirs(output_cleaned_folder, exist_ok=True)

    # CSVファイルを取得
    csv_files = sorted(list(output_folder.glob('*.csv')))

    print(f"処理対象のCSVファイル数: {len(csv_files)}\n")

    all_dataframes = []

    for csv_file in csv_files:
        print("=" * 60)
        print(f"処理中: {csv_file.name}")
        print("=" * 60)

        # 言語を判定
        language = detect_language_from_filename(csv_file.name)
        if language is None:
            print(f"警告: 言語を判定できませんでした - {csv_file.name}")
            continue

        # 列名マッピングを取得
        mapping = COLUMN_MAPPINGS.get(language)
        if mapping is None:
            print(f"警告: マッピングが見つかりません - {language}")
            continue

        # CSVを読み込み
        df = pd.read_csv(csv_file, encoding='utf-8-sig')

        print(f"言語: {language}")
        print(f"元の行数: {len(df)}")
        print(f"元の列数: {len(df.columns)}")

        # 列を統合
        merged_df = merge_columns(df, mapping)

        # 言語列を追加
        merged_df.insert(0, '言語', language)

        # PDFページ番号と表番号を追加（存在する場合）
        if 'PDFページ番号' in df.columns:
            merged_df.insert(1, 'PDFページ番号', df['PDFページ番号'])
        if 'PDF表番号' in df.columns:
            merged_df.insert(2, 'PDF表番号', df['PDF表番号'])

        print(f"統合後の列数: {len(merged_df.columns)}")
        print(f"統合後の行数: {len(merged_df)}")
        print()

        all_dataframes.append(merged_df)

    # 全データフレームを結合
    if all_dataframes:
        print("="*60)
        print("全言語のデータを統合中...")
        print("="*60)

        final_df = pd.concat(all_dataframes, ignore_index=True)

        # 出力ファイル名
        output_file = output_cleaned_folder / '全言語統合.csv'

        # CSVファイルに保存（UTF-8 BOM）
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"\n完了!")
        print(f"  総行数: {len(final_df)}")
        print(f"  総列数: {len(final_df.columns)}")
        print(f"  出力ファイル: {output_file}")
        print()

        # 言語別の行数を表示
        print("言語別の行数:")
        lang_counts = final_df['言語'].value_counts()
        for lang, count in lang_counts.items():
            print(f"  {lang}: {count}行")

        print("="*60)
    else:
        print("エラー: 処理するファイルがありません")


if __name__ == '__main__':
    main()
