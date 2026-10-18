# V1.1 — Đánh giá tính khả thi thực tế

Tài liệu này quy định cách so sánh một quy trình AI có wiki được duy trì với một quy trình AI tương đương chỉ dùng tài liệu nguồn. Mục tiêu là kiểm tra giá trị sử dụng; test hạ tầng thành công không chứng minh năng suất hoặc chất lượng câu trả lời thực tế.

**Tính khả thi thực tế: NOT YET MEASURED** cho đến khi có nguồn thực được phép, gold do người phụ trách xác nhận, hai nhánh AI chạy độc lập và số đo sử dụng có bằng chứng. Không thực hiện V2 theo tài liệu này.

## Điểm xuất phát và phạm vi bằng chứng

- [Independent final audit](reports/independent-final-audit-2026-10-18.md) ghi kết luận NOT READY tại thời điểm audit.
- [Governance remediation](reports/governance-remediation-completion-2026-10-18.md) giải quyết riêng H-GOV-01 và H-GOV-02 bằng test giả lập, không tự đổi kết luận toàn workspace thành READY. Không coi tiền đề “latest Final Audit has passed” là một kết quả đã xác nhận.
- [Workflow reliability](WORKFLOW_RELIABILITY.md) cung cấp fixture, API Ingest/Query/Lint và benchmark lexical có thể tái sử dụng. [Governance](KNOWLEDGE_GOVERNANCE.md), [Source integrity](SOURCE_INTEGRITY.md) và [Security policy](SECURITY_POLICY.md) tiếp tục áp dụng.
- Guide này không cấp quyền nhập nguồn thực, tạo human approval, truy cập repository dự án, mở bí mật, gọi API, mua dịch vụ hay thay đổi permission.

Đánh giá giữ riêng ba tầng: tính đúng của harness; kết quả retrieval và recovery trên dữ liệu giả lập; lợi ích thực tế của AI đối với người dùng. Không suy diễn kết quả tầng sau từ tầng trước.

## Câu hỏi cần trả lời

1. Wiki giúp tìm đúng tài liệu hoặc bằng chứng hơn so với đọc cùng nguồn thô hay không?
2. Câu trả lời có được nguồn hỗ trợ và đúng với nhiệm vụ hay chỉ có citation đúng cú pháp?
3. Khi nguồn thay đổi hoặc mâu thuẫn, hệ thống giữ lịch sử và trình bày trạng thái hiện hành đúng hay không?
4. Một phiên AI mới có khôi phục quyết định, phạm vi và các điểm chưa rõ mà không được gợi ý từ phiên trước hay không?
5. Lợi ích có bù được thời gian tiếp nhận, tổng hợp, review, sửa lỗi, Lint và duy trì wiki hay không?

## Dataset và ground truth

Gold là dữ liệu kiểm thử độc lập với kết quả retrieval. Không sinh gold bằng cách hỏi wiki câu trả lời mong đợi, không đổi expected result chỉ để benchmark đạt và không cho phiên thực thi đọc answer key.

Format và fixture nằm tại `tests/fixtures/feasibility/dataset.json`. Runner là `scripts/evaluate_feasibility.py`; dùng `--help` để xác nhận CLI. Kết quả của một lượt chạy phải có report riêng; sự tồn tại của entry point không phải bằng chứng đã chạy.

Dataset cần có đủ các nhóm riêng, không cộng hai ngôn ngữ của một pair thành hai pair:

- 30 câu hỏi knowledge.
- 20 pair truy vấn Việt–Anh; lưu hai prompt và giữ nguyên API, định danh, tên file, thuật ngữ kỹ thuật.
- 10 ca thông tin mâu thuẫn, superseded hoặc chưa có hiệu lực.
- 10 ca cô lập project, gồm lookup ngoài scope được yêu cầu rõ và trường hợp phải từ chối.
- 5 ca phiên mới, có context packet đầu vào và dữ kiện cần khôi phục.
- 8–10 nhiệm vụ research hoặc coding đại diện cho công việc người dùng.

