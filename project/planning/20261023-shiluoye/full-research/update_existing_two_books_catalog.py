"""依据既有正式全书检查点刷新蜗牛双书目录，保留旧研究入口。"""
import json,pathlib,runpy
root=pathlib.Path(__file__).resolve().parents[3]
vault=root/'writing-vault';folder=vault/'library/reports/collection'
path=folder/'catalog-config.json';config=json.loads(path.read_text(encoding='utf-8'))
for sid,key,slug,count in [
 ('src-359a2bd5a60747038b12a7ba483a5f80','l','leveling',387),
 ('src-2d8a13f33737429da512e5cc9e839712','z','zeidan',463)]:
    run=json.loads((vault/f'exchanges/runs/run-full-two-books-20261025-{key}.json').read_text(encoding='utf-8'))
    assert run['source_id']==sid and run['state']=='full-source-read-and-distilled'
    assert run['actual_reading_units']==count and not run['pending_chapters']
    assert run['terminal_question_audit'] and len(run['dimensions'])==9
    report=vault/f'library/reports/two-books-full-20261025/{slug}/README.md'
    assert report.exists()
    book=config['books'][sid]
    old=book.get('report');extras=book.setdefault('additional_reports',[])
    if old and old!=f'../two-books-full-20261025/{slug}/README.md' and not any(e['path']==old for e in extras):
        extras.append({'title':'保留的旧研究入口','path':old})
    book.update(task_state='completed_full_nine',report=f'../two-books-full-20261025/{slug}/README.md',
        note=f'既有双书任务已完成{count}个实际阅读单元的全书九维、人物与问题终态核验；由正式检查点及专题验收证明。本轮仅刷新统一管理入口，不宣称重新阅读；旧试读和迁移记录保留。')
path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
runpy.run_path(str(folder/'rebuild_catalog.py'))['main']()
