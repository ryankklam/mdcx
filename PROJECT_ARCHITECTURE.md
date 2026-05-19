# MDCx 项目架构与功能分析

## 项目概述

**MDCx** 是一个用于电影/视频元数据抓取和管理的工具，支持从多个成人视频网站自动获取视频信息、封面、演员等数据，并生成符合媒体服务器（如 Emby）要求的元数据文件。

### 项目历史
- 基于早期项目 Movie_Data_Capture (CLI 工具) 和 AVDC (PyQt GUI 版本)
- 2023年在原作者删库后，基于遗留版本进行重构和维护

---

## 技术栈

### 后端 (Python)
- **GUI 框架**: PyQt5
- **Web 框架**: FastAPI (提供 REST API 和 WebSocket 服务)
- **Web 自动化**: patchright (Playwright)
- **网络请求**: httpx, curl-cffi
- **数据解析**: BeautifulSoup4, lxml, parsel
- **图像处理**: Pillow, OpenCV
- **视频处理**: av (PyAV)
- **配置管理**: pydantic-settings
- **AI/LLM**: OpenAI API 集成
- **中文转换**: zhconv

### 前端 (React + TypeScript)
- **构建工具**: Rsbuild
- **UI 框架**: Material-UI (MUI)
- **状态管理**: Zustand, React Query
- **路由**: TanStack Router
- **表单处理**: React JSON Schema Form (RJSF)
- **拖拽功能**: @dnd-kit
- **API 生成**: @hey-api/openapi-ts

---

## 核心功能

### 1. 元数据抓取
- **多网站支持**: 内置 40+ 个爬虫，包括 DMM、JavBus、JavLibrary、FC2 等
- **智能识别**: 根据文件名自动识别番号类型（有码/无码/国产/FC2/同人等）
- **字段优先级**: 可配置不同字段从不同网站获取的优先级
- **数据整合**: 合并多个来源的数据，生成完整元数据

### 2. 文件管理
- **批量处理**: 支持批量扫描和处理视频文件
- **文件重命名**: 根据元数据自动重命名文件
- **目录整理**: 按规则整理视频文件目录结构
- **NFO 生成**: 生成符合 Kodi/Emby 标准的 NFO 元数据文件

### 3. 媒体处理
- **封面下载**: 自动下载视频封面和缩略图
- **海报裁剪**: 内置海报裁剪工具
- **视频信息提取**: 从视频文件中提取元数据

### 4. 界面与交互
- **桌面应用**: PyQt5 实现的传统桌面 GUI
- **Web UI**: 基于 React 的现代化 Web 界面
- **双模式支持**: 可通过桌面应用或 Web 服务访问

---

## 项目结构

```
/workspace/
├── mdcx/                    # 核心 Python 包
│   ├── base/               # 基础工具模块
│   │   ├── file.py         # 文件操作
│   │   ├── image.py        # 图像处理
│   │   ├── number.py       # 番号解析
│   │   ├── translate.py    # 翻译功能
│   │   ├── video.py        # 视频处理
│   │   └── web.py          # Web 工具
│   ├── cmd/                # 命令行工具
│   ├── config/             # 配置管理
│   │   ├── models.py       # 配置数据模型
│   │   ├── manager.py      # 配置管理器
│   │   └── enums.py        # 枚举定义
│   ├── controllers/        # UI 控制器
│   │   └── main_window/    # 主窗口控制器
│   ├── core/               # 核心业务逻辑
│   │   ├── file_crawler.py # 文件扫描和爬虫调度
│   │   ├── scraper.py      # 数据抓取核心
│   │   └── nfo.py          # NFO 文件生成
│   ├── crawlers/           # 网站爬虫实现
│   │   ├── base/           # 爬虫基类
│   │   │   ├── base.py     # 通用爬虫基类
│   │   │   ├── compat.py   # 兼容性适配
│   │   │   ├── parser.py   # 数据解析器
│   │   │   └── types.py    # 类型定义
│   │   └── [各网站爬虫]    # 40+ 个网站的具体实现
│   ├── gen/                # 自动生成的代码
│   ├── models/             # 数据模型
│   ├── server/             # Web 服务端
│   │   ├── api/            # REST API
│   │   └── ws/             # WebSocket 服务
│   ├── tools/              # 辅助工具
│   ├── utils/              # 通用工具函数
│   ├── views/              # PyQt UI 视图
│   ├── browser.py          # 浏览器自动化
│   ├── crawler.py          # 爬虫提供者
│   ├── consts.py           # 常量定义
│   └── signals.py          # 信号系统
├── ui/                     # React 前端
│   ├── src/
│   │   ├── client/         # API 客户端（自动生成）
│   │   ├── components/     # React 组件
│   │   ├── contexts/       # React Context
│   │   ├── hooks/          # 自定义 Hooks
│   │   ├── routes/         # 路由
│   │   ├── store/          # Zustand 状态管理
│   │   └── App.tsx         # 应用入口
│   └── package.json
├── resources/              # 资源文件
│   ├── Img/                # 图标和图片
│   ├── fonts/              # 字体文件
│   └── mapping_table/      # 映射表
├── scripts/                # 构建和开发脚本
├── tests/                  # 测试代码
├── main.py                 # PyQt 桌面应用入口
├── server.py               # FastAPI 服务入口
└── pyproject.toml          # 项目配置
```

