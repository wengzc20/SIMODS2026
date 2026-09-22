# DBLP Affiliation-Network Analysis：DBLP 作者—论文 affiliation 外部验证

## 目标

使用 DBLP 官方月度版本化 XML 快照，构造真实“作者—论文”二分关系，并运行统一高阶表示适用性诊断。禁止使用作者共著投影图，也禁止从投影图三角形反推论文。

## 数据源

- 固定版本：DBLP Monthly Snapshot `2026-07-01`
- DOI：`10.4230/dblp.xml.2026-07-01`
- XML 官方 MD5：`22550bbcdaf58412bd5fbc1e04825a8b`
- DTD：`2023-06-28`
- DTD 官方 MD5：`96e4283e71886dec2173718957293648`
- 许可：CC0 1.0

## 本文件夹入口

运行：

```powershell
python DBLP\pipeline.py plan
```

下载约1GB数据：

```powershell
python student_tasks\01_DBLP\pipeline.py download --data-dir D:\research_data\dblp
```

转换建议先做小规模冒烟测试：

```powershell
python student_tasks\01_DBLP\pipeline.py convert `
  --data-dir D:\research_data\dblp `
  --year-min 2023 --year-max 2025 `
  --max-records 10000
```

冒烟测试通过后去掉 `--max-records`，运行正式转换。随后：

```powershell
python student_tasks\01_DBLP\pipeline.py diagnose --data-dir D:\research_data\dblp
```

## Generated outputs

1. `dblp_edges.csv`
2. `dblp_authors.csv`
3. `dblp_metadata.json`
4. `dblp_q2.json`
5. 运行命令与终端日志
6. 数据文件MD5/SHA-256核验截图或文本
7. 一页结果说明：全体/活跃相关、逆转率、top-K、零节点敏感性

## Methodological constraints

- 不得使用 `com-dblp.ungraph`。
- 不得把共著边或共著三角形当成论文。
- 必须保留 DBLP publication key。
- 必须记录快照版本、DTD版本、年份和文献类型过滤条件。
- 正式结果不得使用 `--max-records` 截断。
- 若使用姓名作为PID缺失时的回退，必须报告回退比例。

## 研究问题

1. 活跃作者中 `k` 与 `P2` 的相关是否仍然很高？
2. top-5%、top-10%作者集合是否一致？
3. 追加共同零节点后，Spearman/Kendall是否机械趋近1？
4. 结果是否随年份窗口或论文类型改变？

