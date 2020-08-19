#  DMP-Phase02设计文档

[TOC]

## 数据库设计

*除特殊情况外一律不使用外键，使用关联表*

### 数据表名统一前缀

​	 `dmp_`

### 数据 **表** 通用字段（**关联表除外**）

| 字段                | 数据类型 | 限制                       | 介绍                     |
| ------------------- | -------- | -------------------------- | ------------------------ |
| id                  | int      | 主键，自增，非重复         | ID主键，具体含义见对应表 |
| created_on          | Datetime | 非空，default:datetime.now | 创建时间                 |
| changed_on          | Datetime | 非空，default:datetime.now | 最后修改时间             |
| created_dmp_user_id | int      | 非空                       | 创建人                   |
| changed_dmp_user_id | int      |                            | 修改人                   |

### 数据看板 表
无前缀表名：`dashboard`

| 字段                           | 数据类型     | 限制               | 介绍                  |
| ------------------------------ | ------------ | ------------------ | --------------------- |
| id                             | int          | 主键，自增，非重复 | 看板ID                |
| dmp_dashboard_name             | varchar(50)  | 非空，唯一         | 数据看板名称          |
| description                    | varchar(400) |                    | 备注，简介            |
| release                        | tinyint      | 默认值0            | 是否发布，0否1是2下线 |
| charts_position                | text         |                    | 图表布局数据          |
| upper_dmp_dashboard_archive_id | int          |                    | 文件夹ID              |

### 数据看板文件夹 表

无前缀表名： `dashboard_archive`

| 字段                           | 数据类型    | 限制               | 介绍                     |
| ------------------------------ | ----------- | ------------------ | ------------------------ |
| id                             | int         | 主键，自增，非重复 | ID主键，具体含义见对应表 |
| dashboard_archive_name         | varchar(50) | 非空，唯一         | 文件夹名称               |
| upper_dmp_dashboard_archive_id | int         |                    | 文件夹ID                 |

### 看板用户收藏 关联表

无前缀表名：`dashboard_star`

| 字段             | 数据类型 | 限制 | 介绍   |
| ---------------- | -------- | ---- | ------ |
| dmp_user_id      | int      | 非空 | 用户ID |
| dmp_dashboard_id | int      | 非空 | 看板ID |

### 文件夹用户收藏 关联表

无前缀表名：`archive_star`

| 字段           | 数据类型 | 限制 | 介绍     |
| -------------- | -------- | ---- | -------- |
| dmp_user_id    | int      | 非空 | 用户ID   |
| dmp_archive_id | int      | 非空 | 文件夹ID |



### 图表 表

无前缀表名：`chart`

| 字段              | 数据类型     | 限制               | 介绍                                              |
| ----------------- | ------------ | ------------------ | ------------------------------------------------- |
| id                | int          | 主键，自增，非重复 | ID主键，具体含义见对应表                          |
| chart_name        | carchar(64)  | 非空               | 图表名称                                          |
| dmp_data_table_id | int          | 非空               | 数据表ID                                          |
| query_string      | text         | 非空               | 查询语句                                          |
| chart_data        | text         | 非空               | 数据                                              |
| chart_type        | int          | 非空               | 图表类型，柱状图1，折线图2，饼图3，地图4，雷达图5 |
| params            | text         | 非空               | 图表参数                                          |
| update_interval   | int          | 非空，默认0        | 时间间隔时间                                      |
| update_unit       | int          | 非空，默认0        | 时间间隔单位，0小时，1日，3周                     |
| description       | varchar(512) |                    | 简介                                              |
| dmp_dashboard_id  | int          | 非空               | 数据看板ID                                        |

### 主页看板用户 关联表

无前缀表名：`user_index_dashboard`

| 字段             | 数据类型 | 限制 | 介绍   |
| ---------------- | -------- | ---- | ------ |
| dmp_user_id      | int      | 非空 | 用户ID |
| dmp_dashboard_id | int      | 非空 | 看板ID |



### 已保存查询 表

无前缀表名：`saved_query`

| 字段              | 数据类型     | 限制               | 介绍                     |
| ----------------- | ------------ | ------------------ | ------------------------ |
| id                | int          | 主键，自增，非重复 | ID主键，具体含义见对应表 |
| query_name        | varchar(50)  | 非空               | 查询语句的保存名称       |
| query_sql         | text         | 非空               | 查询语句                 |
| description       | varchar(400) |                    | 备注                     |
| dmp_data_table_id | int          | 非空               | 数据表ID                 |
| dmp_case_id       | int          | 非空               | 所属案例ID               |
|                   |              |                    |                          |

