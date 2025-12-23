# 学术/业界在做什么

## AI Agent 助力部门业务运维

### ai_session part00 OS 补丁合入自动化
公司：**深信服**

功能：
* 补丁合入工作流（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_003&hit=/AI+Agent+驱动的自动化流程.*生成最终报告/is)）
    * 自然语言下达任务（拉取指定 Linux 主线节点、与当前内核版本做对比分析）
    * **自动拉取代码 + 分析差异**（commit/patch 细节）+ 生成分析报告
    * **多模型交叉分析 + 人工审核校准**后再继续
    * **自动合并确认的补丁** + 尝试自动解决冲突；失败则标记交人工
    * 生成最终合入报告：成功合入补丁列表、每个补丁结果详情、对应提交链接

* 基层测试自动化（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_004&hit=当前实现：基于+commit+信息自动生成测试用例。)）
    - **用例生产 Agent**
        - **当前实现**：基于 **commit 信息**自动生成测试用例。
        - **未来规划**：增强 Agent 对代码上下文及补丁改动的理解能力，以提供更精准的测试建议。
    - **用例执行 Agent**：自动化执行生成的测试用例。
    - **用例入库 Agent**：对测试用例进行基线管理与归档。

* Vmcore 智能分析（多 Agent + 研判 + 人机协同迭代）（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_004&hit=实践案例二与三：集成测试及+Vmcore+分析)）
    - **堆栈遍历**：自动遍历崩溃时的函数调用堆栈。
    - **寄存器解析**：解析关键寄存器状态，如 RSP（栈指针）、RIP（指令指针）等。
    - **死锁分析**：检测代码栈中可能存在的典型死锁或锁问题。
    - **静态变量分析**：分析全局静态变量的状态。

架构：（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_005&hit=1.%20技术架构)）
- **交互控制层 (Interaction Control Layer)**
  - 集成于基于 **VS Code** 实现的 **`Codelet`** 代码编辑器中，提供便捷的交互界面。

- **智能分析层 (Intelligent Analysis Layer)**
  - 通过 API 调用方式，集成了公司内部部署的**基座大模型平台**。
  - 该方式确保了代码数据不离开内部环境，解决了**代码安全性**的问题。

- **执行引擎层 (Execution Engine Layer)**
  - 负责核心任务的调度与执行，包括 Agent 的调度及 **MCP (Multi-agent Control Plane)** 相关服务。

开发原则：（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_005&hit=原则二：引入监督机制)）
- **原则一：先打通流程，再优化节点**
  - **初期目标**：首要目标是利用 Agent 打通关键节点，实现完整的工作流程。此阶段**允许人工协同介入**，不追求每个节点的完美自动化。
  - **迭代策略**：在完整流程跑通并能展示直观效果后，再针对性地优化关键 Agent 的效率，如提升任务准确率或识别效率。
  - **验收标准**：初期接受 Agent **70%-80% 的成功率**，剩余部分通过人工介入校准。

- **原则二：引入监督机制，逐步减少人工**
  - **引入监督 Agent (Supervisor Agent)**：项目中引入了“监督 Agent”角色，其核心职责是**自动校准“执行 Agent”的产出结果**。
  - **实现方式**：通过综合评估多个模型的结果或采用其他增强策略，对执行结果进行二次加强，从而提升整体自动化水平。
  - **最终目标**：通过监督 Agent 的不断优化，逐步减少人工介入的需求，最终实现更高程度的自动化。

效果（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_003&hit=/实践成果与价值/)）：

内核团队的季度性代码分析与合入工作中取得了显著成效，主要体现在以下方面：

*   **分析准确率**
    *   初期使用单一模型，准确率在 75% 至 93% 之间。
    *   通过综合多个模型进行分析，最终准确率稳定在 **90% 以上**。

*   **效率提升**
    *   **之前**：每次分析与合入工作，开发人员需投入至少一周以上的时间。
    *   **现在**：开发人员的实际投入时间缩短至 **1 到 2 小时**，实现了**数量级**的效率提升。

### ai_session Part 06：AIOps 平台工程化
公司：**凝思软件**

产品：基于 openEuler Intelligence 的调优/诊断 Agent 基座构建智能运维平台（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_003)）

核心能力：（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_003)）
*   **全面监控**
*   **主动预警**
*   **智能分析**
*   **自动化作业**
*   **故障自愈**

架构（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_004)）：
* 数据来源：OS 级**低开销数据采集**（覆盖硬件/OS/JVM/容器/应用/动环系统）
* 抽象三类模型（系统运行/系统行为/资产告警）做实时告警分析，并用 **(RCA)根因分析智能体**深度诊断
* 上层提供“开箱即用运维工具”（基线核查、巡检、智能对话、调优自愈、漏洞扫描与修复）

亮点：
* 支持接入通用大模型和行业大模型（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_004&hit=平台已具备灵活的大模型（LLM）接入能力，目前支持的主流模型包括：)）
    - **电网行业模型**：
        - 国网：光明大模型
        - 南网：大问头模型
    - **通用主流模型**：
        - 阿里通义千问
        - **DeepSeek**
* **双模型协同**：大模型负责与用户交互、意图识别、任务规划；**小模型**做异常检测、趋势检测（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_005&hit=根因分析（RCA）是双模型协同的典型应用场景，其工作流程如下：)）

落地覆盖行业：（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_007&hit=我们的智能运维产品已在多个关键领域得到成功应用。)）
- 能源
- 金融
- 交通
- 电信


### ai_session Part 07：中间件智能体
公司：**东方通**

产品：**中间件智能体** (中间件生命周期的智能化管理)（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=7&sec=sec_005)）

功能（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=7&sec=sec_005&hit=/核心能力：全生命周期智能化/)）：
* 覆盖中间件**全生命周期**：
    * 规划
    * 配置
    * 测试
* **智能规划**：结合业务场景/历史数据/硬件容量生成资源规划与系统配置
* **智能配置**：自动应用配置方案，支持热部署/冷部署；“**自然语言描述需求**，实现从规划到部署的全流程贯通”
* **智能测试**：内置“**智能编码模块**”
    - **自动生成性能/功能测试用例**（例如内存/TPS/CPU）
    - 可生成简单业务场景测试用例
    - 另有测试智能体/运维智能体负责执行与后续维护

架构：（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=7&sec=sec_005&hit=能力中心)）
-   **智能体服务 (Agent Service)**：作为核心协调层，负责承接上层应用的指令，并对底层能力进行调度。该服务能够解析多样化的用户输入（如图形界面操作、自然语言描述、视频等），进行语义识别，并将其转换为具体的任务链，交由能力中心执行。

-   **能力中心 (Capability Center)**：负责执行由智能体服务层下发的任务链，是各项智能化能力的具体实现与执行单元。

-   **模型层 (Model Layer)**：作为 AI 能力的基石，为上层服务提供**垂直领域训练**的智能化模型支持。

效果：
-   **降本增效**
    -   **成本降低**：显著降低开发、运维及资源成本。
    -   **效率提升**：通过 AI 驱动的自动化流程，将系统部署和变更时间从“天级”缩短至**“分钟级”**。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=7&sec=sec_005&hit=效率提升：通过+AI+驱动的自动化流程，将系统部署和变更时间从“天级”缩短至“分钟级”。)）

### ai_session Part 11：DevSecOps 化漏洞运营
公司：**天翼云**
产品：**CTyunOS 智能安全中心**（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=11&sec=sec_002&hit=CTyunOS+智能安全中心是由天翼云操作系统团队开发的一款智能化漏洞全生命周期管理平台。该平台旨在实现对漏洞从感知、播报、分析、修复、测试到公告的全流程智能化跟踪与管理。)）

功能：智能化漏洞全生命周期管理平台（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=11&sec=sec_002&hit=CTyunOS+智能安全中心是由天翼云操作系统团队开发的一款智能化漏洞全生命周期管理平台。该平台旨在实现对漏洞从感知、播报、分析、修复、测试到公告的全流程智能化跟踪与管理。)）
（感知、播报、分析、修复、测试、公告）

