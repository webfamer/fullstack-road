# NestJS 面试题与参考答案

> 欢迎来到 NestJS 面试题与答案仓库！

- 本仓库旨在为准备面试的 NestJS 开发者提供一份尽可能全面的资料。不论你是刚入门，还是已有实战经验，这份问答集合都可以帮助你系统复习 NestJS 知识，并在面试中更好地发挥。
  > 如果你喜欢这个项目，欢迎点个 ⭐；如果你也想参与贡献，也非常欢迎。在开始之前，请先花一点时间阅读项目指南。

## 重要链接

- [行为准则](./CODE_OF_CONDUCT.md)：希望所有参与本项目的人都遵守行为准则，请务必先了解并遵循相关要求。

- [贡献指南](./CONTRIBUTING.md)：在参与贡献之前，请先阅读贡献指南。里面说明了如何提交问题、反馈 issue 等内容。

> 欢迎关注我 [@gasangw](https://github.com/gasangw)。

### <a id="table-of-contents"></a>目录

| 编号 | 问题 |
| --- | --- |
| 1 | [什么是 NestJS？](#what-is-nestjs) |
| 2 | [NestJS 是谁开发的？为什么要开发它？](#who-developed-nestjs-why-did-they-develop-nestjs) |
| 3 | [NestJS 最早是什么时候发布的？](#when-was-nestjs-first-released) |
| 4 | [如何在本地安装 NestJS 并创建一个新项目？](#how-can-you-install-nestjs-and-set-up-a-new-project-on-your-machine) |
| 5 | [NestJS 和 Angular 有什么区别？](#what-s-the-difference-between-nestjs-and-angular?) |
| 6 | [NestJS 能否配合 C++、Ruby、Python 等其他语言一起使用？如果可以，怎么做？](#is-it-possible-to-use-other-languages-like-c-ruby-or-python-with-nestjs-if-yes-then-how) |
| 7 | [NestJS 应用的核心组成部分有哪些？](#what-are-the-main-components-of-a-nestjs-application) |
| 8 | [如何在 Nest.js 中把一个类声明为控制器？](#how-to-declare-a-class-as-a-controller-in-nestjs) |
| 9 | [能否说明一下如何在 NestJS 控制器中使用装饰器？](#can-you-explain-how-to-use-decorators-in-a-nestjs-controller) |
| 10 | [如何在 NestJS 控制器中使用路由参数？](#how-can-you-use-route-parameters-in-a-nestjs-controller) |
| 11 | [`@Body()` 装饰器的作用是什么？](#what-is-the-role-of-the-body-decorator) |
| 12 | [在 NestJS 中，拦截器（Interceptor）是什么？](#what-is-an-interceptor-in-the-context-of-nestjs) |
| 13 | [在 NestJS 中，管道（Pipe）是什么？](#what-are-pipes-in-the-context-of-nestjs) |
| 14 | [在 NestJS 中，守卫（Guard）是什么？](#what-are-guards-in-the-context-of-nestjs) |
| 15 | [在 NestJS 中，中间件（Middleware）是什么？](#what-are-middlewares-in-the-context-of-nestjs) |
| 16 | [请解释 NestJS 中的依赖注入（Dependency Injection）概念。它如何帮助我们构建模块化且易于测试的应用？](#explain-the-concept-of-dependency-injection-in-nestjs-how-does-it-help-in-building-modular-and-testable-applications) |
| 17 | [`@Injectable()` 和 `@Inject()` 装饰器有什么区别？](#what-s-the-difference-between-injectable-and-inject-decorators) |
| 18 | [Nest 的 Logger 和普通的 `console.log()` 有什么区别？分别适合在什么场景下使用？](#how-does-the-nest-logger-differ-from-the-standard-console-log-and-when-would-you-prefer-one-over-the-other) |
| 19 | [拦截器和中间件有什么区别？](#what-is-the-difference-between-interceptors-and-middleware) |
| 20 | [NestJS 最适合搭配哪些测试框架？](#what-testing-frameworks-work-best-with-nestjs) |
| 21 | [请解释 DTO（Data Transfer Object，数据传输对象）在 NestJS 中的作用。](#explain-the-purpose-of-dtos-data-transfer-objects-in-nestjs.) |
| 22 | [如何在 NestJS 中处理异步操作？Promise 在其中扮演什么角色？](#how-can-you-handle-asynchronous-operations-in-nestjs-and-what-is-the-role-of-the-promise-object) |
| 23 | [请解释 `@InjectRepository()` 装饰器在 NestJS 中的用途。](#explain-the-purpose-of-the-injectrepository-decorator-in-nestjs) |
| 24 | [请解释 `@nestjs/jwt` 包在 NestJS 中的作用。](#explain-the-purpose-of-the-nestjs-jwt-package-in-nestjs) |
| 25 | [请说明 Token 在 API 授权中的使用方式。认证（Authentication）和授权（Authorization）有什么区别？基于 Token 的实现流程是怎样的？](#discuss-how-tokens-are-used-for-authorization-in-an-api-what-is-the-difference-between-authentication-and-authorization-and-how-are-these-processes-implemented-with-tokens) |
| 26 | [为什么 Token 必须设置过期时间？在 NestJS 中如何实现 Token 过期？Refresh Token 在维持用户会话时起什么作用？](#why-is-it-important-for-tokens-to-have-an-expiration-time-How-can-you-implement-token-expiration-in-nestjs-and-what-role-do-refresh-tokens-play-in-maintaining-user-sessions) |
| 27 | [请描述 NestJS 中的 Token 刷新机制。如何实现自动刷新 Token，以维持用户会话？](#describe-the-mechanism-for-a-token-refresh-in-nestjs-how-can-you-implement-an-automatic-token-refresh-strategy-to-maintain-user-sessions) |
| 28 | [NestJS 如何支持认证与授权？](#how-does-nestjs-support-authentication-and-authorization) |
| 29 | [NestJS 中 Provider 和 Service 有什么区别？Provider 能否不使用 `@Injectable()`？请举例说明。](#what-is-the-difference-between-provider-and-services-in-nestjs-can-we-have-a-provider-without-an-injectable-decorator-give-examples.) |
| 30 | [什么是自定义 Provider？它和 Nest.js 中的标准 Provider 有什么区别？](#what-are-custom-providers-and-how-do-they-differ-from-standard-providers-in-nestjs) |
| 31 | [如何在 NestJS 中使用 Swagger 生成 API 文档？为什么要做接口文档，它对开发者有什么价值？](#how-can-you-generate-api-documentation-using-swagger-in-nestjs-discuss-the-importance-of-documenting-your-api-and-how-it-benefits-developers) |
| 32 | [请解释 `@nestjs/swagger` 中 `ApiProperty()`、`ApiOperation()` 装饰器的作用。](#explain-the-purpose-of-the-nestjs-swagger-apiproperty-apioperation-decorators) |
| 33 | [请解释 Dockerfile 在 NestJS 应用中的作用，以及它如何帮助实现容器化。](#explain-the-purpose-of-the-dockerfile-in-a-nestjs-application-and-how-it-facilitates-containerization) |
| 34 | [如何在 NestJS 中使用 Docker Compose？它在多容器场景中的作用是什么？](#how-can-you-use-docker-compose-with-nestjs-and-what-is-its-role-in-a-multi-container-setup) |
| 35 | [`@nestjs/passport` 包的作用是什么？它如何帮助 NestJS 实现认证？](#what-is-the-purpose-of-the-nestjs-passport-package-and-how-does-it-facilitate-authentication-in-nestjs) |
| 36 | [如何在 NestJS 中处理文件上传？Multer 库扮演什么角色？](#how-can-you-handle-file-uploads-in-nestjs-and-what-is-the-role-of-the-multer-library) |
| 37 | [NestJS 如何处理数据库交互？支持哪些数据库方案？](#how-does-nestjs-handle-database-interactions-and-what-are-the-supported-databases) |
| 38 | [什么是 NestJS 中的循环依赖（dependency cycle）？如何解决？](#what-is-circular-dependency-dependency-cycle-in-nestjs-and-how-can-they-be-fixed) |
| 39 | [如何在 NestJS 中处理错误？](#how-can-you-handle-errors-in-nestjs) |
| 40 | [NestJS 如何处理 CORS（跨域资源共享）？](#how-does-nestjs-handle-cors-cross-origin-resource-sharing) |
| 41 | [ExecutionContext 在 NestJS Middleware 中的作用是什么？](#explain-the-purpose-of-the-executioncontext-in-nestjs-middleware) |
| 42 | [如何在 NestJS + TypeORM 中实现软删除？为什么有些场景下软删除比硬删除更合适？](#how-can-you-implement-soft-deletes-in-nestjs-using-typeorm-and-why-might-soft-deletes-be-preferred-over-hard-deletes) |
| 43 | [请解释 NestJS 中环境变量的概念，以及它如何用于配置管理。](#explain-the-concept-of-environment-variables-in-nestjs-and-how-can-they-be-utilized-for-configuration-management) |
| 44 | [TypeORM 中迁移脚本（Migration）的作用是什么？如何在 NestJS 应用中创建并执行迁移？](#what-is-the-role-of-migration-scripts-in-typeorm-and-how-can-you-create-and-run-migrations-in-a-nestjs-application) |
| 45 | [ExecutionContext 在 NestJS 中的用途是什么？](#what-is-the-purpose-of-executioncontext-in-nestjs) |
| 46 | [`@Res()` 装饰器在 NestJS 控制器中的作用是什么？](#what-is-the-purpose-of-the-res-decorator-in-nestjs-controllers) |
| 47 | [请解释 NestJS 中各种模块（Module）的类型与作用。](#explain-the-various-modules-in-nestjs) |
| 48 | [如何保护你的 NestJS 应用安全？](#how-can-you-secure-your-nestjs-application) |
| 49 | [NestJS 应用的入口文件是什么？](#what-is-the-entry-file-of-nestjs-application) |
| 50 | [依赖注入（DI）和控制反转（IoC）有什么区别？](#what-is-the-difference-between-dependency-injection-and-inversion-of-control-ioc) |
| 51 | [如何在 NestJS 中实现缓存？](#how-can-you-implement-caching-in-nestjs) |
| 52 | [请解释依赖倒置原则（DIP）在 NestJS 中的作用。](#explain-the-purpose-of-the-dependency-inversion-principle-dip-in-nestjs) |
| 53 | [如何在 NestJS 中实现任务调度？](#how-can-you-schedule-tasks-in-nestjs) |
| 54 | [如何在 NestJS 中处理数据库事务？为什么某些场景必须使用事务？](#how-can-you-handle-database-transactions-in-nestjs-and-why-are-transactions-important-in-certain-scenarios) |
| 55 | [如何在 NestJS API 中实现版本控制？](#how-can-you-implement-versioning-in-nestjs-api) |
| 56 | [请解释 `@nestjs/graphql` 中 `Resolver` 与 `Scalar` 装饰器的作用，以及它们与 GraphQL 的关系。](#explain-the-purpose-of-the-nestjs-graphql-resolver-and-nestjs-graphql-scalar-decorators-and-how-they-relate-to-graphql-in-nestjs) |
| 57 | [请解释 NestJS 中的序列化（Serialization）与反序列化（Deserialization）。](#explain-the-concept-of-serialization-and-deserialization-in-nestjs) |
| 58 | [请解释 NestJS 中间件在微服务场景下的作用，并举一个适合使用中间件的微服务案例。](#explain-the-role-of-nestjs-middleware-in-the-context-of-microservices-and-provide-a-scenario-where-middleware-is-beneficial-in-a-microservices-setup) |
| 59 | [请说明紧耦合、松耦合等不同类型的耦合，并举例说明 NestJS 模块如何帮助模块化应用实现松耦合。](#discuss-the-different-types-of-coupling-such-as-tight-coupling-and-loose-coupling-and-provide-examples-of-how-nestjs-modules-contribute-to-achieving-loose-coupling-in-a-modularized-application) |
| 60 | [NestJS 如何支持 SSE（Server-Sent Events，服务器发送事件）？它在 Web 实时通信中的主要优势是什么？](#how-does-nestjs-support-server-sent-events-sse-and-what-are-the-primary-advantages-of-using-sse-for-real-time-communication-in-web-applications) |

### 答案

1. ### <a id="what-is-nestjs"></a>什么是 NestJS？

   Nest（NestJS）是一个用于构建高效、可扩展 Node.js 服务端应用的框架。它采用渐进式 JavaScript 设计理念，基于 TypeScript 构建，并对 TypeScript 提供完整支持。

2. ### <a id="who-developed-nestjs-why-did-they-develop-nestjs"></a>NestJS 是谁开发的？为什么要开发它？

   NestJS 由波兰软件工程师 Kamil Myśliwiec 开发。他创建 NestJS 的初衷，是为了解决 Node.js 应用缺乏统一工程结构的问题，并把 Angular 一类框架中成熟的工程化思想带到服务端开发中。

3. ### <a id="when-was-nestjs-first-released"></a>NestJS 最早是什么时候发布的？

   NestJS 首次发布于 2016 年 10 月 5 日。

4. ### <a id="how-can-you-install-nestjs-and-set-up-a-new-project-on-your-machine"></a>如何在本地安装 NestJS 并创建一个新项目？

   要在本机安装 NestJS，你需要先安装好 Node.js 和 npm（Node Package Manager）。准备好之后，可以通过以下命令在全局安装 NestJS CLI（命令行工具）：

   ```javascript
     $ npm i -g @nestjs/cli
   ```

   这条命令会全局安装 `NestJS CLI`，这样你就可以在任意目录下使用 `nest` 命令。安装完成后，可以通过下面的命令创建新项目：

   ```javascript
     $ nest new project-name
   ```

   创建项目后，还可以继续生成模块、服务等代码：

   ```javascript
    $ nest generate module users
   ```

   运行：

   ```javascript
     $ nest g resource users
   ```

   会一次性生成一组用于完成某个实体 CRUD（Create、Read、Update、Delete，增删改查）操作的文件。这里以 `users` 为例，通常会生成：

   一个用于处理 HTTP 请求的 `controller`（例如 `users.controller.ts`）

   一个承载业务逻辑的 `service`（例如 `users.service.ts`）

   一个封装该资源的 `module`（例如 `users.module.ts`）

   如果你选择生成 REST API，还会生成用于接收输入数据的 `DTO`（Data Transfer Object，数据传输对象）类，例如 `create-user.dto.ts`、`update-user.dto.ts`

   如果你选择生成 GraphQL API，还会额外生成一个 resolver（例如 `users.resolver.ts`）

5. ### <a id="what-s-the-difference-between-nestjs-and-angular?"></a>NestJS 和 Angular 有什么区别？

   Angular 是一个面向客户端的前端框架，用来构建浏览器中的应用。它通过组件、模块、服务等机制来组织前端代码。

   而 NestJS 是一个面向服务端的框架，用来构建后端应用。NestJS 基于 TypeScript 和 Express 构建，目标是为企业级应用提供更健壮、可扩展的架构。不过，它在设计理念上深受 Angular 影响，因此也共享了模块、装饰器、依赖注入等相似概念。

6. ### <a id="is-it-possible-to-use-other-languages-like-c-ruby-or-python-with-nestjs-if-yes-then-how"></a>NestJS 能否配合 C++、Ruby、Python 等其他语言一起使用？如果可以，怎么做？

   可以。NestJS 本身对语言并不“排他”，只要最终能够和 JavaScript 运行环境协作即可。

   不过，Python、Ruby 以及其他语言不能直接在 NestJS 内部运行，因为 NestJS 依赖的是执行 JavaScript 的 Node.js 运行时。

   更常见的做法是：把 Python、Ruby 或其他语言分别实现成独立服务，再通过 HTTP、gRPC 或其他通信协议与 NestJS 应用通信。这在微服务架构中非常常见。

7. ### <a id="what-are-the-main-components-of-a-nestjs-application"></a>NestJS 应用的核心组成部分有哪些？

   一个 NestJS 应用的核心组成通常包括：

   `Modules：` 模块用于把相关组件组织到一起，是应用结构化的基础。

   `Controllers：` 控制器负责接收传入的 `request`，并向客户端返回 `response`。它们用于组织路由并处理落到这些路由上的 HTTP 请求。

   `Services：` 服务负责承载业务逻辑，以及与数据源交互。它们可以被注入到控制器或其他服务中，从而提升代码复用性并实现关注点分离。

8. ### <a id="how-to-declare-a-class-as-a-controller-in-nestjs"></a>如何在 Nest.js 中把一个类声明为控制器？

   在 Nest.js 中，可以通过 **`@Controller()`** 装饰器把一个类声明为控制器。下面是一个基础示例：

   ```javascript
   import { Controller, Get } from "@nestjs/common";

   @Controller("example")
   class ExampleController {
     @Get()
     getHello(): string {
       return "Hello world!";
     }
   }
   ```

   在这个例子中，`ExampleController` 就是一个控制器类。`@Controller('example')` 表示这个控制器负责处理 `example` 路径下的请求。`getHello` 方法上的 `@Get()` 装饰器表示它用于处理 HTTP GET 请求。

   **[⬆ 返回顶部](#table-of-contents)**

9. ### <a id="can-you-explain-how-to-use-decorators-in-a-nestjs-controller"></a>能否说明一下如何在 NestJS 控制器中使用装饰器？

   在讲怎么使用装饰器之前，先说明一下什么是 `decorator`（装饰器）：

   `decorator` 是一类以 `@` 符号开头的特殊函数，可以附加在类、方法、属性或参数上。它们通常用于添加元数据，扩展行为，或者描述被修饰对象的用途。

   NestJS 提供了许多内置装饰器，你也可以自定义装饰器。常见的内置装饰器包括：

   1. `类装饰器`：例如 `@Controller()`、`@Module()`、`@Injectable()` 等，用于标注类。

   2. `方法装饰器`：例如 `@Get()`、`@Post()`、`@Put()` 等，用于标注控制器中的方法，以处理特定路由。

   3. `参数装饰器`：例如 `@Req()`、`@Res()`、`@Body()` 等，用于标注路由处理函数中的参数。

   4. `属性装饰器`：例如 `@Inject()`，用于标注类中的属性。

   5. `自定义装饰器`：你可以自行封装装饰器，用来处理应用中的通用逻辑。

   下面的例子展示了如何使用 `方法装饰器` 分别处理 GET、POST、PUT、DELETE 请求：

   ```javascript
   import {
     Controller,
     Get,
     Param,
     Body,
     Post,
     Patch,
     Delete,
   } from "@nestjs/common";

   @Controller("cats")
   export class CatsController {
     @Get()
     findAll(): string {
       return "This action returns all cats";
     }

     @Get(":id")
     findOne(@Param("id") id: number): string {
       return `This action returns a cat with the provided id`;
     }

     @Post()
     create(@Body() body: any): string {
       return `This action returns the body of the cat`;
     }

     @Patch("id")
     update(@Param("id") id: number, @Body() body: any): string {
       return `This action updates the body of the cat`;
     }

     @Delete("id")
     remove(@Param("id") id: number): string {
       return `This action removes a cat`;
     }
   }
   ```

   **[⬆ 返回顶部](#table-of-contents)**

10. ### <a id="how-can-you-use-route-parameters-in-a-nestjs-controller"></a>如何在 NestJS 控制器中使用路由参数？

    在 NestJS 控制器中，可以通过控制器方法里的 `@Param()` 装饰器来获取路由参数。

    ```javascript
        @Patch('id')
        update(@Param('id') id: number, @Body() body: any ): string {
           return `This action updates the body of the cat`;
        }
    ```

    **[⬆ 返回顶部](#table-of-contents)**

11. ### <a id="what-is-the-role-of-the-body-decorator"></a>`@Body()` 装饰器的作用是什么？

    NestJS 中的 `@Body()` 装饰器用于提取传入 HTTP 请求的整个请求体。它常用于处理 POST、PUT 这类把数据放在请求体中的接口。

    例如，如果你在控制器中有一个创建用户的方法，就可以通过 `@Body()` 读取客户端传过来的用户数据：

    ```javascript
     @Post()
     create(@Body() createUserDto: CreateUserDto) {
      return this.usersService.create(createUserDto);
     }
    ```

    在这个例子中，`createUserDto` 就是请求体中携带的数据对象。`@Body()` 会自动解析 JSON 请求体，并把结果赋值给 `createUserDto` 参数。

    **[⬆ 返回顶部](#table-of-contents)**

12. ### <a id="what-is-an-interceptor-in-the-context-of-nestjs"></a>在 NestJS 中，拦截器（Interceptor）是什么？

    拦截器是一个使用 `@Injectable()` 装饰器标注、并实现了 `NestInterceptor` 接口的类。

    拦截器可以在请求真正进入路由处理函数之前或之后切入执行逻辑，因此常用于日志记录、认证、响应转换等场景。

    拦截器的设计思路来源于 `面向切面编程（AOP，Aspect Oriented Programming）`。

    AOP 是一种 `编程范式`，目标是通过把横切关注点拆分出来，提升系统的 `模块化程度`。

    拦截器通常可以做到：

    `在方法执行前后附加额外逻辑：` 比如记录日志、统计耗时、转换返回结果、统一处理错误等。

    `转换函数返回结果：` 比如把所有接口响应统一包装成固定格式。

    `处理错误：` 拦截器也可以接住应用内部抛出的错误，在返回给客户端之前做统一处理或记录。
    下面是一个来自 [NestJS 文档](https://docs.nestjs.com/interceptors) 的日志拦截器示例：

    ```javascript
    import {
      Injectable,
      NestInterceptor,
      ExecutionContext,
      CallHandler,
    } from "@nestjs/common";
    import { Observable } from "rxjs";
    import { tap } from "rxjs/operators";

    @Injectable()
    export class LoggingInterceptor implements NestInterceptor {
      intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
        console.log("Before...");

        const now = Date.now();
        return next
          .handle()
          .pipe(tap(() => console.log(`After... ${Date.now() - now}ms`)));
      }
    }
    ```

    **[⬆ 返回顶部](#table-of-contents)**

13. ### <a id="what-are-pipes-in-the-context-of-nestjs"></a>在 NestJS 中，管道（Pipe）是什么？

    Pipe 是 NestJS 提供的一类机制，用于在数据传给路由处理函数之前先做校验或转换。它可以原样返回参数、对参数进行修改，或者在不满足条件时直接抛出异常。
    一个 Pipe 通常是一个使用 `@Injectable()` 标注并实现了 `PipeTransform` 接口的类。

    `校验：` 这是 Pipe 最常见的使用场景。它可以用来验证传入的数据是否符合预期的数据结构；若不符合，可以直接抛出异常，阻止后续处理逻辑继续执行。

    `转换：` Pipe 也可以把输入数据转换成目标格式。例如自动把字符串转成数字，或者把某个实体的 ID 转成实体对象本身。
    下面是一个简单的 Pipe 示例，用于把传入字符串校验并转换为数字：

    ```javascript
    import {
      PipeTransform,
      Injectable,
      ArgumentMetadata,
      BadRequestException,
    } from "@nestjs/common";

    @Injectable()
    export class ParseIntPipe implements PipeTransform<string, number> {
      transform(value: string, metadata: ArgumentMetadata): number {
        const val = parseInt(value, 10);
        if (isNaN(val)) {
          throw new BadRequestException("Validation failed");
        }
        return val;
      }
    }
    ```

    这个 `ParseIntPipe` 的使用方式如下：

    ```javascript

      @Get()
      async findOne(@Query('id', ParseIntPipe) id: number) {
        return this.usersService.findOne(id);
      }

    ```

    Nest 默认内置了 9 种常用 Pipe：
    `ParseIntPipe：` 把传入字符串转换为整数；如果无法转换，会抛出异常。上面已经展示过。

    `ValidationPipe：` 校验传入请求体是否符合指定 DTO（Data Transfer Object）结构；如果数据非法，就会抛出异常。

    `ParseFloatPipe：` 和 `ParseIntPipe` 类似，但用于转换为浮点数。

    `ParseBoolPipe：` 把传入字符串转换为布尔值，接受 `'true'` 和 `'false'`。

    `ParseArrayPipe：` 把逗号分隔的字符串转换为数组；如果你传入校验规则，还能顺带校验数组元素。

    `ParseUUIDPipe：` 校验传入字符串是否为合法 UUID；如果不是，会抛出异常。

    `ParseEnumPipe：` 校验传入字符串是否为某个 TypeScript 枚举的合法值。

    `DefaultValuePipe：` 当传入值为 `undefined` 或 `null` 时，提供默认值。

    `ParseFilePipe：` 用于文件上传场景，或对文件数据做解析与校验。

    **[⬆ 返回顶部](#table-of-contents)**

14. ### <a id="what-are-guards-in-the-context-of-nestjs"></a>在 NestJS 中，守卫（Guard）是什么？

    Guard 的职责非常单一：根据运行时条件（如权限、角色、ACL 等）决定某个请求是否允许继续交给路由处理函数处理。比如，你可以使用 Guard 判断用户是否已登录，只有通过后才允许访问某个接口。

    `guard` 一般是一个使用 `@Injectable()` 装饰器标注，并实现了 `CanActivate` 接口的类。该接口需要返回一个布尔值，或者返回一个最终解析为布尔值的 Promise。返回 `true` 表示允许请求继续；返回 `false` 表示拒绝请求，路由处理函数不会执行。
    下面是一个基础示例：

    ```javascript
    import { Injectable, CanActivate, ExecutionContext } from "@nestjs/common";

    @Injectable()
    export class AuthGuard implements CanActivate {
      canActivate(context: ExecutionContext): boolean | Promise<boolean> {
        const request = context.switchToHttp().getRequest();
        // 在这里编写你的认证逻辑
        // 例如，检查请求头中是否存在合法的 JWT token
        return true; // 如果不允许通过，则返回 false
      }
    }
    ```

    这个示例中的 `AuthGuard` 默认允许所有请求通过。真实项目中，你通常会在 `canActivate` 中实现具体的认证或鉴权逻辑。

    **[⬆ 返回顶部](#table-of-contents)**

15. ### <a id="what-are-middlewares-in-the-context-of-nestjs"></a>在 NestJS 中，中间件（Middleware）是什么？

    Middleware 是在路由处理函数执行之前被调用的函数。它可以访问 `request`、`response` 对象，以及请求处理链中的 `next()` 函数。

    `next` 通常就是传递给下一个中间件的控制函数。中间件常见的用途包括日志记录、认证、授权等。它可以执行任意代码，修改请求和响应对象，提前结束本次请求-响应流程，或者把控制权交给下一个中间件。

    下面是一个最简单的日志中间件示例：

    ```javascript
    import { Injectable, NestMiddleware } from "@nestjs/common";
    import { Request, Response, NextFunction } from "express";

    @Injectable()
    export class LoggerMiddleware implements NestMiddleware {
      use(req: Request, res: Response, next: NextFunction) {
        console.log(`[${req.method}] ${req.originalUrl}`);
        req["requestTime"] = Date.now();
        next();
      }
    }
    ```

    这个例子里：

    - `console.log(...)` 用来记录本次请求的基本信息。
    - `req["requestTime"] = Date.now()` 演示了中间件可以在请求对象上挂载额外字段，后续的 Guard、Interceptor、Controller 都可以继续读取它。
    - `next()` 表示把控制权继续交给后面的处理流程。如果这里不调用 `next()`，并且也没有主动返回响应，请求就会一直挂起。

    中间件可以完成以下事情：

    1. 执行任意代码。
    2. 修改请求对象和响应对象。
    3. 结束本次请求-响应流程。
    4. 把控制权交给下一个中间件。
       如果当前中间件没有结束请求流程，就必须调用 `next()`，否则请求会一直挂起。
       关于如何创建中间件，可参考 [NestJS 官方文档](https://docs.nestjs.com/middleware)

    **[⬆ 返回顶部](#table-of-contents)**

16. ### <a id="explain-the-concept-of-dependency-injection-in-nestjs-how-does-it-help-in-building-modular-and-testable-applications"></a>请解释 NestJS 中的依赖注入（Dependency Injection）概念。它如何帮助我们构建模块化且易于测试的应用？

    依赖注入（DI）是一种设计模式：一个类不自己创建依赖，而是由外部把依赖提供给它。这个模式是 NestJS 架构设计的核心之一。在 NestJS 中，依赖注入意味着由框架负责管理依赖的创建与注入，并按需提供给控制器、服务等组件。

    它主要通过装饰器、Provider，以及 NestJS 的 IoC（控制反转）容器来实现。
    下面是一个简单示例：

    ```javascript
    import { Injectable } from "@nestjs/common";

    @Injectable()
    export class AppService {
      getHello(): string {
        return "Hello World!";
      }
    }
    ```

    ```javascript

      import { Controller, Get } from '@nestjs/common';
      import { AppService } from './app.service';

      @Controller()
      export class AppController {
        constructor(private appService: AppService) {}

          @Get()
           getHello(): string {
            return this.appService.getHello();
          }
      }

    ```

    在这个例子里，`AppService` 是一个被注入到 `AppController` 构造函数中的 Provider。当 `AppController` 被创建时，NestJS 会自动实例化 `AppService` 并传入构造函数。

    `DI` 能从多个方面帮助我们构建模块化、易测试的应用：

    `模块化：` 通过注入依赖，你可以很容易地替换某个实现，而不必改动依赖它的类。这对于调整系统局部行为尤其有用。

    `可测试性：` DI 让单元测试更容易编写，因为你可以注入 mock 依赖来替代真实实现。

    `关注点分离：` 每个类只关心自己的职责，把依赖逻辑交给其他类完成，因此代码会更清晰、更易读。

    **[⬆ 返回顶部](#table-of-contents)**

17. ### <a id="what-s-the-difference-between-injectable-and-inject-decorators"></a>`@Injectable()` 和 `@Inject()` 装饰器有什么区别？

    `@Injectable()`：这个装饰器用于把一个类标记为可由 NestJS 依赖注入系统管理的 Provider。也就是说，NestJS 可以创建该类的实例，并在需要的地方注入它。

    它通常用于 Service 这类业务类，随后这些服务可以注入到控制器或其他服务中。

    ```javascript
    @Injectable()
    export class CatsService {
      // ...
    }
    ```

    `@Inject()`：这个装饰器用于在类内部显式注入某个依赖，通常写在构造函数参数上。

    如果你注入的是类 Provider，通常不需要写 `@Inject()`，因为 TypeScript 的反射系统可以推断出类型。但如果你注入的是非类 Provider（比如值 Provider、工厂 Provider），或者使用的是 JavaScript 而不是 TypeScript，就需要通过 `@Inject()` 明确告诉 NestJS 应该注入什么。

    ```javascript
      export class CatsController {
        constructor(@Inject('CatsService') private catsService: CatsService) {}
      }
    ```

    **[⬆ 返回顶部](#table-of-contents)**

18. ### <a id="how-does-the-nest-logger-differ-from-the-standard-console-log-and-when-would-you-prefer-one-over-the-other"></a>Nest 的 Logger 和普通的 `console.log()` 有什么区别？分别适合在什么场景下使用？

    相比 `console.log()`，`NestJS Logger` 提供了更多能力。它支持上下文信息、日志级别（如 `log`、`fatal`、`error`、`warn`、`debug`、`verbose`），并且可以自定义扩展。

    `console.log()` 更适合临时调试或非常简单的日志输出。

    当你需要更强的日志管理能力时，尤其是在中大型项目或生产环境中，更推荐使用 NestJS Logger。它便于按级别过滤日志，也能带上上下文，帮助你更快定位日志来源。

    关于 `Nest logger` 的具体实现方式，可以参考 [NestJS 官方文档](https://docs.nestjs.com/techniques/logger)

    **[⬆ 返回顶部](#table-of-contents)**

19. ### <a id="what-is-the-difference-between-interceptors-and-middleware"></a>拦截器和中间件有什么区别？

    在 NestJS 中，`interceptor` 和 `middleware` 都可以在 HTTP 请求前后加入额外逻辑，但两者有明显区别：

    `Interceptors：` 拦截器的适用范围更广，不仅可以用于 HTTP，还可以用于 WebSocket、微服务等其他传输层场景。

    拦截器还可以处理返回给客户端的响应，比如转换响应对象、添加响应头、修改状态码，也常用于性能监控、日志记录、缓存等场景。

    `Middleware：` NestJS 中的中间件更接近 Express 的中间件，它只作用于 HTTP 请求-响应流程，不能直接用于其他传输方式。中间件可以访问 request/response，并且可以提前结束请求，或者把控制权交给下一个中间件。

    中间件适合做日志记录、错误处理、请求数据校验等工作。

    一般来说，如果你的逻辑只发生在 HTTP 层，而且不需要改写响应内容，那么中间件通常就够了；如果你需要兼容 WebSocket、微服务等更多场景，或者需要统一处理/改造响应结果，那更适合使用拦截器。

    如果把 `Middleware`、`Guard`、`Interceptor`、`Pipe` 放到同一个接口里理解，会更直观。假设有一个接口：

    ```javascript
    @Post("users")
    @UseGuards(AuthGuard)
    @UseInterceptors(LoggingInterceptor)
    createUser(@Body(new ValidationPipe()) dto: CreateUserDto) {
      return this.usersService.create(dto);
    }
    ```

    这个请求的大致执行顺序可以理解为：

    1. `Middleware`
       请求一进入应用就先经过中间件。它最适合做请求日志、给 request 挂一些通用字段、处理 CORS 之类偏 HTTP 层的工作。
    2. `Guard`
       守卫会在真正调用路由方法前判断“这个请求有没有资格继续”。例如检查用户是否已登录、JWT 是否有效、角色是否匹配。
    3. `Interceptor（前置部分）`
       拦截器会先进入 `intercept()` 方法，在这里你可以先记录 `Before...` 日志、开始计时，或者做一些调用前准备。
    4. `Pipe`
       当 Nest 准备把参数传给控制器方法时，Pipe 会对参数做转换和校验。例如 `ValidationPipe` 会校验 `dto` 是否符合 DTO 规则，失败则直接抛错，控制器方法不会执行。
    5. `Controller / Service`
       前面的检查都通过后，才会真正进入 `createUser()` 以及后续的 service 业务逻辑。
    6. `Interceptor（后置部分）`
       控制器方法返回结果后，拦截器里 `next.handle().pipe(...)` 后面的逻辑才会执行，因此它特别适合做统一包装响应、记录耗时、追加响应日志等工作。

    用一句话概括它们的职责：

    - `Middleware`：更偏 HTTP 层的通用预处理。
    - `Guard`：决定请求能不能继续。
    - `Pipe`：保证传入控制器的数据是合法且格式正确的。
    - `Interceptor`：包住整个调用过程，既能在前面做事，也能在返回后处理结果。

    **[⬆ 返回顶部](#table-of-contents)**

20. ### <a id="what-testing-frameworks-work-best-with-nestjs"></a>NestJS 最适合搭配哪些测试框架？

    NestJS 是一个 Node.js 框架，因此理论上任何适用于 Node.js 的测试框架都能与它配合使用。常见选择包括 `Jest`、`Mocha` 和 `Jasmine`。
    NestJS 本身也非常重视测试体验，并内置了专门的测试模块 `@nestjs/testing`。这个模块提供了测试模块构建、HTTP 测试辅助等实用工具。

    **[⬆ 返回顶部](#table-of-contents)**

21. ### <a id="explain-the-purpose-of-dtos-data-transfer-objects-in-nestjs."></a>请解释 DTO（Data Transfer Object，数据传输对象）在 NestJS 中的作用。

    DTO 用于定义应用不同层之间传递数据的结构。它描述的是某个具体操作所需的数据形状，例如创建、更新或返回数据时的结构。

    DTO 的主要价值包括：
    `校验：` 借助 `class-validator`，你可以在 DTO 字段上声明校验规则。NestJS 可以自动根据这些规则校验传入请求，并在不合法时返回错误。

    `文档：` DTO 能清晰描述接口需要什么数据、返回什么数据，这既方便其他开发者理解，也便于 Swagger 这类工具自动生成 API 文档。

    `类型安全：` DTO 在 TypeScript 中提供类型约束，能帮助你在编译阶段提前发现问题。

    ```javascript
    import { IsString, IsInt } from "class-validator";

    export class CreateCatDto {
      @IsString()
      name: string;

      @IsInt()
      age: number;

      @IsString()
      breed: string;
    }
    ```

    在上面的例子中，`CreateCatDto` 表示创建一个猫对象所需的数据结构：`name` 和 `breed` 需要是字符串，`age` 需要是数字。`@IsString()` 和 `@IsInt()` 装饰器就是用来声明校验规则的。

    **[⬆ 返回顶部](#table-of-contents)**

22. ### <a id="how-can-you-handle-asynchronous-operations-in-nestjs-and-what-is-the-role-of-the-promise-object"></a>如何在 NestJS 中处理异步操作？Promise 在其中扮演什么角色？

    NestJS 通过 `async` / `await` 机制支持异步操作。当一个函数返回 Promise 时，就可以通过 `await` 等待其结果，从而以非阻塞方式编写代码。Promise 对象表示一个当前可能尚未可用、未来才会产生，甚至最终可能失败的值。

    ```javascript
    import { Injectable } from "@nestjs/common";

    @Injectable()
    export class AppService {
      async getHello(): Promise<string> {
        const result = await someAsyncOperation();
        return `Hello ${result}`;
      }
    }
    ```

    在这个例子中，`getHello()` 是一个返回 Promise 的异步方法。`await` 会让函数在 `someAsyncOperation()` 完成并 resolve 后再继续往下执行。

    Promise 很适合处理单次异步结果；如果你要处理的是连续的异步数据流，则更适合使用 RxJS 提供的 Observable，而 NestJS 也对其做了良好集成。

    **[⬆ 返回顶部](#table-of-contents)**

23. ### <a id="explain-the-purpose-of-the-injectrepository-decorator-in-nestjs"></a>请解释 `@InjectRepository()` 装饰器在 NestJS 中的用途。

    NestJS 中的 `@InjectRepository()` 装饰器常与 `TypeORM` 搭配使用，用于把某个实体对应的 repository 实例注入到 service 或 controller 中，方便进行数据库操作。

    在 TypeORM 中，repository 是管理实体的一种方式：它提供插入、更新、删除、查询等常用方法。通过注入 repository，你就可以在业务类中直接调用这些能力。

    示例：

    ```javascript
      import { Injectable } from '@nestjs/common';
      import { InjectRepository } from '@nestjs/typeorm';
      import { Repository } from 'typeorm';
      import { User } from './user.entity';

      @Injectable()
      export class UserService {
        constructor(
          @InjectRepository(User)
          private usersRepository: Repository<User>,
        ) {}

        findAll(): Promise<User[]> {
          return this.usersRepository.find();
        }
      }
    ```

    在这个例子中，`@InjectRepository(User)` 会把 `User` 实体对应的 repository 注入进来，后续 `findAll` 方法就能直接通过它查询所有用户。

    **[⬆ 返回顶部](#table-of-contents)**

24. ### <a id="explain-the-purpose-of-the-nestjs-jwt-package-in-nestjs"></a>请解释 `@nestjs/jwt` 包在 NestJS 中的作用。

    `@nestjs/jwt` 是 NestJS 提供的一个 JWT（JSON Web Token）相关模块，用于在应用中处理基于 Token 的认证与授权。JWT 是 Web 应用中非常常见的认证方式。

    它通常会和 `@AuthGuard('jwt')` 这类机制一起使用，用于保护路由，并支持 JWT 的生成、校验与解析。

    使用 `@nestjs/jwt` 可以完成的常见工作包括：

    `生成 JWT：` 根据指定 payload 和密钥签发 Token。

    `校验 JWT：` 验证收到的 JWT 是否有效、是否被篡改。

    `解码 JWT：` 解出 Token 中的 payload 信息。

    `@nestjs/jwt` 通常还会和 `@nestjs/passport` 配合使用。后者提供更灵活、模块化的认证策略机制，二者结合后，就可以比较完整地实现基于 JWT 的认证方案。

    **[⬆ 返回顶部](#table-of-contents)**

25. ### <a id="discuss-how-tokens-are-used-for-authorization-in-an-api-what-is-the-difference-between-authentication-and-authorization-and-how-are-these-processes-implemented-with-tokens"></a>请说明 Token 在 API 授权中的使用方式。认证（Authentication）和授权（Authorization）有什么区别？基于 Token 的实现流程是怎样的？

    在 API 中，Token（例如 JWT）通常用于授权，以确保用户只能访问自己有权限访问的资源，或执行被允许的操作。

    `Authentication（认证）` 是“确认你是谁”的过程。用户使用用户名、密码等凭据登录后，服务端会校验这些凭据；如果校验通过，就会生成一个 Token 返回给客户端。这个 Token 往往会携带用户的身份信息。

    `Authorization（授权）` 则是“确认你能做什么”的过程。用户后续每次请求都带上 Token，服务端会先校验 Token，再根据其中的信息判断该用户是否具备执行当前操作所需的权限。

    一个典型流程如下：

    1. 用户把登录凭据（如用户名和密码）提交给服务端。

    2. 服务端校验凭据，如果合法，就生成 Token 并返回给客户端。

    3. 在后续请求中，客户端把这个 Token 放到请求头中发送给服务端。

    4. 服务端校验 Token，并检查该用户是否具备当前操作所需权限；如果具备，就继续处理请求。

    因此，Token 既可以作为“已认证”的证明，也可以承载授权所需的信息。它是一种无状态、易扩展的 API 安全方案。

    **[⬆ 返回顶部](#table-of-contents)**

26. ### <a id="why-is-it-important-for-tokens-to-have-an-expiration-time-How-can-you-implement-token-expiration-in-nestjs-and-what-role-do-refresh-tokens-play-in-maintaining-user-sessions"></a>为什么 Token 必须设置过期时间？在 NestJS 中如何实现 Token 过期？Refresh Token 在维持用户会话时起什么作用？

    为 Token 设置过期时间，最主要是出于安全考虑。如果 Token 被窃取或泄露，攻击者就可能利用它非法访问系统；有了过期时间后，这种风险窗口会被显著缩短。

    在 NestJS 中，你可以在调用 `JwtService` 签发 JWT 时直接指定过期时间，例如：

    ```javascript
    this.jwtService.sign(payload, { expiresIn: "60s" });
    ```

    这个例子表示 Token 会在签发 60 秒后过期。

    但如果访问 Token 一过期就要求用户重新登录，体验通常会比较差。这时就需要 `refresh token`（刷新令牌）来协助维持登录状态。

    **[⬆ 返回顶部](#table-of-contents)**

27. ### <a id="describe-the-mechanism-for-a-token-refresh-in-nestjs-how-can-you-implement-an-automatic-token-refresh-strategy-to-maintain-user-sessions"></a>请描述 NestJS 中的 Token 刷新机制。如何实现自动刷新 Token，以维持用户会话？

    在 NestJS 中，`Token 刷新策略` 通常是在用户登录时，除了签发 access token，还会额外签发一个 refresh token。

    Refresh Token 是一种专门用于换取新 access token 的令牌。当用户登录成功后，服务端会同时把 access token 和 refresh token 一起返回给客户端。

    当 access token 过期后，客户端可以拿 refresh token 去请求服务端。服务端校验 refresh token 通过后，会重新签发一个新的 access token。

    这样既可以让用户保持登录状态，而不必频繁重新输入账号密码；同时又能通过缩短 access token 的有效期，降低 token 泄露后的风险。

    一般来说，refresh token 的过期时间会比 access token 长得多，而且服务端也可以在必要时主动吊销它，例如用户退出登录时。

    一个常见实现流程如下：

    `签发 Refresh Token：` 用户登录成功时，除了 access token，再额外签发 refresh token。通常 refresh token 的有效期会更长。

    `存储 Refresh Token：` 把 refresh token 和用户建立关联，保存到数据库中。这样在用户退出登录或需要强制失效时，就可以主动废弃它。

    `创建刷新接口：` 提供一个专门接收 refresh token 的接口，用来换取新的 access token。在这个接口中，需要校验 refresh token 是否有效、是否已失效，然后再签发新的 access token。

    `客户端自动刷新：` 在客户端，如果收到 `401 Unauthorized`，通常意味着 access token 已过期。这时就可以自动调用刷新接口，用 refresh token 获取新的 access token，并替换本地保存的旧 token。

    **[⬆ 返回顶部](#table-of-contents)**

28. ### <a id="how-does-nestjs-support-authentication-and-authorization"></a>NestJS 如何支持认证与授权？

    NestJS 支持认证与授权的方式很多，常见包括：

    1. `Passport.js 集成：` NestJS 可以很好地集成 Passport.js。Passport 是 Node.js 中非常流行的认证中间件，支持 OAuth、JWT、本地登录（用户名/密码）等多种策略。

    2. `JWT 模块：` NestJS 提供 `@nestjs/jwt` 用于生成和校验 JSON Web Token，这是实现无状态服务端认证的常见方式。

    3. `Guards：` 在 NestJS 中，Guard 用于决定一个请求是否允许继续进入路由处理函数，因此非常适合做授权检查。

    4. `Decorators：` 你可以通过自定义装饰器为路由附加元数据，例如标记访问某个接口所需的角色。

    5. `Interceptors：` 拦截器也可以用来根据 Token 把用户数据绑定到请求对象上。

    ```javascript
      import { Controller, UseGuards, Post, Request } from '@nestjs/common';
      import { AuthService } from './auth/auth.service';
      import { LocalAuthGuard } from './auth/local-auth.guard';

      @Controller('auth')
      export class AuthController {
        constructor(private authService: AuthService) {}

        @UseGuards(LocalAuthGuard)
        @Post('login')
        async login(@Request() req) {
          return this.authService.login(req.user);
        }
      }
    ```

    在这个例子中，`LocalAuthGuard` 是一个自定义 Guard，它基于 Passport 的 local strategy 来校验用户名和密码。校验通过后，`login()` 方法会调用 `AuthService` 为当前用户生成 JWT。

    **[⬆ 返回顶部](#table-of-contents)**

29. ### <a id="what-is-the-difference-between-provider-and-services-in-nestjs-can-we-have-a-provider-without-an-injectable-decorator-give-examples."></a>NestJS 中 Provider 和 Service 有什么区别？Provider 能否不使用 `@Injectable()`？请举例说明。

    `provider` 是一个更宽泛的概念，而 `service` 可以看作 Provider 的一种具体形式。Provider 是 NestJS 依赖注入体系中的基础概念，不仅可以注入 service，也可以注入值、工厂函数等其他对象。

    `service` 一般是一个使用 `@Injectable()` 标记的类，常用于承载业务逻辑或提供共享数据访问能力。示例如下：

    ```javascript
    import { Injectable } from "@nestjs/common";

    @Injectable()
    export class CatsService {
      // ...
    }
    ```

    不过，Provider 不一定非得是 service。它也可以是任何需要被注入的值。例如，你可以注册一个普通字符串：

    ```javascript

        {
          provide: 'HelloMessage',
          useValue: 'Hello, World!',
        }

    ```

    这里的 `HelloMessage` 就是一个注入 Token，对应的值是字符串 `Hello, World!`。

    虽然 service 通常会配合 `@Injectable()` 使用，但其他类型的 Provider 不一定需要这个装饰器。只有当某个类本身还依赖其他对象、需要 Nest 继续为它注入依赖时，才必须使用 `@Injectable()`。像上面这种简单值 Provider，就不需要。

    **[⬆ 返回顶部](#table-of-contents)**

30. ### <a id="what-are-custom-providers-and-how-do-they-differ-from-standard-providers-in-nestjs"></a>什么是自定义 Provider？它和 Nest.js 中的标准 Provider 有什么区别？

    `Provider` 是 NestJS 依赖注入系统的核心组成部分。它的主要职责，是创建并管理那些可以被注入到其他组件中的实例，从而让系统更模块化、更易测试。

    NestJS 中的标准 Provider，通常就是一个使用 `@Injectable()` 装饰的类。这个类本身还可以继续依赖其他对象，并通过构造函数注入。示例如下：

    ```javascript
       import { Injectable } from '@nestjs/common';

       @Injectable()
       export class CatsService {
         constructor(private readonly catsRepository: CatsRepository) {}
       }
    ```

    在这个例子中，`CatsService` 就是一个标准 Provider，它依赖 `CatsRepository`，并且可以被其他类继续注入使用。当然，并不是所有 Provider 都一定是 service。

    `自定义 Provider` 则是一种更灵活的提供依赖方式。它既可以是一个简单值，也可以是工厂函数，甚至是异步工厂函数。这些类型通常不需要 `@Injectable()` 装饰器。例如：

    ```javascript

     {
       provide: 'MagicNumber',
       useValue: 42,
     }

    ```

    这里的 `MagicNumber` 是一个注入 Token，对应的值是数字 `42`。

    `Custom providers` 的意义就在于：你不必只能注入“服务类”，还可以以值、工厂、异步工厂等形式提供依赖，让应用在创建依赖对象时有更高的灵活性。

    **[⬆ 返回顶部](#table-of-contents)**

31. ### <a id="how-can-you-generate-api-documentation-using-swagger-in-nestjs-discuss-the-importance-of-documenting-your-api-and-how-it-benefits-developers"></a>如何在 NestJS 中使用 Swagger 生成 API 文档？为什么要做接口文档，它对开发者有什么价值？

    在 NestJS 中，可以通过 `@nestjs/swagger` 包生成 API 文档。这个包提供了大量装饰器和 `SwaggerModule`，可以比较方便地生成 Swagger 文档。

    一个基础用法如下：

    - 先安装依赖。
    - `npm install --save @nestjs/swagger`

    ```javascript
    import { NestFactory } from "@nestjs/core";
    import { SwaggerModule, DocumentBuilder } from "@nestjs/swagger";
    import { AppModule } from "./app.module";

    async function bootstrap() {
      const app = await NestFactory.create(AppModule);

      const config = new DocumentBuilder()
        .setTitle("Cats example")
        .setDescription("The cats API description")
        .setVersion("1.0")
        .addTag("cats")
        .build();
      const document = SwaggerModule.createDocument(app, config);
      SwaggerModule.setup("api", app, document);

      await app.listen(3000);
    }
    bootstrap();
    ```

    在上面的例子中，`SwaggerModule.createDocument(app, config)` 会生成 Swagger JSON 文档，而 `SwaggerModule.setup('api', app, document)` 则会把 Swagger UI 挂载到指定路径（这里是 `api`）。

    接口文档的重要性主要体现在：

    `易用性：` 帮助其他开发者快速了解 API 有哪些接口、请求参数长什么样、返回结构是什么。

    `测试便利：` 通过 Swagger UI 这类工具，开发者可以直接在浏览器里调试接口。

    `可维护性：` 文档可以作为接口行为的参考标准，在系统变更时帮助团队确认接口仍然符合预期。

    `新人上手：` 新成员不必先翻源码，就能较快理解系统对外暴露了哪些能力。

    **[⬆ 返回顶部](#table-of-contents)**

32. ### <a id="explain-the-purpose-of-the-nestjs-swagger-apiproperty-apioperation-decorators"></a>请解释 `@nestjs/swagger` 中 `ApiProperty()`、`ApiOperation()` 装饰器的作用。

    `@nestjs/swagger` 提供了多种装饰器，帮助你为 API 自动生成 Swagger 文档。其中比较常用的两个是 `@ApiProperty()` 和 `@ApiOperation()`。

    `@ApiProperty()`：这个装饰器通常写在 DTO（数据传输对象）类的属性上，用来为属性补充元数据。这些元数据会被用于生成 Swagger 中的模型说明，也就是接口请求体或响应体的数据结构说明。

    ```javascript
    import { ApiProperty } from "@nestjs/swagger";

    export class CreateUserDto {
      @ApiProperty({
        description: "The id of the user.",
        minimum: 1,
        example: 42,
      })
      id: number;

      @ApiProperty({ description: "The name of the user.", example: "Thomas" })
      username: string;
    }
    ```

    这里的 `@ApiProperty` 用于告诉 Swagger：`CreateUserDto` 中的 `id` 和 `username` 都是需要展示的字段。

    `@ApiOperation()`：这个装饰器通常用在控制器方法上，用于描述某个接口（操作）的元信息，比如接口摘要、说明、标签等。这样生成出来的 Swagger 文档会更完整、更易读。

    示例：

    ```javascript
    import { ApiOperation } from "@nestjs/swagger";

    @Controller("users")
    export class UsersController {
      @Post()
      @ApiOperation({ summary: "Create user" })
      create(@Body() createUserDto: CreateUserDto) {
        // ...
      }
    }
    ```

    这里的 `@ApiOperation()` 为 `create` 接口添加了摘要说明，Swagger UI 中会直接展示出来。

    此外，`@nestjs/swagger` 还提供很多用于描述成功/错误响应的装饰器，比如 `@ApiNotFoundResponse`、`@ApiBadRequestResponse`、`@ApiInternalServerErrorResponse`、`@ApiOkResponse`、`@ApiCreatedResponse` 等。

    **[⬆ 返回顶部](#table-of-contents)**

33. ### <a id="explain-the-purpose-of-the-dockerfile-in-a-nestjs-application-and-how-it-facilitates-containerization"></a>请解释 Dockerfile 在 NestJS 应用中的作用，以及它如何帮助实现容器化。

    `Dockerfile` 是一个文本文件，其中包含一系列构建镜像所需的命令。在 NestJS 应用场景中，Dockerfile 用于把应用打包为一个 Docker 镜像。

    `Docker image（Docker 镜像）` 是一个轻量级、独立、可执行的软件包，里面包含运行应用所需的一切内容：代码、运行时、系统工具、系统库以及相关配置。

    这样一来，只要目标机器安装了 Docker，不管底层操作系统是什么，这个镜像都可以以一致的方式运行。

    下面是一个 Nest 应用的 Dockerfile 示例：

    ```javascript
       // Start from a base image
       FROM node:14-alpine // or node:latest to use the latest version of node

       // Set the working directory
       WORKDIR /usr/src/app

       //Install dependencies
       COPY package*.json ./
       RUN npm install

       // Copy source code
       COPY . .

       // Expose the application on port 3000
       EXPOSE 3000

       // Start the application
       CMD ["npm", "run", "start"]
    ```

    这个 Dockerfile 做了以下几件事：

    以一个已经安装了 Node.js 的基础镜像开始（如 `node:14-alpine`）。

    把容器内工作目录设置为 `/usr/src/app`。

    复制 `package.json` 和 `package-lock.json`（如果存在）到工作目录。

    执行 `npm install` 安装依赖。

    再把其余源码复制到工作目录中。

    暴露应用所使用的 3000 端口。

    定义启动命令（`npm run start`）。

    _说明：_ 这样做的好处在于，它把应用和运行环境一起封装成一个可执行单元（也就是容器）。无论部署到哪里，运行行为都能保持一致，从而提升不同环境下的稳定性与可预测性。

    **[⬆ 返回顶部](#table-of-contents)**

34. ### <a id="how-can-you-use-docker-compose-with-nestjs-and-what-is-its-role-in-a-multi-container-setup"></a>如何在 NestJS 中使用 Docker Compose？它在多容器场景中的作用是什么？

    `Docker Compose` 是一个用于定义和运行多容器应用的工具。它可以通过一个清晰的 YAML 配置文件，把整个应用栈中的服务、网络、卷等内容统一描述出来。随后你只需要一条命令，就可以把整套服务启动起来。

    下面是一个 NestJS + PostgreSQL 的基础 `docker-compose.yml` 示例：

    ```javascript
     version: '3'
      services:
        app:
          build: .
          ports:
            - 3000:3000
          depends_on:
            - db
        db:
          image: postgres:13-alpine
          environment:
            POSTGRES_USER: user
            POSTGRES_PASSWORD: password
            POSTGRES_DB: dbname
    ```

    在这个例子中，一共有两个服务：`app` 和 `db`。`app` 服务由当前目录中的 Dockerfile 构建，并对外暴露 3000 端口；`db` 服务则直接使用 `postgres:13-alpine` 镜像，并通过环境变量配置数据库。

    `depends_on` 用来表达服务间依赖关系，主要有两个含义：

    `db` 会先于 `app` 启动。
    Docker Compose 会等待 `db` 就绪后，再启动 `app`。
    启动整套服务时，只需执行 `docker-compose up`。

    使用 Docker Compose 的好处在于：它大大简化了多容器应用的管理工作。你可以用一条命令完成服务的启动、停止和重建，同时还能确保各个服务按正确顺序启动。

    **[⬆ 返回顶部](#table-of-contents)**

35. ### <a id="what-is-the-purpose-of-the-nestjs-passport-package-and-how-does-it-facilitate-authentication-in-nestjs"></a>`@nestjs/passport` 包的作用是什么？它如何帮助 NestJS 实现认证？

    `@nestjs/passport` 是围绕 Passport.js 封装的 NestJS 认证支持包。它的主要作用，是帮助开发者以统一、模块化的方式在 NestJS 应用中实现多种认证策略，例如 local、JWT、OAuth 等。

    它本质上提供了一组工具，让你更容易把 Passport.js 的认证能力整合进 NestJS 应用。

    下面是一个基础示例：

    ```javascript
    import { Injectable } from "@nestjs/common";
    import { AuthGuard } from "@nestjs/passport";

    @Injectable()
    export class JwtAuthGuard extends AuthGuard("jwt") {}
    ```

    **[⬆ 返回顶部](#table-of-contents)**

36. ### <a id="how-can-you-handle-file-uploads-in-nestjs-and-what-is-the-role-of-the-multer-library"></a>如何在 NestJS 中处理文件上传？Multer 库扮演什么角色？

    NestJS 提供了比较方便的文件上传处理方式，其中最常见的方案是使用 `multer` 中间件。同时，框架还提供了 `@UploadedFile` 装饰器，方便你在控制器中直接获取上传的文件。

    借助这些能力，NestJS 可以比较灵活、高效地完成文件上传处理。

    你通常会配合 `@UseInterceptors()` 与 `FileInterceptor` 或 `FilesInterceptor` 一起使用，从而支持单文件或多文件上传。

    **[⬆ 返回顶部](#table-of-contents)**

37. ### <a id="how-does-nestjs-handle-database-interactions-and-what-are-the-supported-databases"></a>NestJS 如何处理数据库交互？支持哪些数据库方案？

    NestJS 本身并不直接操作数据库，而是通过集成不同的数据访问库，让你按项目需求自由选择。常见方案包括：

    `TypeORM：` 一个对象关系映射（ORM）库，支持 MySQL、PostgreSQL、MongoDB、SQLite 等多种数据库。它通过较高层的 API，把数据库记录映射为 JavaScript 对象。

    `Mongoose：` 如果你使用的是 MongoDB，Mongoose 是很常见的选择。它基于 Schema 来建模数据，并内置类型转换、校验、查询构造以及业务钩子等能力。

    `Sequelize：` 一个基于 Promise 的 Node.js ORM，支持 Postgres、MySQL、MariaDB、SQLite、Microsoft SQL Server 等数据库，并提供 CRUD、事务、迁移等能力。

    `Prisma：` 一个开源数据库工具集，可以看作传统 ORM 的替代方案，常用于构建 GraphQL Server、REST API、微服务等。

    每种库如何与 NestJS 集成，可以参考 [Nest 官方数据库文档](https://docs.nestjs.com/techniques/database)

    **[⬆ 返回顶部](#table-of-contents)**

38. ### <a id="what-is-circular-dependency-dependency-cycle-in-nestjs-and-how-can-they-be-fixed"></a>什么是 NestJS 中的循环依赖（dependency cycle）？如何解决？

    `循环依赖` 指的是两个类互相依赖。例如：`class A` 依赖 `class B`，而 `class B` 又反过来依赖 `class A`。在 Nest 中，模块之间、Provider 之间都可能出现循环依赖。

    Nest 提供了两种常见方式来解决 Provider 之间的循环依赖。

    1. `forward referencing（前向引用）`：可以通过 `forwardRef()` 工具函数，让 Nest 引用一个“稍后才会定义”的类。比如 `CatsService` 和 `CommonService` 互相依赖时，双方都可以结合 `@Inject()` + `forwardRef()` 来打破循环。否则由于关键元数据尚未准备好，Nest 无法正确实例化它们。示例如下：

    ```javascript
      import { forwardRef } from '@nestjs/common'

     @Injectable()
     export class CatsService {
       constructor(
         @Inject(forwardRef(() => CommonService))
         private commonService: CommonService,
       ) {}
     }

    ```

    再看 `CommonService` 这一侧：

    ```javascript
    import { forwardRef } from '@nestjs/common'

    @Injectable()
     export class CommonService {
       constructor(
         @Inject(forwardRef(() => CatsService))
         private catsService: CatsService,
       ) {}
     }
    ```

    2. `ModuleRef class`：这是另一种替代 `forwardRef()` 的方式。你可以重构上面的写法，在循环关系的某一侧通过 `ModuleRef` 动态获取所需 Provider。

    **[⬆ 返回顶部](#table-of-contents)**

39. ### <a id="how-can-you-handle-errors-in-nestjs"></a>如何在 NestJS 中处理错误？

    NestJS 主要通过异常机制处理错误，例如可以使用 `throw new HttpException()` 这样的方式抛出异常。

    一旦抛出异常，NestJS 会自动返回合适的 HTTP 状态码和错误信息。

    ```javascript
    import { HttpException, HttpStatus } from "@nestjs/common";

    throw new HttpException("Resource not found", HttpStatus.NOT_FOUND);
    ```

    在这个例子中，抛出了一个 `HttpException`，错误信息为 `Resource not found`，状态码是 404（Not Found）。

    如果你有更复杂的错误处理需求，也可以通过继承 `HttpException` 自定义异常类。
    此外，NestJS 还内置了许多标准 HTTP 异常，它们都继承自 `HttpException`，并通过 `@nestjs/common` 导出，例如：`BadRequestException`、`UnauthorizedException`、`NotFoundException`、`ForbiddenException`、`NotAcceptableException`、`ConflictException`、`NotImplementedException` 等。

    **[⬆ 返回顶部](#table-of-contents)**

40. ### <a id="how-does-nestjs-handle-cors-cross-origin-resource-sharing"></a>NestJS 如何处理 CORS（跨域资源共享）？

    `CORS（Cross-Origin Resource Sharing，跨域资源共享）` 是一种机制，允许网页中的资源（例如字体、JavaScript 等）从资源原始域之外的其他域请求获取。

    在 Web 开发中，经常会出现前端页面和 API 服务不在同一个域名或端口下的情况。出于安全考虑，浏览器默认不允许网页向不同来源发起请求，除非服务端明确支持 CORS。

    开启 CORS 后，服务端就可以对跨域请求作出合法响应，也就意味着其他域、协议或端口下的前端可以访问你的服务资源。

    NestJS 依赖底层平台（Express 或 Fastify）提供的能力来处理 `CORS`。
    以 Express 为例，你可以在 `main.ts` 中为所有路由全局开启 CORS：

    ```javascript
    import { NestFactory } from "@nestjs/core";
    import { AppModule } from "./app.module";

    async function bootstrap() {
      const app = await NestFactory.create(AppModule);
      app.enableCors({
        origin: "http://localhost:3000",
        methods: "GET,HEAD,PUT,PATCH,POST,DELETE",
        allowedHeaders: "Content-Type",
      });
      await app.listen(3000);
    }
    bootstrap();
    ```

    这个例子中，只有来自 `http://localhost:3000` 的请求，并且使用指定 methods 和 headers 时，才会被允许跨域访问。

    **[⬆ 返回顶部](#table-of-contents)**

41. ### <a id="explain-the-purpose-of-the-executioncontext-in-nestjs-middleware"></a>ExecutionContext 在 NestJS Middleware 中的作用是什么？

    `ExecutionContext` 可以用来访问 `Request`、`Response` 对象，以及当前请求-响应流程中的其他上下文信息。这对于日志、校验、数据转换等需要在请求到达路由处理函数前执行的逻辑很有帮助。

    **[⬆ 返回顶部](#table-of-contents)**

42. ### <a id="how-can-you-implement-soft-deletes-in-nestjs-using-typeorm-and-why-might-soft-deletes-be-preferred-over-hard-deletes"></a>如何在 NestJS + TypeORM 中实现软删除？为什么有些场景下软删除比硬删除更合适？

    在 TypeORM 中，`软删除（Soft Delete）` 通常通过 `@DeleteDateColumn` 装饰器实现。对于带有 `@DeleteDateColumn` 的实体，删除时 TypeORM 不会真的把记录从数据库中移除，而是把该字段设置为当前时间戳。这就是“软删除”。

    下面是一个实体示例：

    ```javascript
     import { Entity, PrimaryGeneratedColumn, Column, DeleteDateColumn } from 'typeorm';

       @Entity()
       export class User {
         @PrimaryGeneratedColumn()
         id: number;

         @Column()
         name: string;

         @DeleteDateColumn()
         deletedAt?: Date;
       }

    ```

    在这个例子里，当你调用 `userRepository.softDelete(user.id)` 时，TypeORM 会把 `deletedAt` 设置为当前时间，但 `User` 记录本身仍然保留在数据库中。

    相比硬删除，软删除通常有以下优势：

    1. `数据恢复：` 如果某条记录被误删，可以相对容易地恢复。

    2. `审计追踪：` 即使记录已被“删除”，你依然保留了它的历史数据。
    3. `关系完整性：` 如果其他表还引用了这条记录，软删除不会像硬删除那样直接破坏引用关系。

    更多内容可参考 [Nestjs-Query 关于软删除的说明](https://doug-martin.github.io/nestjs-query/docs/persistence/typeorm/soft-delete)

    **[⬆ 返回顶部](#table-of-contents)**

43. ### <a id="explain-the-concept-of-environment-variables-in-nestjs-and-how-can-they-be-utilized-for-configuration-management"></a>请解释 NestJS 中环境变量的概念，以及它如何用于配置管理。

    环境变量是一种用于存储配置项的方式，特别适合那些会随着环境变化而不同的配置，例如开发、测试、预发、生产环境中的差异配置。

    它也经常用来保存敏感信息，比如数据库密码、API Key，或者其他不适合直接写进代码里的配置项。

    NestJS 提供了 `ConfigModule`，它基于 `dotenv` 包把 `.env` 文件中的变量加载到 `process.env` 中。

    下面是一个简单示例：

    ```javascript
    import { Module } from "@nestjs/common";
    import { ConfigModule } from "@nestjs/config";

    @Module({
      imports: [ConfigModule.forRoot()],
    })
    export class AppModule {}
    ```

    在这个例子中，`ConfigModule.forRoot()` 会加载 `.env` 文件，之后你就可以在应用的任意位置通过 `process.env` 读取这些变量。

    **[⬆ 返回顶部](#table-of-contents)**

44. ### <a id="what-is-the-role-of-migration-scripts-in-typeorm-and-how-can-you-create-and-run-migrations-in-a-nestjs-application"></a>TypeORM 中迁移脚本（Migration）的作用是什么？如何在 NestJS 应用中创建并执行迁移？

    `Migration scripts` 在 TypeORM 中用于管理数据库 Schema 随时间发生的变化。它能让数据库结构也像代码一样进入版本控制，并以可控方式完成升级。这在团队协作、多环境部署（开发、测试、生产）中尤其重要，因为它可以帮助各环境保持一致的数据库结构。

    一般流程如下：

    1. 先在 NestJS 应用中配置好 TypeORM。通常这意味着把 `TypeOrmModule` 导入应用模块，并填写数据库连接配置。

    2. 然后需要在 `ormconfig.json` 或 `ormconfig.js` 中增加 `migrations` 路径以及 CLI 配置，例如：

    ```javascript
     {
         "type": "postgres",
         "host": "localhost",
         "port": 5432,
         "username": "test",
         "password": "test",
         "database": "test",
         "entities": ["src/**/*.entity.ts"],
         "migrations": ["src/migrations/*.ts"],
         "cli": {
           "migrationsDir": "src/migrations"
         }
       }
    ```

    3. 生成迁移文件时，可以使用 TypeORM CLI 命令 `typeorm migration:generate -n MigrationName`。它会在 `src/migrations` 目录下生成一个形如 `TIMESTAMP-MigrationName.ts` 的文件。

    4. 生成的迁移文件通常包含 `up` 和 `down` 两个方法：`up` 用于执行迁移，`down` 用于回滚迁移。

    5. 执行迁移时，可以运行 `typeorm migration:run`，它会按顺序应用所有尚未执行的迁移。

    6. 如果要撤销最近一次迁移，可以运行 `typeorm migration:revert`，它会执行最近一次迁移中的 `down` 方法。

    **[⬆ 返回顶部](#table-of-contents)**

45. ### <a id="what-is-the-purpose-of-executioncontext-in-nestjs"></a>ExecutionContext 在 NestJS 中的用途是什么？

    `ExecutionContext` 表示当前正在被处理的请求上下文。它内部包含 `request`、`response`、`route handler` 等信息，因此经常被用于自定义装饰器、Guard 和拦截器中，以便读取或操作与当前请求相关的数据。

    **[⬆ 返回顶部](#table-of-contents)**

46. ### <a id="what-is-the-purpose-of-the-res-decorator-in-nestjs-controllers"></a>`@Res()` 装饰器在 NestJS 控制器中的作用是什么？

    Nest 提供了 `@Res()` 和 `@Response()` 两个装饰器，其中 `@Res()` 只是 `@Response()` 的别名。
    `@Res()` / `@Response()` 允许你直接访问底层的 `response` 对象，并调用其方法完成响应处理。

    使用它们时，通常也建议引入底层库的类型定义（例如 `@types/express`），这样可以获得更完整的类型提示。

    下面是一个使用 `@Res()` 的示例：

    ```javascript
    import { Controller, Get, Res } from "@nestjs/common";
    import { Response } from "express";

    @Controller("cats")
    export class CatsController {
      @Get()
      findAll(@Res() res: Response) {
        res.status(200).send("This action returns all cats");
      }
    }
    ```

    **注意：** 当你在某个路由处理函数中注入 `@Res()` 或 `@Response()` 后，该处理函数就进入了依赖底层库的模式（library-specific mode），此时响应的发送需要你自己负责。也就是说，你必须主动调用 `res.json(...)`、`res.send(...)` 等方法返回响应，否则请求会一直挂起。

    **[⬆ 返回顶部](#table-of-contents)**

47. ### <a id="explain-the-various-modules-in-nestjs"></a>请解释 NestJS 中各种模块（Module）的类型与作用。

    `module` 是一个使用 `@Module()` 装饰器标注的类。`@Module()` 提供的元数据会被 Nest 用来组织整个应用结构。

    `module` 是 NestJS 架构中的核心概念之一，它帮助我们把应用拆分成结构清晰、便于维护的逻辑单元。NestJS 中常见的模块类型主要有以下几种：

    1. `Feature Modules（功能模块）：` 这是最常见的一类模块，用于把同一业务领域下的控制器、服务等组织在一起，从而保持清晰边界，方便管理复杂度，也更符合 SOLID 原则。随着应用规模或团队规模增大，这一点会越来越重要。

    例如：`CatsController` 和 `CatsService` 同属于猫这个业务域，因此把它们放进同一个功能模块是很自然的做法。

    ```javascript
    import { Module } from "@nestjs/common";
    import { CatsController } from "./cats.controller";
    import { CatsService } from "./cats.service";

    @Module({
      controllers: [CatsController],
      providers: [CatsService],
    })
    export class CatsModule {}
    ```

    2. `Shared Modules（共享模块）：` Nest 中的模块默认是单例，因此你可以很方便地在多个模块之间共享同一个 Provider 实例。当一个模块被另一个模块导入时，它导出的 Provider 也会对导入方可用。凡是需要被多个模块复用的能力，都适合封装为共享模块。

    ![shared module](https://github.com/gasangw/NestJS-Interview-Questions-And-Answers/assets/99269832/91871589-f7ce-4e74-8063-3bac46d4b31a)

    假设我们希望多个模块共享同一个 `CatsService` 实例，就需要先在原模块中通过 `exports` 导出它：

    ```javascript
    import { Module } from "@nestjs/common";
    import { CatsController } from "./cats.controller";
    import { CatsService } from "./cats.service";

    @Module({
      controllers: [CatsController],
      providers: [CatsService],
      exports: [CatsService],
    })
    export class CatsModule {}
    ```

    这样一来，任何导入 `CatsModule` 的模块都可以使用 `CatsService`，并且共享的是同一个实例。

    3. `Global modules（全局模块）：` 如果你有一组需要“开箱即用、全局可用”的 Provider（例如帮助方法、数据库连接等），可以通过 `@Global()` 把该模块声明为全局模块。

    ```javascript
    import { Module, Global } from "@nestjs/common";
    import { CatsController } from "./cats.controller";
    import { CatsService } from "./cats.service";

    @Global()
    @Module({
      controllers: [CatsController],
      providers: [CatsService],
      exports: [CatsService],
    })
    export class CatsModule {}
    ```

    `@Global()` 会把模块声明为全局作用域模块。全局模块通常只需要注册一次，一般放在根模块或核心模块中。上面的例子中，`CatsService` 会自动在全局可注入，其他模块如果要使用它，就不再需要在 `imports` 中手动导入 `CatsModule`。

    4. `Dynamic Modules（动态模块）：` 动态模块适合创建可配置模块。它允许你在注册模块时根据传入配置动态创建 Provider。通常通过 `register()` 方法实现，该方法接收配置对象并返回一个动态模块。

    **[⬆ 返回顶部](#table-of-contents)**

48. ### <a id="how-can-you-secure-your-nestjs-application"></a>如何保护你的 NestJS 应用安全？

    要保护一个 NestJS 应用，通常需要从认证、授权、数据校验、错误处理等多个维度一起考虑。常见做法包括：

    `Authentication（认证）：` 可以使用 `Passport.js`。NestJS 通过 `@nestjs/passport` 对其做了集成，而 Passport 支持 OAuth、JWT、本地用户名/密码等多种认证策略。

    `Authorization（授权）：` NestJS 提供了 `@Roles()` 装饰器以及 `AuthGuard` 等机制来实现基于角色的访问控制（RBAC）。你可以在路由上声明所需角色，再由 Guard 判断当前用户是否具备权限。

    `数据校验：` 可以配合 `class-validator`、`class-transformer` 与 NestJS 提供的 `ValidationPipe` 来校验请求数据，从而降低 SQL 注入、XSS 等常见 Web 风险。

    `错误处理：` 可以使用 Filter 统一处理异常。NestJS 提供 `@Catch()` 装饰器来定义异常过滤器，从而返回更友好的错误响应。

    `限流：` 可以使用 `@nestjs/throttler` 来限制客户端在一定时间内的请求次数，防止滥用。

    `HTTPS：` 通过 HTTPS 加密客户端与服务端之间的传输数据。Nest 中可以在 `NestFactory.create()` 时配置 SSL 证书来启用。

    `Helmet：` Helmet 是一组通过设置 HTTP 头提升安全性的中间件。NestJS 通过 `@nestjs/platform-express` 提供了对 Helmet 的支持。

    `CORS：` 正确配置跨域策略，只允许可信域访问你的 API。Nest 中可以通过应用实例上的 `enableCors()` 来配置。

    当然，安全是一个很大的话题，上面这些只是 NestJS 应用中比较常见的一部分实践。

    **[⬆ 返回顶部](#table-of-contents)**

49. ### <a id="what-is-the-entry-file-of-nestjs-application"></a>NestJS 应用的入口文件是什么？

    NestJS 应用的入口文件通常是 `main.ts`。它负责启动应用，并引导根模块完成初始化。

    一个典型的 `main.ts` 可能如下所示：

    ```javascript
    import { NestFactory } from "@nestjs/core";
    import { AppModule } from "./app.module";

    async function bootstrap() {
      const app = await NestFactory.create(AppModule);
      await app.listen(3000);
    }
    bootstrap();
    ```

    `NestFactory.create(AppModule)` 会以根模块 `AppModule` 为入口初始化整个应用，而 `app.listen(3000)` 则会让服务开始监听 3000 端口上的请求。

    **[⬆ 返回顶部](#table-of-contents)**

50. ### <a id="what-is-the-difference-between-dependency-injection-and-inversion-of-control-ioc"></a>依赖注入（DI）和控制反转（IoC）有什么区别？

    `Dependency Injection（DI，依赖注入）` 和 `Inversion of Control（IoC，控制反转）` 都是为了降低类之间的 `耦合`、提升代码模块化、可测试性和可维护性而采用的设计思想。但它们并不是同一个概念，准确地说，`DI` 是 `IoC` 的一种实现方式。

    `IoC（控制反转）` 是一种更宽泛的原则：程序的控制流程不再完全由开发者手动驱动，而是交由外部框架或运行时来管理。

    `DI（依赖注入）` 则是 IoC 的具体落地方式之一。它把依赖对象的创建和绑定交给容器或框架，而不是让类自己 new、自己查找依赖。也就是说，依赖会在运行时由外部代码（通常是容器或框架）传进来。这样做的好处是：对象的“使用”与“创建”解耦了，因此代码会更灵活、更易测试、更模块化。

    Angular、Spring、NestJS 等现代框架中，广泛采用的就是这种 IoC 实现方式。

    总结一下：`IoC` 是设计原则，`DI` 是实现该原则的其中一种方式。

    **[⬆ 返回顶部](#table-of-contents)**

51. ### <a id="how-can-you-implement-caching-in-nestjs"></a>如何在 NestJS 中实现缓存？

    缓存是一种简单但非常有效的 `技术手段`，可以显著提升应用性能。它本质上是一个临时数据存储层，用更快的访问方式换取更短的响应时间。

    NestJS 支持多种缓存方式，包括基于 `cache-manager` 的缓存能力，以及内置的 `@CacheKey`、`@CacheTTL` 等装饰器。通过合理引入缓存策略，可以提升高频请求的处理效率并降低响应延迟。

    要启用缓存，先导入 `CacheModule`，并调用它的 `register()` 方法：

    ```javascript
    import { Module } from "@nestjs/common";
    import { CacheModule } from "@nestjs/cache-manager";
    import { AppController } from "./app.controller";

    @Module({
      imports: [CacheModule.register()],
      controllers: [AppController],
    })
    export class AppModule {}
    ```

    如果你想直接操作缓存管理器实例，可以通过 `CACHE_MANAGER` 这个 token 把它注入到类中：

    > ```javascript
    > constructor(@Inject(CACHE_MANAGER) private cacheManager: Cache) {}
    > ```

    `get` 方法用于从缓存中读取数据；如果键不存在，通常会返回 `null`。

    > ```javascript
    > const value = await this.cacheManager.get("key");
    > ```

    使用 `set` 方法可以把数据写入缓存：

    > ```javascript
    > await this.cacheManager.set("key", "value");
    > ```

    缓存默认过期时间通常是 5 秒，不过你可以自行修改：

    > ```javascript
    > await this.cacheManager.set("key", "value", 1000);
    > ```

    如果希望缓存不过期，可以把 `ttl` 设为 0：

    > ```javascript
    > await this.cacheManager.set("key", "value", 0);
    > ```

    删除某一项缓存时，使用 `del`：

    > ```javascript
    > await this.cacheManager.del("key");
    > ```

    清空整个缓存时，使用 `reset`：

    > ```javascript
    > await this.cacheManager.reset();
    > ```

    **[⬆ 返回顶部](#table-of-contents)**

52. ### <a id="explain-the-purpose-of-the-dependency-inversion-principle-dip-in-nestjs"></a>请解释依赖倒置原则（DIP）在 NestJS 中的作用。

    `Dependency Inversion Principle（DIP，依赖倒置原则）` 是 [SOLID](https://www.freecodecamp.org/news/solid-design-principles-in-software-development/) 五大原则之一。它的核心思想是：

    > ```javascript
    >     1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
    >     2. Abstractions should not depend on details. Details should depend on abstractions.
    > ```

    放到 NestJS 这类支持依赖注入的框架语境下，`DIP` 的价值在于降低模块之间的 `耦合`，让系统更灵活、更容易测试，也更容易维护。

    当系统依赖的是 `抽象` 而不是某个具体实现时，你就可以在不改动高层业务代码的前提下，轻松替换底层实现。比如一个 service 依赖 repository：如果你的代码是面向接口/抽象编写的，那么后续无论是把内存仓库切换成数据库仓库，还是替换成别的实现，service 本身都不用改。

    如果想进一步了解 `DIP`，可以参考 [这里](https://trilon.io/blog/dependency-inversion-principle)

    NestJS 主要通过模块化体系，以及 `@Injectable()`、`@Inject()`、`custom providers` 等机制来支持 `DIP`。这些能力让你可以基于抽象定义 Provider，并在需要的地方注入，从而更容易遵循依赖倒置原则。

    **[⬆ 返回顶部](#table-of-contents)**

53. ### <a id="how-can-you-schedule-tasks-in-nestjs"></a>如何在 NestJS 中实现任务调度？

    任务调度允许你让某段代码（方法/函数）在固定时间执行、按固定周期执行，或者在延迟一段时间后执行一次。

    Nest 提供了 `@nestjs/schedule` 包，并集成了常用的 `Node.js cron` 能力。

    1. 首先安装依赖：

    ```
     npm install --save @nestjs/schedule
    ```

    2. 然后把 `ScheduleModule` 导入模块：

    ```javascript
    import { Module } from "@nestjs/common";
    import { ScheduleModule } from "@nestjs/schedule";
    import { TasksService } from "./tasks.service";

    @Module({
      imports: [ScheduleModule.forRoot()],
      providers: [TasksService],
    })
    export class TasksModule {}
    ```

    3. 接下来，就可以在服务中通过装饰器声明定时任务。例如：

    ```javascript
    import { Injectable } from "@nestjs/common";
    import { Cron, CronExpression } from "@nestjs/schedule";

    @Injectable()
    export class TasksService {
      @Cron(CronExpression.EVERY_5_SECONDS)
      handleCron() {
        console.log("Called every 5 seconds");
      }
    }
    ```

    在这个例子中，`handleCron()` 会每 5 秒执行一次。`@Cron()` 接收一个 `CronExpression` 来描述调度规则。

    另外，`ScheduleModule` 底层依赖的是 `node-schedule`，因此凡是 `node-schedule` 支持的 cron 表达式，你都可以使用。

    **[⬆ 返回顶部](#table-of-contents)**

54. ### <a id="how-can-you-handle-database-transactions-in-nestjs-and-why-are-transactions-important-in-certain-scenarios"></a>如何在 NestJS 中处理数据库事务？为什么某些场景必须使用事务？

    在 NestJS 中，数据库事务通常可以借助 `TypeORM` 来处理。事务的重要性在于：当一组数据库操作必须“要么全部成功，要么全部失败”时，事务能保证数据一致性。如果其中任何一步失败，系统可以回滚所有变更，避免数据库进入不一致状态。

    这类场景在金融、库存、订单等业务中尤其关键，因为这些操作往往不允许只执行一半。

    **[⬆ 返回顶部](#table-of-contents)**

55. ### <a id="how-can-you-implement-versioning-in-nestjs-api"></a>如何在 NestJS API 中实现版本控制？

    版本控制允许你在同一个应用中同时运行 `不同版本` 的控制器或单个路由。

    NestJS 支持 4 种版本控制方式：

    1. `URI Versioning：` 在请求 URI 中携带版本号（默认方式）。
    2. `Header Versioning：` 通过自定义请求头指定版本号。
    3. `Media Type Versioning：` 通过请求的 `Accept` 头指定版本。
    4. `Custom Versioning：` 通过请求中的任意信息提取版本号，开发者可以自定义提取函数。

    如果要启用 `Header Versioning`，可以这样配置：

    ```javascript
    const app = await NestFactory.create(AppModule);
    app.enableVersioning({
      type: VersioningType.HEADER,
      header: "Custom-Header",
    });
    await app.listen(3000);
    ```

    关于上述 4 种版本控制方式的具体实现，可以参考 [Nest 官方文档](https://docs.nestjs.com/techniques/versioning)

    **[⬆ 返回顶部](#table-of-contents)**

56. ### <a id="explain-the-purpose-of-the-nestjs-graphql-resolver-and-nestjs-graphql-scalar-decorators-and-how-they-relate-to-graphql-in-nestjs"></a>请解释 `@nestjs/graphql` 中 `Resolver` 与 `Scalar` 装饰器的作用，以及它们与 GraphQL 的关系。

    `GraphQL` 是一种用于 API 的强大查询语言，同时也是一套运行时机制，用来根据查询从现有数据中组织返回结果。相比传统 REST，它在很多场景下能以更优雅的方式解决接口设计问题。

    `@nestjs/graphql` 提供了一套装饰器，使你可以直接基于 TypeScript 类来定义 GraphQL Schema。

    1. `@Resolver()`：用于把一个类标记为 GraphQL Resolver。Resolver 是 GraphQL 服务端的核心构件之一，负责为 Schema 中的字段提供数据。当客户端向 GraphQL 服务发起查询时，服务端会调用相应的 resolver 函数来组装响应。具体用法可参考 [这里](https://docs.nestjs.com/graphql/resolvers)

    2. `@Scalar()`：用于定义自定义标量类型。GraphQL 内置的标量包括 `Int`、`Float`、`String`、`Boolean`、`ID`。如果你需要表达诸如 `Date` 这类自定义原始类型，或者数据库中的特殊基础类型，就可以使用自定义 Scalar。具体用法可参考 [这里](https://docs.nestjs.com/graphql/scalars)

    如果你想更直观地理解 `GraphQL` 和 `REST` 的区别，可以阅读 [这篇文章](https://www.apollographql.com/blog/graphql-vs-rest)

    **[⬆ 返回顶部](#table-of-contents)**

57. ### <a id="explain-the-concept-of-serialization-and-deserialization-in-nestjs"></a>请解释 NestJS 中的序列化（Serialization）与反序列化（Deserialization）。

    序列化和反序列化是计算机科学中的基础概念，并不仅限于 NestJS。它们通常出现在“数据需要被存储或传输，然后再恢复使用”的场景中。

    `Serialization（序列化）：` 指的是把一个数据结构或对象状态转换成可存储、可传输的格式，例如写入文件、内存缓冲区，或者通过网络发送。之后还可以在相同或不同环境中重新还原。更多关于序列化的内容可参考 [这里](https://docs.nestjs.com/techniques/serialization)。

    `Deserialization（反序列化）：` 则是反过来，把序列化后的数据格式重新恢复成内存中的实际对象。

    在 NestJS 里，这两个概念经常出现在 `HTTP 请求` 与 `响应` 的处理过程中。例如，客户端发送数据给服务端时，通常会先把数据序列化成 `JSON`，通过网络传输后，服务端再把它反序列化为 JavaScript 对象。

    NestJS 提供了 `Pipes` 机制，可用于数据转换（包括序列化/反序列化相关处理）和校验。例如，NestJS 提供的 `ValidationPipe` 就可以自动把传入请求转换并校验为 `DTO` 类实例。

    **[⬆ 返回顶部](#table-of-contents)**

58. ### <a id="explain-the-role-of-nestjs-middleware-in-the-context-of-microservices-and-provide-a-scenario-where-middleware-is-beneficial-in-a-microservices-setup"></a>请解释 NestJS 中间件在微服务场景下的作用，并举一个适合使用中间件的微服务案例。

    `Middleware` 是在路由处理函数执行前运行的函数。它可以访问请求对象、响应对象以及请求处理链中的 `next()` 方法。中间件可以执行任意代码、修改请求与响应、提前终止请求流程，或者继续把控制权交给下一个中间件。

    在微服务场景中，中间件通常可以发挥以下作用：

    1. `请求日志：` 记录传入请求的关键信息。这对于排查问题、分析使用模式和理解用户行为都很有帮助。

    2. `认证与授权：` 在请求进入具体服务前，先验证用户身份和权限，避免每个服务都各自重复实现一套认证逻辑。

    3. `错误处理：` 中间件可以统一捕获和处理错误，保证即使服务内部出错，对外返回的错误结构依然一致、可预期。

    4. `限流：` 记录客户端请求频率，并在必要时限制访问，防止接口被滥用。

    **[⬆ 返回顶部](#table-of-contents)**

59. ### <a id="discuss-the-different-types-of-coupling-such-as-tight-coupling-and-loose-coupling-and-provide-examples-of-how-nestjs-modules-contribute-to-achieving-loose-coupling-in-a-modularized-application"></a>请说明紧耦合、松耦合等不同类型的耦合，并举例说明 NestJS 模块如何帮助模块化应用实现松耦合。

    `Coupling（耦合）` 指的是软件模块之间相互依赖的程度，也就是两个模块或两段逻辑之间连接得有多紧密。

    `Tight Coupling（紧耦合）：` 指一个模块（或类）高度依赖另一个模块。这样一来，一方的改动很可能迫使另一方跟着改，系统会更难维护，也更难演进。

    `Loose Coupling（松耦合）：` 指模块之间依赖较弱，一个模块的变动对其他模块影响较小，甚至没有影响。因此系统更易维护，也更适应变化。

    NestJS 通过模块化开发结构天然鼓励松耦合。每个模块负责应用的一部分功能，可以相对独立地工作。这样一个模块内部的变更，通常不会直接影响其他模块。

    下面是一个更直观的例子：

    ```javascript
    // users.service.ts
      import { Injectable } from '@nestjs/common';
      import { User } from './user.entity';

      @Injectable()
      export class UsersService {
        private users: User[] = [];

        create(user: User) {
          this.users.push(user);
        }

        findAll(): User[] {
          return this.users;
        }
      }

      // meal.service.ts
      import { Injectable } from '@nestjs/common';
      import { UsersService } from '../users/users.service';

      @Injectable()
      export class MealService {
        constructor(private usersService: UsersService) {}

        createMeal(userId: string, MealData: CreateMealDTO) {
          const user = this.usersService.findById(userId);
          // Create meal for the user
        }
      }
    ```

    在这个例子里，`MealService` 依赖 `UsersService`，但它并不直接操作用户数据的底层实现。这就是一种较为典型的松耦合关系。

    **[⬆ 返回顶部](#table-of-contents)**

60. ### <a id="how-does-nestjs-support-server-sent-events-sse-and-what-are-the-primary-advantages-of-using-sse-for-real-time-communication-in-web-applications"></a>NestJS 如何支持 SSE（Server-Sent Events，服务器发送事件）？它在 Web 实时通信中的主要优势是什么？

    `Server-Sent Events（SSE）` 是一种服务端主动推送技术，它允许客户端通过 HTTP 连接持续接收服务端发送的更新。`SSE` 是一种单向通信机制：数据只从服务端流向客户端。如果你需要双向通信，通常更适合使用 WebSocket。

    `SSE` 常见于 Facebook / Twitter 动态更新、股票行情推送、新闻流更新等场景。

    如果要在某个路由上启用 `Server-Sent Events`，可以在控制器方法上使用 `@Sse()` 装饰器：

    ```javascript
      @Sse('sse')
        sse(): Observable<MessageEvent> {
          return interval(1000).pipe(map((_) => ({ data: { hello: 'world' } })));
      }
    ```

    在上面的例子中，我们定义了一个名为 `sse` 的路由，用于持续向客户端推送实时更新。客户端可以通过 [EventSource API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 来监听这些事件。

    `SSE` 在 Web 实时通信中的主要优势包括：

    1. `基于 HTTP：` SSE 构建在 HTTP 之上，因此通常能较好地兼容大多数防火墙和网络环境，不需要额外特殊配置。

    2. `自动重连：` 一旦连接中断，浏览器通常会自动尝试重新连接服务端。

    3. `事件 ID：` 服务端可以为每条事件附带 ID。这样客户端断线重连后，有机会继续获取中断期间错过的事件。

    4. `高效推送：` SSE 非常适合“服务端一有新数据就立刻推送给客户端”的场景，例如实时新闻、实时分析看板等。

    更多关于 `SSE` 的说明，可以参考 [NestJS 官方文档](https://docs.nestjs.com/techniques/server-sent-events)

    **[⬆ 返回顶部](#table-of-contents)**
