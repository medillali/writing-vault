const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { pathToFileURL } = require('url');
const { chromium } = require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const here = __dirname;
const fixture = path.join(here, 'ui-fixture');
const vault = path.join(fixture, 'vault');
const sourceId = 'src-9ff09c395734410b856f77c77a652834';
const revision = 'fixture-revision';
const output = path.join(fixture, 'review.html');
const python = 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';

function writeJson(relativePath, value) {
  const target = path.join(vault, relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, JSON.stringify(value, null, 2), 'utf8');
}

function buildFixture() {
  fs.mkdirSync(path.join(vault, 'library', 'reports', 'super-skeleton'), { recursive: true });
  writeJson(`library/sources/${sourceId}.json`, {
    source_id: sourceId,
    title: '《超级骷髅兵》原创合成审查样本',
    revision,
    revisions: [{
      revision,
      characters: 321,
      line_count: 30,
      chapters: [
        { chapter_id: 'ch-0001', title: '章前内容', start_line: 1, end_line: 2 },
        { chapter_id: 'ch-0002', title: '第一集 黄金骷髅', start_line: 3, end_line: 3 },
        { chapter_id: 'ch-0003', title: '第一章 合成正文', start_line: 4, end_line: 30 },
      ],
    }],
  });
  const raw = path.join(vault, 'private-sources', 'normalized', 'sources', sourceId, `${revision}.txt`);
  fs.mkdirSync(path.dirname(raw), { recursive: true });
  fs.writeFileSync(raw, 'PRIVATE_MANUSCRIPT_SENTINEL_20261022\n章前内容\n合成说明\n第一集 黄金骷髅\n第一章 合成正文\n仅用于界面验证。\n', 'utf8');
  const evidence = [{ source_id: sourceId, revision, chapter_id: 'ch-0003', start_line: 4, end_line: 8, claim_kind: 'fact' }];
  const dimension = {
    claim: '恶意字符串 <img src=x onerror="window.__xss=1"> 只能作为文字显示',
    mechanism: '用角色选择制造因果推进',
    application: '迁移时保留选择与代价的对应关系',
    limitation: '证据不足时不得外推',
    claim_kind: 'inference',
    evidence: evidence.map(({ chapter_id, start_line, end_line }) => ({ chapter_id, start_line, end_line })),
  };
  const dimensions = Object.fromEntries([
    'worldbuilding', 'characters', 'plot', 'style', 'narrative', 'dialogue', 'pacing', 'themes', 'continuity',
  ].map((key) => [key, [{ ...dimension, claim: `${key}：${dimension.claim}` }]]));
  writeJson('library/reports/super-skeleton/vol01.json', {
    volume: 1,
    title: '第一集 <script>window.__xss=2</script> 黄金骷髅',
    source_id: sourceId,
    revision,
    read_parts: [1],
    chapter_ids: ['ch-0001', 'ch-0002', 'ch-0003'],
    overview: '本集通过一个完整选择链展示角色目标、阻碍与后果，合成内容仅用于验证界面。',
    chapter_notes: [
      { chapter_id: 'ch-0001', observation: '章前内容，非叙事。', dimensions_checked: [] },
      { chapter_id: 'ch-0002', observation: '集标题，非叙事。', dimensions_checked: [] },
      { chapter_id: 'ch-0003', observation: '正文观察：角色承担选择后果。', dimensions_checked: Object.keys(dimensions) },
    ],
    dimensions,
    characters: [{ name: '样本角色', aliases: [], summary: '用于筛选测试的新增人物。', goal: '完成选择', conflict: '证据边界', arc_change: '犹豫到行动', relationships: [], knowledge_limits: '不知道后文', evidence }],
    scenes: [{ key: 'v01-s01', title: '样本场景', summary: '角色在阻碍中选择。', goal: '前进', obstacle: '风险', choice: '行动', consequence: '付出代价', state_change: '局势变化', why_it_works: '因果清晰', applicability: '转折场景', failure_mode: '代价虚假时失效', evidence }],
    patterns: [{ key: 'v01-p01', title: '样本机制', summary: '用选择展示价值。', steps: ['设定目标', '施加阻碍', '兑现代价'], applicability: '人物转折', failure_mode: '缺少铺垫时失效', scene_keys: ['v01-s01'], evidence }],
    events: [], edges: [], threads: [],
    questions: [{ question: '该线索是否会在后文回收？', reason: '当前只读到第一集。', evidence }],
    revisions_to_earlier: [{ description: '合成样本修订：前序判断需要收窄。', evidence }],
  });
  writeJson('library/characters/chr-original.json', {
    asset_id: 'chr-original', asset_type: 'character', title: '原有样段人物', source_id: sourceId,
    content: { summary: '原有开篇样段资产。' }, tags: ['开篇样段'], evidence, revision: 1,
  });
  writeJson('library/characters/chr-new.json', {
    asset_id: 'chr-new', asset_type: 'character', title: '第01集新增人物',
    content: { summary: '全书蒸馏新增资产。', volume_history: [{ volume: 1, note: '第01集变化' }] },
    tags: ['第01集', '全书蒸馏'], evidence, revision: 2,
  });
  writeJson('library/scenes/scn-new.json', {
    asset_id: 'scn-new', asset_type: 'scene', title: '可检索针线场景',
    content: { summary: '搜索关键字：蓝铜针。', volume_history: { '第01集': '建立场景' } },
    tags: ['第01集'], evidence, revision: 1,
  });
  writeJson('library/patterns/pat-new.json', {
    asset_id: 'pat-new', asset_type: 'pattern', title: '第02集未来机制',
    content: { summary: '未读卷资产不应被错归第一集。' }, tags: ['第02集'], evidence, revision: 1,
  });
  writeJson('library/characters/chr-foreign.json', {
    asset_id: 'chr-foreign', asset_type: 'character', title: '其他来源人物',
    content: { summary: '不得混入。' }, tags: ['第01集'],
    evidence: [{ ...evidence[0], source_id: 'src-other' }], revision: 1,
  });
}

