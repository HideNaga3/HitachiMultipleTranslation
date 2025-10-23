"""
作成したJSONファイルを検証するスクリプト
"""
import json

# JSONファイルのパス
base_path = r'C:\python_script\test_space\MitsubishiMultipleTranslation\core_files'
txt_path = f'{base_path}\\jp_headers_of_output_csv.txt'
mapping_json = f'{base_path}\\language_code_mapping.json'
reverse_json = f'{base_path}\\language_name_to_code.json'
codes_json = f'{base_path}\\language_codes_41.json'

print("=" * 80)
print("JSONファイル検証")
print("=" * 80)
print()

# txtファイル読み込み
with open(txt_path, 'r', encoding='utf-8') as f:
    txt_languages = [line.strip() for line in f if line.strip()]

print(f"[txtファイル] {len(txt_languages)}言語")
print()

# JSONファイル読み込み
with open(mapping_json, 'r', encoding='utf-8') as f:
    code_to_name = json.load(f)

with open(reverse_json, 'r', encoding='utf-8') as f:
    name_to_code = json.load(f)

with open(codes_json, 'r', encoding='utf-8') as f:
    codes_41 = json.load(f)

print(f"[language_code_mapping.json] {len(code_to_name)}エントリ（代替コード含む）")
print(f"[language_name_to_code.json] {len(name_to_code)}エントリ")
print(f"[language_codes_41.json] {codes_41['total_languages']}言語")
print()

# 検証1: txtファイルの全言語がname_to_codeに含まれているか
print("=" * 80)
print("検証1: txtファイルの全言語がJSONに含まれているか")
print("=" * 80)
missing_in_json = []
for lang in txt_languages:
    if lang not in name_to_code:
        missing_in_json.append(lang)

if missing_in_json:
    print(f"[NG] JSONに含まれていない言語: {len(missing_in_json)}言語")
    for lang in missing_in_json:
        print(f"  - {lang}")
else:
    print("[OK] txtファイルの全言語がJSONに含まれています")
print()

# 検証2: name_to_codeとcode_to_nameの整合性
print("=" * 80)
print("検証2: 日本語名→言語コード→日本語名の変換整合性")
print("=" * 80)
inconsistent = []
for jp_name, code in name_to_code.items():
    if code not in code_to_name:
        inconsistent.append(f"{jp_name} -> {code} (コードがmapping.jsonに存在しない)")
    elif code_to_name[code] != jp_name:
        inconsistent.append(f"{jp_name} -> {code} -> {code_to_name[code]} (名前が一致しない)")

if inconsistent:
    print(f"[NG] 不整合: {len(inconsistent)}件")
    for item in inconsistent:
        print(f"  - {item}")
else:
    print("[OK] 日本語名と言語コードの変換が整合しています")
print()

# 検証3: language_codes_41.jsonの内容確認
print("=" * 80)
print("検証3: language_codes_41.jsonの内容確認")
print("=" * 80)
print(f"言語コード数: {len(codes_41['language_codes'])}個")
print(f"日本語名数: {len(codes_41['language_names_jp'])}個")

if len(codes_41['language_codes']) != len(codes_41['language_names_jp']):
    print("[NG] 言語コードと日本語名の数が一致しません")
else:
    print("[OK] 言語コードと日本語名の数が一致しています")

# 言語コードと日本語名の対応が正しいか確認
print()
print("言語コードと日本語名の対応確認:")
mismatches = []
for i, (code, jp_name) in enumerate(zip(codes_41['language_codes'], codes_41['language_names_jp']), 1):
    expected_name = code_to_name.get(code, "【未定義】")
    if expected_name != jp_name:
        mismatches.append(f"  {i}. {code}: 期待={expected_name}, 実際={jp_name}")

if mismatches:
    print(f"[NG] 不一致: {len(mismatches)}件")
    for m in mismatches:
        print(m)
else:
    print("[OK] 全ての言語コードと日本語名が正しく対応しています")
print()

# 検証4: txtファイルとlanguage_codes_41.jsonの順番が一致しているか
print("=" * 80)
print("検証4: txtファイルとlanguage_codes_41.jsonの順番が一致しているか")
print("=" * 80)
order_mismatches = []
for i, (txt_lang, json_lang) in enumerate(zip(txt_languages, codes_41['language_names_jp']), 1):
    if txt_lang != json_lang:
        order_mismatches.append(f"  {i}行目: txt={txt_lang}, json={json_lang}")

if order_mismatches:
    print(f"[NG] 順番の不一致: {len(order_mismatches)}件")
    for m in order_mismatches:
        print(m)
else:
    print("[OK] txtファイルとJSONの順番が完全に一致しています")
print()

# サマリー
print("=" * 80)
print("検証サマリー")
print("=" * 80)
all_ok = (
    len(missing_in_json) == 0 and
    len(inconsistent) == 0 and
    len(codes_41['language_codes']) == len(codes_41['language_names_jp']) and
    len(mismatches) == 0 and
    len(order_mismatches) == 0
)

if all_ok:
    print("[SUCCESS] 全ての検証に合格しました")
    print()
    print("作成されたJSONファイル:")
    print(f"  - language_code_mapping.json: {len(code_to_name)}エントリ（代替コード含む）")
    print(f"  - language_name_to_code.json: {len(name_to_code)}エントリ")
    print(f"  - language_codes_41.json: {codes_41['total_languages']}言語")
else:
    print("[FAILED] いくつかの検証に失敗しました。上記の詳細を確認してください。")
