# PDFから抽出したCSVの全ヘッダー情報をJSON化するスクリプト
import pandas as pd
from pathlib import Path
import json

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


def main():
    """メイン処理"""
    output_folder = Path('output')

    # CSVファイルを取得
    csv_files = sorted(list(output_folder.glob('*.csv')))

    print(f"処理対象のCSVファイル数: {len(csv_files)}\n")

    # 全言語のヘッダー情報を格納する辞書
    all_headers = {}

    for csv_file in csv_files:
        print("=" * 60)
        print(f"処理中: {csv_file.name}")
        print("=" * 60)

        # 言語を判定
        language = detect_language_from_filename(csv_file.name)
        if language is None:
            print(f"警告: 言語を判定できませんでした - {csv_file.name}")
            continue

        # CSVを読み込み（ヘッダーのみ）
        df = pd.read_csv(csv_file, encoding='utf-8-sig', nrows=0)

        # 列インデックスと列名のマッピングを作成
        headers_info = {
            "ファイル名": csv_file.name,
            "総列数": len(df.columns),
            "列マッピング": {}
        }

        for idx, col_name in enumerate(df.columns):
            headers_info["列マッピング"][idx] = {
                "列インデックス": idx,
                "列名": col_name,
                "列名長": len(col_name),
                "列名バイト(UTF-8)": col_name.encode('utf-8').hex()
            }

        all_headers[language] = headers_info

        print(f"言語: {language}")
        print(f"列数: {len(df.columns)}")
        print()

    # JSONファイルに保存
    output_json = 'headers_mapping.json'

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_headers, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print(f"完了!")
    print(f"出力ファイル: {output_json}")
    print("=" * 60)

    # サマリー表示
    print("\nサマリー:")
    for lang, info in all_headers.items():
        print(f"  {lang}: {info['総列数']}列")


if __name__ == '__main__':
    main()
