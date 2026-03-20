---
name: medlit-research
description: 医学文献检索、批判性评价与综合分析。支持PubMed/Embase/Cochrane多数据库检索、PMC全文获取、AI辅助分析、研究质量评价、系统综述写作。使用场景：(1)检索多数据库医学文献，(2)自动获取PMC开放获取全文，(3)基于全文的深度批判性评价，(4)AI辅助PICO提取与质量评价，(5)辅助系统综述和Meta分析。
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: erongcao/medlit-research
# corpus-url: https://github.com/erongcao/medlit-research/blob/cc245745bf39315a97d11dc9cc77f9502ce833d0/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# 医学文献检索与批判性评价

综合医学文献检索、全文获取、AI辅助分析、质量评价和分析工具，支持循证医学实践。

## 核心功能

1. **多数据库检索** - PubMed + Embase + Cochrane
2. **PMC全文获取** - 自动识别并下载开放获取文献
3. **全文深度评价** - 基于完整论文的结构化批判性评价
4. **AI辅助分析** - 自动提取PICO、生成摘要、评价研究质量
5. **多维度分析** - 从摘要到全文的多层次质量评估

## 使用场景

### 场景1: 多数据库联合检索

```bash
# 多数据库检索（PubMed + Embase + Cochrane）
python3 scripts/multi_database_search.py "intestinal fibrosis" \
  --dbs pubmed,embase,cochrane \
  --max 20 \
  --date 2022:2025

# 仅检索PubMed
python3 scripts/multi_database_search.py "liver cirrhosis treatment" \
  --dbs pubmed \
  --max 30
```

### 场景2: 检查文献可获取性并获取全文

```bash
# 检查单篇文献的开放获取状态
python3 scripts/pmc_fulltext.py 39024569

# 直接通过PMC ID获取全文
python3 scripts/pmc_fulltext.py PMC10850402
```

输出包含：
- 可获取性状态（开放获取/PMC免费/仅摘要）
- 全文内容（标题、摘要、分节文本）
- 自动提取的关键信息（研究设计、样本量、主要发现等）

### 场景3: 基于全文的深度批判性评价

```bash
# 生成全文评价清单（RCT）
python3 scripts/fulltext_appraisal.py RCT

# 生成系统综述评价清单
python3 scripts/fulltext_appraisal.py systematic_review

# 生成观察性研究评价清单
python3 scripts/fulltext_appraisal.py observational
```

评价维度：
- **必需项目** (Essential) - 影响研究质量的关键要素
- **重要项目** (Important) - 提升研究质量的重要要素
- **可选项目** (Optional) - 增强透明度的补充要素

### 场景4: AI辅助文献分析

```bash
# AI分析单篇文献（提取PICO + 质量评价 + 临床建议）
python3 scripts/ai_assistant.py paper.txt all

# 仅提取PICO要素
python3 scripts/ai_assistant.py paper.txt pico

# 生成一句话核心发现
python3 scripts/ai_assistant.py paper.txt summary

# 研究质量评价
python3 scripts/ai_assistant.py paper.txt quality
```

AI分析输出包括：
- **PICO提取** - 自动识别研究人群、干预、对照、结局
- **一句话总结** - "在[人群]中，[干预]相比[对照]，[主要结局]"
- **质量评价** - 证据等级、GRADE质量、优缺点分析
- **临床建议** - 是否推荐使用、适用人群、关键考虑因素

### 场景5: 完整工作流程

```bash
# 1. 多数据库检索
python3 scripts/multi_database_search.py "主题词" --date 2022:2025 --max 30 > search_results.json

# 2. 筛选开放获取文献并获取全文
python3 scripts/pmc_fulltext.py PMID > fulltext.json

# 3. AI辅助分析（自动提取关键信息）
python3 scripts/ai_assistant.py fulltext.txt all > ai_analysis.json

# 4. 全文深度评价
python3 scripts/fulltext_appraisal.py RCT > appraisal_template.json

# 5. 填写评价结果并计算质量评分
# （结合AI分析结果和人工评价）
```

## 数据库支持

### PubMed (已配置)
- ✅ 完整支持
- ✅ 通过NCBI E-utilities API
- ✅ 无需API Key
- ⚠️ 速率限制: 每秒3次请求

### Embase (需配置)
- ⏳ 需要Elsevier API Key
- 配置方法:
  ```bash
  export EMBASE_API_KEY="your_api_key_here"
  ```
- 获取API Key: https://dev.elsevier.com/

### Cochrane Library (手动)
- 📖 建议通过网页搜索
- 替代方案: PubMed中使用 `"cochrane database syst rev"[ta]` 过滤器
- 直接访问: https://www.cochranelibrary.com/

## PMC全文获取

### 可获取性类型

1. **Open Access** - 完全开放获取
2. **PMC Free** - PubMed Central免费全文
3. **Free Article** - 出版商免费提供
4. **Abstract Only** - 仅摘要可用

### 全文结构解析

获取的全文自动解析为：
- **Title** - 标题
- **Abstract** - 摘要
- **Introduction** - 引言/背景
- **Methods** - 方法
- **Results** - 结果
- **Discussion** - 讨论
- **Conclusion** - 结论
- **Full Text** - 完整文本