---

## 核心模块详解

### 1. 爬虫系统 ([mdcx/crawlers/](file:///workspace/mdcx/crawlers/))

#### 架构设计
爬虫系统采用分层设计：
- **基类层** ([base/base.py](file:///workspace/mdcx/crawlers/base/base.py)): 定义通用爬虫接口和基础功能
- **解析层** ([base/parser.py](file:///workspace/mdcx/crawlers/base/parser.py)): 提供 HTML/XML 解析工具
- **兼容性层** ([base/compat.py](file:///workspace/mdcx/crawlers/base/compat.py)): 适配旧版爬虫代码
- **实现层**: 各网站独立爬虫实现

#### 爬虫提供者 ([mdcx/crawler.py](file:///workspace/mdcx/crawler.py))
`CrawlerProvider` 类负责：
- 懒加载爬虫实例
- 管理浏览器自动化实例
- 提供统一的爬虫获取接口

### 2. 文件扫描与数据抓取 ([mdcx/core/file_crawler.py](file:///workspace/mdcx/core/file_crawler.py))

`FileScraper` 类是核心业务逻辑：
- **番号识别**: 从文件名中提取番号
- **网站调度**: 根据番号类型选择合适的网站组
- **字段聚合**: 按优先级从不同网站获取各字段
- **数据清洗**: 统一处理日期、评分、标签等格式

### 3. 配置系统 ([mdcx/config/](file:///workspace/mdcx/config/))

采用 pydantic 进行配置管理：
- 支持多配置文件切换
- 字段级优先级配置
- 网站启用/禁用配置
- UI 配置通过 JSON Schema 生成表单

### 4. Web 服务 ([server.py](file:///workspace/server.py))

FastAPI 服务提供：
- REST API: 配置、文件、任务管理
- WebSocket: 实时日志推送、进度更新
- 静态文件服务: 托管 React 前端

### 5. 前端架构 ([ui/src/](file:///workspace/ui/src/))

- **状态管理**: Zustand 管理日志，React Query 管理服务端数据
- **路由**: TanStack Router 提供类型安全的路由
- **表单**: React JSON Schema Form 自动生成配置表单
- **实时通信**: WebSocket 接收日志和进度

---

## 工作流程

### 典型使用流程

1. **文件扫描**
   - 用户选择目录
   - 系统扫描视频文件
   - 提取文件名中的番号

2. **元数据抓取**
   - 根据番号类型选择网站组
   - 按配置的优先级调用各网站爬虫
   - 聚合多源数据

3. **数据处理**
   - 下载封面和缩略图
   - 生成 NFO 文件
   - 重命名和整理文件

4. **结果输出**
   - 保存元数据
   - 更新媒体库

---

## 扩展性与可维护性

### 新增网站爬虫
1. 在 [mdcx/crawlers/](file:///workspace/mdcx/crawlers/) 下创建新文件
2. 继承 `GenericBaseCrawler` 或使用兼容性适配器
3. 在 [mdcx/config/enums.py](file:///workspace/mdcx/config/enums.py) 中添加网站枚举
4. 实现 `search` 和 `get_detail` 方法

### 配置扩展
配置通过 JSON Schema 定义，在 [mdcx/config/ui_schema.py](file:///workspace/mdcx/config/ui_schema.py) 中添加新字段即可自动在 UI 中显示。

---

## 构建与部署

### 桌面应用
使用 PyInstaller 打包为单文件可执行程序，支持 Windows、macOS、Linux。

### Web 服务
- 后端: FastAPI + Uvicorn
- 前端: Rsbuild 构建静态文件
- 支持 Docker 部署

---

## 开发指南

### 环境设置
```bash
# 后端
uv sync
uv pip install -e ".[web,dev]"

# 前端
cd ui
pnpm install
```

### 运行开发环境
```bash
# 桌面应用
python main.py

# Web 服务
fastapi dev server.py

# 前端开发
cd ui
pnpm dev
```

### 代码规范
- 后端: Ruff 格式化和 lint
- 前端: Biome 格式化和 lint
- 提交前自动检查 (pre-commit)
