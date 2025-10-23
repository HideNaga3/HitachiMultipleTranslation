# CLAUDE_GLOBAL.md

This file provides global guidance to Claude Code (claude.ai/code) for all projects.

---

## 【グローバル設定】Global Settings

このセクションの設定は**すべてのプロジェクト**に適用されます。

### 言語設定 / Language Settings

**このプロジェクトでは必ず日本語で対応してください。**

- すべての説明を日本語で行うこと
- すべての質問を日本語で行うこと
- すべてのコメントを日本語で記述すること
- エラーメッセージの説明も日本語で行うこと
- コード内のコメントも日本語で記述すること

**IMPORTANT: Always communicate in Japanese for this project.**
- All explanations must be in Japanese
- All questions must be in Japanese
- All comments must be in Japanese
- All error message explanations must be in Japanese
- All code comments must be in Japanese

### プロジェクト設定ファイル (CLAUDE.md) の使用方法 / How to Use Project Settings File (CLAUDE.md)

**CLAUDE.mdはプロジェクト固有の設定ファイルで、自由に編集・追記可能です。**

- **CLAUDE.mdの目的**: プロジェクト固有の情報を記録し、セッション間で引き継ぐ
- **記載すべき内容**:
  - プロジェクトの概要と目的
  - 重要な技術仕様（エンコーディング、データ形式、変換ルールなど）
  - プロジェクト固有のコーディング規約
  - ファイル構成とディレクトリ構造
  - 使用ライブラリとバージョン情報
  - セッション引継ぎに必要な注意事項
  - 進行中のタスクや次回セッションへの申し送り事項
  - よくあるエラーとその対処方法

**CLAUDE.md is a project-specific settings file that can be freely edited and updated.**

- **Purpose of CLAUDE.md**: Record project-specific information and maintain continuity between sessions
- **What to include**:
  - Project overview and objectives
  - Important technical specifications (encoding, data formats, conversion rules, etc.)
  - Project-specific coding conventions
  - File structure and directory organization
  - Libraries used and version information
  - Important notes for session handover
  - Ongoing tasks and notes for next session
  - Common errors and their solutions

**使用例 / Usage Example:**

プロジェクト開始時や重要な仕様が判明したときに、CLAUDE.mdに追記すること。
例えば：

```markdown
## プロジェクト概要
eStaffing勤怠データをStaffExpress形式に変換するツール

## 重要な技術仕様
- すべてのCSVファイルはCP932エンコーディング
- 入力: 1行が1人の半月分（最大16日分）
- 出力: 1行が1人の1日分（最大16行に展開）

## 進行状況
- Phase 1: CSV変換ロジック実装完了 ✓
- Phase 2: GUI実装（次回セッション）
```

**IMPORTANT: Always update CLAUDE.md when you discover important project information or specifications.**

### 作業スタイル / Working Style

- コードレビュー時は丁寧に説明すること
- エラーが発生した場合は、原因と解決策を明確に説明すること
- 変更前に既存のコードを必ず確認すること

### 絵文字の使用禁止 / No Emoji Policy

**重要: 絵文字は絶対に使用しないこと**

- すべてのテキスト出力で絵文字を使用しない
- Pythonスクリプトの出力でも絵文字を使用しない
- マークダウンファイルでも絵文字を使用しない
- コメントやログでも絵文字を使用しない
- チェックマークや記号が必要な場合は、テキスト表記を使用すること
  - OK: `[OK]`, `[SUCCESS]`, `[DONE]`, `チェック`, `完了`
  - NG: 絵文字全般

**IMPORTANT: Never use emojis**

- Do not use emojis in any text output
- Do not use emojis in Python script output
- Do not use emojis in markdown files
- Do not use emojis in comments or logs
- Use text representations when checkmarks or symbols are needed
  - OK: `[OK]`, `[SUCCESS]`, `[DONE]`, `check`, `completed`
  - NG: All emojis

**理由 / Reason:**
- Windows環境のコマンドプロンプトやPowerShellでは絵文字が正しく表示されない
- CP932エンコーディングでは絵文字がサポートされない
- 文字化けやエンコーディングエラーの原因となる

**Reason:**
- Emojis do not display correctly in Windows Command Prompt or PowerShell
- CP932 encoding does not support emojis
- Causes garbled text and encoding errors

### コマンド実行環境 / Command Execution Environment

**コマンドを使用する場合は PowerShell または コマンドプロンプト (cmd) を優先的に使用すること**