流程（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=11&sec=sec_003)）：
1. 漏洞感知

此阶段旨在自动化地发现并筛选漏洞信息。

- **数据源**: 系统从多元化的数据源自动抓取漏洞信息，包括：
  - NVD (National Vulnerability Database)
  - CNVD (China National Vulnerability Database)
  - openEuler 社区
  - Yum 源
- **处理流程**:
  1. 自动抓取原始漏洞数据。
  2. 通过**智能化筛选**，过滤无关信息。
  3. 将有效的漏洞信息推送给相关研发人员。

2. **漏洞分析**

利用 **AI 智能体**对漏洞的实际影响进行分析和定级。

- **分析核心**: AI 智能体
- **分析流程**:
  1. **参考 CVSS 评分**: 针对公开披露的漏洞，系统会获取其 CVSS 评分。
  2. **阈值判断**:
     - **低于阈值**: 若 CVSS 评分低于预设阈值，系统将采纳 AI 的分析结果，判定为“不受影响”，并直接进入公告环节。
     - **高于阈值**: 若 CVSS 评分高于预设阈值，系统将判定为“受影响”，并**自动触发人工审核流程**。此举旨在对高危漏洞采取更为审慎的态度，确保分析的准确性。

3. **漏洞修复**

此阶段的目标是高效、准确地生成并合入修复补丁。

- **初步尝试**:
  - 使用 **`CVE-word` 工具**尝试获取官方或社区提供的修复补丁。
  - 判断补丁是否能够成功合入现有代码库。
- **修复触发**:
  - 当补丁确认可合入并通过**代码门禁（CI/CD）**检查后，系统将**自动触发**漏洞修复流程。
  - **注**: 当前流程由于基础设施尚在完善中，部分环节仍需人工参与，最终目标是实现全自动化修复。
  - **AI 辅助修复**:
  - 系统将安全漏洞的相关信息构建成 AI 智能体，研发人员可在修复过程中直接与其交互，获取修复建议。
  - AI 源码分析的结果也会作为佐证材料，输出到最终的漏洞分析报告中。

4. 测试与公告

在修复完成后，对结果进行验证并通知相关方。

- **测试**: 修复后的版本需通过完整的测试流程，确保补丁的有效性和稳定性。
- **公告**:
  - **官网发布**: 在官方网站上发布安全公告。
  - **邮件通知**: 通过邮件向外部客户通知漏洞修复情况，形成管理闭环。




## 垂类专家 Agent

### ai_session Part 01：医疗 CDSS 智能引擎
公司：**惠每云**

产品：openEuler Intelligence CDSS知识库 / 惠每IntelliCore 智能决策核心
> CDSS 是 Clinical Decision Support System，中文 临床决策支持系统/临床决策辅助系统（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=1&sec=sec_001&hit=Clinical+Decision+Support+System)）

作用：
- openEuler Intelligence CDSS知识库：面向**四级诊疗场景**，帮助医护人员能够高效检索临床知识（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=1&sec=sec_003&hit=该知识库主要面向四级诊疗场景，旨在让临床知识能被医护人员更高效地使用。相较于传统基于Elasticsearch架构的知识库（仅通过分词搜索，返回)）
- 惠每IntelliCore 智能决策核心：应对五、六、七级等更高级的智能决策场景，基于海量的病历信息，当医护人员开立医嘱或进行检查时，系统能根据患者的实时情况进行分析，对可能存在问题的操作进行提醒（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=1&sec=sec_003&hit=此架构主要应对五、六、七级等更高级的智能决策场景。其核心能力是在患者的诊疗全流程中，基于海量的病历信息进行智能决策。这些信息包括：)）

架构（openEuler Intelligence CDSS 知识库）：

* 基座：**GaussDB + openEuler**
* 模块：团队管理 / 资产管理 / **向量化检索（Chunk Search）** / 综合评估
* 检索增强：高频问题加速 + **Reranking**；**父子分块检索**（命中子块时返回父块，尽量保持语义完整性）
* 产品化：CDSS 一体机；应用包括循证问答（强调抑制幻觉、证据链）、文献分析（OCR 解析后提炼）、病例分析（内部数据微调的专用模型）

（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=1&sec=sec_004&hit=openEuler+Intelligence+知识库的核心架构基于高斯数据库（GaussDB）和+openEuler+操作系统构建，主要包含四大模块：)）


自研 IntelliCore 决策引擎：
核心：**Text-to-Rule**（模型生成可执行规则产物）+ **GoRules 通用规则引擎**；另有 Text-to-SQL 支撑报表类需求

GoRules 特性：业务解耦、基于输入/输出模型、内置算子；价值是降本增效与业务扩展性
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=1&sec=sec_005&hit=文本转规则)）

其他：
昇腾社区开源模型/镜像做 Embedding 模型 NPU 加速；探索 **vNPU 切分**做隔离与稳定加速
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=1&sec=sec_003&hit=模型与镜像，实现了Embedding模型的NPU加速。此外，我们也在探索vNPU（虚拟NPU）切分技术，该技术能将一张物理NPU卡虚拟化为多张逻)）

## 大模型训推加速
### ai_session Part 05：CPU+XPU 异构协同（PD 分离）（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_003&hit=调度模块作为用户请求的代理，对推理任务进行+PD+分离处理：)）
公司：**华为**

收益场景：加速大模型推理场景

核心思路：**Decode动态卸载到CPU**，利用**CPU的大内存**增加在线推理的并发量或者离线推理的吞吐量（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_003&hit=Prefill-Decode+Separation)）

具体工作：

改造 **vLLM** 让它支持在 XPU/CPU 上做 **Prefill-Decode 分离**（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_004&hit=优化+vLLM+调度模块：改造+vLLM，使其支持在异构算力（XPU+和+CPU）上实现+Prefill-Decode+分离。)）

做**动态调度**：Decode 按实时负载在 CPU 与 XPU 间分配，并用历史数据训练预测模型做更前瞻的分配（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_004&hit=构建动态调度引擎：设计一个基于实时负载（如计算负载、显存占用）感知的动态调度引擎，以实现最优的任务分配。)）

提升 CPU 执行 Decode 的性能：**NUMA 亲和** / 多线程 / **SIMD 指令级算子优化**（NEON/I8MM）（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_005&hit=NUMA+亲和性)）

在 MoE 上的分工策略：**XPU 做 Attention，CPU 做专家（Expert）计算**（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_005&hit=混合专家模型)）

收益（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_006)）：
- 在线推理并发：Qwen-32B **+12.5%**，Qwen-7B **+8.8%**
- 离线推理吞吐：Qwen-32B **+20.1%**，Qwen-7B **+7.1%**

### ai_session Part 08：通信加速（UMDK/CAM/MIXL）
公司：**华为**
收益场景：大模型推理
产出：**UMDK** 是通信基础底座(实质仓库是工具集) 和 UMDK内的的通信加速库**CAM**。兼容 **DeepEP/Mooncake**、AI 框架“不修改代码即可无缝使用”。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_003)）

UMDK/URMA是什么（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_003)）：
会议：UMDK 是“高性能通信基础底座”，构建于 **URMA“统一内存语义”**之上；UMDK 面向智算提供 CAM