### 数据服务 表

无前缀表名：`data_service`

| 字段                  | 数据类型     | 限制               | 介绍                     |
| --------------------- | ------------ | ------------------ | ------------------------ |
| id                    | int          | 主键，自增，非重复 | ID主键，具体含义见对应表 |
| data_service_name     | varchar(64)  | 非空               | 数据服务名称             |
| request_method        | int          | default:1          | 请求方法，1GET 2POST     |
| api_path              | varchar(255) | 非空，唯一         | API地址                  |
| source_dmp_data_table | int          | 非空               | 数据表ID                 |
| query_sql             | text         |                    | 查询语句，mysql必须项    |
| query_params          | text         |                    | 查询参数，mongodb必须项  |
| state                 | tinyint      | default:0          | 是否启用                 |
| description           | varchar(512) |                    | 服务简介                 |



### 数据服务参数 表

*无需通用字段*

无前缀表名：`data_service_parameter`

| 字段                | 数据类型     | 限制               | 介绍                               |
| ------------------- | ------------ | ------------------ | ---------------------------------- |
| id                  | int          | 主键，自增，非重复 | ID主键，具体含义见对应表           |
| dmp_data_service_id | int          | 非空               | 数服务ID                           |
| parameter_name      | varchar(100) | 非空               | 参数名（要进行筛选的字段名）       |
| type                | varchar(50)  | default ： "-"     | 参数类型。取决于源数据表的类型定义 |
| required_parameter  | tinyint      | default :  0       | 是否为必填项                       |
| description         | varchar(400) |                    | 简介                               |



### 用户服务访问 关联表

无前缀表名：`user_data_service`

| 字段                | 数据类型 | 限制                 | 介绍       |
| ------------------- | -------- | -------------------- | ---------- |
| dmp_user_id         | int      | 非空                 | 用户ID     |
| dmp_data_service_id | int      | 非空                 | 数据服务ID |
| access_time         | datetime | default:datetime.now | 访问时间   |



### [中文表名]

无前缀表名：`[tablename]`

| 字段 | 数据类型 | 限制               | 介绍                     |
| ---- | -------- | ------------------ | ------------------------ |
| id   | int      | 主键，自增，非重复 | ID主键，具体含义见对应表 |
|      |          |                    |                          |



## 接口设计

### 说明

#### 响应状态码

| status | msg               | info                                 |
| ------ | ----------------- | ------------------------------------ |
| 0      | success           | 响应成功                             |
| 101    | invalid_params    | 参数错误                             |
| 201    | Invalid_token     | 无效的Token或Token过期               |
| 301    | permission_denied | 权限不足                             |
| 4404   |                   | 数据表不存在或在操作期间被删除       |
| 7101   |                   | 文件夹不存在或在操作期间被删除       |
| 7201   |                   | 看板不存在或在操作期间被删除         |
| 7301   |                   | 图表不存在或在操作期间被删除         |
| 7401   |                   | 数据服务不存在或在操作期间被删除     |
| 7501   |                   | 数据服务参数不存在或在操作期间被删除 |
| 8101   |                   | 缺少秘钥                             |
| 8102   |                   | 秘钥无效或已失效                     |
| 8104   |                   | 数据服务不存在或已被删除             |
| 8015   |                   | 数据服务参数错误                     |
| 999    | unknow_error      | 未知错误                             |



#### 返回值固有字段

| 参数名  | 类型           | 参数说明   |
| ------- | -------------- | ---------- |
| status  | Int            | 状态码     |
| msg     | string         | 状态码信息 |
| results | Dict/ArrayList | 返回值     |

------------------

### *获取看板及文件夹列表信息

**接口描述**

1.  解析headers信息获取当前用户ID；
2.  接受参数并进行校验，校验失败，返回状态码201
3.  根据接收到的过滤条件，将文件夹表和看板表进行联合查询并将结果返回

**请求说明**

| URL           | /bi/dashboards |
| ------------- | -------------- |
| 格式          | JSON           |
| http 请求方式 | GET            |
| 登陆保护      | 是             |

 **请求参数**

