# MySQL 表结构设计与 SQL 场景练习手册

> 面向全栈与 AI 应用开发者：从“页面字段映射”升级到“业务规则建模”

## 0. 学习目标与使用方法

这份手册使用 MySQL 8.x。完成后，你应该能独立完成：

```text
需求 → 业务规则 → 实体关系 → 表和字段 → 约束 → 索引 → SQL → 并发检查
```

建议顺序：

1. 阅读基础知识并手敲示例。
2. 阅读建模技巧。
3. 独立完成练习题，不要立即看答案。
4. 用参考答案检查遗漏，而不是机械比较字段名。
5. 每个练习都解释“为什么这样设计”。

---

# 第一部分：SQL 与建表基础

## 1. 从业务实体理解表

### 1.1 表不是页面表单

错误思路：

```text
页面有姓名、角色、权限三个输入框
→ 建 user(name, role, permission)
```

正确思路：

```text
用户、角色、权限是否有各自生命周期？
一个用户有几个角色？
一个角色属于几个用户？
角色名称能否重复？
删除角色后用户怎么办？
```

由此可能得到：

```text
user
role
permission
user_role
role_permission
```

### 1.2 实体、属性与关系

- **实体**：可独立识别、具有生命周期的业务对象，如用户、订单、文档。
- **属性**：描述实体的信息，如用户昵称、订单金额。
- **关系**：实体之间的联系，如订单属于用户。

判断某个名词要不要单独成表，可以问：

1. 它是否有自己的 ID？
2. 它是否会独立新增、修改、删除或查询？
3. 它是否有多个属性？
4. 它是否会被多个对象引用？
5. 它是否需要保存历史？

### 1.3 三种基本关系

#### 一对一

```text
user 1 ── 1 user_profile
```

适合拆分低频、敏感或体积较大的扩展信息。

#### 一对多

```text
user 1 ── N address
```

外键通常放在“多”的一方：`address.user_id`。

#### 多对多

```text
user N ── N role
```

使用中间表：`user_role(user_id, role_id)`。

## 2. 字段类型怎么选

### 2.1 整数

```sql
id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT
age TINYINT UNSIGNED
retry_count INT UNSIGNED NOT NULL DEFAULT 0
```

- ID 通常用 `BIGINT`，给长期增长留空间。
- 小范围状态也可用 `TINYINT`，但可读性需要枚举文档配合。
- 不要为了省几个字节过度优化。

### 2.2 字符串

```sql
username VARCHAR(64) NOT NULL
phone VARCHAR(32) NOT NULL
description TEXT
```

手机号、身份证号、业务编号不是用于计算的数字，应使用字符串。

`VARCHAR(n)` 的 `n` 是字符数上限。长度要基于业务规则，不要所有字段都写 `VARCHAR(255)`。

### 2.3 金额

```sql
amount DECIMAL(18, 2) NOT NULL
```

不要用 `FLOAT` 或 `DOUBLE` 保存金额，因为二进制浮点存在精度误差。

如果业务以分为最小单位，也可以使用整数：

```sql
amount_cent BIGINT NOT NULL
```

### 2.4 日期时间

```sql
birthday DATE
created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
    ON UPDATE CURRENT_TIMESTAMP(3)
```

- `DATE`：只需要日期。
- `DATETIME`：业务时间，范围大，不自动做时区转换。
- `TIMESTAMP`：常用于时间戳，MySQL 会按会话时区转换。

团队必须统一：数据库存 UTC，展示层转换为用户时区，是常见做法。

### 2.5 JSON

```sql
request_params JSON NOT NULL
```

适合：

- 结构变化频繁、主要整体读写的配置。
- 原始第三方响应。
- 不同任务类型差异很大的参数。

不适合：

- 经常用于筛选、JOIN、排序的核心字段。
- 需要外键或唯一约束的业务字段。
- 只是因为暂时“不知道怎么设计”。

MySQL 不能直接给整个 JSON 值建立普通索引；常见方式是提取生成列后索引。

## 3. 字段设计的固定问题

### 3.1 是否允许 NULL