> CAM具体是什么：是Ascend NPU 的 **PyTorch 自定义算子包**被上层（比如 **vLLM/SGLang** 之类的推理框架）集成调用。向下靠 **torch_npu + HCCL + aclnn** 吊起 Ascend 侧实现。
> （开源的 EP + FusedDeepMoE，没有依赖 URMA；另外两个听起来可能依赖 URMA）
> （[来源](https://gitee.com/openeuler/umdk)）

CAM加速的四大子库：（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=大EP通信库：针对MoE（Mixture+of+Experts）场景，提供Prefill和Decode阶段的高性能通信算子。)）
- **大 EP 通信库（MoE）**：Dispatch/Combine 通信开销占比可到 30%；做**向量化地址偏移**、通信时序编排（减少冲突）、负载均衡（哈希散列到端口）、**EPLB + 通算融合**掩盖同步等待
- **FusedDeepMoE**：将 Decode 阶段 MoE 层的 Dispatch/GEMM/Combine 融合为“大算子”，以**细粒度流水并行**实现计算/通信 **overlap**；并提到已接入 SGLang、与 vLLM 合作中
- **M2N（AFD 分离推理）**：NPU 直驱通信、通信融合与编排调度（A2F/F2A 与本地计算融合）、支持节点动态增减且通信域无需销毁重建：
- **MIXL（KV Cache 传输）**：用于 PD 分离推理下跨节点 **KV Cache 传输**；作为“屏蔽底层传输差异、对接上层 AI 框架的中间件层”，提到 KV Cache 传输性能提升 30%；技术点是“**分片消息聚合**”和“**异构多径聚合**”

提到的收益：
KV Cache 传输（MIXL）：在 PD 分离推理架构下，MIXL 作为传输中间件“可将 KV Cache 传输性能提升 **30%**”（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=可将+KV+Cache传输性能提升30%25)）



### ai_session Part 09：软 FP8 全栈调优
公司：**河南昆仑技术有限公司**

收益场景：昇腾 910B/910B3 等**不支持FP8原生计算芯片**的Moe推理（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_001&hit=不支持+FP8+数据类型的原生计算)）

核心思路：基于 **Ascend C** 做 **“软 FP8”** ，通过自研**反量化算子**把 FP8 权重在计算时动态转为 BF16 参与运算（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_002&hit=三、基于昇腾+Ascend+C+的软+FP8+解决方案)）

具体工作：
动态反量化路径：**Vector Core 反量化** FP8 转 BF16，**Cube Core 做 Matmul/GroupedMatmul**，Vector Core 做类型转换
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_003&hit=类型转换)）

MoE 场景：利用专家激活信息（group_list）**只对被激活专家做反量化/计算**
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_003&hit=优化逻辑：算子根据+group_list+动态调度计算任务，仅对被激活专家的权重数据执行反量化和矩阵乘法计算，而完全跳过未激活专家的处理流程，从而显著减少不必要的计算开销。)）

大 Shape：通过调度策略优化带宽/反量化性能，表格给出的指标为显存带宽 +50%~65%、反量化性能 +51%~66%
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_003&hit=|+大+Shape+|+50%25+-+65%25+|+51%25+-+66%25+|)）

特定模型 Shape 亲和：以 Qwen3-32B-FP8 的 down 权重反量化系数行数（300）与 A2 Vector Core 数量对齐来做负载均衡/局部性优化

框架级优化：用 PyTorch meta 入图 + **懒加载下发 (Lazy Loading)**，避免算子逐个下发开销；并做“动态路径调整”
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_002&hit=高效算子下发:+通过PyTorch的+meta+函数实现算子入图，并基于懒加载（Lazy+Loading）方式下发，避免了单个算子依次下发带来的性能开销。)）

收益：
    - 实现 **32% 的端到端推理效率提升**。
        - **GroupedMatmul (`down` 层)**：FP8 吞吐量相较于开源版本平均提升 **40%**。
        - **普通 Matmul (`gate` 和 `up` 层)**：FP8 吞吐量相较于开源版本平均提升 **25%**。
    - 在模型精度几乎无损的前提下，单台设备即可流畅运行完整版 **`DeepSeek V3.1`**。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_002&hit=DeepSeek+V3.1)）
    - 在板卡机型上，可支持的模型参数规模翻倍，从而运行更大规模的模型。
    - 大幅提升并发处理能力，让不同硬件配置的用户都能享受到FP8的技术红利。
    （[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_002&hit=32%25+的端到端推理效率提升)）


### 科教创新 Part 4：学术分享：异构融合的AI Infra系统软件资源管理与可靠性保障
机构：**北京航空航天大学（RAIDS Lab）**
收益场景：异构集群训练混部调度、LLM 推理调度、稳定性/可观测/恢复

背景：
- AI Infra 进入超异构时代，目标形态是构建“云 OS”：向下统一管理异构资源，向上提供统一接口，覆盖离线训练与在线 Serving。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_003)）
- 规模与效能矛盾：截至 2025Q1，全国已建成 165 个智算中心，但平均利用率仅 **10%–15%**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_003)）
- 系统稳定性：规模扩大导致系统失效概率显著增加，且缺乏有效的可观测性手段。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_003)）
- 运维成本：故障发生后存在检测滞后、定位不准、诊断困难及恢复缓慢等问题，导致严重的算力损失。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_003)）

核心思路：系统软件视角下同时做两件事
- **资源管理**：异构算力的高效调度与配置。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_001)）
- **稳定性/可靠性**：异常检测、根因分析与训练恢复链路。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_001)）

具体工作：
- **训练 Colocation（多作业混部调度）**
  - 痛点：性能非对称、成本效益差异、CPU/GPU/NPU 利用失衡。
  - 方法：将执行时间（Execution Time）与异构性共同建模；引入 **Job Grouping** 做组内作业并行交错执行；加入 Deadline 约束；用**图匹配算法**求作业与异构节点的最优映射。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_004&hit=作业组视角（Job+Grouping）：打破单一作业调度的局限，从作业组维度进行资源分配，实现组内作业的并行交错执行。)）
- **LLM 推理调度（PD 分离 + GPU Combo 资源套餐）**
  - 前提：Prefill 计算密集、Decode 访存密集，资源需求非对称。
  - 方法：预定义不同 P/D 配比的 **Combo**；支持在 GPU/NPU 等异构硬件上部署 PD 实例；对不同配比做成本与性能收益量化；提供 **Combo 间/Combo 内两级动态调度**以满足 QoS。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_005&hit=面向+LLM+推理的异构算力调度方案：GPU+Combo+资源套餐)）
- **MoE 推理异构融合（Expert Kit）**
  - 方法：以 Expert 为中心做运行时异构调度，区分 **hot/cold expert**；**CPU/XPU 协同与 Offloading**；并做 Attention 与 Expert 解耦与异构存储布局优化。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_006&hit=Expert+Kit：以+Expert+为中心的异构融合推理系统)）
- **稳定性/可观测/恢复（异常检测 + RCA + 训练恢复）**
  - 目标：及时检测（毫秒级故障感知）；通过全栈可观测性数据做精准定位与诊断；优化失效恢复流程，最大限度减少停机时间。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_003)）
  - 全栈可观测性：软硬件状态的深度追踪与监控，为自动化调度提供数据支撑。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_003)）
  - 闭环链路：从底层监控到运行时恢复的闭环链路；全链路追踪与隔离 + 高效 Checkpoint + **网络层容错（NCCL 深度定制**，通信失效恢复与动态剔除故障节点以维持训练连续性）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=全链路追踪与隔离)）
  - Straggler 与 RCA：定义 5 大类、10 余种失效类型；跨节点采集多维运行指标并聚合分析识别掉队者；引入**图学习**与 **RAG**（结合历史故障知识库）辅助生成根因解释与修复建议。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=失效类型)）
- **可靠性补充（推荐模型训练的 Checkpoint 与 Failover）**
  - Checkpoint：Embedding 冷热特征分离 + 差异化持久化；**Pipeline 化编排**实现计算与 IO 并行。
  - Failover：**Device Proxy + Flexible CCL**，通过动态链路重构与通信路径重映射降低恢复成本。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_008&hit=Device+Proxy：引入设备代理机制，解耦物理设备与逻辑训练单元。)）
- **平台化系统：Crater（多租户异构集群智能调度）**
  - 能力：异构算力统一管理、多租户资源隔离、多维数据管理，覆盖训练到分布式推理（含 **DeepSeek** 分布式推理）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_009&hit=Crater：多租户异构集群智能调度系统)）

