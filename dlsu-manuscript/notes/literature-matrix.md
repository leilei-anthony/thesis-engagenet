# Literature Matrix: Chapter 2 (Related Works)

Working notes, not part of the build. Each row records what was checked and how.

**Checked** values:
- **Full text:** I read the relevant section of the paper.
- **Abstract:** abstract or publisher listing only.
- **Secondary:** the figure comes from another paper's description of the work.

Anything not marked full text should be confirmed by you before the defense if the panel is likely to ask about it.

**Venue:** peer-reviewed venue, or "preprint" (arXiv, not peer reviewed). The panel asked for reputable venues, so preprints are named as preprints in the text.

## 1. Automated detection of engagement and affect in learning

| Key | Work | Venue | What / how | Findings used | Checked | Relevance |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| dmello2015 | D'Mello & Kory (2015) | ACM Computing Surveys 47(3) | Meta-analysis of 90 multimodal affect detection systems | Multimodal systems beat the best single modality in 85% of systems; mean gain 9.83%; smaller gains with natural (vs. acted) data | Abstract | Background: more signals help, but gains shrink on natural data |
| whitehill2014 | Whitehill et al. (2014) | IEEE TAC 5(1) | 34 students, cognitive-skills training; engagement labeled on frames and 10 s clips | Clip labels predicted from the average of frame labels, r = 0.85; "static expressions contain the bulk of the information used by observers" | Abstract | Supports using a few frames per clip, and why frame choice could matter |
| bosch2016 | Bosch et al. (2016) | ACM TiiS 6(2) | Face and body video in a school computer lab | Above-chance detection of several affective states; generalized across time of day and days | Abstract | Video works in real classrooms. **No numbers quoted.** |
| monkaresi2017 | Monkaresi et al. (2017) | IEEE TAC 8(1) | Kinect facial features, LBP-TOP, and heart rate; self-reported engagement during essay writing | Video features detect engagement; heart rate added little (secondary) | Abstract and secondary | Background only |

## 2. Engagement datasets

| Key | Dataset | Venue | Size | Setting | Labels / annotation | Checked |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| gupta2016 | DAiSEE | Preprint (arXiv, v7 2022) | 9,068 clips (10 s), 112 users | Webcam, e-learning | 4 states (boredom, confusion, engagement, frustration) × 4 levels; crowd labels; gold standard from psychologists | Full text: Table 2, label counts; Table 3, benchmarks |
| kaur2018 | EngageWild | DICTA 2018 | 195 videos (about 16.5 h), 78 subjects | In the wild | 4 levels, several labelers; multiple-instance learning | Abstract |
| singh2023 | EngageNet | ICMI 2023 | About 11.3K clips (10 s), 127 participants (83 M, 44 F, aged 18–37) | Unconstrained: labs, dorms, open spaces; webcam ≥ 640×480 | 4 levels; 3 annotators; quadratic weighted κ = 0.73, 0.79, 0.77 | Full text: §3 |
| wu2024cmose | CMOSE | CVPR Workshops 2024 | 12,193 segments (mean 13.72 s), 102 participants | Online presentation-training classes (gallery view) | 4 levels; 7 labelers trained by psychologists; ICC(2,1) = 0.84; video, audio and speech | Full text (arXiv v2 HTML) |
| zhao2025 | RAER | ICCV 2025 (panel suggestion) | About 2,700 clips (5–15 s), about 140 students | Classrooms, libraries, labs, dormitories | **Five academic emotions** (enjoyment, neutrality, confusion, fatigue, distraction); coarse set: engaged (first four) vs. distracted; neutrality 65.23%; about 10 annotators per clip; 80/20 split "striving to exclude overlapping individuals" | Full text (arXiv 2507.00586), checked 10 Nov |

Two facts from DAiSEE:
- **Engagement label counts:** very low 61, low 459, high 4,477, very high 4,071. Only 5.7% of clips are in the two low levels.
- **4-level benchmark accuracies:** InceptionNet frame-level 47.1%, video-level 46.4%, C3D trained 48.6%, C3D fine-tuned 56.1%, LRCN 57.9%.