| 参数名                         | 类型   | 是否必填 | 最大长度 | 参数说明                      |
| ------------------------------ | ------ | -------- | -------- | ----------------------------- |
| upper_dmp_dashboard_archive_id | int    | 否       | -        | 父文件夹ID                    |
| is_owner                       | bool   | 是       |          | 是否是我的，默认否            |
| state                          | int    | 否       |          | 发布状态0未发布1已发布2已下线 |
| name                           | string | 否       | 64       | 看板名或者用户名              |
| pagenum                        | int    | 是       |          | 页码默认为1                   |
| pagesize                       | int    | 是       |          | 每页内容数量，默认10          |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
      count:123,
      pagesize:10,
      pagenum:2,
      data:[
          {
            "type":"archive",
            "id":1,
            "name":"dashboard_archive_name",
            "upper_dmp_dashboard_archive_id":null,
            "release":null,
            "description":"简介",
            "created_on":"2020-08-08 12:33:33",
            "changed_on":"2020-08-08 12:33:33",
            "created_dmp_user_id":1,
            "changed_dmp_user_id":2,
            "upper_dmp_dashboard_archive_name":null,
            "created_dmp_user_name":"admin",
            "changed_dmp_user_name":"user02",
          },
          {
              "type":"dashboard",
              "id":1,
              "name":"dashboard01",
              "description":"简介",
              "release":-1,
              "upper_dmp_dashboard_archive_id":1,
              "upper_dmp_dashboard_archive_name":null,
              "created_on":"2020-08-11 12:00:00",
              "changed_on":"2020-08-11 12:00:00",
              "created_dmp_user_id":1,
              "changed_dmp_user_id":1,
              "created_dmp_user_name":"admin",
              "changed_dmp_user_name":"admin"
          }
          ...
      ]
  }
}
```

**result说明:**

| 参数名                           | 类型   | 参数说明               |
| -------------------------------- | ------ | ---------------------- |
| count                            | int    | 文件夹总数             |
| pagesize                         | int    | 该次响应返回的内容数量 |
| pagenum                          | int    | 当前页码               |
| type | string | dashboard 看板  archive   文件夹 |
| id                               | int    | 文件夹或看板ID          |
| name           | string | 文件夹或看板名称          |
| upper_dmp_dashboard_archive_id   | int    | 所属文件夹ID           |
| upper_dmp_dashboard_archive_name | string | 所属文件夹名称         |
| description                    | string | 文件夹或看板简介   |
| release                        | int    | 看板发布状态， |
| created_on                       | string | 创建日期的字符串       |
| changed_on                       | string | 修改日期的字符串       |
| created_dmp_user_id              | int    | 创建人ID               |
| created_dmp_user_name            | string | 创建人名称             |
| changed_dmp_user_id              | int    | 最后修改人ID           |
| changed_dmp_user_name            | string | 最后修改人名称         |

-------------

### 创建文件夹

**接口描述**

1.   解析headers信息获取当前用户ID；
2.  根据接收请求参数获取文件夹名称，及父文件夹ID（非必须项），进行字段校验若失败成功否则返回状态码【101】；
3.   若果有父文件夹ID，要判断父文件夹是不是自己的
4.   将文件夹信息添加到数据表内。

**请求说明**

| URL           | /bi/archives |
| ------------- | ------------ |
| 格式          | JSON         |
| http 请求方式 | POST         |
| 登陆保护      | 是           |

 **请求参数**

| 参数名                         | 类型   | 是否必填 | 最大长度 | 参数说明     |
| ------------------------------ | ------ | -------- | -------- | ------------ |
| dashboard_archive_name         | string | 是       | 50       | 文件夹名称   |
| upper_dmp_dashboard_archive_id | int    | 否       |          | 父文件夹名称 |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{"res":"OK!"}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |
----------------------

### 修改文件夹信息

**接口描述**

1.  解析headers信息获取当前用户ID；
2.  根据URL参数获取要修改的文件夹ID，根据ID判断当前文件夹是否存在否则返回错误码【7101】
3.  根据接收请求文件夹名称，进行字段校验若失败返回状态码【101】；
4.  判断用户为文件夹用户否则返回错误码【301】；
5.  对文件夹信息对应的数据库信息进行修改。

**请求说明**

| URL           | `/bi/archives/<id:int`> |
| ------------- | ----------------------- |
| 格式          | JSON                    |
| http 请求方式 | POST                    |
| 登陆保护      | 是                      |

 **请求参数**

| 参数名                 | 类型   | 是否必填 | 最大长度 | 参数说明                      |
| ---------------------- | ------ | -------- | -------- | ----------------------------- |
| id                     | int    | 是       |          | URL参数，要进行修改的文件夹ID |
| dashboard_archive_name | string | 是       | 50       | 修改之后的文件夹名称          |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{"res":"OK"}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |
### 删除文件夹

**接口描述**

1.  解析headers信息获取当前用户ID；
2.  根据URL参数获取要删除的文件夹ID，进行字段校验若失败返回状态码【101】；
3.  判断用户为超级管理员或自己否则返回错误码【301】；
4.  根据ID判断当前文件夹是否存在否则返回错误码【7101】;
5.  对文件夹信息对应的数据库信息及该文件夹下的内容进行删除。

**请求说明**

| URL           | `/bi/archives/<id:int>` |
| ------------- | ----------------------- |
| 格式          | JSON                    |
| http 请求方式 | DELETE                  |
| 登陆保护      | 是                      |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明           |
| ------ | ---- | -------- | -------- | ------------------ |
| id     | int  | 是       | -        | 要删除的文件夹的ID |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |

### 获取单一数据看板信息

**接口描述**

1.  根据URL参数取得要获取的看板的ID，如果不存在返回错误【101】；
2.   根据看板ID判断该看板是否存在，如果不存在返回错误【7201】；
3.  查询该看板信息，进行返回

**请求说明**

| URL           | `/bi/dashboards/<id:int>` |
| ------------- | ------------------------- |
| 格式          | JSON                      |
| http 请求方式 | GET                       |
| 登陆保护      | 是                        |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明      |
| ------ | ---- | -------- | -------- | ------------- |
| id     | int  | 是       | -        | URL参数看板ID |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
      "id":1,
      "dmp_dashboard_name":"dashboard01",
      "description":"简介",
      "release":-1,
      "charts_position":"{...}",
      "upper_dmp_dashboard_archive_id":1,
      "created_on":"2020-08-11 12:00:00",
      "changed_on":"2020-08-11 12:00:00",
      "created_dmp_user_id":1,
      "changed_dmp_user_id":1,
      "created_dmp_user_name":"admin",
      "changed_dmp_user_name":"admin"
  }
}
```

