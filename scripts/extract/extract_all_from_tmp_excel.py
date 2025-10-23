"""tmpフォルダ内の全Excelファイルからデータを抽出（タイ語の処理を応用）"""
import pandas as pd
from pathlib import Path
import sys

# ログファイル
log_file = open('for_claude/tmp_excel_extraction.txt', 'w', encoding='utf-8')

print("=" * 80, file=log_file)
print("tmpフォルダ内の全Excelファイルからのデータ抽出", file=log_file)
print("=" * 80, file=log_file)
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
        for idx in range(min(10, len(df_raw))):  # 最初の10行を探索
            row = df_raw.iloc[idx]
            if 'No.' in row.values:
                header_row_idx = idx
                break

        if header_row_idx is None:
            print(f"エラー: ヘッダー行が見つかりません", file=log_file)
            continue

        print(f"ヘッダー行: 行{header_row_idx}", file=log_file)
        header_row = df_raw.iloc[header_row_idx]
        print(f"ヘッダー: {list(header_row[:10])}", file=log_file)
        print(file=log_file)

        # データ行を抽出（ヘッダー行の次から）
        df_data = df_raw.iloc[header_row_idx + 1:].copy()

        # ヘッダーを設定
        df_data.columns = header_row

        # インデックスをリセット
        df_data = df_data.reset_index(drop=True)

        # NaNを空文字列に置換
        df_data = df_data.fillna('')

        # 番号列が空の行を除外
        if 'No.' in df_data.columns:
            df_data = df_data[df_data['No.'] != '']

        # 番号を数値型に変換できる行のみを残す
        def is_valid_number(val):
            try:
                float(str(val))
                return True
            except:
                return False

        if 'No.' in df_data.columns:
            df_data = df_data[df_data['No.'].apply(is_valid_number)]

        # インデックスをリセット
        df_data = df_data.reset_index(drop=True)

        print(f"抽出後の行数: {len(df_data)}", file=log_file)
        print(file=log_file)

        # 翻訳列を検出
        translation_cols = []
        for col in df_data.columns:
            col_str = str(col).lower()
            # 各言語の翻訳列パターン
            if any(keyword in col_str for keyword in ['pagsasalin', 'translation', 'dịch', 'terjemahan', '中文词意', 'ค าแปล', 'คำแปล']):
                translation_cols.append(col)

        if translation_cols:
            print(f"翻訳列の候補: {translation_cols}", file=log_file)
            # 翻訳データ状況を確認
            for col in translation_cols:
                filled = (df_data[col] != '').sum()
                total = len(df_data)
                print(f"  '{col}': {filled}行 ({filled/total*100:.1f}%)", file=log_file)
        else:
            print("警告: 翻訳列が見つかりません", file=log_file)

        print(file=log_file)

        # サンプルデータ
        print("サンプルデータ（最初の3行）:", file=log_file)
        sample_cols = [col for col in df_data.columns if col][:8]  # 最初の8列
        print(df_data[sample_cols].head(3).to_string(index=False), file=log_file)
        print(file=log_file)

        # CSVに保存
        output_file = output_dir / f"【全課統合版】{language}_げんばのことば_建設関連職種_from_tmp_excel.csv"
        df_data.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"保存完了: {output_file.name}", file=log_file)
        print(f"  行数: {len(df_data)}", file=log_file)
        print(f"  列数: {len(df_data.columns)}", file=log_file)
        print(file=log_file)

        results.append({
            'language': language,
            'rows': len(df_data),
            'cols': len(df_data.columns),
            'file': output_file.name
        })

        # コンソール出力
        print(f"{language}: {len(df_data)}行抽出完了")

    except Exception as e:
        print(f"エラー: {e}", file=log_file)
        print(f"エラー: {excel_file.name} - {e}")
        continue

print(file=log_file)
print("=" * 80, file=log_file)
print("【抽出結果サマリー】", file=log_file)
print("=" * 80, file=log_file)

for result in results:
    print(f"{result['language']}: {result['rows']}行、{result['cols']}列 → {result['file']}", file=log_file)

print(file=log_file)
print(f"総計: {len(results)}言語を抽出", file=log_file)
print("=" * 80, file=log_file)

log_file.close()

print(f"\n全体完了: {len(results)}言語を抽出")
print("詳細: for_claude/tmp_excel_extraction.txt")
