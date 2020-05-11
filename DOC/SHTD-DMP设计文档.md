# SHTD-DMP-SERVER设计文档

DMP( *Data Management Platform*)数据管理平台

[toc]

## 功能列表

- 数据集群连接
- 数据库绑定
   - MongoDB
   - MySQL
-  数据上传(！大文件)
   - SQLite
   - CSV
   - JSON
   - EXCEL
- 数据量化
- 数据周转
   - 数据库到集群
   - 集群到数据库
- 数据检索
   - 简单检索
   - ES
- 表单审批数据导入表单审批
   - 数据导出表单审批
- 数据导出
   - 下载验证确保数据安全
- 用户注册
   - 单一注册（邮箱+管理员确认激活）
   - 批量注册
- 用户管理
   - 创建
   - 删除
   - 冻结
- 用户组系统
   - 系统功能模块化（超级管理员可以自由组合相应功能的用户组）
   - 权限限制及确认机制





## 表设计
### 用户表
表名：dmp_user

| 字段               | 数据类型 | 限制       | 介绍                                  |
| ------------------ | -------- | ---------- | ------------------------------------- |
| id                 | Int      | Primay Key | 用户ID                                |
| dmp_username       | string   | 非空       | 用户名                                |
| real_name          | string   | 非空       | 真实姓名                              |
| email              | string   | Unique     | 用户邮箱                              |
| passwd             | string   | 非空       | 用户密码，加密储存                    |
| confirmed          | boolean  |            | 用户激活状态，默认FALSE               |
| dmp_group_id       | int      |            | 所属用户组ID，默认学生用户组,使用外键 |
| leader_dmp_user_id | Int      |            | 直属管理者，默认是超级管理员用户      |
| icon               | string   |            | 头像                                  |
| dmp_user_info       | String   |            | 个人简介                              |
| last_login         | Date     |            | 最后登录时间                          |
| created_on         | Date     |            | 创建时间                              |
| changed_on         | Date     |            | 修改时间                              |
### 用户组表
表名：dmp_group

| 字段       | 数据类型 | 限制       | 介绍         |
| ---------- | -------- | ---------- | ------------ |
| id         | Int      | Primay Key | 用户组ID     |
| dmp_group_name | string   | Unique     | 用户组名     |
| max_count  | Int      |            | 最大用户数量 |
| created_on | Date     |            | 创建时间     |
| changed_on | Date     |            | 修改时间     |
### 权限表
表名：dmp_permission

| 字段                | 数据类型 | 限制       | 介绍         |
| ------------------- | -------- | ---------- | ------------ |
| id                  | int      | Primay Key | 功能ID       |
| route               | string   | 非空       | 路由         |
| dmp_permission_name | string   | 非空       | 路由功能名称 |
### 用户组_功能表
表名：dmp_group_permission

| 字段              | 数据类型 | 限制               | 介绍     |
| ----------------- | -------- | ------------------ | -------- |
| id                | int      | Primay Key、Unique | ID       |
| dmp_permission_id | int      | 非空               | 权限ID   |
| dmp_group_id      | Int      | 非空               | 用户组ID |
### 权利表
表名：dmp_rights

| 字段            | 数据类型 | 限制       | 介绍         |
| --------------- | -------- | ---------- | ------------ |
| id              | int      | Primay Key | 功能ID       |
| dmp_rights_name | string   | 非空       | 路由功能名称 |
### 用户组_权利
表名：dmp_group_rights

| 字段          | 数据类型 | 限制               | 介绍     |
| ------------- | -------- | ------------------ | -------- |
| id            | int      | Primay Key、Unique | ID       |
| dmp_rights_id | int      | 非空               | 权限ID   |
| dmp_group_id  | Int      | 非空               | 用户组ID |



### 数据库表

表名：dmp_datebase

| 字段           | 数据类型 | 限制       | 介绍                              |
| -------------- | -------- | ---------- | --------------------------------- |
| id             | int      | Primay Key |                                   |
| dmp_datebase_name  | string   | Unique     | 数据显示名称                      |
| dmp_user_id | Int      | 非空       | 所属用户ID                        |
| db_type        | int      | 非空       | 数据库类型,hive:0,mysql:1,mongo:2 |
| db_host        | string   | 非空       | 数据库主机地址                    |
| db_port        | int      | 非空       | 数据库端口号                      |
| db_name        | string   |            | 数据库名称                        |
| db_username    | string   |            | 数据库用户名                      |
| db_passwd      | string   |            | 数据库密码                        |
| description    | string   |            | 数据库说明                        |
| created_on     | Date     | 非空       | 创建时间                          |
| changed_on     | Date     |            | 修改时间                          |

### 案例表

表名：dmp_case

| 字段        | 数据类型 | 限制       | 介绍           |
| ----------- | -------- | ---------- | -------------- |
| id          | int      | Primay Key |                |
| dmp_case_name | String   | 非空       | 案例名称       |
| description | string   |            | 案例说明       |
| url_name    | string   |            | 可视化网站名称 |
| Url         | String   |            | 网址           |
| created_on | Date | 非空 | 创建时间 |
| changed_on | Date |  | 修改时间 |


### 数据表

表名：dmp_data_table

| 字段                 | 数据类型 | 限制       | 介绍               |
| -------------------- | -------- | ---------- | ------------------ |
| id                   | int      | Primay Key |                    |
| dmp_data_table_name      | string   | Unique     | 数据名称           |
| db_table_name        |          | 非空       | 数据库内数据表名称 |
| dmp_database_id      | int      | 非空       | 数据库ID           |
| dmp_data_case_id | Int      |            | 所属案例id         |
| dmp_user_id           | int      | 非空       | 添加人             |
| description          | String   |            | 数据说明           |
| created_on           | Date     | 非空       | 创建时间           |
| changed_on           | Date     |            | 修改时间           |
### 数据列信息
表名：dmp_data_table_column

