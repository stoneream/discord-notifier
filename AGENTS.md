# Repository Guidelines

## ローカリゼーション
- リポジトリで作業する Codex エージェントは、日本語での入出力を期待されます。指示や補足は日本語で記述し、回答も日本語ベースで行ってください。

## プロジェクト構成とモジュール整理
- `main.py` は `exchange-rate` と `tenki-jp` の各モードを切り替えるエントリーポイントです。新しい通知モードを追加する場合は `*_mode.py` を作成し、引数パーサーに登録してください。
- `discord_webhook_client.py` と `open_exchange_rate_client.py` は外部サービスへの通信をまとめたクライアントです。HTTP リクエストはここで扱い、各モードから再利用する方針を守ってください。
- `tenki_jp_mode.py` は Selenium を用いた天気情報取得を担当し、対象 URL は `tenki-jp-urls.txt` に記載されています。スクレイピング対象の XPath やオプションを更新した際はコメントや README で補足すると保守しやすくなります。
- スクリーンショットは既定でリポジトリ直下の `screenshot.png` に保存されます。複数ファイルを出力する必要が生じた場合は `assets/` 配下など専用ディレクトリを用意してください。
- テストコードは未整備ですが、追加する際は `tests/` ディレクトリを作成し、対象モジュールに合わせた `tests/test_exchange_rate_mode.py` のような命名を推奨します。

## ビルド・テスト・開発コマンド
- `uv sync` — `pyproject.toml` と `uv.lock` に基づいて依存関係をインストールします。
- `uv run python main.py --mode exchange-rate --app-id <APP_ID> --discord-webhook-url <WEBHOOK>` — 最新の USD/JPY レートを取得し、指定した Discord Webhook に送信します。
- `uv run python main.py --mode tenki-jp --chromedriver_path /usr/bin/chromedriver --discord-webhook-url <WEBHOOK> [--dry-run true]` — 天気ページのスクリーンショットを撮影し、必要に応じて送信します。`--dry-run true` を付けると投稿をスキップします。
- `uv run black .` — Black によるコード整形を実行します。
- GitHub Actions も `astral-sh/setup-uv@v2` と `uv sync --frozen` / `uv run` を利用しており、ローカルと CI の解決結果が揃うよう `uv.lock` を更新・コミットしてください。

## Dev Container
- `.devcontainer/Dockerfile` で `uv` と `direnv` を導入しています。再ビルド時にはイメージ内の `uv` が利用可能です。
- `.devcontainer/postCreateCommand.sh` では `uv sync --group dev` を実行し、`.venv` を自動的にアクティベートする設定を `.bashrc` に追記します。
- 環境変数 `UV_PROJECT_ENVIRONMENT=.venv` により、プロジェクト直下に仮想環境が作成されます。

## CI/CD
- `.github/workflows/notify-exchange-rate.yml` と `.github/workflows/notify-tenki-jp.yml` は `uv sync --frozen` で依存関係を解決し、`uv run python main.py` で各モードを実行します。
- ワークフローの更新後は `workflow_dispatch` で手動起動し、`uv` セットアップやスケジュール実行の成功を確認してください。

## コーディングスタイルと命名規約
- Python 3.13 を前提とし、インデントは 4 スペースで統一します。公開関数やクラスには可能な限り型ヒントを付与してください。
- Black によるフォーマットを標準とし、手動でのラップ指定は Black の整形結果を優先します。
- 関数・変数は `snake_case`、クラスは `PascalCase`、定数は `UPPER_SNAKE_CASE` とし、モジュールごとに関心事を分離します。
- 重複しがちなユーティリティ（時刻フォーマット、Discord 送信処理など）は共通関数化を検討し、責務を明確に保ちます。

## テスト指針
- テストには `pytest` を想定し、`uv run pytest` で実行できるように整備してください。ファイル名は `test_<対象>.py` とし、機能ごとにスイートを分けます。
- Open Exchange Rates や Discord Webhook などの外部通信はモックし、Selenium もヘッドレスでの挙動確認に留めると CI を軽量化できます。
- 為替レートの値検証やスクリーンショットの切り抜き範囲など、再発しやすい不具合には境界値テストを追加し、想定外ケースがある場合はコメントで明示します。

## コミットとプルリクエスト
- Git 履歴では簡潔で説明的なサマリ（例: `Fix exchange rate webhook error` や短い日本語文）を用いています。命令形を維持し、1 コミット 1 トピックを心掛けます。
- プルリクエスト本文には関連 Issue、動作確認コマンド、Selenium での UI 変更がある場合はスクリーンショットを添付してください。
- レビュー前に `uv run pytest` もしくは手動確認を完了し、必要なフォローアップや設定依存があれば明記します。

## 設定とシークレット管理
- API キーや Webhook URL は環境変数や `.env`（Git から除外）で管理し、CLI 引数で注入してください。リポジトリへ直書きしないよう注意します。
- Chromedriver のパスは環境によって異なるため、`--chromedriver_path` で上書きできる状態を維持し、標準以外のパスを使う場合はドキュメントか PR で共有してください。
- 本番運用環境では Discord 側のレート制限とエラーハンドリングを踏まえ、Webhook 失敗時のリトライ戦略や通知抑止設定を検討することを推奨します。
