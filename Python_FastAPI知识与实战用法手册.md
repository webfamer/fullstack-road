# Python FastAPI 知识与实战用法手册

> 面向正在用 AI 编写 Python 项目的全栈开发者

## 0. 这份手册的目标

读完后，你应该可以：

- 看懂并修改 AI 生成的 FastAPI 项目。
- 独立设计 API、Pydantic 模型、依赖和业务层。
- 正确使用 `async/await`、SQLAlchemy `AsyncSession` 和事务。
- 实现鉴权、异常处理、日志、测试与部署。
- 为 RAG、Agent、文件解析和 SSE 流式接口选择合适实现。
- 识别“代码能跑但生产会出问题”的写法。

示例使用 Python 3.11+、Pydantic v2、SQLAlchemy 2.x 风格。

---

# 第一部分：先补够用的 Python

## 1. 类型标注是 FastAPI 的核心

FastAPI 通过类型标注判断参数来源、执行校验并生成 OpenAPI。

```python
def find_user(user_id: int, include_disabled: bool = False) -> dict | None:
    ...
```

常见类型：

```python
name: str
age: int
price: float
enabled: bool
tags: list[str]
metadata: dict[str, str]
user_id: int | None
```

`Optional[str]` 与 `str | None` 表达相同类型，但“可为 None”不等于“参数可省略”。是否必填还取决于默认值：

```python
class Example(BaseModel):
    value1: str | None        # 必须提供，但值可以是 null
    value2: str | None = None # 可以省略
```

## 2. dataclass、Pydantic 与 ORM 模型不要混用

- `dataclass`：普通 Python 数据对象。
- Pydantic `BaseModel`：输入输出校验、序列化、JSON Schema。
- SQLAlchemy ORM Model：数据库映射和持久化状态。

不要让一个类承担全部职责。典型拆分：

```text
UserCreate       API 创建输入
UserUpdate       API 更新输入
UserRead         API 输出
User             SQLAlchemy ORM 实体
```

## 3. 异常与上下文管理器

```python
try:
    result = await call_service()
except TimeoutError as exc:
    raise ExternalServiceError("service timed out") from exc
finally:
    await resource.close()
```

数据库事务、文件和网络连接通常使用上下文管理器，确保异常时正确释放资源：

```python
async with session.begin():
    ...
```

## 4. 虚拟环境与依赖

使用项目级虚拟环境，不把依赖装到系统 Python。

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic-settings
```

或使用 `uv`：

```bash
uv init
uv add fastapi uvicorn pydantic-settings
uv run uvicorn app.main:app --reload
```

生产依赖应锁定版本并经过升级测试，不要依赖“AI 当前记得的版本”。

---

# 第二部分：FastAPI 核心

## 5. 最小应用

```python
from fastapi import FastAPI

app = FastAPI(title="AI Platform API", version="1.0.0")

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
```

运行：

```bash
uvicorn app.main:app --reload
```

常用地址：

```text
/docs       Swagger UI
/redoc      ReDoc
/openapi.json
```

## 6. 路径、查询与请求体

```python
from typing import Annotated

from fastapi import Body, Path, Query
from pydantic import BaseModel, Field

class ReportCreate(BaseModel):
    dataset_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=128)
    filters: dict[str, object] = Field(default_factory=dict)

@app.post("/datasets/{dataset_id}/reports")
async def create_report(
    dataset_id: Annotated[int, Path(gt=0)],
    payload: ReportCreate,
    preview: Annotated[bool, Query()] = False,
) -> dict:
    return {
        "dataset_id": dataset_id,
        "preview": preview,
        "payload": payload.model_dump(),
    }
```

FastAPI 的判断规则：

- 出现在路径模板中的标量参数：Path。
- 其他标量参数：通常是 Query。
- Pydantic 模型：Body。
- `Header`、`Cookie`、`File` 等需显式声明。

不要在 GET 中设计复杂请求体；中间代理和文档工具可能不支持。

## 7. Pydantic v2 模型

### 7.1 输入校验

```python
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_type: Literal["RAG", "TEXT_TO_SQL"]
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=50)

    @field_validator("question")
    @classmethod
    def question_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("question cannot be blank")
        return value
```

`extra="forbid"` 可以阻止客户端悄悄传入未定义字段，适合严格 API。

### 7.2 创建、更新、输出分开

```python
class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    nickname: str | None = None
    enabled: bool | None = None

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    nickname: str | None
```

输出模型不能包含密码 Hash、内部错误栈或敏感 Token。

### 7.3 PATCH 的未设置字段

```python
changes = payload.model_dump(exclude_unset=True)
```

这能区分“客户端没传字段”和“客户端明确传 null”。

## 8. 响应模型与状态码

```python
from fastapi import status