收益：
- 训练混部：作业完成率提升 **44.7%**，JCT（作业周转时间）缩短近 **2 倍**（快手千卡集群验证）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_004&hit=|+作业完成率+|+提升+44.7%25+|)）
- LLM 推理调度：整体推理性能提升 **25%–38%**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_005&hit=初步实验数据表明，采用+GPU+Combo+异构调度方案后，系统整体推理性能提升了+25%25+-+38%25。该方案证明了通过精确的资源配比与异构算力协同，可以显著优化+LLM+推理的成本效率比。)）
- 稳定性诊断：集成到快手 AI 平台后，诊断耗时从约 30 分钟缩短到**分钟级**（数十倍效率提升）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=/诊断耗时.*分钟级/)）
- Crater：上线运行超过 1 年，累计处理任务数超过 20,000。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_009&hit=任务规模：累计处理并执行任务数已突破+20,000+个。)）


## 非大模型训推加速&训推基建优化
### ai_session Part 10：CPU 推理图编译器（ANNC）
公司：**华为**
收益场景：搜推/广告等 CPU 推理（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_001)）

产出：**ANNC**（XLA-based Deep Learning **Graph Compiler**），面向 **CPU 推理**；上接 TensorFlow / PyTorch，下亲和鲲鹏 CPU。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_003)）

核心思路：用**编译技术**把图优化/算子生成“自动化”，减少运行时 Repack/调度/访存开销。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_003)）

具体工作：
- 框架层：**图算融合**（算法等价融合小算子）
- 编译前端：冗余算子消除、CPU 感知图优化、多内核搜索策略
- 编译后端：**自动生成高性能算子**、指令级优化、对接开源算子库
- MatMul 数据布局：编译期静态打包权重 + **最优布局传递**，**消除运行时 Repack**（开源推荐模型吞吐 +5%）
- 算子快速生成：硬件感知（Cache Line/指令集）+ **MLIR**（Tiling/Packing/Buffer 复用）+ **模板化生成**（对比 OpenBLAS +9%–123%）
- 客户案例（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_004)）：
  - 广告推荐 Embedding（占比 30%–40%）：Profiling、识别 Pattern、**TensorFlow 图重写**、融合算子 + 手写 kernel（推理 +5%）
  - MatMul + BiasAdd + BatchNorm **常量折叠**：数学等价变换 + 轻量 TF 改造（时延 -10%）

收益（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_003)）：
- 多个开源推荐模型：性能 **+20%**
- 某客户推荐模型：性能 **+25%**

开源与后续：
- ANNC 已在 openEuler 社区开源；计划开源更多优化 Pass，并探索结合 **Triton** 增强算子生成（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_006)）

### ai_session Part 03：AI 存储调优（MLPerf Storage）
公司：**Linaro**

收益场景：训练数据加载/存储（目标 GPU 利用率 >90%）（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_001)）

对象：**JuiceFS**（JuiceData 开源分布式文件系统）+ openEuler 24.03 LTS SP2（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_001)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_002)）
核心思路：用 **MLPerf Storage v2.0** 聚焦 **“训练数据加载路径”** （用 sleep 模拟训练计算），沿 I/O 路径定位瓶颈，再从并发、Direct IO、NUMA/内存带宽入手调优。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_001&hit=计算模拟)）

具体工作（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_002)）：
- 数据集：> 可用内存 5 倍（排除 Page Cache 影响）；JuiceFS 数据预热到本地缓存
- UNet3D：
  - 5 GPU 最佳：GPU 利用率 **98%**，I/O 14.8 GB/s；`reader.read_threads` 由 4 调整为 16，`reader.odirect=True` (**Direct I/O**)
  - 6 GPU：GPU 利用率 83%，带宽顶在 15.1 GB/s；FIO 也测到 15.1 GB/s（瓶颈在 JuiceFS 吞吐）
  - 绑核：Memory Bound（大量**内存拷贝** `runtime.memove`、`arch_copy_to_user` + LLC miss）
  - 不绑核：>80% **remote NUMA 访问**导致带宽/时延受限
- ResNet50：
  - 50 GPU 最佳：GPU 利用率 **95%**，I/O 9.2 GB/s；`reader.read_threads` 由 8 调整为 1（batch ~58.5 MiB）
  - 55 GPU：GPU 利用率 86%，I/O 仍 9.2 GB/s（瓶颈在后端带宽）
  - “9.2 < 15.1”的解释：Buffer IO 与系统内存拷贝带宽竞争；用 `stream` 验证 JuiceFS 吞吐与 memcpy 带宽强相关

结论（调优要点）（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_003)）：
- 能撑多少 GPU，本质取决于总吞吐带宽上限
- **内存拷贝** + **NUMA 访问模式**会直接卡住 I/O 吞吐
- Go runtime 缺少 NUMA 感知：多 NUMA/多 Socket 尽量**避免跨 NUMA 内存访问**

### 科教创新 Part 2：推荐大模型参数存储系统
机构：**中国人民大学**
研究定位：面向人工智能的存储（Storage for AI）中，“参数存储（Parameter Storage）”方向
收益场景：推荐模型 Embedding/稀疏参数的存储与访问瓶颈缓解（训/推）

背景（容量墙 + 带宽墙）：
- 推荐模型的核心是巨大的 Embedding 层：高维稀疏 ID 需要通过 Embedding 查询转成低维稠密向量，整体以访存为主。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_002)）
- **容量墙（Capacity Wall）**：Embedding 参数规模可达到万亿级（例如 12 万亿），存储容量需求持续增长。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_002)）
- **带宽墙（Bandwidth Wall）**：Embedding 查询涉及稀疏、随机访存；讲者提到 Embedding 查询耗时占端到端时间 **70% 以上**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_002)）
- 叠加效应：双重制约导致硬件成本高昂（以快手为例，上万台参数存储服务器、十亿元级硬件成本）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_002)）

核心思路：
- 利用**分层存储**硬件突破容量/带宽瓶颈：HBM 作为性能层缓存缓解带宽墙；持久性内存（PM）作为容量层扩容打破容量墙。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_002)）
- 方向上强调算法、系统、硬件协同设计。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_003)）

代表性工作（按算法/系统/硬件/介质层）：
- 算法层：**OptEmbed**（OSDI 2022）（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_003&hit=算法层实践：面向异构内存的参数放置算法)）
  - 传统缓存替换（如 LRU）仅按访问频率/近期性淘汰，忽略参数对模型精度的重要性。
  - OptEmbed 同时评估访问频率与参数重要性，为参数计算综合分数 `Score = f(访问频率, 参数重要性)`，优先淘汰综合分数最低的参数；在保证模型精度前提下提升缓存命中率。
- 系统层：**Fluid**（SC 2022）（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_004&hit=系统层优化：分层式参数存储系统+Fluid)）
  - **分层存储**：热点参数存 **HBM**，温点参数存 **DRAM**，冷点参数存 **SSD**。
  - 关键功能：**动态迁移**；快照与恢复。
  - 收益：系统吞吐量提升超过 **2 倍**；系统成本降低超过 **50%**。
- 硬件层：**Smart-Prefetcher**（MICRO 2022）（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_004&hit=Smart-Prefetcher)）
  - 利用推荐模型参数访问的局部性，将可能被访问的相关参数**预取到缓存**中，以提升缓存命中率；并指出传统硬件预取方法无法直接适用于推荐模型独特的参数访问模式，需要针对性设计。
- PM 层：**PetPS**（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_005&hit=PetPS：面向持久性内存的解决方案)）
  - 利用网卡（NIC）的 **DMA 引擎卸载（Offload）** 参数聚集（Gather）操作，规避持久性内存高延迟特性带来的 CPU 高昂访存开销；同时解决一致性问题。
- SSD 层：**MaxEmbed**（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_006&hit=针对上述问题，我们设计并提出了+MaxEmbed+方法。其核心机制与目标如下：)）
  - 选择性地为高频访问的“热点”参数**创建副本**，以捕获数据中多种复杂共现关系；从根本上缓解 SSD 层读放大问题，提升有效带宽。
- 框架与业界影响：**RecStore**（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_007&hit=解决方案：RecStore+稀疏参数存储系统)）
  - 智能感知与预测推荐模型稀疏特征的访问模式，提供高效的参数预取与缓存管理；其核心设计已被多家业界领先公司采纳并应用于核心推荐业务。

