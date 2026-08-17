# 张政 个人作品集 · 网站版

一个纯静态网站，没有后端、没有构建步骤。把这个文件夹推到 Git 仓库就能上线。

**首页**：`index.html`（自动跳到 `portfolio.dc.html`）
**总体积**：约 20 MB（157 张项目图 + 22 张海报，全部 WebP）

---

## 一、部署（推荐 Cloudflare Pages，免费 + 流量无上限）

### 第 1 步：把代码放到 GitHub

最简单的方式，不用命令行：

1. 打开 https://github.com/new，仓库名填 `portfolio`，选 **Public**，创建
2. 进入仓库，点 **uploading an existing file**
3. 把这个文件夹里的**所有内容**拖进去（这个包已经是干净的，全部都要）
4. 点 **Commit changes**

> 图片较多，上传要几分钟。GitHub 网页版单次最多 100 个文件，`assets/proj/` 里有 157 张，分两次拖即可（先拖 `assets` 外的所有文件 + `assets/works`，再单独拖 `assets/proj`）。
> 嫌麻烦就装 **GitHub Desktop**，把整个文件夹拖进去一次搞定，以后更新也是点两下。

### 第 2 步：Cloudflare Pages 接管

1. 打开 https://dash.cloudflare.com，注册（免费，不用实名）
2. 左侧 **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
3. 授权 GitHub，选中刚建的 `portfolio` 仓库
4. 构建设置**全部留空**（这是纯静态站，没有构建命令）
5. **Save and Deploy**，等约 1 分钟

拿到网址：`https://portfolio-xxx.pages.dev` —— 这就是发给 HR 的链接。

### 想更快看到结果？

不想碰 Git：打开 https://app.netlify.com/drop，把整个文件夹拖进浏览器，30 秒出链接。缺点是之后更新要重新拖一次全部文件。

---

## 二、加新作品

只改一个文件：**`works-data.js`**

### 1. 放图片

图片存进 `assets/proj/`，按现有规则命名：

```
p16-01.webp   ← 第 16 组作品的第 1 张
p16-02.webp   ← 第 2 张
```

格式建议 WebP 或 JPG，长图宽度 1600px、横图 1500px 就够清晰，单张控制在 300 KB 以内。

### 2. 登记作品

打开 `works-data.js`，把新作品加到列表**最前面**：

```js
window.__ZZ_WORKS = [
  {
    ord: 15, id: "u20260817", cat: "event", year: "2026",
    title: "作品名称",
    coverIdx: 0,
    images: [
      "assets/proj/p16-01.webp",
      "assets/proj/p16-02.webp"
    ]
  },
  // ↓ 原来的作品保持不动
```

| 字段 | 填什么 |
| --- | --- |
| `ord` | 排序号，填一个比现有最大值更大的数字 |
| `id` | 唯一标识，随便填，别和现有的重复 |
| `cat` | 只能是 `"event"`（活动策划）/ `"poster"`（海报）/ `"collateral"`（物料） |
| `year` | 年份，显示在卡片上 |
| `title` | 作品名 |
| `coverIdx` | 用第几张图当封面，`0` = 第一张 |
| `images` | 图片路径，按你想要的展示顺序排 |

### 3. 推上去

GitHub Desktop 里点 **Commit** → **Push**，Cloudflare 一两分钟后自动更新，链接不变。

> 如果你自己改过网站内容（在页面上传过作品），浏览器里可能存着旧缓存。改 `works-data.js` 最后那行的 `__ZZ_SEED_VER` 数字 +1，缓存就会被新数据覆盖。

---

## 三、管理入口

页面上的「上传作品」和卡片上的「编辑」按钮**默认隐藏**，HR 看不到。

需要用的时候，网址后面加 `#admin`：

```
https://portfolio-xxx.pages.dev/portfolio.dc.html#admin
```

注意：这里上传的作品只存在**你自己的浏览器里**，别人打不开。要真正上线，还是按上面第二节改 `works-data.js`。

---

## 四、文件说明

| 文件 | 作用 |
| --- | --- |
| `index.html` | 首页，跳转到作品集 |
| `portfolio.dc.html` | 作品集主页面 |
| `resume.dc.html` | 简历（作品集里点「查看简历」弹出） |
| `works-data.js` | **作品清单 —— 加作品改这里** |
| `assets/proj/` | 项目图（157 张） |
| `assets/works/` | 节日海报（22 张） |
| `assets/` | 头像、公司 logo、图标、鱼缸动画 |
| `support.js` `rive-asset.js` | 运行库，别动 |

---

## 五、已知事项

- **外部依赖**：页面从 CDN 加载 React、Lenis（滚动）、Rive（鱼缸动画）。已配 jsDelivr + unpkg 双线兜底，国内正常访问。
- **简历字体**走 Google Fonts，国内可能加载慢并回退到系统字体（排版不变）。要彻底解决可以换成本地字体，跟我说。
- **想换成自己的域名**：Cloudflare Pages 里绑域名不用 ICP 备案（服务器在境外）。国内服务器托管才需要备案。
- **离线单文件版**（发邮件用的那两个大文件）不在这个包里，两条路互不影响。