@app.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(payload: UserCreate):
    ...
```

`response_model` 的价值：

- 序列化与校验输出。
- 过滤未声明字段。
- 生成 OpenAPI。
- 防止 ORM 对象中的敏感字段意外返回。

常见状态码：

```text
200 查询或更新成功
201 创建成功
202 已接受，异步处理中
204 成功但无响应体
400 请求语义错误
401 未认证
403 已认证但无权限
404 资源不存在
409 状态冲突、重复提交、乐观锁失败
422 请求校验失败
429 请求过多
500 未预期服务端错误
503 依赖暂时不可用
```

## 9. APIRouter 与项目结构

推荐从小而清晰开始：

```text
app/
├── main.py
├── core/
│   ├── config.py
│   ├── errors.py
│   ├── logging.py
│   └── security.py
├── db/
│   ├── base.py
│   ├── session.py
│   └── models/
├── modules/
│   ├── users/
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── repository.py
│   └── rag/
│       ├── router.py
│       ├── schemas.py
│       ├── service.py
│       └── repository.py
└── tests/
```

路由器：

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int):
    ...
```

注册：

```python
app.include_router(user_router, prefix="/api/v1")
```

避免两个极端：

- 所有逻辑都写在 `main.py`。
- 一个简单 CRUD 被拆成十几层抽象。

## 10. 依赖注入 Depends

依赖注入适合：

- 数据库 Session
- 当前用户
- 权限校验
- 配置或客户端
- 分页参数
- 请求级上下文

```python
from typing import Annotated

from fastapi import Depends, Header, HTTPException

async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    if not authorization:
        raise HTTPException(401, "missing token")
    return await decode_and_load_user(authorization)

CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/me", response_model=UserRead)
async def read_me(current_user: CurrentUser):
    return current_user
```

Depends 会形成依赖图，并复用同一请求内相同依赖的结果（默认缓存）。不要把它当成全局单例容器。

---

# 第三部分：async、阻塞与并发

## 11. 什么时候使用 async def

如果调用库提供可等待的异步 API：

```python
@app.get("/documents/{document_id}")
async def get_document(document_id: int):
    return await async_repository.get(document_id)
```

如果使用阻塞库，普通 `def` 路由会由 FastAPI 放在线程池执行：

```python
@app.get("/legacy")
def legacy_call():
    return blocking_client.fetch()
```

错误写法：

```python
@app.get("/bad")
async def bad():
    time.sleep(5)  # 阻塞事件循环
    return {"ok": True}
```

### 11.1 CPU 密集任务

PDF OCR、大文件解析、Embedding 本地推理等 CPU 密集任务不适合直接占用 API 事件循环。可选：

- 进程池。
- 独立 worker。
- Celery、Arq、RQ 等任务队列。
- 专门推理服务。

`BackgroundTasks` 不是可靠任务队列，进程重启可能丢任务，也不适合长时间重任务。

## 12. 并发不是无限并行

```python
semaphore = asyncio.Semaphore(8)

async def embed(text: str):
    async with semaphore:
        return await embedding_client.embed(text)
```

还要同时考虑：

- 数据库连接池大小。
- 下游 API 限流。
- HTTP 客户端连接池。
- Uvicorn worker 数量。
- 内存和 CPU。

不要为每个请求创建新的 HTTP Client 或数据库 Engine。

---

# 第四部分：配置与生命周期

## 13. Pydantic Settings

```python
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Platform"
    environment: str = "development"
    database_url: str
    redis_url: str
    jwt_secret: str

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

原则：

- 密钥不写入代码和 Git。
- 配置启动时校验，缺失则尽早失败。
- `.env` 用于本地开发，不是生产密钥管理系统。
- 日志禁止打印完整配置对象。

## 14. lifespan

官方推荐使用 lifespan 管理启动与关闭资源：

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = AsyncClient(timeout=30)
    await warm_up_models()
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)
```

适合管理：

- HTTP Client
- 数据库 Engine
- Redis 连接池
- 模型或配置预热
- 关闭清理

不要把每个请求需要的事务 Session 做成全局共享对象。

---

# 第五部分：SQLAlchemy 2.x 异步数据库

## 15. Engine 与 Session

```python
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session:
        yield session

DbSession = Annotated[AsyncSession, Depends(get_session)]
```