| 字段              | 数据类型 | 限制               | 介绍               |
| ----------------- | -------- | ------------------ | ------------------ |
| id                | int      | Primay Key、Unique |                    |
| dmp_data_table_id | int      | 非空               | 数据ID             |
| dmp_data_table_column_name       | string   | 非空               | 列名               |
| groupby           | boolearn | 默认FALSE          | 可以进行分组       |
| Wherein           | boolearn | 默认FALSE          | 可以区间筛选       |
| Isdate            | boolearn | 默认FALSE          | 是否为时间日期字段 |
| description       | string   |                    | 字段说明           |
### 数据列区间
表名：dmp_data_table_column_range

| 字段                     | 数据类型 | 限制               | 介绍 |
| ------------------------ | -------- | ------------------ | ---- |
| id                       | int      | Primay Key、Unique |      |
| dmp_data_table_column_id | Int      | 非空               | 列ID |
| context                  | String   | 非空               | 内容 |
### 数据从数据库添加表单表
表名：dmp_form_add_data_table

| 字段            | 数据类型 | 限制               | 介绍     |
| --------------- | -------- | ------------------ | -------- |
| id              | int      | Primay Key、Unique |          |
| submit_on | date     | 非空 | 提交时间 |
| submit_dmp_user_id | int      | 非空 | 提交人   |
| dmp_data_table_name | string   | Unique     | 数据名称           |
| db_table_name   |          | 非空       | 数据库内数据表名称 |
| dmp_database_id     | int      | 非空 | 数据库ID           |
| dmp_case_id     | Int      | 非空 | 所属案例id         |
| description              | string   |                    | 说明             |
| approve_dmp_user_id   | Int      |                    | 审批人           |
| approve_on             | date     |                    | 审批时间         |
| approve_result           | int      |                    | 审批结果,默认为0，通过是1不通过是2 |
| answer | string | | 审批答复 |
| created_on | Date | 非空 | 创建时间 |
| changed_on | Date | | 修改时间 |




### 数据文件上传单表
表名：dmp_form_upload

| 字段                        | 数据类型 | 限制               | 介绍                               |
| --------------------------- | -------- | ------------------ | ---------------------------------- |
| id                          | int      | Primay Key、Unique |                                    |
| submit_on                   | date     | 非空               | 提交时间                           |
| submit_dmp_user_id       | int      | 非空               | 提交人                             |
| filetype                    | Int      | 非空               | 文件类型                           |
| filepath                    | string   | 非空               | 文件路径                           |
| column_line                 | Int      |                    | 列名行号                           |
| column                      | string   |                    | 自定义列名                         |
| json_dimension_reduction    | Boolearn |                    | json数据是否遍历存储               |
| destination_dmp_datebase_id | int      | 非空               | 目标数据库ID                       |
| new_table_name              | string   | 非空               | 表名                               |
| method                      | String   | 非空               | 新建还是添加覆盖                   |
| dmp_data_case_id        | Int      | 非空               | 所属案例                           |
| description                 | string   |                    | 说明                               |
| approve_dmp_user_id          | Int      |                    | 审批人                             |
| approval_on                 | date     |                    | 审批时间                           |
| approve_result              | int      |                    | 审批结果,默认为0，通过是1不通过是2 |
| answer                      | String   |                    | 审批答复                           |
| upload                      | bool     |                    | 是否成功                           |
| upload_result               | string   |                    | 数据上传结果                       |
| created_on                  | Date     | 非空               | 创建时间                           |
| changed_on                  | Date     |                    | 修改时间                           |


### 数据迁移表单表
表名：dmp_form_migrate

| 字段                        | 数据类型 | 限制               | 介绍                               |
| --------------------------- | -------- | ------------------ | ---------------------------------- |
| id                          | int      | Primay Key、Unique |                                    |
| submit_on                   | date     | 非空               | 提交时间                           |
| submit_dmp_user_id       | int      | 非空               | 提交人                             |
| origin_dmp_table_id             | int      | 非空               | 起点数据表                         |
| rule                        | string   |                    | 数据提取规则                       |
| destination_dmp_datebase_id | int      | 非空               | 目标数据库ID                       |
| new_table_name              | string   | 非空               | 新表名                             |
| method                      | String   | 非空               | 覆盖添加新建                       |
| description                 | string   |                    | 说明                               |
| approve_dmp_user_id      | int      |                    | 审批人                             |
| approval_on                 | date     |                    | 审批时间                           |
| approve_result              | int      |                    | 审批结果,默认为0，通过是1不通过是2 |
| answer                      | string   |                    | 审批答复                           |
| migrate                     | Boolearn |                    | 迁移成功                           |
| migrate_result              | string   |                    | 迁移结果                           |
| created_on                  | Date     | 非空               | 创建时间                           |
| changed_on                  | Date     |                    | 修改时间                           |


### 数据下载表单表
表名：dmp_form_download

