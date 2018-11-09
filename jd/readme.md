# 一. 使用方法

* Step 1：打开`.\NSD-jd-tm\jd\jdWare\jdWare\spiders\jdSpider`，根据需求修改line 14的keyword，该项含义为“搜索关键字”；
* Step 2：`cd`至`.\NSD-jd-tm\jd\jdWare`目录下；
* Step 3：`scrapy crawl jdSpider`。

# 二. 环境要求

* python 3；
* 安装scrapy；
* 安装mongodb，且mongod服务打开。

# 三. 字段说明

`NSD_JD`数据库下有三个**collections**：

**`SPU` collection**：

* `SPU_NUM`：产品编号（字符串）；
* `SPU_ID`：产品ID（字符串）；
* `SPU_TIT`：产品标题（字符串）；
* `SPU_DESP`：产品描述（数组）；
* `SPU_SPEC`：产品规格（数组）；
* `SPU_RATE`：产品口碑得分（浮点数）；
* `SPU_REVNUM`：页面显示总评论数（整数）；
* `SPU_TREVNUM`：排除默认评论后的实际评论数（整数）；


**`SKU` collection**：

* `SPU_NUM`：产品编号（字符串）；
* `SKU_ID`：版本ID（字符串）；
* `SKU_PRICEBF`：版本原价（浮点数）；
* `SKU_PRICEAF`：版本现价（浮点数）；
* `SKU_TIT`：版本分类（字符串）；


**`REVIEW` collection**：

* `SPU_NUM`：产品编号（字符串）；
* `SPU_TIT`：产品标题（字符串）；
* `U_NAME`：用户名称（字符串）；
* `U_LEVEL`：用户等级（字符串）
* `SKU_TIT`：购买的产品类型（字符串）；
* `REV_TIME`：评论时间（字符串）；
* `REV_CONTENT`：评论内容（字符串）；
* `REV_SCORE`：购买评价分数（整数）；
* `REV_PIC`：是否晒图（1为有图）；

# 四. 其他

* 每个关键字搜索结束，开始下一个关键字搜索后，商品的NUM又会从P1开始标注；
* 每个关键字搜索，最多搜索到75*100，即7500个结果；
* 评论部分，由于存在后期访问不稳定的原因，爬取到的评论并非全部评论，目前是按“多多益善”的原则，尽可能爬取多的评论。