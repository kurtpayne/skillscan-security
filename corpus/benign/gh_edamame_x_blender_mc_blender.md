---
name: blender
description: Blender MCP scene creation, look-development, animation planning, and render-optimization workflow. Use when Codex needs to drive Blender through MCP to create or refine scenes, organize collections and materials, write and maintain a strict timeline-based specification, iterate with EEVEE, finish with Cycles GPU, choose camera and lens settings, gather references, or validate output with targeted frame or range renders. Also use when the user explicitly invokes $blender or asks in Japanese about コレクション整理, 仕様書, タイムライン管理, カメラ設定, and レンダリング最適化.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: EdamAme-x/blender-mcp-skills
# corpus-url: https://github.com/EdamAme-x/blender-mcp-skills/blob/8530e3ffc79fbad69490e2bee267ead68b9b925a/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# blender

Blender MCP を「見た目の勘」で動かさない。先に仕様を固定し、コレクション所有権とレビューゲートを厳格に運用してから Blender を触る。

## 非交渉ルール

- 仕様書なしで Blender を触り始めない。
- 単位系とスケール基準を決める前に lookdev を始めない。
- `Collection` にオブジェクトを放置しない。放置されたままのオブジェクトは未整理資産として扱い、先に移動と命名を済ませる。
- アセット所有権とショット配置を同じコレクションに混ぜない。
- 仕様変更が入ったら、先に仕様書を更新し、その後でシーンを更新する。
- 作業中は `EEVEE` を標準にする。`Cycles` は最終品質確認と本番レンダーまで持ち込まない。
- フルレンダーで確認しない。単フレーム、短区間、低品質で先に詰める。
- 画としての判断は viewport ではなくレンダー結果と仕様書の一致で行う。

## この skill の重点

- 仕様を文章化して、AI が視覚情報を見失っても再現できるようにする。
- Outliner をアセット所有権ベースで整理し、マテリアルやライトの責務を明確にする。
- 単位、寸法、命名を早期に固定し、後段のカメラ、DOF、ライティングのズレを防ぐ。
- タイムライン単位でショット意図、確認フレーム、完成条件を持たせる。
- レンダー設定を段階化し、制作中は速度、最終では品質に寄せる。
- カメラ、焦点距離、魚眼、被写界深度、`f-stop` を意図ベースで選ばせる。
- 参考資料を単に集めず、どの参考が何を担当するかまで仕様に落とす。

## 追加資料

見た目の質を上げたいときは、次の資料を必要なものだけ読む。

- 画作りの原則を詰めるなら [references/look-bible.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/look-bible.md)
- 定番の勝ち筋から始めるなら [references/style-recipes.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/style-recipes.md)
- 出力が素人っぽいときの切り分けは [references/failure-patterns.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/failure-patterns.md)
- Blender MCP をどう回すかの実行順は [references/blender-mcp-runbook.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/blender-mcp-runbook.md)
- still の実例は [references/example-still-session.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/example-still-session.md)
- animation の実例は [references/example-animation-session.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/example-animation-session.md)

## 最初に作るもの

Blender の編集前に、次の 4 つを必ず作る。

1. タイムライン仕様書
2. コレクション設計
3. 参考資料リスト
4. レビュー計画

長い作業ではワークスペースに `timeline_spec.md` を作る。ファイル作成が不要な場では同じ構造を Blender の Text datablock か会話内メモで維持する。
テンプレートが必要なら用途に応じて次を複製して始める。

- still なら [assets/timeline_spec_still_template.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/assets/timeline_spec_still_template.md)
- animation, loop, sequence なら [assets/timeline_spec_animation_template.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/assets/timeline_spec_animation_template.md)
- まだ形式が固まっていないなら [assets/timeline_spec_template.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/assets/timeline_spec_template.md)

## 仕様書の書き方

仕様書は感想文ではなく、後から別の agent が読んでも同じ判断ができる記録にする。曖昧語だけで終わらせず、フレーム、所有コレクション、レンズ、確認条件まで書く。

### テンプレート運用