| 字段                  | 数据类型 | 限制               | 介绍                               |
| --------------------- | -------- | ------------------ | ---------------------------------- |
| id                    | int      | Primay Key、Unique |                                    |
| submit_on             | date     | 非空               | 提交时间                           |
| submit_dmp_user_id | int      | 非空               | 提交人                             |
| dmp_data_table_id     | int      | 非空               | 源数据表ID                         |
| rule                  | string   |                    | 数据提取规则                       |
| description           | string   |                    | 说明                               |
| approve_dmp_user_id    | int      |                    | 审批人                             |
| approval_on           | date     |                    | 审批时间                           |
| approve_result        | int      |                    | 审批结果,默认为0，通过是1不通过是2 |
| answer                | string   |                    | 审批答复                           |
| ftp_url               | string   |                    | FTP下载链接                        |
| ftp_pid               | int      |                    | FTP进程号                          |
| filepath              | string   |                    | 文件路径                           |
| finish                | boolearn |                    | 是否完成                           |
| created_on            | Date     | 非空               | 创建时间                           |
| changed_on            | Date     |                    | 修改时间                           |

## API 文档

### 说明

#### 响应状态码

| status | msg                               | info                   |
| ------ | --------------------------------- | ---------------------- |
| 0      | success                           | 响应成功               |
| 101    | required_parameter_missing        | 缺少必要参数           |
| 201    | Invalid_token                     | 无效的Token或Token过期 |
| 301    | required_Insufficient_permissions | 权限不足               |
| 302    | unauthorized                      | 未授权                 |
|        | database_occupied                 | 数据库占用中           |
|        | database_connection_failed        | 数据库连接失败         |
| 999    | unknow_error                      | 未知错误               |



#### 返回值固有字段

| 参数名  | 类型           | 参数说明                       |
| ------- | -------------- | ------------------------------ |
| status  | Int            | 标志结果集中所含设备或视频数量 |
| msg     | string         | 状态码信息                     |
| results | Dict/ArrayList | 返回值                         |

### 注册

**接口描述**

接收前端提交的用户相关信息，在数据库内添加用户的信息，并发送激活邮件至对应邮箱


**请求说明**

| URL           | /user/register/ |
| ------------- | --------------- |
| 格式          | JSON            |
| http 请求方式 | POST            |
| 登陆保护      | 否              |

 **请求参数**

| 参数名        | 类型   | 是否必填 | 最大长度 | 参数说明 |
| ------------- | ------ | -------- | -------- | -------- |
| dmp_username  | String | 是       | 16       | 用户名   |
| real_name | String | 是       | 16       | 真实姓名 |
| email         | string | 是       |          | 邮箱     |
| dmp_group_id  | int    | 否       |          | 用户组ID |
| leader_dmp_user_id     | int    | 否       |          | 上级ID   |
| password      | string | 是       |          | 密码     |

**返回结果**

```json
{
 "status": 0,
  "msg": "success",
  "results":"OK"
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 邮件激活

**接口描述**

使用带有token的链接激活用户


**请求说明**

| URL           | /user/activate/ |
| ------------- | --------------- |
| 格式          | JSON            |
| http 请求方式 | POST            |
| 登陆保护      | 否              |

 **请求参数**

| 参数名 | 类型   | 是否必填 | 最大长度 | 参数说明             |
| ------ | ------ | -------- | -------- | -------------------- |
| token  | string | 是       |          | 用户激活的加密字符串 |

**返回结果**

```json
{
 "status": 0,
  "msg": "success",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |



### 登陆

**接口描述**

实现用户的登录功能


**请求说明**

| URL           | /user/login/ |
| ------------- | ------------ |
| 格式          | JSON         |
| http 请求方式 | POST         |

**请求参数**

| 参数名       | 类型   | 是否必填             | 最大长度 | 参数说明           |
| ------------ | ------ | -------------------- | -------- | ------------------ |
| dmp_username | String | 当无email时为必填    | N/A      | 用户名             |
| email        | String | 当无username时为必填 | N/A      | 返回结果集规模限制 |
| passwd       | String | 必填                 | N/A      | 密码，加密传输     |
| remember_me  | Bool   | 是，默认为FALSE      | N/A      | 记住登录状态       |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
  		"token":"212fsdf32fdwffdsfsd"
  }
}
```



### 退出登录

**接口描述**

实现用户的退出登录功能


**请求说明**

| URL           | /user/logout/ |
| ------------- | ------------- |
| 格式          | JSON          |
| http 请求方式 | GET           |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":None
}
```

### 忘记密码

**接口描述**

发送用于重置密码的链接邮件


**请求说明**

| URL           | /user/forgetpwd |
| ------------- | --------------- |
| 格式          | JSON            |
| http 请求方式 | POST            |
| 登陆保护      | 否              |

 **请求参数**

| 参数名 | 类型   | 是否必填 | 最大长度 | 参数说明             |
| ------ | ------ | -------- | -------- | -------------------- |
| email  | string | 是       |          | 要重置密码的账户邮箱 |

**返回结果**

```json
{
 "status": 0,
  "msg": "success",
  "results":{}
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 修改密码

**接口描述**




**请求说明**

| URL           | /user/changepwd/ |
| ------------- | ---------------- |
| 格式          | JSON             |
| http 请求方式 | put              |
| 登陆保护      | 否               |

 **请求参数**

| 参数名    | 类型   | 是否必填           | 最大长度 | 参数说明     |
| --------- | ------ | ------------------ | -------- | ------------ |
| newpasswd | string | 是                 |          | 新密码       |
| token     | string | 否，邮件重置时必填 |          | 用户加密信息 |

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



### 获取用户信息

**接口描述**

获取单一用户的信息


**请求说明**

| URL           | /user/info/ |
| ------------- | ----------- |
| 格式          | JSON        |
| http 请求方式 | GET         |
|               | 是          |

 **请求参数**

| 参数名      | 类型 | 是否必填                   | 最大长度 | 参数说明 |
| ----------- | ---- | -------------------------- | -------- | -------- |
| dmp_user_id | Int  | 否（默认返回当前用户信息） | N/A      | 用户ID   |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
     "id":"01",
     "dmp_username":"user01",
     "real_name":"user01",
     "email":"user01@test.com",
     "dmp_group":"admin",
     "leader_dmp_user":"admin",
     "user_info":"test_user",
     "last_login":"2020-04-21 09:00:00",
     "created_on":"2020-02-21 09:00:00",
     "changed_on":"2020-03-21 09:00:00",
  }
}
```

