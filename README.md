# PuppleTrouble · 玩犊紫

以颜色为核心的 AI 辅助设计应用。帮助普通用户发现颜色、理解作品中的配色关系，并将其应用到自己的页面。

**当前状态：产品与工程文档基线，尚无可运行的 Web、Android 应用或业务 API。** 本仓库中的环境样例只启动开发数据库，不应据此认为后端已实现。

**开始修改前先阅读 [HANDOFF 工作交接](docs/HANDOFF.md)，修改后更新交接记录并一同提交。**

## 文档入口

| 文档 | 内容 |
|---|---|
| [HANDOFF 工作交接](docs/HANDOFF.md) | 当前真实状态、协作约定、验证及下一接手任务 |
| [项目文档](docs/项目文档.md) | 产品定位、颜色核心功能、AI 职责与首版边界 |
| [项目开发计划](docs/项目开发计划.md) | 4 人、30 天，三天一周期；2026-11-15 开始，前 21 天完成基础版，12-14 交付 |
| [分工安排](docs/分工安排.md) | 四人职责、模块归属、评审和交接 |
| [接口文档](docs/接口文档.md) | v0.1 拟定 REST API、数据模型、异步任务与版本冲突 |
| [技术栈说明](docs/技术栈说明.md) | React Web、Android 移动端、Python 服务、色彩与 AI |
| [环境配置说明](docs/环境配置说明.md) | 前端、后端、数据库、算法与 AI、移动端配置分册 |
| [项目协作](docs/项目协作.md) | 中文提交描述、HANDOFF、拉取同步、分支、PR 与验证 |
| [项目启动](docs/项目启动.md) | 当前可启动范围、完整启动顺序、入口与排障 |

## 技术路线

- Web 前端：React、TypeScript、Vite、Tailwind CSS、Konva、Zustand、TanStack Query。
- Android 移动端：Kotlin、Jetpack Compose、Material 3、Navigation Compose、ViewModel/StateFlow、Retrofit/OkHttp、Coil、Room。
- 服务端：Python 3.12、FastAPI、Pydantic、SQLAlchemy、Alembic、PostgreSQL 16。
- 颜色计算：Pillow、OpenCV、NumPy、colour-science；多模态模型承担语义理解和解释，不代替准确取色。
- AI：通过服务端接入千问多模态 API；模型可替换，密钥不进入安装包。

## 当前可用的环境样例

复制 `.env.example` 为 `.env`，填写本地开发配置后执行 `docker compose --env-file .env -f compose.dev.yaml up -d db`，只启动数据库。其余运行说明见环境配置文档。

四人配置：A Web 前端兼架构与后端接口框架，B 后端兼数据库，C 后端兼算法，D Android 移动端兼每六天一次的联合测试组织。

计划代码目录为 `frontend/`、`android/`、`backend/`、`data/catalog/` 和 `tests/`，尚未生成应用脚手架。小规模经过授权的作品元数据可版本管理；私人上传、缓存和大型素材留在存储中。

仓库尚未选择源码开源许可证；第三方模型、库和图像各自遵循原许可。

## 目录组织

```text
PuppleTrouble/
├── README.md
├── .gitignore / .gitattributes / .editorconfig
├── .env.example
├── compose.dev.yaml
├── docs/                 项目、计划、分工、接口、技术、启动、协作与 HANDOFF；环境配置分册
├── backend/
│   └── requirements.txt  后端依赖候选清单
└── frontend/
    └── .env.example      仅公开的浏览器配置
```

Android 等代码目录在对应工程建立后新增。说明文档集中于 docs；README、Git 配置、环境样例、Compose 和模块依赖留在其正常运行位置。所有文档中的终端命令，除明确切换目录外，均从仓库根目录执行。