`NULL` 表示未知或不存在，不等于空字符串、0 或空数组。

```sql
name VARCHAR(64) NOT NULL
finished_at DATETIME NULL
```

任务未完成时 `finished_at` 不存在，使用 `NULL` 合理；用户名缺失通常不合理。

### 3.2 默认值

```sql
status VARCHAR(32) NOT NULL DEFAULT 'PENDING'
retry_count INT UNSIGNED NOT NULL DEFAULT 0
```

默认值应代表明确业务语义。不要为了避免 NULL 给所有字符串默认空串。

### 3.3 通用字段

```sql
id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
    ON UPDATE CURRENT_TIMESTAMP(3)
```

按需增加：

```text
created_by       谁创建
updated_by       谁修改
deleted_at       逻辑删除时间
version          乐观锁版本
tenant_id        租户隔离
trace_id         链路追踪
```

不要机械地给所有表添加全部字段。日志表通常只追加，不需要 `updated_at`。

### 3.4 当前值与快照

订单明细不能只保存 `product_id`，还应保存下单时的商品名称和单价：

```sql
product_name VARCHAR(255) NOT NULL,
unit_price DECIMAL(18, 2) NOT NULL
```

商品以后改名、改价，历史订单仍应保持原样。

## 4. 主键、外键与约束

### 4.1 主键

```sql
id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)
```

主键负责数据库行身份；订单号、文件 Hash 等业务标识通常另建唯一索引。

### 4.2 唯一约束

```sql
UNIQUE KEY uk_user_username (username)
```

联合唯一约束：

```sql
UNIQUE KEY uk_user_role (user_id, role_id)
```

它把“同一个用户不能重复拥有同一个角色”变成数据库不可违反的规则。

注意：MySQL 唯一索引允许多个 `NULL`，需要唯一时通常同时设 `NOT NULL`。

### 4.3 外键

```sql
CONSTRAINT fk_address_user
FOREIGN KEY (user_id) REFERENCES user(id)
ON DELETE CASCADE
```

常见删除策略：

- `RESTRICT`：存在引用时拒绝删除。
- `CASCADE`：父记录删除时自动删除子记录。
- `SET NULL`：父记录删除后外键置空，外键必须允许 NULL。

外键可以保护引用完整性，但高并发、大规模系统也可能选择应用层维护。无论是否使用物理外键，关系和约束逻辑都必须明确。

### 4.4 CHECK

```sql
stock INT NOT NULL,
CONSTRAINT ck_product_stock CHECK (stock >= 0)
```

CHECK 是最后防线，但库存扣减仍需带条件的原子更新，不能依赖插入失败作为正常流程。

## 5. CREATE TABLE 完整示例

```sql
CREATE TABLE product (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    sku VARCHAR(64) NOT NULL,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(18, 2) NOT NULL,
    stock INT UNSIGNED NOT NULL DEFAULT 0,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    version INT UNSIGNED NOT NULL DEFAULT 0,
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
        ON UPDATE CURRENT_TIMESTAMP(3),
    PRIMARY KEY (id),
    UNIQUE KEY uk_product_sku (sku),
    KEY idx_product_status_created (status, created_at),
    CONSTRAINT ck_product_price CHECK (price >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

检查结构：

```sql
DESCRIBE product;
SHOW CREATE TABLE product;
SHOW INDEX FROM product;
```

## 6. CRUD 基础

### 6.1 INSERT

```sql
INSERT INTO product (sku, name, price, stock)
VALUES ('SKU-001', 'Mechanical Keyboard', 499.00, 100);
```

批量插入：

```sql
INSERT INTO product (sku, name, price, stock)
VALUES
    ('SKU-002', 'Mouse', 199.00, 50),
    ('SKU-003', 'Monitor', 1299.00, 20);
```

### 6.2 SELECT

```sql
SELECT id, sku, name, price
FROM product
WHERE status = 'ACTIVE' AND price >= 200
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

分页较深时，游标分页通常优于大 OFFSET：

```sql
SELECT id, name
FROM product
WHERE status = 'ACTIVE' AND id < :last_id
ORDER BY id DESC
LIMIT 20;
```