**result结构如下:**

| 参数名          | 类型   | 参数说明     |
| --------------- | ------ | ------------ |
| id              | Int    | 用户ID       |
| dmp_username    | string | 用户名       |
| real_name       | string | 真实姓名     |
| email           | string | 用户邮箱     |
| dmp_group       | int    | 所属用户组   |
| leader_dmp_user | Int    | 直属管理者   |
| user_info       | String | 个人简介     |
| last_login      | Date   | 最后登录时间 |
| created_on      | Date   | 创建时间     |
| changed_on      | Date   | 修改时间     |



### 邮箱是否已使用

**接口描述**

实现验证当前邮箱是否已经被使用。


**请求说明**

| URL           | /verifier/email/ |
| ------------- | ---------------- |
| 格式          | JSON             |
| http 请求方式 | GET              |
| 登陆保护      | 否               |

 **请求参数**

| 参数名 | 类型   | 是否必填 | 最大长度 | 参数说明 |
| ------ | ------ | -------- | -------- | -------- |
| email  | String | 必填     | N/A      | 邮箱     |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":Flase
}
```



### 用户名是否已使用

**接口描述**

实现验证当前用户名是否已经被使用。


**请求说明**

| URL           | /verifier/username/ |
| ------------- | ------------------- |
| 格式          | JSON                |
| http 请求方式 | GET                 |
| 登陆保护      | 否                  |

 **请求参数**

| 参数名   | 类型   | 是否必填 | 最大长度 | 参数说明 |
| -------- | ------ | -------- | -------- | -------- |
| username | String | 必填     | N/A      | 用户名   |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":Flase
}
```



### 头像上传

**接口描述**

接收二进制的图片数据对用户的头像进行修改


**请求说明**

| URL           | /user/icon |
| ------------- | ---------- |
| 格式          | JSON       |
| http 请求方式 | POST       |
| 登陆保护      | 是         |

 **请求参数**

| 参数名 | 类型   | 是否必填 | 最大长度 | 参数说明                      |
| ------ | ------ | -------- | -------- | ----------------------------- |
| bin    | String |          | N/A      | Base64 编码过的二进制图片数据 |

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

### 修改资料

**接口描述**

修改用户资料的接口

**请求说明**

| URL           | /user/changeprofile/ |
| ------------- | -------------------- |
| 格式          | JSON                 |
| http 请求方式 | PUT                  |
| 登陆保护      | 是                   |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
| dmp_user_id | int | 否 |  | 用户ID,不填就是修改自己;填了需验证权利后执行操作 |
| dmp_username | String | 否      | 16       | 用户名   |
| real_name | String | 否      | 16       | 真实姓名 |
| email     | string | 否      |          | 邮箱     |
| dmo_group_id | int    | 否       |          | 用户组ID |
| leader_dmp_user_id | int | 否       |          | 上级ID   |
| password  | string | 否      |          | 密码     |
| confirmed | boolearn | 否 | | 激活状态 |

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

### 获取用户列表

**接口描述**

管理员返回所有用户，其他角色仅返回leader_dmp_user等于自己的用户的列表


**请求说明**

| URL           | /user/list |
| ------------- | ---------- |
| 格式          | JSON       |
| http 请求方式 | GET        |
| 登陆保护      | 是         |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":[
    "user01":{
      "id":"01",
      "dmp_username":"user01",
      "real_name":"user01",
      "email":"user01@test.com",
      "dmp_group":"stu",
      "leader_dmp_user_id":01,
      "user_info":"test_user",
      "last_login":"2020-04-21 09:00:00",
      "created_on":"2020-02-21 09:00:00",
      "changed_on":"2020-03-21 09:00:00",
    },
		"user02":{
      "id":"02",
      "dmp_username":"user02",
      "real_name":"user02",
      "email":"user02@test.com",
      "dmp_group":"stu",
      "leader_dmp_user_id":1,
      "user_info":"test_user",
      "last_login":"2020-04-21 09:00:00",
      "created_on":"2020-02-21 09:00:00",
      "changed_on":"2020-03-21 09:00:00",
    }
  ]
}
```

**result说明:**

| 参数名           | 类型 | 参数说明 |
| ---------------- | ---- | -------- |
| 参见获取用户信息 |      |          |

### 删除用户

**接口描述**

传入userID删除用户

**请求说明**

| URL           | /user/del |
| ------------- | --------- |
| 格式          | JSON      |
| http 请求方式 | DEL       |
| 登陆保护      | 是        |

 **请求参数**

| 参数名      | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ----------- | ---- | -------- | -------- | -------- |
| dmp_user_id | int  | 是       | N/A      | 用户ID   |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
    "res":"用户删除成功",
  }
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 获取所有权限信息

**接口描述**

所有权限的信息


**请求说明**

| URL           | /permission/all |
| ------------- | --------------- |
| 格式          | JSON            |
| http 请求方式 | GET             |
| 登陆保护      | 是              |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |

 **返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":[
    {
      "id":1,
      "permission":"permission211"
    },
    {
      "id":2,
      "permission":"permission2"
    }
  ]
}
```

**result说明:**

| 参数名     | 类型   | 参数说明 |
| ---------- | ------ | -------- |
| id         | int    | 权限ID   |
| permission | string | 权限名称 |

### 获取所有权利信息

**接口描述**

所有权利的信息

**请求说明**