## 3. Engagement classification models

| Key | Work | Venue | Data | Input / frames | Model | Result | Checked |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| gupta2016 | Gupta et al. (2016) | Preprint | DAiSEE | Raw frames | LRCN | 57.9% (4-level) | Full text |
| liao2021 | Liao et al. (2021) | Applied Intelligence 51(10) | DAiSEE | Face crops; SE-ResNet-50 and LSTM with global attention | DFSTN | 58.84% | Abstract (Springer), checked 10 Nov; pp. 6609–6621 |
| abedi2021 | Abedi & Khan (2021) | CRV 2021 | DAiSEE (1,784 test clips) | Raw frames, down-sampled to 50 per clip, 224×224 | ResNet + TCN | 63.9% | Full text |
| mehta2022 | Mehta et al. (2022) | Applied Intelligence 52 | DAiSEE | 3D video volumes | 3D DenseNet with self-attention | 63.59% | Abstract |
| selim2022 | Selim et al. (2022) | IEEE Access 10 | DAiSEE; VRESEE (own) | Frames | EfficientNetB7 + LSTM | 67.48% on DAiSEE | Abstract |
| singh2023 | Singh et al. (2023) | ICMI 2023 | EngageNet | OpenFace 2.0 gaze, head pose and AUs. The clip is split into 20 uniform segments (Transformer) or 10 (LSTM), with mean and SD per segment; every frame contributes | Transformer | 67.61% test (G+HP+AU); fusion with MARLIN 66.5% | Full text: Tables 3–5 |
| vedernikov2024 | Vedernikov et al. (2024), TCCT-Net | CVPR Workshops 2024 | EngageNet | 2 head-pose signals (vs. 98 features in the baselines), as continuous signals | Two-stream CNN–Transformer | **68.91% on the validation split** (not test); inference 2.59 s for the validation set vs. 61–97 s for image-based RNNs, excluding feature extraction | Full text (arXiv 2404.09474v2), checked 10 Nov |
| baltrusaitis2018 | OpenFace 2.0 | FG 2018 | Not applicable | Facial behavior toolkit used by EngageNet | Not applicable | Not applicable | From Singh's reference list |
| cai2023marlin | Cai et al. (2023), MARLIN | CVPR 2023 | Not applicable | Masked autoencoder pretrained on unlabeled face videos; general-purpose facial representation | Not applicable | Fused with OpenFace in Singh's baselines: 66.5% | Crossref record (added 10 Nov) |
| abedi2024stgcn | Abedi & Khan (2024) | ICPR 2024, LNCS, pp. 321–338 | EngageNet; Online Student Engagement | 78 MediaPipe facial landmarks (68 Dlib-matched + 10 iris), every frame | Spatial-temporal graph conv. net (ordinal) | 71.24% four-class on **validation** (test labels not released); ST-GCN 69.37%; Singh Transformer 69.10% on the same split. Every 2nd–16th frame: 68.13–69.07% | Crossref + arXiv v2 Tables 1, 3 (added 14 Nov). **Closest work to your feature set: read it** |

**Added 10 Nov for Chapter 3 (§3.1, engagement vs. emotion):** dmello2013, D'Mello (2013), *Journal of Educational Psychology* 105(4), 1082–1099. A meta-analysis of 24 studies (1,740 students) of 14 discrete affective states during learning with technology. "Engagement/flow" was consistently among the most frequent. Checked: Crossref and abstract.

**Caution:** the DAiSEE accuracies come from papers that differ in input, model, preprocessing, and sometimes the test set. They are not a controlled comparison. The chapter says so.

## 4. Vision-language models (VLMs / MLLMs) for engagement and academic emotion (R2)

