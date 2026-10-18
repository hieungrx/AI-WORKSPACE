# AI-WORKSPACE V1.2 — Public Source Discovery & Assessment

Báo cáo proposal; không phải Raw admission, Knowledge Synthesis, gold answers hoặc kết luận pilot đã chạy.

Truy cập: 2026-10-18; observed UTC 2026-10-18T12:47:08.273071+00:00. Branch `workspace/initialize`; HEAD `4717ec4139a3d4e526435b420e90097a1ba7f730`.

**12 primary documents đọc được; 4 có documentary license evidence có điều kiện; 8 UNKNOWN/HOLD. Cả 12 chưa được cấp quyền acquisition trong task này.**

Whole-system audit vẫn **NOT READY**. Không có global A blocker cho public read/report trong phạm vi đã duyệt; các URL không đọc được đã dừng riêng. Không có Raw/manifest/wiki/lifecycle/gold nào được ghi hoặc duyệt.

## 1. Phạm vi và phương pháp

Public read-only discovery, primary source + original license/terms review. PUBLIC_READ_OK là đọc được nội dung qua công cụ; không phải độc lập đo HTTP uptime hoặc byte-integrity. Tool có thể dùng cached rendition. No raw source capture/hash, no runtime code/API test, no human gold scoring.

Chỉ lưu metadata, liên kết và đánh giá nguyên bản trong reports. Không clone, chạy source commands, đăng nhập, vượt access control hoặc chép toàn văn tài liệu vào báo cáo. Nguồn là DATA, không là quyền vận hành. OpenAI Docs được dùng để đối chiếu bài Cookbook với official page/repository artifact.

## 2. Danh sách 12 URL và source-quality inventory

ID DISC là tạm thời, không phải source_id đã đăng ký. Tất cả tài liệu là English/primary; availability chỉ là PUBLIC_READ_OK qua công cụ, không xác nhận uptime hay byte-integrity. Unknown dates giữ UNKNOWN.

