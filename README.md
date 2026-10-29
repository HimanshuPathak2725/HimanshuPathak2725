# Hi, I'm Himanshu Pathak

I'm a B.Tech CSE student and RL Engineering Intern at Wootzapp, interested in reinforcement learning, LLM post-training, and the evaluation of intelligent systems.

I build systems and run controlled experiments to understand how agents learn from rewards, execution feedback, and imperfect models. My work spans RL research, coding-model evaluation, systems engineering, and open-source software.

[Portfolio](https://himanshupathak.is-a.dev/) · [GitHub](https://github.com/HimanshuPathak2725) · [LinkedIn](https://www.linkedin.com/in/himanshu-pathak-/) · [Hugging Face](https://huggingface.co/HimanshuPathak)

## Selected Work

### [Let Execution Do the Teaching](https://github.com/HimanshuPathak2725/let-execution-do-the-teaching)

Research and evaluation work on coding-model post-training, including supervised fine-tuning, GRPO, execution-based verification, and multi-turn feedback. The repository contains evaluation artifacts, verifier implementations, and experiments comparing training approaches using executable tests and task-level evidence.

### [VaporWall](https://github.com/HimanshuPathak2725/VaporWall)

A systems-security project exploring network filtering and threat analysis with Rust and eBPF/XDP. Its architecture combines kernel-level packet filtering with asynchronous user-space inspection, TCP stream reassembly, signature matching, and ONNX-based threat classification.

### [Fraud Radar](https://github.com/HimanshuPathak2725/Real_Time_Fraud_Detection_System)

A real-time fraud-scoring prototype built with Python, Isolation Forest, FastAPI, and Kafka. It uses synthetic transaction data to explore anomaly scoring, event processing, and live WebSocket monitoring. This is a learning and portfolio project, not a production fraud-detection system.

## Research & Writing

I use small, inspectable experiments to investigate learning dynamics, reward design, uncertainty, and model-based decision-making.

<details>
<summary><strong>Selected research notes and interactive experiments</strong></summary>

- **[Policy Gradients and the Meaning of Credit](https://himanshupathak.is-a.dev/posts/policy-gradients-and-the-meaning-of-credit/)** — An experiment on stochastic policy-gradient updates, baselines, and the difference between an unbiased estimator and the outcome of an individual update.

- **[Reward Shaping Without Changing the Task](https://himanshupathak.is-a.dev/posts/reward-shaping-without-changing-the-task/)** — A controlled Q-learning experiment exploring how potential-based reward shaping can preserve returns while changing the learning trajectory.

- **[What Uncertainty Can Tell a Planner](https://himanshupathak.is-a.dev/posts/what-uncertainty-can-tell-a-planner/)** — An investigation into model misspecification, predictive uncertainty, extrapolation, and the value of collecting informative observations.

- **[The World Models Today](https://himanshupathak.is-a.dev/posts/the-world-models-today/)** — An interactive guide to latent dynamics, partial observability, planning, and evaluating predictions through their consequences for decisions.

</details>

## Technical Skills

- **RL & LLMs:** Policy gradients, reward shaping, GRPO workflows, supervised fine-tuning, execution-based evaluation, verifier design
- **Machine Learning:** PyTorch, Hugging Face, scikit-learn, NumPy, ONNX
- **Languages:** Python, C++, Go, Rust, TypeScript, JavaScript
- **Backend & Systems:** FastAPI, Node.js, Kafka, Docker, Linux, eBPF/XDP, WebSockets
- **Web & Data:** React, Next.js, PostgreSQL, Supabase, MongoDB

## Open Source Contributions

My open-source work includes core Go engineering, WebSocket security, backend authorization, AI input hardening, distributed-system reliability, resource management, and developer tooling.

<details>
<summary><strong>ECSoC'26 — Go Gatekeeper: Concurrency, WebSocket Security &amp; Runtime Reliability</strong></summary>

Contributed core Go changes to a collaborative remote-terminal relay.

- **[Prevent a goroutine leak during room teardown — #8](https://github.com/VishalRaut2106/go-gatekeeper/pull/8)** · Merged  
  Fixed a blocked `readPump` during room destruction using a room-level completion channel and synchronized closure. Added a regression test for the host-disconnect scenario with a connected guest.

- **[Add per-IP WebSocket rate limiting — #9](https://github.com/VishalRaut2106/go-gatekeeper/pull/9)** · Merged  
  Added rate limiting before WebSocket upgrades to restrict excessive connection attempts.

- **[Validate WebSocket Origin headers — #17](https://github.com/VishalRaut2106/go-gatekeeper/pull/17)** · Merged  
  Added an Origin allowlist to strengthen the WebSocket security boundary.

- **[Stop exposing session codes through `/stats` — #20](https://github.com/VishalRaut2106/go-gatekeeper/pull/20)** · Merged  
  Removed session codes from the unauthenticated statistics endpoint and increased generated code length from six to ten hexadecimal characters.

- **[Enforce WebSocket message limits and keepalives — #30](https://github.com/VishalRaut2106/go-gatekeeper/pull/30)** · Merged  
  Added a 32 KiB message-size limit, read/write deadlines, and ping/pong handling to improve resource control and connection lifecycle management.

- **[Implement graceful shutdown — #18](https://github.com/VishalRaut2106/go-gatekeeper/pull/18)** · Merged  
  Added signal-aware shutdown handling for `SIGTERM` and `SIGINT`.

- **[Verify downloaded CLI binaries with SHA-256 — #19](https://github.com/VishalRaut2106/go-gatekeeper/pull/19)** · Merged  
  Added checksum generation and verification to strengthen downloaded-binary integrity.

</details>

<details>
<summary><strong>ECSoC'26 — MediFlow: AI Security, Authorization &amp; Backend Reliability</strong></summary>

- **[Harden AI prompt construction against untrusted input — #443](https://github.com/Nebulyn-Labs/MediFlow/pull/443)** · Merged  
  Added prompt-hardening utilities across Node.js and Dart, sanitized user-controlled input before delimiting it, and introduced automated tests for delimiter spoofing and instruction-override attempts.

- **[Validate facility ownership during registration — #394](https://github.com/Nebulyn-Labs/MediFlow/pull/394)** · Merged  
  Strengthened facility ownership validation to prevent users from registering themselves against another facility.

- **[Handle transient Firestore approval failures correctly — #445](https://github.com/Nebulyn-Labs/MediFlow/pull/445)** · Merged  
  Separated expected business-rule failures from transient infrastructure errors so retryable failures are not incorrectly treated as permanent rejections.

- **[Add rate limiting to callable Cloud Functions — #96](https://github.com/Nebulyn-Labs/MediFlow/pull/96)** · Merged  
  Introduced reusable server-side rate limiting to reduce endpoint abuse and excessive AI inference costs.

</details>

<details>
<summary><strong>ECSoC'26 — YuvaHub: Database Security, Messaging &amp; Cache Management</strong></summary>

- **[Prevent Firestore privilege escalation — #619](https://github.com/uditt490-pixel/YuvaHub/pull/619)** · Merged  
  Tightened Firestore access controls, added ownership checks for events and groups, and introduced 33 automated security-rule tests.

- **[Add RabbitMQ publisher confirms and dead-letter queues — #565](https://github.com/uditt490-pixel/YuvaHub/pull/565)** · Merged  
  Improved message-delivery observability with publisher confirmations, bounded retries, dead-letter routing, and regression tests.

- **[Add LRU eviction to the persistent API cache — #562](https://github.com/uditt490-pixel/YuvaHub/pull/562)** · Merged  
  Added bounded cache eviction and recovery from browser storage quota errors while preserving the existing two-tier cache design.

</details>

<details>
<summary><strong>ECSoC'26 — Developer Tooling: Code Retrieval, Tracing &amp; Project Detection</strong></summary>

- **[Add AST-based symbol-level indexing — DevWhisper #173](https://github.com/Aharshi3614/Devwhisper/pull/173)** · Merged  
  Introduced Python AST-based extraction of functions, classes, and methods as discrete indexing units. Combined symbol-level and line-based chunks, enriched retrieval metadata, and added tests. The PR reports 80 passing tests, including 18 new tests.

- **[Add scoped symbol tracing — DiffGuardian #19](https://github.com/Aryan0628/diffguardian/pull/19)** · Merged  
  Added `--scope` support to limit trace results to a directory or package, including path normalization and filtering during recursive barrel traversal.

- **[Add JSON output to the trace CLI — DiffGuardian #16](https://github.com/Aryan0628/diffguardian/pull/16)** · Merged  
  Added structured JSON output for trace results, making the CLI easier to integrate into automated workflows.

- **[Improve Python project detection fallbacks — RepoStart #37](https://github.com/ZarrarPeshimam/RepoStart/pull/37)** · Merged  
  Added fallback detection through common Python entry-point files when dependency manifests are absent, while preserving information about how a project was detected.

</details>

<details>
<summary><strong>ECSoC'26 — Security &amp; Resource Management</strong></summary>

- **[Prevent DNS rebinding in webhook requests — Semantic Plagiarism Detector #1695](https://github.com/Ganesh-403/semantic-plagiarism-detector/pull/1695)** · Merged  
  Added DNS-pinning support to the SSRF protection layer, using the validated IP for requests while preserving the hostname and supporting IPv6. Included six focused security tests.

- **[Add concurrent SQLite thread-safety stress tests — Semantic Plagiarism Detector #1697](https://github.com/Ganesh-403/semantic-plagiarism-detector/pull/1697)** · Merged  
  Added stress testing for SQLite connection behavior under concurrent access.

- **[Fix WebAssembly memory leaks in PDF signature verification — WorkSphere #2138](https://github.com/SatyamPandey-07/WorkSphere/pull/2138)** · Merged  
  Added explicit WASM heap cleanup, worker lifecycle handling, and a memory-retention test covering 50 consecutive verifications.

- **[Prevent open redirects in download URLs — PrepPilot #306](https://github.com/Canopus-Labs/PrepPilot/pull/306)** · Merged  
  Added URL parsing and HTTPS validation, restricted redirects to an allowlisted download host, and introduced regression tests for unsafe redirect targets.

</details>

## Current Interests

Reinforcement learning · LLM post-training · Coding-agent evaluation · Reward design · Model uncertainty · World models · Systems engineering

---

More about my work and experiments: [himanshupathak.is-a.dev](https://himanshupathak.is-a.dev/)