| Key | Work | Venue | Models | Data / input | Findings | Checked |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| teotia2024 | Teotia et al. (2024) | IEEE ICDM Workshops 2024 | GPT-4o mini, LLaVA-v1.5 | Images: SCB classroom behavior; EMOTIC | VLMs good at basic emotion struggle with in-context engagement; confuse engaged and distracted behavior (reading vs. bowing the head) | Full text: abstract and introduction |
| wang2025vlm | Wang, Yang & Chen (2025) | Preprint | Llama-3.2-11B-Vision, Qwen2.5-VL-7B, zero-shot | 5,000 face images; confused, distracted, happy, neutral, tired | Moderate overall; good on happy; failed on distracted; Qwen better on confused | Abstract |
| goyal2026 | Goyal et al. (2026) | Preprint; non-archival CV4Edu workshop at CVPR 2026 | CLIP, BLIP-VQA, GPT-4o, LLaVA-1.5-7B, Qwen2.5-VL-7B, zero-shot | DAiSEE (300 test clips); SCB scene images | κ ≤ 0.10 on individual DAiSEE students; 85–100% of predictions in one class; up to 32-point swings from prompt wording; GPT-4o refused 98% of chain-of-thought requests on student faces; scene-level κ ≈ 0.60 | Abstract |
| vedernikov2025 | Vedernikov et al. (2025) | Preprint | VLM used to judge label reliability, not to classify | EngageNet, DREAMS, PAFE | Curriculum learning with refined labels: EngageNet up to +1.21% in 3 of 6 feature settings | Abstract |
| zhao2025 | Zhao et al. (2025), CLIP-CAER | ICCV 2025 | CLIP with learnable text prompts | RAER clips; face plus context | UAR 68.00% on RAER vs. 61.19% for the next best (DFER-CLIP); beats video facial-expression methods built for basic emotions | Full text, checked 10 Nov |
| cheng2024 | Cheng et al. (2024), Emotion-LLaMA | NeurIPS 2024 | Audio, visual and text MLLM | MER2023, DFEW, EMER | F1 0.9036 on MER2023-SEMI; best zero-shot UAR and WAR on DFEW | Abstract |

## 5. Frame selection in video understanding

| Key | Work | Venue | Rule type | Findings used | Checked |
| :-- | :--- | :--- | :--- | :--- | :--- |
| wang2016 | TSN | ECCV 2016 | Position: equal segments | Sparse coverage of the whole video | Checked earlier |
| korbar2019 | SCSampler | ICCV 2019 | Content: salient *clips* | +7% accuracy and more than 15× less compute on Sports1M | Abstract |
| tang2025aks | Tang et al. (2025), AKS | CVPR 2025 | Content: prompt relevance and coverage | Uniform sampling can miss information; keyframe selection under a fixed token budget raises video QA accuracy | Abstract |
| brkic2025 | Brkić et al. (2025) | Preprint | Benchmark of sampling strategies | Small-VLM results depend on the sampling strategy; the best strategy varies by dataset and task | Abstract |

## 6. How frames are used in engagement and affect recognition

| Key | Work | Frames reaching the model | Checked |
| :-- | :--- | :--- | :--- |
| whitehill2014 | Whitehill et al. (2014) | Single frames; clip label from the frame average | Abstract |
| kaur2018 | Kaur et al. (2018) | Segments as instances in multiple-instance learning; localizes engaging parts | Abstract |
| meng2019 | Meng et al. (2019), FAN (ICIP 2019) | All frames weighted by learned attention (facial expression in video) | Abstract and listing |
| singh2023 | Singh et al. (2023) | All frames, pooled into uniform segments (mean and SD) | Full text |
| abedi2021 | Abedi & Khan (2021) | 50 down-sampled frames per clip | Full text |
| abedi2024bag | Abedi et al. (2024), Multimedia Systems 30(1) | Per-segment states counted as a bag, order ignored; up to 66.58% on DAiSEE; shuffling states barely changed predictions | Abstract |
| das2024 | Das & Dev (2024), Applied Intelligence 54(2) | Frame-level labels via transfer from the image-based WACV dataset to DAiSEE | Abstract |
| resurreccion2024 | Resurreccion (2024), DLSU MS thesis (adviser: J. Azcarraga) | **Two frame-selection methods, Targeted and Changepoint, 3 frames per clip**, on DAiSEE academic emotions. Changepoint had a slight edge for dynamic emotions (engagement, frustration); Targeted was good across all, especially static (boredom, confusion). KNN and CNN were best | Abstract (repository page) |
| sityar2026icce | Preliminary study | SME vs. 3/5/7-Changepoint on EngageNet (threshold 3) | Your own work |
| abedi2024stgcn | Abedi & Khan (2024) | Every frame; sparser uniform rates (every 2–16 frames) lowered validation accuracy slightly | arXiv v2 Table 3 |

