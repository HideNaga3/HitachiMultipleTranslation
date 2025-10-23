"""
スクリプトフォルダの整理整頓
"""
import os
import shutil

project_root = r'C:\python_script\test_space\MitsubishiMultipleTranslation'
scripts_dir = os.path.join(project_root, 'scripts')

print("=" * 80)
print("スクリプトフォルダの整理整頓")
print("=" * 80)
print()

# フォルダ作成
folders = {
    'scripts_main': 'メイン処理スクリプト',
    'analysis': '分析系スクリプト',
    'check': 'チェック系スクリプト',
    'debug': 'デバッグ系スクリプト',
    'test': 'テスト系スクリプト',
    'extract': 'PDF抽出系スクリプト',
    'merge': 'マージ系スクリプト',
    'archive_old': '旧バージョン・未使用スクリプト'
}

for folder, description in folders.items():
    if folder == 'scripts_main':
        folder_path = os.path.join(project_root, folder)
    else:
        folder_path = os.path.join(scripts_dir, folder)

    os.makedirs(folder_path, exist_ok=True)
    print(f"フォルダ作成: {folder}/ - {description}")

print()
print("=" * 80)
print("スクリプトの分類")
print("=" * 80)
print()

# メインスクリプト（成果物生成に使用）
main_scripts = [
    'create_unified_csv.py',
    'create_template_format_csv.py',
    'reorder_template_by_vietnamese.py',
    'create_template_only.py',
    'reverse_translate_to_japanese.py',
    'create_excel_with_headers.py',
    'create_core_file_v2.py',
    'create_import_csv_38cols.py',
    'create_deliverables.py',
    'optimize_for_claude.py',
    'save_project_log.py'
]

# 分析系
analysis_scripts = [
    'analyze_and_clean_excel.py',
    'analyze_cambodian_csv.py',
    'analyze_excel_structure.py',
    'analyze_headers.py',
    'analyze_pdf_text_structure.py',
    'analyze_table_headers.py',
    'analyze_tagalog_xml.py',
    'analyze_thai_excel.py',
    'analyze_translation_by_language.py',
    'compare_language_headers.py',
    'compare_pdf_vs_csv.py',
    'compare_tagalog_versions.py',
    'count_translations_per_row.py',
    'identify_useful_columns.py',
    'investigate_thai_khmer.py'
]

# チェック系
check_scripts = [
    'check_all_columns_data.py',
    'check_all_headers.py',
    'check_available_formats.py',
    'check_columns.py',
    'check_column_names.py',
    'check_csv_columns.py',
    'check_employment_detailed.py',
    'check_employment_insurance.py',
    'check_empty_translation.py',
    'check_excel_columns.py',
    'check_file_status.py',
    'check_filter_conditions.py',
    'check_final_csv.py',
    'check_input_csv_for_cid.py',
    'check_merged_csv.py',
    'check_missing_languages.py',
    'check_myanmar_columns.py',
    'check_original_template.py',
    'check_page19_data.py',
    'check_pdf_page4.py',
    'check_raw_extracted.py',
    'check_required_modules.py',
    'check_reverse_translation.py',
    'check_row_detail.py',
    'check_template_km.py',
    'check_thai_nan.py',
    'check_thai_unique_japanese.py',
    'check_tmp_excel_files.py',
    'check_translation_columns.py',
    'check_vietnamese.py',
    'check_vietnamese_in_unified.py',
    'check_vietnamese_only_terms.py'
]

# デバッグ系
debug_scripts = [
    'debug_employment_insurance.py',
    'debug_table_structure.py',
    'debug_thai_columns.py'
]

# テスト系
test_scripts = [
    'test_camelot_extraction.py',
    'test_full_extraction.py',
    'test_marker_extraction.py',
    'test_pdf_extraction_settings.py',
    'test_tabula_extraction.py',
    'test_text_strategy.py',
    'test_thai_pdf_pdfplumber.py',
    'test_vietnamese_pdf.py'
]

