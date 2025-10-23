"""
txtファイルとCSVファイルの言語リストを比較するスクリプト
"""
import csv

# txtファイルから言語リストを読み込み
txt_path = r'C:\python_script\test_space\MitsubishiMultipleTranslation\core_files\jp_headers_of_output_csv.txt'
csv_path = r'C:\python_script\test_space\MitsubishiMultipleTranslation\core_files\ourput_csv_template_utf8bom.csv'

# txtファイル読み込み
with open(txt_path, 'r', encoding='utf-8') as f:
    txt_languages = [line.strip() for line in f if line.strip()]

# CSVファイル読み込み（1行目がヘッダー）
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    csv_headers = next(reader)

# 言語コードと日本語名のマッピング（Google Translation API準拠）
language_code_mapping = {
    'ja': '日本語',
    'en': '英語',
    'zh': '中国語（簡体）',
    'zh-CN': '中国語（簡体）',
    'vi': 'ベトナム語',
    'fil': 'タガログ語（フィリピン）',
    'fil-PH': 'タガログ語（フィリピン）',
    'tl': 'タガログ語（フィリピン）',
    'ne': 'ネパール語',
    'pt': 'ポルトガル語（ポルトガル）',
    'pt-PT': 'ポルトガル語（ポルトガル）',
    'pt-BR': 'ポルトガル語（ブラジル）',
    'es': 'スペイン語（スペイン）',
    'es-ES': 'スペイン語（スペイン）',
    'es-MX': 'スペイン語（メキシコ）',
    'th': 'タイ語',
    'id': 'インドネシア語',
    'my': 'ミャンマー語',
    'ko': '韓国語',
    'mn': 'モンゴル語',
    'ar': 'アラビア語（アラブ首長国連邦）',
    'ar-AE': 'アラビア語（UAE）',
    'ar-EG': 'アラビア語（エジプト）',
    'fa': 'ペルシャ語(イラン)',
    'tr': 'トルコ語',
    'ru': 'ロシア語',
    'hi': 'ヒンディー語（インド）',
    'ur': 'ウルドゥー語（パキスタン）',
    'bn': 'ベンガル語（バングラデシュ）',
    'si': 'シンハラ語（スリランカ）',
    'km': 'クメール語（カンボジア）',
    'lo': 'ラオ語（ラオス）',
    'ms': 'マレー語（マレーシア）',
    'ta': 'タミル語（インド）',
    'fr': 'フランス語（フランス）',
    'fr-FR': 'フランス語（フランス）',
    'fr-CA': 'フランス語（カナダ）',
    'de': 'ドイツ語',
    'hu': 'ハンガリー語',
    'cs': 'チェコ語',
    'pl': 'ポーランド語',
    'nl': 'オランダ語',
    'da': 'デンマーク語',
    'fi': 'フィンランド語',
    'sv': 'スウェーデン語',
    'lb': 'ルクセンブルク語',
    'af': 'アフリカーンス語（南アフリカ）',
}

print("=" * 80)
print("txtファイルとCSVファイルの言語リスト比較")
print("=" * 80)
print()

print(f"[txtファイル] {txt_path}")
print(f"言語数: {len(txt_languages)}言語")
print()

print(f"[CSVファイル] {csv_path}")
print(f"言語コード数: {len(csv_headers)}言語")
print()

# CSVの言語コードを日本語名に変換
csv_languages_jp = []
for code in csv_headers:
    jp_name = language_code_mapping.get(code, f"【未定義: {code}】")
    csv_languages_jp.append(jp_name)

print("=" * 80)
print("CSVファイルの言語コード一覧（日本語名変換）")
print("=" * 80)
for i, (code, jp_name) in enumerate(zip(csv_headers, csv_languages_jp), 1):
    print(f"{i:2d}. {code:10s} → {jp_name}")
print()

# 差異分析
txt_set = set(txt_languages)
csv_set = set(csv_languages_jp)

missing_in_csv = txt_set - csv_set
extra_in_csv = csv_set - txt_set

print("=" * 80)
print("差異分析")
print("=" * 80)
print()

if missing_in_csv:
    print(f"[txtにあるがCSVにない言語] {len(missing_in_csv)}言語")
    for lang in sorted(missing_in_csv):
        print(f"  - {lang}")
    print()
else:
    print("[txtにあるがCSVにない言語] なし")
    print()

if extra_in_csv:
    print(f"[CSVにあるがtxtにない言語] {len(extra_in_csv)}言語")
    for lang in sorted(extra_in_csv):
        if lang.startswith("【未定義"):
            print(f"  - {lang} ← マッピング定義が必要")
        else:
            print(f"  - {lang}")
    print()
else:
    print("[CSVにあるがtxtにない言語] なし")
    print()

# 完全一致チェック
if txt_set == csv_set:
    print("[OK] txtとCSVの言語リストは完全に一致しています")
else:
    print(f"[NG] txtとCSVの言語リストに差異があります（差分: {len(missing_in_csv) + len(extra_in_csv)}言語）")

print()
print("=" * 80)
print("推奨される対応")
print("=" * 80)
if missing_in_csv:
    print()
    print("txtにあってCSVにない言語の言語コードを追加してください：")
    for lang in sorted(missing_in_csv):
        # 逆引き（日本語名→言語コード）
        code_candidates = [k for k, v in language_code_mapping.items() if v == lang]
        if code_candidates:
            print(f"  - {lang}: {', '.join(code_candidates)}")
        else:
            print(f"  - {lang}: 【言語コード要確認】")