| URL           | /rights/all |
| ------------- | ----------- |
| 格式          | JSON        |
| http 请求方式 | GET         |
| 登陆保护      | 是          |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":[
    {
      "id":1,
      "rights":"rights211"
    },
    {
      "id":2,
      "rights":"rights2"
    }
  ]
}
```

**result说明:**

| 参数名 | 类型   | 参数说明 |
| ------ | ------ | -------- |
| id     | int    | 权利信息 |
| rights | string | 权利名称 |



### 获取用户组信息

**接口描述**

获取所有的用户组信息


**请求说明**

| URL           | /usergroup/info |
| ------------- | --------------- |
| 格式          | JSON            |
| http 请求方式 | GET             |
| 登陆保护      | 是              |

 **请求参数**

| 参数名       | 类型 | 是否必填 | 最大长度 | 参数说明                         |
| ------------ | ---- | -------- | -------- | -------------------------------- |
| dmp_group_id | int  | 否       |          | 用户组id，不填返回所有用户组信息 |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":[
    {
      "id":01,
      "dmp_group_name":"group01",
      "max_count":1000,
      "created_on":"2020-03-09 12:00:00",
      "changed_on":"2020-04-09 12:00:00",
      "dmp_permission":["permission01","permission02","permission03","permission04"],
      "dmp_lights":["lights01","lights02","lights,03","lights04","lights05"],
    },
		{
      "id":02,
      "group_name":"group02",
      "max_count":1000,
      "created_on":"2020-03-09 12:00:00",
      "changed_on":"2020-04-09 12:00:00",
      "dmp_permission":["permission01","permission02","permission03","permission04"],
      "dmp_lights":["lights01","lights02","lights,03","lights04","lights05"],
    }
  ]
}
```

**result说明:**

| 参数名  | 类型   | 参数说明                                 |
| ------- | ------ | ---------------------------------------- |
| {group} | string | 用户组名称，内容字段见【获取用户组信息】 |

### 添加/修改用户组

**接口描述**

仅能管理员能访问的接口，创建用户组

**请求说明**

| URL           | /usergroup/post |
| ------------- | --------------- |
| 格式          | JSON            |
| http 请求方式 | POST            |
| 登陆保护      | 是              |

 **请求参数**

| 参数名         | 类型       | 是否必填 | 最大长度 | 参数说明                     |
| -------------- | ---------- | -------- | -------- | ---------------------------- |
| dmp_group_id   | int        | 否       |          | 用户组id,修改时必填          |
| dmp_group_name | string     | 是       |          | 用户组名称                   |
| max_count      | int        | 否       |          | 用户组容量，若不填表示无限制 |
| dmp_permission     | ArraryList | 是       |          | 用户权限id的数组             |
| dmp_rights         | ArraryList | 是       |          | 用户权权利id的数组           |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
    "res":"OK"
  }
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 删除用户组

**接口描述**

仅管理员，删除用户组


**请求说明**

| URL           | /usergroup/del |
| ------------- | -------------- |
| 格式          | JSON           |
| http 请求方式 | POST           |
| 登陆保护      | 是             |

 **请求参数**

| 参数名       | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------------ | ---- | -------- | -------- | -------- |
| dmp_group_id | int  | 是       |          | 用户组ID |

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



------



### 获取首页数据概览

**接口描述**

获取首页使用的数据概览。


**请求说明**

