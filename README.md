# PuppleTrouble · 玩犊紫

以颜色为核心的 AI 辅助设计应用，帮助普通用户发现颜色、理解作品中的配色关系，并应用到自己的页面。

**当前已建立可运行的后端、Web、Android 工程及 PostgreSQL 初始迁移。** 现阶段功能为运行检查和两端连接检查首页；取色、作品、模板编辑、AI 调整、保存与导出等业务尚未实现，相关空文件仅作开发位置预留。

## 启动入口

首次安装工具、生成配置、安装依赖、迁移及各终端的日常命令见[项目启动](docs/项目启动.md)。环境配置由团队自行完成本机设置，不按成员分配。

1. 根目录执行 `scripts/setup-local.ps1`，生成本机配置。
2. Python 3.12 创建 .venv，安装 backend/requirements.lock.txt；frontend 执行 npm ci。
3. 启动 Compose 的 db 并执行 Alembic 迁移，再启动后端。
4. frontend 执行 npm run dev；Android Studio 打开 android，或使用 Gradle Wrapper 构建安装。

Web：http://127.0.0.1:5173；API 文档：http://127.0.0.1:8000/docs；数据库仅本机 5432。详细步骤、模拟器／真机地址和验证范围以启动文档为准。

## 文档入口

| 文档 | 内容 |
|---|---|
| [项目文档](docs/项目文档.md) | 产品定位、颜色核心功能、AI 职责与首版边界 |
| [项目开发计划](docs/项目开发计划.md) | 5 个六天 Sprint，分前／后三天；D21 完成基础版，D30 交付 |
| [分工安排](docs/分工安排.md) | A Web 兼架构框架，B 后端数据库，C 后端算法，D Android 兼六天联合测试 |
| [架构设计](docs/架构设计.md) | 分层、两端边界、算法／模型／业务与实际实现范围 |
| [数据库设计](docs/数据库设计.md) | 已有 users 迁移、目标实体、事务约束与删除策略 |
| [功能对应的模块](docs/功能对应的模块.md) | 功能到 Web／API／后端／Android 文件的映射和真实状态 |
| [接口文档](docs/接口文档.md) | 已实现运行检查与待开发业务契约 |
| [技术栈说明](docs/技术栈说明.md) | 实际工具链、固定依赖与后续选型 |
| [环境配置说明](docs/环境配置说明.md) | 前端、后端、数据库、算法与 AI、移动端分册 |
| [项目协作](docs/项目协作.md) | 拉取同步、任务分支、中文提交与交接规则 |
| [项目启动](docs/项目启动.md) | 首次准备、日常命令、检查、停止和排障 |
| [HANDOFF](docs/HANDOFF.md) | 按当前要求留空，现阶段暂不填写 |

## 目录

```text
PuppleTrouble/
├── README.md / .gitignore / .gitattributes / .editorconfig
├── .env.example / compose.dev.yaml
├── scripts/setup-local.ps1
├── backend/     FastAPI、Alembic、依赖与测试；后续业务模块已预留
├── frontend/    React、Vite、TypeScript、首页与客户端检查
├── android/     Kotlin、Compose、Gradle Wrapper 与启动首页
└── docs/        产品、Sprint、架构、数据库、模块、配置与启动说明
```

不提交真实环境配置、密钥、私人素材、数据库数据、node_modules、.venv、APK 和构建产物。源码许可证尚未确定；第三方库、模型和图像各自遵循原许可。项目名固定为 PuppleTrouble／玩犊紫。
