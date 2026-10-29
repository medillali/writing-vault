from pathlib import Path
import urllib.request,json,hashlib,base64,tarfile,io
root=Path(__file__).resolve().parents[3]
out=root/'writing-vault/library/reports/super-skeleton/map/vendor'
m=json.load(urllib.request.urlopen('https://registry.npmjs.org/openseadragon/6.1.1'))
assert m['repository']['url']=='git+https://github.com/openseadragon/openseadragon.git'
raw=urllib.request.urlopen(m['dist']['tarball']).read()
assert 'sha512-'+base64.b64encode(hashlib.sha512(raw).digest()).decode()==m['dist']['integrity']
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tar:
    names=tar.getnames()
    js=next(n for n in names if n.endswith('/build/openseadragon/openseadragon.min.js'))
    lic=next(n for n in names if n.lower().endswith(('/license.txt','/license')))
    out.mkdir(parents=True,exist_ok=True)
    (out/'openseadragon.min.js').write_bytes(tar.extractfile(js).read())
    (out/'LICENSE.txt').write_bytes(tar.extractfile(lic).read())
    (out/'source.json').write_text(json.dumps({'name':m['name'],'version':m['version'],'license':m['license'],'repository':m['repository']['url'],'tarball':m['dist']['tarball'],'integrity':m['dist']['integrity'],'js_sha256':hashlib.sha256((out/'openseadragon.min.js').read_bytes()).hexdigest()},indent=2)+'\n')
print('OpenSeadragon 6.1.1 verified and saved')
