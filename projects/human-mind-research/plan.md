# Human Mind Research — Kế hoạch 40 tuần (bản nháp)

- **Project:** `human-mind-research`
- **Status:** `DRAFT_FOR_REVIEW`
- **Updated at:** 2026-11-05
- **Input được xác nhận bởi người dùng:** một báo cáo Deep Research định dạng **Markdown `.md`**. Chưa có nội dung file trong workspace để kiểm tra.
- **Không giả định:** file ZIP, 28 ghi chú tách riêng, bundles, metadata hoặc trích dẫn đã được kiểm chứng.
- **Cadence đề xuất:** 6–8 giờ/tuần, 40 tuần (~9–10 tháng), có thể giãn thành 11–12 tháng.
- **Trạng thái:** `TODO`, `IN_PROGRESS`, `BLOCKED`, `READY_FOR_REVIEW`, `ACCEPTED_BY_HUMAN`.

## 1. Đầu ra mong muốn

1. **Một báo cáo `.md` gốc được lưu giữ nguyên vẹn** ở vị trí do người dùng phê duyệt, kèm thông tin tên file, ngày nhận và hash khi kiểm được file thực tế.
2. Một bảng đối chiếu 28 chủ đề với **các mục thực sự có trong báo cáo**. Nếu thiếu, ghi `MISSING_IN_REPORT`, không tự bịa phần nội dung.
3. Một lộ trình 40 tuần, nghiên cứu sâu từng chủ đề, active recall, câu hỏi nghiên cứu, bài thực hành an toàn, synthesis và capstone.
4. Bảng nguồn/bằng chứng: `FACT`, `INTERPRETATION`, `HYPOTHESIS`, `UNKNOWN`, vị trí trong báo cáo, nguồn gốc/DOI/URL nếu có, trạng thái kiểm chứng.
5. **Tùy chọn:** 28 note Obsidian phái sinh theo 7 module sau khi báo cáo được đọc và người dùng xác nhận muốn tách. Mỗi note phải ghi rõ phần nào trích/tóm tắt từ báo cáo và phần nào do nghiên cứu bổ sung.

## 2. Các gate

| Gate | Điều kiện hoàn thành | Trạng thái hiện tại |
| --- | --- | --- |
| G0 — Project setup | Có context, plan, checklist và index trên branch review | `IN_PROGRESS`; chờ review/merge |
| G1 — Markdown intake | Người dùng đính kèm `.md`, xác định tên file, kiểm UTF-8/structure, lưu pointer | `BLOCKED`: chưa nhận file thực tế |
| G2 — Coverage audit | Đối chiếu nội dung `.md` với 28 chủ đề, đánh dấu covered/partial/missing | `TODO` |
| G3 — Evidence audit | Rà citation và claim trọng yếu, ghi nguồn, độ chắc chắn và giới hạn | `TODO` |
| G4 — Canonical storage | Chọn nơi lưu bản gốc và commit snapshot đã được review nếu được phép | `BLOCKED`: chờ chọn đích |
| G5 — Learning rollout | Triển khai học, review, research log theo từng module | `TODO` |
| G6 — Capstone | Bài tổng hợp liên ngành và đánh giá nguồn | `TODO` |

**Giới hạn:** không đăng ký/ingest nguồn vào AI-WORKSPACE theo quy trình hiện tại khi chưa có task authorization và điều kiện an toàn. Báo cáo AI không phải chứng nhận tính đúng của các nguồn.

## 3. Workstreams

### W1 — Tiếp nhận đúng báo cáo Markdown

- [ ] Nhận file `.md` từ người dùng, không yêu cầu file nén.
- [ ] Đọc nguyên nội dung và mục lục; kiểm số mục thực tế, bảng, link, bibliography, độ dài và phần bị cắt.
- [ ] Lưu hash, nguồn, ngày nhận và đường dẫn sau khi file thực sự có mặt.
- [ ] Xác định có bao nhiêu trong 28 chủ đề được bao phủ và ở mức nào.
- [ ] Không tự nhận đã đọc nội dung chỉ dựa vào tóm tắt trong hội thoại.

