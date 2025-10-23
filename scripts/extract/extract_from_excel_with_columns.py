"""Excelファイルから指定列（A, C, M）のみを抽出"""
import pandas as pd
from pathlib import Path
import sys

# ログファイル
log_file = open('for_claude/excel_acm_extraction.txt', 'w', encoding='utf-8')

print("=" * 80, file=log_file)
print("Excelファイルから指定列（A, C, J）を抽出", file=log_file)
print("=" * 80, file=log_file)
print()
print("列の指定:", file=log_file)
print("  A列（0）: No.（番号）", file=log_file)
print("  C列（2）: 日本語（単語）", file=log_file)
print("  J列（9）: 翻訳", file=log_file)
print(file=log_file)

tmp_dir = Path('tmp')
output_dir = Path('output')

# Excelファイルを取得
excel_files = sorted(list(tmp_dir.glob('*.xlsx')) + list(tmp_dir.glob('*.xls')))

print(f"処理対象: {len(excel_files)}ファイル", file=log_file)
print(file=log_file)

results = []

for excel_file in excel_files:
    print("=" * 80, file=log_file)
    print(f"処理中: {excel_file.name}", file=log_file)
    print("=" * 80, file=log_file)

    # 言語を判定
    language = None
    for lang_name in ['英語', 'タガログ語', 'カンボジア語', '中国語', 'インドネシア語', 'ミャンマー語', 'タイ語', 'ベトナム語']:
        if lang_name in excel_file.name:
            language = lang_name
            break

    if not language:
        print(f"警告: 言語を判定できませんでした - {excel_file.name}", file=log_file)
        continue

    print(f"言語: {language}", file=log_file)

    try:
        # Excelファイルを読み込み（ヘッダーなし）
        df_raw = pd.read_excel(excel_file, sheet_name='Table 1', header=None)

        print(f"元の行数: {len(df_raw)}", file=log_file)
        print(f"元の列数: {len(df_raw.columns)}", file=log_file)
        print(file=log_file)

        # ヘッダー行を検索（"No."を含む行）
        header_row_idx = None
        for idx in range(min(10, len(df_raw))):
            row = df_raw.iloc[idx]
            if 'No.' in row.values:
                header_row_idx = idx
                break

        if header_row_idx is None:
            print(f"エラー: ヘッダー行が見つかりません", file=log_file)
            continue

        print(f"ヘッダー行: 行{header_row_idx}", file=log_file)
        print(file=log_file)

        # データ行を抽出（ヘッダー行の次から）
        df_data = df_raw.iloc[header_row_idx + 1:].copy()

        # インデックスをリセット
        df_data = df_data.reset_index(drop=True)

        # 指定列のみを抽出（A列=0, C列=2, J列=9）
        # Pythonは0始まりなので: A=0, C=2, J=9
        col_a = 0   # A列（番号）
        col_c = 2   # C列（日本語）
        col_j = 9   # J列（翻訳）

        # 列が存在するか確認
        max_col_needed = max(col_a, col_c, col_j)
        if len(df_data.columns) <= max_col_needed:
            print(f"警告: 列数不足（必要: {max_col_needed+1}列、実際: {len(df_data.columns)}列）", file=log_file)
            print(file=log_file)

        # 指定列を抽出
        df_extracted = pd.DataFrame()
        df_extracted['番号'] = df_data.iloc[:, col_a] if col_a < len(df_data.columns) else ''
        df_extracted['単語'] = df_data.iloc[:, col_c] if col_c < len(df_data.columns) else ''
        df_extracted['翻訳'] = df_data.iloc[:, col_j] if col_j < len(df_data.columns) else ''

        # NaNを空文字列に置換
        df_extracted = df_extracted.fillna('')

        # 番号が空の行を除外
        df_extracted = df_extracted[df_extracted['番号'] != '']

        # 番号を数値型に変換できる行のみを残す
        def is_valid_number(val):
            try:
                float(str(val))
                return True
            except:
                return False

        df_extracted = df_extracted[df_extracted['番号'].apply(is_valid_number)]

        # インデックスをリセット
        df_extracted = df_extracted.reset_index(drop=True)

        print(f"抽出後の行数: {len(df_extracted)}", file=log_file)
        print(file=log_file)

        # 翻訳列のデータ状況を確認
        translation_filled = (df_extracted['翻訳'] != '').sum()
        translation_empty = (df_extracted['翻訳'] == '').sum()
        total = len(df_extracted)

        print(f"翻訳データ状況:", file=log_file)
        print(f"  データあり: {translation_filled}行 ({translation_filled/total*100:.1f}%)", file=log_file)
        print(f"  空欄: {translation_empty}行 ({translation_empty/total*100:.1f}%)", file=log_file)
        print(file=log_file)

        # サンプルデータ
        print("サンプルデータ（最初の5行）:", file=log_file)
        print(df_extracted.head(5).to_string(index=False), file=log_file)
        print(file=log_file)

        # CSVに保存
        output_file = output_dir / f"【全課統合版】{language}_げんばのことば_建設関連職種_excel_acm.csv"
        df_extracted.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"保存完了: {output_file.name}", file=log_file)
        print(file=log_file)

        results.append({
            'language': language,
            'rows': len(df_extracted),
            'translation_filled': translation_filled,
            'translation_rate': f"{translation_filled/total*100:.1f}%",
            'file': output_file.name
        })

        # コンソール出力
        print(f"{language}: {len(df_extracted)}行抽出、翻訳充足率 {translation_filled/total*100:.1f}%")

    except Exception as e:
        print(f"エラー: {e}", file=log_file)
        import traceback
        traceback.print_exc(file=log_file)
        print(f"エラー: {excel_file.name} - {e}")
        continue

print(file=log_file)
print("=" * 80, file=log_file)
print("【抽出結果サマリー】", file=log_file)
print("=" * 80, file=log_file)

for result in results:
    print(f"{result['language']}: {result['rows']}行、翻訳充足率 {result['translation_rate']} → {result['file']}", file=log_file)

print(file=log_file)
print(f"総計: {len(results)}言語を抽出", file=log_file)
print("=" * 80, file=log_file)

log_file.close()

print(f"\n全体完了: {len(results)}言語を抽出")
print("詳細: for_claude/excel_acm_extraction.txt")