Mỗi case cần case ID ổn định, nhóm, prompt, relevant source IDs, required citations/pointers, expected scope, decision validity, abstention rule, severity và expected answer hoặc rubric. Nên lưu ngôn ngữ và các lỗi nghiêm trọng riêng như “chọn cấu hình project khác làm hiện hành”. Expected answer không cần một câu văn cố định nếu nhiều cách trả lời cùng đúng.

Mọi tài liệu giả lập ghi TEST_ONLY rõ ràng. Source ID, project và quyết định trong fixture không xác nhận một sự kiện thực. Approval mô phỏng trong disposable fixture không phải human approval của workspace thật.

Để chuyển một case sang pilot thực, người phụ trách phải xác nhận quyền dùng tài liệu, phiên bản nguồn, expected results, citation có ý nghĩa, scope và rubric trước khi chạy hai nhánh. Ghi người xác nhận, ngày và tham chiếu review. Ghi nhận local reviewer ID là thông tin truy vết, không phải cơ chế xác thực danh tính. Chưa có xác nhận thì trạng thái là UNCONFIRMED và không đưa vào điểm factual correctness thực.

## Hai nhánh A/B

### A — Baseline

Cùng model/version/settings và cùng loại tool với B. A nhận task packet, nguồn thô được phép và tài liệu quyết định gốc do con người phê duyệt độc lập. A được dùng search/read tương đương trên nguồn. A không đọc wiki được duy trì, index tổng hợp của wiki, câu trả lời của B, gold hoặc review của trial khác.

Không làm A thiếu dữ kiện: thông tin provenance gốc, ngày nguồn, permissions, scope và quyết định độc lập cần để giải nhiệm vụ phải có trong source packet của cả hai nhánh. Nếu chỉ B nhận một quyết định thật hoặc một nguồn cần thiết thì trial không so sánh được và phải đánh dấu INVALID_COMPARISON. Khi wiki nêu một quyết định chỉ tồn tại dưới dạng tổng hợp AI, không biến nó thành nguồn phê duyệt của A hoặc B.

### B — AI-WORKSPACE

Cùng task packet, raw snapshot, quyết định độc lập và quyền phạm vi như A; thêm wiki, metadata liên kết và các interface Ingest/Query/Lint hiện có. B phải kiểm tra nguồn, phân biệt FOUND với usable_as_current_truth, giữ conflict và lịch sử. Chi phí chuẩn bị/duy trì wiki thuộc B, kể cả khi chuẩn bị trước trial đầu.

Không cấp cho B thêm web, repository, model lớn hơn, số lượt hỗ trợ hoặc quyền thực thi chỉ vì có workspace. Nếu công việc thực tế cần quyền khác, cấp giống nhau cho cả hai nhánh và ghi lý do trước khi chạy.

### Kiểm soát thí nghiệm

1. Chốt dataset/hash, model ID cùng version nếu provider cung cấp, settings, instructions, tool inventory, permission boundary và raw corpus/hash. Chụp wiki revision cho B; giữ task answer key ở nơi hai nhánh không đọc được.
2. Với mỗi case tạo hai phiên AI mới, tắt/không mang lịch sử task trước và ghi session ID thật. “Gọi lại hàm Python” không phải một phiên AI độc lập. Nếu không thể tắt memory hoặc xác nhận model version, ghi hạn chế; không tự điền phiên bản suy đoán.
3. Dùng seed lưu trong protocol để chia thứ tự AB/BA cân bằng theo nhóm và batch; lưu lịch chạy trước khi thực thi. Không chỉ chạy toàn bộ A trước rồi B. Chạy mỗi arm một lần trong một pair; retry có nguyên nhân được ghi là retry, không chọn kết quả đẹp hơn.
4. Phân quyền và đường dẫn phải thực sự chặn A đọc maintained wiki. Nếu host không hỗ trợ hạn chế tương đương, dùng hai task packet/thư mục cho phép riêng và audit tool trace; báo rõ độ tin cậy của việc cô lập. Một lời nhắc “đừng đọc wiki” không chứng minh isolation.
5. Dùng prompt nội dung giống nhau, cùng thời hạn, budget và chính sách hỏi người dùng. Khác biệt được phép là khả năng truy cập maintained wiki. Ghi mọi human intervention, câu trả lời bổ sung và số phút; cung cấp dữ kiện bổ sung giống nhau nếu chúng ảnh hưởng tính công bằng.
6. Bản trả lời lưu nguyên bản, citations và tool evidence cục bộ; không ghi secret vào artifact. Reviewer đánh giá bản đã ẩn arm/order khi làm được, đối chiếu nguồn gốc và rubric đã chốt. Ghi lúc reviewer không thể blind vì format lộ nhánh.
7. Đối chiếu hash sau run để phát hiện đổi corpus/wiki giữa trial. Không sửa nguồn hoặc trạng thái knowledge để cứu một câu trả lời sai. Nếu fixture hoặc gold lỗi, lập revision riêng, giữ kết quả cũ và chạy lại cả pair.