- Windows環境では、PowerShellまたはcmdを第一選択とすること
- Bash や他のシェルよりも、Windows標準のコマンド環境を優先すること
- スクリプト実行時も、PowerShellまたはバッチファイルを優先すること

**IMPORTANT: When using commands, prioritize PowerShell or Command Prompt (cmd)**

- In Windows environment, use PowerShell or cmd as the first choice
- Prioritize Windows native command environments over Bash or other shells
- When executing scripts, prefer PowerShell or batch files

**Bashツール使用時の重要な注意事項 / Important Notes for Bash Tool Usage**

Claude Codeには「Bash」ツールしかありませんが、必ずPowerShellコマンドをラップして実行すること。

**正しい使用例:**
```bash
# ファイル一覧
powershell -Command "Get-ChildItem"

# ファイル移動・リネーム
powershell -Command "Move-Item -Path 'old.txt' -Destination 'new.txt'"
powershell -Command "Rename-Item -Path 'temp_folder' -NewName 'new_folder'"

# ファイル削除
powershell -Command "Remove-Item 'file.txt'"

# ディレクトリ作成
powershell -Command "New-Item -ItemType Directory -Path 'newfolder'"

# ファイルコピー
powershell -Command "Copy-Item -Path 'source.txt' -Destination 'dest.txt'"
```

**避けるべき使用例:**
```bash
# ❌ 直接Bashコマンドを使わない
ls
dir
mv old.txt new.txt
rm file.txt
```

**Although Claude Code only has a "Bash" tool, always wrap PowerShell commands inside it.**

**Correct usage examples:**
```bash
# List files
powershell -Command "Get-ChildItem"

# Move/Rename files
powershell -Command "Move-Item -Path 'old.txt' -Destination 'new.txt'"
powershell -Command "Rename-Item -Path 'temp_folder' -NewName 'new_folder'"

# Delete files
powershell -Command "Remove-Item 'file.txt'"

# Create directory
powershell -Command "New-Item -ItemType Directory -Path 'newfolder'"

# Copy files
powershell -Command "Copy-Item -Path 'source.txt' -Destination 'dest.txt'"
```

**Examples to avoid:**
```bash
# ❌ Don't use direct Bash commands
ls
dir
mv old.txt new.txt
rm file.txt
```

### ファイルエンコーディング / File Encoding

**PowerShellファイル (.ps1) は必ずUTF-8 BOMで保存すること**

- `.ps1`ファイルを作成・編集する際は、UTF-8 BOM (Byte Order Mark) エンコーディングを使用すること
- これにより、PowerShellスクリプトでの日本語文字化けを防止できます

**IMPORTANT: Always save PowerShell files (.ps1) with UTF-8 BOM encoding**
- When creating or editing `.ps1` files, use UTF-8 BOM (Byte Order Mark) encoding
- This prevents Japanese character corruption in PowerShell scripts

### Python仮想環境の管理 / Python Virtual Environment Management

**Pythonモジュールをインストールする前に、必ず仮想環境の存在を確認すること**

- Pythonプロジェクトでは、必ず仮想環境 (.venv) を使用すること
- モジュールインストール前に以下を確認:
  1. `.venv` フォルダが存在するか確認
  2. 存在しない場合は、ユーザーに確認してから作成
  3. 仮想環境を有効化してからインストール
- グローバル環境へのインストールは避けること（システム汚染を防ぐため）

**IMPORTANT: Always check for virtual environment before installing Python modules**

- Always use virtual environment (.venv) for Python projects
- Before installing modules, check:
  1. Check if `.venv` folder exists
  2. If not exists, confirm with user before creating
  3. Activate virtual environment before installation
- Avoid installing to global environment (to prevent system pollution)

**仮想環境の確認と作成手順:**

```powershell
# 仮想環境の存在確認
Test-Path .venv

# 存在しない場合は作成 (ユーザー確認後)
python -m venv .venv

# 仮想環境の有効化 (Windows)
.venv\Scripts\activate

# モジュールインストール
pip install <module_name>
```

**Virtual environment check and creation:**

```powershell
# Check if virtual environment exists
Test-Path .venv

# Create if not exists (after user confirmation)
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install modules
pip install <module_name>
```

**Claude Codeでの実践的なコマンド実行方法 / Practical Command Execution in Claude Code**

Claude CodeのBashツールから仮想環境を使用する際は、以下の方法を使用すること:

```powershell
# ❌ 誤った方法（Bashコマンドとして直接実行）
.venv\Scripts\python.exe -m pip install pandas

# ✅ 正しい方法（PowerShell経由で実行）
powershell -Command ".venv\Scripts\python.exe -m pip install pandas"
```