- still は [assets/timeline_spec_still_template.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/assets/timeline_spec_still_template.md) を使う。
- animation は [assets/timeline_spec_animation_template.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/assets/timeline_spec_animation_template.md) を使う。
- 未確定案件だけ [assets/timeline_spec_template.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/assets/timeline_spec_template.md) を使う。
- テンプレートを削るより、空欄を埋める方向で使う。
- 使わない項目は黙って消さず、`not used` と理由を書く。
- レビュー後の差分はテンプレートではなく案件側の仕様書へ記録する。

### 必須セクション

- `Project`
- `Global Constraints`
- `Scale and Naming`
- `Collection Plan`
- `Asset Register`
- `Shot Timeline`
- `Reference Plan`
- `Review Plan`
- `Change Log`

### 必須ルール

- 1 ショットにつき `開始フレーム`, `終了フレーム`, `目的`, `画面の主役`, `カメラ`, `光`, `マテリアル`, `確認フレーム`, `完成条件` を持たせる。
- 1 アセットにつき `所有コレクション`, `使用ショット`, `主要マテリアル`, `依存するリグや FX` を持たせる。
- 1 プロジェクトにつき `単位系`, `スケール基準`, `命名規約` を先に固定する。
- 1 参考資料につき `用途` を 1 つ以上明記する。用途を書けない参考資料は採用しない。
- 変更が入るたびに `Change Log` に「何を」「なぜ」「どこまで更新済みか」を残す。
- still 画像でも `SHOT_010` のような 1 ショット構成を切り、確認フレームを定義する。

### 仕様書テンプレート

```md
# Project
- Goal:
- Output: still | shot | loop | sequence
- Resolution:
- Aspect Ratio:
- FPS:
- Global Frame Range:
- Unit System:
- Scale Reference:
- Style Sentence:
- Definition of Done:
  - 

# Global Constraints
- Must keep:
- Must avoid:
- Render budget during work:
- Final render target:

# Scale and Naming
- Unit System:
- Hero Scale Reference:
- Environment Scale Reference:
- Naming Rules:
  - AST_
  - OBJ_
  - MAT_
  - LGT_
  - CAM_
  - FX_

# Collection Plan
- COL_SRC_ENV:
- COL_SRC_HERO:
- COL_SRC_PROP:
- COL_SHOT_010:
- COL_SHOT_020:
- COL_LIGHT:
- COL_CAM:
- COL_FX:
- COL_RENDER_HELPER:
- COL_ARCHIVE:

# Asset Register
## AST_
- Owner Collection:
- Used In Shots:
- Materials:
- Modifiers/Rig/FX:
- Reuse Rule:
- Notes:

# Shot Timeline
## SHOT_010
- Frames:
- Purpose:
- Main Subject:
- Composition:
- Camera Type: perspective | fisheye | orthographic
- Lens / Focal Length:
- Sensor / Framing Note:
- Focus Target:
- f-stop:
- Camera Motion:
- Lighting Plan:
- Materials To Build:
- Collections Used:
- Review Frames:
- Short Range Preview:
- Accept If:
  - 

## SHOT_020
- Frames:
- Purpose:
- Main Subject:
- Composition:
- Camera Type:
- Lens / Focal Length:
- Focus Target:
- f-stop:
- Camera Motion:
- Lighting Plan:
- Materials To Build:
- Collections Used:
- Review Frames:
- Short Range Preview:
- Accept If:
  - 

# Reference Plan
## REF_
- Source:
- Role: silhouette | material | lighting | camera | motion | composition
- What To Borrow:
- What Not To Borrow:
- Related Shot / Asset:

# Review Plan
- Frame checks:
- Range checks:
- Preview quality settings:
- Final quality gate:

# Change Log
- YYYY-MM-DD HH:MM - Changed:
  - Reason:
  - Spec updated:
  - Scene updated:
```

## 仕様書を厳格にするコツ