| URL           | /index/overview/ |
| ------------- | ---------------- |
| 格式          | JSON             |
| http 请求方式 | GET              |
| 登陆保护      | 是               |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
    	"database_count":20,
     "datatable_count":30,
     "data_count":1236718231,
     "case_count":5,
  }
}
```

**result说明:**

| 参数名          | 类型   | 参数说明   |
| --------------- | ------ | ---------- |
| database_count  | Int    | 数据库数量 |
| datatable_count | string | 数据表数量 |
| data_count      | string | 数据数量   |
| case_count      | Int    | 案例数量   |



### 获取数据库信息

**接口描述**

从数据库 `dmp_database` 表中查询所有自己或自己下属的数据库的信息，若请求的用户身份管理员不进行筛选返回所有的数据库信息

**请求说明**

| URL           | /database/info |
| ------------- | -------------- |
| 格式          | JSON           |
| http 请求方式 | GET            |
| 登陆保护      | 是             |

 **请求参数**

| 参数名      | 类型 | 是否必填 | 最大长度 | 参数说明                         |
| ----------- | ---- | -------- | -------- | -------------------------------- |
| dmp_database_id | int  | 否       |          | 数据库ID，不填返回所有数据库信息 |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":[
		{
      "id":01,
      "dmp_datebase_name":"main",
      "dmp_user_id":01,
      "db_type":01,
      "db_host":"192.168.3.221",
      "db_port":"3306",
      "db_name":"dmp",
      //"db_username":"root",
      //"db_passwd":"123456",
      "description":"主数据库HIVE数据库",
      "created_on":"2020-03-18 15:00:00",
      "changed_on":"2020-03-28 15:00:00",
    },
    {
      "id":03,
      "dmp_datebase_name":"test_mysql",
      "dmp_user_id":012,
      "db_type":02,
      "db_host":"192.168.3.221",
      "db_port":"3306",
      "db_name":"dmp",
      //"db_username":"root",
      //"db_passwd":"123456",
      "description":"测试使用的mysql数据库",
      "created_on":"2020-03-18 15:00:00",
      "changed_on":"2020-03-28 15:00:00",
    }
  ]
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|id|int|数据库ID|
|dmp_datebase_name|string|数据库显示名称|
|dmp_user_id|string|所属用户ID|
|db_type|int|数据库类型ID|
|db_host|string|数据库主机|
|db_port|int|数据库端口|
|db_name|string|数据库名称|
|db_username|string|数据库用户|
|db_passwd|string|数据库密码|
|description|string|数据库简介|
|created_on|string|创建时间|
|changed_on|string|修改时间|



### 删除数据库

**接口描述**

给你数据库ID从 `dmp_database ` 表中删除数据库的连接信息，删除前需要检验数据库是否占用，若占用返回数据库的错误


**请求说明**

| URL           | /database/del |
| ------------- | ------------- |
| 格式          | JSON          |
| http 请求方式 | DEL           |
| 登陆保护      | 是            |

 **请求参数**

| 参数名      | 类型 | 是否必填 | 最大长度 | 参数说明           |
| ----------- | ---- | -------- | -------- | ------------------ |
| dmp_database_id | int  | 是       |          | 要删除的数据库的id |

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

### 验证数据库链接

**接口描述**

通过接受数据库类型、主机、端口[用户名、密码]参数，根据对应的数据库类型选择引擎进行数据库的连接测试，若失败返回数据库连接超时错误

**请求说明**

| URL           | /database/connect/ |
| ------------- | ------------------ |
| 格式          | JSON               |
| http 请求方式 | POST               |
| 登陆保护      | 是                 |

 **请求参数**

| 参数名      | 类型   | 是否必填 | 最大长度 | 参数说明       |
| ----------- | ------ | -------- | -------- | -------------- |
| db_type     | int    | 是       |          | 数据库类型编号 |
| db_host     | string | 是       |          | 数据库主机地址 |
| db_port     | int    | 是       |          | 数据库端口号   |
| db_user     | string | 否       |          | 数据库用户名   |
| db_name     |        |          |          |                |
| db_password | string | 否       |          | 数据库密码     |

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

### 添加/修改数据库连接信息

**接口描述**

将数据库的链接信心存入 `dmp_database` 表中

**请求说明**

| URL           | /database/post |
| ------------- | -------------- |
| 格式          | JSON           |
| http 请求方式 | POST           |
| 登陆保护      | 是             |

 **请求参数**

| 参数名        | 类型   | 是否必填 | 最大长度 | 参数说明                             |
| ------------- | ------ | -------- | -------- | ------------------------------------ |
| dmp_database_id   |        | 否       |          | 修改数据库信息时为必填，添加时必不填 |
| dmp_database_name | string | 否       |          | 数据库显示名称，添加时必填           |
| db_type       | int    | 是       |          | 数据库类型编号，添加时必填           |
| db_host       | string | 是       |          | 数据库主机地址，添加时必填           |
| db_port       | int    | 是       |          | 数据库端口号，添加时必填             |
| db_user       | string | 否       |          | 数据库用户名                         |
| db_password   | string | 否       |          | 数据库密码                           |
| description   | string | 否       |          | 数据库简介                           |

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

### 获取案例信息

**接口描述**

获取所有案例的信息


**请求说明**

| URL           | /case/all |
| ------------- | --------- |
| 格式          | JSON      |
| http 请求方式 | GET       |
| 登陆保护      | 是        |

 **请求参数**

| 参数名  | 类型 | 是否必填 | 最大长度 | 参数说明                     |
| ------- | ---- | -------- | -------- | ---------------------------- |
| dmp_case_id | int  | 否       |          | 案例ID不填时返回所有案例信息 |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":[
    {
      "id":1,
      "dmp_case_name":"lixian",
      "description":"lainxiandashuju",
      "url_name":"离线分析平台",
      "url":"http://www.xxxx.com",
      "data_table_count":10,
      "data_count":100000000,
      "created_on":"2020-03-18 15:00:00",
      "changed_on":"2020-03-28 15:00:00",
    },{
      "id":1,
      "dmp_case_name":"lixian",
      "description":"lainxiandashuju",
      "url_name":"离线分析平台",
      "Url":"http://www.xxxx.com",
      "data_table_count":10,
      "data_count":100000000,
      "created_on":"2020-03-18 15:00:00",
      "changed_on":"2020-03-28 15:00:00",
    }
}
```

**result说明:**

| 参数名           | 类型   | 参数说明     |
| ---------------- | ------ | ------------ |
| id               | int    | 案例ID       |
| dmp_case_name        | string | 案例名称     |
| description      | string | 案例简介     |
| url_name         | string | 案例页面名称 |
| url              | strng  | 案例页面链接 |
| data_table_count | int    | 案例表数量   |
| data_count       | int    | 案例总数据量 |
| created_on       | date   | 创建时间     |
| changed_on       | date   | 修改时间     |

### 添加/修改案例/绑定页面

**接口描述**

接收案例参数判断case_id字段是否为空添加或修改案例

**请求说明**

| URL           | /case/post |
| ------------- | ---------- |
| 格式          | JSON       |
| http 请求方式 | POST       |
| 登陆保护      | 是         |

 **请求参数**

| 参数名      | 类型   | 是否必填 | 最大长度 | 参数说明                     |
| ----------- | ------ | -------- | -------- | ---------------------------- |
| case_id     | int    | 否       |          | 案例ID，修改或绑定页面时必填 |
| dmp_case_name   | string |          |          | 案例名称，添加案例时必填     |
| description | string |          |          | 案例简介，添加案例时必填     |
| url_name    | string |          |          | 案例页面名称，不填不该       |
| url         | string |          |          | 案例页面网址，不填不该       |

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

### 删除案例

**接口描述**

接收案例id,检查案例无数据表绑定时从数据库内将案例数据删除


**请求说明**

| URL           | /case/del |
| ------------- | --------- |
| 格式          | JSON      |
| http 请求方式 | DEL       |
| 登陆保护      | 是        |

 **请求参数**