### W2 — Kiểm chứng khoa học

- [ ] Tách claim thực nghiệm khỏi giải thích, giả thuyết, tranh luận và triết học.
- [ ] Với claim quan trọng, tìm evidence pointer trong nguồn gốc; kiểm DOI/URL và mối liên hệ giữa nguồn–claim.
- [ ] Nêu sample, replication, correlation/causation, measurement, publication bias và giới hạn khái quát.
- [ ] Đánh dấu `UNKNOWN` khi thiếu bằng chứng; không suy đồng thuận khoa học từ một bài tổng hợp.
- [ ] Các chủ đề sức khỏe tâm thần và giấc ngủ chỉ dùng thực hành an toàn, không thay tư vấn y tế.

### W3 — Tổ chức tri thức (tùy chọn)

- [ ] Sau khi có báo cáo, hỏi người dùng có muốn **tách 28 note** hay giữ một file.
- [ ] Nếu tách: tạo note theo đúng phần có trong báo cáo, gắn `derived draft` và đường dẫn tới section nguồn.
- [ ] Với chủ đề thiếu nội dung: tạo research backlog thay vì placeholder giả làm note hoàn chỉnh.
- [ ] Nếu dùng Obsidian: frontmatter YAML/wikilinks thuộc vault riêng, không copy nguyên vào `wiki/` của AI-WORKSPACE (schema khác).
- [ ] ChatGPT Project, nếu được tạo, là snapshot có ngày và phiên bản; không phải sync hai chiều.

### W4 — Học tập và đánh giá

- [ ] Research log hằng tuần: nguồn đọc, nội dung hiểu, nghi vấn, retrieval prompts và bước tiếp theo.
- [ ] Sau mỗi module: synthesis 250–400 từ, sơ đồ liên kết và một mini-project an toàn.
- [ ] Tự kiểm tra nhớ lại ở khoảng cách 1/7/30 ngày khi phù hợp; không coi điểm tự đánh giá là tăng IQ.
- [ ] Cuối lộ trình: capstone liên ngành và evidence-gap register.

## 4. Roadmap 40 tuần

| Tuần | Nhóm và chủ đề | Deliverable dự kiến |
| --- | --- | --- |
| 1–4 | Đọc báo cáo `.md`, lập source map, đánh giá coverage, học phương pháp nghiên cứu | Bản audit 28 chủ đề và baseline kế hoạch |
| 5–8 | **I. Sinh học và não bộ** (01–04): tiến hóa, sinh học, thần kinh, neuroplasticity | 4 topic summaries và sơ đồ cơ chế |
| 9–12 | **II. Nhận thức và học tập** (05–08): tri giác, chú ý, trí nhớ, khoa học học tập | Bài thực hành retrieval/spacing và báo cáo giới hạn |
| 13–17 | **III. Trí tuệ và tư duy** (09–13): trí tuệ, tư duy phản biện, thiên kiến, siêu nhận thức, sáng tạo | 5 topic summaries và calibration log |
| 18–21 | **IV. Cảm xúc và hành vi** (14–17): cảm xúc, động lực, thói quen, quyết định | Mô hình quyết định và nhật ký quan sát |
| 22–26 | **V. Giấc ngủ và ý thức** (18–22): giấc ngủ, giấc mơ, ý thức, altered states, hiện tượng nhận thức | Bảng so sánh lý thuyết và mức độ bằng chứng |
| 27–30 | **VI. Con người và xã hội** (23–26): nhân cách, xã hội, phát triển, sức khỏe tâm thần | Synthesis về cá nhân, môi trường và đạo đức |
| 31–32 | **VII. Triết học và ứng dụng** (27–28): triết học tâm trí, thực hành nhận thức | Sơ đồ tích hợp |
| 33–36 | Tổng hợp 7 module, xử lý mâu thuẫn và thiếu nguồn | Knowledge map và evidence-gap register |
| 37–40 | Capstone, tự kiểm tra, audit cuối và retrospective | Báo cáo 3.000–5.000 từ hoặc dự án tương đương |

