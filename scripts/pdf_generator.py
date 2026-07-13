"""
K12英语试卷PDF生成脚本
依赖：pip install weasyprint markdown
"""
import markdown
from weasyprint import HTML, CSS
import os

def generate_exam_pdf(markdown_text: str, output_dir: str = "./output"):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 拆分试卷、答题卡、答案解析
    parts = markdown_text.split("## 答题卡")
    exam_main = parts[0]
    rest = parts[1].split("## 答案与解析")
    answer_sheet = rest[0]
    analysis = rest[1] if len(rest) > 1 else ""

    # 标准打印CSS（A4纸，符合公立校试卷排版）
    print_css = CSS(string="""
        @page {
            size: A4;
            margin: 2cm 1.5cm;
            @top-center {
                content: "XX年级英语试卷";
                font-size: 12px;
                color: #333;
            }
            @bottom-center {
                content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
                font-size: 10px;
                color: #666;
            }
        }
        body {
            font-family: "SimSun", "宋体", serif;
            font-size: 14px;
            line-height: 1.6;
        }
        h1 {
            text-align: center;
            font-size: 22px;
            margin-bottom: 10px;
        }
        h2 {
            font-size: 16px;
            margin-top: 20px;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
        }
        .question {
            margin: 10px 0;
        }
        .options {
            margin-left: 20px;
        }
        .answer-blank {
            border-bottom: 1px solid #000;
            display: inline-block;
            width: 100px;
            margin: 0 5px;
        }
    """)

    # 转换为HTML
    def md_to_html(md_content):
        return markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # 生成三个PDF文件
    HTML(string=md_to_html(exam_main)).write_pdf(
        os.path.join(output_dir, "试卷正文.pdf"),
        stylesheets=[print_css]
    )
    HTML(string=md_to_html("## 答题卡\n" + answer_sheet)).write_pdf(
        os.path.join(output_dir, "答题卡.pdf"),
        stylesheets=[print_css]
    )
    if analysis:
        HTML(string=md_to_html("## 答案与解析\n" + analysis)).write_pdf(
            os.path.join(output_dir, "答案解析.pdf"),
            stylesheets=[print_css]
        )

    print(f"PDF生成完成，文件已保存至 {output_dir} 目录")

if __name__ == "__main__":
    # 示例调用
    with open("exam.md", "r", encoding="utf-8") as f:
        md_content = f.read()
    generate_exam_pdf(md_content)