关键边界：

- Engine/连接池可以全局复用。
- 每个请求或每个工作单元创建独立 Session。
- `AsyncSession` 是有状态对象，不能被多个并发任务共享。

错误示例：

```python
global_session = SessionFactory()  # 不要让所有请求共享
```

## 16. ORM 模型

```python
from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
```

生产环境使用 Alembic Migration 管理表结构，不要在每次启动时直接 `create_all()` 代替迁移。

## 17. 查询

```python
from sqlalchemy import select

stmt = select(User).where(User.email == email)
result = await session.execute(stmt)
user = result.scalar_one_or_none()
```

列表：

```python
stmt = (
    select(User)
    .where(User.enabled.is_(True))
    .order_by(User.id.desc())
    .limit(20)
)
users = list((await session.scalars(stmt)).all())
```

避免在循环中逐条查询关联数据造成 N+1，按需要使用 `selectinload`、JOIN 或批量查询。

## 18. 事务

```python
async def create_order(session: AsyncSession, payload: OrderCreate):
    async with session.begin():
        result = await session.execute(
            update(Product)
            .where(Product.id == payload.product_id)
            .where(Product.stock >= payload.quantity)
            .values(stock=Product.stock - payload.quantity)
        )

        if result.rowcount != 1:
            raise ConflictError("insufficient stock")

        order = Order(...)
        session.add(order)
        await session.flush()  # 获取数据库生成的 ID，但还没有提交
        return order
```

不要在 repository 每执行一条 SQL 就自动 commit，这会破坏跨多个 repository 的业务事务。

推荐边界：service/use-case 层决定事务，repository 负责数据访问。

---

# 第六部分：业务分层与异常

## 19. 路由层不要堆业务逻辑

```python
@router.post("/reports", response_model=ReportRead, status_code=201)
async def create_report(
    payload: ReportCreate,
    session: DbSession,
    current_user: CurrentUser,
):
    return await report_service.create(
        session=session,
        user_id=current_user.id,
        payload=payload,
    )
```

推荐职责：

```text
router       HTTP 参数、状态码、响应模型
service      业务规则、事务边界、流程编排
repository   SQL 与持久化
schemas      API 输入输出模型
models       ORM 模型
client       外部服务适配
```

## 20. 业务异常与全局处理

```python
class AppError(Exception):
    status_code = 500
    code = "INTERNAL_ERROR"

    def __init__(self, message: str):
        self.message = message

class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"

class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"
```

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "request_id": getattr(request.state, "request_id", None),
        },
    )
```

客户端错误返回稳定 code；完整异常栈只写服务端日志，不能返回生产客户端。

## 21. 统一响应体要谨慎

并非所有 API 都需要包成：

```json
{"code": 0, "data": {}, "message": "success"}
```

HTTP 状态码、响应模型和错误结构本身已经能表达语义。若团队统一包裹，需要确保：

- 不能所有错误都返回 HTTP 200。
- 文件流、SSE、204 响应不强行包裹。
- OpenAPI 模型仍然准确。

---

# 第七部分：鉴权与安全

## 22. JWT 基础

JWT 通常是签名令牌，不是加密容器。不要放密码、身份证、敏感业务数据。

```python
from datetime import datetime, timedelta, timezone

import jwt

def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=30),
        "type": "access",
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
```

验证时必须固定允许的算法，检查 `exp`、`sub` 和 token 类型。

密码必须使用专用密码 Hash 算法，例如 Argon2 或 bcrypt；不能使用 MD5、SHA-256 直接保存密码。

## 23. 认证与授权分开

- 认证：你是谁？
- 授权：你能做什么？

```python
def require_permission(code: str):
    async def dependency(current_user: CurrentUser):
        if code not in current_user.permissions:
            raise HTTPException(403, "permission denied")
        return current_user
    return dependency
```

对象级权限也必须检查，例如用户有 `document:read` 权限，不代表能读取任意租户的文档。

## 24. 基本安全清单

```text
[ ] 输入通过 Pydantic 验证
[ ] SQL 使用参数化或 ORM，不拼接用户输入
[ ] 密码使用密码哈希
[ ] JWT 有过期时间且固定验证算法
[ ] CORS 只允许需要的来源
[ ] 上传文件限制大小、类型和文件名
[ ] 日志脱敏 Token、密码和个人信息
[ ] 外部 URL 防 SSRF
[ ] 返回模型不包含内部字段
[ ] 管理接口具有明确权限
```

---

# 第八部分：中间件、日志和可观测性

## 25. 请求 ID 中间件

```python
from uuid import uuid4

