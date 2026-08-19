/* ============================================================
   张政 作品集 · 作品数据
   ------------------------------------------------------------
   加一个新作品：
     1. 图片放进 assets/proj/，按 p17-01.webp、p17-02.webp … 命名
        （编号往后顺延，别和已有的 p01～p16 重复）
     2. 复制下面任意一段 { … }，粘到列表里；图片按顺序列进 images
     3. ord 决定排序，越小越靠前。要排在最前面就填一个比现有最小值
        更小的数（现在最小是 -1）；要排最后就填比最大值更大的数
     4. cat 六选一：
          "poster"     海报
          "book"       书籍装帧
          "event"      活动视觉
          "collateral" 项目物料
          "ui"         网页UI
     5. coverIdx = 用第几张图当封面（0 = 第一张）
   改完保存、推到仓库，网站一两分钟后自动更新。
   ============================================================ */

window.__ZZ_WORKS = [
  /* ↓↓↓ COMART 双年鉴：图片(p16-01.webp …)做好放进 assets/proj/ 后，
         把下面这段的注释去掉，并把 images 按实际张数补齐 ↓↓↓
  {
    ord: -1, id: "u1787106388407", cat: "book", year: "2025",
    title: "《COMART 国际数艺双年鉴》2024—2025",
    coverIdx: 0,
    images: [
      "assets/proj/p16-01.webp"
    ]
  },
  ↑↑↑ COMART 双年鉴 ↑↑↑ */
  {
    ord: 0, id: "u1786857110042", cat: "poster", year: "2024",
    title: "全球数字艺术标杆项目考察&引进之旅·日本站（第四站）未成团",
    coverIdx: 1,
    images: [
      "assets/proj/p01-01.webp",
      "assets/proj/p01-02.webp"
    ]
  },
  {
    ord: 1, id: "u1786856983922", cat: "poster", year: "2024",
    title: "全球数字艺术标杆项目考察&引进之旅·日本站（第三场）未成团",
    coverIdx: 0,
    images: [
      "assets/proj/p02-01.webp"
    ]
  },
  {
    ord: 2, id: "u1786696433243", cat: "event", year: "2024",
    title: "全球数字艺术标杆项目考察&引进之旅·日本站(第二站)",
    coverIdx: 0,
    images: [
      "assets/proj/p03-01.webp",
      "assets/proj/p03-02.webp",
      "assets/proj/p03-03.webp",
      "assets/proj/p03-04.webp",
      "assets/proj/p03-05.webp",
      "assets/proj/p03-06.webp",
      "assets/proj/p03-07.webp",
      "assets/proj/p03-08.webp",
      "assets/proj/p03-09.webp",
      "assets/proj/p03-10.webp",
      "assets/proj/p03-11.webp",
      "assets/proj/p03-12.webp"
    ]
  },
  {
    ord: 3, id: "u1786692557876", cat: "event", year: "2023",
    title: "全球数字艺术标杆项目考察&引进之旅·日本站（第一站）",
    coverIdx: 0,
    images: [
      "assets/proj/p04-01.webp",
      "assets/proj/p04-02.webp",
      "assets/proj/p04-03.webp",
      "assets/proj/p04-04.webp",
      "assets/proj/p04-05.webp",
      "assets/proj/p04-06.webp",
      "assets/proj/p04-07.webp",
      "assets/proj/p04-08.webp",
      "assets/proj/p04-09.webp",
      "assets/proj/p04-10.webp",
      "assets/proj/p04-11.webp",
      "assets/proj/p04-12.webp"
    ]
  },
  {
    ord: 4, id: "u1786438772417", cat: "event", year: "2024",
    title: "2024·苏州高新区数字文化产业合作发展大会",
    coverIdx: 1,
    images: [
      "assets/proj/p05-01.webp",
      "assets/proj/p05-02.webp",
      "assets/proj/p05-03.webp",
      "assets/proj/p05-04.webp",
      "assets/proj/p05-05.webp",
      "assets/proj/p05-06.webp",
      "assets/proj/p05-07.webp",
      "assets/proj/p05-08.webp",
      "assets/proj/p05-09.webp",
      "assets/proj/p05-10.webp",
      "assets/proj/p05-11.webp",
      "assets/proj/p05-12.webp",
      "assets/proj/p05-13.webp",
      "assets/proj/p05-14.webp",
      "assets/proj/p05-15.webp",
      "assets/proj/p05-16.webp",
      "assets/proj/p05-17.webp",
      "assets/proj/p05-18.webp",
      "assets/proj/p05-19.webp",
      "assets/proj/p05-20.webp",
      "assets/proj/p05-21.webp",
      "assets/proj/p05-22.webp",
      "assets/proj/p05-23.webp"
    ]
  },
  {
    ord: 5, id: "u1786345737902", cat: "event", year: "2025",
    title: "2025城聚·长沙站",
    coverIdx: 0,
    images: [
      "assets/proj/p06-01.webp",
      "assets/proj/p06-02.webp",
      "assets/proj/p06-03.webp",
      "assets/proj/p06-04.webp",
      "assets/proj/p06-05.webp",
      "assets/proj/p06-06.webp",
      "assets/proj/p06-07.webp",
      "assets/proj/p06-08.webp",
      "assets/proj/p06-09.webp",
      "assets/proj/p06-10.webp"
    ]
  },
  {
    ord: 6, id: "u1786265334500", cat: "event", year: "2025",
    title: "2025城聚·上海站",
    coverIdx: 1,
    images: [
      "assets/proj/p07-01.webp",
      "assets/proj/p07-02.webp",
      "assets/proj/p07-03.webp",
      "assets/proj/p07-04.webp",
      "assets/proj/p07-05.webp",
      "assets/proj/p07-06.webp",
      "assets/proj/p07-07.webp",
      "assets/proj/p07-08.webp",
      "assets/proj/p07-09.webp",
      "assets/proj/p07-10.webp",
      "assets/proj/p07-11.webp",
      "assets/proj/p07-12.webp"
    ]
  },
  {
    ord: 7, id: "u1786165931872", cat: "event", year: "2024",
    title: "2024城聚·杭州站",
    coverIdx: 0,
    images: [
      "assets/proj/p08-01.webp",
      "assets/proj/p08-02.webp",
      "assets/proj/p08-03.webp",
      "assets/proj/p08-04.webp",
      "assets/proj/p08-05.webp",
      "assets/proj/p08-06.webp",
      "assets/proj/p08-07.webp",
      "assets/proj/p08-08.webp",
      "assets/proj/p08-09.webp",
      "assets/proj/p08-10.webp",
      "assets/proj/p08-11.webp",
      "assets/proj/p08-12.webp",
      "assets/proj/p08-13.webp"
    ]
  },
  {
    ord: 8, id: "u1786071322146", cat: "event", year: "2024",
    title: "2024城聚·北京站",
    coverIdx: 0,
    images: [
      "assets/proj/p09-01.webp",
      "assets/proj/p09-02.webp",
      "assets/proj/p09-03.webp",
      "assets/proj/p09-04.webp",
      "assets/proj/p09-05.webp",
      "assets/proj/p09-06.webp",
      "assets/proj/p09-07.webp",
      "assets/proj/p09-08.webp",
      "assets/proj/p09-09.webp",
      "assets/proj/p09-10.webp",
      "assets/proj/p09-11.webp",
      "assets/proj/p09-12.webp"
    ]
  },
  {
    ord: 9, id: "u1786068127382", cat: "event", year: "2024",
    title: "2024城聚·济南站",
    coverIdx: 0,
    images: [
      "assets/proj/p10-01.webp",
      "assets/proj/p10-02.webp",
      "assets/proj/p10-03.webp",
      "assets/proj/p10-04.webp",
      "assets/proj/p10-05.webp",
      "assets/proj/p10-06.webp",
      "assets/proj/p10-07.webp",
      "assets/proj/p10-08.webp",
      "assets/proj/p10-09.webp",
      "assets/proj/p10-10.webp",
      "assets/proj/p10-11.webp"
    ]
  },
  {
    ord: 10, id: "u1785919124084", cat: "event", year: "2024",
    title: "2024城聚·深圳站",
    coverIdx: 0,
    images: [
      "assets/proj/p11-01.webp",
      "assets/proj/p11-02.webp",
      "assets/proj/p11-03.webp",
      "assets/proj/p11-04.webp",
      "assets/proj/p11-05.webp",
      "assets/proj/p11-06.webp",
      "assets/proj/p11-07.webp",
      "assets/proj/p11-08.webp",
      "assets/proj/p11-09.webp",
      "assets/proj/p11-10.webp"
    ]
  },
  {
    ord: 11, id: "u1785838351076", cat: "event", year: "2024",
    title: "2024城聚·苏州站",
    coverIdx: 0,
    images: [
      "assets/proj/p12-01.webp",
      "assets/proj/p12-02.webp",
      "assets/proj/p12-03.webp",
      "assets/proj/p12-04.webp",
      "assets/proj/p12-05.webp",
      "assets/proj/p12-06.webp",
      "assets/proj/p12-07.webp",
      "assets/proj/p12-08.webp",
      "assets/proj/p12-09.webp",
      "assets/proj/p12-10.webp",
      "assets/proj/p12-11.webp",
      "assets/proj/p12-12.webp",
      "assets/proj/p12-13.webp",
      "assets/proj/p12-14.webp",
      "assets/proj/p12-15.webp",
      "assets/proj/p12-16.webp"
    ]
  },
  {
    ord: 12, id: "u1785749231498", cat: "event", year: "2023",
    title: "2023城聚·上海站",
    coverIdx: 0,
    images: [
      "assets/proj/p13-01.webp",
      "assets/proj/p13-02.webp",
      "assets/proj/p13-03.webp",
      "assets/proj/p13-04.webp",
      "assets/proj/p13-05.webp",
      "assets/proj/p13-06.webp",
      "assets/proj/p13-07.webp",
      "assets/proj/p13-08.webp"
    ]
  },
  {
    ord: 13, id: "u1785558149711", cat: "event", year: "2023",
    title: "2023城聚·济南站",
    coverIdx: 0,
    images: [
      "assets/proj/p14-01.webp",
      "assets/proj/p14-02.webp",
      "assets/proj/p14-03.webp",
      "assets/proj/p14-04.webp",
      "assets/proj/p14-05.webp",
      "assets/proj/p14-06.webp",
      "assets/proj/p14-07.webp",
      "assets/proj/p14-08.webp"
    ]
  },
  {
    ord: 14, id: "u1785306705602", cat: "collateral", year: "2024",
    title: "数艺之友咖啡馆 X 爰跻书店",
    coverIdx: 1,
    images: [
      "assets/proj/p15-01.webp",
      "assets/proj/p15-02.webp",
      "assets/proj/p15-03.webp",
      "assets/proj/p15-04.webp",
      "assets/proj/p15-05.webp",
      "assets/proj/p15-06.webp",
      "assets/proj/p15-07.webp"
    ]
  }
];

/* 以下不用改 */
(function () {
  var d = (window.__ZZ_WORKS || []).slice();
  d.forEach(function (w) {
    w.cover = w.images[w.coverIdx] || w.images[0] || '';
    /* 卡片用 assets/thumb 里的 4:3 缩略图（省 75% 下载量），
       灯箱大图仍然用 images 里的原图。
       加了新作品后跑一次 `python3 生成缩略图.py` 重新生成。 */
    w.thumb = w.cover.replace('assets/proj/', 'assets/thumb/');
    delete w.coverIdx;
  });
  d.sort(function (a, b) { return (a.ord || 0) - (b.ord || 0); });
  window.__ZZ_PUBLISHED_SEED = d;
  window.__ZZ_SEED_TOTAL = d.length;
  /* 每次改上面的作品列表，这个数字都要 +1，
     否则老访客浏览器里的缓存会盖掉新内容 */
  window.__ZZ_SEED_VER = 5;
})();
