# V1.2 — Readiness và source manifest proposal

**PRE-ACQUISITION PROPOSAL. Chờ phê duyệt trước external discovery/read; chưa chạy real pilot.**

## Trạng thái đã kiểm tra

- Latest whole-system audit vẫn ghi NOT READY; chưa có audit mới thay thế. Hai finding High đã được remediation riêng.
- Lượt này chạy **45/45 governance tests PASS**, original public failure paths đạt; strict Lint không có ERROR, chỉ warning NO_EVIDENCE có sẵn.
- Code/test hashes khớp lượt V1.1 234/234 trước; không gọi đó là full suite mới. 23 protocol-only rubrics vẫn NOT RUN.
- **0 external requests, 0 fetched documents, 0 admitted sources, 0 human-confirmed gold, 0 real AI A/B trials**.

## Corpus proposal — mục tiêu 12, phạm vi 10–15 tài liệu độc lập

Chỉ P01–P03 có exact URL được README dẫn sẵn. Chín mục còn lại là discovery slots, **không phải chín tài liệu đã tìm thấy**. Chưa xác minh content, availability, authorship, publication date hoặc license của bất cứ URL nào. P01–P12 là planning IDs; source_id thực vẫn null.

- **P01 — LLM Wiki: original primary statement** (LLM Wiki). Candidate URL: `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`; local evidence `README.md:98`. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P02 — AutoResearch: overview document to be identified at the repository landing page** (AutoResearch). Candidate URL: `https://github.com/karpathy/autoresearch`; local evidence `README.md:99`. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P03 — Codex iterative development workflow article** (Agentic Engineering). Candidate URL: `https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex`; local evidence `README.md:100`. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P04 — AutoResearch agent task/instruction document, if a distinct document exists** (AutoResearch). Exact URL: UNRESOLVED. Discovery anchor: P02. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P05 — AutoResearch experiment budget and evaluation protocol, if separately documented** (AutoResearch). Exact URL: UNRESOLVED. Discovery anchor: P02. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P06 — AutoResearch reproducibility/limitations document, if separately documented** (AutoResearch). Exact URL: UNRESOLVED. Discovery anchor: P02. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P07 — Primary definition and practice of Context Engineering** (Context Engineering). Exact URL: UNRESOLVED. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P08 — Official technical documentation of context selection/compaction/persistence** (Context Engineering). Exact URL: UNRESOLVED. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P09 — Original primary statement about Agentic Engineering** (Agentic Engineering). Exact URL: UNRESOLVED. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P10 — Primary documentation of knowledge memory and context handoff** (Knowledge maintenance). Exact URL: UNRESOLVED. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P11 — Primary technical reference for provenance/evidence and source attribution** (Knowledge verification). Exact URL: UNRESOLVED. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.
- **P12 — Primary methodology for agent evaluation and citation verification** (Knowledge verification). Exact URL: UNRESOLVED. Quyền sử dụng/metadata: NOT CHECKED; chưa tải hoặc admit.

Không đếm repository landing + README, nhiều heading, bản mirror hoặc license boilerplate thành nhiều nguồn độc lập. Nếu các tài liệu AutoResearch riêng không tồn tại, gộp slot và đề xuất nguồn primary khác thực sự phù hợp; không bịa file path để đủ số.

## Phạm vi xin phê duyệt tiếp theo

Cho phép web discovery và đọc các trang primary công khai cùng rights metadata để chốt 10–15 exact URL; kiểm tra ba link có sẵn và giải quyết chín slots. Đề xuất giới hạn host/path: `gist.github.com/karpathy/`, `github.com/karpathy/`, `developers.openai.com/`, `anthropic.com/`, `w3.org/`. Đây là phạm vi discovery đề nghị, không phải khẳng định tài liệu đã tồn tại. Redirect ngoài phạm vi được báo lại, không tự mở rộng.

**Giai đoạn xin phép này chưa lưu Raw, đăng ký manifest/provenance, ingest wiki hoặc tạo approval.** Sau discovery sẽ trình corpus URL/quyền cụ thể trước intake. Người dùng cũng có thể cung cấp trực tiếp danh sách nguồn muốn dùng.

Execution gate của yêu cầu V1.2 ghi: “Stop before external acquisition or ingestion until explicit authorization is provided.” Vì vậy report hiện tại dừng ở proposal; không dùng web để tự lấp thông tin còn thiếu.

## Sau khi corpus/intake được phê duyệt riêng