| 参数名  | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------- | ---- | -------- | -------- | -------- |
| dmp_case_id | int  | 是       |          | 案例ID   |

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

### 获取数据表信息

**接口描述**

通过传入数据表id或案例ID获得单一数据表或某一案例下所有数据表的信息

**请求说明**

| URL           | /dbtable/info |
| ------------- | ------------- |
| 格式          | JSON          |
| http 请求方式 | GET           |
| 登陆保护      | 是            |

 **请求参数**

| 参数名            | 类型 | 是否必填 | 最大长度 | 参数说明                      |
| ----------------- | ---- | -------- | -------- | ----------------------------- |
| dmp_data_table_id | int  |          |          | 数据表ID，当case_id为空时必填 |
| dmp_case_id           | int  |          |          | 案例ID，当table_id为空时必填  |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":[
    {
      "id":01,
      "data_table_name":"zhiliandata",
      "db_table_name":"zhanlian_data",
      "dmp_database_id":"01",
      "dmp_datebase_name":"main",
      "db_type":01,
      "dmp_case_id":"10",
      "user_id":"124",
      "description":"test",
      "created_on":"2020-03-18 15:00:00",
      "changed_on":"2020-03-28 15:00:00",
    },{
      "id":01,
      "data_table_name":"zhiliandata",
      "db_table_name":"zhanlian_data",
      "dmp_database_id":01,
      "dmp_datebase_name":"main",
      "db_type":01,
      "dmp_case_id":10,
      "user_id":123,
      "description":"test",
      "created_on":"2020-03-18 15:00:00",
      "changed_on":"2020-03-28 15:00:00",
    }
  ]
}
```

**result说明:**

| 参数名           | 类型   | 参数说明             |
| ---------------- | ------ | -------------------- |
| id               | int    | 数据表ID             |
| data_table_name  | string | 数据表名称           |
| db_table_name    | string | 数据表在数据库的名称 |
| dmp_database_id  | int    | 数据表所在数据库ID   |
| datebase_name    | string | 数据库显示名称       |
| db_type          | int    | 数据库格式编号       |
| dmp_data_case_id | int    | 所属案例ID           |
| dmp_user_id      | int    | 添加该数据的用户ID   |
| description      | string | 数据表简介           |
| created_on       | date   | 添加日期             |
| changed_on       | date   | 最后修改时间         |

### 获取数据列信息

**接口描述**




**请求说明**

| URL           | /dbtable/column |
| ------------- | --------------- |
| 格式          | JSON            |
| http 请求方式 | GET             |
| 登陆保护      | 是              |

 **请求参数**

| 参数名   | 类型 | 是否必填 | 最大长度 | 参数说明 |
| -------- | ---- | -------- | -------- | -------- |
| dmp_data_table_id | int  | 是       |          | 数据表ID |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":[
  	{"id":"",
    "dmp_data_table_id":"",
    "dmp_data_table_column_name":"job_name",
    "groupby":"",
    "wherein":"",
    "isdate":"",
    "description":"zhiweimingcheng",}
    ]
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
| id                | int |                    |
| dmp_data_table_id | int                     | 数据ID             |
| dmp_data_table_column_name       | string                  | 列名               |
| groupby           | boolearn           | 可以进行分组       |
| Wherein           | boolearn           | 可以区间筛选       |
| Isdate            | boolearn           | 是否为时间日期字段 |
| description       | string  | 字段说明           |

### 数据列设置

**接口描述**




**请求说明**

| URL           | /dbtable/columnsetting |
| ------------- | ---------------------- |
| 格式          | JSON                   |
| http 请求方式 | POST                   |
| 登陆保护      | 是                     |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
| id                | int      | 是||                    |
| dmp_data_table_id | int      | 是||              |
| dmp_data_table_column_name       | string   | 是||               列名               |
| groupby           | boolearn | 是||          可以进行分组       |
| Wherein           | boolearn | 是||          可以区间筛选       |
| Isdate            | boolearn | 是||          是否为时间日期字段 |
| description       | string   | 是||字段说明           |

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



### 删除数据表关联

**接口描述**

传入数据表ID进行删除数据，表删除表时需同时删除相关的数据列信息表和数据列区间表


**请求说明**

| URL           | /dbtable/del |
| ------------- | ------------ |
| 格式          | JSON         |
| http 请求方式 | GET          |
| 登陆保护      | 是           |

 **请求参数**

| 参数名        | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------------- | ---- | -------- | -------- | -------- |
| dmp_data_table_id | int  | 是       |          | 数据表ID |

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

### 文件上传

**接口描述**

文件上传


**请求说明**

| URL           | /file/upload |
| ------------- | ------------ |
| 格式          | JSON         |
| http 请求方式 | POST         |
| 登陆保护      | 是           |

 **请求参数**

| 参数名  | 类型   | 是否必填 | 最大长度 | 参数说明       |
| ------- | ------ | -------- | -------- | -------------- |
| task_id | string | 是       |          | 文件上传任务id |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
  }
}
```

**result说明:**

| 参数名 | 类型 | 参数说明 |
| ------ | ---- | -------- |
|        |      |          |

### 文件上传完成

**接口描述**

文件上传完成后


**请求说明**

| URL           | /file/success |
| ------------- | ------------- |
| 格式          | JSON          |
| http 请求方式 | GET           |
| 登陆保护      | 是            |

 **请求参数**