Tính tương đương permissions có nghĩa hai nhánh có cùng năng lực và quyền dữ kiện gốc; chênh lệch wiki là treatment có chủ đích. Không coi hash của hai đường dẫn root khác nhau là bằng chứng chúng có quyền tương đương: cần đối chiếu inventory cho phép đọc, scope và tool capability.

### Synthetic component proxy được triển khai trong harness

Trong harness, A là lexical scan trên raw fixtures có cùng scope, source metadata và quyền; B gọi Query helper thực trên wiki được dựng từ đúng những nguồn đó. Hai nhánh không dùng model AI. A không đọc wiki. So sánh này đo ảnh hưởng của representation/search path trong fixture đã chọn, không phải “cùng AI có/không có memory”.

Fixture source text và wiki metadata khác nhau có chủ đích: wiki có aliases, synthesis và liên kết được duy trì. Chênh lệch recall có thể do curated aliases hoặc bố cục/từ khóa của fixture; không tự quy thành khả năng reasoning, semantic retrieval hay dịch tự động. Ghi raw/gold/wiki fingerprint, seed và thứ tự chạy trong report để reviewer tái tạo và xem thiên lệch thiết kế.

Các số có thể đo trực tiếp gồm nguồn trả về, citation structural validity, output scope/current flags và elapsed wall-clock của component. Elapsed này không bao gồm AI/human và không phải CPU usage. Rubric cho research/coding, factual correctness của AI, semantic citation accuracy, cross-session agent continuity, human correction/time, token/cost và net productivity vẫn NOT MEASURED dù fixture retrieval trả đúng ID.

## Hợp đồng observations cho pilot thủ công

Runner hiện tại chỉ chạy synthetic deterministic components; **không có CLI import real observations hoặc tự chạy AI A/B**. Các observations dưới đây là hợp đồng thu thập thủ công cho pilot được cho phép sau này, không phải interface đã triển khai. File observations chỉ là artifact được khai báo, không tự chứng minh các phiên AI hoặc human review đã xảy ra. Một scorer tương lai cần tách số liệu imported khỏi số liệu runner tự đo và giữ hash của file, dataset và bằng chứng đính kèm. Không nhập rồi tự đổi gold synthetic thành gold real đã xác nhận.

Mỗi observation cần mô tả tối thiểu:

- `case_id`, `arm` A/B, run/trial ID, batch, thứ tự chạy, session ID và task packet revision.
- Model provider/ID/version/settings; tool và permission fingerprint; raw corpus fingerprint; wiki revision cho B và giá trị không áp dụng cho A.
- Prompt và answer artifact, retrieved source IDs theo thứ tự, citation targets/pointers, tool trace hoặc evidence reference.
- Human interventions và lý do; elapsed task time; thời gian review/sửa; số correction theo cùng đơn vị.
- Token usage, context size và API cost chỉ khi có telemetry/receipt. Field chưa quan sát được là null cùng reason, không là 0.
- Human review gồm reviewer, nguồn review, các điểm rubric độc lập, quyết định abstention/scope/current truth và hạn chế blind review.

