"""
処理に必要な全モジュールが揃っているか確認するスクリプト
"""
import sys

# 必要なモジュールのリスト
REQUIRED_MODULES = {
    # PDF処理
    'pdfplumber': 'PDFテーブル抽出',
    'pdfminer': 'PDF解析（pdfplumberの依存）',
    'pypdfium2': 'PDF処理（pdfplumberの依存）',
    'PIL': 'Pillow - 画像処理（pdfplumberの依存）',

    # データ処理
    'pandas': 'データ処理・CSV操作',
    'numpy': '数値計算（pandasの依存）',
    'openpyxl': 'Excel処理',

    # Google Translation API
    'google.cloud.translate': 'Google Translation API',
    'google.auth': 'Google認証',
    'google.api_core': 'Google API Core',

    # HTTP・通信
    'requests': 'HTTP通信',

    # 環境変数管理
    'dotenv': 'python-dotenv - 環境変数読み込み',

    # その他の依存モジュール
    'grpc': 'grpcio - gRPC通信',
    'cryptography': '暗号化処理',
}

# オプションモジュール（あると便利）
OPTIONAL_MODULES = {
    'marker': 'marker-pdf - PDF抽出（使用していない）',
}

def check_module(module_name, description):
    """モジュールのインポートを試行"""
    try:
        # モジュール名にドットが含まれる場合（サブモジュール）
        if '.' in module_name:
            parts = module_name.split('.')
            __import__(module_name)
            mod = sys.modules[module_name]
        else:
            mod = __import__(module_name)

        # バージョン情報を取得（可能な場合）
        version = getattr(mod, '__version__', 'バージョン不明')
        return True, version
    except ImportError as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("必要なモジュールの確認")
    print("=" * 80)
    print()

    # 必須モジュールのチェック
    print("-" * 80)
    print("必須モジュール")
    print("-" * 80)
    print()

    missing_modules = []
    available_modules = []

    for module_name, description in REQUIRED_MODULES.items():
        success, info = check_module(module_name, description)

        if success:
            status = "[OK]"
            available_modules.append(module_name)
            print(f"{status} {module_name:30s} {info:20s} - {description}")
        else:
            status = "[NG]"
            missing_modules.append((module_name, description))
            print(f"{status} {module_name:30s} {'インストール必要':20s} - {description}")

    print()

    # オプションモジュールのチェック
    print("-" * 80)
    print("オプションモジュール（参考）")
    print("-" * 80)
    print()

    for module_name, description in OPTIONAL_MODULES.items():
        success, info = check_module(module_name, description)

        if success:
            status = "[OK]"
            print(f"{status} {module_name:30s} {info:20s} - {description}")
        else:
            status = "[--]"
            print(f"{status} {module_name:30s} {'未インストール':20s} - {description}")

    print()

    # サマリー
    print("=" * 80)
    print("サマリー")
    print("=" * 80)
    print()

    total_required = len(REQUIRED_MODULES)
    total_available = len(available_modules)
    total_missing = len(missing_modules)

    print(f"必須モジュール: {total_required}個")
    print(f"利用可能: {total_available}個")
    print(f"不足: {total_missing}個")
    print()

    if missing_modules:
        print("[警告] 以下のモジュールが不足しています：")
        print()
        for module_name, description in missing_modules:
            print(f"  - {module_name}: {description}")
        print()
        print("インストールコマンド:")
        module_names = ' '.join([name for name, _ in missing_modules])
        print(f"  pip install {module_names}")
        print()
        return 1
    else:
        print("[成功] すべての必須モジュールが揃っています")
        print()

        # 実行可能な機能のリスト
        print("-" * 80)
        print("実行可能な機能")
        print("-" * 80)
        print()
        print("  1. PDF抽出データの検証")
        print("     - scripts/verify_pdf_extraction.py")
        print()
        print("  2. 言語コード辞書の検証")
        print("     - scripts/verify_language_json.py")
        print()
        print("  3. Google Translation API翻訳")
        print("     - scripts_google_translation/scripts/translator.py")
        print("     - scripts_google_translation/scripts/batch_translator.py")
        print()
        print("  4. CSV/Excel処理")
        print("     - scripts/compare_language_headers.py")
        print()
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
