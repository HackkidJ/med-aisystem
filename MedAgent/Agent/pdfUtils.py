import PyPDF2
import os

def split_pdf():
    # 输入PDF文件路径
    pdf_path = "MedAgent\\knowledges\\pdfs\\医学教材\\外科学\\外科学.pdf"

    # 检查文件是否存在
    if not os.path.exists(pdf_path):
        print("文件不存在，请检查路径是否正确")
        return
    
    try:
        # 打开PDF文件
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            print(f"PDF总页数: {total_pages}")
            
            while True:
                # 输入页码范围
                page_range = input("请输入页码范围 (如: 1-5)，输入q退出: ").strip()
                if page_range.lower() == 'q':
                    break
                
                # 输入文件名
                filename = input("请输入保存的文件名 (不需要.pdf后缀): ").strip()
                
                try:
                    # 解析页码范围
                    start_page, end_page = map(int, page_range.split('-'))
                    start_page = max(1, start_page) - 1  # 转换为0-based索引
                    end_page = min(total_pages, end_page)
                    
                    if start_page >= end_page:
                        print("页码范围无效")
                        continue
                    
                    # 创建PDF写入器
                    pdf_writer = PyPDF2.PdfWriter()
                    
                    # 添加指定页面
                    for page_num in range(start_page, end_page):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                    
                    # 保存文件
                    output_path = f"{filename}.pdf"
                    with open(output_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                    
                    print(f"成功保存: {output_path}")
                    
                except ValueError:
                    print("页码范围格式错误，请使用'起始页-结束页'的格式")
                except Exception as e:
                    print(f"处理过程中出现错误: {e}")
                    
    except Exception as e:
        print(f"读取PDF文件时出现错误: {e}")

if __name__ == "__main__":
    split_pdf()