---
name: myrag
description: 開発で得た知見・教訓・ノウハウを SQLite ベクトルDB に蓄積し、応答時にベクトル検索で関連情報を取得する。「情報を記録したい」「過去の知見を検索したい」「学んだことを保存して」という依頼で起動。知識の蓄積・検索・活用の流れで進める。copilot-instructions.md や AGENTS.md の作成は対象外（agent-customization スキルを使用）。
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: aokumablue/myrag
# corpus-url: https://github.com/aokumablue/myrag/blob/560272e8809443dc1cd1fcf9aedfefd227c417fb/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Myrag

開発で得た知見・教訓・ノウハウを SQLite + sqlite-vec でベクトル検索可能な形で蓄積・活用する。

**技術スタック**: [sqlite-vec](https://alexgarcia.xyz/sqlite-vec/) / [sentence-transformers](https://sbert.net/) / intfloat/multilingual-e5-small

## 設計原則

1. **ローカル完結**: 外部 API に依存しない。Embedding 生成もローカルモデルで行う
2. **自動蓄積**: エージェントが得た知見は明示的な指示がなくても蓄積を提案する
3. **検索優先**: 新しいタスクに着手する前に関連知識を検索し、過去の失敗を繰り返さない
4. **冪等操作**: content_hash で重複を検出し、同じ内容は二重登録しない

## DB 初期化

初回利用時に以下を実行する。DB が既に存在する場合はスキップする。

```bash
python3 .github/skills/myrag/scripts/init_db.py
```

DB パス: `~/myrag.sqlite3`

## 知識の蓄積（Store）

### いつ蓄積するか

- ユーザーが「記録して」「保存して」「覚えておいて」と依頼した時
- デバッグで原因と解決策が判明した時
- 新しい技術パターン・ベストプラクティスを発見した時
- ミスの原因と対策が確定した時

### 蓄積コマンド

```bash
python3 .github/skills/myrag/scripts/store.py \
  --content "Next.js 15 で middleware.ts のマッチャーに '/((?!_next|api).*)' を使うと静的アセットもマッチする。'/((?!_next|api|favicon.ico).*)' に修正する" \
  --source "debugSession:2025-03-10" \
  --category "nextjs" \
  --tags "middleware,routing,gotcha"
```

**引数**:

| 引数         | 必須 | 説明                                          |
| ------------ | ---- | --------------------------------------------- |
| `--content`  | Yes  | 蓄積するテキスト。事実と解決策をセットで書く  |
| `--source`   | No   | 情報源（ファイルパス、URL、セッション名など） |
| `--category` | No   | 分類（技術名、プロジェクト名など）            |
| `--tags`     | No   | カンマ区切りのタグ                            |

### content の書き方

```
# 良い例: 事実 + 原因 + 解決策がセット
"Prisma の findMany で include を深くネストすると N+1 が発生する。
select 句で必要なリレーションのみ指定し、_count を使って件数だけ取得する"

# 悪い例: 曖昧で再利用できない
"Prisma のクエリが遅い"
```

## 知識の検索（Search）

### いつ検索するか

- 新しいタスクに着手する前
- エラーや問題が発生した時
- 技術選定で過去の判断を参照したい時

### 検索コマンド

```bash
python3 .github/skills/myrag/scripts/search.py \
  --query "Next.js middleware routing" \
  --limit 5
```

**引数**:

| 引数          | 必須 | 説明                                                |
| ------------- | ---- | --------------------------------------------------- |
| `--query`     | Yes  | 検索クエリ（自然文で書く）                          |
| `--limit`     | No   | 返す件数（デフォルト: 5）                           |
| `--category`  | No   | カテゴリでフィルタ                                  |
| `--threshold` | No   | 類似度閾値 0.0-1.0（デフォルト: 0.0、低いほど近い） |

### 検索結果の活用

検索結果は JSON で返る。`distance` が小さいほど関連度が高い。

```json
[
  {
    "id": 42,
    "content": "Next.js 15 で middleware.ts のマッチャーに...",
    "source": "debugSession:2025-03-10",
    "category": "nextjs",
    "tags": "middleware,routing,gotcha",
    "distance": 0.234,
    "created_at": "2025-03-10T14:30:00"
  }
]
```

## DB 管理

```bash
# 統計情報を表示
python3 .github/skills/myrag/scripts/manage.py stats

# カテゴリ一覧
python3 .github/skills/myrag/scripts/manage.py categories

# 特定エントリを削除
python3 .github/skills/myrag/scripts/manage.py delete --id 42

# 全件削除（確認プロンプトあり）
python3 .github/skills/myrag/scripts/manage.py clear
```

## 同梱リソース

- [references/schema.md](references/schema.md) — テーブル設計・インデックス詳細
- `scripts/init_db.py` — DB 初期化（テーブル作成・sqlite-vec ロード）
- `scripts/store.py` — 知識の蓄積（Embedding 生成 + INSERT）
- `scripts/search.py` — ベクトル検索（KNN クエリ）
- `scripts/manage.py` — DB 管理（統計・削除・一覧）

## 依存パッケージ

初回利用前にインストールが必要:

```bash
pip install sqlite-vec sentence-transformers
```

## 完了チェック

- [ ] `~/myrag.sqlite3` が作成されている
- [ ] `store.py` で知識を蓄積できる
- [ ] `search.py` でベクトル検索が動作する
- [ ] 重複 content は content_hash で弾かれる
- [ ] 検索結果が JSON で返る