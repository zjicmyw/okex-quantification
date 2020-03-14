# OK API相关小脚本

---

## common文件夹:基础脚本 

- email_send.py 发送邮件
- ms_sql.py 数据库
- tools.py 个人工具 

##  ok文件夹:okapi脚本 
- ok510.py  定时记录几个账号的资金变化
- ok_baodao.py 提醒期货开仓
- ok_bd2 提醒现货BTC买入
- straddle 记录ok期货出现溢价，提醒套利机会
- ok_skyrocketing 记录ok暴涨暴跌



## sql建表语句

- 发送邮件
```
  CREATE TABLE tab_send_email(
	[id] [int] IDENTITY(1,1) NOT NULL,
	address_to varchar(30) not null,
	mail_subject nvarchar(300) not null,
	mail_text nvarchar(500) not null,
	type tinyint not null,
	create_time [datetime] NOT NULL  DEFAULT (getdate()),
	status bit default(1),
)
```

- 记录几个账号的资金
```
  CREATE TABLE tab_okex_price_history(
    [id] [int] IDENTITY(1,1) NOT NULL,
    name varchar(10) not null,
    present float not null,
    this_week float not null,
    next_week float not null,
    quarter float not null,
    create_time [datetime] NOT NULL  DEFAULT (getdate()),
    status bit default(1),
)
```

- 记录okb的买入卖出策略
```
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
```
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