"""
Claude Code用のファイル最適化
"""
import os
import shutil
from datetime import datetime
import glob

project_root = r'C:\python_script\test_space\MitsubishiMultipleTranslation'
for_claude_dir = os.path.join(project_root, 'for_claude')
output_dir = os.path.join(project_root, 'output')

output_lines = []
output_lines.append("=" * 80)
output_lines.append("Claude Code用ファイル最適化")
output_lines.append("=" * 80)
output_lines.append(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
output_lines.append("")

print("最適化処理を実行中...")

# for_claudeディレクトリの整理
output_lines.append("[1] for_claudeディレクトリの整理")
output_lines.append("-" * 80)

important_files = [
    'reverse_translation_analysis.txt',
    'input_csv_cid_check.txt',
    'reverse_translation_check.txt',
    'reverse_translation_summary.txt',
]

for_claude_files = [f for f in os.listdir(for_claude_dir) if os.path.isfile(os.path.join(for_claude_dir, f))]
output_lines.append(f"現在のファイル数: {len(for_claude_files)}件")

old_logs = [f for f in for_claude_files if f not in important_files and f.endswith('.txt') and f != 'optimization_report.txt']

if old_logs:
    archive_dir = os.path.join(for_claude_dir, 'archive')
    os.makedirs(archive_dir, exist_ok=True)

    moved_count = 0
    for log in old_logs:
        src = os.path.join(for_claude_dir, log)
        dst = os.path.join(archive_dir, log)
        try:
            if os.path.exists(src):
                shutil.move(src, dst)
                moved_count += 1
        except:
            pass

    output_lines.append(f"アーカイブ: {moved_count}件のログファイル")
else:
    output_lines.append("アーカイブ対象なし")

output_lines.append("")

# outputディレクトリの整理
output_lines.append("[2] outputディレクトリの整理")
output_lines.append("-" * 80)

final_outputs = [
    '全言語統合_テンプレート_インポート用.csv',
    '逆翻訳_検証結果.xlsx',
]

output_files = glob.glob(os.path.join(output_dir, '*.csv'))
output_files += glob.glob(os.path.join(output_dir, '*.xlsx'))
output_lines.append(f"現在のファイル数: {len(output_files)}件")

intermediate_files = [os.path.basename(f) for f in output_files if os.path.basename(f) not in final_outputs]

if intermediate_files:
    intermediate_dir = os.path.join(output_dir, 'intermediate')
    os.makedirs(intermediate_dir, exist_ok=True)

    moved_count = 0
    for f in intermediate_files:
        src = os.path.join(output_dir, f)
        dst = os.path.join(intermediate_dir, f)
        try:
            if os.path.exists(src):
                shutil.move(src, dst)
                moved_count += 1
        except:
            pass

    output_lines.append(f"移動: {moved_count}件の中間ファイル")
else:
    output_lines.append("移動対象なし")

output_lines.append("")

# サマリー
output_lines.append("=" * 80)
output_lines.append("最適化完了")
output_lines.append("=" * 80)
output_lines.append("")

output_lines.append("重要ファイル:")
output_lines.append(f"  for_claude: {len(important_files)}件")
for f in important_files:
    exists = "OK" if os.path.exists(os.path.join(for_claude_dir, f)) else "NG"
    output_lines.append(f"    [{exists}] {f}")

output_lines.append("")
output_lines.append(f"  output: {len(final_outputs)}件")
for f in final_outputs:
    path = os.path.join(output_dir, f)
    if os.path.exists(path):
        size_mb = os.path.getsize(path) / 1024 / 1024
        output_lines.append(f"    [OK] {f} ({size_mb:.2f} MB)")
    else:
        output_lines.append(f"    [NG] {f}")

output_lines.append("")
output_lines.append("=" * 80)

# ファイルに保存
report_file = os.path.join(for_claude_dir, 'optimization_report.txt')
with open(report_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"最適化完了: {report_file}")
