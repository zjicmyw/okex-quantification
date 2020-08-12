# OK API相关小脚本

---
## 功能介绍

根据okex交易所API实现的一系列功能如下

- 记录多个账户的持仓
- 记录期现套利溢价
- 记录暴涨暴跌
- 记录现货下单
- 记录期货下单
- 进行期货跟单
- 各类数据使用微信机器人查询
- 各类数据邮件提醒


## 目录说明
- ./utils :工具脚本 

	- email_send.py 发送邮件
	- ms_sql.py 数据库
	- tools.py 个人工具 

-  ./ok :okapi脚本 
	- account_record.py  定时记录几个账号的资金变化
	- ok_baodao.py 提醒期货开仓
	- spot_record 提醒现货BTC买入
	- straddle_info 记录ok期货出现溢价，提醒套利机会
	- skyrocketing_info 记录ok暴涨暴跌



## sql建表语句

- 发送邮件
```sql
  CREATE TABLE tab_send_email(
	[id] [int] IDENTITY(1,1) NOT NULL,
	address_to varchar(30) not null,
	mail_subject nvarchar(300) not null,
	mail_text nvarchar(1000) not null,
	type tinyint not null,
	create_time [datetime] NOT NULL  DEFAULT (getdate()),
	status bit default(1),
)
```
- 记录帐号相关信息：API/期货选择/张数
```sql

CREATE TABLE tab_accounts(
	[id] [int] IDENTITY(1,1) NOT NULL,
	[keyvalue] [varchar](50) NOT NULL,
	[api_key] [varchar](80) NOT NULL,
	[seceret_key] [varchar](80) NOT NULL,
	[passphrase] [varchar](80) NOT NULL,
	[order_instrument_id] [varchar](20) NULL,
	[order_size] [varchar](10) NULL,
	[status] [tinyint] NULL
)
```

- 记录几个账号的资金变化
```sql
  CREATE TABLE tab_okex_price_history(
    [id] [int] IDENTITY(1,1) NOT NULL,
    name varchar(10) not null,
    present float not null,
    this_week float not null,
    next_week float not null,
    quarter float not null,
    create_time [datetime] NOT NULL  DEFAULT (getdate()),
    status tinyint default(1),
)
CREATE TABLE tab_okex_account_swapbytoken(
    [id] [int] IDENTITY(1,1) NOT NULL,
    keyvalue varchar(50) not null,
    eos_equity float not null,
    bsv_equity float not null,
	tab_price_id int not null,
	eos_value float not null,
	bsv_value float not null,
	total_value float null,
    create_time [datetime] NOT NULL  DEFAULT (getdate()),
    status tinyint default(1),
)

CREATE TABLE tab_okex_account_swapbydoller(
    [id] [int] IDENTITY(1,1) NOT NULL,
    keyvalue varchar(50) not null,
    eos_usd_equity float not null,
    eth_usd_equity float not null,
	total_value float null,
    create_time [datetime] NOT NULL  DEFAULT (getdate()),
    status tinyint default(1),
)

CREATE TABLE tab_price(
    [id] [int] IDENTITY(1,1) NOT NULL,
    eos_price float not null,
    bsv_price float not null,
    create_time [datetime] NOT NULL  DEFAULT (getdate()),
)
```


- 记录量化的买入卖出策略
```sql
 CREATE TABLE tab_bd_buy(
	[id] [int] IDENTITY(1,1) NOT NULL,
	token varchar(10) not null,
	price float not null,
	[action] float not null,
	status bit not null default (1),
	create_time [datetime] NOT NULL  DEFAULT (getdate())
)
```

- 记录ok暴涨暴跌
```sql
   CREATE TABLE tab_minutes_price(
	[id] [int] IDENTITY(1,1) NOT NULL,
	token_price varchar(200) not null,
	create_time [datetime] NOT NULL  DEFAULT (getdate())
)
  CREATE TABLE tab_price_change(
	[id] [int] IDENTITY(1,1) NOT NULL,
	before_price float not null,
	now_price float not null,
	change float not null,
	status bit not null default (1),
	create_time [datetime] NOT NULL  DEFAULT (getdate())
)
```