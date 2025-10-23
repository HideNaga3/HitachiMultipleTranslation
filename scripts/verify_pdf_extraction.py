"""
建設関連PDF抽出データの検証スクリプト
翻訳前の日本語列を比較し、各PDFの行数と値を検証する
"""
import pandas as pd
from datetime import datetime
import os

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
log_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

# 8言語のCSVファイル
language_files = {
    '英語': '英語_pdfplumber_抽出_最終版.csv',
    'タガログ語': 'タガログ語_pdfplumber_抽出_最終版.csv',
    'カンボジア語': 'カンボジア語_pdfplumber_抽出_最終版.csv',
    '中国語': '中国語_pdfplumber_抽出_最終版.csv',
    'インドネシア語': 'インドネシア語_pdfplumber_抽出_最終版.csv',
    'ミャンマー語': 'ミャンマー語_pdfplumber_抽出_最終版.csv',
    'タイ語': 'タイ語_pdfplumber_抽出_最終版.csv',
    'ベトナム語': 'ベトナム語_pdfplumber_抽出_最終版.csv',
}

# ログファイル
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(log_dir, f'pdf_extraction_verification_{timestamp}.txt')

def write_log(message, print_console=True):
    """ログファイルとコンソールに出力"""
    if print_console:
        print(message)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def main():
    write_log("=" * 80)
    write_log("建設関連PDF抽出データ検証")
    write_log("=" * 80)
    write_log(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    write_log("")

    # 各言語のデータを読み込み
    language_data = {}

    write_log("-" * 80)
    write_log("1. 各言語CSVファイルの読み込み")
    write_log("-" * 80)
    write_log("")

    for lang_name, file_name in language_files.items():
        file_path = os.path.join(output_dir, file_name)
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            language_data[lang_name] = df
            write_log(f"[OK] {lang_name}: {len(df)}行, {len(df.columns)}列")
            write_log(f"     列名: {', '.join(df.columns.tolist())}")
        except Exception as e:
            write_log(f"[ERROR] {lang_name}: 読み込み失敗 - {e}")

    write_log("")

    # 行数比較
    write_log("-" * 80)
    write_log("2. 各言語の行数比較")
    write_log("-" * 80)
    write_log("")

    row_counts = {lang: len(df) for lang, df in language_data.items()}
    max_rows = max(row_counts.values())
    min_rows = min(row_counts.values())

    write_log(f"最大行数: {max_rows}行")
    write_log(f"最小行数: {min_rows}行")
    write_log(f"行数差: {max_rows - min_rows}行")
    write_log("")

    write_log("言語別行数:")
    for lang, count in sorted(row_counts.items(), key=lambda x: x[1], reverse=True):
        diff = count - min_rows
        diff_str = f"(+{diff})" if diff > 0 else ""
        write_log(f"  {lang:15s}: {count:4d}行 {diff_str}")

    write_log("")

    # 日本語の「単語」列の存在確認
    write_log("-" * 80)
    write_log("3. 日本語「単語」列の確認")
    write_log("-" * 80)
    write_log("")

    # 列構成を確認（言語、Page、番号、単語、翻訳）
    word_column = '単語'

    for lang_name, df in language_data.items():
        if word_column in df.columns:
            non_null_count = df[word_column].notna().sum()
            null_count = df[word_column].isna().sum()
            null_rate = (null_count / len(df)) * 100 if len(df) > 0 else 0
            write_log(f"[OK] {lang_name:15s}: 「{word_column}」列あり")
            write_log(f"     データあり: {non_null_count}行, 空欄: {null_count}行 ({null_rate:.1f}%)")
        else:
            write_log(f"[NG] {lang_name:15s}: 「{word_column}」列なし")
            write_log(f"     利用可能な列: {', '.join(df.columns.tolist())}")

    write_log("")

    # 日本語の単語データを抽出して比較
    write_log("-" * 80)
    write_log("4. 日本語「単語」データの一致性確認")
    write_log("-" * 80)
    write_log("")

    # 基準となる言語（最も行数が少ない言語）
    base_lang = min(row_counts.items(), key=lambda x: x[1])[0]
    base_df = language_data[base_lang]

    write_log(f"基準言語: {base_lang} ({len(base_df)}行)")
    write_log("")

    # 各言語の日本語「単語」列を比較
    word_comparison = {}

    for lang_name, df in language_data.items():
        if word_column in df.columns:
            word_comparison[lang_name] = df[word_column].tolist()

    # 最初のN行のサンプルデータを確認
    write_log("各言語の最初の10行の日本語「単語」サンプル:")
    write_log("")

    sample_size = min(10, min_rows)

    for i in range(sample_size):
        write_log(f"行 {i+1}:")
        for lang_name in sorted(word_comparison.keys()):
            if i < len(word_comparison[lang_name]):
                word = word_comparison[lang_name][i]
                word_str = str(word) if pd.notna(word) else "[空欄]"
                write_log(f"  {lang_name:15s}: {word_str}")
        write_log("")

    # 不一致の検出
    write_log("-" * 80)
    write_log("5. 言語間の日本語「単語」不一致検出")
    write_log("-" * 80)
    write_log("")

    mismatches = []

    # 行数が最小の範囲で比較
    for i in range(min_rows):
        words_at_row = {}
        for lang_name, words in word_comparison.items():
            if i < len(words):
                words_at_row[lang_name] = words[i]

        # 全ての言語で値が一致しているか確認
        unique_words = set()
        for word in words_at_row.values():
            if pd.notna(word):
                unique_words.add(str(word))

        if len(unique_words) > 1:
            mismatches.append({
                'row': i + 1,
                'words': words_at_row,
                'unique_count': len(unique_words)
            })

    if mismatches:
        write_log(f"[警告] 不一致が検出されました: {len(mismatches)}箇所")
        write_log("")
        write_log(f"最初の{min(10, len(mismatches))}件の不一致:")
        for mismatch in mismatches[:10]:
            write_log(f"  行 {mismatch['row']}:")
            for lang, word in mismatch['words'].items():
                word_str = str(word) if pd.notna(word) else "[空欄]"
                write_log(f"    {lang:15s}: {word_str}")
            write_log("")
    else:
        write_log("[OK] 全ての言語で日本語「単語」が一致しています")

    write_log("")

    # 統計サマリー
    write_log("-" * 80)
    write_log("6. 統計サマリー")
    write_log("-" * 80)
    write_log("")

    total_rows = sum(row_counts.values())
    avg_rows = total_rows / len(row_counts)

    write_log(f"総行数: {total_rows}行")
    write_log(f"平均行数: {avg_rows:.1f}行")
    write_log(f"言語数: {len(language_data)}言語")
    write_log(f"不一致箇所: {len(mismatches)}箇所 ({len(mismatches)/min_rows*100:.1f}%)")
    write_log("")

    # 完了メッセージ
    write_log("=" * 80)
    write_log("検証完了")
    write_log("=" * 80)
    write_log(f"ログファイル: {log_file}")
    write_log("")

if __name__ == "__main__":
    main()