- `かっこよく`, `シネマっぽく`, `良い感じ` で止めない。必ず `何が`, `どこに`, `どの程度` を補う。
- 数値を書ける項目は数値で書く。書けないなら比較語ではなく、対象と理由を書く。
- 色は `暖色`, `寒色` だけでなく、コントラスト、彩度、暗部の扱いまで書く。
- マテリアルは `金属` だけでなく、塗装、傷、粗さ、反射の強さ、汚れの分布まで書く。
- カメラは `寄る` だけでなく、焦点距離、アングル、高さ、被写界深度、歪みの意図まで書く。
- ライトは `明るく` だけでなく、key/fill/rim の役割、方向、硬さ、色温度感まで書く。
- モーションは `動く` だけでなく、開始、ピーク、収束、速度変化を書く。
- 空欄のまま進めない。未確定なら `TBD` ではなく「何を見て決めるか」を書く。

## スケールと命名

単位と命名が曖昧だと、カメラ、被写界深度、ライティング、物理系、マテリアルの判断が全部ぶれる。ここは初手で固定する。

### スケール規律

- `Unit System` を仕様書に書く。
- 主役アセットの基準寸法を `Hero Scale Reference` に書く。
- 環境物の代表寸法を `Environment Scale Reference` に書く。
- レンズや `f-stop` を詰める前に、主役と背景の相対スケールを確認する。
- 実寸前提の見た目を狙う場合、縮尺が合っているかを先に検証する。

### 命名規律

- アセットは `AST_`
- オブジェクトは `OBJ_`
- マテリアルは `MAT_`
- ライトは `LGT_`
- カメラは `CAM_`
- エフェクトは `FX_`
- ショットは `SHOT_010` のように 3 桁以上で揃える。
- 命名規則を途中で変えない。変えるなら `Change Log` に記録する。

## コレクション設計

コレクションは「見やすさ」のためではなく「責務分離」のために切る。少なくとも `source`, `shot`, `light/camera/fx`, `archive` を分ける。

### 推奨トップレベル構成

```text
COL_SRC_ENV
COL_SRC_HERO
COL_SRC_PROP
COL_SHOT_010
COL_SHOT_020
COL_LIGHT
COL_CAM
COL_FX
COL_RENDER_HELPER
COL_ARCHIVE
```

### 所有権ルール

- `COL_SRC_*` にアセットの本体、主要マテリアル、モディファイア、ジオメトリノード制御物、rig を置く。
- `COL_SHOT_*` にショット固有の配置、表示切り替え、ショット専用複製、ショット専用 override を置く。
- `COL_LIGHT` にライト rig を置き、ショット名や用途で名前を切る。
- `COL_CAM` にカメラを置き、ショット単位で命名する。
- `COL_FX` にシミュレーション、パーティクル、ボリューム、補助エミッタを置く。
- `COL_RENDER_HELPER` に holdout, shadow catcher, matte 用補助物、テスト用プローブを置く。
- `COL_ARCHIVE` に没案や古いバリエーションを退避させ、現役ショットから切り離す。

### マテリアル運用ルール

- マテリアルはアセット所有権に紐づける。ショット配置コレクションの都合でマテリアルを量産しない。
- 名前を `MAT_<asset>_<role>` の形で統一する。
- ショット専用バリエーションだけ `__S010` のようにショット suffix を付ける。
- `Material.001` を残さない。発生したら意図的な複製か accidental clone かを判定し、不要なら統合する。
- Boolean cutter, empty, helper mesh も所有アセットの source collection に置く。

### 禁止事項

- デフォルト `Collection` に新規オブジェクトを置いたまま lookdev を始める。
- `COL_SHOT_*` で本来 source にあるべきマテリアルを直接増殖させる。
- ライトやカメラをアセットコレクションに混ぜる。
- 1 コレクションに `source` と `shot override` を同居させる。

## 作業順序

次の順で進める。順序を飛ばすと、AI が後で視覚判断を再現できなくなる。

1. 仕様書を書く。
2. コレクション設計を切る。
3. 参考資料を集めて用途を割り当てる。
4. blockout を置く。
5. カメラを決める。
6. ライトの大枠を決める。
7. 主要マテリアルを作る。
8. 単フレーム確認を回す。
9. 短区間確認を回す。
10. 最終設定に上げる。