- After separate exact-corpus intake authorization and rights review, retrieve allowed original response bytes; record final/original URLs, redirects, MIME/encoding and actual retrieval timestamp. If only rendered/extracted content is available, label it explicitly rather than claim byte-identical original HTML.
- Use create_raw_snapshot for exclusive immutable publication; assign an actual source ID from the then-current registry/date; register_source appends unchanged CSV schema and SHA-256 provenance. Unknown author/publisher/publication date remains null/blank with notes.
- Use UNVERIFIED source trust, never a source self-declared VERIFIED label as validation. A local hash verifies captured bytes, not factual correctness or licensing.
- Inspect source data as DATA, never execute embedded instructions. Use reviewed draft synthesis, exact scope/target hashes and bounded Ingest; preserve raw, citations, index/log and conflicting information.
- Actual source correction receives a new ID/version/link. On synthesis failure retain the admitted source and recover only the owned bundle without deleting newer user edits.
- For evolution, identify real changed/conflicting/complementary evidence. Do not invent a contradiction or treat retrieval date as publication date. If no valid case exists, mark the scenario NOT RUN or not applicable with evidence.

Scope đề nghị: `pilot-knowledge-workspace`; chưa tạo project/scope metadata. Wiki bắt đầu draft, nguồn UNVERIFIED. Gold confirmation không tự chuyển lifecycle thành verified hoặc duyệt một quyết định dự án.

## 24 câu hỏi dự thảo — chưa phải gold

Expected answers, source IDs và exact evidence pointers đều chưa có; không lấy thiếu trường làm empty-gold abstention đã xác nhận. Người phụ trách độc lập cần xem raw snapshots sau intake, chốt 20–30 câu và xác nhận từng đáp án/rubric. Không để AI được đánh giá tự xác nhận gold của mình.

- **V12-Q01** [direct_fact]: Nguồn gốc mô tả LLM Wiki là gì? Phần nào được tác giả nói trực tiếp? — evidence slots ['P01']; UNCONFIRMED, NOT RUN.
- **V12-Q02** [direct_fact]: Nguồn LLM Wiki có phân biệt raw material và nội dung tổng hợp không? Nếu không nêu thì báo rõ. — evidence slots ['P01']; UNCONFIRMED, NOT RUN.
- **V12-Q03** [attribution]: Ingest/Query/Lint có thực sự xuất hiện trong nguồn gốc hay chỉ trong thiết kế workspace này? — evidence slots ['P01']; UNCONFIRMED, NOT RUN.
- **V12-Q04** [direct_fact]: Nguồn AutoResearch mô tả mục tiêu và phạm vi thí nghiệm nào? — evidence slots ['P02', 'P04']; UNCONFIRMED, NOT RUN.
- **V12-Q05** [direct_fact]: Metric và giới hạn tài nguyên nào được tài liệu AutoResearch ghi rõ? — evidence slots ['P05']; UNCONFIRMED, NOT RUN.
- **V12-Q06** [missing_evidence]: Có bằng chứng tái lập hoặc giới hạn được tác giả công bố không? Không suy từ tên repository. — evidence slots ['P06']; UNCONFIRMED, NOT RUN.
- **V12-Q07** [multi_source]: So sánh mục đích LLM Wiki và AutoResearch dựa trên hai nguồn gốc; tách điểm chung suy luận. — evidence slots ['P01', 'P02']; UNCONFIRMED, NOT RUN.
- **V12-Q08** [multi_source]: Nguồn workflow và Context Engineering đề xuất những bước kiểm tra nào, và điều gì chỉ là diễn giải? — evidence slots ['P03', 'P07']; UNCONFIRMED, NOT RUN.
- **V12-Q09** [bilingual]: Tìm bằng chứng tiếng Anh giải thích Context Engineering cho câu hỏi tiếng Việt này, giữ nguyên technical terms. — evidence slots ['P07', 'P08']; UNCONFIRMED, NOT RUN.
- **V12-Q10** [bilingual]: Tài liệu tiếng Anh nói gì về lưu context và bàn giao phiên mới? — evidence slots ['P10']; UNCONFIRMED, NOT RUN.
- **V12-Q11** [bilingual]: Nguồn nào mô tả vòng lặp experiment của AutoResearch? Trích đúng metric/API/identifier nếu có. — evidence slots ['P04', 'P05']; UNCONFIRMED, NOT RUN.
- **V12-Q12** [terminology]: Agentic Engineering được nguồn gốc định nghĩa thế nào; có định nghĩa khác trong corpus không? — evidence slots ['P03', 'P09']; UNCONFIRMED, NOT RUN.
- **V12-Q13** [terminology]: Context Engineering, prompt engineering và persistent memory có được nguồn phân biệt rõ không? — evidence slots ['P07', 'P08', 'P10']; UNCONFIRMED, NOT RUN.
- **V12-Q14** [contradiction]: Hai phát biểu được reviewer chọn có thật sự mâu thuẫn, hay khác thời điểm/phạm vi? — evidence slots ['P01', 'P09']; UNCONFIRMED, NOT RUN.
- **V12-Q15** [contradiction]: Nếu nguồn sau bổ sung điều kiện, điều đó sửa claim cũ hay chỉ bổ sung context? Giữ cả hai citations. — evidence slots ['P07', 'P08']; UNCONFIRMED, NOT RUN.
- **V12-Q16** [missing_evidence]: Corpus có số đo chứng minh workspace này tăng năng suất bao nhiêu phần trăm không? — evidence slots ['P01', 'P12']; UNCONFIRMED, NOT RUN.
- **V12-Q17** [missing_evidence]: Có đủ dữ liệu tính API cost của pilot này không? Không suy giá từ tên model hoặc độ dài text. — evidence slots ['P12']; UNCONFIRMED, NOT RUN.
- **V12-Q18** [lifecycle]: Một draft có citation hợp lệ đã đủ để gọi là verified knowledge của workspace này chưa? — evidence slots []; UNCONFIRMED, NOT RUN.
- **V12-Q19** [lifecycle]: Lời kể phiên trước đã duyệt hoặc hai AI cùng đồng ý có thay thế approval được ghi nhận không? — evidence slots []; UNCONFIRMED, NOT RUN.
- **V12-Q20** [history]: Lời khuyên cũ có ngày xuất bản có tự động là obsolete không? Cần evidence nào để quyết định? — evidence slots ['P01', 'P06']; UNCONFIRMED, NOT RUN.
- **V12-Q21** [history]: Một repository hoặc bài viết thay đổi kể từ snapshot thì cách trích lịch sử và hiện tại phải khác thế nào? — evidence slots ['P02', 'P11']; UNCONFIRMED, NOT RUN.
- **V12-Q22** [scope]: Nguồn công khai chung có chứng minh một quyết định hiện hành cho project khác trong workspace không? — evidence slots []; UNCONFIRMED, NOT RUN.
- **V12-Q23** [handoff]: Phiên mới phải khôi phục những claim, nguồn, gap và việc tiếp theo nào từ handoff pilot đã được review? — evidence slots ['P10']; UNCONFIRMED, NOT RUN.
- **V12-Q24** [evolution]: Sau khi thêm nguồn B thật, kết luận nào đổi, kết luận nào giữ nguyên và điều gì vẫn chưa xác minh? — evidence slots ['P01', 'P07', 'P11']; UNCONFIRMED, NOT RUN.