from fastapi import Request

@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

生产日志建议结构化：

```json
{
  "level": "INFO",
  "event": "report_created",
  "request_id": "...",
  "user_id": 123,
  "report_id": 456,
  "duration_ms": 28
}
```

不要只记录“操作失败”。至少记录事件、标识、阶段、耗时和可操作错误原因。

## 26. 健康检查

```text
/health/live    进程是否存活
/health/ready   是否可以接收流量
```

readiness 可检查关键依赖，但要设置很短超时，不能让健康检查本身拖垮数据库。

---

# 第九部分：文件、后台任务与 AI 场景

## 27. 文件上传

```python
from fastapi import File, UploadFile

@router.post("/documents")
async def upload_document(file: Annotated[UploadFile, File()]):
    if file.content_type not in {"application/pdf", "text/plain"}:
        raise HTTPException(415, "unsupported file type")

    content = await file.read(1024 * 1024 + 1)
    if len(content) > 1024 * 1024:
        raise HTTPException(413, "file too large")
```

真实大文件不要一次读入内存，应分块写对象存储并在网关和应用两层限制大小。

不要信任客户端文件名，避免路径穿越；不要只根据 `content_type` 判断真实类型。

## 28. BackgroundTasks 的边界

```python
from fastapi import BackgroundTasks

@router.post("/notifications", status_code=202)
async def send_notification(
    payload: NotificationCreate,
    tasks: BackgroundTasks,
):
    tasks.add_task(send_email, payload.email)
    return {"accepted": True}
```

适合短小、允许进程退出时丢失的附加工作。以下任务应使用可靠队列：

- 文档解析与 Embedding。
- 长报表生成。
- 必须重试的通知。
- 跨多个 worker 协调的任务。

## 29. SSE 流式接口

```python
import json

from fastapi.responses import StreamingResponse

async def event_stream():
    async for event in agent.run_stream():
        data = json.dumps(event, ensure_ascii=False)
        yield f"event: progress\ndata: {data}\n\n"

@router.post("/agent/runs/stream")
async def stream_agent(payload: AgentRunCreate):
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
```

需要考虑：

- 客户端断开后取消下游任务。
- 心跳保持连接。
- 代理缓冲。
- 每个事件的 ID 和重连策略。
- 生成结果和任务状态持久化。
- 不在生成器里共享同一个全局 DB Session。

## 30. RAG/Agent API 建议

```text
POST /agent/runs             创建 run，返回 202 + run_id
GET  /agent/runs/{run_id}    查询状态
GET  /agent/runs/{run_id}/events  SSE 订阅事件
POST /agent/runs/{run_id}/cancel  请求取消
```

状态：

```text
PENDING → RUNNING → SUCCEEDED
                  ↘ FAILED
                  ↘ CANCELLED
```

关键字段：

```text
run_id
thread_id
status
current_node
input
output
error_code
error_message
started_at
finished_at
```

`thread_id` 用于会话状态，`run_id` 标识一次执行，`idempotency_key` 防止重复创建；三者不要混为一谈。

---

# 第十部分：测试

## 31. TestClient

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

## 32. 依赖覆盖

```python
def fake_current_user():
    return User(id=1, email="test@example.com")

app.dependency_overrides[get_current_user] = fake_current_user
```

测试结束要清理覆盖，避免测试互相污染。

## 33. 异步测试

```python
import pytest
from httpx import ASGITransport, AsyncClient

@pytest.mark.anyio
async def test_create_report():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/reports",
            json={"dataset_id": 1, "name": "Sales", "filters": {}},
        )
    assert response.status_code == 201
```

测试层次：

```text
单元测试       纯 service、校验和状态机
集成测试       API + 测试数据库/Redis
契约测试       OpenAPI 和外部接口适配
并发测试       幂等、库存、任务抢占
端到端测试     关键业务链路
```

不要大量 mock 数据库 ORM 行为，复杂 mock 容易和真实数据库行为偏离。

---

# 第十一部分：部署与生产检查

## 34. Uvicorn 与 worker

开发：

```bash
uvicorn app.main:app --reload
```

生产不要使用 `--reload`。worker 数量需要压测，不是固定“CPU × 2 + 1”。

多个 worker 表示多个进程：

- 内存变量不共享。
- `asyncio.Lock` 不能跨 worker。
- 每个 worker 有自己的连接池，注意总连接数。
- lifespan 会在每个 worker 执行。

