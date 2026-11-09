# PuppleTrouble · 玩犊紫

以颜色为核心的 AI 辅助设计应用。帮助普通用户发现颜色、理解作品中的配色关系，并将其应用到自己的页面。

**当前状态：产品与工程文档基线，尚无可运行的 Web、Android 应用或业务 API。** 本仓库中的环境样例只启动开发数据库，不应据此认为后端已实现。

## 文档入口

| 文档 | 内容 |
|---|---|
| [项目文档](项目文档.md) | 产品定位、颜色核心功能、AI 职责与首版边界 |
| [项目开发计划](项目开发计划.md) | 4 人、30 天，自 2026-11-15 至 2026-12-14 |
| [分工安排](分工安排.md) | 四人职责、模块归属、评审和交接 |
| [接口文档](接口文档.md) | v0.1 拟定 REST API、数据模型、异步任务与版本冲突 |
| [技术栈说明](技术栈说明.md) | React Web、Android 移动端、Python 服务、色彩与 AI |
| [环境配置说明](环境配置说明.md) | 工具、配置、数据库、模拟器与真机连接 |
| [协作规范](CONTRIBUTING.md) | Git 流程、验证、密钥与 AI 编程记录 |

## 技术路线

- Web 前端：React、TypeScript、Vite、Tailwind CSS、Konva、Zustand、TanStack Query。
- Android 移动端：Kotlin、Jetpack Compose、Material 3、Navigation Compose、ViewModel/StateFlow、Retrofit/OkHttp、Coil、Room。
- 服务端：Python 3.12、FastAPI、Pydantic、SQLAlchemy、Alembic、PostgreSQL 16。
- 颜色计算：Pillow、OpenCV、NumPy、colour-science；多模态模型承担语义理解和解释，不代替准确取色。
- AI：通过服务端接入千问多模态 API；模型可替换，密钥不进入安装包。

## 当前可用的环境样例

复制 `.env.example` 为 `.env`，填写本地开发配置后执行 `docker compose --env-file .env -f compose.dev.yaml up -d db`，只启动数据库。其余运行说明见环境配置文档。

四人配置：A Web 前端，B 后端兼数据库，C 后端兼算法，D Android 移动端。

计划代码目录为 `frontend/`、`android/`、`backend/`、`data/catalog/` 和 `tests/`，尚未生成应用脚手架。小规模经过授权的作品元数据可版本管理；私人上传、缓存和大型素材留在存储中。

仓库尚未选择源码开源许可证；第三方模型、库和图像各自遵循原许可。
