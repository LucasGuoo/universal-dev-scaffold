# Design — <feature-name>

> 模板：proposal 确认后填写。聚焦"怎么拆"，不写逐行代码（代码在 tasks）。
> 借鉴 writing-plans 的 Scope Check / File Structure / Interfaces。

## 1. 范围与子系统拆分
（若跨多独立子系统，列出每系统边界，各自可独立测试交付）

## 2. 文件结构与职责
（创建 / 修改哪些文件；单一职责、小文件优先）

## 3. 关键接口契约
（模块间 `Consumes` / `Produces` 精确签名，供 `tasks.md` 直接引用，避免信息墙）

## 4. 数据流 / 时序
（关键路径示意）

## 5. 风险与回退
