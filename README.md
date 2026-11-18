# Awesome Comics & Manga AI

A curated, maintained map of research on comics in computer vision, language and graphics: manga, manhwa, manhua, webtoons, bandes dessinées, comic strips, graphic novels and single-panel cartoons. It covers how models read, search, translate, describe, create and reason about them, and the datasets, benchmarks and tools behind that work. It lists work from top venues and their workshops, the datasets the field builds on, and the newest preprints ([inclusion rule](#inclusion-rule)).

**119 papers** in 17 sections, 30 of them from 2025–2026. Every entry is checked against arXiv, Crossref or the venue's own pages, and a monthly arXiv sweep finds new work ([how the list stays current](#how-the-list-stays-current)). Browse and search it on the [site](https://sochastic.me/awesome-comics-ai/).

## Contents

- [Surveys and overviews](#surveys-and-overviews) (3)
- [Datasets](#datasets) (10)
- [Understanding and reasoning](#understanding-and-reasoning) (17)
- [Page and panel analysis](#page-and-panel-analysis) (14)
- [Text, balloons and speakers](#text-balloons-and-speakers) (9)
- [Character identification](#character-identification) (3)
- [Retrieval and recommendation](#retrieval-and-recommendation) (5)
- [Translation and localization](#translation-and-localization) (1)
- [Accessibility](#accessibility) (1)
- [Comic and manga generation](#comic-and-manga-generation) (11)
- [Colorization, screentones and line art](#colorization-screentones-and-line-art) (14)
- [Restoration, vectorization and editing](#restoration-vectorization-and-editing) (5)
- [Animation, sound and motion comics](#animation-sound-and-motion-comics) (5)
- [Comics as a probe for models](#comics-as-a-probe-for-models) (1)
- [Computational comics studies](#computational-comics-studies) (4)
- [Comics in HCI, education and data storytelling](#comics-in-hci-education-and-data-storytelling) (9)
- [Adjacent: story visualization](#adjacent-story-visualization) (7)
- [Tools and models](#tools-and-models)
- [Workshops and competitions](#workshops-and-competitions)
- [Related lists](#related-lists)
- [Inclusion rule](#inclusion-rule)
- [How the list stays current](#how-the-list-stays-current)
- [Contributing](#contributing)

## Surveys and overviews

Reviews of the field and of comics research in computer science.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2024 | arXiv | One missing piece in Vision and Language: A Survey on Comics Understanding | [arXiv](https://arxiv.org/abs/2409.09502) |
| 2019 | Topics in Cognitive Science | Computational Approaches to Comics Analysis | [paper](https://doi.org/10.1111/tops.12476) |
| 2018 | J. Imaging | A survey of comics research in computer science | [paper](https://doi.org/10.3390/jimaging4070087) · [arXiv](https://arxiv.org/abs/1804.05490) |

## Datasets

Annotated collections of pages, panels, text and characters. Benchmarks built for vision-language models are in the next section.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2026 | ICML Workshops | Manga109-v2026: Revisiting Manga109 Annotations for Modern Manga Understanding | [paper](https://icml.cc/virtual/2026/74741) · [arXiv](https://arxiv.org/abs/2605.21182) |
| 2025 | CVPR | Advancing Manga Analysis: Comprehensive Segmentation Annotations for the Manga109 Dataset | [paper](https://doi.org/10.1109/cvpr52734.2025.00829) |
| 2025 | EMNLP | ComicScene154: A Scene Dataset for Comic Analysis | [paper](https://doi.org/10.18653/v1/2025.emnlp-main.1608) · [arXiv](https://arxiv.org/abs/2508.16190) |
| 2024 | ICDAR Workshops | Comics Datasets Framework: Mix of Comics datasets for detection benchmarking | [paper](https://doi.org/10.1007/978-3-031-70645-5_11) · [arXiv](https://arxiv.org/abs/2407.03540) |
| 2024 | NeurIPS | CoMix: A Comprehensive Benchmark for Multi-Task Comic Understanding | [paper](https://doi.org/10.52202/079017-4470) · [arXiv](https://arxiv.org/abs/2407.03550) · [code](https://github.com/emanuelevivoli/CoMix) |
| 2024 | ECCV Workshops | Unlocking Comics: The AI4VA Dataset for Visual Understanding | [paper](https://doi.org/10.1007/978-3-031-92808-6_10) · [arXiv](https://arxiv.org/abs/2410.20459) · [code](https://github.com/IVRL/AI4VA) |
| 2022 | IJDAR | BCBId: First Bangla Comic Dataset and Its Applications | [paper](https://doi.org/10.1007/s10032-022-00412-9) |
| 2022 | DICTA | ComicLib: A New Large-Scale Comic Dataset for Sketch Understanding | [paper](https://doi.org/10.1109/dicta56598.2022.10034579) |
| 2022 | DataverseNL | The Visual Language Research Corpus (VLRC) Project | [paper](https://doi.org/10.34894/LWMZ7G) |
| 2020 | IEEE MultiMedia | Building a Manga Dataset "Manga109" with Annotations for Multimedia Applications | [paper](https://doi.org/10.1109/mmul.2020.2987895) · [arXiv](https://arxiv.org/abs/2005.04425) |

## Understanding and reasoning

Reading comics with vision-language models and multimodal transformers, including question answering, panel cloze, narrative understanding, humor and the benchmarks that measure them.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2026 | EACL | CHROMIC: Chronological Reasoning Across Multi-Panel Comics | [paper](https://doi.org/10.18653/v1/2026.eacl-long.205) |
| 2026 | Findings of EACL | MangaVQA and MangaLMM: A Benchmark and Specialized Model for Multimodal Manga Understanding | [paper](https://doi.org/10.18653/v1/2026.findings-eacl.284) · [arXiv](https://arxiv.org/abs/2505.20298) |
| 2026 | Findings of EMNLP | ManGo: Manga Active Narrative Grounding Optimization | [paper](https://doi.org/10.18653/2026.findings-emnlp.753) · [arXiv](https://arxiv.org/abs/2608.29865) |
| 2026 | Findings of EMNLP | Memes-as-Replies: Can Models Select Humorous Manga Panel Responses? | [paper](https://doi.org/10.18653/2026.findings-emnlp.2076) · [arXiv](https://arxiv.org/abs/2602.15842) |
| 2025 | ICDAR | ComicsPAP: understanding comic strips by picking the correct panel | [paper](https://doi.org/10.1007/978-3-032-04614-7_19) · [arXiv](https://arxiv.org/abs/2503.08561) |
| 2025 | ICCV | From Panels to Prose: Generating Literary Narratives from Comics | [paper](https://doi.org/10.1109/iccv51701.2025.02030) · [arXiv](https://arxiv.org/abs/2503.23344) |
| 2025 | Findings of EMNLP | Humor in Pixels: Benchmarking Large Multimodal Models Understanding of Online Comics | [paper](https://doi.org/10.18653/v1/2025.findings-emnlp.755) · [arXiv](https://arxiv.org/abs/2509.12248) |
| 2025 | IEEE MultiMedia | MangaUB: A Manga Understanding Benchmark for Large Multimodal Models | [paper](https://doi.org/10.1109/mmul.2025.3550451) · [arXiv](https://arxiv.org/abs/2407.19034) |
| 2025 | ICCV Workshops | Re:Verse -- Can Your VLM Read a Manga? | [paper](https://doi.org/10.1109/iccvw69036.2025.00398) · [arXiv](https://arxiv.org/abs/2508.08508) |
| 2024 | ECCV Workshops | ComiCap: A VLMs pipeline for dense captioning of Comic Panels | [paper](https://doi.org/10.1007/978-3-031-92808-6_4) · [arXiv](https://arxiv.org/abs/2409.16159) |
| 2024 | ICDAR Workshops | ComicBERT: A Transformer Model and Pre-training Strategy for Contextual Understanding in Comics | [paper](https://doi.org/10.1007/978-3-031-70645-5_16) · [code](https://github.com/gsoykan/comicbert) |
| 2024 | NeurIPS | Cracking the Code of Juxtaposition: Can AI Models Understand the Humorous Contradictions | [paper](https://doi.org/10.52202/079017-1494) · [arXiv](https://arxiv.org/abs/2405.19088) |
| 2024 | ICDAR Workshops | Investigating Neural Networks and Transformer Models for Enhanced Comic Decoding | [paper](https://doi.org/10.1007/978-3-031-70645-5_10) |
| 2024 | ICDAR | Multimodal Transformer for Comics Text-Cloze | [paper](https://doi.org/10.1007/978-3-031-70552-6_8) · [arXiv](https://arxiv.org/abs/2403.03719) |
| 2023 | Findings of EMNLP | M2C: Towards Automatic Multimodal Manga Complement | [paper](https://doi.org/10.18653/v1/2023.findings-emnlp.661) · [arXiv](https://arxiv.org/abs/2310.17130) |
| 2017 | CVPR | The Amazing Mysteries of the Gutter: Drawing Inferences Between Panels in Comic Book Narratives | [paper](https://doi.org/10.1109/cvpr.2017.686) · [arXiv](https://arxiv.org/abs/1611.05118) · [code](https://github.com/miyyer/comics) |
| 2016 | MANPU | Designing a Question-Answering System for Comic Contents | [paper](https://doi.org/10.1145/3011549.3011554) |

## Page and panel analysis

Detection and segmentation of panels, characters and faces, reading order, layout, depth, pose, genre and style.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2025 | ICCV Workshops | CoSMo: A Multimodal Transformer for Page Stream Segmentation in Comic Books | [paper](https://doi.org/10.1109/iccvw69036.2025.00778) · [arXiv](https://arxiv.org/abs/2507.10053) |
| 2023 | CVPR Workshops | Dense Multitask Learning to Reconfigure Comics | [paper](https://doi.org/10.1109/cvprw59228.2023.00598) · [arXiv](https://arxiv.org/abs/2307.08071) |
| 2023 | TIP | Panel-Page-Aware Comic Genre Understanding | [paper](https://doi.org/10.1109/tip.2023.3270105) |
| 2022 | WACV | Estimating Image Depth in the Comics Domain | [paper](https://doi.org/10.1109/wacv51458.2022.00118) · [arXiv](https://arxiv.org/abs/2110.03575) · [code](https://github.com/IVRL/ComicsDepth) |
| 2022 | ICPR Workshops | Towards Content-Aware Pixel-Wise Comic Panel Segmentation | [paper](https://doi.org/10.1007/978-3-031-37742-6_1) |
| 2021 | ICDAR | ICDAR 2021 Competition on Multimodal Emotion Recognition on Comics Scenes | [paper](https://doi.org/10.1007/978-3-030-86337-1_51) |
| 2019 | ICDAR Workshops | CNN based Extraction of Panels/Characters from Bengali Comic Book Page Images | [paper](https://doi.org/10.1109/icdarw.2019.00012) · [arXiv](https://arxiv.org/abs/1910.09233) |
| 2019 | ICDAR Workshops | What Do We Expect from Comic Panel Extraction? | [paper](https://doi.org/10.1109/icdarw.2019.00013) |
| 2018 | CVPR | Cross-Domain Weakly-Supervised Object Detection through Progressive Domain Adaptation | [paper](https://doi.org/10.1109/cvpr.2018.00525) · [arXiv](https://arxiv.org/abs/1803.11365) · [code](https://github.com/naoto0804/cross-domain-detection) |
| 2017 | ICDAR | A Faster R-CNN Based Method for Comic Characters Face Detection | [paper](https://doi.org/10.1109/icdar.2017.178) |
| 2017 | ICDAR | Comic Story Analysis Based on Genre Classification | [paper](https://doi.org/10.1109/icdar.2017.293) |
| 2017 | ICDAR | Histogram of Exclamation Marks and Its Application for Comics Analysis | [paper](https://doi.org/10.1109/icdar.2017.294) |
| 2016 | MANPU | Pose Estimation of Anime/Manga Characters: A Case for Synthetic Data | [paper](https://doi.org/10.1145/3011549.3011552) |
| 2014 | ACM MM | Line-Based Drawing Style Description for Manga Classification | [paper](https://doi.org/10.1145/2647868.2654962) |

## Text, balloons and speakers

Text detection and recognition, speech balloons, onomatopoeia, speaker attribution, transcription and dialogue.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2024 | ICDAR Workshops | A Comprehensive Gold Standard and Benchmark for Comics Text Detection and Recognition | [paper](https://doi.org/10.1007/978-3-031-70645-5_12) · [arXiv](https://arxiv.org/abs/2212.14674) · [code](https://github.com/gurkansoykan/comic-text-detection-benchmark) |
| 2024 | ICME | Manga109Dialog: A Large-scale Dialogue Dataset for Comics Speaker Detection | [paper](https://doi.org/10.1109/icme57554.2024.10687709) · [arXiv](https://arxiv.org/abs/2306.17469) · [code](https://github.com/manga109/public-annotations) |
| 2024 | ICDAR Workshops | Spatially Augmented Speech Bubble to Character Association via Comic Multi-task Learning | [paper](https://doi.org/10.1007/978-3-031-70645-5_15) · [code](https://github.com/gsoykan/spatially_augmented_comic_mtl) |
| 2024 | CVPR | The Manga Whisperer: Automatically Generating Transcriptions for Comics | [paper](https://doi.org/10.1109/cvpr52733.2024.01232) · [arXiv](https://arxiv.org/abs/2401.10224) · [code](https://github.com/ragavsachdeva/magi) |
| 2023 | ACL | Multimodal Persona Based Generation of Comic Dialogs | [paper](https://doi.org/10.18653/v1/2023.acl-long.791) |
| 2022 | ECCV | COO: Comic Onomatopoeia Dataset for Recognizing Arbitrary or Truncated Texts | [paper](https://doi.org/10.1007/978-3-031-19815-1_16) · [arXiv](https://arxiv.org/abs/2207.04675) · [code](https://github.com/ku21fan/COO-Comic-Onomatopoeia) |
| 2020 | ECCV Workshops | Unconstrained Text Detection in Manga: a New Dataset and Baseline | [paper](https://doi.org/10.1007/978-3-030-67070-2_38) · [arXiv](https://arxiv.org/abs/2009.04042) · [code](https://github.com/juvian/Manga-Text-Segmentation) |
| 2019 | ICDAR | Deep CNN-based Speech Balloon Detection and Segmentation for Comic Books | [paper](https://doi.org/10.1109/icdar.2019.00200) · [arXiv](https://arxiv.org/abs/1902.08137) |
| 2015 | ICDAR | Speech Balloon and Speaker Association for Comics and Manga Understanding | [paper](https://doi.org/10.1109/icdar.2015.7333782) |

## Character identification

Recognizing, re-identifying and clustering characters across panels, pages and chapters.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2026 | NeurIPS | Re:Cognize -- A Framework For Open-Set Comic Character Re-Identification | [arXiv](https://arxiv.org/abs/2609.34032) |
| 2024 | ACM MM | Zero-Shot Character Identification and Speaker Prediction in Comics via Iterative Multimodal Fusion | [paper](https://doi.org/10.1145/3664647.3681659) · [arXiv](https://arxiv.org/abs/2404.13993) |
| 2021 | ICDAR | Manga-MMTL: Multimodal Multitask Transfer Learning for Manga Character Analysis | [paper](https://doi.org/10.1007/978-3-030-86331-9_27) |

## Retrieval and recommendation

Finding pages, panels and characters by sketch, text or example, and recommending titles.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2017 | ICDAR | Sketch-Based Manga Retrieval Using Deep Features | [paper](https://doi.org/10.1109/icdar.2017.291) |
| 2017 | ICDAR | Using Posters to Recommend Anime and Mangas in a Cold-Start Scenario | [paper](https://doi.org/10.1109/icdar.2017.287) · [arXiv](https://arxiv.org/abs/1709.01584) |
| 2016 | MTAP | Sketch-based Manga Retrieval using Manga109 Dataset | [paper](https://doi.org/10.1007/s11042-016-4020-z) · [arXiv](https://arxiv.org/abs/1510.04389) |
| 2011 | ACM MM | Automatic Preview Generation of Comic Episodes for Digitized Comic Search | [paper](https://doi.org/10.1145/2072298.2072047) |
| 2011 | ICDAR | Similar Manga Retrieval Using Visual Vocabulary Based on Regions of Interest | [paper](https://doi.org/10.1109/icdar.2011.217) |

## Translation and localization

Machine translation of comics with the page in view, from balloon text to onomatopoeia and visual adaptation.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2021 | AAAI | Towards Fully Automated Manga Translation | [paper](https://doi.org/10.1609/aaai.v35i14.17537) · [arXiv](https://arxiv.org/abs/2012.14271) |

## Accessibility

Making comics readable for blind and low-vision readers, from descriptions to accessible readers.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2024 | ICDAR Workshops | Toward accessible comics for blind and low vision readers | [paper](https://doi.org/10.1007/978-3-031-70645-5_13) · [arXiv](https://arxiv.org/abs/2407.08248) |

## Comic and manga generation

Creating comics from stories, scripts, photographs or videos, with layout, characters and lettering.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2026 | arXiv | Investigating Social Bias in Narrative Image Generation | [arXiv](https://arxiv.org/abs/2608.01780) |
| 2026 | EMNLP | MangaFlow: An End-to-End Agentic Framework for Controllable Story to Manga Generation | [paper](https://doi.org/10.18653/2026.emnlp-main.263) · [arXiv](https://arxiv.org/abs/2605.28173) |
| 2026 | CHI EA | One Kiss: Emojis as Agents of Genre Flux in Generative Comics | [paper](https://doi.org/10.1145/3772363.3798758) · [arXiv](https://arxiv.org/abs/2603.16359) |
| 2025 | CVPR | DiffSensei: Bridging Multi-Modal LLMs and Diffusion Models for Customized Manga Generation | [paper](https://doi.org/10.1109/cvpr52734.2025.02671) · [arXiv](https://arxiv.org/abs/2412.07589) |
| 2024 | ECAI Workshops | Collaborative Comic Generation: Integrating Visual Narrative Theories with AI Models for Enhanced Creativity | [paper](https://ceur-ws.org/Vol-3810/paper8.pdf) · [arXiv](https://arxiv.org/abs/2409.17263) |
| 2022 | SIGGRAPH Asia | WebtoonMe: A Data-Centric Approach for Full-Body Portrait Stylization | [paper](https://doi.org/10.1145/3550340.3564226) · [arXiv](https://arxiv.org/abs/2210.10335) |
| 2021 | AAAI | MangaGAN: Unpaired Photo-to-Manga Translation Based on The Methodology of Manga Drawing | [paper](https://doi.org/10.1609/aaai.v35i3.16364) · [arXiv](https://arxiv.org/abs/2004.10634) |
| 2015 | TMM | Content-Aware Video2Comics With Manga-Style Layout | [paper](https://doi.org/10.1109/tmm.2015.2474263) |
| 2012 | ACM TOG | Automatic Stylistic Manga Layout | [paper](https://doi.org/10.1145/2366145.2366160) |
| 2012 | TMM | Movie2Comics: Towards a Lively Video Content Presentation | [paper](https://doi.org/10.1109/tmm.2012.2187181) |
| 2012 | TMM | Scalable Comic-like Video Summaries and Layout Disturbance | [paper](https://doi.org/10.1109/tmm.2012.2192917) |

## Colorization, screentones and line art

Tools for the drawing itself, including colorization, screentone and shading, line extraction and line-art correspondence.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2026 | CVPR | Region-Wise Correspondence Prediction between Manga Line Art Images | [paper](https://cvpr.thecvf.com/virtual/2026/poster/39720) · [arXiv](https://arxiv.org/abs/2509.09501) · [code](https://github.com/liyingxuan1012/r2r-lineart-correspondence) |
| 2025 | SIGGRAPH | Cobra: Efficient Line Art COlorization with BRoAder References | [paper](https://doi.org/10.1145/3721238.3730660) · [arXiv](https://arxiv.org/abs/2504.12240) · [project](https://zhuang2002.github.io/Cobra/) |
| 2025 | CVPR | MangaNinja: Line Art Colorization with Precise Reference Following | [paper](https://doi.org/10.1109/cvpr52734.2025.00532) · [arXiv](https://arxiv.org/abs/2501.08332) · [project](https://johanan528.github.io/MangaNinjia/) |
| 2025 | ICCV Workshops | OnomatoGen: Onomatopoeia Generation with the Alpha-Channel in Manga | [arXiv](https://arxiv.org/abs/2509.24331) · [project](https://comiq-iccv25.github.io) |
| 2024 | TVCG | Shading-Guided Manga Screening from Reference | [paper](https://doi.org/10.1109/tvcg.2023.3282223) |
| 2022 | CHI | FlatMagic: Improving Flat Colorization through AI-driven Design for Digital Comic Professionals | [paper](https://doi.org/10.1145/3491102.3502075) |
| 2021 | CVPR | Generating Manga from Illustrations via Mimicking Manga Creation Workflow | [paper](https://doi.org/10.1109/cvpr46437.2021.00559) · [code](https://github.com/lllyasviel/MangaFilter) |
| 2021 | SIGGRAPH Asia | Interactive Manga Colorization with Fast Flat Coloring | [paper](https://doi.org/10.1145/3476124.3488628) |
| 2020 | ACM TOG | Manga Filling Style Conversion with Screentone Variational Autoencoder | [paper](https://doi.org/10.1145/3414685.3417873) |
| 2017 | ICDAR | cGAN-based Manga Colorization Using a Single Training Image | [paper](https://doi.org/10.1109/icdar.2017.295) · [arXiv](https://arxiv.org/abs/1706.06918) · [code](https://github.com/ryanliwag/cGan-Based-Manga-Colorization-using-1-training-image) |
| 2017 | SIGGRAPH Asia Technical Briefs | Comicolorization: Semi-Automatic Manga Colorization | [arXiv](https://arxiv.org/abs/1706.06759) · [code](https://github.com/DwangoMediaVillage/Comicolorization) |
| 2017 | ACM TOG | Deep Extraction of Manga Structural Lines | [paper](https://doi.org/10.1145/3072959.3073675) · [code](https://github.com/ljsabc/MangaLineExtraction_PyTorch) |
| 2014 | SIGGRAPH Asia | Reference-based Manga Colorization by Graph Correspondence Using Quadratic Programming | [paper](https://doi.org/10.1145/2669024.2669037) |
| 2006 | ACM TOG | Manga Colorization | [paper](https://doi.org/10.1145/1141911.1142017) |

## Restoration, vectorization and editing

Inpainting, super-resolution, dewarping, vectorization, retargeting and editing of comic images.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2021 | SIGGRAPH Asia | Comic Image Inpainting via Distance Transform | [paper](https://doi.org/10.1145/3478512.3488607) |
| 2021 | CVPR | Exploiting Aliasing for Manga Restoration | [paper](https://doi.org/10.1109/cvpr46437.2021.01320) · [arXiv](https://arxiv.org/abs/2105.06830) · [code](https://github.com/msxie92/MangaRestoration) |
| 2021 | ACM TOG | Seamless Manga Inpainting with Semantics Awareness | [paper](https://doi.org/10.1145/3450626.3459822) |
| 2017 | TVCG | Manga Vectorization and Manipulation with Procedural Simple Screentone | [paper](https://doi.org/10.1109/tvcg.2016.2525774) |
| 2011 | ICDAR | Recognizing Text Elements for SVG Comic Compression and Its Novel Applications | [paper](https://doi.org/10.1109/icdar.2011.267) |

## Animation, sound and motion comics

Bringing pages to life with motion, voices, speech and music.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2026 | arXiv | Manga2Animate: An Agentic Framework for Faithful Manga Animation with Script and Storyboard Planning | [arXiv](https://arxiv.org/abs/2610.26851) |
| 2025 | IUI | DancingBoard: Streamlining the Creation of Motion Comics to Enhance Narratives | [paper](https://doi.org/10.1145/3708359.3712167) · [arXiv](https://arxiv.org/abs/2503.09061) |
| 2021 | ICDAR | C2VNet: A Deep Learning Framework Towards Comic Strip to Audio-Visual Scene Synthesis | [paper](https://doi.org/10.1007/978-3-030-86331-9_11) · [code](https://github.com/gesstalt/IMCDB) |
| 2019 | ACM TOG | Comic-Guided Speech Synthesis | [paper](https://doi.org/10.1145/3355089.3356487) · [project](https://bitwangyujia.github.io/research/project/comic2speech.html) |
| 2017 | TMM | Dynamic Manga: Animating Still Manga via Camera Movement | [paper](https://doi.org/10.1109/tmm.2016.2609415) |

## Comics as a probe for models

Work that uses comic strips to study how multimodal models attend, reason and stay safe.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2026 | TIFS | Sequential Comics for Jailbreaking Multimodal Large Language Models via Structured Visual Storytelling | [paper](https://doi.org/10.1109/tifs.2026.3734766) · [arXiv](https://arxiv.org/abs/2510.15068) |

## Computational comics studies

Large-scale and quantitative analysis of comics as a medium, including layout, genre, narrative structure and reader response.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2026 | arXiv | Studying Comics at Scale with Artificial Intelligence: The PAGE Framework and Three Studies of American Comics and Japanese Manga | [arXiv](https://arxiv.org/abs/2610.13840) |
| 2019 | ICDAR Workshops | Analysis Based on Distributed Representations of Various Parts Images in Four-Scene Comics Story Dataset | [paper](https://doi.org/10.1109/icdarw.2019.00014) |
| 2017 | ICDAR | Story Pattern Analysis Based on Scene Order Information in Four-Scene Comics | [paper](https://doi.org/10.1109/icdar.2017.296) |
| 2016 | MANPU | Manga Content Analysis Using Physiological Signals | [paper](https://doi.org/10.1145/3011549.3011555) |

## Comics in HCI, education and data storytelling

Comics as an interface, a teaching tool and a form for explaining data, and tools that support comic creators.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2026 | arXiv | Drawing the Line: Where AI Guidance and Human Creativity Meet in Emotion-Driven Comic Storyboarding | [arXiv](https://arxiv.org/abs/2610.09155) |
| 2026 | arXiv | Onomatopoeia Cursor: Verbal Mirroring of Mouse Movement with Comic-Style Lettering | [arXiv](https://arxiv.org/abs/2609.13184) |
| 2025 | TVCG | DG Comics: Semi-Automatically Authoring Graph Comics for Dynamic Graphs | [paper](https://doi.org/10.1109/tvcg.2024.3456340) · [arXiv](https://arxiv.org/abs/2408.04874) |
| 2025 | NeurIPS Creative AI | Panel-by-Panel Souls: A Performative Workflow for Expressive Faces in AI-Assisted Manga Creation | [paper](https://papers.neurips.cc/paper_files/paper/2025/hash/a3386597cce5ce1b2fe0f5c5c5a531db-Abstract-Creative_AI_Track.html) · [arXiv](https://arxiv.org/abs/2511.16038) |
| 2023 | TVCG | ChartStory: Automated Partitioning, Layout, and Captioning of Charts into Comic-Style Narratives | [paper](https://doi.org/10.1109/tvcg.2021.3114211) · [arXiv](https://arxiv.org/abs/2103.03996) |
| 2023 | SIGCSE | Developing Comic-based Learning Toolkits for Teaching Computing to Elementary School Learners | [paper](https://doi.org/10.1145/3545947.3576272) |
| 2022 | UIST | CodeToon: Story Ideation, Auto Comic Generation, and Structure Mapping for Code-Driven Storytelling | [paper](https://doi.org/10.1145/3526113.3545617) · [arXiv](https://arxiv.org/abs/2208.12981) |
| 2022 | TVCG | Interactive Data Comics | [paper](https://doi.org/10.1109/tvcg.2021.3114849) |
| 2021 | SIGCSE | Using Comics to Introduce and Reinforce Programming Concepts in CS1 | [paper](https://doi.org/10.1145/3408877.3432465) |

## Adjacent: story visualization

Generating consistent image sequences from stories, the line of work that comic generation builds on.

| Year | Venue | Title | Links |
|:---:|:---|:---|:---|
| 2024 | WACV | Synthesizing Coherent Story with Auto-Regressive Latent Diffusion Models | [paper](https://doi.org/10.1109/wacv57701.2024.00290) · [arXiv](https://arxiv.org/abs/2211.10950) · [code](https://github.com/xichenpan/ARLDM) |
| 2023 | CVPR | Make-A-Story: Visual Memory Conditioned Consistent Story Generation | [paper](https://doi.org/10.1109/cvpr52729.2023.00246) |
| 2022 | EMNLP | Character-Centric Story Visualization via Visual Planning and Token Alignment | [paper](https://doi.org/10.18653/v1/2022.emnlp-main.565) · [arXiv](https://arxiv.org/abs/2210.08465) · [code](https://github.com/PlusLabNLP/VP-CSV) |
| 2022 | ECCV | StoryDALL-E: Adapting Pretrained Text-to-Image Transformers for Story Continuation | [paper](https://doi.org/10.1007/978-3-031-19836-6_5) · [arXiv](https://arxiv.org/abs/2209.06192) · [code](https://github.com/adymaharana/storydalle) |
| 2021 | NAACL | Improving Generation and Evaluation of Visual Stories via Semantic Consistency | [paper](https://doi.org/10.18653/v1/2021.naacl-main.194) · [arXiv](https://arxiv.org/abs/2105.10026) · [code](https://github.com/adymaharana/StoryViz) |
| 2021 | EMNLP | Integrating Visuospatial, Linguistic and Commonsense Structure intoStory Visualization | [paper](https://doi.org/10.18653/v1/2021.emnlp-main.543) · [arXiv](https://arxiv.org/abs/2110.10834) · [code](https://github.com/adymaharana/VLCStoryGan) |
| 2019 | CVPR | StoryGAN: A Sequential Conditional GAN for Story Visualization | [paper](https://doi.org/10.1109/cvpr.2019.00649) · [arXiv](https://arxiv.org/abs/1812.02784) · [code](https://github.com/yitong91/StoryGAN) |

## Tools and models

| Tool | What it does | Links |
|:---|:---|:---|
| Magi | Detects panels, text and characters on manga pages, clusters characters and writes a chapter transcript with speaker names. | [code](https://github.com/ragavsachdeva/magi) |
| manga-ocr | Optical character recognition for Japanese manga text, vertical or horizontal, with or without furigana. | [code](https://github.com/kha-white/manga-ocr) |
| mokuro | Turns manga pages into a browser reader with selectable Japanese text, using manga-ocr. | [code](https://github.com/kha-white/mokuro) |
| comic-text-detector | Text detection and segmentation for manga and comics. | [code](https://github.com/dmMaze/comic-text-detector) |
| BallonsTranslator | Computer-aided comic and manga translation with machine translation and image and text editing. | [code](https://github.com/dmMaze/BallonsTranslator) |
| manga-image-translator | Detects, translates and re-letters the text in manga and other images. | [code](https://github.com/zyddnys/manga-image-translator) |
| Kumiko | Cuts comic pages into panels and orders them for reading. | [code](https://github.com/njean42/kumiko) |
| manga109api | A Python API for reading the Manga109 annotations. | [code](https://github.com/manga109/manga109api) |
| Manga109 public annotations | Additional annotations of Manga109 released by the community, such as onomatopoeia and dialogue. | [code](https://github.com/manga109/public-annotations) |
| CoMix | A framework that unifies comics datasets and annotations for detection, captioning and other tasks. | [code](https://github.com/emanuelevivoli/CoMix) |
| Open Mantra dataset | A manga translation evaluation set with Japanese, English and Chinese text. | [code](https://github.com/mantra-inc/open-mantra-dataset) |

## Workshops and competitions

- **MANPU**: The IAPR International Workshop on coMics ANalysis, Processing and Understanding, first held with ICPR 2016; its seventh edition ran with ICPR 2026 in Lyon. [proceedings on DBLP](https://dblp.org/search?q=MANPU)
- **AI4VA at ECCV 2024**: The AI for Visual Arts workshop and challenges, with depth, segmentation and saliency tracks on Franco-Belgian comics. [workshop page](https://sites.google.com/view/ai4vaeccv2024)
- **ICDAR 2021 competition on multimodal emotion recognition on comics scenes**: A shared task on recognizing emotions in comic panels from the image and the text together. [paper](https://doi.org/10.1007/978-3-030-86337-1_51)

## Related lists

- [Awesome Comics Understanding](https://github.com/emanuelevivoli/awesome-comics-understanding): the companion list of the 2024 comics-understanding survey by Vivoli et al., organized by its layers of understanding.
- [AwesomeAnimeResearch](https://github.com/SerialLain3170/AwesomeAnimeResearch): a large, active list of anime and manga research, strongest on generation, colorization and illustration.
- [awesome-acg-machine-learning](https://github.com/dimpurr/awesome-acg-machine-learning): an earlier list of machine learning for anime, comics and games.

## Inclusion rule

A paper is in the list when it meets one of these conditions:

1. It appeared at a conference or in a journal ranked **A\* or A by CORE** (CORE2023 for conferences, CORE2020 for journals). `data/venues.yaml` gives every venue's rank.
2. It appeared at a **workshop** of any conference, or in a peer-reviewed track of an A\* or A conference (Findings, technical briefs, extended abstracts).
3. It is a **dataset or benchmark paper**, at any published venue.
4. It is an **arXiv preprint** whose first version is at most 4 months old. After that, it stays only if a venue that meets conditions 1–3 has published it.

Surveys follow their own rule: a survey of comics is listed when it is peer-reviewed at any venue, or when it is a preprint with at least 10 citations. The four-month window does not apply to surveys.

Verified papers that do not meet the rule are kept, with the reason, in `data/not_included.yaml`, so a later publication brings them back.

## How the list stays current

- `data/papers.yaml` is the single source. `scripts/build.py` writes this README and the site from it, so the two never drift.
- `scripts/verify.py` checks every entry: required fields, a known section, no duplicate titles, and, with `--online`, that each arXiv id resolves to the listed title.
- A monthly GitHub Action runs `scripts/refresh.py`, which promotes preprints that have been published, retires those past the 4-month window and brings back retired ones published since, and opens a pull request with the change.
- The same Action runs `scripts/arxiv_sweep.py` and opens an issue with the new arXiv papers whose title or abstract names comics, manga or webtoons. A maintainer adds the ones that belong.

## Contributing

Additions and corrections are welcome. Add or edit an entry in `data/papers.yaml`, run `python scripts/build.py`, and open a pull request; [CONTRIBUTING.md](CONTRIBUTING.md) gives the fields and the scope. A paper belongs here when comics are its subject or its main test bed.

## License

[CC0 1.0](LICENSE): to the extent possible under law, the maintainers waive all copyright to this list.
