# CLAUDE.md

这是一个基于 VS Code 的 Markdown 文档写作工作台，用于 AI 辅助文档撰写与修订。

## 项目结构

- `ai-doc-workbench`（根目录）：存放工作区配置（`ai-doc-workbench.code-workspace`）与顶层要求。
- `workbench/`：写作工作区。其下每个一级子文件夹是一个写作任务的工作文件夹（`workbench/template/` 为工作文件夹模板）；文档勿直接堆放于 `workbench/` 下。
  - `workbench/<工作文件夹>`：`.import/` 存放导入的原始素材；`.assets/` 存放文档引用的媒体/二进制文件；`.export/` 存放导出的 DOCX 文档；其余结构由用户自由创建（如 `参考资料/`）。
- `extension/`：VS Code 插件，提供工作区所需各项功能的便捷操作入口，由开发者维护。
- `tools/`：Python 工具，实现工作区所需各项功能，由开发者维护。

## 工作流程

使用 VS Code 打开 `ai-doc-workbench.code-workspace`，按如下流程工作：

1. **新建项目**：在 `workbench/` 下新建工作文件夹，将整理后的素材文档放入其下的 `.import/`。
2. **转换素材**：右键素材文件或文件夹，选择「转换为 Markdown」，支持 PDF、DOCX、DOC、XLSX、XLS、PPTX、PPT 逐个或批量转换；将所得 Markdown 分类整理至工作文件夹内（如 `参考资料/`）。转换提取的图片存于该 Markdown 同级的 `<文件名>.assets/` 目录，以相对路径引用，移动该 Markdown 时须连同 `<文件名>.assets/` 目录一并移动。
3. **撰写与修订**：手动新建、撰写、修订 Markdown，或与 Claude Code 对话完成新建、撰写与修订；支持全局（整篇文档）与局部（段落、句子）撰写与修订。
4. **比较与提交**：通过 VS Code 自带的 Git diff 查看修订前后的内容；可在素材导入完成、文档撰写完成或所有修订均确认后提交一次。
5. **导出文档**：右键 Markdown 文件，选择「导出为 DOCX」；DOCX 默认生成于该 Markdown 旁，可移入 `.export/`。

## 注意事项

- **工作分支**：撰写、修订与提交均须在 `workbench` 分支下进行；`dev` 分支修改后，`workbench` 分支需主动与其合并，以获取功能更新。
- **样式模板**：Markdown 样式基准为 `workbench/template/template.md`，仅允许使用其中出现过的样式；标题层级为 `#` 文档标题、`##` 一级标题，依次递推。
- **读取范围**：用户在工作文件夹下撰写时，Claude Code 仅读取该文件夹下未被 `.gitignore` 忽略的文件（一般为 Markdown 及其他文本文件），不得读取上级或同级文件夹下的文件（样式模板 `workbench/template/template.md` 除外）。
- **版本控制范围**：在 `workbench` 分支下，`workbench/` 下所有未被 `.gitignore` 忽略的文件均由 Git 跟踪。