## 35. 容器与优雅关闭

容器化时：

- 让应用进程接收 SIGTERM。
- 设置合理的关闭宽限时间。
- readiness 先摘流量，再等待请求结束。
- 长任务需要可恢复，而不是只存在进程内存。
- 数据库 Migration 作为独立部署步骤运行。

## 36. 性能不要先猜

按顺序检查：

1. 日志和追踪确认慢在哪里。
2. 数据库使用 `EXPLAIN ANALYZE`。
3. 检查 N+1 和连接池等待。
4. 检查同步阻塞代码。
5. 检查下游模型/API 延迟。
6. 再决定缓存、批处理或异步化。

---

# 第十二部分：AI 生成 FastAPI 代码审查清单

## 37. 高频错误

### 错误 1：路由直接写所有逻辑

结果：事务、权限和测试难以维护。把业务规则移入 service。

### 错误 2：所有函数都写 async

如果里面调用 `requests`、`time.sleep`、同步 SDK，事件循环仍然被阻塞。

### 错误 3：共享 AsyncSession

一个 Session 对应一个有状态事务上下文，不能并发共享。

### 错误 4：自己捕获所有 Exception 并返回 200

这会破坏状态码、隐藏故障并让监控失真。

### 错误 5：ORM 模型直接作为输入输出

容易越权更新字段、泄漏密码 Hash，并把 API 与数据库结构强耦合。

### 错误 6：每个请求创建 Engine 或 HTTP Client

失去连接池价值，增加握手和资源消耗。

### 错误 7：在请求中执行长任务

导致超时、重试和重复执行。应创建持久化任务并交给 worker。

### 错误 8：用 BackgroundTasks 保证可靠任务

它没有持久化、ACK、重试和分布式调度语义。

### 错误 9：JWT 里放敏感信息

JWT 通常可被客户端解码，只能依赖签名防篡改。

### 错误 10：用 create_all 管理生产表结构

它不能替代可审计、可回滚的 Migration。

## 38. 提交前检查

```text
[ ] 输入和输出使用独立 Pydantic 模型
[ ] 输出模型不暴露敏感字段
[ ] async 路由中没有阻塞调用
[ ] 每个请求使用独立 AsyncSession
[ ] 事务边界位于业务层
[ ] 不在事务中调用长时间外部服务
[ ] 所有 SQL 参数化
[ ] 鉴权区分 401 和 403
[ ] 业务冲突使用 409
[ ] 错误日志包含 request_id 且已脱敏
[ ] HTTP Client、Engine 等资源正确复用和关闭
[ ] 长任务可持久化、重试和恢复
[ ] 核心接口有成功、失败、权限和并发测试
[ ] 配置与密钥不写入仓库
[ ] Migration 与部署步骤明确
```

---

# 第十三部分：推荐练习

## 练习 1：用户 CRUD

要求：

- 创建、查询、PATCH 更新用户。
- 创建与输出 Schema 分离。
- 邮箱唯一冲突返回 409。
- 使用 Alembic Migration。
- service 决定事务。

## 练习 2：JWT + RBAC

要求：

- 登录签发短期 access token。
- 密码 Hash。
- 当前用户依赖。
- `report:read`、`report:create` 权限依赖。
- 对象级 user_id/tenant_id 校验。

## 练习 3：异步报表任务

要求：

- 创建任务返回 202。
- 幂等键防重复。
- worker 条件更新抢占任务。
- 查询任务状态。
- SSE 输出进度。
- 失败后有限重试。

## 练习 4：RAG 文档导入

要求：

- 流式上传并限制大小。
- 文件 Hash 去重。
- 导入任务持久化。
- 分块处理并限制 Embedding 并发。
- 保存 chunk 元数据和向量 ID。
- 重试不会重复写 chunk。

## 练习 5：Agent Run API

要求：

- 区分 thread_id、run_id、idempotency_key。
- checkpoint 恢复状态。
- 有副作用节点幂等。
- 支持 SSE、取消、失败查询。
- 测试重复创建与重复节点执行。

---

## 推荐学习顺序

```text
类型标注与 Pydantic
→ 路由、状态码、响应模型
→ Depends 与项目分层
→ async 与阻塞边界
→ SQLAlchemy Session 与事务
→ 鉴权、异常、日志
→ 测试
→ 文件、SSE、任务队列
→ 部署与性能
```

## 参考资料

- [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI Concurrency and async/await](https://fastapi.tiangolo.com/async/)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- [FastAPI OAuth2 and JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [SQLAlchemy Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/)