Chưa có schema import có thể thực thi cho các observations thực; phải review artifact thủ công. Khi bổ sung scorer trong một nhiệm vụ riêng, định dạng field cụ thể cần schema độc lập được kiểm tra, không mặc định một bản JSON tùy ý là hợp lệ. Missing pair, trùng arm/run, sai hash, khác model/tools/source rights hoặc thiếu evidence cần báo không so sánh được, thay vì lặng lẽ ghép nhầm trial. Một record khai `human_review=true` không đủ để tuyên bố đã kiểm chứng human identity hoặc factual truth.

## Metrics và rubric

Mỗi metric lưu status MEASURED / ESTIMATED / NOT MEASURED, số mẫu, numerator/denominator khi có và evidence reference. Trạng thái NOT YET MEASURED mô tả kết luận feasibility thực; dùng NOT MEASURED cho từng metric chưa có quan sát. ESTIMATED phải ghi phương pháp/giả định và không cộng vào tổng đo thực như dữ kiện đã quan sát.

- **Recall@5:** với một query có relevant source IDs độc lập, tính số relevant IDs xuất hiện trong top 5 distinct retrieved IDs chia tổng relevant IDs. Macro-average trên query có nonempty gold; báo số query bị loại vì empty gold, VI/EN riêng và phân phối theo nhóm. Nếu interface chỉ trả một lexical score tier, đó là top 5 của output hiện có, không giả định một full ranking không được thực thi. Không có output truy xuất của baseline thì Recall@5 của A là NOT MEASURED.
- **Citation structural validity:** nguồn tồn tại, đúng ID/path/hash/pointer và truy vết được tại snapshot. Báo valid citations / citations kiểm tra; câu trả lời không có citation không được đạt 100% do mẫu số 0. Missing required citations tính riêng theo case.
- **Citation accuracy về nghĩa:** reviewer đối chiếu từng claim cần bằng chứng với đoạn nguồn; 2 = hỗ trợ đủ và đúng phạm vi/thời điểm, 1 = chỉ hỗ trợ một phần, 0 = không hỗ trợ hoặc mâu thuẫn. Báo phân phối, số claim/citation được chấm và số chưa review. Citation đúng đường dẫn không tự nhận điểm này.
- **Task correctness:** rubric theo task chốt trước; 2 = đạt tất cả tiêu chí bắt buộc, 1 = đúng một phần nhưng còn sai/gap quan trọng, 0 = sai hoặc không thực hiện yêu cầu. Coding task cần actual output/check phù hợp; research task cần factual/source review. Synthetic keyword hits không tự nhận điểm correctness của AI.
- **Continuity:** phiên mới khôi phục đủ dữ kiện/decision IDs, lý do, scope và gap đã chốt mà không nhận answer từ phiên trước; báo số rubric item đúng / item áp dụng. Một test subprocess chỉ đo continuity của file/API, không đo context continuity của agent.
- **Scope leakage:** số query có foreign-scope evidence được dùng ngoài explicit scope/cross-ref cho phép / query chạy. Tách “retrieved as explicit context” khỏi “dùng như current project truth”.
- **Unsupported current-truth assertion:** số claim hiện hành không có đủ source/valid decision supporting evidence / claim hiện hành được chấm; ghi cả case rate. Trường hợp đủ dữ liệu nhưng AI abstain là recall/task outcome, không phải unsupported assertion.
- **Knowledge evolution:** kiểm tra raw A/B và provenance giữ nguyên, cả hai citation tồn tại, conflict/state đúng, superseded khác disputed, index/log nhất quán và các file ngoài scope giữ hash. Đó là structural/governance correctness; semantic detection của AI cần reviewer riêng.
- **Ingestion/recovery:** successful expected operations / attempts, idempotent retries riêng, expected fault rejection riêng. Rollback phải khôi phục reviewed before-images mà không xóa source đã admit hoặc thay đổi dữ liệu người dùng. Báo mã lỗi và hash, không chỉ exit 0 của probe.
- **Human corrections:** số issue theo taxonomy cố định và số vòng sửa; không đếm edit keystrokes khác nhau thành số lỗi tùy ý. Ghi review minutes riêng với correction minutes và thời gian người dùng cung cấp context.
- **Elapsed time:** dùng monotonic clock quanh thao tác thực thi; ghi rõ bao gồm/exclude queue, tool latency và waiting human. Benchmark Python latency chỉ là chi phí local retrieval, không phải elapsed AI task time.
- **Tokens/context/API cost:** chỉ ghi từ telemetry/provider receipt của đúng run. Không suy từ độ dài text, model pricing hiện tại hoặc một trial khác; không coi không gọi API trong harness là model cost $0 của pilot.