**重要なポイント:**
- Claude CodeのBashツールはUnixシェル互換のため、Windows固有のパスが正しく解釈されない
- 必ず `powershell -Command` でラップすること
- 複数のモジュールを同時にインストールする場合は、スペース区切りで指定可能

**よく使うコマンド集:**

```powershell
# pipのアップグレード
powershell -Command ".venv\Scripts\python.exe -m pip install --upgrade pip"

# 複数モジュールの一括インストール
powershell -Command ".venv\Scripts\python.exe -m pip install pandas openpyxl oletools"

# インストール済みモジュールの確認
powershell -Command ".venv\Scripts\python.exe -m pip list"

# 特定モジュールのバージョン確認
powershell -Command ".venv\Scripts\python.exe -m pip show pandas"

# requirements.txtからインストール
powershell -Command ".venv\Scripts\python.exe -m pip install -r requirements.txt"

# Pythonスクリプトの実行
powershell -Command ".venv\Scripts\python.exe scripts/your_script.py"
```

**When using virtual environment from Claude Code's Bash tool:**

```powershell
# ❌ Wrong (direct execution as Bash command)
.venv\Scripts\python.exe -m pip install pandas

# ✅ Correct (wrap with PowerShell)
powershell -Command ".venv\Scripts\python.exe -m pip install pandas"
```

**Important points:**
- Claude Code's Bash tool is Unix shell compatible, so Windows-specific paths are not interpreted correctly
- Always wrap with `powershell -Command`
- For installing multiple modules, separate with spaces

**Frequently used commands:**

```powershell
# Upgrade pip
powershell -Command ".venv\Scripts\python.exe -m pip install --upgrade pip"

# Install multiple modules at once
powershell -Command ".venv\Scripts\python.exe -m pip install pandas openpyxl oletools"

# List installed modules
powershell -Command ".venv\Scripts\python.exe -m pip list"

# Check specific module version
powershell -Command ".venv\Scripts\python.exe -m pip show pandas"

# Install from requirements.txt
powershell -Command ".venv\Scripts\python.exe -m pip install -r requirements.txt"

# Execute Python script
powershell -Command ".venv\Scripts\python.exe scripts/your_script.py"
```

### よく使うツール / Frequently Used Tools

ユーザーが日常的に使用するツールとテクノロジー:

- **Python** - スクリプト作成、自動化、データ処理
- **Excel VBA** - Excel自動化、マクロ開発
- **AutoHotkey v1** - Windows自動化、ホットキー管理
- **Excel Power Query** - データ取得、変換、統合
- **PowerShell** - Windowsシステム管理、自動化スクリプト
- **コマンドプロンプト (Command Prompt)** - バッチ処理、基本的なシステム操作

**User's frequently used tools and technologies:**

- **Python** - Scripting, automation, data processing
- **Excel VBA** - Excel automation, macro development
- **AutoHotkey v1** - Windows automation, hotkey management
- **Excel Power Query** - Data retrieval, transformation, integration
- **PowerShell** - Windows system administration, automation scripts
- **Command Prompt** - Batch processing, basic system operations

### バックアップ方針 / Backup Policy

**ファイル編集時は必ず変更前バックアップを作成すること**

- ファイルを編集する前に、自動バックアップを作成すること
- **バックアップ対象**: テキストベースのスクリプトファイルのみ
  - 対象拡張子: `.py`, `.ps1`, `.txt`, `.ahk`, `.vbs`, `.bat`, `.cmd`, `.md`, `.json`, `.xml`, `.csv`, `.ini`, `.config`など
  - バイナリファイル（`.exe`, `.dll`, `.pdf`, `.xlsx`など）は除外
- バックアップの頻度: **約10分間隔**（同じファイルの編集が続く場合）
- バックアップファイル名形式: `元のファイル名_YYYYMMDD_HHMMSS.拡張子`
  - 例: `script.ps1` → `script_20250118_143022.ps1`
- バックアップ保存先: `backup/YYYY-MM-DD/` 形式の日付別フォルダ
  - 例: `backup/2025-01-18/script_20250118_143022.ps1`
- フォルダが存在しない場合は自動的に作成すること
- **古いバックアップの自動削除**: 3日前より古いバックアップフォルダは自動的に削除すること

**IMPORTANT: Always create backup before editing files**

- Create automatic backup before editing files
- **Backup targets**: Text-based script files only
  - Target extensions: `.py`, `.ps1`, `.txt`, `.ahk`, `.vbs`, `.bat`, `.cmd`, `.md`, `.json`, `.xml`, `.csv`, `.ini`, `.config`, etc.
  - Exclude binary files (`.exe`, `.dll`, `.pdf`, `.xlsx`, etc.)