### 6.3 UPDATE

```sql
UPDATE product
SET name = 'Wireless Mechanical Keyboard'
WHERE id = 1;
```

库存扣减：

```sql
UPDATE product
SET stock = stock - 1
WHERE id = 1 AND stock > 0;
```

必须检查 affected rows：0 表示没有库存或记录不存在。

### 6.4 DELETE 与逻辑删除

物理删除：

```sql
DELETE FROM product WHERE id = 1;
```

逻辑删除：

```sql
UPDATE product SET deleted_at = NOW(3) WHERE id = 1;
```

逻辑删除会增加所有查询、唯一约束和数据清理的复杂度，不应默认使用。

## 7. JOIN 与关系查询

### 7.1 INNER JOIN

只返回两边都有匹配的数据：

```sql
SELECT u.id, u.username, r.name AS role_name
FROM user u
JOIN user_role ur ON ur.user_id = u.id
JOIN role r ON r.id = ur.role_id
WHERE u.id = :user_id;
```

### 7.2 LEFT JOIN

保留左表记录，即使右表没有匹配：

```sql
SELECT u.id, u.username, a.city
FROM user u
LEFT JOIN address a ON a.user_id = u.id
WHERE u.status = 'ACTIVE';
```

一个用户有多个地址时，用户会出现多行。这不是数据库重复，而是一对多结果的自然展开。

### 7.3 EXISTS

只关心“是否存在”时：

```sql
SELECT u.id, u.username
FROM user u
WHERE EXISTS (
    SELECT 1
    FROM user_role ur
    JOIN role r ON r.id = ur.role_id
    WHERE ur.user_id = u.id AND r.code = 'ADMIN'
);
```

## 8. 聚合与 BI 查询

```sql
SELECT
    DATE(created_at) AS order_date,
    COUNT(*) AS order_count,
    SUM(total_amount) AS sales_amount
FROM customer_order
WHERE status = 'PAID'
  AND created_at >= '2026-07-01'
GROUP BY DATE(created_at)
HAVING SUM(total_amount) > 10000
ORDER BY order_date;
```

条件聚合：

```sql
SELECT
    COUNT(*) AS total_count,
    SUM(status = 'SUCCEEDED') AS succeeded_count,
    SUM(status = 'FAILED') AS failed_count
FROM report_task;
```

聚合查询要先明确统计口径：按创建时间还是支付时间、退款是否扣除、时区是什么。

## 9. 索引：从查询反推，不从字段猜

查询：

```sql
SELECT id, status, created_at
FROM report_task
WHERE user_id = :user_id AND status = 'FAILED'
ORDER BY created_at DESC
LIMIT 20;
```

候选联合索引：

```sql
KEY idx_task_user_status_created (user_id, status, created_at DESC)
```

### 9.1 联合索引顺序

一般考虑：

1. 等值过滤字段。
2. 范围过滤字段。
3. 排序字段。
4. 选择性与实际查询组合。

最左前缀示意：索引 `(user_id, status, created_at)` 通常能支持：

```text
user_id
user_id + status
user_id + status + created_at
```

不能因为有 `status` 就认为 `WHERE status = ?` 一定能高效使用这个索引。

### 9.2 EXPLAIN

```sql
EXPLAIN ANALYZE
SELECT ...;
```

先关注：

- 是否全表扫描。
- 实际扫描行数。
- 使用了哪个索引。
- 是否出现额外排序或临时表。
- 估算行数和实际行数是否差异很大。

索引不是越多越好：每个索引都会增加写入、存储和维护成本。

## 10. 事务与并发最低要求

