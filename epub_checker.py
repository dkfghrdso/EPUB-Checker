import os
import sys
from ebooklib import epub
from bs4 import BeautifulSoup
import glob

def get_chapter_content(item):
    """从epub item中提取纯文本内容"""
    content = item.get_content().decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    # 移除脚本和样式
    for script in soup(['script', 'style']):
        script.extract()
    # 获取纯文本
    text = soup.get_text()
    # 清理空白字符
    text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
    return text

def get_chapters(book):
    """从epub书中提取章节"""
    chapters = []
    
    for item in book.get_items():
        item_type = item.get_type()
        item_name = item.get_name()
        
        # 检查是否为HTML或XHTML文件（类型9表示HTML内容）
        if item_type == 9 and (item_name.endswith('.html') or item_name.endswith('.xhtml')):
            try:
                content = item.get_content().decode('utf-8', errors='ignore')
                if len(content) > 100:
                    chapters.append((item_name, get_chapter_content(item)))
            except Exception as e:
                continue
    
    # 按文件名排序章节
    chapters.sort(key=lambda x: x[0])
    return chapters

def check_epub_chapters(epub_path, num_chapters=3):
    """检查epub文件的前三章末尾"""
    print(f"\n=== 检查文件: {os.path.basename(epub_path)} ===")
    
    try:
        # 打开epub文件
        book = epub.read_epub(epub_path)
        
        # 获取所有章节
        chapters = get_chapters(book)
        
        if not chapters:
            print("未找到章节")
            return False
        
        # 只检查前三章
        chapters_to_check = chapters[:num_chapters]
        
        # 检查是否所有章节末尾都包含指定链接
        all_chapters_have_link = True
        
        for i, (title, content) in enumerate(chapters_to_check, 1):
            print(f"\n--- 第{i}章: {title} ---")
            
            if not content:
                print("章节内容为空")
                all_chapters_have_link = False
                continue
            
            # 获取章节末尾内容（最后1000个字符）
            end_content = content[-1000:]
            
            # 检查是否包含指定链接
            import re
            target_pattern = r'https?://github\.com'
            
            # 处理可能的特殊字符和编码问题
            cleaned_end = end_content.encode('ascii', 'ignore').decode('ascii')
            
            # 使用正则表达式检查链接
            if re.search(target_pattern, cleaned_end, re.IGNORECASE):
                print("✓ 章节末尾包含GitHub链接")
            else:
                print("✗ 章节末尾缺少GitHub链接")
                all_chapters_have_link = False
            
            print("章节末尾内容:")
            print("=" * 50)
            print(end_content)
            print("=" * 50)
            print(f"章节总长度: {len(content)} 字符")
            
        return all_chapters_have_link
        
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return False

def main(directory):
    """主函数，遍历目录中的所有epub文件"""
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        sys.exit(1)
    
    # 查找所有epub文件
    epub_files = glob.glob(os.path.join(directory, '*.epub'))
    
    if not epub_files:
        print(f"在目录 '{directory}' 中未找到epub文件")
        sys.exit(1)
    
    print(f"找到 {len(epub_files)} 个epub文件")
    
    # 处理每个epub文件
    for epub_file in epub_files:
        # 检查文件是否所有章节都包含指定链接
        all_chapters_have_link = check_epub_chapters(epub_file)
        
        # 获取文件所在目录和文件名
        file_dir = os.path.dirname(epub_file)
        file_name = os.path.basename(epub_file)
        
        # 检查文件名是否已经被标注
        is_already_marked = "[缺少链接]" in file_name
        
        if not all_chapters_have_link and not is_already_marked:
            # 重命名文件，添加标注
            new_file_name = "[缺少链接]" + file_name
            new_file_path = os.path.join(file_dir, new_file_name)
            
            try:
                os.rename(epub_file, new_file_path)
                print(f"\n✓ 文件已重命名为: {new_file_name}")
            except Exception as e:
                print(f"\n✗ 重命名文件失败: {str(e)}")
        elif all_chapters_have_link and is_already_marked:
            # 如果文件已经被标注但现在符合要求，移除标注
            new_file_name = file_name.replace("[缺少链接]", "")
            new_file_path = os.path.join(file_dir, new_file_name)
            
            try:
                os.rename(epub_file, new_file_path)
                print(f"\n✓ 文件已移除标注: {new_file_name}")
            except Exception as e:
                print(f"\n✗ 重命名文件失败: {str(e)}")

if __name__ == "__main__":
    # 硬编码test_books路径，只检查该文件夹中的小说
    directory = "test_books"
    print(f"正在检查 {directory} 文件夹中的小说...")
    main(directory)
