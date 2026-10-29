# 本卷元数据准备交接

卷7；210正文，含卷标题211原片段；范围`ch-1294—ch-1504`，印刷正文1286—1495。

**状态：prepared_unread，正文、标题和原片段实际已读均0。** 没有打开normalized或调用读章器。

来源与阅读单元映射已按正式登记核对；`assignment.json`固定全部指定ID，`reader-state.json`、`read-log.json`空账，`chapter-notes.jsonl`为空。

保存器`save_notes.py --check`只核元数据/已有账；`--batch`默认因reading_authorized=false拒绝保存。以后主代理明确启动后，在assignment和state同时解除metadata_only并记start_authorization_reference，再按全文实际提供观察。不要为测试伪造已读记录。

批次JSON顶层需source_id/revision/volume/reader/observations；每条提供chapter_id、facts/inferences/state_changes/unresolved数组，model_full_text_read=true、begin_marker_seen=true、end_marker_seen=true、end_marker精确匹配、unresolved_truncation=false。保存器拒重复、越卷、错修订和不连续输入；本身不读取正文。

续读先读本卷state与前卷handoff；未读前史明确标派生/未知，不能把纵横或其他书同名人物命运倒灌。本代理顺序卷五→卷七，单卷交付八类产物后再换卷，不写正式库。

当前只完成隔离准备，不运行check_volume/import_volume、不伪造研究包；启动后仍须实际读全卷标题和正文全部片段才满足覆盖。
