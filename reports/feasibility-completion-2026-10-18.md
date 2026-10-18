# V1.1 — Báo cáo tính khả thi và hoàn tất evaluation harness

**Verdict: INCONCLUSIVE. Real-world feasibility: NOT YET MEASURED.**

No curated real corpus, independent human-confirmed gold, equivalent same-model AI A/B trials, human review burden or observable usage/cost data. Synthetic component gains cannot establish practical value.

## 1. Methodology

Đã hoàn tất synthetic harness trước pilot thực. A quét raw, B dùng Query/wiki thật; cả hai có cùng raw bytes và scope packet. Đây là component proxy, không phải cùng một AI chạy hai workflow. Seed 1101, shuffle rồi cân bằng AB/BA. Model/settings không áp dụng cho proxy; chưa có independent same-model AI A/B trials.

Đã đọc policies/schema/prompts, current APIs/tests, independent audit và remediation. Tiền đề latest whole-system audit đã PASS chưa được xác nhận; hai lỗi High đã xử lý không tự nâng workspace lên READY.

## 2. Dataset

30 tài liệu English giả lập; 103 case: knowledge30, bilingual40/20pair, evolution10, scope10, continuity5, research/coding8. Gold độc lập với wiki/Query nhưng AI-authored synthetic, chưa phải human-confirmed real gold. Mỗi case có prompt, nguồn/citation, scope, expected authority, rubric, abstention và severity.

80 retrieval cases chạy hai nhánh = **160 arm executions**. **23 protocol-only rubrics vẫn NOT RUN**; generic evolution và một readback độc lập không thay thế toàn bộ những rubric này.

## 3. Baseline A và 4. AI-WORKSPACE B

- Source Recall@5: A **0.555556**, B **0.750000**, mỗi arm có 72 query nonempty gold.
- Retrieval outcomes: {"A": {"HIT": 40, "MISS": 32, "CORRECT_ABSTENTION_SIGNAL": 8}, "B": {"HIT": 54, "MISS": 18, "CORRECT_ABSTENTION_SIGNAL": 8}}. MISS được giữ là lỗi retrieval, không biến thành PASS.
- Citation cấu trúc: A 45/45, B 57/57. Citation source-ID relevance gold: A 42/45, B 56/57. Cả hai chưa phải citation semantic accuracy.
- Cross-project leakage: A 0/80, B 0/80. Wiki current flags: 0/57 ở corpus unverified; chưa đo unsupported assertions của AI.
- Mean local query elapsed: A 0.533477s, B 0.633243s. Đây là một lượt có cache/system activity không kiểm soát, không phải AI task time hoặc bằng chứng tốc độ tốt hơn.

## 5. Paired comparison

{"tie": 38, "B_higher": 24, "A_higher": 10, "excluded_empty_gold": 8}

Các số trên chỉ mô tả output của raw adapter và wiki helper. Curated aliases/representation là khác biệt được đo; raw adapter không đại diện năng lực một AI biết tự tìm tài liệu, dịch truy vấn hoặc reasoning. Không suy ra practical advantage từ chênh lệch này. JSON có breakdown VI/EN, từng miss, query/scope và source IDs.

## 6. Reliability failures và test

**234/234 test PASS**, zero failure/error/skip: 219 regressions cũ + 15 test mới. Code/test hashes giữ nguyên trong run và khớp implementation checkpoint `b533de2`. Strict Lint sau update có 0 errors, một cảnh báo NO_EVIDENCE có sẵn. Infrastructure harness PASS chỉ kiểm tra execution/preservation/integrity; B vẫn có 18 miss.

Trước recorded benchmark, review độc lập phát hiện scorer có thể đếm hơn 5 source từ một trang và chấp nhận pointer NoEvidence. Đã sửa, thêm test pointer/hash/cap/missing evidence, đồng thời tách per-case MISS khỏi infrastructure verdict. Không thay gold để tăng điểm.

## 7. Knowledge evolution và continuity

Actual admission A → draft Ingest → unverified Query → admit B mâu thuẫn → controlled draft update → injected failed write → exact rollback → retry → disputed Query/Lint đã chạy. Hai raw histories, citations/conflict, lifecycle/index/log và trang không liên quan được bảo toàn; không tạo approval của con người.

Một agent `fork_turns=none` chỉ nhận fixture/root/query/scope đã đọc lại hai mức 60 và 45 requests/minute, trả DISPUTED, conflict chưa resolve, current=false. Root Query và hash check xác nhận lại persisted state. Đây là một synthetic readback, không phải chấm 5 continuity cases hoặc đánh giá fact bởi người dùng. Báo cáo continuity lưu snapshot/hashes trước khi fixture tạm được xóa.