**result说明:**

| 参数名                         | 类型   | 参数说明       |
| ------------------------------ | ------ | -------------- |
| id                             | int    | 看板ID         |
| dmp_dashboard_name             | string | 看板名称       |
| description                    | string | 看板简介       |
| release                        | int    | 看板发布状态   |
| charts_position                | string | 图表布局数据   |
| upper_dmp_dashboard_archive_id | int    | 父文件夹ID     |
| created_on                     | string | 创建时间       |
| changed_on                     | string | 最后修改时间   |
| created_dmp_user_id            | int    | 创建人ID       |
| changed_dmp_user_id            | int    | 最后修改人ID   |
| created_dmp_user_name          | string | 创建人名称     |
| changed_dmp_user_name          | string | 最后修改人名称 |

### 创建看板

**接口描述**

**接口描述**

1.   解析headers信息获取当前用户ID，若解析失败返回状态码【201】；

2.  根据接收请求参数获取看板名称名称，简介及父文件夹ID（非必须项），进行字段校验若失败成功否则返回状态码【101】；
3.  将看板信息添加到数据表内。


**请求说明**

| URL           | /bi/dashboards |
| ------------- | -------------- |
| 格式          | JSON           |
| http 请求方式 | POST           |
| 登陆保护      | 是             |

 **请求参数**

| 参数名                         | 类型   | 是否必填 | 最大长度 | 参数说明     |
| ------------------------------ | ------ | -------- | -------- | ------------ |
| dmp_dashboard_name             | string | 是       | 50       | 看板名称     |
| //description                  | string | 否       | 400      | 简介         |
| upper_dmp_dashboard_archive_id | int    | 否       |          | 父文件夹ID   |
| charts_position                | string | 否       | 65535    | 图表布局信息 |
|                                |        |          |          |              |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |

### 修改看板

**接口描述**

1.   解析headers信息获取当前用户ID，若解析失败返回状态码【201】；
2.  根据URL参数获取看板ID，根据请求参数获取其他要进行修改的信息，进行字段校验，若失败返回状态码【101】;
3.  判断用户为自己否则返回状态码【301】；
4.  根据ID进行判断当前看板是否存在，若不存在返回状态码【7201】
5.  对看板信息更新到数据库。


**请求说明**

| URL           | `/bi/dashboards/<id:int>` |
| ------------- | ------------------------- |
| 格式          | JSON                      |
| http 请求方式 | PUT                       |
| 登陆保护      | 是                        |



 **请求参数**

| 参数名                         | 类型   | 是否必填 | 最大长度 | 参数说明     |
| ------------------------------ | ------ | -------- | -------- | ------------ |
| id                             | int    | 是       | -        | 看板ID       |
| dmp_dashboard_name             | string | 否       | 50       | 看板名称     |
| description                    | string | 否       | 400      | 简介         |
| upper_dmp_dashboard_archive_id | int    | 否       | -        | 父文件夹ID   |
| charts_position                | string | 否       | 65535    | 图表布局信息 |
| release                        | int    | 否       |          | 发布状态     |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 删除看板