Không gộp các metric khác đơn vị thành “AI tốt hơn X%”. Báo A/B theo từng cặp hợp lệ, số thắng/hòa/thua cùng raw deltas và nhóm task. Mẫu nhỏ/correlated paraphrases không đủ cho kết luận thống kê hoặc production SLA. Nếu tính uncertainty thì ghi phương pháp, đơn vị lấy mẫu và giả định; không tự gọi một pair là hai mẫu độc lập.

## Knowledge evolution và giá trị tích lũy

Synthetic integration phải chạy actual immutable admission → Ingest → Query → introduce Source B → Ingest → Query → Lint. Giữ raw A/B cùng lineage; thay đổi synthesis qua controlled transition hoặc draft thay thế, không sửa nội dung verified theo đường tắt. Ghi hash các trang không liên quan, nguồn, index và log trước/sau. Chạy Query trong một process mới để đo khả năng đọc persisted state, với nhãn rõ rằng agent-session correctness vẫn chưa đo.

Pilot AI thực thêm bước phiên mới độc lập, trả lời câu hỏi initial/current/history và tự giải thích điểm thay đổi có citations. Nếu B không đủ để kết luận supersession, trạng thái phải disputed/unknown thay vì chọn winner. Reviewer xem cả nguồn, không chỉ wiki đã tổng hợp.

Đo compounding theo ít nhất ba batch nguồn tăng dần trong cùng một đợt thử nghiệm khi được phép. A nhận toàn bộ raw/history hợp lệ đến batch hiện tại; B nhận đúng cùng raw/history cộng wiki revision đã duy trì. Không cho A chỉ đọc batch mới trong khi B giữ toàn lịch sử. Mỗi batch dùng prompt chưa thấy để hạn chế ghi nhớ câu hỏi; phiên thực thi mới cho từng arm.

Lưu số sources/pages, maintenance operations/time, repeated research/tool steps, prior-decision recovery, ability to identify changes và correctness theo batch. “Nhiều file hơn” hoặc “retrieval nhanh hơn trên fixture” chưa phải compounding value. Chưa có AI runs/human observations thì các metric này NOT MEASURED.

## Năng suất ròng và tổng chi phí

Với cùng tập task đạt chất lượng yêu cầu, ghi riêng tổng thời gian AI/tool, human task/review/correction/context và wiki maintenance. B bao gồm initial setup cần thiết cho pilot, source registration, synthesis, review, Lint, conflict resolution và recovery. A bao gồm source preparation tương đương, tìm lại nguồn và tái cung cấp context; không miễn các chi phí này hoặc tự cộng chi phí chưa quan sát.

Định nghĩa trước cách phân bổ shared intake/setup cho batch và số lần sử dụng. Báo cả chi phí một lần lẫn marginal task cost; không chỉ báo task time của B sau khi bỏ hết maintenance ra ngoài.

Net human time saved = tổng human minutes của A − tổng human minutes của B gồm maintenance phân bổ. Net elapsed/task time và monetary cost là số riêng; không cộng phút của người với phút wall-clock trùng lặp. Không monetise thời gian nếu chưa có đơn giá do người dùng cung cấp; phần đó là ESTIMATED.

Task không đạt quality gate không được báo năng suất tăng chỉ vì kết thúc sớm. Báo incomplete/failed task và repair burden cạnh thời gian. Chưa đo đủ thành phần thì net productivity là NOT MEASURED, dù một thành phần retrieval latency đã có số.

## Trình tự chạy có thể review