```sql
START TRANSACTION;

UPDATE account
SET balance = balance - 100
WHERE id = 1 AND balance >= 100;

UPDATE account
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

需要复杂读取判断时：

```sql
SELECT id, stock
FROM product
WHERE id = 1
FOR UPDATE;
```

乐观锁：

```sql
UPDATE article
SET content = :content, version = version + 1
WHERE id = :id AND version = :old_version;
```

详细并发内容请结合《全栈开发中的并发、事务与数据一致性实战》学习。

---

# 第二部分：表设计技巧

## 11. 八步建模法

### 第一步：写业务规则

不要先写字段。先写完整句子：

```text
一个用户可以拥有多个角色。
一个角色可以分配给多个用户。
同一用户不能重复拥有同一角色。
角色不能在仍被用户使用时直接删除。
```

### 第二步：圈出实体

找名词，再判断它是否有独立生命周期：用户、角色、权限。

### 第三步：确定关系和基数

给每条关系标记 `1:1`、`1:N` 或 `N:N`。

### 第四步：定义身份

- 数据库主键是什么？
- 业务唯一标识是什么？
- 外部系统标识是什么？

### 第五步：定义不变量

把规则翻译成 `NOT NULL`、`UNIQUE`、外键、CHECK、状态条件更新。

### 第六步：画生命周期

```text
PENDING → RUNNING → SUCCEEDED
                  ↘ FAILED