**接口描述**

1.  解析headers信息获取当前用户ID；
2.  根据URL参数获取要删除看板ID，进行字段校验若失败返回状态码【101】；
3.  判断用户为管理员类用户或者为创建者的Leader用户否则返回错误码【301】；
4.  根据ID判断当前看板是否存在否则返回错误码【7101】;
5.  对对应的看板数据库信息进行删除。


**请求说明**

| URL           | `/bi/dashboards/<id:int>` |
| ------------- | ------------------------- |
| 格式          | JSON                      |
| http 请求方式 | DELETE                    |
| 登陆保护      | 是                        |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明       |
| ------ | ---- | -------- | -------- | -------------- |
| id     | int  | 是       | -        | 要删除的看板ID |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 添加图表接口

**接口描述**

1.   解析headers信息获取当前用户ID，若解析失败返回状态码【201】；

2.   根据接收请求参数获取图表相关信息，进行字段校验若失败成功否则返回状态码【101】；
3.   将图表信息添加到数据库内。


**请求说明**

| URL           | /bi/charts |
| ------------- | ---------- |
| 格式          | JSON       |
| http 请求方式 | POST       |
| 登陆保护      | 是         |

 **请求参数**

| 参数名            | 类型   | 是否必填 | 最大长度 | 参数说明                                              |
| ----------------- | ------ | -------- | -------- | ----------------------------------------------------- |
| chart_name        | string | 是       | 50       | 图表名称                                              |
| dmp_data_table_id | int    | -        |          | 数据源表ID                                            |
| query_string      | string | -        |          | 查询语句                                              |
| chart_data        | string | -        |          | 图表数据                                              |
| chart_type        | int    | 是       |          | 图表类型代码，柱状图1，折线图2，饼图3，地图4，雷达图5 |
| chart_params      | string | -        |          | 图表参数                                              |
| description       | string | -        |          | 图表简介                                              |
| dmp_dashboard_id  | int    | 是       |          | 数据看板ID                                            |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |

### 修改图表

**接口描述**

1.   解析headers信息获取当前用户ID，若解析失败返回状态码【201】；
2.   根据URL参数获取图表ID，根据请求参数获取其他要进行修改的信息，进行字段校验，若失败返回状态码【101】;
3.   判断用户为管理员类用户或者为创建者的Leader用户否则返回状态码【301】；
4.   根据ID进行判断当前图表是否存在，若不存在返回状态码【7301】
5.   对图表信息更新到数据库。


**请求说明**

| URL           | `/bi/charts/<chart_id:int>` |
| ------------- | --------------------------- |
| 格式          | JSON                        |
| http 请求方式 | PUT                         |
| 登陆保护      | 是                          |

**请求参数**

| 参数名            | 类型   | 是否必填 | 最大长度 | 参数说明                                              |
| ----------------- | ------ | -------- | -------- | ----------------------------------------------------- |
| chart_name        | string | 是       | 50       | 图表名称                                              |
| dmp_data_table_id | int    | -        |          | 数据源表ID                                            |
| query_string      | string | -        |          | 查询语句                                              |
| chart_data        | string | -        |          | 图表数据                                              |
| chart_type        | int    | -        |          | 图表类型代码，柱状图1，折线图2，饼图3，地图4，雷达图5 |
| chart_params      | string | -        |          | 图标参数                                              |
| description       | string | -        |          | 图表简介                                              |
| dmp_dashboard_id  | int    | -        |          | 数据看板ID                                            |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -·       |

### 数据查询接口

**接口描述**

1.  获取情求参数的dmp_data_table_id判断是否存在，否则获取不到返回状态码【101】数据表不存在返回状态码【4404】
2.  根据数据库类型获取相应的查询参数并进行校验，否则返回状态码【101】
3.  根据对应数据库类型拼接查询语句或参数，进行查询将结果进行返回

**请求说明**

| URL           | /bi/dataquery |
| ------------- | ------------- |
| 格式          | JSON          |
| http 请求方式 | GET           |
| 登陆保护      | 是            |

 **请求参数**