未来展望：
- 生成式推荐大模型成为趋势，对底层参数服务与存储系统提出新的挑战。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_008&hit=未来展望：生成式推荐大模型)）

## 万卡集群建设
### day1_main Part 07：百度超万卡智算集群
公司：**百度**
整体方案：面向超万卡集群的混合云升级“全生命周期一站式方案”，底座 OS 是 BaiduLinux CloudOS
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=day1_main&part=7&sec=sec_002&hit=本方案提供覆盖建设与使用全生命周期的全栈产品与服务体系，具体包括：)）

架构革新：
Scale-out：跨园区 **RDMA** 长传，最远 **150 公里** 无损；大模型训练跨园区损耗 <3%；组网支持 10 万卡规模。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=day1_main&part=7&sec=sec_003&hit=支持最远+150公里+的无损传输。)）
Scale-up：提出“**超节点（SuperNode）**”+ 自研 **XPU-Link**；OS 侧与 openEuler/CloudOS 协作做统一内存视图、异构调度、**数据零拷贝**（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=day1_main&part=7&sec=sec_003&hit=百度实践：基于开放兼容的理念，我们推出了自研的+XPU-Link+互联通信协议。)）


效能与运维：强调“全链路协同优化 + 一站式智能运维”。
云原生调度：毫秒级响应、分钟级调度上百任务；CloudOS 异构协同+可编程缓存使“单机推理性能提升一倍以上”（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=day1_main&part=7&sec=sec_004&hit=推理性能：单机推理性能提升一倍以上。)）
与 openEuler 共建一站式运维平台：自动定位 **>95% 慢节点**（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=day1_main&part=7&sec=sec_004&hit=慢节点定位：平台能够自动定位超过+95%25+的慢节点问题。)）

安全：异构机密计算（CloudOS + openEuler 深度融合）；机密 VM 免改代码迁移；“**机密直通 (Confidential Passthrough)**”让机密 VM 可直通 GPU。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=day1_main&part=7&sec=sec_005&hit=创新性地采用机密直通技术（Confidential+Passthrough）。)）

openEuler 合作与后续：自 2021 深度合作；BaiduLinux 部署超 20,000 套，支撑“千帆大模型平台/百舸异构计算平台”；后续共建 **Arm CCA 机密计算**、异构融合软件标准、超节点原生 OS 等。
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=day1_main&part=7&sec=sec_007&hit=目标：联合社区发布业内首个基于+Arm+CCA（Confidential+Compute+Architecture）的机密计算解决方案。)）

## OS安全
机构：**北京大学**

产物：端到端系统 **SysArmor**（面向海量底层日志，自动生成 APT 攻击报告）（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_008&hit=SysArmor+旨在实现端到端的攻击模拟与分析，其核心能力包括：)）

背景挑战：

数据：企业日志难公开、标注极贵；攻击/正常极端不均衡，可能到 **1:10,000,000**

语义：底层日志与自然语言有鸿沟、行为强依赖上下文；攻击周期长导致日志维度超大（上下文窗口百万 token 也可能只覆盖“半天”）

成本：安全行业算力投入有限，但要求“及时”处理海量数据
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_003&hit=在真实环境中，攻击数据相对于正常数据的比例极其悬殊，可能达到+1:10,000,000+的级别。)）

核心方法：
* 采集 OS 底层日志（进程/文件/网络端口等）
* 构建**溯源数据流动图（Provenance Graph）**
* 在图上进行**无监督异常挖掘**
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_004&hit=Provenance+Graph)）

三项关键技术：
1. **无监督快速日志过滤**（先“淘汰大头”，再上强模型）
两阶段：**快速过滤** + **深度分析**
关键洞察：统计异常性 + 拓扑聚合性；在线搜索算法基于 **Steiner Tree**，把复杂度从 O(N²) 降到 O(N)，并保持竞争比。
数据工程：热/冷分离缓存（可疑事件进内存，其他下沉磁盘）
效果：误报节点数 **“降低两个数量级”** ；与深信服合作在真实环境发现 7 个真实攻击事件
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_005&hit=斯坦纳树（Steiner+Tree）模型)）

2. **基于 LLM 的攻击检测与日志理解**（把“图”变成“报告”）
提出 **`gIoC` 中间表述**，让 LLM 更容易把底层事件泛化/对齐到威胁情报知识。
用“**攻击步骤逻辑推理**”校验 LLM 初标注，降低误报。
Pipeline（处理链路）：
* 小模型：从“千万级事件”筛到“几十个核心事件”
* LLM：对核心事件做结构化描述
* 安全 Agent：生成报告
效果：在华为 openEuler 运维数据测试，误报率降低 **“一个数量级”** 
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_006&hit=gIoC+在形式上贴近底层事件的结构。)）

3. **低开销日志采集系统**（可观测但别把系统拖死）
软件：**分片式隔离架构**（每进程独立处理日志，避免集中采集器破坏隔离）
硬件：**DPU 卸载监控负载** + 优化数据拉取路径。
效果：即便采集“每一个系统调用”，整体开销仍 **<3%**；对比 sysdig/Linux audit 开销 **“降低一个数量级”** 
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_007&hit=卸载监控负载：利用+DPU+强大的处理能力来执行监控任务，从而减少主+CPU+的负担。)）

原型与开源：

SysArmor 原型集成上述能力，支持自然语言问答式分析；已在华为 openEuler 社区开源，另提到 Gitee/openEuler 双处开源与计划公开数据集（隐私保护前提下）
部分成果获“中国电子学会科技进步一等奖”
（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_009&hit=项目开源：SysArmor+系统已在+Gitee+和+openEuler+社区开源。)）


# 可能会比较感兴趣的技术或者亮点

## AI OS 诊断调优

### 模型形态（LLM/小模型/混合）

#### 1) **LLM 驱动的工作流/智能体**（补丁合入/测试/Vmcore）
- 工作内容
  * LLM 负责解析自然语言、任务编排、生成执行计划；下游多个专用 Agent 执行补丁分析/合入、用例生成/执行/入库、Vmcore 分析等；关键节点由**人工审核确认**后继续推进。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_003)）
- 适用范围
  * OS 维护长链路任务（补丁合入、集成测试、Vmcore 分析）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_002)）
- 收益
  * 分析耗时：仅分析阶段，每千条补丁需要投入 80–100 小时以上（约两周工作量）。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_002&hit=分析耗时：仅分析阶段，每千条补丁就需要一位资深工程师投入80至100小时以上（约两周工作量）。)）
  * 合入冲突：超过 **10%** 的补丁在合入时会产生代码冲突，需要人工介入分析和解决。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_002&hit=代码冲突：超过10%25的补丁在合入时会产生代码冲突，需要人工介入分析和解决。)）
  * SLA：需承诺在 14 天内完成中高危漏洞的修复并推送给客户。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_002&hit=服务等级协议（SLA）压力：需承诺在14天内完成中高危漏洞的修复并推送给客户。)）
  * 准确率：通过综合多个模型进行分析，最终准确率稳定在 **90% 以上**。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_003&hit=通过综合多个模型进行分析，最终准确率稳定在+90%25+以上。)）
  * 人工投入：开发人员的实际投入时间缩短至 **1–2 小时**。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_003&hit=现在：开发人员的实际投入时间缩短至+1+到+2+小时，实现了数量级的效率提升。)）

