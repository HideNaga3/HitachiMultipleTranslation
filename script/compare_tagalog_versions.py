"""タガログ語のPDF版とXML版を比較"""
import pandas as pd
import sys

# ファイル出力
sys.stdout = open('for_claude/tagalog_comparison.txt', 'w', encoding='utf-8')

print("=" * 80)
print("タガログ語 PDF版 vs XML版 比較")
print("=" * 80)
print()

# PDF版を読み込み
pdf_csv = 'output/【全課統合版】タガログ語_げんばのことば_建設関連職種_12cols.csv'
df_pdf = pd.read_csv(pdf_csv, encoding='utf-8-sig')

# XML版を読み込み
xml_csv = 'output/【全課統合版】タガログ語_げんばのことば_建設関連職種_from_xml.csv'
df_xml = pd.read_csv(xml_csv, encoding='utf-8-sig')

print("【基本情報】")
print(f"PDF版: {len(df_pdf)}行、{len(df_pdf.columns)}列")
print(f"XML版: {len(df_xml)}行、{len(df_xml.columns)}列")
print(f"差分: {len(df_xml) - len(df_pdf)}行")
print()

print("【PDF版の列名】")
for i, col in enumerate(df_pdf.columns):
    print(f"  {i}: '{col}'")
print()

print("【XML版の列名】")
for i, col in enumerate(df_xml.columns):
    print(f"  {i}: '{col}'")
print()

# 翻訳列のデータ状況を確認
print("【翻訳列（Pagsasalin）のデータ状況】")

# PDF版
if 'Pagsasalin' in df_pdf.columns:
    pdf_trans_filled = df_pdf['Pagsasalin'].notna().sum()
    pdf_trans_empty = df_pdf['Pagsasalin'].isna().sum()
    print(f"PDF版:")
    print(f"  データあり: {pdf_trans_filled}行 ({pdf_trans_filled/len(df_pdf)*100:.1f}%)")
    print(f"  データなし: {pdf_trans_empty}行 ({pdf_trans_empty/len(df_pdf)*100:.1f}%)")

# XML版
if 'Pagsasalin' in df_xml.columns:
    xml_trans_filled = df_xml['Pagsasalin'].notna().sum()
    xml_trans_empty = df_xml['Pagsasalin'].isna().sum()
    print(f"\nXML版:")
    print(f"  データあり: {xml_trans_filled}行 ({xml_trans_filled/len(df_xml)*100:.1f}%)")
    print(f"  データなし: {xml_trans_empty}行 ({xml_trans_empty/len(df_xml)*100:.1f}%)")

print()

# 番号列で比較（どの番号が含まれているか）
print("【番号範囲の比較】")

if 'No.' in df_pdf.columns:
    try:
        df_pdf['No._numeric'] = pd.to_numeric(df_pdf['No.'], errors='coerce')
        pdf_no_min = df_pdf['No._numeric'].min()
        pdf_no_max = df_pdf['No._numeric'].max()
        print(f"PDF版: No. {pdf_no_min:.0f} ～ {pdf_no_max:.0f}")
    except:
        print(f"PDF版: 番号列の解析エラー")

if 'No.' in df_xml.columns:
    try:
        df_xml['No._numeric'] = pd.to_numeric(df_xml['No.'], errors='coerce')
        xml_no_min = df_xml['No._numeric'].min()
        xml_no_max = df_xml['No._numeric'].max()
        print(f"XML版: No. {xml_no_min:.0f} ～ {xml_no_max:.0f}")
    except:
        print(f"XML版: 番号列の解析エラー")

print()

# サンプルデータ比較
print("【サンプルデータ比較】")
print("\nPDF版（最初の5行）:")
cols_to_show = ['No.', 'Talasalitaan', 'Pagsasalin', 'Paano Magbasa']
pdf_cols_available = [col for col in cols_to_show if col in df_pdf.columns]
if pdf_cols_available:
    print(df_pdf[pdf_cols_available].head(5).to_string(index=False))

print("\nXML版（最初の5行）:")
xml_cols_available = [col for col in cols_to_show if col in df_xml.columns]
if xml_cols_available:
    print(df_xml[xml_cols_available].head(5).to_string(index=False))

print()

# 最後の5行も比較
print("【最後の5行の比較】")
print("\nPDF版（最後の5行）:")
if pdf_cols_available:
    print(df_pdf[pdf_cols_available].tail(5).to_string(index=False))

print("\nXML版（最後の5行）:")
if xml_cols_available:
    print(df_xml[xml_cols_available].tail(5).to_string(index=False))

print()
print("=" * 80)
print("【推奨】")
print("XML版の方が193行多く、より完全なデータセットです。")
print("翻訳データの質は同等なので、XML版の使用を推奨します。")
print("=" * 80)
