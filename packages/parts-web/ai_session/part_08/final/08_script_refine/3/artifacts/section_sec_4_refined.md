# 昇腾亲和的通信加速库CAM关键技术介绍

## 1. CAM库定位与组成

通信加速库CAM（Communication Acceleration for Ascend）是为昇腾平台打造的通信加速解决方案，旨在为不同的大模型训练与推理场景构建高效的通信能力。CAM主要包含以下四个面向特定场景的加速库：

- **大EP通信库**：针对MoE（Mixture of Experts）场景，提供Prefill和Decode阶段的高性能通信算子。
- **通算融合加速库 (FusedDeepMoE)**：通过深度融合MoE层内的计算与通信，实现极致性能。
- **M2N通信加速库**：为AFD（Attention/FFN Decoupling）分离等M2N（Many-to-Many）通信场景提供弹性可靠的通信能力。
- **KV Cache传输加速库 (MIXL)**：在PD（Pipeline/Data Parallelism）分离场景下，加速节点间的KV Cache传输。

---

## 2. 大EP通信库：MoE场景优化

在MoE模型中，`Dispatch`和`Combine`等通信操作的开销显著，通信耗时占比可达30%。通信时延主要由传输时延和静态时延（控制面开销、算子启动开销）构成。我们针对`Dispatch`算子进行分析，发现其主要瓶颈并实施了以下优化：

| 瓶颈分析 | 原因 | 优化措施 |
| :--- | :--- | :--- |
| **1. 通信数据准备耗时** | 在多核NPU上，为避免地址冲突，分发Token到同一专家时需进行地址偏移计算。该过程采用Scalar计算，效率低下。 | **向量化计算**：将地址偏移计算改造为Vector方式执行，大幅加速数据准备过程。 |
| **2. 数据传输带宽利用率低** | 网络冲突或NPU端口负载不均导致实际传输带宽未被充分利用。 | **通信时序编排**：优化共享专家的Token通信模式（如从2/6打1改为8打1），减少网络冲突。<br>**负载均衡**：通过优化地址偏移的哈希算法，使数据更均匀地散列到不同NPU端口。 |
| **3. 同步等待耗时长** | 大EP（Expert Parallelism）通信模式下，各计算卡之间需要进行全量同步，导致等待开销较大。 | **EPLB负载均衡**：引入负载均衡机制。<br>**通算融合**：构建大融合算子，将通信与计算深度融合，掩盖同步开销。 |

---

## 3. FusedDeepMoE：通算融合加速库

尽管对MoE通信进行了优化，但计算与通信的串行执行模式依然限制了整体性能。此外，MoE层算子数量多导致Kernel Launch开销大，且部分算子算力利用率不高。

**核心思路**：将Decode阶段的整个MoE层（从`Dispatch`到两次GEMM运算，再到`Combine`）融合成一个大算子，通过细粒度流水并行技术实现计算与通信的深度重叠。

**实现方式**：
1.  **Dispatch与GEMM1的深度融合**：
    -   对Token进行动态分组。
    -   采用流水线作业模式：接收一组Token后立即开始计算，同时异步接收下一组Token。
2.  **GEMM2与Combine的深度融合**：
    -   同样采用流水线模式：计算完一部分Token后，立即对这部分数据进行`Combine`通信与聚合，同时开始计算下一组Token。

**社区合作**：该能力已接入SGLang社区，并正与vLLM社区展开合作。

---

## 4. M2N通信加速：AFD分离场景

在LLM推理的Decode阶段，由于Batch Size较小，FFN部分的算力利用率通常较低。AFD（Attention/FFN Decoupling）分离思想通过将Attention和FFN解耦，允许FFN独立组建更大的Batch，从而提升系统总吞吐。然而，该方案引入了Attention节点与FFN节点之间额外的M2N通信开销。

我们构建了M2N通信加速库以应对此挑战，关键技术包括：

- **NPU直驱通信**：通信请求由NPU侧直接发起，而非传统的CPU侧，显著减少了控制面的时间开销。
- **通信融合与编排调度**：将A2F（Attention to FFN）和F2A（FFN to Attention）的通信过程与本地计算进行融合调度，消除冗余通信，掩盖通信延迟。
- **弹性通信能力**：支持Attention和FFN节点的动态增减。通信域能够弹性适应节点变化，无需销毁并重建整个通信域，保证了系统的弹性伸缩能力。

---

## 5. MIXL：KV Cache传输加速库

在PD（Pipeline/Data Parallelism）分离的推理架构下，跨节点的KV Cache传输是关键性能瓶颈之一。我们为此构建了推理传输加速库MIXL（Middleware for Inference Communication Acceleration Layer），作为屏蔽底层传输差异、对接上层AI框架的中间件，可将KV Cache传输性能提升30%。

**核心技术**：
1.  **分片消息聚合 (Sliced Message Aggregation)**：
    -   根据不同策略，将多层KV Cache数据在发送前聚合成一个或少数几个大的消息包。
    -   通过传输大消息包来提升单次传输的数据量，从而提高有效带宽利用率和系统吞吐。
2.  **异构多径聚合 (Heterogeneous Multi-path Aggregation)**：
    -   昇腾架构下，NPU可访问多种传输通道（如片上UB、RoCE网卡等）。
    -   该技术能够聚合利用多种传输路径，包括利用其他空闲NPU卡的传输资源，实现多路径并行传输，最大化整体传输带宽。