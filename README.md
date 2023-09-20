
1、每日晚将金线股股票code提取放入code.txt文件中
1.1、 执行jingxian.py 中的record_start,先记录每日的金线股基础信息
1.2、 第二日盘后执行jingxian.py 中的record_end,记录每日的金线股收盘信息，计算收益
1.3、再将code清空导入当日新的金线股code

2、每日收盘执行task.py的方法清空盘中记录文件

3、每3天更新一次股票板块概念信息，执行ticket.py 中的

4、每天重启通达信软件