Lịch có thể thay đổi sau khi kiểm nội dung báo cáo thực tế; 28 topic summaries là **đầu ra dự kiến**, không phải 28 file đã tồn tại.

## 5. Lịch 6–8 giờ/tuần

- **2 giờ:** đọc nguồn gốc/review hoặc phần tương ứng trong báo cáo.
- **1,5 giờ:** đối chiếu claim–evidence, ghi điểm chưa chắc.
- **1,5 giờ:** active recall, giải thích theo Feynman, tự kiểm tra.
- **1,5 giờ:** viết synthesis, sơ đồ, ví dụ và mini-project.
- **0,5 giờ:** research log và kế hoạch tuần sau.

## 6. Rubric đề xuất (0–4 mỗi tiêu chí)

| Tiêu chí | Điểm tối đa | Cách đánh giá |
| --- | --- | --- |
| Độ bao phủ | 4 | Khái niệm, cơ chế, tranh luận, giới hạn |
| Provenance | 4 | Claim quan trọng nối tới nguồn và vị trí kiểm được |
| Độ chính xác | 4 | Diễn giải cân bằng, phân biệt empirical/philosophical |
| Khả năng học | 4 | Retrieval, bài tập, ứng dụng và feedback |
| Tính liên kết | 4 | Liên kết chéo có giải thích, prerequisite rõ |

Ngưỡng review đề xuất ≥16/20, không còn lỗi nguồn nghiêm trọng. Không có điểm số nào đã được đo.

## 7. Rủi ro

| ID | Rủi ro | Hành động |
| --- | --- | --- |
| R1 | Chưa có báo cáo `.md` để đọc | G1 BLOCKED, chờ người dùng đính kèm |
| R2 | Báo cáo không có đủ 28 phần chi tiết | Ghi coverage thực tế, lập backlog bổ sung |
| R3 | Citation hoặc DOI không hỗ trợ claim | Rà nguồn và evidence pointer trước khi chấp nhận |
| R4 | Tách note làm mất bối cảnh nguồn | Giữ bản `.md` gốc, liên kết section và diff |
| R5 | Schema Obsidian và AI-WORKSPACE khác nhau | Vault độc lập, chỉ pointer trong `projects/` |
| R6 | Khẳng định quá mức về IQ, dreams, mental health | Đánh dấu mức độ bằng chứng và thực hành an toàn |
| R7 | Kế hoạch quá tải | Giãn 11–12 tháng và ưu tiên chất lượng |

## 8. Next actions

1. **Đã làm trên nhánh review:** tạo context, plan, checklist, index; sửa giả định ZIP sau khi người dùng làm rõ.
2. **Cần người dùng:** đính kèm báo cáo `.md` gốc.
3. **Sau khi nhận file:** kiểm nội dung và coverage 28 chủ đề; điều chỉnh roadmap theo dữ liệu thực.
4. **Sau khi chọn canonical storage:** lưu snapshot gốc, tạo branch/PR riêng nếu có yêu cầu.
5. **Tùy chọn:** tách 28 note Obsidian theo nội dung đã được kiểm và review.
6. **Tùy chọn/phê duyệt riêng:** đăng ký hoặc Ingest nguồn theo governance AI-WORKSPACE.

## 9. Definition of done

- **Project setup:** files và index tồn tại, được review/merge.
- **Report intake:** đã đọc và kiểm báo cáo `.md` thực tế, ghi vị trí/phiên bản và coverage.
- **Derived notes:** chỉ DONE nếu thực sự tạo, kiểm và lưu các note theo quyết định của người dùng.
- **Scientific review:** chỉ DONE sau khi kiểm nguồn và người duyệt chấp nhận.

Xem [checklist tiếp nhận báo cáo](import-checklist.md) và [project context](context.md).
