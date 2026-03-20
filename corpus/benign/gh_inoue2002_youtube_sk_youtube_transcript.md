---
name: youtube-transcript
description: YouTube動画の文字起こし（トランスクリプト）をダウンロード・テキスト抽出するスキル。「YouTube文字起こし」「動画の内容を取得」「YouTubeの字幕を取得」「transcribe YouTube」などの依頼時に使用。
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: inoue2002/youtube-skill
# corpus-url: https://github.com/inoue2002/youtube-skill/blob/4c2458f0bed9c4d59de2510fecec9f9043735fac/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# YouTube Transcript Skill

YouTube動画の字幕・自動生成字幕をダウンロードし、テキストとして抽出するスキル。

## Prerequisites

- Python 3.x
- `yt-dlp` (`pip install yt-dlp` or `brew install yt-dlp`)

## Setup

スキルのディレクトリにある `transcript.py` を使用する。初回実行時に `yt-dlp` がインストールされていなければ、先にインストールすること。

```bash
# yt-dlpがインストールされていない場合
pip install yt-dlp
# または
brew install yt-dlp
```

## Usage

### Basic: SRT字幕をダウンロード

```bash
python <skill-dir>/transcript.py <YouTube_URL_or_VIDEO_ID>
```

### テキストのみ抽出（タイムスタンプ除去）

```bash
python <skill-dir>/transcript.py <YouTube_URL_or_VIDEO_ID> -t
```

### オプション

| Flag | Description | Default |
|------|-------------|---------|
| `-l LANG` | 字幕の言語コード | `ja` |
| `-o DIR` | 出力ディレクトリ | `output` |
| `-t` | テキストのみ出力 | off |

### 英語字幕を取得する場合

```bash
python <skill-dir>/transcript.py <URL> -l en -t
```

## Workflow

1. ユーザーからYouTube URLまたは動画IDを受け取る
2. `transcript.py` を `-t` フラグ付きで実行してテキストを取得
3. 出力ファイル（`output/<video_id>.<lang>.txt`）を読み取る
4. ユーザーの要求に応じて要約・分析・翻訳などを行う

## Notes

- 自動生成字幕（auto-generated subtitles）に対応している
- 字幕が存在しない動画ではエラーになる
- SRTファイルからテキスト抽出時にHTMLタグと重複行は自動除去される
- `<skill-dir>` は、このSKILL.mdがあるディレクトリのパスに読み替えること