1. Kiểm tra branch, diff và protected baselines. Không làm trên main; bảo toàn raw, registry, lịch sử và uncommitted work. Chốt report filename mới, không ghi đè report cũ.
2. Chạy harness synthetic bằng Python standard library. Expected artifacts: dataset/hash, từng case actual output, metrics có denominator, evolution/recovery evidence, code fingerprints và known limitations. Synthetic load chỉ nằm trong disposable test workspace.
3. Kiểm tra failed test và metric bằng actual output; sửa defect trong phạm vi, giữ gold độc lập và chạy lại affected test. Strict Lint không chứng minh citation nghĩa đúng hoặc human review xảy ra.
4. Lưu một report mới qua bounded report API. Entry point: `python -B scripts/evaluate_feasibility.py --output reports/feasibility-v1.1-2026-10-18-rerun.json`. Không lặp lại với cùng tên nếu report đã tồn tại; dùng suffix mới.
5. Đọc actual report trước khi bàn pilot. Nếu chưa có curated sources và reviewer, dừng với real-world feasibility NOT YET MEASURED; không tự nhập nguồn thực để lấp phần thiếu.
6. Khi có nhiệm vụ pilot được người dùng cho phép riêng: lập source/permissions packet và human-confirmed gold, thu observations từng pair trong fresh sessions, rồi review artifact thủ công. Runner hiện tại không thực hiện phần này. Chỉ bổ sung import/scoring khi có phạm vi được duyệt riêng và tests kiểm tra dữ liệu quan sát.
7. Reviewer đối chiếu artifacts và các cặp bị loại. Lưu phiên bản report mới, không sửa kết quả gốc. Quyết định tiếp theo vẫn ở phạm vi V1; báo cáo này không cấp quyền V2.

Một pilot khởi đầu có thể chọn tối đa 8 representative task pairs để review thủ công trong một checkpoint, cùng các nhóm retrieval/governance bổ trợ. Đây là giới hạn công việc đề xuất để dễ kiểm tra, **không phải ngưỡng đã chứng minh đủ mẫu**. Số mẫu và success criteria thực phải chốt trước với người phụ trách. Không giảm yêu cầu đầy đủ của reusable dataset vì chọn subset cho pilot đầu.

## Quy tắc verdict

- **VIABLE:** có lợi ích thực tế đo được trên những pair so sánh được, quality không suy giảm ngoài tiêu chí đã thỏa thuận, chi phí/maintenance chấp nhận được và không có critical governance failure. Automated PASS riêng lẻ không đủ.
- **PROMISING:** có bằng chứng thực về một phần lợi ích nhưng số mẫu, chi phí hoặc hạn chế còn quan trọng. Synthetic proxy thắng không tự đủ điều kiện này.
- **NOT YET VIABLE:** bằng chứng đáng tin cậy cho thấy chi phí vượt lợi ích hoặc còn lỗi correctness/governance nghiêm trọng cản use case được đánh giá. Không dùng nhãn này chỉ vì chưa có dữ liệu thực.
- **INCONCLUSIVE:** thiếu curated gold, independent sessions, human scores, usage observations hoặc dữ liệu không so sánh được. Đây là verdict phù hợp khi mới xác nhận synthetic harness.

Mỗi report cần methodology, dataset characteristics, baseline/B outputs, paired comparison, reliability failures, knowledge evolution, productivity/cost, human burden, limitations, V1 recommendations và V2 recommendation. Nếu chưa đo AI A/B thực, các mục đó vẫn xuất hiện với NOT MEASURED và lý do; không thay bằng số đo proxy mà bỏ nhãn.

## Rủi ro và giới hạn cần giữ rõ

Kết quả lexical với aliases được curate không chứng minh semantic search, translation tổng quát hoặc answer accuracy. Output trên nguồn giả lập không dự đoán tài liệu riêng, dữ liệu nhiều nhiễu hoặc prompt injection mới. Human local records chưa xác thực danh tính. Host tool containment, physical power loss, dense dependency graph performance và những phát hiện Medium/Low từ independent audit chưa tự được giải quyết bởi một runner mới.

Không chạy web/API, tải dữ liệu, truy cập secret hoặc production repository để hoàn thiện metric thiếu. Không nhập real knowledge, phê duyệt quyết định thực, tạo database/QMD/vector/RAG, push, merge, deploy hoặc bắt đầu V2. Kết thúc sau report và đề xuất nhỏ dựa trên kết quả đã quan sát.