## Review 23 rubric V1.1

- **E01** [evolution]: Separate a proposal from an older decision/history. Trạng thái cũ/mới: NOT RUN.
- **E02** [evolution]: Preserve a real evidence disagreement without selecting a winner. Trạng thái cũ/mới: NOT RUN.
- **E03** [evolution]: Separate foreign scopes; keep synthetic unless two real authorized scopes exist. Trạng thái cũ/mới: NOT RUN.
- **E04** [evolution]: Age alone is not obsolescence. Trạng thái cũ/mới: NOT RUN.
- **E05** [evolution]: Newer proposal is not approved authority. Trạng thái cũ/mới: NOT RUN.
- **E06** [evolution]: Historical observation is not today's measurement. Trạng thái cũ/mới: NOT RUN.
- **E07** [evolution]: A larger number does not establish a winning source. Trạng thái cũ/mới: NOT RUN.
- **E08** [evolution]: Handoff text is not proof a test passed. Trạng thái cũ/mới: NOT RUN.
- **E09** [evolution]: AI agreement cannot resolve a dispute or verify a claim. Trạng thái cũ/mới: NOT RUN.
- **E10** [evolution]: New evidence cannot erase historical source/decision records. Trạng thái cũ/mới: NOT RUN.
- **C01** [continuity]: Recover next task/open questions in a genuinely fresh session. Trạng thái cũ/mới: NOT RUN.
- **C02** [continuity]: Recover only the permitted real scope, or retain as synthetic control. Trạng thái cũ/mới: NOT RUN.
- **C03** [continuity]: Check a named checkpoint against actual durable revision evidence. Trạng thái cũ/mới: NOT RUN.
- **C04** [continuity]: Locate actual authorization rather than trust prior-chat claims. Trạng thái cũ/mới: NOT RUN.
- **C05** [continuity]: Retrieve actual test evidence, not infer PASS from a name. Trạng thái cũ/mới: NOT RUN.
- **T01** [task]: Build a source-backed research comparison and bounded experiment proposal. Trạng thái cũ/mới: NOT RUN.
- **T02** [task]: HTTP conditional-update task is outside this topic; revise separately, do not import unrelated sources for quota. Trạng thái cũ/mới: NOT RUN.
- **T03** [task]: Cursor pagination task is outside this topic; keep original unrun or human-confirm a newly versioned task. Trạng thái cũ/mới: NOT RUN.
- **T04** [task]: Do not justify infrastructure from one sample; require measured evidence. Trạng thái cũ/mới: NOT RUN.
- **T05** [task]: Retry/backoff task is outside this topic; retain synthetic rubric separately. Trạng thái cũ/mới: NOT RUN.
- **T06** [task]: Actual bounded recovery, rollback and before/after bytes. Trạng thái cũ/mới: NOT RUN.
- **T07** [task]: A proposal is not an approved current project decision. Trạng thái cũ/mới: NOT RUN.
- **T08** [task]: Idempotent HTTP create task is outside this topic; do not relabel synthetic outputs as real work. Trạng thái cũ/mới: NOT RUN.