| 参数名            | 类型   | 是否必填                 | 最大长度 | 参数说明                  |
| ----------------- | ------ | ------------------------ | -------- | ------------------------- |
| dmp_data_table_id | int    | 是                       |          | 要进行查询的数据表ID      |
| param_select      | string | mysql必填，默认“*”       |          | mysql查询参数select参数   |
| param_form        | string | mysql必填，默认当前表名  |          | mysql查询参数from参数     |
| param_where       | string |                          |          | mysql查询参数where参数    |
| param_group_by    | string |                          |          | mysql查询参数group_by参数 |
| param_having      | string |                          |          | mysql查询参数having参数   |
| param_order_by    | string |                          |          | mysql查询参数order_by参数 |
| param_filter      | string |                          |          | monogo参数filter参数      |
| param_projection  | string |                          |          | monogo参数projection参数  |
| param_sort        | string |                          |          | monogo参数sort参数        |
| param_maxtimes    | string | mongodb必填，默认30000ms |          | monogo参数maxtimes参数    |
| param_offset      | string |                          |          | 通用参数偏移量            |
| param_limit       | string | 必填，默认值100          |          | 通用参数数据量            |


**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
      ****依实际数据格式为准****
  }
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |

### 查询多个数据服务

**接口描述**

1.  接受情求参数
2.  如果有要进行检索的服务名，进行长度校验，校验失败返回错误码【201】
3.  根据参数进行查询并返回


**请求说明**

| URL           | /ds/dataservices |
| ------------- | ---------------- |
| 格式          | JSON             |
| http 请求方式 | GET              |
| 登陆保护      | 是               |

 **请求参数**

| 参数名            | 类型   | 是否必填    | 最大长度 | 参数说明           |
| ----------------- | ------ | ----------- | -------- | ------------------ |
| data_service_name | string | 否          | 50       | 要进行检索的服务名 |
| page_num          | int    | 是          |          | 页码               |
| pagesize          | int    | 是,默认10条 |          | 单页数量           |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名                   | 类型   | 参数说明          |
| ------------------------ | ------ | ----------------- |
| id                       | int    | 数据服务ID        |
| data_service_name        | string | 数据服务名称      |
| request_method           | int    | 请求方法1get2post |
| source_dmp_data_table_id | int    | 源数据表ID        |
| projection               | string | 预选字段          |
| state                    | int    | 是否启用          |
| description              | string | 数据服务简介      |
| created_on                     | string | 创建时间       |
| changed_on                     | string | 最后修改时间   |
| created_dmp_user_id            | int    | 创建人ID       |
| changed_dmp_user_id            | int    | 最后修改人ID   |
| created_dmp_user_name          | string | 创建人名称     |
| changed_dmp_user_name          | string | 最后修改人名称 |
|                          |        |                   |

### 获取单一数据服务

**接口描述**

1.  接受请求参数获取数据服务ID，获取不到返回状态码【201】
2.  根据参数进行查找返回


**请求说明**

| URL           | `/ds/dataservices/<id:int>` |
| ------------- | --------------------------- |
| 格式          | JSON                        |
| http 请求方式 | GET                         |
| 登陆保护      | 是                          |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明                        |
| ------ | ---- | -------- | -------- | ------------------------------- |
| id     | int  | 是       | -        | URL参数要获取的数据服务内容的ID |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名                   | 类型   | 参数说明          |
| ------------------------ | ------ | ----------------- |
| id                       | int    | 数据服务ID        |
| data_service_name        | string | 数据服务名称      |
| api_path | string | 数据服务接口 |
| request_method           | int    | 请求方法1get2post |
| source_dmp_data_table_id | int    | 源数据表ID        |
| projection               | string | 预选字段          |
| state                    | int    | 是否启用          |
| description              | string | 数据服务简介      |
| parameters               | arrary | 数据服务字段信息  |
| created_on                     | string | 创建时间       |
| changed_on                     | string | 最后修改时间   |
| created_dmp_user_id            | int    | 创建人ID       |
| changed_dmp_user_id            | int    | 最后修改人ID   |
| created_dmp_user_name          | string | 创建人名称     |
| changed_dmp_user_name          | string | 最后修改人名称 |

**parameters字段介绍:**

| 参数名                   | 类型   | 参数说明   |
| ------------------------ | ------ | ---------- |
| id                       | int    | 字段ID     |
| parameter_name           | string | 子弹名称   |
| type                     | string | 数据类型   |
| source_dmp_data_table_id | int    | 源数据表ID |
| required_parameter       | int    | 是否必填   |
| description              | string | 字段简介   |



### 添加数据服务

**接口描述**

1.  解析headers参数获取当前用户id，解析不到返回错误码【201】判断是否为教师类及管理员类用户，否则返回状态码【301】
2.  根据情求参数回去数据服务相关信息进行字段校验，校验失败返回错误码【101】
3.  将数据添加到数据库


