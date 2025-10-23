"""
.envファイルを読み込んでGOOGLE_API_KEY変数に代入するスクリプト
"""
import os
from pathlib import Path


def load_google_api_key():
    """
    .envファイルからGOOGLE_API_KEYを読み込む

    Returns:
        str: Google API Key

    Raises:
        FileNotFoundError: .envファイルが見つからない場合
        ValueError: GOOGLE_API_KEYが.envファイルに存在しない場合
    """
    # プロジェクトルートディレクトリのパスを取得（scriptsフォルダの親）
    project_root = Path(__file__).parent.parent
    env_path = project_root / ".env"

    # .envファイルの存在確認
    if not env_path.exists():
        raise FileNotFoundError(f".envファイルが見つかりません: {env_path}")

    # .envファイルを読み込む
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # コメント行と空行をスキップ
            if not line or line.startswith("#"):
                continue

            # KEY=VALUE形式をパース
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # GOOGLE_API_KEYを探す
                if key == "GOOGLE_API_KEY":
                    # クォートを除去（もしあれば）
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    return value

    # GOOGLE_API_KEYが見つからなかった場合
    raise ValueError(".envファイルにGOOGLE_API_KEYが定義されていません")


if __name__ == "__main__":
    # テスト実行
    try:
        GOOGLE_API_KEY = load_google_api_key()
        print("[OK] GOOGLE_API_KEYを読み込みました")
        print(f"APIキーの長さ: {len(GOOGLE_API_KEY)} 文字")
    except Exception as e:
        print(f"[ERROR] {e}")
