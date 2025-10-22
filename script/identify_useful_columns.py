# 各言語のCSVから必要そうな列を特定して記録するスクリプト
import pandas as pd
from pathlib import Path
import json
import sys

# UTF-8で出力
output_log = 'for_claude/columns_identification.txt'
sys.stdout = open(output_log, 'w', encoding='utf-8')

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


def analyze_column_content(df, col_name):
    """列の内容を分析"""
    # 非空値の数
    non_empty_count = df[col_name].notna().sum()
    non_empty_ratio = non_empty_count / len(df) * 100 if len(df) > 0 else 0

    # 空でない最初の5つのサンプル値
    samples = []
    for val in df[col_name]:
        if pd.notna(val) and str(val).strip() != '':
            val_str = str(val).strip()
            if len(val_str) > 100:
                val_str = val_str[:100] + "..."
            samples.append(val_str)
            if len(samples) >= 5:
                break

    return {
        "非空値数": int(non_empty_count),
        "非空値割合(%)": round(non_empty_ratio, 1),
        "サンプル値": samples
    }


def categorize_column(col_name, samples):
    """列のカテゴリを推測"""
    col_lower = col_name.lower()

    # 番号列
    if 'no.' in col_lower or 'số' in col_name or col_name == 'No.':
        return "番号"

    # PDF関連（メタデータ）
    if 'pdf' in col_lower or 'page' in col_lower or 'table' in col_lower:
        return "メタデータ"

    # Column_X（不明列）
    if col_name.startswith('Column_'):
        return "不明列"

    # サンプル値から判定
    if samples:
        sample_text = ' '.join(samples).lower()

        # 日本語の単語が多い → 単語列
        if any(c in samples[0] for c in ['技能', '工場', '安全', '機械'] if samples):
            return "単語（日本語）"

        # ひらがなが多い → 読み方列
        if any('ぎのう' in s or 'あんぜん' in s or 'こうじょう' in s for s in samples):
            return "読み方（ひらがな）"

    # 列名から判定
    if any(keyword in col_name for keyword in ['vựng', ' kata', 'Word', 'Phrase', '词汇', 'ခ', 'ศพ', 'វាក', 'Talasalitaan']):
        return "単語"

    if any(keyword in col_name for keyword in ['Dịch', 'Translation', 'jemahan', 'salin', '译', 'แปล', 'ប្រប', 'ဘာသာ']):
        return "翻訳"

    if any(keyword in col_name for keyword in ['Hiragana', 'đọc', 'Baca', '读音', 'อ่าน', 'អាន', 'ဖတ']):
        return "読み方"

    if any(keyword in col_name for keyword in ['Note', 'thích', 'tasi', '注解', 'เห็น', 'เหตุ', 'ណា', 'မှတ']):
        return "備考"

    if any(keyword in col_name for keyword in ['Example', 'dụ', 'toh', '例句', 'อย่าง', 'ហរ', 'ဥ']):
        return "例文"

    if any(keyword in col_name for keyword in ['Picture', 'Foto', 'Ảnh', 'Larawan', '照片', 'ภาพ', 'ថត']):
        return "写真"

    if any(keyword in col_name for keyword in ['Sign', 'báo', 'Tanda', 'andaan', '标识', 'หมาย', 'ញ្ញា', 'အမှတ']):
        return "標識"

    return "その他"


def main():
    """メイン処理"""
    output_folder = Path('output')

    # CSVファイルを取得
    csv_files = sorted(list(output_folder.glob('*.csv')))

    print(f"処理対象のCSVファイル数: {len(csv_files)}\n")

    # 全言語の列情報を格納する辞書
    all_columns_info = {}

    for csv_file in csv_files:
        print("=" * 80)
        print(f"処理中: {csv_file.name}")
        print("=" * 80)

        # 言語を判定
        language = detect_language_from_filename(csv_file.name)
        if language is None:
            print(f"警告: 言語を判定できませんでした - {csv_file.name}")
            continue

        # CSVを読み込み（全行）
        df = pd.read_csv(csv_file, encoding='utf-8-sig')

        # 列情報を作成
        columns_info = {
            "ファイル名": csv_file.name,
            "総行数": len(df),
            "総列数": len(df.columns),
            "列詳細": []
        }

        for idx, col_name in enumerate(df.columns):
            # 列の内容を分析
            analysis = analyze_column_content(df, col_name)

            # 列のカテゴリを推測
            category = categorize_column(col_name, analysis["サンプル値"])

            col_info = {
                "列インデックス": idx,
                "列名": col_name,
                "列名長": len(col_name),
                "カテゴリ": category,
                "非空値数": analysis["非空値数"],
                "非空値割合(%)": analysis["非空値割合(%)"],
                "サンプル値": analysis["サンプル値"][:3]  # 最初の3つのみ
            }

            columns_info["列詳細"].append(col_info)

        all_columns_info[language] = columns_info

        print(f"言語: {language}")
        print(f"行数: {len(df)}")
        print(f"列数: {len(df.columns)}")

        # 重要な列を表示
        print("\n重要な列:")
        for col_info in columns_info["列詳細"]:
            if col_info["カテゴリ"] in ["番号", "単語", "翻訳", "読み方", "単語（日本語）", "読み方（ひらがな）"]:
                print(f"  [{col_info['カテゴリ']}] {col_info['列名']} (非空値: {col_info['非空値割合(%)']}%)")
        print()

    # JSONファイルに保存
    output_json = 'columns_analysis.json'

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_columns_info, f, ensure_ascii=False, indent=2)

    print("=" * 80)
    print(f"完了!")
    print(f"出力ファイル: {output_json}")
    print("=" * 80)

    sys.stdout.close()


if __name__ == '__main__':
    main()
