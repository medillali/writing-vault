"""生成《超级骷髅兵》全书蒸馏的独立离线审查页。"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from pathlib import Path
from typing import Any, Iterable


SOURCE_ID = "src-9ff09c395734410b856f77c77a652834"
BOOK_TITLE = "超级骷髅兵"
VOLUME_COUNT = 18
DIMENSIONS = (
    "worldbuilding",
    "characters",
    "plot",
    "style",
    "narrative",
    "dialogue",
    "pacing",
    "themes",
    "continuity",
)
DIMENSION_LABELS = {
    "worldbuilding": "世界构建",
    "characters": "人物",
    "plot": "情节",
    "style": "文风",
    "narrative": "叙事",
    "dialogue": "对话",
    "pacing": "节奏",
    "themes": "主题",
    "continuity": "连续性",
}
TYPE_LABELS = {"character": "人物", "scene": "场景", "pattern": "机制"}
KIND_LABELS = {"fact": "事实", "inference": "推断", "synthesis": "机制抽象", "plan": "计划"}
FIELD_LABELS = {
    "name": "人物",
    "aliases": "异名",
    "identity_notes": "身份辨析",
    "opening_observations": "原开篇观察（保留历史）",
    "summary": "概述",
    "goal": "目标",
    "conflict": "冲突",
    "arc_change": "本集变化",
    "relationships": "关系",
    "knowledge_limits": "认知边界",
    "obstacle": "阻碍",
    "choice": "选择",
    "consequence": "后果",
    "state_change": "状态变化",
    "why_it_works": "有效原因",
    "applicability": "适用场景",
    "failure_mode": "失效条件",
    "steps": "迁移步骤",
    "limits": "适用边界",
    "volume_history": "逐集变化",
    "coverage_note": "阅读范围",
    "unknowns": "尚未确认",
    "decision_pattern": "决策方式",
    "contradiction": "内在矛盾",
    "originality_note": "原创使用提示",
    "aliases_in_source": "原文别名",
    "alias_basis": "别名依据",
    "relationship": "关系",
    "confirmed": "可确认行为",
    "uncertain": "不确定项",
    "narrative_function": "叙事作用",
    "knowledge_boundary": "认知边界",
    "misbeliefs": "错误判断",
    "perspective_boundary": "视角边界",
    "relationship_in_sample": "样段关系",
    "name_note": "姓名辨析",
    "arc_in_sample": "样段变化",
    "volume": "集数",
    "note": "记录",
    "status": "状态",
    "title": "标题",
}


def esc(value: Any) -> str:
    """将任意字段转换成适合 HTML 文本或属性的安全字符串。"""

    return html.escape(str(value), quote=True)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_script_json(value: Any) -> str:
    """序列化嵌入 script 的 JSON，并阻断标签闭合与实体解析。"""

    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def latest_revision(source: dict[str, Any]) -> dict[str, Any]:
    revisions = source.get("revisions") or []
    wanted = source.get("revision")
    for revision in revisions:
        if revision.get("revision") == wanted:
            return revision
    return revisions[-1] if revisions else {}


def chapter_map(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(chapter.get("chapter_id")): chapter
        for chapter in latest_revision(source).get("chapters", [])
        if chapter.get("chapter_id")
    }


def is_non_narrative(chapter_id: str, chapter: dict[str, Any]) -> bool:
    title = str(chapter.get("title", "")).strip()
    return chapter_id == "ch-0001" or title == "章前内容" or bool(
        re.match(r"^第[一二三四五六七八九十百零〇两\d]+集(?:\s|$)", title)
    )


def load_volumes(report_dir: Path) -> list[dict[str, Any] | None]:
    volumes: list[dict[str, Any] | None] = []
    for number in range(1, VOLUME_COUNT + 1):
        path = report_dir / f"vol{number:02d}.json"
        if not path.exists():
            volumes.append(None)
            continue
        try:
            report = read_json(path)
            if not isinstance(report, dict):
                raise ValueError("顶层不是对象")
            report["_file"] = path.name
            volumes.append(report)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            volumes.append({"volume": number, "_load_error": str(exc), "_file": path.name})
    return volumes


def evidence_label(
    evidence: dict[str, Any],
    chapters: dict[str, dict[str, Any]],
    fallback_kind: str = "",
) -> str:
    chapter_id = str(evidence.get("chapter_id", "未标章节"))
    chapter = chapters.get(chapter_id, {})
    title = chapter.get("title") or chapter_id
    start = evidence.get("start_line")
    end = evidence.get("end_line")
    if start is not None and end is not None:
        lines = f"第{start}–{end}行"
    elif start is not None:
        lines = f"第{start}行"
    else:
        lines = "未标行号"
    kind = evidence.get("claim_kind") or fallback_kind
    kind_text = f" · {KIND_LABELS.get(str(kind), str(kind))}" if kind else ""
    return f"{title}（{chapter_id}） · {lines}{kind_text}"


def render_evidence(
    evidence: Iterable[dict[str, Any]] | None,
    chapters: dict[str, dict[str, Any]],
    fallback_kind: str = "",
) -> str:
    items = [item for item in (evidence or []) if isinstance(item, dict)]
    if not items:
        return '<p class="muted">未附章节证据。</p>'
    rows = "".join(f"<li>{esc(evidence_label(item, chapters, fallback_kind))}</li>" for item in items)
    return f'<details class="evidence"><summary>展开证据（{len(items)} 条）</summary><ul>{rows}</ul></details>'


def render_dimension_item(item: dict[str, Any], chapters: dict[str, dict[str, Any]]) -> str:
    fields = (
        ("主张", item.get("claim")),
        ("机制", item.get("mechanism")),
        ("迁移", item.get("application")),
        ("边界", item.get("limitation")),
    )
    body = "".join(
        f'<div class="analysis-field"><b>{label}</b><p>{esc(value or "未填写")}</p></div>'
        for label, value in fields
    )
    return (
        '<article class="analysis-item">'
        f"{body}{render_evidence(item.get('evidence'), chapters, str(item.get('claim_kind', '')))}"
        "</article>"
    )


def render_dimensions(report: dict[str, Any], chapters: dict[str, dict[str, Any]]) -> str:
    dimensions = report.get("dimensions") if isinstance(report.get("dimensions"), dict) else {}
    groups = []
    for key in DIMENSIONS:
        items = dimensions.get(key) or []
        content = "".join(
            render_dimension_item(item, chapters) for item in items if isinstance(item, dict)
        )
        if not content:
            content = '<p class="muted">本维度没有可展示条目。</p>'
        groups.append(
            f'<section class="dimension-group"><h4>{esc(DIMENSION_LABELS[key])}</h4>{content}</section>'
        )
    return "".join(groups)


def render_chapter_notes(report: dict[str, Any], chapters: dict[str, dict[str, Any]]) -> str:
    rows = []
    for note in report.get("chapter_notes") or []:
        if not isinstance(note, dict):
            continue
        chapter_id = str(note.get("chapter_id", "未标章节"))
        chapter = chapters.get(chapter_id, {})
        title = chapter.get("title") or chapter_id
        badge = "非正文" if is_non_narrative(chapter_id, chapter) else "正文"
        rows.append(
            '<article class="chapter-note">'
            f'<div class="card-meta">{esc(badge)} · {esc(chapter_id)}</div>'
            f"<h4>{esc(title)}</h4><p>{esc(note.get('observation', '未填写观察'))}</p>"
            "</article>"
        )
    return "".join(rows) or '<p class="muted">没有章节观察。</p>'


def render_questions(report: dict[str, Any], chapters: dict[str, dict[str, Any]]) -> str:
    questions = []
    for item in report.get("questions") or []:
        if isinstance(item, str):
            questions.append(f"<li><p>{esc(item)}</p></li>")
        elif isinstance(item, dict):
            questions.append(
                "<li>"
                f"<b>{esc(item.get('question', '未命名疑点'))}</b>"
                f"<p>{esc(item.get('reason', ''))}</p>"
                f"{render_evidence(item.get('evidence'), chapters)}"
                "</li>"
            )
    revisions = []
    for item in report.get("revisions_to_earlier") or []:
        if isinstance(item, str):
            revisions.append(f"<li>{esc(item)}</li>")
        elif isinstance(item, dict):
            description = item.get("description") or item.get("revision") or item.get("note") or json.dumps(item, ensure_ascii=False)
            revisions.append(
                f"<li><p>{esc(description)}</p>{render_evidence(item.get('evidence'), chapters)}</li>"
            )
    return (
        '<div class="review-columns">'
        '<section><h4>疑点</h4>'
        + (f"<ul>{''.join(questions)}</ul>" if questions else '<p class="muted">本集未记录疑点。</p>')
        + '</section><section><h4>对前序判断的修订</h4>'
        + (f"<ul>{''.join(revisions)}</ul>" if revisions else '<p class="muted">本集没有提出修订。</p>')
        + "</section></div>"
    )


def volume_counts(report: dict[str, Any], chapters: dict[str, dict[str, Any]]) -> tuple[int, int]:
    narrative = 0
    non_narrative = 0
    for chapter_id_value in report.get("chapter_ids") or []:
        chapter_id = str(chapter_id_value)
        if is_non_narrative(chapter_id, chapters.get(chapter_id, {})):
            non_narrative += 1
        else:
            narrative += 1
    return narrative, non_narrative


def render_progress(volumes: list[dict[str, Any] | None], chapters: dict[str, dict[str, Any]]) -> str:
    cards = []
    for number, report in enumerate(volumes, 1):
        if report is None:
            status = "尚未入库"
            detail = "等待九维报告审查入库"
            css = "pending"
        elif report.get("_load_error"):
            status = "读取失败"
            detail = "报告存在，但当前无法解析"
            css = "error"
        else:
            narrative, non_narrative = volume_counts(report, chapters)
            status = "已完成"
            detail = f"{narrative} 章正文 · {non_narrative} 个标题/章前"
            css = "complete"
        cards.append(
            f'<a class="progress-card {css}" data-volume="{number}" href="#vol-{number:02d}">'
            f'<span class="volume-number">{number:02d}</span><b>第{number:02d}集 · {status}</b><small>{esc(detail)}</small></a>'
        )
    return "".join(cards)


def render_volume(
    number: int,
    report: dict[str, Any] | None,
    chapters: dict[str, dict[str, Any]],
) -> str:
    if report is None:
        return (
            f'<section class="volume pending-volume" id="vol-{number:02d}">'
            f'<div class="section-kicker">第{number:02d}集</div><h3>尚未入库</h3>'
            '<p class="muted">对应报告到达后，重新运行生成脚本即可纳入审查页。</p></section>'
        )
    if report.get("_load_error"):
        return (
            f'<section class="volume error-volume" id="vol-{number:02d}">'
            f'<div class="section-kicker">第{number:02d}集</div><h3>报告读取失败</h3>'
            f'<p>{esc(report.get("_file"))}：{esc(report.get("_load_error"))}</p></section>'
        )
    narrative, non_narrative = volume_counts(report, chapters)
    title = report.get("title") or f"第{number:02d}集"
    return (
        f'<section class="volume" id="vol-{number:02d}">'
        f'<div class="section-kicker">第{number:02d}集 · 已完成 · {narrative}章正文 · {non_narrative}个标题/章前</div>'
        f"<h3>{esc(title)}</h3>"
        f'<p class="overview">{esc(report.get("overview", "未填写本集概述。"))}</p>'
        '<details class="volume-block" open><summary>九维实质分析</summary>'
        f'<div class="dimension-list">{render_dimensions(report, chapters)}</div></details>'
        '<details class="volume-block"><summary>逐章观察</summary>'
        f'<div class="chapter-grid">{render_chapter_notes(report, chapters)}</div></details>'
        '<div class="volume-block"><h4>疑点与修订</h4>'
        f"{render_questions(report, chapters)}</div>"
        '<details class="volume-block raw-json"><summary>展开本集 JSON 主档</summary>'
        f'<pre>{esc(json.dumps({k: v for k, v in report.items() if not k.startswith("_")}, ensure_ascii=False, indent=2))}</pre>'
        "</details></section>"
    )


def source_asset(card: dict[str, Any]) -> bool:
    if card.get("source_id") == SOURCE_ID:
        return True
    evidence = card.get("evidence") or []
    return any(isinstance(item, dict) and item.get("source_id") == SOURCE_ID for item in evidence)


def volume_markers(value: Any) -> set[int]:
    found: set[int] = set()
    if isinstance(value, dict):
        explicit = value.get("volume")
        if isinstance(explicit, int) and 1 <= explicit <= VOLUME_COUNT:
            found.add(explicit)
        for key, item in value.items():
            found.update(volume_markers(key))
            found.update(volume_markers(item))
    elif isinstance(value, list):
        for item in value:
            found.update(volume_markers(item))
    elif isinstance(value, str):
        for match in re.finditer(r"第\s*0*(\d{1,2})\s*集", value):
            number = int(match.group(1))
            if 1 <= number <= VOLUME_COUNT:
                found.add(number)
    return found


def load_assets(vault: Path) -> list[dict[str, Any]]:
    assets = []
    for asset_type, folder in (("character", "characters"), ("scene", "scenes"), ("pattern", "patterns")):
        directory = vault / "library" / folder
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            try:
                card = read_json(path)
            except (OSError, UnicodeError, json.JSONDecodeError):
                continue
            if not isinstance(card, dict) or not source_asset(card):
                continue
            tags = card.get("tags") if isinstance(card.get("tags"), list) else []
            content = card.get("content") if isinstance(card.get("content"), dict) else {}
            volumes = volume_markers(tags) | volume_markers(content.get("volume_history"))
            assets.append(
                {
                    "asset_id": card.get("asset_id") or path.stem,
                    "asset_type": card.get("asset_type") or asset_type,
                    "title": card.get("title") or "未命名卡片",
                    "content": content,
                    "tags": tags,
                    "evidence": card.get("evidence") or [],
                    "revision": card.get("revision", ""),
                    "volumes": sorted(volumes),
                    "origin": "全书蒸馏" if volumes else "原有开篇样段",
                }
            )
    return assets


def render_synthesis(synthesis: dict[str, Any] | None, chapters: dict[str, dict[str, Any]]) -> str:
    if synthesis is None:
        return (
            '<section class="synthesis pending-synthesis" id="synthesis">'
            '<div class="section-kicker">全书综合</div><h2>全书九维综合尚未完成</h2>'
            '<p>逐集阅读完成后才会形成跨集判断；当前页面不会用未读内容补齐结论。</p></section>'
        )
    dimensions = synthesis.get("dimensions") if isinstance(synthesis.get("dimensions"), dict) else {}
    parts = []
    for key in DIMENSIONS:
        items = dimensions.get(key) or []
        if isinstance(items, dict):
            items = [items]
        rendered = "".join(render_dimension_item(item, chapters) for item in items if isinstance(item, dict))
        parts.append(
            f'<section class="dimension-group"><h3>{esc(DIMENSION_LABELS[key])}</h3>'
            f'{rendered or "<p class=\"muted\">未提供该维度综合。</p>"}</section>'
        )
    overview = synthesis.get("overview") or synthesis.get("summary") or "已载入全书综合。"
    stages = "".join(
        f'<article class="chapter-note"><h4>{esc(item.get("title", "阶段"))}</h4>'
        f'<p>{esc(item.get("summary", ""))}</p>{render_evidence(item.get("evidence"), chapters)}</article>'
        for item in synthesis.get("stages", []) if isinstance(item, dict)
    )
    arcs = "".join(
        f'<article class="chapter-note"><h4>{esc(item.get("name", "人物"))}</h4>'
        + "".join(f'<p><b>{label}：</b>{esc(item.get(key, ""))}</p>' for key, label in
                  [("initial", "起点"), ("turns", "转变"), ("ending", "终点"), ("unresolved", "边界")])
        + render_evidence(item.get("evidence"), chapters) + '</article>'
        for item in synthesis.get("character_arcs", []) if isinstance(item, dict)
    )
    focus = "".join(f'<li>{esc(item)}</li>' for item in synthesis.get("review_focus", []))
    extras = ((f'<details class="volume-block"><summary>主线阶段</summary><div class="chapter-grid">{stages}</div></details>' if stages else "")
              + (f'<details class="volume-block"><summary>主要人物弧</summary><div class="chapter-grid">{arcs}</div></details>' if arcs else "")
              + (f'<details class="volume-block"><summary>建议优先审查</summary><ul>{focus}</ul></details>' if focus else ""))
    return (
        '<section class="synthesis" id="synthesis"><div class="section-kicker">全书综合</div>'
        f'<h2>全书九维综合</h2><p class="overview">{esc(overview)}</p>{extras}'
        f'<div class="dimension-list">{"".join(parts)}</div>'
        '<details class="raw-json"><summary>展开全书综合 JSON 主档</summary>'
        f'<pre>{esc(json.dumps(synthesis, ensure_ascii=False, indent=2))}</pre></details></section>'
    )


def render_question_ledger(ledger: dict[str, Any] | None, chapters: dict[str, dict[str, Any]]) -> str:
    if ledger is None:
        return ""
    labels = {"answered": "已有答案", "partial": "部分回答", "open": "仍未回答", "text-uncertain": "文本待辨"}
    groups = []
    entries = ledger.get("entries", [])
    for state, label in labels.items():
        selected = [item for item in entries if isinstance(item, dict) and item.get("status") == state]
        rows = "".join(
            f'<article class="chapter-note"><div class="card-meta">{esc(item.get("id", ""))} · 原始问题第{esc(item.get("origin_volume", ""))}集</div>'
            f'<h4>{esc(item.get("question", ""))}</h4><p>{esc(item.get("answer", ""))}</p>'
            f'<p class="muted">{esc(item.get("revisit_focus", ""))}</p>'
            f'<details><summary>问题与结论的证据</summary><p>原问题</p>{render_evidence(item.get("origin_evidence"), chapters)}'
            f'<p>终点复核</p>{render_evidence(item.get("answer_evidence"), chapters)}</details></article>'
            for item in selected
        )
        groups.append(f'<details class="volume-block"><summary>{label}（{len(selected)}）</summary><div class="chapter-grid">{rows}</div></details>')
    return ('<section class="source-material" id="question-ledger"><div class="section-kicker">整书复核</div>'
            '<h2>疑点与回收清单</h2><p class="lead">保留问题首次出现时的证据，再列全书终点的回答与边界。文本待辨不等于已经证实的作者错误。</p>'
            + "".join(groups) + '</section>')


def relative_link(output: Path, target: Path) -> str:
    return Path(os.path.relpath(target, output.parent)).as_posix()


def build_html(vault: Path, output: Path) -> str:
    source_path = vault / "library" / "sources" / f"{SOURCE_ID}.json"
    if not source_path.exists():
        raise FileNotFoundError(f"缺少来源主档：{source_path}")
    source = read_json(source_path)
    chapters = chapter_map(source)
    report_dir = vault / "library" / "reports" / "super-skeleton"
    volumes = load_volumes(report_dir)
    synthesis_path = report_dir / "book-synthesis.json"
    synthesis = read_json(synthesis_path) if synthesis_path.exists() else None
    if synthesis is not None and not isinstance(synthesis, dict):
        raise ValueError(f"全书综合顶层必须是对象：{synthesis_path}")
    assets = load_assets(vault)
    complete = [item for item in volumes if item and not item.get("_load_error")]
    narrative_total = sum(volume_counts(item, chapters)[0] for item in complete)
    non_narrative_total = sum(volume_counts(item, chapters)[1] for item in complete)
    plot_target = vault / "library" / "views" / "plots" / f"{SOURCE_ID}-full-nine" / "index.html"
    plot_href = relative_link(output, plot_target)
    source_title = source.get("title") or BOOK_TITLE
    progress = render_progress(volumes, chapters)
    volume_sections = "".join(render_volume(i, report, chapters) for i, report in enumerate(volumes, 1))
    synthesis_html = render_synthesis(synthesis, chapters)
    ledger_path = report_dir / "question-ledger.json"
    ledger = read_json(ledger_path) if ledger_path.exists() else None
    ledger_html = render_question_ledger(ledger, chapters)
    complete_review = len(complete) == VOLUME_COUNT and synthesis is not None and ledger is not None
    introduction = ('18集研究、全书综合与疑点终审已整理完成。您可以先读综合报告，再按问题、人物或场景查看证据；收藏与个人评价由您决定。'
                    if complete_review else '页面呈现已入库的研究草稿，未入库报告与尚未形成的全书综合保留为空。研究审查通过与您的收藏、审阅决定分别记录。')
    ledger_nav = '<a href="#question-ledger">疑点回收</a>' if ledger else ''
    asset_payload = safe_script_json(assets)
    chapter_payload = safe_script_json({key: value.get("title", key) for key, value in chapters.items()})
    source_json = esc(json.dumps(source, ensure_ascii=False, indent=2))

    return rf'''<!doctype html>
<html lang="zh-CN" data-ready="true">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light">
<title>《超级骷髅兵》全书蒸馏审查</title>
<style>
:root{{--ink:#202521;--muted:#657067;--paper:#f6f2e8;--card:#fffdf7;--line:#d9d3c5;--green:#235f4a;--green-soft:#dce9df;--amber:#996519;--amber-soft:#f4e9cf;--red:#8b3b35;--shadow:0 9px 28px rgba(57,49,35,.08);font-family:"Microsoft YaHei","PingFang SC",system-ui,sans-serif;color:var(--ink);background:var(--paper);line-height:1.72}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;overflow-wrap:anywhere}}a{{color:inherit}}.page{{width:min(1180px,100%);margin:auto;padding:34px 26px 72px}}header{{padding:30px 0 24px;border-bottom:1px solid var(--line)}}.eyebrow,.section-kicker{{font-size:12px;letter-spacing:.15em;color:var(--green);font-weight:700}}h1{{font-family:serif;font-size:clamp(31px,6vw,58px);line-height:1.14;margin:10px 0 14px}}h2{{font-family:serif;font-size:clamp(25px,4vw,38px);line-height:1.25;margin:8px 0}}h3{{font-size:24px;line-height:1.35;margin:7px 0 13px}}h4{{font-size:17px;margin:7px 0}}p{{margin:.5em 0}}.lead{{max-width:820px;color:#4e5b52}}.metrics{{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}}.metric{{min-width:150px;padding:13px 16px;background:var(--card);border:1px solid var(--line);border-radius:12px}}.metric b{{display:block;font-size:23px;color:var(--green)}}.metric span,.muted,small{{color:var(--muted)}}nav{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}nav a,.plot-link{{text-decoration:none;border:1px solid var(--green);border-radius:999px;padding:8px 14px;color:var(--green);font-weight:700}}.plot-link{{display:inline-flex;margin-top:12px}}main>section{{margin-top:44px}}.progress-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:18px}}.progress-card{{display:grid;grid-template-columns:38px 1fr;text-decoration:none;border:1px solid var(--line);border-radius:12px;padding:13px;background:var(--card);box-shadow:var(--shadow)}}.progress-card.complete{{border-color:#94b5a0;background:#f3faf4}}.progress-card.pending{{background:#f2efe7;color:var(--muted)}}.progress-card.error{{border-color:#d3a6a2;background:#fff2f0}}.progress-card small{{grid-column:2}}.volume-number{{grid-row:1/3;font:700 19px/1 serif;color:var(--green);padding-top:3px}}.synthesis,.volume,.assets,.source-material{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:clamp(20px,4vw,38px);box-shadow:var(--shadow)}}.pending-synthesis,.pending-volume{{background:#f1eee5;box-shadow:none}}.error-volume{{border-color:#d3a6a2}}.overview{{max-width:900px;font-size:16px;color:#3f4b43}}.volume-block{{margin-top:18px;padding-top:16px;border-top:1px solid var(--line)}}details>summary{{cursor:pointer;color:var(--green);font-weight:700}}.dimension-list{{display:grid;gap:14px;margin-top:15px}}.dimension-group{{border-left:3px solid #9bb7a5;padding:5px 0 5px 18px}}.analysis-item{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 18px;margin:12px 0;padding:16px;border:1px solid #e4ded0;border-radius:10px;background:#fff}}.analysis-field b{{font-size:13px;color:var(--green)}}.analysis-field p{{font-size:14px}}.evidence{{grid-column:1/-1;border-top:1px dashed var(--line);padding-top:9px}}.evidence summary{{font-size:13px}}.evidence ul{{font-size:13px;color:var(--muted)}}.chapter-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:14px}}.chapter-note{{border:1px solid var(--line);border-radius:10px;padding:15px}}.card-meta{{font-size:12px;color:var(--muted)}}.review-columns{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}.review-columns>section{{min-width:0}}pre{{white-space:pre-wrap;word-break:break-word;background:#252a26;color:#f1f1e8;padding:18px;border-radius:10px;max-height:520px;overflow:auto;font:12px/1.55 Consolas,monospace}}.tools{{position:sticky;top:0;z-index:3;display:grid;grid-template-columns:minmax(180px,1fr) 170px 170px;gap:9px;padding:13px 0;background:rgba(246,242,232,.96)}}input,select{{width:100%;min-width:0;border:1px solid #aeb9af;background:#fff;color:var(--ink);border-radius:9px;padding:10px 12px;font:inherit;font-size:14px}}.asset-status{{font-size:13px;color:var(--muted);margin:5px 0 13px}}.asset-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}}.asset-card{{border:1px solid var(--line);border-radius:12px;padding:18px;background:#fff}}.badges{{display:flex;gap:6px;flex-wrap:wrap;margin:9px 0}}.badge{{font-size:12px;color:var(--green);background:var(--green-soft);border-radius:99px;padding:2px 8px}}.badge.origin{{color:var(--amber);background:var(--amber-soft)}}.asset-card dl{{margin:10px 0}}.asset-card dt{{font-size:13px;font-weight:700;color:var(--green);margin-top:9px}}.asset-card dd{{margin:2px 0;white-space:pre-line;font-size:14px;color:#445048}}.empty{{grid-column:1/-1;padding:24px;color:var(--muted)}}.source-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}}.source-grid details{{min-width:0;border:1px solid var(--line);border-radius:10px;padding:14px}}footer{{margin-top:42px;padding-top:20px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}}
@media(max-width:760px){{.page{{padding:22px 16px 54px}}.progress-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.analysis-item,.chapter-grid,.review-columns,.asset-grid,.source-grid{{grid-template-columns:1fr}}.tools{{position:static;grid-template-columns:1fr}}.synthesis,.volume,.assets,.source-material{{border-radius:13px}}}}
@media(max-width:430px){{.page{{padding-left:12px;padding-right:12px}}.progress-grid{{grid-template-columns:1fr}}.metrics{{display:grid;grid-template-columns:1fr 1fr}}.metric{{min-width:0;padding:10px}}h3{{font-size:21px}}.analysis-item{{padding:12px}}pre{{padding:12px}}}}
</style>
</head>
<body>
<div class="page">
<header>
<div class="eyebrow">本地资料库 · 全书蒸馏审查</div>
<h1>《超级骷髅兵》全书审查</h1>
<p class="lead">{esc(introduction)}</p>
<div class="metrics"><div class="metric"><b>{len(complete)} / {VOLUME_COUNT}</b><span>已完成集数</span></div><div class="metric"><b>{narrative_total}</b><span>已读正文章节</span></div><div class="metric"><b>{non_narrative_total}</b><span>标题／章前索引段</span></div><div class="metric"><b>{len(assets)}</b><span>本来源资产</span></div></div>
<nav><a href="#progress">阅读进度</a><a href="#synthesis">全书综合</a><a href="#dimensions">逐集九维</a>{ledger_nav}<a href="#assets">资料卡</a><a href="#source-material">来源材料</a></nav>
<a class="plot-link" id="plot-link" href="{esc(plot_href)}">打开主线／暗线图 ↗</a>
</header>
<main>
<section id="progress"><div class="section-kicker">覆盖范围</div><h2>18 集阅读进度</h2><div class="progress-grid">{progress}</div></section>
{synthesis_html}
{ledger_html}
<section id="dimensions"><div class="section-kicker">逐集报告</div><h2>逐集九维分析、疑点与修订</h2><div id="review-notes"><div id="dimension-evidence">{volume_sections}</div></div></section>
<section class="assets" id="assets"><div class="section-kicker">来源资产</div><h2>人物、场景与机制卡</h2><p class="lead">仅收录证据指向本书来源的卡片。原有开篇样段与带“第NN集”或逐集变化记录的全书蒸馏资产分开标识。</p>
<div class="tools"><input id="asset-search" aria-label="搜索资料卡" placeholder="搜索人物、场景、机制或内容"><select id="asset-type" aria-label="按类型筛选"><option value="">全部类型</option><option value="character">人物</option><option value="scene">场景</option><option value="pattern">机制</option></select><select id="asset-volume" aria-label="按集数筛选"><option value="">全部集数</option>{''.join(f'<option value="{i}">第{i:02d}集</option>' for i in range(1, VOLUME_COUNT + 1))}</select></div>
<div class="asset-status" id="asset-status" aria-live="polite"></div><div class="asset-grid" id="asset-cards"></div></section>
<section class="source-material" id="source-material"><div class="section-kicker">核对入口</div><h2>研究主档与证据索引</h2><p class="lead">来源主档记录版本、章节及行号；逐集研究JSON可在各集末尾展开。小说原文单独保存在本机，不包含在审查页中。</p><div class="source-grid"><details><summary>展开来源主档</summary><pre>{source_json}</pre></details></div></section>
</main>
<footer>离线审查副本 · 证据行号对应本机原书的固定版本。研究结论与您的创作偏好分别保存。</footer>
</div>
<script type="application/json" id="asset-data">{asset_payload}</script>
<script type="application/json" id="chapter-data">{chapter_payload}</script>
<script>
const assets=JSON.parse(document.getElementById('asset-data').textContent);
const chapterTitles=JSON.parse(document.getElementById('chapter-data').textContent);
const typeLabels={{character:'人物',scene:'场景',pattern:'机制'}};
const kindLabels={{fact:'事实',inference:'推断',synthesis:'机制抽象',plan:'计划'}};
const fieldLabels={safe_script_json(FIELD_LABELS)};
const escapeHtml=value=>String(value??'').replace(/[&<>"']/g,char=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[char]));
function textValue(value){{
  if(Array.isArray(value))return value.map((item,index)=>`${{index+1}}. ${{textValue(item)}}`).join('\n');
  if(value&&typeof value==='object')return Object.entries(value).map(([key,item])=>`${{fieldLabels[key]||'补充信息'}}：${{textValue(item)}}`).join('\n');
  return value??'';
}}
function evidenceHtml(items){{
  if(!Array.isArray(items)||!items.length)return '<p class="muted">未附章节证据。</p>';
  return `<details class="evidence"><summary>展开证据（${{items.length}} 条）</summary><ul>${{items.map(item=>{{const id=item.chapter_id||'未标章节';const title=chapterTitles[id]||id;const lines=item.start_line!=null&&item.end_line!=null?`第${{item.start_line}}–${{item.end_line}}行`:'未标行号';const kind=kindLabels[item.claim_kind]||item.claim_kind||'';return `<li>${{escapeHtml(title)}}（${{escapeHtml(id)}}） · ${{escapeHtml(lines)}}${{kind?' · '+escapeHtml(kind):''}}</li>`}}).join('')}}</ul></details>`;
}}
function renderAssets(){{
  const query=document.getElementById('asset-search').value.trim().toLocaleLowerCase();
  const type=document.getElementById('asset-type').value;
  const volume=Number(document.getElementById('asset-volume').value||0);
  const shown=assets.filter(asset=>(!type||asset.asset_type===type)&&(!volume||asset.volumes.includes(volume))&&(!query||JSON.stringify(asset).toLocaleLowerCase().includes(query)));
  document.getElementById('asset-status').textContent=`显示 ${{shown.length}} / ${{assets.length}} 张本来源卡片`;
  document.getElementById('asset-cards').innerHTML=shown.map(asset=>{{
    const fields=Object.entries(asset.content||{{}}).filter(([key])=>key!=='summary').map(([key,value])=>`<dt>${{escapeHtml(fieldLabels[key]||key)}}</dt><dd>${{escapeHtml(textValue(value))}}</dd>`).join('');
    const tags=(asset.tags||[]).map(tag=>`<span class="badge">${{escapeHtml(tag)}}</span>`).join('');
    const volumes=asset.volumes.map(item=>`<span class="badge">第${{String(item).padStart(2,'0')}}集</span>`).join('');
    return `<article class="asset-card"><div class="card-meta">${{escapeHtml(typeLabels[asset.asset_type]||asset.asset_type)}} · v${{escapeHtml(asset.revision)}}</div><h3>${{escapeHtml(asset.title)}}</h3><p>${{escapeHtml(asset.content?.summary||'未填写概述。')}}</p><div class="badges"><span class="badge origin">${{escapeHtml(asset.origin)}}</span>${{volumes}}${{tags}}</div><details><summary>展开分析与证据</summary><dl>${{fields}}</dl>${{evidenceHtml(asset.evidence)}}<details class="raw-json"><summary>展开卡片 JSON</summary><pre>${{escapeHtml(JSON.stringify(asset,null,2))}}</pre></details></details></article>`;
  }}).join('')||'<p class="empty">没有符合当前条件的卡片。</p>';
}}
for(const id of ['asset-search','asset-type','asset-volume'])document.getElementById(id).addEventListener('input',renderAssets);
renderAssets();
</script>
</body>
</html>'''


def parse_args() -> argparse.Namespace:
    location = Path(__file__).resolve()
    default_vault = next((p for p in location.parents if (p / "vault.json").is_file()),
                         location.parents[3] / "writing-vault")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, default=default_vault, help="资料库根目录")
    parser.add_argument("--output", type=Path, help="输出 HTML；默认写入资料库 library/views")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    vault = args.vault.resolve()
    output = (args.output or vault / "library" / "views" / f"{BOOK_TITLE}全书审查.html").resolve()
    rendered = build_html(vault, output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
