#### 安装
```
# 注意PyFDF2的版本，2.3.0之后使用的方法名称不同
# 例如旧版为PdfFileReader，新版为PdfReader，本篇默认版本2.3.0及以上
pip install pypdf2
```
#### PDF 信息提取
```
from PyPDF2 import PdfReader
filepath = ""
with open(filepath, "rb+") as f:
    pdf = PdfReader(f)
    infomation = pdf.metadata
    print("文件信息：", infomation)
    number_of_pages = len(pdf.pages)
    print("pdf页数", number_of_pages)
```

#### PDF读写
```
from PyPDF2 import PdfReader, PdfWriter
# 基础PDF读对象
pdf_writer = PdfWriter()
# 基础PDF写对象
pdf_path = ""
pdf_reader = PdfReader(pdf_path)
```

#### 拆分PDF
```
# 每一页单独拆分
pdf_path = ""
save_path = ""
pdf_reader = PdfReader(pdf_path)
for i in range(0, pdf_reader.getNumPages()):
    pdf_writer = PdfWriter()
    pdf_writer.addPage(pdf_reader.getPage(i))
    # Every page write to a path
    with open(save_path + '{}.pdf'.format(str(i)), 'wb') as fh:
        pdf_writer.write(fh)

# 按照间隔拆分
def split_pdf(filename, filepath, save_dirpath, step=5):
    """
    拆分PDF为多个小的PDF文件，
    @param filename:文件名
    @param filepath:文件路径
    @param save_dirpath:保存小的PDF的文件路径
    @param step: 每step间隔的页面生成一个文件，例如step=5，表示0-4页、5-9页...为一个文件
    @return:
    """
    if not os.path.exists(save_dirpath):
        os.mkdir(save_dirpath)
    pdf_reader = PdfReader(filepath)
    # 读取每一页的数据
    pages = pdf_reader.getNumPages()
    for page in range(0, pages, step):
        pdf_writer = PdfWriter()
        # 拆分pdf，每 step 页的拆分为一个文件
        for index in range(page, page + step):
            if index < pages:
                pdf_writer.addPage(pdf_reader.getPage(index))
        # 保存拆分后的小文件
        save_path = os.path.join(save_dirpath, filename + str(int(page / step) + 1) + '.pdf')
        print(save_path)
        with open(save_path, "wb") as out:
            pdf_writer.write(out)
```

#### PDF加水印
```
from PyPDF2 import PdfReader, PdfWriter

watermark = '有水印的pdf路径'
input_pdf = '要加水印的路径'
output = '存放位置'

watermark_obj = PdfReader(watermark)
watermark_page = watermark_obj.getPage(0)

pdf_reader = PdfReader(input_pdf)
pdf_writer = PdfWriter()
# Watermark all the pages
for page in range(pdf_reader.getNumPages()):
    page = pdf_reader.getPage(page)
    page.merge_page(watermark_page)
    pdf_writer.add_page(page)
with open(output, 'wb') as out:
    pdf_writer.write(out)
```


#### 旋转pdf
```
from  PyPDF2 import PdfFileReader,PdfFileWriter
​
pdf_writer = PdfFileWriter()
pdf_reader = PdfFileReader(pdf_path)
# Rotate page 90 degrees to the right
page_1 = pdf_reader.getPage(0).rotateClockwise(90)
pdf_writer.addPage(page_1)
# Rotate page 90 degrees to the left
page_2 = pdf_reader.getPage(1).rotateCounterClockwise(90)
pdf_writer.addPage(page_2)
# 之后的正常写出
for i in range(2,pdf_reader.getNumPages()):
    pdf_writer.addPage(pdf_reader.getPage(i))
​
with open(pdf_path, 'wb') as fh:
     pdf_writer.write(fh)
```