**请求说明**

| URL           | /ds/dataservices |
| ------------- | ---------------- |
| 格式          | JSON             |
| http 请求方式 | POST             |
| 登陆保护      | 是               |

 **请求参数**

| 参数名            | 类型   | 是否必填 | 最大长度 | 参数说明          |
| ----------------- | ------ | -------- | -------- | ----------------- |
| data_service_name | string | 是       | 50       | 数据服务名称      |
| api_path          | string | 是       | 255      | 数据服务接口      |
| request_method    | int    | 是       |          | 请求方法1get2post |
| description       | string |          | 400      | 简介              |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |

### 修改数据服务

**接口描述**

1.  解析headers参数获取当前用户id，解析不到返回错误码【201】判断是否为本人，否则返回状态码【301】
2.  获取URL参数id，获取不到返回错误码【101】，判断参数是否存在不存在返回【7641】
3.  根据情求参数回去数据服务相关信息进行字段校验，校验失败返回错误码【101】
4.  将数据更新到数据库


**请求说明**

| URL           | `/ds/dataservices/<id:int>` |
| ------------- | --------------------------- |
| 格式          | JSON                        |
| http 请求方式 | PUT                         |
| 登陆保护      | 是                          |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明                      |
| ------ | ---- | -------- | -------- | ----------------------------- |
| id     | int  | 是       |          | URL参数，要修改的数据服务的ID |
| data_service_name | string |        | 50       | 数据服务名称      |
| api_path          | string |        | 255      | 数据服务接口      |
| request_method    | int    |        |          | 请求方法1get2post |
| description       | string |          | 400      | 简介              |
| source_dmp_data_table_id | int |          |          | 源数据表ID |
| query_sql | string |          |          | 查询语句（mysql） |
| query_params | string | | | 查询参数（mongodb） |
| state | int |          |          | 是否启用 |
|        |      |          |          |                               |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |

### 添加数据服务参数接口

**接口描述**

1.  解析请求获取相关信息进行字段校验，校验失败返回状态码【101】
2.  将信息添加到数据库


**请求说明**

| URL           | /ds/ds_parameters |
| ------------- | ----------------- |
| 格式          | JSON              |
| http 请求方式 | POST              |
| 登陆保护      | 是                |

 **请求参数**

| 参数名              | 类型   | 是否必填            | 最大长度 | 参数说明     |
| ------------------- | ------ | ------------------- | -------- | ------------ |
| dmp_data_service_id | int    | 是                  |          | 数据服务ID   |
| parameter_name      | string | 是                  | 100      | 参数名       |
| type                | string | 是，默认为“varchar” | 50       | 字段类型     |
| required_parameter  | int    | 是                  |          | 是否是必填项 |
| description         | string |                     | 400      | 简介         |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 修改数据服务参数

**接口描述**

1.  获取URL参数id，获取不到返回错误码【101】，判断参数是否存在不存在返回【7641】
2.  解析请求获取相关信息进行字段校验，校验失败返回状态码【101】
3.  将信息更新到数据库


**请求说明**

| URL           | `/ds/ds_parameters/<id:int>` |
| ------------- | ---------------------------- |
| 格式          | JSON                         |
| http 请求方式 | PUT                          |
| 登陆保护      | 是                           |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
| dmp_data_service_id | int    |             |          | 数据服务ID   |
| parameter_name      | string |             | 100      | 参数名       |
| type                | string |  | 50       | 字段类型     |
| required_parameter  | int    |             |          | 是否是必填项 |
| description         | string |               | 400      | 简介         |




**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |

### *删除数据服务参数（作废）

**接口描述**

1.  获取URL参数id，获取不到返回错误码【101】，判断参数是否存在不存在返回【7641】
2.  将参数信息删除


**请求说明**

| URL           | `/ds/ds_parameters<id:int>` |
| ------------- | --------------------------- |
| 格式          | JSON                        |
| http 请求方式 | DELETER                     |
| 登陆保护      | 是                          |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明       |
| ------ | ---- | -------- | -------- | -------------- |
| id     | int  | 是       |          | 要删除的字段ID |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| -      | -    | -        |

### 删除数据服务

**接口描述**

1.  获取URL参数id，获取不到返回错误码【101】，判断参数是否存在不存在返回【7401】
2.  将数据服务及其参数信息删除


**请求说明**

