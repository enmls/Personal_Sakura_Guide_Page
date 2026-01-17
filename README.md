# Personal_Sakura_Guide_web

## 📖 项目简介

本项目是基于 [Personal_Sakura_Guide_Page]([原项目链接](https://github.com/NianBroken/Personal_Sakura_Guide_Page)) 使用 **Flask** 框架重构的 Web 版本。

---

## ✨ 新增功能

### 🚀 新特性
- ✅ **新增登录页面** - 用户身份验证系统
- ✅ **自定义 404 页面** - 友好的错误提示界面
- ✅ **文件管理** - 支持文件上传与下载
- ✅ **在线 Python 编辑器** - 可直接编辑和运行 Python 脚本

### 🎨 界面优化
- **文字丝滑下划线特效** - 鼠标悬停时显示动态下划线
- **实时 IP 显示** - 在首页展示用户当前的 IP 地址及地理位置信息
在首页显示格式示例：您当前 IP 地址：123.xx.xx.xx 中国-香港 城市电讯有限公司
---

## 🌐 IP 显示功能说明


### 📦 依赖组件
- **纯真 IP 数据库离线版**（需手动配置）
  - 数据库文件：`cz88_public_v4.czdb`
  - 需要对应的解密密钥（key）

### ⚙️ 配置方法
1. 获取纯真 IP 数据库文件(官网),pip install czdb-searcher
2. 将 `cz88_public_v4.czdb` 文件放置于指定目录
3. 在配置文件中设置正确的密钥
4. 重启应用生效

---

## 🛠️ 技术栈

```bash
Python 3.x
Flask
HTML/CSS/JavaScript
纯真 IP 数据库

<img width="873" height="769" alt="image" src="https://github.com/user-attachments/assets/1bcb0c56-5563-470d-a98f-ebd3fd001e4b" />