async function main() {
  buildFixture();
  const generated = spawnSync(python, ['-X', 'utf8', path.join(here, 'build_review.py'), '--vault', vault, '--output', output], { encoding: 'utf8' });
  assert.strictEqual(generated.status, 0, `生成失败：\n${generated.stdout}\n${generated.stderr}`);
  assert(fs.existsSync(output), '未生成审查页');
  const html = fs.readFileSync(output, 'utf8');
  assert(!html.includes('PRIVATE_MANUSCRIPT_SENTINEL_20261022'), '审查页不得嵌入原文');
  assert(!html.includes('private-sources'), '审查页不得嵌入原文路径');
  const rawFile = path.join(vault, 'private-sources', 'normalized', 'sources', sourceId, `${revision}.txt`);
  // 只删除隔离样本的确切文件，确认生成器不依赖原文在场。
  assert(rawFile.startsWith(fixture + path.sep));
  fs.unlinkSync(rawFile);
  const withoutRaw = spawnSync(python, ['-X', 'utf8', path.join(here, 'build_review.py'), '--vault', vault, '--output', output], { encoding: 'utf8' });
  assert.strictEqual(withoutRaw.status, 0, '没有原文时应照常生成研究审查页');
  assert.strictEqual(fs.readFileSync(output, 'utf8'), html, '原文有无不应改变生成内容');
  assert(!/https?:\/\//i.test(html), '审查页源码不得包含外部请求地址');
  assert(!html.includes('<script>window.__xss=2</script>'), 'JSON/HTML 字段没有严格转义');

  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const remoteRequests = [];
    page.on('request', (request) => {
      if (/^https?:/i.test(request.url())) remoteRequests.push(request.url());
    });
    await page.goto(pathToFileURL(output).href);
    await page.waitForSelector('[data-ready="true"]');

  assert.strictEqual(await page.locator('[data-volume]').count(), 18, '必须显示 18 集进度');
  assert.match(await page.locator('[data-volume="1"]').innerText(), /已完成/);
  assert.match(await page.locator('[data-volume="1"]').innerText(), /1\s*章正文/);
  assert.match(await page.locator('[data-volume="1"]').innerText(), /2\s*个标题\/章前/);
  assert.match(await page.locator('[data-volume="2"]').innerText(), /尚未入库/);
  assert.match(await page.locator('#synthesis').innerText(), /尚未完成/);
  assert.match(await page.locator('#dimensions').innerText(), /机制/);
  assert.match(await page.locator('#dimensions').innerText(), /迁移/);
  assert.match(await page.locator('#dimensions').innerText(), /边界/);
  assert.match(await page.locator('#review-notes').innerText(), /疑点/);
  assert.match(await page.locator('#review-notes').innerText(), /修订/);

  const firstEvidence = page.locator('#dimension-evidence details.evidence').first();
  await firstEvidence.click();
  assert.match(await firstEvidence.innerText(), /ch-0003/);

  assert.strictEqual(await page.locator('#asset-cards .asset-card').count(), 4, '应排除其他来源资产');
  assert.match(await page.locator('#asset-cards').innerText(), /原有样段人物/);
  assert.match(await page.locator('#asset-cards').innerText(), /第01集新增人物/);
  assert(!((await page.locator('#asset-cards').innerText()).includes('其他来源人物')));
  const evolvedCard = page.locator('#asset-cards .asset-card').filter({ hasText: '第01集新增人物' });
  await evolvedCard.locator('details').first().click();
  const evolvedText = await evolvedCard.innerText();
  assert.match(evolvedText, /逐集变化/);
  assert(!evolvedText.includes('"volume"'), 'volume_history 不应以开发字段形式展示');
  await page.selectOption('#asset-type', 'scene');
  assert.strictEqual(await page.locator('#asset-cards .asset-card').count(), 1, '类型筛选失败');
  await page.selectOption('#asset-type', '');
  await page.selectOption('#asset-volume', '1');
  assert.strictEqual(await page.locator('#asset-cards .asset-card').count(), 2, '集数筛选应匹配 tags 与 volume_history');
  await page.selectOption('#asset-volume', '');
  await page.fill('#asset-search', '蓝铜针');
  assert.strictEqual(await page.locator('#asset-cards .asset-card').count(), 1, '搜索筛选失败');
  assert.match(await page.locator('#asset-cards').innerText(), /可检索针线场景/);

  assert.strictEqual(await page.locator('img').count(), 0, '恶意 HTML 被解释为元素');
  assert.strictEqual(await page.evaluate(() => window.__xss), undefined, '恶意脚本被执行');
  assert.strictEqual(remoteRequests.length, 0, '页面发起了外部请求');
  assert.strictEqual(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth), true, '390px 出现页面横向溢出');
  assert.match(await page.locator('#source-material').innerText(), /来源主档/);
  assert.match(await page.locator('#source-material').innerText(), /研究主档与证据索引/);
  const graphHref = await page.locator('#plot-link').getAttribute('href');
    assert(graphHref.replace(/\\/g, '/').endsWith('library/views/plots/src-9ff09c395734410b856f77c77a652834-full-nine/index.html'), '图入口路径错误');
  } finally {
    await browser.close();
  }
  console.log('PASS: 18集进度、正文/标题计数、九维证据、综合占位、卡片筛选、来源隔离、XSS转义、离线请求与390px布局均通过。');
}

main().catch((error) => {
  console.error(error.stack || error);
  process.exitCode = 1;
});