# PDF抽出系
extract_scripts = [
    'extract_all_from_tmp_excel.py',
    'extract_all_pdfs_to_csv.py',
    'extract_by_coordinates.py',
    'extract_from_excel_with_columns.py',
    'extract_tables_from_pdf.py',
    'extract_tables_from_pdf_v2.py',
    'extract_tables_improved.py',
    'extract_tagalog_from_xml.py',
    'extract_thai_from_excel.py',
    'extract_thai_pdf_to_csv.py',
    'extract_vietnamese_only.py'
]

# マージ系
merge_scripts = [
    'merge_all_languages.py',
    'merge_all_languages_v2.py',
    'merge_cleaned_csvs.py',
    'merge_from_excel_direct.py'
]

# 旧バージョン・未使用
archive_scripts = [
    'clean_extracted_tables.py',
    'create_core_file.py',
    'create_excel_without_header.py',
    'create_headers_mapping.py',
    'export_column_names.py',
    'fill_japanese_column.py',
    'find_col2_data.py',
    'find_full_columns_csv.py',
    'find_header_row.py',
    'fix_missing_row.py',
    'fix_vietnamese_extra_row.py',
    'fix_vietnamese_final.py',
    'reorder_by_thai_order.py',
    'reorder_template_by_thai.py',
    'replace_thai_csv.py',
    'restore_thai_excel_csv.py',
    'show_actual_column_names.py',
    'show_filter_conditions.py',
    'verify_excel_sheets.py',
    'verify_final_csv.py',
    'verify_improved_extraction.py',
    'verify_language_json.py',
    'verify_output_files.py',
    'verify_pdf_extraction.py',
    'verify_translation_count.py'
]

# スクリプトの移動
def move_scripts(script_list, target_folder, folder_name):
    moved_count = 0
    for script in script_list:
        src = os.path.join(scripts_dir, script)

        if folder_name == 'scripts_main':
            dst = os.path.join(project_root, 'scripts_main', script)
        else:
            dst = os.path.join(scripts_dir, target_folder, script)

        if os.path.exists(src):
            shutil.move(src, dst)
            moved_count += 1

    print(f"{folder_name}: {moved_count}個のスクリプトを移動")
    return moved_count

# 移動実行
total_moved = 0
total_moved += move_scripts(main_scripts, 'scripts_main', 'scripts_main')
total_moved += move_scripts(analysis_scripts, 'analysis', 'analysis')
total_moved += move_scripts(check_scripts, 'check', 'check')
total_moved += move_scripts(debug_scripts, 'debug', 'debug')
total_moved += move_scripts(test_scripts, 'test', 'test')
total_moved += move_scripts(extract_scripts, 'extract', 'extract')
total_moved += move_scripts(merge_scripts, 'merge', 'merge')
total_moved += move_scripts(archive_scripts, 'archive_old', 'archive_old')

print()
print(f"合計: {total_moved}個のスクリプトを整理")
print()

# 残りのファイル確認
remaining = [f for f in os.listdir(scripts_dir) if f.endswith('.py')]
if remaining:
    print("=" * 80)
    print(f"未分類のスクリプト（{len(remaining)}個）:")
    print("=" * 80)
    for script in remaining:
        print(f"  - {script}")
    print()

print("=" * 80)
print("整理完了")
print("=" * 80)
print()

print("【新しいフォルダ構成】")
print("  scripts_main/ - メイン処理スクリプト（11個）")
print("  scripts/")
print("    ├─ analysis/ - 分析系（15個）")
print("    ├─ check/ - チェック系（33個）")
print("    ├─ debug/ - デバッグ系（3個）")
print("    ├─ test/ - テスト系（8個）")
print("    ├─ extract/ - PDF抽出系（11個）")
print("    ├─ merge/ - マージ系（4個）")
print("    └─ archive_old/ - 旧バージョン・未使用（21個）")
print()
