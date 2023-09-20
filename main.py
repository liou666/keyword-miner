import core.wb as wb
import core.xhs as xhs
import tools.logger as logger

if __name__ == '__main__':
    platform = logger.choices("🐞 选择要爬取的平台",["all","小红书", "微博"],"all")
    keyName = ""
    pageSize= "20"

    while True:
        keyName = logger.ask("📖 输入要检索的关键字")
        if keyName.strip() != "":  break
   
    while True:
      pageSize = logger.ask("🤔️ 输入要抓取的数据量")
      if (pageSize.strip().isdigit() and pageSize.strip() != ""): break


    if platform=="all":
        xhs.start(keyName,pageSize)
        wb.start(keyName,pageSize)
    if platform=="小红书":
        xhs.start(keyName,pageSize)
    if platform=="微博":
        wb.start(keyName,pageSize)

    