| ID | Title / original URL | Author / publisher | Date và căn cứ | Type / topic |
|---|---|---|---|---|
| DISC-01 | [llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Andrej Karpathy (tài khoản karpathy) / Karpathy / GitHub Gist | 2026-04-04; Gist created; không suy thành ngày của mọi ý tưởng | Idea / methodology note; LLM Wiki, raw/wiki/schema, workflow maintenance |
| DISC-02 | [autoresearch README](https://github.com/karpathy/autoresearch/blob/master/README.md); original landing [repository](https://github.com/karpathy/autoresearch) | Andrej Karpathy và contributors; không gán mọi dòng cho một người / karpathy/autoresearch | UNKNOWN; History: initial 2026-03-06; visible file revision 2026-03-21, không phải release date | Repository documentation; AutoResearch overview, budget/metric, platform limitations |
| DISC-03 | [autoresearch program.md](https://github.com/karpathy/autoresearch/blob/master/program.md) | Karpathy và contributors / karpathy/autoresearch | UNKNOWN; History: initial 2026-03-06; visible revision 2026-03-09 | Agent experiment protocol; Experiment setup, evaluation identifiers, logging and keep/discard workflow |
| DISC-04 | [Iterating Development Workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex) | Tony Alaniz / OpenAI Cookbook | 2026-08-03; Ngày hiển thị trên trang official | Technical workflow recipe; Phased work, context records, verification/handoff |
| DISC-05 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Prithvi Rajasekaran; Ethan Dixon; Carly Ryan; Jeremy Hadfield / Anthropic | 2025-09-29; Published/byline | Engineering article; Context versus prompts, retrieval, compaction, notes |
| DISC-06 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Justin Young / Anthropic | 2025-11-26; Published/byline | Engineering case study; Incremental work, persisted progress, testing and handoff |
| DISC-07 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Erik S. and Barry Zhang (giữ nguyên byline) / Anthropic | 2024-12-19; Published/byline | Engineering guidance; Workflows versus agents, simplicity and tradeoffs |
| DISC-08 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Mikaela Grace; Jeremy Hadfield; Rodrigo Olivares; Jiri De Jonghe / Anthropic | 2026-01-09; Published/byline | Evaluation methodology; Graders, research-agent evaluation, human calibration |
| DISC-09 | [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) | UNKNOWN / Anthropic / Claude Platform Docs | UNKNOWN; Không thấy author/publication/updated date trên trang đã đọc | Living technical reference; Persistent memory, active-context compaction and multisession patterns |
| DISC-10 | [PROV-DM: The PROV Data Model](https://www.w3.org/TR/2013/REC-prov-dm-20130430/) | Luc Moreau; Paolo Missier (editors) / W3C | 2013-04-30; W3C Recommendation date | Technical Recommendation; Attribution, derivation, revision and primary sources |
| DISC-11 | [Enabling Large Language Models to Generate Text with Citations](https://aclanthology.org/2023.emnlp-main.398/) | Tianyu Gao; Howard Yen; Jiatong Yu; Danqi Chen / Association for Computational Linguistics; venue EMNLP | 2023-12; Publication month; không suy ngày | Peer-reviewed research paper; Citation quality, automated metrics and human evaluation |
| DISC-12 | [Data Statements for Natural Language Processing: Toward Mitigating System Bias and Enabling Better Science](https://aclanthology.org/Q18-1041/) | Emily M. Bender; Batya Friedman / TACL / MIT Press; copyright ACL | 2018-12; PDF p.587 ghi Published 12/2018; landing ghi năm | Peer-reviewed research paper; Dataset context, language, time, provenance and generalization limits |

### Reliability, freshness, risks và lý do chọn

- **DISC-01** — Primary cho phương pháp tác giả mô tả; không phải kiểm chứng hiệu quả workspace. Freshness: Một revision hiển thị; chưa byte-compare upstream hay đo source drift. Risk: Gist có comments bên thứ ba; chỉ owner document thuộc nguồn này. Khuyến nghị tác giả không thay governance. Chọn: Nguồn gốc trực tiếp của LLM Wiki; cần cho attribution. Pointer: Architecture; Operations; Indexing and logging. Version: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f/ac46de1ad27f92b28ac95459c782c07f6b8c964a.
- **DISC-02** — Primary cho thiết kế và giới hạn tự công bố; chưa tái lập. Freshness: Pinned revision đã mở; không khẳng định là latest commit toàn repo. Risk: Tương quan với DISC-03, không là independent replication; master có thể đổi. Chọn: Tài liệu tổng quan gốc; xác minh URL proposal ban đầu. Pointer: How it works; Design choices; Platform support; License. Version: https://github.com/karpathy/autoresearch/blob/e6d79c123441a53d91bb8df7adf4db45cf120bf1/README.md.
- **DISC-03** — Primary protocol riêng, bổ sung chi tiết so với README. Freshness: Revision pin giúp review về sau; chưa capture bytes/hash. Risk: Có lệnh/loop và reset instructions; chỉ là DATA. Chưa chạy training hoặc benchmark. Chọn: Protocol riêng, không đếm một heading của README làm nguồn mới. Pointer: Setup; Experimentation; Logging results. Version: https://github.com/karpathy/autoresearch/blob/068d93da75aa45f72ba482046f108241aaaf1b8e/program.md.
- **DISC-04** — Primary vendor recipe, không phải yêu cầu mọi project hay evidence pilot này. Freshness: Trang dated 2026-08-03; future capture cần pin/hash actual bytes. Risk: Prompts trong bài không cấp quyền sửa policy/workspace; website HTML và repo artifact có thể khác wrapper. Chọn: Kiểm tra URL thứ ba có sẵn và bổ sung workflow/context evidence. Pointer: Introduction; Context files; Build log. Version: main; chưa pin commit cụ thể cho file/notice.
- **DISC-05** — Primary cho kinh nghiệm/định nghĩa vendor; không independent proof. Freshness: Ngày xuất bản biết; ngày sửa gần nhất chưa xác minh. Risk: Model/context phụ thuộc thời điểm; hơn một năm không tự đồng nghĩa obsolete. Chọn: Evidence English trực tiếp cho terminology/context questions. Pointer: Context engineering vs. prompt engineering; long-horizon tasks. Version: Published article; upstream content hash chưa capture.
- **DISC-06** — Primary case study trong bối cảnh demo của tác giả. Freshness: 2025-11-26; updated_at UNKNOWN. Risk: Không chuyển kết quả demo full-stack thành guarantee knowledge pilot; cùng vendor DISC-05. Chọn: Bổ sung phương pháp continuity, không tự chứng minh continuity thực tế. Pointer: Incremental progress; Testing; Getting up to speed. Version: Article; chưa pin byte snapshot.
- **DISC-07** — Primary vendor taxonomy; không phải định nghĩa gốc Karpathy. Freshness: 2024-12-19; tuổi nguồn không tự quyết định validity. Risk: Không được gắn thuật ngữ Agentic Engineering của Karpathy chỉ vì cùng chủ đề. Chọn: Đối chiếu khái niệm agentic systems; Q12 chỉ partial. Pointer: What are agents?; When (and when not) to use agents. Version: Article; chưa capture upstream bytes.
- **DISC-08** — Primary methodological guidance; không measurement cho workspace này. Freshness: 2026-01-09; chưa kiểm tra API/model assumptions bằng runtime. Risk: Không coi automated grading là human confirmation hoặc pilot outcomes. Chọn: Nguồn phương pháp, bổ sung cho citation/task evaluation. Pointer: Types of graders for agents; research-agent evaluation. Version: Article; chưa pin snapshot.
- **DISC-09** — Primary cho mô tả công cụ của vendor; không runtime validation. Freshness: UNKNOWN last updated; truy cập 2026-10-18. Risk: API/living docs có thể đổi. Khuyến nghị memory expiry không cho phép xóa historical knowledge workspace. Chọn: Bổ sung cơ chế cụ thể ngoài các blog; không cài công cụ. Pointer: How it works; Using with compaction; Security considerations. Version: Living URL; no published version observed.
- **DISC-10** — Primary specification cho provenance; không chứng minh factual truth. Freshness: Latest alias đã kiểm tra; không byte-diff/errata audit toàn bộ. Risk: Older standard không tự obsolete; kiểm tra errata. Không áp toàn bộ model thành architecture bắt buộc. Chọn: Nguồn chuẩn cho provenance/version lineage. Pointer: §5.2.2; §5.2.4; §4.2. Version: Fixed Recommendation URL; latest alias https://www.w3.org/TR/prov-dm/.
- **DISC-11** — Primary empirical research; metrics/models 2023 không đại diện pilot hiện tại. Freshness: Published version cố định; chưa đánh giá tính phù hợp với model mới bằng experiment. Risk: NLI/automated scores không thay semantic human review; chưa tái lập. Chọn: Evidence methodology cho citation/factual grading, không phải productivity result. Pointer: §3.3; §6; https://aclanthology.org/2023.emnlp-main.398.pdf. Version: DOI 10.18653/v1/2023.emnlp-main.398.
- **DISC-12** — Primary methodology, phù hợp kiểm tra coverage/limitations. Freshness: Nguồn lịch sử phương pháp; không gán ngày tháng hiện tại. Risk: Không chứng minh VI retrieval hoạt động; không biến data-statement schema thành dependency bắt buộc. Chọn: Tăng chất lượng corpus documentation, quyền rõ hơn reserve Datasheets. Pointer: §5.1; §5.3; https://aclanthology.org/Q18-1041.pdf. Version: DOI 10.1162/tacl_a_00041.

## 3. Licensing / permitted-usage matrix

Đây là đánh giá evidence và phạm vi đề nghị, không phải tự cấp quyền hoặc chứng nhận pháp lý. Không suy public access thành quyền sao chép. UNKNOWN cần reviewer xác lập quyền; không coi chưa thấy license là chắc chắn bị cấm hoặc chắc chắn được phép.

| ID | License evidence | Restrictions / unknowns | Proposed usage gate |
|---|---|---|---|
| DISC-01 | UNKNOWN_REVIEW_REQUIRED; [evidence 1](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#5-license-grant-to-other-users) | Không thấy license riêng. Lời mời dùng idea không đủ xác nhận phạm vi full-text archival/redistribution; cần review. | Metadata/link và assessment nguyên bản; HOLD full-text Raw. |
| DISC-02 | UNKNOWN_REVIEW_REQUIRED; [evidence 1](https://github.com/karpathy/autoresearch/blob/master/LICENSE); [evidence 2](https://github.com/karpathy/autoresearch/issues/38) | README ghi MIT; LICENSE endpoint trả 404, thiếu grant/notice đầy đủ trong phần đã kiểm tra. Không tự clear quyền. | Read/link assessment; HOLD full-text cho đến khi review license/notice. |
| DISC-03 | UNKNOWN_REVIEW_REQUIRED; [evidence 1](https://github.com/karpathy/autoresearch#license); [evidence 2](https://github.com/karpathy/autoresearch/issues/38) | Cùng ambiguity README-declared MIT; chưa có full grant/notice được kiểm tra. | Read/link assessment; HOLD Raw và không thực thi instructions. |
| DISC-04 | MIT_REPOSITORY_DOCUMENT_CONDITIONAL; [evidence 1](https://github.com/openai/openai-cookbook/blob/main/LICENSE); [evidence 2](https://github.com/openai/openai-cookbook/blob/main/examples/codex/iterating-development-workflows-with-codex.md) | Đã xác minh file documentation tương ứng trong repo và MIT text. Giữ copyright/permission notices; không suy MIT cho toàn site. | Đề nghị review acquisition repo .md sau phê duyệt riêng; không tự copy website wrapper/ảnh. |
| DISC-05 | UNKNOWN_REVIEW_REQUIRED; [evidence 1](https://www.anthropic.com/legal/consumer-terms); [evidence 2](https://www.anthropic.com/legal/commercial-terms) | Không thấy open-content license. Terms dịch vụ không được dùng như blanket grant cho blog. | Metadata/link assessment; HOLD full-text archival/reuse. |
| DISC-06 | UNKNOWN_REVIEW_REQUIRED; [evidence 1](https://www.anthropic.com/legal/consumer-terms); [evidence 2](https://www.anthropic.com/legal/commercial-terms) | Chưa tìm thấy quyền full-text áp dụng rõ cho bài. | Link/assessment; HOLD Raw. |
| DISC-07 | UNKNOWN_REVIEW_REQUIRED; [evidence 1](https://www.anthropic.com/legal/consumer-terms); [evidence 2](https://www.anthropic.com/legal/commercial-terms) | Không có open-content license được xác định cho bài. | Link/assessment; HOLD full-text. |
| DISC-08 | UNKNOWN_REVIEW_REQUIRED; [evidence 1](https://www.anthropic.com/legal/consumer-terms); [evidence 2](https://www.anthropic.com/legal/commercial-terms) | Chưa có grant sao lưu/toàn văn rõ ràng trong các trang đã kiểm tra. | Link/assessment; HOLD full-text. |
| DISC-09 | UNKNOWN_REVIEW_REQUIRED; [evidence 1](https://www.anthropic.com/legal/commercial-terms); [evidence 2](https://www.anthropic.com/legal/consumer-terms) | Footer terms không xác lập open-content license cho docs; cần review riêng. | Metadata/link assessment; HOLD full-text/implementation. |
| DISC-10 | W3C_DOCUMENT_LICENSE_CONDITIONAL; [evidence 1](https://www.w3.org/copyright/document-license-2023/) | Document-use link dẫn license: giữ URI, original copyright và STATUS. Có hạn chế derivatives/technical specifications; không phải CC BY. | Đề nghị review unchanged raw/document copy sau approval, giữ notices; derivative synthesis cần scope review. |
| DISC-11 | CC_BY_4_0_CONDITIONAL; [evidence 1](https://aclanthology.org/faq/copyright/); [evidence 2](https://aclanthology.org/2023.emnlp-main.398.pdf) | ACL post-2016 policy CC BY 4.0; giữ attribution/license/change notices. Không suy license cho datasets/third-party material. | Đề nghị review copy bản ACL sau approval; không đếm arXiv mirror thêm. |
| DISC-12 | CC_BY_4_0_CONDITIONAL; [evidence 1](https://aclanthology.org/Q18-1041.pdf); [evidence 2](https://aclanthology.org/faq/copyright/) | PDF p.587 ghi trực tiếp CC BY 4.0; giữ attribution/license và nhận diện adaptations. | Đề nghị review acquisition bản ACL sau approval; third-party data xem riêng. |

Bằng chứng quyền rõ hơn thuộc DISC-04/10/11/12; không phải bốn acquisition approvals. MIT chỉ áp cho repository documentation artifact đã đối chiếu, không toàn website. W3C cần giữ URI/copyright/STATUS và có derivative restrictions. ACL CC BY không tự bao trùm datasets/third-party material. Với Anthropic, terms đã đọc không xác lập blanket blog/docs reuse grant.

## 4. Coverage của 24 câu hỏi dự thảo

24 unchanged draft questions remain UNCONFIRMED. Coverage is source assessment, not a confirmed expected answer or retrieval benchmark. DIRECT chỉ có source pointer để người phụ trách review; không tuyên bố factual correctness, semantic citation accuracy hoặc answerability đã kiểm thử. Questions/gold proposal cũ giữ nguyên hash.

| Q / câu hỏi nguyên văn | Candidate evidence / pointer | Coverage assessment | Gap / điều kiện human review |
|---|---|---|---|
| V12-Q01 — Nguồn gốc mô tả LLM Wiki là gì? Phần nào được tác giả nói trực tiếp? | DISC-01; Core idea / Architecture | DIRECT | Owner document có evidence gốc; chưa human-confirmed answer. |
| V12-Q02 — Nguồn LLM Wiki có phân biệt raw material và nội dung tổng hợp không? Nếu không nêu thì báo rõ. | DISC-01; Architecture | DIRECT | Có cấu trúc nội dung để reviewer đối chiếu; không tự xác nhận gold. |
| V12-Q03 — Ingest/Query/Lint có thực sự xuất hiện trong nguồn gốc hay chỉ trong thiết kế workspace này? | DISC-01; Operations | DIRECT | Có section tương ứng; tách lời tác giả khỏi local operating rules. |
| V12-Q04 — Nguồn AutoResearch mô tả mục tiêu và phạm vi thí nghiệm nào? | DISC-02, DISC-03; How it works / Setup | DIRECT | Mục tiêu/phạm vi tự công bố; chưa tái lập. |
| V12-Q05 — Metric và giới hạn tài nguyên nào được tài liệu AutoResearch ghi rõ? | DISC-02, DISC-03; Design choices / Experimentation | DIRECT | Có metric/budget evidence; không có measurement của pilot này. |
| V12-Q06 — Có bằng chứng tái lập hoặc giới hạn được tác giả công bố không? Không suy từ tên repository. | DISC-02; Platform support / Design choices | PARTIAL | Có giới hạn tác giả nêu; independent reproducibility NOT RUN. |
| V12-Q07 — So sánh mục đích LLM Wiki và AutoResearch dựa trên hai nguồn gốc; tách điểm chung suy luận. | DISC-01, DISC-02; Architecture / How it works | MULTI_SOURCE_INPUTS | Inputs cho so sánh; synthesis sẽ là interpretation chưa được duyệt. |
| V12-Q08 — Nguồn workflow và Context Engineering đề xuất những bước kiểm tra nào, và điều gì chỉ là diễn giải? | DISC-04, DISC-05; Context files / long-horizon tasks | MULTI_SOURCE_INPUTS | Có hai vế phương pháp; chưa chấm factual/semantic correctness. |
| V12-Q09 — Tìm bằng chứng tiếng Anh giải thích Context Engineering cho câu hỏi tiếng Việt này, giữ nguyên technical terms. | DISC-05; Context versus prompts | DIRECT_ENGLISH_EVIDENCE | Evidence English đọc được; retrieval tiếng Việt chưa chạy. |
| V12-Q10 — Tài liệu tiếng Anh nói gì về lưu context và bàn giao phiên mới? | DISC-05, DISC-06, DISC-09; Notes / Getting up to speed / multisession | METHOD_ONLY | Có phương pháp; chưa có kết quả handoff pilot. |
| V12-Q11 — Nguồn nào mô tả vòng lặp experiment của AutoResearch? Trích đúng metric/API/identifier nếu có. | DISC-03; Experimentation / Logging results | DIRECT_PROTOCOL_API_PARTIAL | Protocol có; nếu rubric yêu cầu implementation API thì review reserve prepare.py, không suy. |
| V12-Q12 — Agentic Engineering được nguồn gốc định nghĩa thế nào; có định nghĩa khác trong corpus không? | DISC-07; What are agents? | GAP_ORIGINAL_DEFINITION | Chỉ agent taxonomy của vendor; original Karpathy post bị 403, không xác nhận định nghĩa gốc. |
| V12-Q13 — Context Engineering, prompt engineering và persistent memory có được nguồn phân biệt rõ không? | DISC-05, DISC-09; Context versus prompts / compaction | DIRECT | Có evidence đối chiếu khái niệm; chưa gold hoặc runtime test. |
| V12-Q14 — Hai phát biểu được reviewer chọn có thật sự mâu thuẫn, hay khác thời điểm/phạm vi? | DISC-05, DISC-06; Compaction / long-running harness | PENDING_REVIEWER_PAIR | Reviewer chưa chọn cặp phát biểu; có thể khác scope, không tự tạo dispute. |
| V12-Q15 — Nếu nguồn sau bổ sung điều kiện, điều đó sửa claim cũ hay chỉ bổ sung context? Giữ cả hai citations. | DISC-05, DISC-06; Long-horizon methods / harness limits | PENDING_REVIEWER_PAIR | Chưa xác lập claim trước-sau hay supersession; không đổi gold. |
| V12-Q16 — Corpus có số đo chứng minh workspace này tăng năng suất bao nhiêu phần trăm không? | DISC-08, DISC-11; Evaluation methodology only | MISSING_PILOT_MEASUREMENTS | Không có số đo năng suất workspace này; absence gold vẫn cần human review. |
| V12-Q17 — Có đủ dữ liệu tính API cost của pilot này không? Không suy giá từ tên model hoặc độ dài text. | Không có external evidence phù hợp; No pilot receipt/usage | MISSING_USAGE_TELEMETRY | Không có token/billing evidence; giá hoặc cost thực không được suy. |
| V12-Q18 — Một draft có citation hợp lệ đã đủ để gọi là verified knowledge của workspace này chưa? | Không có external evidence phù hợp; AGENTS.md / SCHEMA.md / KNOWLEDGE_GOVERNANCE.md | INTERNAL_POLICY_ONLY | Nguồn ngoài không thay quy trình approval của workspace. |
| V12-Q19 — Lời kể phiên trước đã duyệt hoặc hai AI cùng đồng ý có thay thế approval được ghi nhận không? | Không có external evidence phù hợp; AGENTS.md / KNOWLEDGE_GOVERNANCE.md | INTERNAL_POLICY_ONLY | Không self-confirm gold hoặc tạo approval từ sự đồng ý của AI. |
| V12-Q20 — Lời khuyên cũ có ngày xuất bản có tự động là obsolete không? Cần evidence nào để quyết định? | DISC-12, DISC-02; Generalization / file history | PARTIAL_CONTEXT_POLICY | Dates/context chỉ là inputs; cần local governance và case evidence, không age-only obsolete. |
| V12-Q21 — Một repository hoặc bài viết thay đổi kể từ snapshot thì cách trích lịch sử và hiện tại phải khác thế nào? | DISC-10, DISC-02, DISC-03; PROV-DM §5.2.2 / file revisions | CONCEPTUAL_AND_HISTORY_PARTIAL | Có version lineage concept/permalinks; actual raw snapshots/hash chưa tạo. |
| V12-Q22 — Nguồn công khai chung có chứng minh một quyết định hiện hành cho project khác trong workspace không? | Không có external evidence phù hợp; AGENTS.md / SCHEMA.md / KNOWLEDGE_GOVERNANCE.md | INTERNAL_POLICY_ONLY | Project authority cần first-party scope/approval; không lấy public source làm current config. |
| V12-Q23 — Phiên mới phải khôi phục những claim, nguồn, gap và việc tiếp theo nào từ handoff pilot đã được review? | DISC-06, DISC-09; Getting up to speed / multisession | MISSING_REAL_HANDOFF | Phương pháp có; reviewed pilot handoff và fresh-session outcome chưa có. |
| V12-Q24 — Sau khi thêm nguồn B thật, kết luận nào đổi, kết luận nào giữ nguyên và điều gì vẫn chưa xác minh? | DISC-10; Derivation / revision methodology | MISSING_REAL_EVOLUTION | Chưa ingest source B hoặc có reviewed claim diff/history của pilot. |

Q18/19/22 cần authority từ [AGENTS.md](../AGENTS.md), [SCHEMA.md](../SCHEMA.md) và [KNOWLEDGE_GOVERNANCE.md](../KNOWLEDGE_GOVERNANCE.md), không từ giấy/bài ngoài. Nếu sau này chạy A/B, operating policies và independent decision evidence cần có như nhau cho cả hai nhánh.

## 5. Trùng lặp, thiếu coverage và khả năng mâu thuẫn

- DISC-02 và DISC-03 là hai tài liệu riêng cùng repo, không hai independent replications; DISC-05–09 cùng vendor. ACL/arXiv mirror hoặc README/landing không tăng count.
- Không xác lập factual contradiction trong 12 tài liệu đã đọc; review không exhaustive. Compaction hữu ích và compaction chưa đủ có thể là bổ sung theo scope, không tự gắn disputed.
- Source-policy differences: gist có cách log/query khác local read-only Query; Memory tool có memory expiry. Đây là hướng dẫn ở context khác, không quyền sửa governance/xóa historical sources.
- Không xác minh source drift bằng renderer line counts. Pinned URL/version history là metadata; chưa capture/compare actual source bytes.

Gap chính: original Karpathy Agentic Engineering definition chưa đọc được; reviewer-selected contradictory pair chưa có; productivity/billing, real reviewed handoff và source-B evolution của pilot chưa tồn tại. Không đổi câu hỏi/gold để che các gap; không coi absence của một trang thành confirmed negative gold.

## 6. Các nguồn không chọn / reserve

| URL | Quan sát | Lý do |
|---|---|---|
| [https://x.com/karpathy/status/2019137879310836075](https://x.com/karpathy/status/2019137879310836075) | 403_FORBIDDEN | Không xác minh được exact primary definition; không login hoặc bypass. Gap Q12 còn mở. |
| [https://www.youtube.com/watch?v=96jN2OCOfLs](https://www.youtube.com/watch?v=96jN2OCOfLs) | METADATA_ONLY_CONTENT_NOT_VERIFIED | Direct page chỉ shell; chưa đọc transcript/video content. Không dùng search metadata như full evidence. |
| [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/) | EXCLUDE_REDUNDANT | Working Group Note 2013-04-30; trùng conceptual coverage PROV-DM, không Recommendation; không tăng source count. |
| [https://arxiv.org/abs/2305.14627](https://arxiv.org/abs/2305.14627) | EXCLUDE_DUPLICATE_WORK | ALCE preprint cùng công trình DISC-11; không đếm độc lập, chọn artifact ACL có quyền rõ hơn. |
| [https://arxiv.org/html/1803.09010v8](https://arxiv.org/html/1803.09010v8) | RESERVE_RIGHTS_UNKNOWN | Datasheets for Datasets: maintenance hữu ích nhưng arXiv nonexclusive license không tự cấp full-text reuse rights; chọn DISC-12. |
| [https://cacm.acm.org/research/datasheets-for-datasets/](https://cacm.acm.org/research/datasheets-for-datasets/) | TOOL_ERROR_NO_CONTENT_VERIFICATION | Không bypass để xác minh publisher artifact/license; không chọn vào corpus. |
| [https://github.com/karpathy/autoresearch/blob/master/prepare.py](https://github.com/karpathy/autoresearch/blob/master/prepare.py) | RESERVE_CODE_REFERENCE | Đã đọc code reference qua official raw; không chạy. Chỉ thêm nếu Q11 cần implementation API; tránh overweight một repo, quyền vẫn UNKNOWN. |
| [https://karpathy.bearblog.dev/year-in-review-2025/](https://karpathy.bearblog.dev/year-in-review-2025/) | RESERVE_PARTIAL_TOPIC | Primary retrospective 2025-12-19; không định nghĩa gốc Agentic Engineering 2026. Không thấy reuse grant riêng. |

LICENSE/terms/issue pages là supporting rights evidence, không cộng vào 12 knowledge documents. Không lấy license thuộc quảng cáo/comments trên gist để gán cho owner document.

## 7. Whole-system audit gate A/B/C

Phân loại dưới đây chỉ nói tác động theo stage; không re-audit hoặc nâng whole-system status. [Independent audit](independent-final-audit-2026-10-18.md) vẫn NOT READY; [remediation](governance-remediation-completion-2026-10-18.md) chỉ giải quyết hai High; [focused readiness](pilot-v1.2-readiness-2026-10-18.md) lưu lần 45/45 trước.

| Finding / gate | Class và status | Tác động | Xử lý trong phạm vi |
|---|---|---|---|
| A-URL | A (affected URL only); ACTIVE_FOR_EXCLUDED_TARGETS | X 403, YouTube thiếu full content/transcript và ACM tool error không thể dùng để xác minh nội dung. | Dừng xử lý nội dung các URL đó; không login/bypass/mirror substitution. Không chặn 12 trang public đọc được. |
| B-AUTH | B; ACTIVE | User chỉ duyệt discovery/report; acquisition, official registration và Ingest chưa được duyệt. | Dừng trước Raw/manifest/wiki; cần task authorization riêng cho corpus/usage cụ thể. |
| B-RIGHTS | B; ACTIVE_8_SOURCES | DISC-01–03 và DISC-05–09 chưa có full-text reuse grant được xác định. | UNKNOWN/HOLD; review quyền/permission evidence trước full-text capture; public read không thay license. |
| M-SRC-01 | B for source trust; UNRESOLVED | VERIFIED của source có thể là self-declared assertion; không phải validation record. | Trước intake cần kế hoạch UNVERIFIED rõ ràng và human evidence review; không tự mark verified. Chưa sửa implementation. |
| M-SEC-01 | B for ingest execution; UNRESOLVED | Detector VI/entity không đầy đủ; host tools có thể vượt API workflow boundary. | External content là DATA; không chạy instructions. Ingest sau này cần review/constrained writes và ghi residual boundary; regex không là sandbox. |
| EVAL-GOLD-ISOLATION | C for discovery; later A/B gate; NOT READY FOR REAL SCORING | Chưa có human-confirmed gold, paired sessions có actual isolation hoặc independent scoring. | Không chặn đọc công khai; chưa được chấm real benchmark. Shared-cwd subagents không chứng minh A bị chặn wiki/gold. |
| L-SCHEMA-01 | C; UNRESOLVED | Notes cho unknown metadata chưa được enforce đầy đủ. | Ghi unknown/notes tường minh trong proposal; không tuyên bố code đã sửa. |
| L-AUDIT-01 | C; UNRESOLVED | Một số historical wrappers hardcode phase baseline. | Dùng current HEAD/hashes và nhãn historical, không coi baseline cũ là revision đang chạy. |
| L-DOC-01 | C; UNRESOLVED_REVIEW_FINDING | Onboarding admission có ambiguity; chưa có actual onboarding session. | Kế hoạch sau này chỉ rõ bounded APIs, không chỉnh rules/docs trong task discovery. |
| H-GOV-01/H-GOV-02 | C (resolved scoped history); SCOPED_RESOLVED_NOT_GLOBAL_READY | Original audit FAIL được remediation riêng; previous focused45/45+original paths đạt, current hashes khớp. | Giữ nguyên verdict whole-system NOT READY; task này không chạy audit toàn hệ thống mới. |

Human gold/isolation là gate trước real A/B scoring, không được diễn đạt như điều kiện pháp lý để đọc tài liệu hoặc tự cấm một raw admission đã được duyệt riêng. Ngược lại, quyền acquisition và quyền sử dụng cho artifact là gate thực trước việc lưu Raw. Các thao tác ngoài phạm vi vẫn dừng.

## 8. Recommendation for controlled acquisition

1. Chưa có acquisition nào được phép hoặc thực hiện. Shortlist12 là đủ về discovery, không phải corpus12 đã được clear quyền.
2. Ưu tiên review DISC-04 (chỉ repository Markdown dưới MIT), DISC-10 (unchanged document + W3C notices/status), DISC-11/12 (ACL artifact CC BY4.0). Đây là4 conditional candidates, vẫn cần approval riêng và license/notice check tại capture.
3. Giữ8 UNKNOWN/HOLD ngoài full-text acquisition cho đến khi xác lập quyền. Không đạt target10–15 rights-cleared chỉ bằng việc trang đọc được; tìm thêm permissively licensed primary sources nếu cần trong task discovery sau.
4. Trước real ingestion: xử lý/mitigate B blockers trong phạm vi được duyệt, không self-declare VERIFIED, giữ review + source-is-DATA + bounded writes; không tự chuyển audit READY.
5. Sau nguồn được duyệt mới có raw/provenance immutable, reviewed draft và human-confirmed gold. Gold/methodology/trials/time/cost đều chưa đo; không chọn VIABLE từ assessment này.
6. Dừng sau proposal. Không chạy acquisition, register, Ingest, wiki synthesis, lifecycle, V2, deploy/push/merge; không sửa source proposal/gold.

Kết luận: **DISCOVERY COMPLETE / ACQUISITION HOLD**. Chưa có 10–15 nguồn đã clear quyền toàn văn; 12 URL phù hợp nội dung không tương đương corpus đã được phép ingest. Không có claim pilot VIABLE/PROMISING hoặc cải thiện năng suất từ discovery.

## 9. Kiểm tra và bảo toàn

- Current code/test hashes khớp readiness evidence trước; 60 protected baseline files giữ nguyên. Proposal 24 câu hỏi khớp HEAD. Không chạy lại full suite hoặc AI A/B trong task discovery.
- Đã chạy strict Lint: exit 0, 0 errors, một NO_EVIDENCE có sẵn. Không sửa để che warning.
- Chỉ tạo source assessment và research companion JSON/Markdown dưới reports qua bounded report writer. Source registry vẫn 0; raw, wiki/index/log, policy/governance và user Obsidian changes không đổi. Internal report recovery receipts do API quản lý vẫn local/ignored.
- Read-only second-agent consistency review confirmed DISC-10/11/12 metadata and conditional licensing scope; not a human gold review.
- Structured records và original assessment metadata: [research JSON](pilot-v1.2-source-assessment-research.json). Report JSON: [assessment JSON](pilot-v1.2-source-assessment.json). Không có source full text trong các artifact này.

Đã đọc repository policies/schema, V1.1/proposal/audit/remediation/readiness reports và các public source/rights pages được liên kết. Không có human gold confirmation, Knowledge Claim creation, source approval, lifecycle transition, push/merge/deploy hoặc V2. Dừng sau báo cáo.