- Backup frequency: **Approximately every 10 minutes** (when editing the same file continuously)
- Backup filename format: `original_filename_YYYYMMDD_HHMMSS.extension`
  - Example: `script.ps1` → `script_20250118_143022.ps1`
- Backup location: Date-based folders in `backup/YYYY-MM-DD/` format
  - Example: `backup/2025-01-18/script_20250118_143022.ps1`
- Automatically create folders if they don't exist
- **Automatic cleanup**: Delete backup folders older than 3 days

### 作業ログ / Work Log

**前回のセッションからの引継ぎ情報は `for_claude\log.txt` を必ず確認すること**

- セッション開始時は最初に `for_claude\log.txt` を読み込むこと
- このファイルには前回の作業内容、実装した機能、次回への引継ぎ事項が記録されています
- **作業中は定期的に `for_claude\log.txt` に進捗を追記すること（途中で中断しても大丈夫なように）**
  - 重要な作業を完了したタイミングで追記
  - 大きなタスクの途中でも、キリの良いところで追記
  - セッション中断に備えて、こまめに記録を残す
- 作業完了時は必ず `for_claude\log.txt` に作業内容を追記すること

**IMPORTANT: Always check `for_claude\log.txt` for session continuity**

- Read `for_claude\log.txt` at the beginning of each session
- This file contains previous work, implemented features, and handover notes
- **Write progress to `for_claude\log.txt` regularly during work (to ensure continuity if interrupted)**
  - Write after completing important tasks
  - Write at good breakpoints even in the middle of large tasks
  - Record frequently to prepare for session interruptions
- Append work progress to `for_claude\log.txt` when finishing tasks

**log.txtの分割 / Splitting log.txt**

**log.txtが大きくなりすぎた場合（約2,500行以上）は、複数ファイルに分割すること**

- 目的: ファイルサイズを管理しやすくし、セッション開始時の読み込みを高速化
- 分割タイミング: log.txtが約2,500行を超えた場合
- 保存場所: `for_claude/archive/` フォルダ

**命名規則:**
- 古いセッション: `sessions_XX-XX_log.txt`
  - 例: `sessions_01-05_log.txt` (セッション1-5の記録)
  - 例: `sessions_06-10_log.txt` (セッション6-10の記録)
- 完全バックアップ: `log_full_backup.txt` (分割前の元ファイル)
- 最新ログ: `log.txt` (現在のセッションから継続)

**分割手順:**
1. 分割用Pythonスクリプトを作成（行番号で分割）
2. アーカイブフォルダに古いセッションログを保存
3. 元のlog.txtを `log_full_backup.txt` としてアーカイブに保存
4. 最新セッション以降のみを新しい `log.txt` として保存
5. 分割スクリプトをアーカイブに移動

**分割例:**
```
元のlog.txt (2,672行)
  ↓ 分割
- archive/sessions_01-05_log.txt (605行)  ← セッション1-5
- archive/sessions_06-10_log.txt (1,109行) ← セッション6-10
- log.txt (958行)                          ← セッション11以降（最新）
- archive/log_full_backup.txt (2,672行)   ← 完全バックアップ
```

**IMPORTANT: Split log.txt when it becomes too large (approximately 2,500 lines or more)**

- Purpose: Manage file size and speed up session initialization
- Split timing: When log.txt exceeds approximately 2,500 lines
- Storage location: `for_claude/archive/` folder

**Naming convention:**
- Old sessions: `sessions_XX-XX_log.txt`
  - Example: `sessions_01-05_log.txt` (records from sessions 1-5)
  - Example: `sessions_06-10_log.txt` (records from sessions 6-10)
- Full backup: `log_full_backup.txt` (original file before split)
- Current log: `log.txt` (continues from current session)

**Split procedure:**
1. Create Python script for splitting (split by line numbers)
2. Save old session logs to archive folder
3. Save original log.txt as `log_full_backup.txt` in archive
4. Save only recent sessions onwards as new `log.txt`
5. Move split script to archive

**Split example:**
```
Original log.txt (2,672 lines)
  ↓ Split into
- archive/sessions_01-05_log.txt (605 lines)  ← Sessions 1-5
- archive/sessions_06-10_log.txt (1,109 lines) ← Sessions 6-10
- log.txt (958 lines)                          ← Session 11+ (current)
- archive/log_full_backup.txt (2,672 lines)   ← Full backup
```