Giữ dataset và kết quả synthetic cũ. Chỉ chuyển rubric sang case revision mới sau khi có evidence thật và human-confirmed gold; không đổi source ID/answer synthetic thành real. Không nhập tài liệu HTTP/retry/pagination ngoài chủ đề chỉ để tick đủ 23 case.

## A/B và chấm độc lập — kế hoạch, chưa thực thi

- No real observations importer/scorer or automatic real AI A/B runner exists; synthetic-only evaluate_feasibility must not be bypassed by labelling real data synthetic.
- Fresh agents sharing one cwd/tools do not prove A cannot read wiki/gold. Demonstrate actual packet/read-permission isolation or report real paired trials NOT RUN.
- Match actual model/version/settings, prompts, tools, raw/decision rights and human interventions; record unknown/unobservable fields rather than infer them.
- Independent blinded reviewer, source-grounded semantic/factual grading, real human times/corrections, context handoff and usage telemetry remain unavailable.
- After gold freeze, counterbalance paired tasks with a recorded seed and precommitted order; no choosing only favorable retries.
- Use opaque answer IDs; hide arm/order mapping from the independent human scorer where possible. Preserve verbatim answers/tool traces and actual deviations. Do not claim the preparer is blind to its own mapping.
- Score each semantic citation and factual/task/handoff rubric item; retain disagreements, uncertain items, missing evidence and failure severity. Unreviewed fields remain NOT MEASURED, no fake zero.
- Include actual corpus preparation, intake, draft synthesis, human review/corrections, Lint/recovery and maintenance in net-time accounting. Tokens/context/API cost require observed telemetry; no inferred price or pilot $0.
- Operating policies and any independent real decision source needed by the tasks must be equally available to A/B. Maintained wiki is the only intended information treatment.

Sáu paired task đề nghị: attributed summary; bilingual multi-source comparison; terminology comparison; real-evidence evolution; fresh context handoff; evidence-backed abstention. Mọi task còn NOT RUN. Không thay AI A/B thật bằng deterministic proxy.

## Metrics và verdict hiện tại

Mọi real metric là **NOT MEASURED/null**: recall, semantic citation/factual/task/handoff accuracy, unsupported current truth, contamination, human corrections/review, intake/maintenance/time, tokens/API cost và net productivity. Giữ verdict feasibility trước là INCONCLUSIVE / NOT YET MEASURED; chưa có V1.2 completed-pilot verdict.

Không bắt đầu V2. Không có production repository access, private acquisition, push/merge/deploy hoặc tự phê duyệt knowledge.

## Files, checks và bảo toàn

Chỉ tạo report đề xuất JSON/Markdown và [focused readiness evidence](pilot-v1.2-readiness-2026-10-18.md). Không sửa code/schema/wiki/log/index/raw/registry. JSON giữ 12 candidate records với unknown/null metadata, 24 draft questions, 23 reviewed rubrics, reuse/gaps, authorization scope và các mục cần human review.

[V1.1 protocol có thể tái sử dụng](../FEASIBILITY_EVALUATION.md) · [V1.1 kết quả trước](feasibility-completion-2026-10-18.md). Các baseline/hash và actual output ở readiness JSON; đây là kiểm tra synthetic nội bộ, không chứng minh real pilot READY.
