# 全书问题审计入口

两池保留原schema与标识；分类未知不等于作者未回收，条目总数不等于伏笔总数。

主代理已逐项审阅；用户评价仍为draft。JSON是两池索引，不合并其schema。

| 池 | 条数 | 可读页 | 原始JSON |
|---|---:|---|---|
| 历史问题与图线程 | 105 | [历史池](audit/whole-book/historical-question-pool.md) | [JSON](audit/whole-book/historical-question-pool.json) |
| 分卷原子问题 | 404 | [原子池](audit/whole-book/local-question-pool.md) | [JSON](audit/whole-book/local-question-pool.json) |

[终点线程叠加](audit/whole-book/terminal-thread-overlay.md) · [27项聚焦终态审计](audit/whole-book/end-state-audit-draft.md) · [审计验收凭据](audit/whole-book/publication-receipt.json)

## 历史池分类

| 分类轴 | 类别 | 数量 |
|---|---|---:|
| terminal_statuses | answered | 58 |
| terminal_statuses | partial | 37 |
| terminal_statuses | unknown | 10 |
| entry_types | analysis.open_questions | 16 |
| entry_types | graph.threads | 89 |
| audit_domains | not-classified-in-pool | 105 |

## 原子池分类

| 分类轴 | 类别 | 数量 |
|---|---|---:|
| terminal_statuses | answered | 44 |
| terminal_statuses | partial | 78 |
| terminal_statuses | unknown | 282 |
| entry_types | local-atomic-item | 404 |
| audit_domains | aggregate-versus-individual-death | 1 |
| audit_domains | aggregate-versus-personal-payment | 2 |
| audit_domains | character-knowledge | 1 |
| audit_domains | conditional-ability-and-gift | 1 |
| audit_domains | conflicting-testimony | 1 |
| audit_domains | culprit-attribution | 1 |
| audit_domains | culprit-inference | 1 |
| audit_domains | defeat-versus-life-state | 1 |
| audit_domains | earlier-event-cross-reference | 1 |
| audit_domains | earlier-story-reference | 1 |
| audit_domains | family-status-and-transaction | 1 |
| audit_domains | health-and-knowledge | 1 |
| audit_domains | item-state-and-unconfirmed-person-fate | 1 |
| audit_domains | knowledge-boundary | 1 |
| audit_domains | knowledge-continuity | 1 |
| audit_domains | listing-versus-cash | 1 |
| audit_domains | motive-inference | 1 |
| audit_domains | narrator-motive-and-memory | 1 |
| audit_domains | plot-or-character | 122 |
| audit_domains | plot-plus-source-clock | 1 |
| audit_domains | prediction-versus-result | 1 |
| audit_domains | promise-and-transaction | 1 |
| audit_domains | qualification-versus-use | 1 |
| audit_domains | quest-plus-item-qualification | 1 |
| audit_domains | reported-past-and-later-choice | 1 |
| audit_domains | result-plus-unmeasured-clock | 1 |
| audit_domains | scope-and-denominator | 1 |
| audit_domains | source-anomaly-plus-promise | 1 |
| audit_domains | source-time-and-reported-economy | 1 |
| audit_domains | source_anomaly | 168 |
| audit_domains | specific-exit-and-property | 1 |
| audit_domains | specific-gifts-and-inventory-continuity | 1 |
| audit_domains | specific-quest-delivery | 1 |
| audit_domains | specific-scene-and-unproven-skill-generalization | 1 |
| audit_domains | stage-knowledge-or-source-boundary | 80 |
| audit_domains | unconfirmed-person-fates | 1 |
