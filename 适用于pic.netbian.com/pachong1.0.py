# 操作系统
import os
# 网络请求
try:
    import requests
except ImportError:
    input('检测到缺少必要的requests库，按回车键进行在线安装...')
    os.system('pip3 install requests')
# 时间模块
import time
# 系统控制
import sys
# 正则匹配
import re


# http://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=Pa%20chong
print('''
██████╗  █████╗      ██████╗██╗  ██╗ ██████╗ ███╗   ██╗ ██████╗ 
██╔══██╗██╔══██╗    ██╔════╝██║  ██║██╔═══██╗████╗  ██║██╔════╝ 
██████╔╝███████║    ██║     ███████║██║   ██║██╔██╗ ██║██║  ███╗
██╔═══╝ ██╔══██║    ██║     ██╔══██║██║   ██║██║╚██╗██║██║   ██║
██║     ██║  ██║    ╚██████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 

  https://pic.netbian.com 专用爬虫 by funnygeeker
''')

# 进度条，只是为了视觉效果
for i in range(1, 51):
    print("\r", end="")
    print(f"{i*2}%: ", "▋" * (i // 2), end="")
    sys.stdout.flush()
    time.sleep(0.01)

print('\n\n创建文件夹中...')

folder_name = 'image/'
# 判断文件夹是否存在
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

# 请求头 浏览器的身份标识（UA）
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
           }

img_type = input('''
请输入你要爬取的图片类别（数字）：
1.风景
2.美女
3.游戏
4.动漫
5.影视
6.汽车
7.动物
8.人物
9.美食
10.宗教
11.背景
12.手机壁纸

> ''')

img_dict = {'1': '4kfengjing', '2': '4kmeinv', '3': '4kyouxi', '4': '4kdongman', '5': '4kyingshi', '6': '4kqiche',
            '7': '4kdongwu', '8': '4krenwu', '9': '4kmeishi', '10': '4kzongjiao', '11': '4kbeijing', '12': 'shoujibizhi'}

# 判断文件夹是否存在，不存在则创建
if not os.path.exists(f'image/{img_dict[img_type]}'):
    os.mkdir(f'image/{img_dict[img_type]}')

start_pages = int(input('''
请输入你要爬取的开始页数（数字）：
> '''))

end_pages = int(input('''
请输入你要爬取的结束页数（数字）：
> '''))
end_pages += 1  # 由于调用了range函数，所以在此加1

# 遍历所有页数
for page in range(start_pages, end_pages):
    page_folder_name = f'image/{img_dict[img_type]}/{page}'
    # 判断文件夹是否存在，不存在则创建
    if not os.path.exists(page_folder_name):
        os.mkdir(page_folder_name)

    # 针对此网页特殊情况做处理
    if page == 1:
        page_file_name = ''
    else:
        page_file_name = f'index_{page}.html'

    # 拿到网页的源码地址
    url = f'https://pic.netbian.com/{img_dict[img_type]}/{page_file_name}'

    # 发送请求
    response = requests.get(url=url, headers=headers)

    # 网页源码
    image_urls = re.findall(
        'target="_blank"><img src="(.*?)" alt="', response.text)
    # print(image_urls)

    print(f'\n当前页数：{page}，状态码：{response.status_code}，图片总数：{len(image_urls)}\n')

    # enumerate函数 输出index和数据  index是索引  int类型
    for index, image_url in enumerate(image_urls):
        if image_url[0] == '/':
            image_url = f'https://pic.netbian.com{image_url}'
        index += 1  # 不然你还想看 张数：0，总数20 ？
        # 对图片的请求地址发送请求
        print(f'张数：{index}，总数{len(image_urls)}，图片地址：{image_url}')
        response = requests.get(url=image_url, headers=headers)
        print(f'状态码：{response.status_code}，尝试保存中...')

        # 拿到图片的信息
        image = response.content

        # 通过链接读取文件扩展名
        file_name_extension = image_url.split('.')[-1]
        print('---------------', file_name_extension, '---------------')

        # 将图片保存到本地
        with open(f'{os.getcwd()}/{page_folder_name}/{index}.{file_name_extension}', 'wb') as file:
            file.write(image)

input('\n操作完成，按回车键关闭...')
