# 수집된 ArXiv 논문 목록

**총 33개 논문**
**생성일:** 2025-11-17 09:53:24

---

## 1. Test Research Paper on Deep RL

**Label:** 0

**내용:**
This paper explores deep reinforcement learning with transformer architectures for complex decision making tasks

---

## 2. Test Paper on Deep RL

**Label:** 1

**내용:**
이것은 심층 강화학습에 대한 테스트 논문입니다. Transformer 아키텍처를 사용합니다.

---

## 3. Optimizing Mixture of Block Attention

**Label:** 0

**내용:**
내용 없음

---

## 4. Implicit inference of the reionization history with higher-order statistics of the 21-cm signal

**Label:** 1

**내용:**
내용 없음

---

## 5. Who Moved My Distribution? Conformal Prediction for Interactive Multi-Agent Systems

**Label:** 0

**내용:**
내용 없음

---

## 6. Estimating Total Effects in Bipartite Experiments with Spillovers and Partial Eligibility

**Label:** 1

**내용:**
내용 없음

---

## 7. A Unified Convergence Analysis for Semi-Decentralized Learning: Sampled-to-Sampled vs. Sampled-to-All Communication

**Label:** 0

**내용:**
내용 없음

---

## 8. Drone Swarm Energy Management

**Label:** 1

**내용:**
This note presents an analytical framework for decision-making in drone swarm systems operating under uncertainty, based on the integration of Partially Observable Markov Decision Processes (POMDP) with Deep Deterministic Policy Gradient (DDPG) reinforcement learning. The proposed approach enables adaptive control and cooperative behavior of unmanned aerial vehicles (UAVs) within a cognitive AI platform, where each agent learns optimal energy management and navigation policies from dynamic environmental states. We extend the standard DDPG architecture with a belief-state representation derived from Bayesian filtering, allowing for robust decision-making in partially observable environments. In this paper, for the Gaussian case, we numerically compare the performance of policies derived from DDPG to optimal policies for discretized versions of the original continuous problem. Simulation results demonstrate that the POMDP-DDPG-based swarm control model significantly improves mission success rates and energy efficiency compared to baseline methods. The developed framework supports distributed learning and decision coordination across multiple agents, providing a foundation for scalable cognitive swarm autonomy. The outcomes of this research contribute to the advancement of energy-aware control algorithms for intelligent multi-agent systems and can be applied in security, environmental monitoring, and infrastructure inspection scenarios.

---

## 9. Multistability of Self-Attention Dynamics in Transformers

**Label:** 0

**내용:**
In machine learning, a self-attention dynamics is a continuous-time multiagent-like model of the attention mechanisms of transformers. In this paper we show that such dynamics is related to a multiagent version of the Oja flow, a dynamical system that computes the principal eigenvector of a matrix corresponding for transformers to the value matrix. We classify the equilibria of the ``single-head'' self-attention system into four classes: consensus, bipartite consensus, clustering and polygonal equilibria. Multiple asymptotically stable equilibria from the first three classes often coexist in the self-attention dynamics. Interestingly, equilibria from the first two classes are always aligned with the eigenvectors of the value matrix, often but not exclusively with the principal eigenvector.

---

## 10. Aligning Machiavellian Agents: Behavior Steering via Test-Time Policy Shaping

**Label:** 1

**내용:**
The deployment of decision-making AI agents presents a critical challenge in maintaining alignment with human values or guidelines while operating in complex, dynamic environments. Agents trained solely to achieve their objectives may adopt harmful behavior, exposing a key trade-off between maximizing the reward function and maintaining the alignment. For the pre-trained agents, ensuring alignment is particularly challenging, as retraining can be a costly and slow process. This is further complicated by the diverse and potentially conflicting attributes representing the ethical values for alignment. To address these challenges, we propose a test-time alignment technique based on model-guided policy shaping. Our method allows precise control over individual behavioral attributes, generalizes across diverse reinforcement learning (RL) environments, and facilitates a principled trade-off between ethical alignment and reward maximization without requiring agent retraining. We evaluate our approach using the MACHIAVELLI benchmark, which comprises 134 text-based game environments and thousands of annotated scenarios involving ethical decisions. The RL agents are first trained to maximize the reward in their respective games. At test time, we apply policy shaping via scenario-action attribute classifiers to ensure decision alignment with ethical attributes. We compare our approach against prior training-time methods and general-purpose agents, as well as study several types of ethical violations and power-seeking behavior. Our results demonstrate that test-time policy shaping provides an effective and scalable solution for mitigating unethical behavior across diverse environments and alignment attributes.