#### 2) **大模型 + 专精小模型**（AIOps 双模型协同）
- 工作内容
  * 数据观测与采集
    * 基于成熟的操作系统级监控解决方案，实现全面、**低开销的数据采集**；强调数据准确、低性能开销。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_004)）
    * 监控范围覆盖硬件、操作系统、JVM 容器、应用程序及动环系统；数据维度覆盖系统、服务、进程、分区、网络等系统级与应用级数据。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_004)）
  * 数据模型化与实时分析
    * 将底层数据抽象为系统运行模型、系统行为模型、资产告警模型；基于模型与原始数据进行实时告警分析（系统告警、行为告警、智能告警），并利用 **RCA 智能体**进行深度诊断。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_004)）
  * 双模型协同与诊断流程
    * **专精小模型**（US-AD/LSTM/贝叶斯等，基于成熟机器学习算法训练）承担异常检测、趋势预测等高频任务；当小模型监控机器指标触发预警后，由大模型介入并启动 RCA 智能体。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_005)）
    * RCA 智能体通过与用户交互确认现象，组织子任务完成日志分析、指标关联、拓扑追踪，并输出包含根本原因与优化建议的分析报告。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_005)）
  * 上层运维工具与平台能力
    * 提供基线核查、系统巡检、智能对话、调优自愈、漏洞扫描与修复等开箱即用运维工具。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_004)）
    * 平台具备大模型接入能力（电网行业模型与通用主流模型等）；高可用网络架构采用多区域部署、负载均衡、冗余链路，保障监控数据稳定采集与控制指令可靠下发。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_004)）
    * 技术栈层面，明确提到 **eBPF** 用于底层数据观测与采集，并结合 **RAG** 与大小模型协同提升分析准确性与深度，目标是形成“感知-决策-优化”的自治闭环。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_008)）
- 收益
  * 未给量化指标（强调“低开销采集 + 双模型协同 + RCA 智能体 + 开箱即用运维工具”）。

#### 3) **大模型用于漏洞影响分析**（DevSecOps）
- 工作内容
  * 将 CVE 相关信息结构化，交给大模型（当前 **DeepSeek-R1**）做影响分析/评分；基于 CVSS 阈值分级分流（低危可快速判定“不受影响”，**高危触发人工审核**）；再跟踪修复/测试/公告。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=11&sec=sec_003)）
- 收益
  * 未给整体量化指标；提到“基于 openEuler 上游的漏洞，分析结果准确率较高”。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=11&sec=sec_005)）

#### 4) **小模型/无监督先缩量 + LLM/Agent 再解释**（跨领域：复杂攻击检测，可迁移到运维诊断输入处理）
- 工作内容
  * **两阶段过滤**（先快速过滤再深度分析）；**`gIoC` 中间表述**让 LLM 理解底层日志并泛化；引入**攻击逻辑推理**剔除误报；安全 Agent 生成自然语言报告；并通过 **DPU 卸载**等手段把“详尽采集”开销压低。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_005)）
- 收益
  * 攻击/正常可到 1:10,000,000；O(N²) 降到 O(N)；误报节点降低**两个数量级**；详尽采集模式整体开销 **<3%**，对 sysdig/audit 降一个数量级。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_006)）

### 训练/微调与材料来源

#### 1) **RAG 资产库**（用于调优/诊断知识注入）
- 资料来源与范围
  * 规划构建 RAG 资产库，涵盖 OS 运维与技术资产、数据库、鲲鹏计算平台、中间件（MQ/Redis/JDK）等。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=2&sec=sec_004)）

#### 2) **微调/蒸馏**（用于领域化与降本）
- 微调/蒸馏情况
  * 明确包含 **Fine-tuning** 与 **Distillation**；蒸馏目标是把通用大模型约 **80%–90%** 的能力迁移到小模型以显著降低成本。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=2&sec=sec_003)）

#### 3) **小模型训练**（AIOps）
- 训练情况
  * 专精小模型（US-AD/LSTM/贝叶斯等）“基于**成熟机器学习算法训练**”，用于异常检测/趋势预测等。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_005)）

#### 4) **训练数据稀缺下的输入处理/表述方式**（APT攻击检测）
- 数据分布现状
  * 攻击数据分布极端不均衡（可达 1:10,000,000）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_003)）
- 输入处理方式
  * 两阶段过滤先缩量再深度分析；用 **`gIoC` 中间表述**把底层事件“结构化+泛化”后再给 LLM。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_006)）

### Agent 设计

#### 避免误诊的机制
- **多模型交叉 + 监督型 agent 校准**
  * 补丁合入流程里明确“可调用多个不同的大模型 Agent 进行交叉分析”，并引入**监督 Agent** 自动校准执行 Agent 产出。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_003&hit=行校准和评估。为提高准确性，系统可调用多个不同的大模型+Agent+进行交叉分析。人工确认后，将结果反馈给系统。)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_005&hit=原则二：引入监督机制)）
- **分级分流 + 人工兜底**
  * 漏洞分析按 **CVSS 阈值分流**，高于阈值触发人工审核。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=11&sec=sec_003&hit=参考+CVSS+评分:+针对公开披露的漏洞，系统会获取其+CVSS+评分。)）
- 基于判定难度<生成难度的原理，用确定性的传统算法剪枝错误结论
  * 构建基于攻击技术逻辑关系的推理引擎：
    - 因果校验：利用攻击阶段的先后顺序（例如：必须先“获取权限”才能执行“安装病毒”）进行逻辑验证。
    - 节点标注：在图结构节点上自动标注对应的攻击技术（ATT&CK TTPs）和手法。
    - 误报消除：通过逻辑不一致性识别并剔除不符合攻击链路规律的孤立事件。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_006&hit=分层处理流程)）

#### 人工确认要求
- 补丁合入
  * AI 生成分析报告，**人工审核确认**后再自动合并与冲突处理。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_003&hit=人工审核与确认：由于+AI+分析无法保证+100%25+的准确性，此环节至关重要。开发人员需对分析报告进行校准和评估。为提高准确性，系统可调用多个不)）
- 高危漏洞
  * CVSS 高于阈值触发人工审核流程。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=11&sec=sec_003&hit=高于阈值:+若+CVSS+评分高于预设阈值，系统将判定为“受影响”，并自动触发人工审核流程。此举旨在对高危漏洞采取更为审慎的态度，确保分析的准确性。)）
- 中间件配置/部署
  * 智能体生成配置方案，用户确认后再应用到中间件。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=7&sec=sec_006&hit=方案生成与应用：智能体生成相应的配置方案，用户确认后即可将其应用到中间件上，完成最终配置。)）


### 避免幻觉的手段
- **RAG**
  * 调优方案里明确把 **RAG** 用作“解决幻觉、提升准确性”的手段（同时也指出其对复杂跨域推理有局限）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=2&sec=sec_003&hit=目的：解决大模型的幻觉问题，提升回答的准确性。)）
- **`gIoC` 中间表述**
  * 用**结构化+泛化的中间表示**弥合底层日志与自然语言之间的语义鸿沟，避免靠硬匹配。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_006&hit=gIoC+在形式上贴近底层事件的结构。)）

### 降本手段（含大小模型协同）
- **蒸馏降本**
  * 将通用大模型约 80%–90% 能力迁移到小模型，目标“显著降低成本”。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=2&sec=sec_003&hit=模型蒸馏)）
- **大小模型协同**
  * 小模型承担异常检测/趋势预测等高频任务，大模型负责交互与规划（未给量化）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=6&sec=sec_005&hit=根因分析（RCA）是双模型协同的典型应用场景，其工作流程如下：)）
- **两阶段过滤**
  * 先快速过滤再深度分析，显著节省计算资源。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_005&hit=为应对海量数据的算力开销，我们提出了一种两阶段过滤策略：)）

### 指标与成果（按 part 汇总）
- ai_session Part 00（补丁合入/维护自动化）
  * 每千条补丁分析 80–100h+；>10% 冲突；14 天内修复中高危；准确率稳定 90%+；**人工投入缩短到 1–2 小时**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_002&hit=分析耗时：仅分析阶段，每千条补丁就需要一位资深工程师投入80至100小时以上（约两周工作量）。)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=0&sec=sec_003&hit=现在：开发人员的实际投入时间缩短至+1+到+2+小时，实现了数量级的效率提升。)）
- ai_session Part 07（中间件智能体）
  * 部署/变更从天级缩短到**分钟级**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=7&sec=sec_005&hit=效率提升：通过+AI+驱动的自动化流程，将系统部署和变更时间从“天级”缩短至“分钟级”。)）
