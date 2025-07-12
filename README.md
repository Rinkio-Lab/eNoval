# 📖 eNoval: 终端小说阅读器

[English](README_en.md) | [日本語](README_jp.md)

一个轻量、纯 Python 的终端小说阅读器，专为命令行爱好者设计。它支持 `.txt` 小说文件，提供章节识别、阅读进度保存、书签标记和章节搜索等核心功能，让您在终端中也能享受沉浸式阅读体验！

![screenshot](assets/screenshot.png) <!-- 您可以在此处添加项目截图 -->

---

## ✨ 主要功能

-   **智能分页**：根据终端尺寸自动调整内容显示，提供最佳阅读布局。
-   **章节识别**：通过正则表达式自动提取章节标题（支持“章”、“节”、“回”等多种形式）。
-   **进度管理**：自动保存阅读进度，确保您随时回到上次阅读的地方。
-   **书签功能**：轻松标记和恢复特定章节，方便回顾。
-   **快速导航**：支持章节搜索和跳转，快速定位所需内容。
-   **国际化支持**：支持多语言界面（中文、英文、日文），提升用户体验。
-   **配置设置**：通过 `config.yaml` 文件轻松配置默认语言等应用设置。
-   **统一命令风格**：采用 `>>>` 风格的命令提示符，简洁易用。
-   **离线可用**：无需网络连接，随时随地享受阅读。

---

## 📦 安装与使用

本项目推荐使用 [`uv`](https://github.com/astral-sh/uv) 包管理器，它比 `pip` 更快、更高效。

### 🛠️ 安装 uv

您可以通过以下方式安装 `uv`：

**独立安装器**：

```bash
# 在 macOS 和 Linux 上
curl -LsSf https://astral.sh/uv/install.sh | sh
# 在 Windows 上
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**通过 PyPI 安装**：

```bash
# 使用 pip
pip install uv
# 或者使用 pipx
pipx install uv
```

如果通过独立安装器安装，`uv` 可以自行更新到最新版本：

```bash
uv self update
```

更多详细信息和替代安装方法，请参阅 [uv 官方安装文档](https://astral.sh/uv/install)。

### 🚀 快速开始

1.  **安装依赖**：

    ```bash
    uv init
    uv add rich pyyaml
    ```

2.  **准备小说文件**：

    将您的 `.txt` 小说文件放入项目根目录下的 `library/` 文件夹中。

3.  **启动阅读器**：

    ```bash
    uv run main.py
    ```

---

## 📷 示例

```text
📘 我的小说.txt — 第 3 / 158 页

这是正文内容……
这是正文内容……
这是正文内容……

>>> [n]下一页 [p]上一页 [q]退出 [g]跳页 [m]目录 [j]跳章节 [c]清除进度 [b]章节书签
```

---

## 📚 命令指南

| 命令         | 功能说明             |
| :----------- | :------------------- |
| `n` 或直接回车 | 阅读下一页           |
| `p`          | 返回上一页           |
| `g`          | 跳转到指定页码       |
| `m`          | 查看书籍章节目录     |
| `j`          | 跳转到指定章节编号   |
| `b`          | 标记当前章节为书签   |
| `c`          | 清除当前书籍的阅读进度 |
| `s`          | 进入设置菜单（可更改语言等） |
| `q`          | 保存进度并退出阅读器 |

---

## 📂 项目结构

```
.
├── main.py           # 主程序入口
├── config.yaml       # 配置文件，用于设置默认语言等
├── progress.yaml     # 自动生成的阅读进度保存文件
├── library/          # 存放 .txt 小说文件的目录
├── lang/             # 存放多语言翻译文件的目录
│   ├── en.json
│   ├── jp.json
│   └── zh-cn.json
├── assets/           # 存放截图及其他资源（可选）
```

---

## 🛠️ 技术栈

-   **Python 3.8+**
-   **[Rich](https://github.com/Textualize/rich)**：用于美化终端输出，提供丰富的色彩和样式。
-   **PyYAML**：用于将阅读进度数据存储为 YAML 格式。
-   **标准库**：`os`, `re`, `shutil`, `textwrap`.

---

## 📜 许可证

本项目采用 MIT 许可证发布。详情请参阅 `LICENSE` 文件。

MIT License © 2025 [Rinkio-Lab](https://github.com/Rinkio-Lab/)

---

## 🤝 贡献

感谢您对 eNoval 的关注！如果您有任何建议或想贡献代码，欢迎提交 Pull Request 或提出 Issue。让我们一起将终端阅读体验推向极致！💪📚
