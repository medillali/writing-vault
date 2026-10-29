from save_focus_manual import P,A,read,write,sha
f=A/'focused-findings-part01.json';items=read(f);assert isinstance(items,list)
write(P/'unsubmitted-self-check/focus01-before-container-wrap.json',items)
b=read(P/'input-receipt.json');write(f,dict(source_id=b['source_id'],revision=items[0]['evidence'][0]['revision'],status='draft-pending-actual-primary-review',formal_input_sha256=b['formal_input_sha256'],findings=items))
assert read(f)['findings']==items
write(P/'focus01-container-wrap-receipt.json',{'change':'list原8对象逐值不变，仅加顶层元数据/findings包装','findings_identical':True,'count':len(items),'after_sha256':sha(f)})
print(sha(f))
