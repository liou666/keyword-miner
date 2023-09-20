import core.wb as wb
import core.xhs as xhs

import tools.prompt as prompt

if __name__ == '__main__':

    platform = prompt.select(
        "🐞 选择要爬取的平台?",
        choices=["all", "小红书", "微博"],
    )
    
    keyName = prompt.input("📖 输入要检索的关键字",validate=lambda x: True if x.strip() != "" else "请输入要检索的关键字")
    pageSize = prompt.input("🤔️ 输入要抓取的数据量",validate=lambda x: True if x.isdigit() and x.strip() != "" else "请输入一个有效数字")

    if(keyName=="" or pageSize==""): exit()
    
    if platform=="all":
        xhs.start(keyName,pageSize)
        wb.start(keyName,pageSize)
    if platform=="小红书":
        xhs.start(keyName,pageSize)
    if platform=="微博":
        wb.start(keyName,pageSize)

    