- ai_session Part 02（LLM 调优）
  * 信创环境参数规模 >13,000；案例“性能提升约 13.6%”（提示硬件不完全对等，仅供参考）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=2&sec=sec_004&hit=效果：性能提升约+13.6%25，效果主要由若干关键参数贡献。)）
- ScienceEducationInnovation Part 03（复杂攻击检测）
  * 攻击/正常 1:10,000,000；O(N²) 降到 O(N)；**误报节点降低两个数量级**；详尽采集模式**开销 <3%**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_003&hit=在真实环境中，攻击数据相对于正常数据的比例极其悬殊，可能达到+1:10,000,000+的级别。)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_005&hit=斯坦纳树（Steiner+Tree）模型)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=3&sec=sec_007&hit=卸载监控负载：利用+DPU+强大的处理能力来执行监控任务，从而减少主+CPU+的负担。)）
- ai_session Part 06 / Part 11
  * 材料未给整体量化指标，主要描述能力边界与研发规划。


#### 2) **OS 底座的全栈观测与协同分析能力**（集群级运维监控手段）
- 工作内容
  * 在 BaiduLinux 智能原生底座操作系统中，集成 openEuler 的全栈观测与协同分析能力，为复杂智算集群提供运维监控手段。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=day1_main&part=7&sec=sec_006&hit=集成了+openEuler+的全栈观测与协同分析能力，为复杂的智算集群提供了高效的运维监控手段。)）
- 收益
  * 未给量化指标，强调“**全栈可观测性**”能力与运维效率提升。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=day1_main&part=7&sec=sec_006&hit=集成了+openEuler+的全栈观测与协同分析能力，为复杂的智算集群提供了高效的运维监控手段。)）

## 训练/推理任务效能与稳定性观测（Straggler/RCA/恢复）

#### 1) **训推场景的 Straggler 检测与智能化 RCA**（图学习 + RAG）

- 背景与目标
  * 在大规模 AI 模型训练过程中，系统失效（Failure）具有**高频发性**与**极高恢复成本**；目标是降低故障对算力资源的损耗，实现快速检测与自动化恢复。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=系统失效（Failure）具有)）
  * 面向分布式训练与推理中常见的 Straggler（掉队者）问题。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=针对分布式训练与推理中常见的+Straggler+问题)）

- Straggler 检测（识别“进度显著滞后”的节点）
  * 数据采集：跨节点收集多维度的运行指标。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=数据采集：跨节点收集多维度的运行指标。)）
  * 聚合分析：通过数据聚合与统计学手段，识别执行进度显著滞后的节点。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=聚合分析：通过数据聚合与统计学手段，识别执行进度显著滞后的节点。)）
  * 失效类型定义：AI 环境下特有的 **5 大类、10 余种**失效类型，用于精准治理的标准分类。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=系统定义了+AI+环境下特有的+5+大类、10+余种失效类型)）

- 智能化 RCA（根因解释与修复建议）
  * **图学习（Graph Learning）**：建模节点间依赖关系，追踪异常传播路径。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=图学习)）
  * **RAG（检索增强生成）**：结合历史故障知识库，辅助生成根因解释与修复建议。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=RAG)）

- 闭环链路（从“定位”走到“隔离/恢复”）
  * **全链路追踪与隔离**：实时监控系统状态，实现故障节点的快速定位与物理隔离。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=全链路追踪与隔离：实时监控系统状态，实现故障节点的快速定位与物理隔离。)）
  * **高效 Checkpoint 机制**：优化读写性能，缩短状态保存与加载的耗时。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=高效+Checkpoint+机制：优化读写性能，缩短状态保存与加载的耗时。)）
  * **网络层容错（NCCL 深度定制）**：通信失效后的及时恢复，并支持动态剔除故障节点以维持训练连续性。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=网络层容错（NCCL+优化）：针对分布式通信库+NCCL+进行深度定制，实现通信失效后的及时恢复，并支持动态剔除故障节点以维持训练连续性。)）

- 落地与收益
  * 集成到**快手 AI 平台**后，诊断耗时从约 **30 分钟**缩短到**分钟级**（数十倍效率提升）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_007&hit=/诊断耗时.*分钟级/)）

- 材料未披露的细节
  * “多维运行指标”具体维度、采集方式与阈值/统计判定准则。
  * “5 大类、10 余种”失效类型的明细列表与对应处置策略。
  * 图学习的图构建方式、训练数据来源与在线推理形态；历史故障知识库（RAG）的构建、更新与评估方式。

## 大模型训推优化（优化可以是提速、提升性能、降低成本等）

### 基架优化(OS调优、存储通讯优化)

#### 1) **通信：UMDK/URMA + CAM**（昇腾亲和通信底座 + 计算通信深度融合）
- 背景与问题
  * Token-per-Token 时延诉求从约 50ms 下探到 10ms 级，前沿要求 <5ms。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_002&hit=原有标准:+典型Token-per-Token时延约为50ms。)）
  * MoE 通信开销上升，`Dispatch/Combine` 通信耗时占比可达 30%。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004)）
  * 通信范式从集合通信演进到 P2P / M2N。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_002)）
- 工作内容
  * **UMDK** 基于 **URMA“统一内存语义”**，提供超异构通信加速库 **CAM**；强调低延迟通信、**计算通信并行（Overlap）**；兼容 **DeepEP/Mooncake** 等接口，AI 框架无需改代码即可集成。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_003)）
- CAM 四大子库
  * **大EP 通信库**（MoE Prefill/Decode 通信算子）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004)）
  * 通算融合加速库 **FusedDeepMoE**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004)）
  * **M2N 通信加速库**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004)）
  * KV Cache 传输加速库 **MIXL**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=MIXL：KV+Cache传输加速库)）
- 收益
  * 给出瓶颈与具体优化点（如向量化数据准备、通信时序编排、**EPLB 负载均衡**、**通算融合**等），但未给统一端到端加速数字；提到已接入 SGLang，正与 vLLM 合作。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004)）

#### 2) **存储：MLPerf Storage + JuiceFS 调优**（以数据加载路径为主）
- 背景与问题
  * **MLPerf Storage** 用 `sleep` 模拟训练计算，聚焦“训练数据加载路径”，辅助目标是让 **GPU 利用率达到 90%+**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_001&hit=计算模拟:+数据加载完成后，通过+sleep+操作模拟实际的计算过程。)）
- 工作内容
  * 沿 I/O 路径定位瓶颈并调参：并发读线程、**Direct I/O**、**NUMA/内存带宽**等；结合 FIO/系统工具把瓶颈归因到 JuiceFS 极限带宽、内存拷贝、NUMA remote 访问等。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_002)）
- 收益
  * UNet3D（5 GPU）GPU 利用率 **98%**、带宽 14.8 GB/s；规模增大后分别暴露 JuiceFS 吞吐、内存拷贝、NUMA 访问等瓶颈。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_002&hit=I/O+带宽:+14.8+GB/s)）

#### 3) **参数存储：Embedding“容量墙/带宽墙” + 分层参数存储系统 Fluid**（推荐大模型）
- 背景与问题
  * Embedding 参数可达万亿级带来容量墙；Embedding 查询稀疏随机访存导致带宽墙（查询耗时可占端到端 70%+）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_002)）
- 工作内容
  * 算法-系统-硬件协同；Fluid 采用 **HBM/DRAM/SSD 分层** + 动态迁移 + 快照/恢复。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_003)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_004&hit=系统层优化：分层式参数存储系统+Fluid)）
- 收益
  * Fluid 吞吐 **>2x**、成本降低 **>50%**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=2&sec=sec_004&hit=系统层优化：分层式参数存储系统+Fluid)）

### 训练优化
- 补充说明
  * CAM 明确面向训练与推理通信场景。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004)）
  * MLPerf Storage 任务包含训练数据加载与 checkpointing 形态，但本次调优重点聚焦读取路径瓶颈。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=3&sec=sec_001)）

### 推理优化