---

## 11. HetDAPAC: Leveraging Attribute Heterogeneity in Distributed Attribute-Based Private Access Control

**Label:** 0

**내용:**
Verifying user attributes to provide fine-grained access control to databases is fundamental to attribute-based authentication. Either a single (central) authority verifies all the attributes, or multiple independent authorities verify the attributes distributedly. In the central setup, the authority verifies all user attributes, and the user downloads only the authorized record. While this is communication efficient, it reveals all user attributes to the authority. A distributed setup prevents this privacy breach by letting each authority verify and learn only one attribute. Motivated by this, Jafarpisheh~et~al. introduced an information-theoretic formulation, called distributed attribute-based private access control (DAPAC). With $N$ non-colluding authorities (servers), $N$ attributes and $K$ possible values for each attribute, the DAPAC system lets each server learn only the single attribute value that it verifies, and is oblivious to the remaining $N-1$. The user retrieves its designated record, without learning anything about the remaining database records. The goal is to maximize the rate, i.e., the ratio of desired message size to total download size. However, not all attributes are sensitive, and DAPAC's privacy constraints can be too restrictive, negatively affecting the rate. To leverage the heterogeneous privacy requirements of user attributes, we propose heterogeneous (Het)DAPAC, a framework which off-loads verification of $N-D$ of the $N$ attributes to a central server, and retains DAPAC's architecture for the $D$ sensitive attributes. We first present a HetDAPAC scheme, which improves the rate from $\frac{1}{2K}$ to $\frac{1}{K+1}$, while sacrificing the privacy of a few non-sensitive attributes. Unlike DAPAC, our scheme entails a download imbalance across servers; we propose a second scheme achieving a balanced per-server download and a rate of $\frac{D+1}{2KD}$.

---

## 12. Incremental Data-Driven Policy Synthesis via Game Abstractions

**Label:** 1

**내용:**
We address the synthesis of control policies for unknown discrete-time stochastic dynamical systems to satisfy temporal logic objectives. We present a data-driven, abstraction-based control framework that integrates online learning with novel incremental game-solving. Under appropriate continuity assumptions, our method abstracts the system dynamics into a finite stochastic (2.5-player) game graph derived from data. Given a requirement over time on this graph, we compute the winning region -- i.e., the set of initial states from which the objective is satisfiable -- in the resulting game, together with a corresponding control policy.
  Our main contribution is the construction of abstractions, winning regions and control policies incrementally, as data about the system dynamics accumulates. Concretely, our algorithm refines under- and over-approximations of reachable sets for each state-action pair as new data samples arrive. These refinements induce structural modifications in the game graph abstraction -- such as the addition or removal of nodes and edges -- which in turn modify the winning region. Crucially, we show that these updates are inherently monotonic: under-approximations can only grow, over-approximations can only shrink, and the winning region can only expand.
  We exploit this monotonicity by defining an objective-induced ranking function on the nodes of the abstract game that increases monotonically as new data samples are incorporated. These ranks underpin our novel incremental game-solving algorithm, which employs customized gadgets (DAG-like subgames) within a rank-lifting algorithm to efficiently update the winning region. Numerical case studies demonstrate significant computational savings compared to the baseline approach, which resolves the entire game from scratch whenever new data samples arrive.

---

## 13. Generalizing Fair Clustering to Multiple Groups: Algorithms and Applications

**Label:** 0