| URL           | `/ds/dataservices/<id:int>` |
| ------------- | --------------------------- |
| 格式          | JSON                        |
| http 请求方式 | DELETER                     |
| 登陆保护      | 是                          |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明           |
| ------ | ---- | -------- | -------- | ------------------ |
| id     | int  | 是       |          | 要删除的数据服务ID |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 数据服务调用

添加访问频次限制，限制为：

**接口描述**

1.  获取token内容获取不到返回【8101】，解析当前用户ID，解析失败返回【8012】
2.  跟局URL参数判断该服务是否存在，不存在返回状态码【8104】
3.  获取该服务信息，进行参数校验，不符合要求返回【8105】
4.  进行查询并返回结果


**请求说明**

| URL           | `/ds/api/<api:path>` |
| ------------- | -------------------- |
| 格式          | JSON                 |
| http 请求方式 | GET                  |
| 登陆保护      | 是                   |

 **请求参数**

| 参数名     | 类型          | 是否必填 | 最大长度 | 参数说明         |
| ---------- | ------------- | -------- | -------- | ---------------- |
| api        | string        | 是       |          | 数据接口路径     |
| secret_key | string        | 是       |          | 个人秘钥         |
| page_num   | Int           | 否       |          | 页码，不填就是1  |
| **         | string or int |          |          | 其他数据服务参数 |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 获取个人秘钥

**接口描述**

1.  接收参数 过期时间，校验是否合法，不合法返回【201】；
2.  使用user_ID和过期时间创建token，进行返回

**请求说明**

| URL           | /user/secretkey |
| ------------- | --------------- |
| 格式          | JSON            |
| http 请求方式 | GET             |
| 登陆保护      | 是              |

 **请求参数**

| 参数名  | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------- | ---- | -------- | -------- | -------- |
| expires | int  | 是       |          | 到期时间 |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 校验文件夹名称是否存在

**接口描述**

将对应文件下载表单的文件删除


**请求说明**

| URL           | /verifier/archive |
| ------------- | ----------------- |
| 格式          | JSON              |
| http 请求方式 | GET               |
| 登陆保护      | 是                |

 **请求参数**

| 参数名                     | 类型   | 是否必填 | 最大长度 | 参数说明           |
| -------------------------- | ------ | -------- | -------- | ------------------ |
| dmp_dashboard_archive_name | string | 是       | 64       | 要校验的文件夹名称 |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 校验看板名称是否存在

**接口描述**

将对应文件下载表单的文件删除


**请求说明**

| URL           | /verifier/dashboard |
| ------------- | ------------------- |
| 格式          | JSON                |
| http 请求方式 | GET                 |
| 登陆保护      | 是                  |

 **请求参数**

| 参数名             | 类型   | 是否必填 | 最大长度 | 参数说明 |
| ------------------ | ------ | -------- | -------- | -------- |
| dmp_dashboard_name | string | 是       | 64       | 看板名称 |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 校验数据服务名称是否存在

**接口描述**

将对应文件下载表单的文件删除


**请求说明**

| URL           | /verifier/dataservice |
| ------------- | --------------------- |
| 格式          | JSON                  |
| http 请求方式 | GET                   |
| 登陆保护      | 是                    |

 **请求参数**

| 参数名               | 类型   | 是否必填 | 最大长度 | 参数说明     |
| -------------------- | ------ | -------- | -------- | ------------ |
| dmp_dataservice_name | string | 是       | 64       | 数据服务名称 |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 【接口名称】

**接口描述**

将对应文件下载表单的文件删除


**请求说明**

| URL           | /    |
| ------------- | ---- |
| 格式          | JSON |
| http 请求方式 | POST |
| 登陆保护      | 是   |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 【接口名称】

**接口描述**

将对应文件下载表单的文件删除


**请求说明**

| URL           | /    |
| ------------- | ---- |
| 格式          | JSON |
| http 请求方式 | POST |
| 登陆保护      | 是   |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 【接口名称】

**接口描述**

将对应文件下载表单的文件删除


**请求说明**

| URL           | /    |
| ------------- | ---- |
| 格式          | JSON |
| http 请求方式 | POST |
| 登陆保护      | 是   |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 【接口名称】

**接口描述**

将对应文件下载表单的文件删除


**请求说明**

| URL           | /    |
| ------------- | ---- |
| 格式          | JSON |
| http 请求方式 | POST |
| 登陆保护      | 是   |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 【接口名称】

**接口描述**

将对应文件下载表单的文件删除


**请求说明**

| URL           | /    |
| ------------- | ---- |
| 格式          | JSON |
| http 请求方式 | POST |
| 登陆保护      | 是   |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |



**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