#### 1) **基于实时负载/显存占用的动态调度**（CPU+XPU 异构推理）
- 背景与问题
  * 目标是在大模型推理服务中，平衡“服务方追求高并发（资源利用率）”与“用户追求低时延（交互体验）”的矛盾。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_004)）
  * 传统“XPU 中心化推理”下，**XPU 显存容量**成为关键瓶颈，直接限制上下文长度与并发；同时 CPU 侧资源被闲置。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_002)）

- 动态调度引擎：用“实时负载/显存占用”做决策
  * 负载感知：设计基于实时负载（如**计算负载、显存占用**）感知的动态调度引擎，以实现更优的任务分配。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_004&hit=基于实时负载（如计算负载、显存占用）感知的动态调度引擎)）
  * 基础策略（实时吞吐量驱动）：
    - 数据收集：实时监测并收集 CPU 与 XPU 上每个 batch 的吞吐量数据。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_004&hit=实时监测并收集+CPU+和+XPU+上每个批次（batch）的吞吐量数据)）
    - 调度决策：新的 Decode 请求到达时，分配给当前吞吐量更高的设备。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_004)）
    - 局限性：当两个 Decode 请求到达间隔极短时，调度器可能来不及感知负载变化而做出次优决策。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_004&hit=调度器可能因来不及感知前一个任务带来的负载变化而做出次优决策)）
  * 增强调度（基于历史数据预测）：
    - 历史数据：持续记录历史调度信息（调度时的设备负载与最终吞吐量）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_004&hit=持续记录历史调度信息)）
    - 预测模型：利用历史数据训练预测模型，预测把 Decode 分配到特定设备后的吞吐变化；据此做更前瞻的动态分配。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_004)）

- 协同侧配套（让 CPU 执行 Decode 更“划算”）
  * CPU 侧通算推理加速关键技术：**NUMA 亲和**、**多线程并行**、**SIMD 指令级算子优化（NEON/I8MM）**；并给出 Dense/MoE 两类场景下的执行策略差异。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_005)）

- 收益
  * 实时在线推理：Qwen-32B 并发 **+12.5%**，Qwen-7B 并发 **+8.8%**。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_006)）
  * 非实时离线批量推理：Qwen-32B 吞吐 **+20.1%**，Qwen-7B 吞吐 **+7.1%**。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=5&sec=sec_006)）

#### 2) **MoE 推理异构融合：以 Expert 为中心的运行时调度与 Offloading（Expert Kit）**
- 背景与问题
  * MoE 模型参数量巨大，传统单一硬件部署难以平衡成本与性能，资源受限或算力需求极端时问题更突出。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_006)）
- 核心设计（以 Expert 为核心单元）
  * **冷热感知**：利用不同 Expert 激活频率差异，动态识别高频与低频专家模块。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_006&hit=冷热感知)）
  * **CPU/XPU 协同 + Offloading**：在运行时实现 CPU 与 XPU 之间的计算协同与权重卸载，确保核心算力聚焦于热点 Expert。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_006&hit=CPU/XPU)）
- 解耦与存储布局优化
  * **Attention 与 Expert 解耦**：允许对不同类型计算任务独立配置存储与计算资源。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_006&hit=Attention)）
  * **异构存储管理**：优化分布式环境下的异构存储布局，提升跨节点/跨硬件的数据读取与交换效率。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_006&hit=异构存储管理)）
- 收益
  * 该 part 主要描述设计理念与系统能力，未给量化加速数据。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ScienceEducationInnovation&part=4&sec=sec_006)）

#### 3) 挖掘硬件特性，使用专有算子加速通信（CAM：大EP / FusedDeepMoE / M2N）
- 背景与问题
  * CAM 是面向昇腾平台的通信加速库，覆盖大模型训练与推理通信场景。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004)）
  * 在 MoE 模型中，`Dispatch/Combine` 等通信操作开销显著，通信耗时占比可达 **30%**。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=通信耗时占比可达30%)）
- 大EP 通信库：减少冲突 + 提升带宽利用率 + 缩短同步等待
  * **通信时序编排**：优化共享专家的 Token 通信模式以减少网络冲突，提高有效带宽利用率。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=通信时序编排)）
  * **端口负载均衡**：通过优化地址偏移的哈希算法，使数据更均匀散列到不同 NPU 端口，缓解端口负载不均。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=负载均衡)）
  * **EPLB + 通算融合**：引入负载均衡与大融合算子，将通信与计算深度融合以掩盖同步等待。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=EPLB负载均衡)）
- FusedDeepMoE：融合算子 + 流水并行的 overlap
  * 将 Decode 阶段 MoE 层的 `Dispatch/GEMM/Combine` 融合为“大算子”，通过细粒度流水并行实现计算与通信重叠。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=FusedDeepMoE)）
- M2N 通信加速：把通信编排进计算时序
  * **通信融合与编排调度**：将 A2F/F2A 通信过程与本地计算融合调度，消除冗余通信，掩盖通信延迟。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=通信融合与编排调度)）
  * **弹性通信能力**：支持 Attention/FFN 节点动态增减，通信域无需销毁并重建。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=支持Attention和FFN节点的动态增减)）
- MIXL：聚合KVcache发送。利用多种传输通道和其他空闲NPU卡的传输资源
  * **分片消息聚合**：将多层 KV Cache 在发送前聚合成一个或少数大消息包，以提高有效带宽利用率与吞吐。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=分片消息聚合)）
  * **异构多径聚合**：聚合利用多种传输通道（如片上 UB、RoCE 网卡等），并利用其他空闲 NPU 卡的传输资源做多路径并行传输，以最大化整体带宽。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=异构多径聚合)）
  * KV Cache 传输性能提升 **30%**。（[引用](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=8&sec=sec_004&hit=传输性能提升30%)）

#### 4) **软 FP8：Ascend C 动态反量化 + Matmul/GroupedMatmul 调优**
- 背景与问题
  * 昇腾 910B/910B3 等不支持 FP8 原生计算，但模型开始广泛采用 FP8 权重（强调在**不支持 FP8 原生计算硬件**上运行 FP8 权重模型）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_001&hit=不支持+FP8+数据类型的原生计算)）
- 工作内容
  * **Vector Core** 做 FP8 转 BF16 **动态反量化**，**Cube Core** 做 **Matmul/GroupedMatmul**；针对 MoE 专家激活做**“选择性反量化”**（`group_list`）；针对大 shape 做带宽优化；对特定模型做 shape 亲和优化。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_002&hit=三、基于昇腾+Ascend+C+的软+FP8+解决方案)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_003&hit=优化逻辑：算子根据+group_list+动态调度计算任务，仅对被激活专家的权重数据执行反量化和矩阵乘法计算，而完全跳过未激活专家的处理流程，从而显著减少不必要的计算开销。)）
- 收益
  * **端到端推理效率提升 32%**；GroupedMatmul（down）吞吐平均 **+40%**，Matmul（gate/up）平均 **+25%**；单台设备可流畅运行完整版 DeepSeek V3.1；兼容 DeepSeek/Qwen3 等 FP8 模型。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_002&hit=32%25+的端到端推理效率提升)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=9&sec=sec_003&hit=GroupedMatmul)）

#### 5) **CPU 推理图编译器 ANNC**（非大模型，但“融合/前移”思路可能可迁移）
- 工作内容
  * **图算融合**把多个小算子融合成大算子、**常量折叠**减少运行时计算；编译期静态打包/**最优布局传递**消除运行时 **Matmul repack** 开销。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_003)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_004)）
- 收益
  * 开源推荐模型 **+20%**；客户推荐模型 **+25%**；Embedding 融合 +5%；常量折叠场景时延 -10%（见各节案例）。（[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_003&hit=在实际应用中，ANNC+在多个开源推荐模型上获得了+20%25+的性能提升，在某客户的推荐模型下获得了+25%25+的性能提升。)；[来源](https://lxchx.github.io/openeuler-2025-notes/show.html?session=ai_session&part=10&sec=sec_004&hit=该优化使单个模型的推理时延降低了约+10%25。)）