定番構図やルックから入るなら [references/style-recipes.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/style-recipes.md) を先に 1 つ選ぶ。MCP 操作順の迷いを減らしたいなら [references/blender-mcp-runbook.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/blender-mcp-runbook.md) を併読する。

## レビューゲート

各段階を通過する条件を先に決める。通過条件を書かずに「少し良くする」を続けない。

### Gate 1: Blockout

- シルエットが仕様書と一致する。
- 主役と背景のレイヤが読める。
- カメラ位置と主題の関係が固まっている。
- 所有コレクションが整理されている。

### Gate 2: Lookdev

- 主役アセットの主要マテリアルが揃っている。
- ラフな光で質感差が読める。
- 参考資料の担当項目が画に反映されている。
- `Review Frames` で破綻がない。

### Gate 3: Motion / Timing

- `Short Range Preview` でカメラと被写体の動きが破綻しない。
- 被写界深度、モーションのピーク、見せ場のフレームが仕様書どおり。
- ショット遷移前後で主役の見え方が崩れない。

### Gate 4: Final

- `Cycles` + `GPU` で単フレーム確認が通る。
- 簡略化とライトパスの制限をかけても意図が崩れない。
- 必要な短区間レンダーが通る。
- フルレンダー前に仕様書の `Definition of Done` を満たしている。

## 凍結点

後半で大崩れしやすい項目は、段階ごとに凍結する。

- Gate 1 通過後: 基本構図、主役配置、主要スケールを凍結する。
- Gate 2 通過後: レンズ方針、主要ライト配置、主要マテリアル方向性を凍結する。
- Gate 3 通過後: ショット尺、見せ場フレーム、カメラモーションの骨格を凍結する。
- Gate 4 直前: 仕様書の `Definition of Done` 以外の変更を止める。

凍結後に戻す場合は、先に仕様書と `Change Log` を更新する。

## レンダリング方針

### 作業中

- `EEVEE` を標準にする。
- 解像度倍率を落としてよい。まず 25% から 50% を使う。
- サンプルは低く抑え、単フレームか短区間で確認する。
- まだ固まっていない段階では full sequence を回さない。
- viewport の印象で判断せず、必ず render result を残す。

### 最終確認と本番

- `Cycles` に切り替える。
- `GPU` を使う。
- `Simplify` を有効にして、見た目を崩さない範囲で subdivision, texture, particle のコストを抑える。
- `Light Paths` は無制限にしない。まず `7` を上限の基準にして、必要なものだけ上げる。
- ノイズで詰まったら、サンプルをむやみに増やす前に、光、材質、被写界深度、ライトパスを見直す。

### 軽量確認のやり方

- 材質確認は単フレームで行う。
- カメラ移動確認は `Short Range Preview` に書いた区間だけを出す。
- ライティング確認は最も明暗差が大きいフレームを優先する。
- 演出確認は見せ場の開始、ピーク、収束の 3 点を先に見る。
- 迷ったらフル尺ではなく `特定フレーム` と `特定区間` に分解する。

### 必須レビュー点

- 各ショットの先頭フレーム
- 主役が最も大きく見えるフレーム
- 明暗差が最も強いフレーム
- 被写界深度が最も目立つフレーム
- ショット末尾か遷移直前フレーム

## カメラとレンズ

カメラは最後に味付けするものではなく、最初に構図を決める道具として扱う。レンズを決めずに layout を進めない。

### 基本ルール

- 通常の画は `perspective` を使う。
- `fisheye` は「広く写るから便利」で選ばない。誇張、没入、監視、極端な近接感など、意図があるときだけ使う。
- 焦点距離を仕様書に書く。広角か中望遠かを曖昧にしない。
- `f-stop` も仕様書に書く。被写界深度は偶然で決めない。
- focus target を明記する。どこにピントを置くか書かない DOF は事故の元になる。

### 判断の指針

- 広角は空間感と誇張を強める。背景が広く入り、近景の歪みが増える。
- 中望遠は被写体分離と圧縮感を作りやすい。
- 低い `f-stop` は浅い被写界深度を作るが、レイアウト確認には不向きになりやすい。
- 高い `f-stop` は安全だが、主役分離が弱くなることがある。
- 魚眼は視覚効果が強いので、参考資料か明確な演出意図がない限り使わない。