### 关键信息自动提取

系统自动提取：
- 研究设计类型
- 样本量
- 干预措施
- 主要结局
- 统计方法
- 关键发现
- 作者声明的局限性

## AI辅助分析工具

### ai_assistant.py - 智能文献分析

**功能**: 自动提取关键信息、生成摘要、评价质量

**分析维度**:

#### 1. PICO自动提取
- **Population** - 样本量、人群特征、纳排标准
- **Intervention** - 干预措施细节、剂量、疗程
- **Comparison** - 对照类型、对照措施
- **Outcomes** - 主要/次要结局、随访时间

#### 2. 一句话总结
格式规范：
```
在[研究人群]中，[干预措施]相比[对照措施]，
[主要发现/效应量]（证据质量：[GRADE等级]）
```

#### 3. 质量评价 (GRADE框架)
- **证据质量** - 高/中/低/极低
- **降级因素** - 研究局限、不一致性、间接性、不精确、发表偏倚
- **升级因素** - 大效应、剂量反应、残余混杂
- **优缺点分析** - 关键优势和局限性

#### 4. 临床适用性建议
- **推荐强度** - 强烈推荐/有条件推荐/不推荐
- **适用人群** - 研究人群的外推性
- **关键考虑** - 实施时的注意事项

**使用示例**:
```bash
# 准备文献文本文件（标题+摘要）
echo "标题: ...
摘要: ..." > paper.txt

# 全面分析
python3 scripts/ai_assistant.py paper.txt all

# 输出JSON格式，便于后续处理
python3 scripts/ai_assistant.py paper.txt all > analysis.json
```

**与人工评价结合**:
AI分析作为初筛和辅助，最终临床决策仍需专业人员结合全文和临床经验判断。

## 批判性评价工具

### 基础评价 (basic_appraisal.py)
- 快速评价清单
- 适用于摘要水平的初步筛选
- 按研究类型定制

### 全文深度评价 (fulltext_appraisal.py)
- 基于完整论文的深度评价
- 符合CONSORT、PRISMA等报告规范
- 结构化分节评价
- 自动计算质量评分

### 评价维度

#### RCT评价维度 (基于CONSORT)
- 标题和摘要 (3项)
- 引言 (3项)
- 方法 (9项)
- 结果 (6项)
- 讨论 (3项)
- 其他 (3项)

#### 系统综述评价维度 (基于PRISMA)
- 标题和摘要 (2项)
- 引言 (3项)
- 方法 (10项)
- 结果 (8项)
- 讨论 (3项)

#### 观察性研究评价维度 (基于STROBE)
- 方法 (7项)
- 结果 (4项)

### 质量评分系统

- **必需项目** (Essential): 权重最高，缺失严重影响质量
- **重要项目** (Important): 权重中等，缺失影响可信度
- **可选项目** (Optional): 权重较低，增强透明度

**总体判断标准**:
- ≥90% 必需项目满足 → 低偏倚风险 (Low Risk)
- 70-89% 必需项目满足 → 存在一些担忧 (Some Concerns)
- <70% 必需项目满足 → 高偏倚风险 (High Risk)

## 检索策略建议

### 构建有效检索式

```
# PICO框架
(Patient terms) AND (Intervention terms) AND (Outcome terms)

# 示例
("Crohn disease"[mh] OR "Crohn*"[tiab]) AND ("fibrosis"[mh] OR "fibrotic"[tiab] OR "stricture*"[tiab])
```

### 常用过滤器

**RCT过滤器**:
```
randomized controlled trial[pt] OR (randomized[tiab] AND controlled[tiab] AND trial[tiab])
```

**系统综述过滤器**:
```
systematic review[pt] OR meta-analysis[pt] OR ("systematic review"[ti] AND review[pt])
```

**人类研究**:
```
Humans[mh] NOT Animals[mh]
```

**英文文献**:
```
English[la]
```

**近3年**:
```
(2022:2025[dp])
```

## 输出格式

### AI辅助分析结果
```json
{
  "pico": {
    "population": "肝硬化伴食管静脉曲张患者 (n=120, 平均年龄58岁)",
    "intervention": "普萘洛尔 40mg bid + 内镜套扎术",
    "comparison": "单独内镜套扎术",
    "outcomes": ["静脉曲张再出血率", "死亡率", "不良反应"],
    "study_design": "多中心随机对照试验"
  },
  "one_sentence_summary": "在肝硬化伴食管静脉曲张患者中，普萘洛尔联合内镜套扎术相比单独套扎术可显著降低再出血率（证据质量：高）",
  "clinical_significance": "对于高危静脉曲张患者，联合治疗可能降低再出血风险约40%",
  "quality": {
    "study_design": "多中心RCT",
    "evidence_level": "I级",
    "evidence_quality": "高",
    "key_strengths": ["多中心设计", "样本量充足", "ITT分析", "盲法充分"],
    "key_limitations": ["随访时间仅12个月", "未报告生活质量", "失访率偏高"],
    "bias_risk": "低",
    "applicability": "适用于肝功能Child-Pugh A-B级患者"
  },
  "statistics": {
    "effect_size": "HR 0.58 (95%CI 0.42-0.81)",
    "p_value": "<0.001",
    "clinical_importance": "有临床意义"
  },
  "recommendation": {
    "clinical_use": "强烈推荐",
    "target_population": "肝硬化伴中-重度食管静脉曲张患者",
    "key_considerations": ["需监测心率", "禁忌于严重心衰", "需患者依从性好"],
    "confidence": "高"
  }
}
```

