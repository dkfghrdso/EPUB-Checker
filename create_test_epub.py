from ebooklib import epub
import os

def create_test_epub():
    """创建一个测试用的EPUB文件"""
    # 创建EPUB书籍对象
    book = epub.EpubBook()
    
    # 设置书籍元数据
    book.set_identifier('test-book-123')
    book.set_title('测试小说')
    book.set_language('zh-CN')
    book.add_author('测试作者')
    
    # 创建章节内容
    chapter1_content = '''第1章 开始

这是测试小说的第一章内容。

故事发生在一个遥远的地方，那里有美丽的风景和善良的人们。

主角是一个年轻的冒险者，他即将踏上一段充满挑战的旅程。

在旅途中，他会遇到各种困难和危险，但他也会结识许多朋友。

经过长时间的跋涉，他终于来到了目的地附近。

这里的景色让他感到惊叹，他知道自己的冒险才刚刚开始。

第一章结束。'''
    
    chapter2_content = '''第2章 冒险

这是测试小说的第二章内容。

主角进入了一片神秘的森林，这里充满了未知的危险。

他小心翼翼地前进，时刻保持警惕。

突然，他听到了奇怪的声音，似乎有什么东西在跟踪他。

他加快了脚步，试图摆脱追踪者。

经过一番追逐，他终于安全地离开了森林。

但他知道，更大的挑战还在后面等着他。

第二章结束。'''
    
    chapter3_content = '''第3章 挑战

这是测试小说的第三章内容。

主角来到了一座古老的城堡前，这里就是他的目的地。

城堡看起来非常神秘，充满了历史的气息。

他推开沉重的大门，走进了城堡内部。

城堡里空无一人，但他能感觉到有什么东西在注视着他。

他继续深入，终于找到了他一直在寻找的宝藏。

但就在他准备拿走宝藏的时候，城堡开始摇晃起来。

他必须尽快离开这里，否则就会被困在里面。

第三章结束。'''
    
    chapter4_content = '''第4章 后续

这是测试小说的第四章内容，这个章节不会被检查工具显示。

主角成功地逃出了城堡，带着宝藏回到了家乡。

他的冒险故事成为了当地的传说，激励着更多的人去探索未知的世界。

故事到这里就结束了，但主角的传奇还在继续。

第四章结束。'''
    
    # 创建EPUB章节对象
    c1 = epub.EpubHtml(title='第1章 开始', file_name='chap_01.html', lang='zh-CN')
    c1.content = '<html><body><h1>第1章 开始</h1><p>' + chapter1_content.replace('\n', '</p><p>') + '</p></body></html>'
    
    c2 = epub.EpubHtml(title='第2章 冒险', file_name='chap_02.html', lang='zh-CN')
    c2.content = '<html><body><h1>第2章 冒险</h1><p>' + chapter2_content.replace('\n', '</p><p>') + '</p></body></html>'
    
    c3 = epub.EpubHtml(title='第3章 挑战', file_name='chap_03.html', lang='zh-CN')
    c3.content = '<html><body><h1>第3章 挑战</h1><p>' + chapter3_content.replace('\n', '</p><p>') + '</p></body></html>'
    
    c4 = epub.EpubHtml(title='第4章 后续', file_name='chap_04.html', lang='zh-CN')
    c4.content = '<html><body><h1>第4章 后续</h1><p>' + chapter4_content.replace('\n', '</p><p>') + '</p></body></html>'
    
    # 添加章节到书籍
    book.add_item(c1)
    book.add_item(c2)
    book.add_item(c3)
    book.add_item(c4)
    
    # 创建目录
    book.toc = (epub.Link('chap_01.html', '第1章 开始', 'chap1'),
                epub.Link('chap_02.html', '第2章 冒险', 'chap2'),
                epub.Link('chap_03.html', '第3章 挑战', 'chap3'),
                epub.Link('chap_04.html', '第4章 后续', 'chap4'))
    
    # 添加导航文件
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # 设置书脊
    book.spine = ['nav', c1, c2, c3, c4]
    
    # 保存EPUB文件
    output_path = os.path.join('test_books', 'test_novel.epub')
    epub.write_epub(output_path, book, {})
    
    print(f"测试EPUB文件已创建: {output_path}")

if __name__ == "__main__":
    create_test_epub()