**내용:**
Clustering is a fundamental task in machine learning and data analysis, but it frequently fails to provide fair representation for various marginalized communities defined by multiple protected attributes -- a shortcoming often caused by biases in the training data. As a result, there is a growing need to enhance the fairness of clustering outcomes, ideally by making minimal modifications, possibly as a post-processing step after conventional clustering. Recently, Chakraborty et al. [COLT'25] initiated the study of \emph{closest fair clustering}, though in a restricted scenario where data points belong to only two groups. In practice, however, data points are typically characterized by many groups, reflecting diverse protected attributes such as age, ethnicity, gender, etc.
  In this work, we generalize the study of the \emph{closest fair clustering} problem to settings with an arbitrary number (more than two) of groups. We begin by showing that the problem is NP-hard even when all groups are of equal size -- a stark contrast with the two-group case, for which an exact algorithm exists. Next, we propose near-linear time approximation algorithms that efficiently handle arbitrary-sized multiple groups, thereby answering an open question posed by Chakraborty et al. [COLT'25].
  Leveraging our closest fair clustering algorithms, we further achieve improved approximation guarantees for the \emph{fair correlation clustering} problem, advancing the state-of-the-art results established by Ahmadian et al. [AISTATS'20] and Ahmadi et al. [2020]. Additionally, we are the first to provide approximation algorithms for the \emph{fair consensus clustering} problem involving multiple (more than two) groups, thus addressing another open direction highlighted by Chakraborty et al. [COLT'25].

---

## 14. Terrain Costmap Generation via Scaled Preference Conditioning

**Label:** 1

**내용:**
Successful autonomous robot navigation in off-road domains requires the ability to generate high-quality terrain costmaps that are able to both generalize well over a wide variety of terrains and rapidly adapt relative costs at test time to meet mission-specific needs. Existing approaches for costmap generation allow for either rapid test-time adaptation of relative costs (e.g., semantic segmentation methods) or generalization to new terrain types (e.g., representation learning methods), but not both. In this work, we present scaled preference conditioned all-terrain costmap generation (SPACER), a novel approach for generating terrain costmaps that leverages synthetic data during training in order to generalize well to new terrains, and allows for rapid test-time adaptation of relative costs by conditioning on a user-specified scaled preference context. Using large-scale aerial maps, we provide empirical evidence that SPACER outperforms other approaches at generating costmaps for terrain navigation, with the lowest measured regret across varied preferences in five of seven environments for global path planning.

---

## 15. CVChess: A Deep Learning Framework for Converting Chessboard Images to Forsyth-Edwards Notation

**Label:** 0

**내용:**
Chess has experienced a large increase in viewership since the pandemic, driven largely by the accessibility of online learning platforms. However, no equivalent assistance exists for physical chess games, creating a divide between analog and digital chess experiences. This paper presents CVChess, a deep learning framework for converting chessboard images to Forsyth-Edwards Notation (FEN), which is later input into online chess engines to provide you with the best next move. Our approach employs a convolutional neural network (CNN) with residual layers to perform piece recognition from smartphone camera images. The system processes RGB images of a physical chess board through a multistep process: image preprocessing using the Hough Line Transform for edge detection, projective transform to achieve a top-down board alignment, segmentation into 64 individual squares, and piece classification into 13 classes (6 unique white pieces, 6 unique black pieces and an empty square) using the residual CNN. Residual connections help retain low-level visual features while enabling deeper feature extraction, improving accuracy and stability during training. We train and evaluate our model using the Chess Recognition Dataset (ChessReD), containing 10,800 annotated smartphone images captured under diverse lighting conditions and angles. The resulting classifications are encoded as an FEN string, which can be fed into a chess engine to generate the most optimal move

---

## 16. Scalable Policy Evaluation with Video World Models

**Label:** 1

**내용:**
Training generalist policies for robotic manipulation has shown great promise, as they enable language-conditioned, multi-task behaviors across diverse scenarios. However, evaluating these policies remains difficult because real-world testing is expensive, time-consuming, and labor-intensive. It also requires frequent environment resets and carries safety risks when deploying unproven policies on physical robots. Manually creating and populating simulation environments with assets for robotic manipulation has not addressed these issues, primarily due to the significant engineering effort required and the often substantial sim-to-real gap, both in terms of physics and rendering. In this paper, we explore the use of action-conditional video generation models as a scalable way to learn world models for policy evaluation. We demonstrate how to incorporate action conditioning into existing pre-trained video generation models. This allows leveraging internet-scale in-the-wild online videos during the pre-training stage, and alleviates the need for a large dataset of paired video-action data, which is expensive to collect for robotic manipulation. Our paper examines the effect of dataset diversity, pre-trained weight and common failure cases for the proposed evaluation pipeline.Our experiments demonstrate that, across various metrics, including policy ranking and the correlation between actual policy values and predicted policy values, these models offer a promising approach for evaluating policies without requiring real-world interactions.

---

## 17. Experience-Guided Adaptation of Inference-Time Reasoning Strategies

**Label:** 0

**내용:**
Enabling agentic AI systems to adapt their problem-solving approaches based on post-training interactions remains a fundamental challenge. While systems that update and maintain a memory at inference time have been proposed, existing designs only steer the system by modifying textual input to a language model or agent, which means that they cannot change sampling parameters, remove tools, modify system prompts, or switch between agentic and workflow paradigms. On the other hand, systems that adapt more flexibly require offline optimization and remain static once deployed. We present Experience-Guided Reasoner (EGuR), which generates tailored strategies -- complete computational procedures involving LLM calls, tools, sampling parameters, and control logic -- dynamically at inference time based on accumulated experience. We achieve this using an LLM-based meta-strategy -- a strategy that outputs strategies -- enabling adaptation of all strategy components (prompts, sampling parameters, tool configurations, and control logic). EGuR operates through two components: a Guide generates multiple candidate strategies conditioned on the current problem and structured memory of past experiences, while a Consolidator integrates execution feedback to improve future strategy generation. This produces complete, ready-to-run strategies optimized for each problem, which can be cached, retrieved, and executed as needed without wasting resources. Across five challenging benchmarks (AIME 2025, 3-SAT, and three Big Bench Extra Hard tasks), EGuR achieves up to 14% accuracy improvements over the strongest baselines while reducing computational costs by up to 111x, with both metrics improving as the system gains experience.

---

## 18. W2S-AlignTree: Weak-to-Strong Inference-Time Alignment for Large Language Models via Monte Carlo Tree Search

**Label:** 1

**내용:**
Large Language Models (LLMs) demonstrate impressive capabilities, yet their outputs often suffer from misalignment with human preferences due to the inadequacy of weak supervision and a lack of fine-grained control. Training-time alignment methods like Reinforcement Learning from Human Feedback (RLHF) face prohibitive costs in expert supervision and inherent scalability limitations, offering limited dynamic control during inference. Consequently, there is an urgent need for scalable and adaptable alignment mechanisms. To address this, we propose W2S-AlignTree, a pioneering plug-and-play inference-time alignment framework that synergistically combines Monte Carlo Tree Search (MCTS) with the Weak-to-Strong Generalization paradigm for the first time. W2S-AlignTree formulates LLM alignment as an optimal heuristic search problem within a generative search tree. By leveraging weak model's real-time, step-level signals as alignment proxies and introducing an Entropy-Aware exploration mechanism, W2S-AlignTree enables fine-grained guidance during strong model's generation without modifying its parameters. The approach dynamically balances exploration and exploitation in high-dimensional generation search trees. Experiments across controlled sentiment generation, summarization, and instruction-following show that W2S-AlignTree consistently outperforms strong baselines. Notably, W2S-AlignTree raises the performance of Llama3-8B from 1.89 to 2.19, a relative improvement of 15.9 on the summarization task.

---

## 19. Distributed Optimization of Pairwise Polynomial Graph Spectral Functions via Subgraph Optimization

**Label:** 0

**내용:**
We study distributed optimization of finite-degree polynomial Laplacian spectral objectives under fixed topology and a global weight budget, targeting the collective behavior of the entire spectrum rather than a few extremal eigenvalues. By re-formulating the global cost in a bilinear form, we derive local subgraph problems whose gradients approximately align with the global descent direction via an SVD-based test on the $ZC$ matrix. This leads to an iterate-and-embed scheme over disjoint 1-hop neighborhoods that preserves feasibility by construction (positivity and budget) and scales to large geometric graphs. For objectives that depend on pairwise eigenvalue differences $h(λ_i-λ_j)$, we obtain a quadratic upper bound in the degree vector, which motivates a ``warm-start'' by degree-regularization. The warm start uses randomized gossip to estimate global average degree, accelerating subsequent local descent while maintaining decentralization, and realizing $\sim95\%{}$ of the performance with respect to centralized optimization. We further introduce a learning-based proposer that predicts one-shot edge updates on maximal 1-hop embeddings, yielding immediate objective reductions. Together, these components form a practical, modular pipeline for spectrum-aware weight tuning that preserves constraints and applies across a broader class of whole-spectrum costs.

---

## 20. Collaborative Representation Learning for Alignment of Tactile, Language, and Vision Modalities

**Label:** 1

**내용:**
Tactile sensing offers rich and complementary information to vision and language, enabling robots to perceive fine-grained object properties. However, existing tactile sensors lack standardization, leading to redundant features that hinder cross-sensor generalization. Moreover, existing methods fail to fully integrate the intermediate communication among tactile, language, and vision modalities. To address this, we propose TLV-CoRe, a CLIP-based Tactile-Language-Vision Collaborative Representation learning method. TLV-CoRe introduces a Sensor-Aware Modulator to unify tactile features across different sensors and employs tactile-irrelevant decoupled learning to disentangle irrelevant tactile features. Additionally, a Unified Bridging Adapter is introduced to enhance tri-modal interaction within the shared representation space. To fairly evaluate the effectiveness of tactile models, we further propose the RSS evaluation framework, focusing on Robustness, Synergy, and Stability across different methods. Experimental results demonstrate that TLV-CoRe significantly improves sensor-agnostic representation learning and cross-modal alignment, offering a new direction for multimodal tactile representation.

---

## 21. OpenUS: A Fully Open-Source Foundation Model for Ultrasound Image Analysis via Self-Adaptive Masked Contrastive Learning

**Label:** 0

**내용:**
Ultrasound (US) is one of the most widely used medical imaging modalities, thanks to its low cost, portability, real-time feedback, and absence of ionizing radiation. However, US image interpretation remains highly operator-dependent and varies significantly across anatomical regions, acquisition protocols, and device types. These variations, along with unique challenges such as speckle, low contrast, and limited standardized annotations, hinder the development of generalizable, label-efficient ultrasound AI models. In this paper, we propose OpenUS, the first reproducible, open-source ultrasound foundation model built on a large collection of public data. OpenUS employs a vision Mamba backbone, capturing both local and global long-range dependencies across the image. To extract rich features during pre-training, we introduce a novel self-adaptive masking framework that combines contrastive learning with masked image modeling. This strategy integrates the teacher's attention map with student reconstruction loss, adaptively refining clinically-relevant masking to enhance pre-training effectiveness. OpenUS also applies a dynamic learning schedule to progressively adjust the difficulty of the pre-training process. To develop the foundation model, we compile the largest to-date public ultrasound dataset comprising over 308K images from 42 publicly available datasets, covering diverse anatomical regions, institutions, imaging devices, and disease types. Our pre-trained OpenUS model can be easily adapted to specific downstream tasks by serving as a backbone for label-efficient fine-tuning. Code is available at https://github.com/XZheng0427/OpenUS.

---

## 22. FarSkip-Collective: Unhobbling Blocking Communication in Mixture of Experts Models

**Label:** 1

**내용:**
Blocking communication presents a major hurdle in running MoEs efficiently in distributed settings. To address this, we present FarSkip-Collective which modifies the architecture of modern models to enable overlapping of their computation with communication. Our approach modifies the architecture to skip connections in the model and it is unclear a priori whether the modified model architecture can remain as capable, especially for large state-of-the-art models and while modifying all of the model layers. We answer this question in the affirmative and fully convert a series of state-of-the-art models varying from 16B to 109B parameters to enable overlapping of their communication while achieving accuracy on par with their original open-source releases. For example, we convert Llama 4 Scout (109B) via self-distillation and achieve average accuracy within 1% of its instruction tuned release averaged across a wide range of downstream evaluations. In addition to demonstrating retained accuracy of the large modified models, we realize the benefits of FarSkip-Collective through optimized implementations that explicitly overlap communication with computation, accelerating both training and inference in existing frameworks.

---

## 23. Honesty over Accuracy: Trustworthy Language Models through Reinforced Hesitation

**Label:** 0

**내용:**
Modern language models fail a fundamental requirement of trustworthy intelligence: knowing when not to answer. Despite achieving impressive accuracy on benchmarks, these models produce confident hallucinations, even when wrong answers carry catastrophic consequences. Our evaluations on GSM8K, MedQA and GPQA show frontier models almost never abstain despite explicit warnings of severe penalties, suggesting that prompts cannot override training that rewards any answer over no answer. As a remedy, we propose Reinforced Hesitation (RH): a modification to Reinforcement Learning from Verifiable Rewards (RLVR) to use ternary rewards (+1 correct, 0 abstention, -$λ$ error) instead of binary. Controlled experiments on logic puzzles reveal that varying $λ$ produces distinct models along a Pareto frontier, where each training penalty yields the optimal model for its corresponding risk regime: low penalties produce aggressive answerers, high penalties conservative abstainers. We then introduce two inference strategies that exploit trained abstention as a coordination signal: cascading routes queries through models with decreasing risk tolerance, while self-cascading re-queries the same model on abstention. Both outperform majority voting with lower computational cost. These results establish abstention as a first-class training objective that transforms ``I don't know'' from failure into a coordination signal, enabling models to earn trust through calibrated honesty about their limits.

---

## 24. Learning and Testing Convex Functions

**Label:** 1

**내용:**
We consider the problems of \emph{learning} and \emph{testing} real-valued convex functions over Gaussian space. Despite the extensive study of function convexity across mathematics, statistics, and computer science, its learnability and testability have largely been examined only in discrete or restricted settings -- typically with respect to the Hamming distance, which is ill-suited for real-valued functions.
  In contrast, we study these problems in high dimensions under the standard Gaussian measure, assuming sample access to the function and a mild smoothness condition, namely Lipschitzness. A smoothness assumption is natural and, in fact, necessary even in one dimension: without it, convexity cannot be inferred from finitely many samples. As our main results, we give:
  - Learning Convex Functions: An agnostic proper learning algorithm for Lipschitz convex functions that achieves error $\varepsilon$ using $n^{O(1/\varepsilon^2)}$ samples, together with a complementary lower bound of $n^{\mathrm{poly}(1/\varepsilon)}$ samples in the \emph{correlational statistical query (CSQ)} model.
  - Testing Convex Functions: A tolerant (two-sided) tester for convexity of Lipschitz functions with the same sample complexity (as a corollary of our learning result), and a one-sided tester (which never rejects convex functions) using $O(\sqrt{n}/\varepsilon)^n$ samples.

---

## 25. Photonic-integrated quantum sensor array for microscale magnetic localisation

**Label:** 0

**내용:**
Nitrogen-vacancy centres (NVs) are promising solid-state nanoscale quantum sensors for applications ranging from material science to biotechnology. Using multiple sensors simultaneously offers advantages for probing spatiotemporal correlations of fluctuating fields or the dynamics of point defects. In this work, by integrating NVs with foundry silicon-nitride photonic integrated circuits, we realise the scalable operation of eight localised NV sensors in an array, with simultaneous, distinct readout of the individual sensors. Using the eight NV sensors and machine-learning methods for multi-point magnetic field reconstruction, we demonstrate microscale magnetic localisation of a 30 $μ$m-sized needle tip. Experimentally, the needle tip can be localised with an error below its dimension and tracked dynamically with high fidelity. We further simulate the feasibility of our platform for monitoring the position and orientation of magnetic microrobots designed for biological and clinical purposes. Without the complexity of bulk optics, our photonic-integrated multi-sensor platform presents a step towards real-life biomedical applications under out-of-the-lab conditions.

---

## 26. Intrinsic Dimension Estimation for Radio Galaxy Zoo using Diffusion Models

**Label:** 1

**내용:**
In this work, we estimate the intrinsic dimension (iD) of the Radio Galaxy Zoo (RGZ) dataset using a score-based diffusion model. We examine how the iD estimates vary as a function of Bayesian neural network (BNN) energy scores, which measure how similar the radio sources are to the MiraBest subset of the RGZ dataset. We find that out-of-distribution sources exhibit higher iD values, and that the overall iD for RGZ exceeds those typically reported for natural image datasets. Furthermore, we analyse how iD varies across Fanaroff-Riley (FR) morphological classes and as a function of the signal-to-noise ratio (SNR). While no relationship is found between FR I and FR II classes, a weak trend toward higher SNR at lower iD. Future work using the RGZ dataset could make use of the relationship between iD and energy scores to quantitatively study and improve the representations learned by various self-supervised learning algorithms.

---

## 27. Power law attention biases for molecular transformers

**Label:** 0

**내용:**
Transformers are the go-to architecture for most data modalities due to their scalability. While they have been applied extensively to molecular property prediction, they do not dominate the field as they do elsewhere. One cause may be the lack of structural biases that effectively capture the relationships between atoms. Here, we investigate attention biases as a simple and natural way to encode structure. Motivated by physical power laws, we propose a family of low-complexity attention biases $b_{ij} = p \log|| \mathbf{r}_i - \mathbf{r}_j||$ which weigh attention probabilities according to interatomic distances. On the QM9 and SPICE datasets, this approach outperforms positional encodings and graph attention while remaining competitive with more complex Gaussian kernel biases. We also show that good attention biases can compensate for a complete ablation of scaled dot-product attention, suggesting a low-cost path toward interpretable molecular transformers.

---

## 28. Data-efficient U-Net for Segmentation of Carbide Microstructures in SEM Images of Steel Alloys

**Label:** 1

**내용:**
Understanding reactor-pressure-vessel steel microstructure is crucial for predicting mechanical properties, as carbide precipitates both strengthen the alloy and can initiate cracks. In scanning electron microscopy images, gray-value overlap between carbides and matrix makes simple thresholding ineffective. We present a data-efficient segmentation pipeline using a lightweight U-Net (30.7~M parameters) trained on just \textbf{10 annotated scanning electron microscopy images}. Despite limited data, our model achieves a \textbf{Dice-Sørensen coefficient of 0.98}, significantly outperforming the state-of-the-art in the field of metallurgy (classical image analysis: 0.85), while reducing annotation effort by one order of magnitude compared to the state-of-the-art data efficient segmentation model. This approach enables rapid, automated carbide quantification for alloy design and generalizes to other steel types, demonstrating the potential of data-efficient deep learning in reactor-pressure-vessel steel analysis.

---

## 29. Risk-Aware Deep Reinforcement Learning for Dynamic Portfolio Optimization

**Label:** 0

**내용:**
This paper presents a deep reinforcement learning (DRL) framework for dynamic portfolio optimization under market uncertainty and risk. The proposed model integrates a Sharpe ratio-based reward function with direct risk control mechanisms, including maximum drawdown and volatility constraints. Proximal Policy Optimization (PPO) is employed to learn adaptive asset allocation strategies over historical financial time series. Model performance is benchmarked against mean-variance and equal-weight portfolio strategies using backtesting on high-performing equities. Results indicate that the DRL agent stabilizes volatility successfully but suffers from degraded risk-adjusted returns due to over-conservative policy convergence, highlighting the challenge of balancing exploration, return maximization, and risk mitigation. The study underscores the need for improved reward shaping and hybrid risk-aware strategies to enhance the practical deployment of DRL-based portfolio allocation models.

---

## 30. Inferring response times of perceptual decisions with Poisson variational autoencoders

**Label:** 1

**내용:**
Many properties of perceptual decision making are well-modeled by deep neural networks. However, such architectures typically treat decisions as instantaneous readouts, overlooking the temporal dynamics of the decision process. We present an image-computable model of perceptual decision making in which choices and response times arise from efficient sensory encoding and Bayesian decoding of neural spiking activity. We use a Poisson variational autoencoder to learn unsupervised representations of visual stimuli in a population of rate-coded neurons, modeled as independent homogeneous Poisson processes. A task-optimized decoder then continually infers an approximate posterior over actions conditioned on incoming spiking activity. Combining these components with an entropy-based stopping rule yields a principled and image-computable model of perceptual decisions capable of generating trial-by-trial patterns of choices and response times. Applied to MNIST digit classification, the model reproduces key empirical signatures of perceptual decision making, including stochastic variability, right-skewed response time distributions, logarithmic scaling of response times with the number of alternatives (Hick's law), and speed-accuracy trade-offs.

---

## 31. Context-aware Adaptive Visualizations for Critical Decision Making

**Label:** 0

**내용:**
Effective decision-making often relies on timely insights from complex visual data. While Information Visualization (InfoVis) dashboards can support this process, they rarely adapt to users' cognitive state, and less so in real time. We present Symbiotik, an intelligent, context-aware adaptive visualization system that leverages neurophysiological signals to estimate mental workload (MWL) and dynamically adapt visual dashboards using reinforcement learning (RL). Through a user study with 120 participants and three visualization types, we demonstrate that our approach improves task performance and engagement. Symbiotik offers a scalable, real-time adaptation architecture, and a validated methodology for neuroadaptive user interfaces.

---

## 32. Quantifying and Improving Adaptivity in Conformal Prediction through Input Transformations

**Label:** 1

**내용:**
Conformal prediction constructs a set of labels instead of a single point prediction, while providing a probabilistic coverage guarantee. Beyond the coverage guarantee, adaptiveness to example difficulty is an important property. It means that the method should produce larger prediction sets for more difficult examples, and smaller ones for easier examples. Existing evaluation methods for adaptiveness typically analyze coverage rate violation or average set size across bins of examples grouped by difficulty. However, these approaches often suffer from imbalanced binning, which can lead to inaccurate estimates of coverage or set size. To address this issue, we propose a binning method that leverages input transformations to sort examples by difficulty, followed by uniform-mass binning. Building on this binning, we introduce two metrics to better evaluate adaptiveness. These metrics provide more reliable estimates of coverage rate violation and average set size due to balanced binning, leading to more accurate adaptivity assessment. Through experiments, we demonstrate that our proposed metric correlates more strongly with the desired adaptiveness property compared to existing ones. Furthermore, motivated by our findings, we propose a new adaptive prediction set algorithm that groups examples by estimated difficulty and applies group-conditional conformal prediction. This allows us to determine appropriate thresholds for each group. Experimental results on both (a) an Image Classification (ImageNet) (b) a medical task (visual acuity prediction) show that our method outperforms existing approaches according to the new metrics.

---

## 33. Stable Quantum Vortices in Lee-Huang-Yang Dipolar Superfluids

**Label:** 0

**내용:**
The nucleation and dynamics of vortices in the quasi-two-dimensional rotating dipolar Bose-Einstein condensate are explored by taking into account the Lee-Huang-Yang (LHY) correction to the mean-field (MF) theory. Assuming approximate cancellation of the MF interactions, we focus on the formation of a pure LHY superfluid. The effect of rotational frequency $Ω$ is investigated numerically by determining the corresponding number of stable vortices in the superfluid, together with the respective energy per particle $E$ and chemical potential $μ$. The LHY superfluid provides a deep minimum of $E$ and $μ$, indicating that it is a remarkably robust state of quantum matter. By fixing the LHY interaction strength, an exact single-vortex critical frequency is found, along with the respective chemical potential. A notable feature, observed when creating the LHY superfluid with fewer than five vortices, which is understood as being due to the superfluid's nonlinearity and trapping aspect ratio, is the large frequency ranges admitting the production of two and four vortices, as compared to the small frequency ranges to obtain one and three vortices.

---