| 参数名   | 类型   | 是否必填 | 最大长度 | 参数说明 |
| -------- | ------ | -------- | -------- | -------- |
| task_id  | int    | 是       |          | 任务iD   |
| filename | string | 是       |          | 文件名称 |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
    "filepath":"csv/test.csv"
  }
}
```

**result说明:**

| 参数名   | 类型   | 参数说明           |
| -------- | ------ | ------------------ |
| filepath | string | 数据在服务器的路径 |

### 从数据库添加数据表单

**接口描述**



**请求说明**

| URL           | /form/fromdb |
| ------------- | ------------ |
| 格式          | JSON         |
| http 请求方式 | POST         |
| 登陆保护      | 是           |

 **请求参数**

| 参数名           | 类型   | 是否必填 | 最大长度 | 参数说明           |
| ---------------- | ------ | -------- | -------- | ------------------ |
| data_tablename   | string | 是       |          | 数据表名称         |
| db_tablename     | string | 是       |          | 数据库内数据表名称 |
| database_id      | int    | 是       |          | 数据库ID           |
| dmp_data_case_id | int    | 是       |          | 案例ID             |
| description      | string | 是       |          | 简介               |

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

### 从文件添加数据表单

**接口描述**




**请求说明**

| URL           | /form/fromfile |
| ------------- | -------------- |
| 格式          | JSON           |
| http 请求方式 | POST           |
| 登陆保护      | 是             |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
| filetype                    | Int     | 是     |        | 文件类型                           |
| filepath                    | string   | 是     |         | 文件路径                           |
| column_line                 | Int      |          |         | 列名行号                          |
| column                      | string   |          |         | 自定义列名                         |
| json_dimension_reduction    | Boolearn |          |          | json数据是否遍历存储               |
| destination_dmp_datebase_id | int      | 是    |          | 目标数据库ID                       |
| tablename              | string   | 是    |          | 表名                               |
| method                      | String   | 是    |          | 新建还是添加覆盖                   |
| dmp_data_case_id        | Int      | 是        |     | 所属案例                           |
| description                 | string   |         |          | 说明                               |

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

### 数据迁移表单

**接口描述**




**请求说明**

| URL           | /form/migration/ |
| ------------- | ---------------- |
| 格式          | JSON             |
| http 请求方式 | POST             |
| 登陆保护      | 是               |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
| origin_dmp_table_id         | int      | 是         |      | 起点数据表                         |
| rule                        | dict |             |       | 数据提取规则                       |
| destination_dmp_datebase_id | int      | 是        |       | 目标数据库ID                       |
| new_table_name              | string   | 是        |       | 新表名                             |
| method                      | String   | 是        |       | 覆盖添加新建                       |
| description                 | string   |            |        | 说明                               |
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

### 文件下载表单

**接口描述**




**请求说明**

| URL           | /form/download |
| ------------- | -------------- |
| 格式          | JSON           |
| http 请求方式 | POST           |
| 登陆保护      | 是             |

 **请求参数**

| 参数名            | 类型   | 是否必填 | 最大长度 | 参数说明   |
| ----------------- | ------ | -------- | -------- | ---------- |
| dmp_data_table_id | int    | 非空     |          | 源数据表ID |
| rule              | dict   |          |          | 提取规则   |
| description       | string |          |          |            |

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



### 获取表单信息

**接口描述**




**请求说明**

| URL           | /form/info |
| ------------- | ---------- |
| 格式          | JSON       |
| http 请求方式 | GET        |
| 登陆保护      | 是         |

 **请求参数**

| 参数名 | 类型 | 是否必填 | 最大长度 | 参数说明 |
| ------ | ---- | -------- | -------- | -------- |
|        |      |          |          |          |

**返回结果**

```json
{
 "status": 0,
  "msg": "ok",
  "results":{
    "committed":[
      {"id":"",
      "form_type":1,
      "submit_on":"",
      "submit_dmp_user_id":"",
      "dmp_data_table_name":"",
      "db_table_name":"",
      "dmp_database_id":"",
      "dmp_case_id":"",
      "description":"",
      "approve_dmp_user_id":"",
      "approve_on":"",
      "approve_result":"",
      "answer":"",
      "created_on":"",
      "changed_on":"",
      }
    ],
    "pending":[],
    "complete":[]
  }
}
```

**result说明:**

| 参数名    | 类型 | 参数说明 |
| --------- | ---- | -------- |
| committed |      |          |
| pending   |      |          |
| complete  |      |          |

### 表单审批接口

**接口描述**




**请求说明**

| URL           | /form/approve |
| ------------- | ------------- |
| 格式          | JSON          |
| http 请求方式 | PUT           |
| 登陆保护      | 是            |

 **请求参数**

| 参数名         | 类型   | 是否必填 | 最大长度 | 参数说明                           |
| -------------- | ------ | -------- | -------- | ---------------------------------- |
| dmp_form_type      | int    | 是       |          | 表单格式                           |
| dmp_form_id        | int    | 是       |          | 表单ID                             |
| approve_result | int    | 是       |          | 审批结果,默认为0，通过是1不通过是2 |
| answer         | string | 是       |          | 审批答复                           |

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



### 下载完成

**接口描述**

接收表单ID‘实现对下载完成的，FTP数据进行处理


**请求说明**

| URL           | /file/dl_complete/ |
| ------------- | --------------- |
| 格式          | JSON            |
| http 请求方式 | GET             |
| 登陆保护      | 是              |

 **请求参数**

| 参数名  | 类型 | 是否必填 | 最大长度 | 参数说明         |
| ------- | ---- | -------- | -------- | ---------------- |
| dmp_form_download_id | int  | 是       |          | 文件下载表单的ID |

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

| URL           | / |
| ------------- | ------------------ |
| 格式          | JSON               |
| http 请求方式 | POST               |
| 登陆保护      | 是                 |

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

