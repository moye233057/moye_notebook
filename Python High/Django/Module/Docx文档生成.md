#### 论文中英文摘要格式
```
# 设置基本格式
doc = Document(demo_path)
doc.styles["Normal"].font.name = u'宋体'
doc.styles["Normal"].font.size = Pt(12)
doc.styles["Normal"]._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
# 写入中文摘要及关键词部分
tit1 = doc.add_paragraph()
tit1.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
tit1_run = tit1.add_run('摘要')
tit1_run.bold = True
para = doc.add_paragraph()
para.paragraph_format.line_spacing = 1.5
zh_abs = zh_abs.split('\n')
for abs in zh_abs:
    para.add_run('    ' + abs + '\n')
para.add_run('    关键词：' + zh_keyword + '\n').bold = True
# 写入英文摘要及关键词部分
# Times New Roman
para_len = len(doc.paragraphs)
doc.paragraphs[para_len - 1].runs[1].add_break(enum.text.WD_BREAK.PAGE)
tit2 = doc.add_paragraph()
tit2.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
tit2_run = tit2.add_run('Abstract')
tit2_run.bold = True
para = doc.add_paragraph()
para.paragraph_format.line_spacing = 1.5

en_abs = en_abs.split('\n')
for abs in en_abs:
    run = para.add_run('    ' + abs + '\n')
    run.font.name = u'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), u'Times New Roman')

run = para.add_run('    Keywords: ' + en_keyword + '\n')
run.bold = True
run.font.name = u'Times New Roman'
run._element.rPr.rFonts.set(qn('w:eastAsia'), u'Times New Roman')
```