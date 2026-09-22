# MovieLens Affiliation-Network Analysis：MovieLens 用户—电影 affiliation 外部验证

## 目标

使用固定 MovieLens 100K 基准数据，构造“用户—电影”属性关联网络，比较不同评分阈值下的覆盖率、全局/活跃层相关、排序逆转和top-K稳定性。

## 数据源

- 数据集：MovieLens 100K
- 官方文件：`ml-100k.zip`
- 规模：100,000条评分、943名用户、1,682部电影
- 引用：Harper & Konstan (2015), DOI `10.1145/2827872`
- 使用与再分发必须遵守官方README；原始数据不要提交到论文代码仓库。

## 下载

从官方目录下载 `ml-100k.zip`：

`https://files.grouplens.org/datasets/movielens/ml-100k.zip`

将文件保存到例如：`D:\research_data\movielens\ml-100k.zip`。

## 本文件夹入口

对所有评分建边：

```powershell
python 02_MovieLens\pipeline.py `
  --data-dir E:\Study\02_MovieLens `
  --rating-min 1
```

对正向偏好评分建边：

```powershell
python MovieLens\pipeline.py `
  --data-dir .\MovieLens `
  --rating-min 4
```

建议分别运行阈值 `1、3、4、5`，不同阈值使用不同输出目录，避免覆盖。

## Generated outputs

每个评分阈值分别提交：

1. `movielens_edges.csv`
2. `movielens_users.csv`
3. `movielens_metadata.json`
4. `movielens_q2.json`
5. 运行命令与终端日志
6. 阈值对比表
7. 一页语义说明：电影是共同属性语境，不是同时群体事件

## Methodological constraints

- 不得使用动态变化的 `ml-latest-small` 作为正式结果。
- 用户全集必须来自 `u.user`，不能只用评分阈值筛选后的活跃用户。
- 必须报告阈值造成的非活跃用户比例。
- MovieLens的电影规模较大，正式运行必须使用 `--skip-deduplicated`；不得强行枚举全部 `S2`。
- 不得把评分高低直接解释为供应链技术关系强度。

## 研究问题

1. 评分阈值提高后，共同零值比例怎样变化？
2. 全体相关与活跃层相关之间的差距是否扩大？
3. top-K用户集合是否比全局相关更稳定或更有辨识力？
4. 零节点敏感性是否重复船舶网络中的机械抬升现象？

