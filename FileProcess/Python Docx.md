### 参考资料
* 关于python内open函数encoding编码问题
https://www.cnblogs.com/wangyi0419/p/11192593.html
* docx
  * Python docx书写的通用设置:https://blog.csdn.net/qq_40521970/article/details/122237166
  * python操作docx文档：https://www.cnblogs.com/wumingxiaoyao/p/8315814.html
  * 页眉和页脚（python-docx官方文档）:https://python-docx.readthedocs.io/en/latest/dev/analysis/features/header.html?highlight=footer
  * 浅谈python-docx的缩进问题——如何缩进两个字符:https://blog.csdn.net/weixin_47383889/article/details/119847787
  * python设置word页眉页脚:https://zhuanlan.zhihu.com/p/379924160 
* excel
  * python实现——处理Excel表格（超详细）: https://blog.csdn.net/weixin_44288604/article/details/120731317
* pdf
  * 总结python中可操作pdf的库：https://zhuanlan.zhihu.com/p/181377229
  * pdfminer读取pdf: https://www.cnblogs.com/wj-1314/p/9429816.html

### 技巧


### Bug
* cannot find reference “WD_ALIGN_PARAGRAPH” in “text.py”
```
import docx
.设置居中对齐
from docx.enum.text import WD_ALIGN_PARAGRAPH
p = file.add_paragraph()
p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run(‘而你在想我’)
# 把"WD_ALIGN_PARAGRAPH"替换成"WD_PARAGRAPH_ALIGNMENT"
```