## 参考資料の集め方

参考資料は多ければ良いわけではない。各参考が何を担当するかを決める。

画作りの基準が曖昧なときは [references/look-bible.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/look-bible.md) を先に読み、構図、値設計、色、レンズ、スケールの優先順位を固定する。

### 参考資料の最低セット

- 構図参考 1 つ以上
- ライティング参考 1 つ以上
- 主要マテリアル参考を材質ごとに 1 つ以上
- カメラやレンズ感の参考 1 つ以上
- 動きがあるなら motion 参考 1 つ以上

### 調べ方

- 被写体名だけで検索しない。`subject + lighting`, `subject + 35mm`, `material close-up`, `cinematic frame`, `turnaround`, `breakdown` のように属性を足す。
- まず広く集め、その後で `何を借りるか` が明確なものだけ残す。
- 参考ごとに `silhouette`, `material`, `lighting`, `camera`, `motion` の役割を割り当てる。
- 参考が衝突したら、ショットごとに hero reference を 1 つ決め、それ以外は補助に回す。
- 参考から読み取った内容を仕様書へ言語化して転記する。画像を見たままにしない。

### 仕様に転記する項目

- シルエットの特徴
- 主役と背景の距離感
- 光の方向と硬さ
- 反射、粗さ、透過、発光の特徴
- 使うレンズ感
- 動きのテンポ
- 借りる要素と借りない要素

## AI が視覚に弱いことへの対策

AI は画面を一瞥して正しく保持し続けるのが苦手だと前提する。だから視覚判断は必ず文章へ落とす。

- レンダーを見たら、良し悪しを仕様書へ 1 行以上で反映する。
- `前より良い` で終わらせず、何が仕様に近づいたか書く。
- 破綻を見つけたら、症状、原因仮説、修正対象を分けて書く。
- レビューごとに `pass`, `fail`, `unknown` をつける。

## 変更管理

- 仕様変更を scene 変更より先に書く。
- カメラ変更、レンズ変更、ショット尺変更、マテリアル方針変更、参考差し替えは必ず `Change Log` に残す。
- 変更後は `Spec updated` と `Scene updated` を別々に記録する。
- 仕様だけ変わって scene が未更新なら、その状態を明示する。

## 失敗しやすい症状と対処

より細かい NG パターンは [references/failure-patterns.md](/mnt/c/Users/yun40/Desktop/blender-mcp-skills/references/failure-patterns.md) を使って診断する。

- 症状: マテリアルが `Material.001` だらけになる
  - 原因: shot collection 側で accidental clone を増やしている
  - 対処: source collection へ責務を戻し、shot 専用差分だけ suffix 付きで分ける

- 症状: 毎ターン見た目の判断がぶれる
  - 原因: 仕様書が弱く、画の意図が文書化されていない
  - 対処: shot ごとの `Accept If` と `Review Frames` を具体化する

- 症状: レンダー時間だけが増えて改善が見えない
  - 原因: 作業中から `Cycles` や高品質設定を回している
  - 対処: `EEVEE`, 低解像度, 単フレーム, 短区間へ戻し、最終だけ `Cycles GPU` に上げる

- 症状: 画角が毎回違って見える
  - 原因: レンズと camera type が仕様に固定されていない
  - 対処: focal length, camera type, focus target, `f-stop` を shot spec に固定する

- 症状: 参考資料はあるのに画がまとまらない
  - 原因: 参考ごとの担当が決まっていない
  - 対処: hero reference と補助 reference を分け、各 reference の借用要素を書く

## 完了条件

次を満たしたら完了とみなす。

- 仕様書が最新である
- source / shot / light / cam / fx / archive の責務が分離されている
- `Review Frames` と `Short Range Preview` が通っている
- 作業中は `EEVEE`、最終は `Cycles GPU` の方針が守られている
- `Simplify` と `Light Paths <= 7` を起点に最終品質が確認されている
- 参考資料の役割が仕様に転記されている