## 6b. Temporal representation of frames (§2.7, added 14 Nov)

| Key | Work | Venue | What it shows | Used for | Checked |
| :-- | :--- | :--- | :--- | :--- | :--- |
| karpathy2014 | Karpathy et al. (2014) | CVPR 2014, 1725–1732 | Early, late and slow fusion of frames. Best spatio-temporal net 60.9% vs. single-frame 59.3% (Sports-1M) | Temporal modeling gains can be modest; late fusion ≈ concatenating frame features | Crossref + abstract |
| ng2015 | Ng et al. (2015) | CVPR 2015, 4694–4702 | Max-pooling frame features vs. LSTM over frames: 71.7% vs. 72.1% video hit-at-1 with 30 frames (Table 3). Average pooling "failed to learn effectively" in their end-to-end setup | Pooling ≈ sequence model | Full text (arXiv) |
| wang2016 | TSN (2016) | ECCV 2016 | Consensus: average beat max and weighted average overall (Table 3). Stacked RGB difference between consecutive frames as an input describing appearance change / motion; RGB + RGB difference reached 87.3% | Precedent for averaging and for "change" | Full text (arXiv) |
| junejo2011 | Junejo et al. (2011) | IEEE TPAMI 33(1), 172–185 | Temporal self-similarity matrices; stable across camera viewpoints | Precedent for "self-similarity" | Crossref + abstract |

Not cited: a 2025 Neural Computing and Applications paper (doi 10.1007/s00521-025-11317-z), reportedly with a landmark-differencing ablation for engagement. It is paywalled and unverified.

## 7. Philippine context (Chapter 1)

| Key | Source | Use | Checked |
| :-- | :--- | :--- | :--- |
| ched2020 | CHED Memorandum Order No. 4, s. 2020, *Guidelines on the Implementation of Flexible Learning* | Philippine HEIs adopted flexible learning, including online and blended delivery | Title and issuer from CHED's site. Delivery modes from secondary summaries; **read the CMO itself.** |

## Core must-read papers (the panel may ask about these)

1. **Singh et al. (2023), EngageNet.** §3 (data, annotation) and §4 (baselines). Your dataset, and the baselines you're positioned against.
2. **Resurreccion (2024).** Ch. 3–4. The closest prior work, from your adviser's group. Know exactly how "Targeted" and "Changepoint" were defined, and whether a random condition existed.
3. **Whitehill et al. (2014).** The frame-average result (r = 0.85).
4. **Gupta et al. (2016), DAiSEE.** Table 2 (imbalance) and Table 3 (benchmarks).
5. **Zhao et al. (2025), RAER / CLIP-CAER.** The panel's suggested reading. Know why it is academic emotion, not engagement.
6. **Teotia et al. (2024) and Goyal et al. (2026).** Your R2 answer: what VLMs can and cannot do for engagement.
7. **Brkić et al. (2025).** Frame sampling changes VLM results (also audit item B8).
8. **Abedi et al. (2024), Bag of States.** Evidence that order may not matter, which bears on LSTM vs. MLP.
9. **Wu et al. (2024), CMOSE.** Label-quality critique of DAiSEE.
