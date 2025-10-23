"""
プロジェクトログの保存
"""
import os
from datetime import datetime

project_root = r'C:\python_script\test_space\MitsubishiMultipleTranslation'
for_claude_dir = os.path.join(project_root, 'for_claude')

# ログ内容作成
log_content = []
log_content.append("=" * 80)
log_content.append("プロジェクトログ - セッション終了時保存")
log_content.append("=" * 80)
log_content.append(f"保存日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log_content.append("")

log_content.append("=" * 80)
log_content.append("最終作業内容")
log_content.append("=" * 80)
log_content.append("")

log_content.append("【完了した作業】")
log_content.append("")
log_content.append("1. Excelヘッダー追加")
log_content.append("   - ファイル: 成果物_20251023/02_逆翻訳_検証結果.xlsx")
log_content.append("   - inputシート: ja, en, fil-PH, zh, th, vi, my, id, km（青色ヘッダー）")
log_content.append("   - outputシート: ja, en, fil-PH, zh, th, vi, my, id, km（緑色ヘッダー）")
log_content.append("   - スクリプト: scripts/create_excel_with_headers.py")
log_content.append("")

log_content.append("2. README.txt にコスト情報追加")
log_content.append("   - Claude Code Max $100プラン: 約15,223円/月")
log_content.append("   - Google Translation API: 約3,045円/100万文字")
log_content.append("   - 本プロジェクト推定コスト: 約304-609円")
log_content.append("   - 為替レート: 1 USD = 152.23 JPY (2025/10/23)")
log_content.append("")

log_content.append("=" * 80)
log_content.append("成果物一覧")
log_content.append("=" * 80)
log_content.append("")

log_content.append("【成果物フォルダ: 成果物_20251023】")
log_content.append("")
log_content.append("1. 00_README.txt")
log_content.append("   - プロジェクト全体の説明")
log_content.append("   - ファイル構成、データ仕様、既知の問題")
log_content.append("   - インポート手順、品質確認手順")
log_content.append("   - 技術情報、コスト情報")
log_content.append("")

log_content.append("2. 01_全言語統合_テンプレート_インポート用.csv")
log_content.append("   - 524行 x 38列")
log_content.append("   - 列: ja, en, fil-PH, pt, es, pt-BR, zh, ko, fr, hi, th, vi, my, ne,")
log_content.append("         bn, id, ta, si, mn, ar, fa, tr, ru, ur, km, lo, ms, de, hu, cs,")
log_content.append("         pl, nl, da, fi, sv, lb, af, fr-CA")
log_content.append("   - UTF-8 BOM エンコーディング")
log_content.append("   - ヘッダーあり")
log_content.append("   - システムインポート用")
log_content.append("")

log_content.append("3. 02_逆翻訳_検証結果.xlsx")
log_content.append("   - inputシート: 元の翻訳データ（524行 x 9列、ヘッダーあり）")
log_content.append("   - outputシート: 日本語逆翻訳データ（524行 x 9列、ヘッダーあり）")
log_content.append("   - 列: ja, en, fil-PH, zh, th, vi, my, id, km")
log_content.append("   - 翻訳品質検証用")
log_content.append("")

log_content.append("4. ドキュメント_逆翻訳分析.txt")
log_content.append("   - 逆翻訳処理の詳細分析")
log_content.append("   - CIDコード問題の調査結果")
log_content.append("")

log_content.append("5. ドキュメント_CID確認.txt")
log_content.append("   - 入力CSV内のCIDコード検出結果（57件）")
log_content.append("")

log_content.append("6. ドキュメント_プロジェクトログ.txt")
log_content.append("   - プロジェクト全体のログ")
log_content.append("")

log_content.append("=" * 80)
log_content.append("core_filesフォルダ")
log_content.append("=" * 80)
log_content.append("")

log_content.append("【core_files/output_csv_template_utf8bom.csv】")
log_content.append("   - 524行 x 39列（翻訳言語数列を含む完全版）")
log_content.append("   - UTF-8 BOM エンコーディング")
log_content.append("")

log_content.append("=" * 80)
log_content.append("スクリプト整理（次回実施予定）")
log_content.append("=" * 80)
log_content.append("")

log_content.append("【scripts フォルダ】")
log_content.append("   - 現在: 106個のスクリプトファイル")
log_content.append("   - 整理予定:")
log_content.append("     * scripts_main/: メイン処理スクリプト")
log_content.append("     * scripts/analysis/: 分析系スクリプト")
log_content.append("     * scripts/check/: チェック系スクリプト")
log_content.append("     * scripts/debug/: デバッグ系スクリプト")
log_content.append("     * scripts/test/: テスト系スクリプト")
log_content.append("     * scripts/extract/: PDF抽出系スクリプト")
log_content.append("     * scripts/merge/: マージ系スクリプト")
log_content.append("     * scripts/archive_old/: 古いバージョン")
log_content.append("")

log_content.append("=" * 80)
log_content.append("主要スクリプト一覧")
log_content.append("=" * 80)
log_content.append("")

log_content.append("【メイン処理スクリプト】")
log_content.append("   1. create_unified_csv.py - 8言語CSVの統合")
log_content.append("   2. create_template_format_csv.py - テンプレート形式への変換")
log_content.append("   3. reorder_template_by_vietnamese.py - ベトナム語順での並び替え")
log_content.append("   4. create_template_only.py - 9列のみ抽出")
log_content.append("   5. reverse_translate_to_japanese.py - Google API逆翻訳")
log_content.append("   6. create_excel_with_headers.py - ヘッダー付きExcel作成")
log_content.append("   7. create_core_file_v2.py - core_files用CSV作成")
log_content.append("   8. create_import_csv_38cols.py - 38列インポート用CSV作成")
log_content.append("   9. create_deliverables.py - 成果物フォルダ作成")
log_content.append("  10. optimize_for_claude.py - ファイル最適化")
log_content.append("")

log_content.append("=" * 80)
log_content.append("技術仕様")
log_content.append("=" * 80)
log_content.append("")

log_content.append("【データ仕様】")
log_content.append("   - 総単語数: 524語")
log_content.append("   - ベトナム語固有: 12語")
log_content.append("   - 共通語: 512語")
log_content.append("   - 翻訳カバレッジ: 95.66%")
log_content.append("")

log_content.append("【エンコーディング】")
log_content.append("   - CSV: UTF-8 BOM")
log_content.append("   - Excel: UTF-8")
log_content.append("")

log_content.append("【並び順】")
log_content.append("   - ベトナム語の順序に基づく")
log_content.append("   - ベトナム語512語 → 他言語固有12語")
log_content.append("")

log_content.append("【既知の問題】")
log_content.append("   - CIDコード: 57件（英語21、タイ語14、カンボジア語22）")
log_content.append("   - 原因: PDF抽出時のpdfplumberの制限")
log_content.append("   - 影響: 翻訳品質には影響なし")
log_content.append("")

log_content.append("=" * 80)
log_content.append("次回セッションへの引継ぎ")
log_content.append("=" * 80)
log_content.append("")

log_content.append("【完了事項】")
log_content.append("   ✓ 8言語のPDF抽出")
log_content.append("   ✓ データ統合・ピボット変換")
log_content.append("   ✓ ベトナム語順での並び替え")
log_content.append("   ✓ インポート用CSV作成（38列）")
log_content.append("   ✓ Google API逆翻訳実行")
log_content.append("   ✓ Excel比較ファイル作成（ヘッダーあり）")
log_content.append("   ✓ 成果物フォルダ作成")
log_content.append("   ✓ ドキュメント作成")
log_content.append("   ✓ コスト情報追加")
log_content.append("")

log_content.append("【次回タスク】")
log_content.append("   - scriptsフォルダの整理整頓")
log_content.append("     * scripts_main フォルダ作成")
log_content.append("     * カテゴリ別フォルダ作成（analysis, check, debug, test, extract, merge）")
log_content.append("     * 各スクリプトを適切なフォルダに移動")
log_content.append("   - 必要に応じてさらなる品質確認")
log_content.append("")

log_content.append("=" * 80)
log_content.append("ログ保存完了")
log_content.append("=" * 80)
log_content.append("")

# ファイル保存
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = os.path.join(for_claude_dir, f'log_session_{timestamp}.txt')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_content))

print(f"ログ保存完了: {output_file}")
print()
print(f"ファイルサイズ: {os.path.getsize(output_file) / 1024:.2f} KB")