```

生命周期会推导出状态、开始时间、结束时间、错误信息、重试次数等字段。

### 第七步：列出前三个核心查询

没有查询模式，索引设计只能靠猜。

### 第八步：检查并发、历史和删除

- 两个请求同时更新怎么办？
- 是否需要版本号？
- 是否保存历史？
- 删除后关系如何处理？

## 12. 当前状态、历史记录和事件

不要把所有东西都塞在一张主表：

```text
article             当前文章
article_revision    内容版本
approval_record     审批历史
```

主表用于高频读取当前状态，历史表用于追溯。

## 13. 命名技巧

- 表名和字段名使用统一的 snake_case。
- 外键使用 `{entity}_id`。
- 布尔语义使用 `is_enabled`、`has_access`。
- 时间使用动作语义：`created_at`、`published_at`。
- 不使用 `data`、`info`、`type1` 等含糊名称。
- SQL 保留字不要作为字段名。

## 14. 设计检查清单

```text
[ ] 实体与关系是否明确？
[ ] 每张表是否有稳定主键？
[ ] 必填字段是否 NOT NULL？
[ ] 重复数据由什么唯一约束阻止？
[ ] 金额是否使用 DECIMAL 或整数最小单位？
[ ] 状态是否合法，如何流转？
[ ] 是否混淆当前状态和历史记录？
[ ] 删除策略是什么？
[ ] 核心查询是什么？
[ ] 索引是否按查询组合设计？
[ ] 两个请求同时更新会发生什么？
[ ] 是否需要审计、版本或幂等字段？
```

---

# 第三部分：场景练习

> 先完成本部分，再看第四部分答案。字段名称可以不同，但必须解释业务规则。

## 练习 1：用户与地址

需求：

- 用户使用邮箱注册，邮箱不能重复。
- 用户可以保存多个收货地址。
- 每个用户最多有一个默认地址。
- 地址需要保存收件人、手机号、省市区和详细地址。
- 用户可以停用，但历史地址暂时保留。

任务：

1. 设计表和关系。
2. 写完整建表 SQL。
3. 写新增地址 SQL。
4. 写设置默认地址的事务。
5. 查询用户及其默认地址。
6. 设计索引并解释。

## 练习 2：RBAC 权限系统

需求：

- 用户可拥有多个角色。
- 角色可拥有多个权限。
- 用户不能重复绑定同一角色。
- 权限使用稳定的 code，例如 `report:read`。
- 查询用户最终拥有的全部权限，结果不能重复。

任务：设计 5 张表，写绑定角色、授权权限、查询用户权限的 SQL。

## 练习 3：审批发布系统

需求：

- 内容状态：DRAFT、PENDING、APPROVED、REJECTED、PUBLISHED。
- 提交人不能审批自己的内容。
- 每次审批需要保存审批人、意见、前后状态和时间。
- 两个审批人同时操作时，只能有一个成功。
- 需要保存内容历史版本。

任务：设计当前内容、版本、审批记录；写提交、审批和发布的条件更新。

## 练习 4：订单与库存

需求：

- 一个订单有多个商品明细。
- 下单后商品改名、改价不能影响历史订单。
- 订单号、支付流水号不能重复。
- 创建订单和扣库存必须一致。
- 重复提交不能创建两张订单。

任务：设计商品、订单、订单明细、支付记录和幂等约束；写下单事务。

## 练习 5：BI 报表生成任务

需求：

- 用户提交数据集、筛选参数和图表配置生成报表。
- 生成过程异步执行。
- 状态：PENDING、RUNNING、SUCCEEDED、FAILED、CANCELLED。
- 任务可能重试，需要记录失败原因和重试次数。
- 相同幂等键只能创建一个任务。
- 用户经常按状态和创建时间分页查询。

任务：设计任务表、结果字段、状态抢占 SQL 和查询索引。

## 练习 6：RAG 知识库

需求：

- 用户可以创建多个知识库。
- 文档可以加入多个知识库。
- 文档支持版本更新。
- 文档拆分成 chunk，chunk 有顺序和页码。
- 同一知识库不能重复导入同一文件内容。
- 需要保存解析任务状态和错误阶段。
- 向量存储在向量数据库，MySQL 保存关系和追踪信息。

任务：设计知识库、文档、版本、关联、chunk 元数据和导入任务。

## 练习 7：设备报文平台

需求：

- 设备持续上报带序列号和设备时间的报文。
- 重连可能导致报文重复。
- 需要保存原始报文和解析结果。
- 页面高频读取设备最新状态。
- 旧报文不能覆盖新状态。
- 经常按设备和时间范围查询历史。

任务：区分设备、原始报文、解析记录和最新状态表；设计去重和索引。

---

# 第四部分：参考答案与复盘

## 答案 1：用户与地址

```sql
CREATE TABLE app_user (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
        ON UPDATE CURRENT_TIMESTAMP(3),
    UNIQUE KEY uk_user_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_address (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    recipient_name VARCHAR(64) NOT NULL,
    phone VARCHAR(32) NOT NULL,
    province VARCHAR(64) NOT NULL,
    city VARCHAR(64) NOT NULL,
    district VARCHAR(64) NOT NULL,
    detail VARCHAR(255) NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    KEY idx_address_user_default (user_id, is_default),
    CONSTRAINT fk_address_user FOREIGN KEY (user_id)
        REFERENCES app_user(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

MySQL 不能用普通唯一索引简单表达“每个用户最多一个 `is_default=true`，但可有多个 false”。实用做法是在事务中先取消旧默认，再设置新默认，并锁定用户或地址集合：

```sql
START TRANSACTION;
SELECT id FROM app_user WHERE id = :user_id FOR UPDATE;
UPDATE user_address SET is_default = FALSE WHERE user_id = :user_id;
UPDATE user_address
SET is_default = TRUE
WHERE id = :address_id AND user_id = :user_id;
COMMIT;
```

## 答案 2：RBAC

```sql
CREATE TABLE role (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(64) NOT NULL,
    name VARCHAR(128) NOT NULL,
    UNIQUE KEY uk_role_code (code)
);

CREATE TABLE permission (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(128) NOT NULL,
    name VARCHAR(128) NOT NULL,
    UNIQUE KEY uk_permission_code (code)
);

CREATE TABLE user_role (
    user_id BIGINT UNSIGNED NOT NULL,
    role_id BIGINT UNSIGNED NOT NULL,
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    PRIMARY KEY (user_id, role_id),
    KEY idx_user_role_role (role_id)
);

CREATE TABLE role_permission (
    role_id BIGINT UNSIGNED NOT NULL,
    permission_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    KEY idx_role_permission_permission (permission_id)
);
```

用户权限：

```sql
SELECT DISTINCT p.code
FROM user_role ur
JOIN role_permission rp ON rp.role_id = ur.role_id
JOIN permission p ON p.id = rp.permission_id
WHERE ur.user_id = :user_id;
```

## 答案 3：审批发布

核心拆分：

```text
content           当前标题、当前版本、当前状态、version
content_revision  每次内容快照
approval_record   审批操作历史
```

审批抢占：

```sql
UPDATE content
SET status = 'APPROVED', version = version + 1, updated_at = NOW(3)
WHERE id = :id
  AND status = 'PENDING'
  AND version = :old_version
  AND submitter_id <> :reviewer_id;
```

检查 affected rows。状态更新和审批记录 INSERT 必须在同一事务中。

## 答案 4：订单与库存

核心表：

```text
product(id, sku, name, price, stock)
customer_order(id, order_no, user_id, total_amount, status, idempotency_key)
order_item(order_id, product_id, product_name, unit_price, quantity)
payment(id, order_id, transaction_no, amount, status)
```

关键约束：

```sql
UNIQUE KEY uk_order_no (order_no)
UNIQUE KEY uk_order_idempotency (user_id, idempotency_key)
UNIQUE KEY uk_payment_transaction (transaction_no)
```

扣库存：

```sql
UPDATE product
SET stock = stock - :quantity
WHERE id = :product_id AND stock >= :quantity;
```

所有商品扣减、订单和明细写入放在同一事务中；任意商品库存不足则回滚。

## 答案 5：BI 报表任务

```sql
CREATE TABLE report_task (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    dataset_id BIGINT UNSIGNED NOT NULL,
    idempotency_key VARCHAR(128) NOT NULL,
    request_params JSON NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    result_url VARCHAR(1024),
    worker_id VARCHAR(128),
    retry_count INT UNSIGNED NOT NULL DEFAULT 0,
    error_code VARCHAR(64),
    error_message TEXT,
    started_at DATETIME(3),
    finished_at DATETIME(3),
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
        ON UPDATE CURRENT_TIMESTAMP(3),
    UNIQUE KEY uk_report_idempotency (user_id, idempotency_key),
    KEY idx_report_user_status_created (user_id, status, created_at DESC),
    KEY idx_report_status_created (status, created_at)
);
```

抢占：

```sql
UPDATE report_task
SET status = 'RUNNING', worker_id = :worker_id, started_at = NOW(3)
WHERE id = :id AND status = 'PENDING';
```

## 答案 6：RAG 知识库

推荐结构：

```text
knowledge_base
document                       文档逻辑身份
document_revision              文件版本、hash、解析状态
knowledge_base_document        多对多关系及启用状态
document_chunk                 chunk 顺序、页码、向量库 point_id
document_import_task           导入过程、阶段、错误和重试
```

关键约束：

```sql
UNIQUE (document_id, revision_no)
UNIQUE (knowledge_base_id, document_id)
UNIQUE (document_revision_id, chunk_index)
UNIQUE (knowledge_base_id, file_hash)
```

如果同一文档版本可以加入多个知识库，`file_hash` 的去重范围需要根据业务放在文档层或知识库关联层，不能机械套用。

## 答案 7：设备报文

推荐拆分：

```text
device               设备主数据
device_message       原始报文，追加写
message_parse_result 解析结果和版本
device_latest_state  每台设备一行的当前状态
```

原始报文去重：

```sql
UNIQUE KEY uk_message_device_seq (device_id, sequence_no)
KEY idx_message_device_time (device_id, device_time)
```

拒绝旧数据覆盖：

```sql
UPDATE device_latest_state
SET payload = :payload,
    sequence_no = :sequence_no,
    device_time = :device_time
WHERE device_id = :device_id
  AND sequence_no < :sequence_no;
```

历史报文数据量很大时，再根据真实规模评估归档、冷热分离、分区或时序数据库；不要在项目刚开始时过早分库分表。

---

## 最终复盘模板

每设计一张表，都用下面的格式解释：

```text
表解决什么业务问题：
主键和业务唯一键：
与其他表的关系：
关键 NOT NULL：
关键唯一约束：
状态与生命周期：
前三个核心查询：
索引及其对应查询：
并发写入风险：
删除与历史策略：
```

## 参考资料

- [MySQL 8.4 CREATE TABLE](https://dev.mysql.com/doc/refman/8.4/en/create-table.html)
- [MySQL Creating a Table](https://dev.mysql.com/doc/refman/8.4/en/creating-tables.html)
- [MySQL Optimization and Indexes](https://dev.mysql.com/doc/refman/8.4/en/optimization-indexes.html)