### 多数据库检索结果
```json
{
  "query": "检索词",
  "databases_searched": ["pubmed", "embase", "cochrane"],
  "results_by_database": {
    "pubmed": { ... },
    "embase": { ... },
    "cochrane": { ... }
  },
  "summary": {
    "total_articles_found": 150
  }
}
```

### PMC全文获取结果
```json
{
  "pmid": "12345678",
  "pmcid": "PMC1234567",
  "status": "success",
  "article_info": {
    "title": "...",
    "abstract": "...",
    "sections": { ... },
    "full_text": "..."
  },
  "analysis": {
    "study_design": "RCT",
    "sample_size": 256,
    "key_findings": [ ... ]
  }
}
```

### 全文评价结果
```json
{
  "study_type": "RCT",
  "overall_judgment": "low_risk",
  "essential_items": {
    "answered": 25,
    "total": 27,
    "score": 92.6
  },
  "sections": {
    "methods": {
      "items": [ ... ]
    }
  }
}
```

## 最佳实践

### 系统综述工作流程

1. **制定检索策略**
   - 使用PICO明确研究问题
   - 构建多数据库检索式
   - 设定日期和语言限制

2. **执行多数据库检索**
   ```bash
   python3 scripts/multi_database_search.py "query" --dbs pubmed,embase --date 2020:2025 --max 100
   ```

3. **去重和筛选**
   - 使用文献管理软件去重
   - 根据标题/摘要初筛
   - 获取全文进行复筛

4. **获取开放获取全文**
   ```bash
   # 批量检查可获取性
   for pmid in pmid_list; do
     python3 scripts/pmc_fulltext.py $pmid >> fulltexts.json
   done
   ```

5. **AI辅助预分析** (新增)
   ```bash
   # 批量AI分析提取关键信息
   for txt in fulltexts/*.txt; do
     python3 scripts/ai_assistant.py "$txt" all >> ai_analysis.json
   done
   ```

6. **全文质量评价**
   - 使用fulltext_appraisal.py生成清单
   - 结合AI分析结果作为参考
   - 两位评价者独立评价
   - 解决分歧，计算一致性

7. **数据提取和合成**
   - 提取关键数据
   - 进行Meta分析（如适用）
   - 评估证据质量（GRADE）

### AI辅助最佳实践

1. **适用场景**
   - 快速初筛大量文献
   - 提取结构化信息（PICO、效应量）
   - 生成标准化的质量评价框架
   - 辅助撰写文献总结

2. **使用建议**
   - AI分析作为**辅助工具**，不替代专业判断
   - 对AI提取的关键信息（如样本量、效应量）应**人工核实**
   - 临床推荐需结合**患者具体情况**和**临床专家意见**
   - 建议**双人独立**使用AI工具后交叉验证

3. **质量把控**
   - AI可能遗漏重要信息（如亚组分析、敏感性分析）
   - 注意识别AI的"幻觉"（生成不存在的内容）
   - 复杂研究设计（如适应性设计、贝叶斯设计）需人工深度阅读

4. **效率提升**
   ```bash
   # 结合AI分析和人工评价的工作流程
   python3 scripts/pmc_fulltext.py $PMID > paper.txt
   python3 scripts/ai_assistant.py paper.txt all > ai_review.json
   # 人工阅读 paper.txt 并对比 ai_review.json
   # 发现不一致时以人工阅读为准
   ```

### 注意事项

1. **伦理使用**
   - 遵守各数据库使用条款
   - NCBI API需要设置邮箱
   - 大量检索请使用批量下载

2. **全文版权**
   - 仅获取开放获取或授权全文
   - 尊重出版商版权政策
   - 合理使用教育/研究用途

3. **评价者培训**
   - 批判性评价需要专业知识
   - 建议双人独立评价
   - 使用标准化评价工具

## 扩展资源

- [PubMed语法参考](references/pubmed_syntax.md)
- [研究类型指南](references/study_types.md)
- [评价工具速查](references/appraisal_tools.md)
- [报告规范指南](references/reporting_guidelines.md)

## 更新日志

### v2.1
- ✨ 新增AI辅助文献分析
  - 自动PICO提取
  - 一句话核心发现生成
  - GRADE质量评价
  - 临床适用性建议
- ✨ 新增AI与人工评价结合的最佳实践指南

### v2.0
- ✨ 新增多数据库检索（PubMed + Embase + Cochrane）
- ✨ 新增PMC全文自动获取
- ✨ 新增基于全文的深度评价工具
- ✨ 新增质量评分系统
- 🔧 优化检索性能和错误处理

### v1.0
- 基础PubMed检索
- 基础批判性评价
- 研究类型分类评价