Ba batch 10/20/30 nguồn chạy cùng bốn câu hỏi: A/B Recall@5 đều 1.0. Chưa có bằng chứng tăng compounding practical value, giảm lặp research hoặc khôi phục quyết định tốt hơn qua nhiều task thực.

## 8. Productivity/cost và 9. Human burden

Máy thực hiện 30 lần admission/synthesis/lifecycle giả lập trong tổng 114.138495s; toàn harness 237.903886s. Tạo nội dung bằng fixture template, không có AI synthesis/human review time trong các số này. Một phần benchmark chạy cùng regression nên latency chỉ là diagnostic.

Human corrections, review/maintenance minutes, real AI task correctness/time, context/tokens/API cost và net productivity: **NOT MEASURED**, lưu null; không coi chưa quan sát là 0 hoặc chi phí pilot $0.

## 10. Limitations

- A deterministic raw adapter is not a competent AI baseline; B curated aliases and layout can improve fixture recall without improving real reasoning or productivity.
- B still misses 18/72 nonempty-gold cases; A misses 32/72. Lexical full-phrase matching misses unlisted paraphrases and grouped keyword strings such as request timeout timeout_ms when queried by a shorter phrase.
- Structural citations and source-ID gold agreement do not prove claim meaning or factual truth; synthetic gold itself lacks independent human confirmation.
- All main-corpus pages remain unverified, so this does not measure practical use of human-approved current decisions. Existing governance behavior remains covered by prior regressions.
- Twenty-three case-specific protocol rubrics, actual coding/research output, paired AI fresh sessions and real compounding value remain NOT RUN/NOT MEASURED.
- Human identity, host containment, physical power loss, dense dependency graphs and earlier Medium/Low audit findings are unchanged residual risks.

## 11. V1 recommendations

- Review exact keyword phrases and API/identifier entries separately instead of joining unrelated terms into one phrase. Keep unlisted paraphrases as holdout gold; do not rewrite expected results to make the benchmark pass.
- Preserve HIT/MISS, citation meaning and current-authority outcomes as separate metrics; prioritize human source review over increasing file count.
- If a pilot is separately authorized, curate a small nonsensitive corpus, human-confirm gold and permissions, freeze model/tools and run balanced independent A/B sessions with the same raw/decision access.
- Collect complete intake/synthesis/review/correction/Lint/conflict overhead alongside task outcomes before estimating reusable value or considering infrastructure upgrades.

## 12. V2 recommendation

Do not start V2. No practical-value or net-cost evidence currently justifies it; do not introduce QMD, embeddings, database or framework on these proxy scores.

## Files, evidence và sử dụng

- [Protocol, rubric và real-pilot guide](../FEASIBILITY_EVALUATION.md)
- [Dataset format](../tests/fixtures/feasibility/README.md) · [103 case specs](../tests/fixtures/feasibility/dataset.json)
- [Benchmark runner](../scripts/evaluate_feasibility.py) · [Evolution runner](../scripts/feasibility_evolution.py)
- [Component results](feasibility-v1.1-2026-10-18.md) · [Full regression](feasibility-regression-2026-10-18.md) · [Independent readback](feasibility-continuity-2026-10-18.md) · [Inspection/plan](feasibility-inspection-2026-10-18.md)

Reproduce: `python -B scripts/evaluate_feasibility.py --seed 1101 --output reports/feasibility-rerun-unique.json`. Existing reports are exclusive: chọn tên mới mỗi lần. `python -B -m unittest discover -s tests -v` chạy regression; `python -B scripts/check_workspace.py --integrity --security` chạy Lint. Không có real-observations importer hoặc tự gọi AI A/B.

JSON đi kèm liệt kê đầy đủ files read/changed, lệnh/kết quả, code/dataset hashes, expected/observed protected hashes, breakdown và phần NOT MEASURED. Trước/sau kiểm tra giữ 16 tệp nguyên vẹn cùng đúng 27166 byte log cũ; log chỉ append, index chỉ thêm guide link. Raw/manifest/provenance vẫn không có source thực; user Obsidian và 10 audit report cũ không bị đưa vào checkpoint.

No new permission is required to finish this authorized synthetic harness. Real sources, human-confirmed gold, source rights and real pilot task/tool scope need a separate direct user task. No real knowledge or decision approval was created.

Dừng sau báo cáo. Không nhập real knowledge, gọi external service, sửa production repository, deploy/push/merge hoặc bắt đầu V2.
