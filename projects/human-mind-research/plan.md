# Human Mind Research — Kế hoạch triển khai và học tập (40 tuần)

- **Project:** `human-mind-research`
- **Plan status:** `DRAFT_FOR_REVIEW`
- **Updated at:** 2026-11-05
- **Scope:** quản trị artifact nghiên cứu và lộ trình học, **không** thực hiện source intake/Ingest
- **Basis:** bản tóm tắt gói Deep Research do người dùng cung cấp; các nội dung file gốc chưa được đối chiếu
- **Target cadence:** 6–8 giờ/tuần, 40 tuần (~9–10 tháng); có thể giãn 11–12 tháng khi cần
- **Tracking convention:** `TODO`, `IN_PROGRESS`, `BLOCKED`, `READY_FOR_REVIEW`, `ACCEPTED_BY_HUMAN`

## 1. Kết quả mong muốn

1. Một canonical Obsidian vault/repo chứa đủ **28 note chi tiết**, chia 7 module và có liên kết chéo, cùng `00-START-HERE.md`, `MASTER-REPORT.md`, `AI_CONTEXT.md`, `RESEARCH-ROADMAP.md`, `SCHEMA.md`, reading list, bibliography và research log.
2. Mỗi note có: frontmatter YAML phù hợp vault, tóm tắt, prerequisite, 5–8 câu hỏi nghiên cứu, thuật ngữ, cơ chế, nguồn/bằng chứng, giới hạn và tranh luận, ví dụ, bài tập retrieval, mini-project, liên kết Obsidian, nguồn tham khảo và câu hỏi mở.
3. Một bảng đối chiếu claim–source–vị trí bằng chứng, giữ rõ `FACT` / `INTERPRETATION` / `HYPOTHESIS` / `UNKNOWN`; không suy diễn “đã verified” từ tổng thuật AI.
4. Kế hoạch học có checkpoint và capstone; các kết quả thực tế được ghi lại, không tự tạo điểm số hoặc tuyên bố đã hoàn thành.

## 2. Trạng thái và các gate

| Gate | Điều kiện hoàn thành | Trạng thái 2026-11-05 |
| --- | --- | --- |
| G0 — Project metadata | `projects/human-mind-research/` có context, plan, manifest và index liên kết | `IN_PROGRESS` trên nhánh review |
| G1 — Package integrity | Có ZIP thực tế; kiểm 28 note, file lõi, cấu trúc, metadata, links và checksum | `BLOCKED`: chưa nhập được artifact để đối chiếu |
| G2 — Evidence review | Citation có URL/DOI truy được; claim quan trọng có evidence pointer, ghi mức độ chắc chắn và tranh luận | `TODO`: chưa duyệt |
| G3 — Canonical vault | Xác nhận repository/vault độc lập, commit snapshot đã review, có rollback | `BLOCKED`: chờ chọn đích |
| G4 — AI-WORKSPACE integration | Chỉ pointer và snapshot metadata được cập nhật; source intake riêng nếu cần | `TODO` |
| G5 — Learning rollout | Mỗi module có note được duyệt, active recall và log học tập | `TODO` |
| G6 — Capstone | Bài tổng hợp, kiểm tra lại nguồn, giới hạn và kết quả học | `TODO` |

**Không vượt gate:** báo cáo AI/ZIP không phải quyền đăng ký nguồn, quyền tái phân phối hoặc xác nhận thực nghiệm. Quy trình real-source intake của AI-WORKSPACE hiện còn HOLD theo tài liệu hiện hành.

## 3. Phân rã công việc (workstreams)

### W1 — Nhập và kiểm tra gói nghiên cứu

- [ ] Nhận `human-mind-research.zip` hoặc `human-mind-research-obsidian.zip` từ kết quả Deep Research.
- [ ] Kiểm kê thực tế từng đường dẫn, kích thước, UTF-8, tên file, trùng lặp, link nội bộ, file rỗng và 7 bundles.
- [ ] So sánh `MASTER-REPORT.md`, `NOTE-MAPPING.md`, `REFERENCES.md` với 28 note; ghi mọi sai lệch.
- [ ] Đánh dấu rõ “AI-generated draft”, nguồn đã truy được, nguồn chưa kiểm và claim không có nguồn.
- [ ] Giữ gói ZIP ban đầu bất biến để có thể so diff sau biên tập.

### W2 — Chuẩn hóa tri thức

- [ ] Mỗi note có ID, title_vi, scope, status `draft` hoặc `unverified`, created/updated date có căn cứ, related topics.
- [ ] Dùng YAML frontmatter và wikilinks **chỉ trong canonical Obsidian vault**. Không sao chép nguyên vào `wiki/` của AI-WORKSPACE vì `SCHEMA.md` ở đó dùng metadata bullets và Markdown links.
- [ ] Claim thực nghiệm phải có citation và vị trí cụ thể (section/page/figure khi có); DOI/URL chỉ là locator, không chứng minh tính đúng.
- [ ] Nêu giới hạn nghiên cứu: sample, replication, causal inference, measurement, population, publication bias.
- [ ] Không đưa bài tập can thiệp sức khỏe hoặc giấc ngủ thiếu an toàn; mental health là kiến thức giáo dục, không thay chẩn đoán.
- [ ] Kiểm định mọi nguồn trước khi đổi status; `verified` chỉ sau human review theo quy trình của kho tương ứng.

### W3 — Liên kết và xuất bản có kiểm soát

- [ ] Chọn vault/repo độc lập làm source of truth; giữ lịch sử Git và pull request cho review.
- [ ] Kiểm tra Obsidian backlinks/Graph View, metadata, anchors, missing note và link URL ngoài.
- [ ] Rebuild 7 bundles từ note đã review; lưu ngày và commit/hash trong upload manifest.
- [ ] Upload snapshot phù hợp giới hạn ChatGPT Project; ghi rõ snapshot date và không gọi đó là sync.
- [ ] Nếu muốn dùng nguồn nghiên cứu trong live AI-WORKSPACE Ingest, xin phê duyệt riêng cho từng artifact và xử lý blocker hiện hành trước.

### W4 — Học tập, thực hành và đánh giá

- [ ] Mỗi tuần có nhật ký: nguồn đã đọc, điều đã hiểu, điều chưa chắc, retrieval prompts, bài thực hành và bước tiếp theo.
- [ ] Sau mỗi module viết synthesis 250–400 từ, ít nhất 10 retrieval prompts/topic, 2 liên kết chéo có giải thích.
- [ ] Đánh giá sau 1, 7 và 30 ngày khi có thể; không xem tự đánh giá là bằng chứng tăng IQ hay thay đổi não.
- [ ] Ghi một mini-project thực tế mỗi module và một capstone liên ngành cuối lộ trình.

## 4. Roadmap 40 tuần

| Tuần | Module / trọng tâm | Deliverable | Checkpoint |
| --- | --- | --- | --- |
| 1–4 | Thiết lập phương pháp: kiểm gói, provenance, đọc nghiên cứu, thiết kế active recall | Vault/repo được chọn; baseline 28 note; source map và rubric | **M1:** G1–G3 sẵn sàng hoặc nêu blocker |
| 5–8 | **01 Foundations:** tiến hóa người, sinh học, thần kinh học, neuroplasticity (01–04) | 4 note được review; sơ đồ từ cơ chế sinh học đến nhận thức | Kiểm tra các “neuromyth” |
| 9–12 | **02 Cognition:** perception, attention, memory, learning (05–08) | 4 note; thiết kế thử nghiệm học tập cá nhân an toàn | **M2:** retrieval/spacing và giới hạn |
| 13–17 | **03 Intelligence:** intelligence, critical thinking, biases, metacognition, creativity (09–13) | 5 note; bộ câu hỏi phản biện và calibration log | Tách đo lường trí tuệ khỏi tuyên bố tăng IQ |
| 18–21 | **04 Behavior:** emotion, motivation, habits, decision-making (14–17) | 4 note; mô hình quyết định và nhật ký thói quen | **M3:** causal vs correlational |
| 22–26 | **05 Consciousness:** sleep, dreams, consciousness, altered states, phenomena (18–22) | 5 note; so sánh lý thuyết và mức độ bằng chứng | Không coi lucid dreaming là kỹ thuật tăng IQ được chứng minh |
| 27–30 | **06 Human Development:** personality, social psychology, development, mental health (23–26) | 4 note; synthesis về khác biệt cá nhân và môi trường | **M4:** an toàn, đạo đức, giới hạn khái quát |
| 31–32 | **07 Integration:** philosophy of mind, cognitive practice (27–28) | 2 note; sơ đồ liên ngành | **M5:** phân biệt empirical và philosophical |
| 33–36 | Tổng hợp 7 module | Bản đồ tri thức, 7 synthesis, đối chiếu tranh luận/nguồn | **M6:** kiểm tra chéo các mâu thuẫn |
| 37–40 | Capstone và audit | Báo cáo 3.000–5.000 từ hoặc dự án tương đương, bibliography và evidence-gap register | **M7:** human review + retrospective |

**Lưu ý:** roadmap là mục tiêu kế hoạch, không phải chứng nhận nghiên cứu đã hoàn tất. Nếu G1/G2 bị chặn, lịch học dịch theo ngày bắt đầu thực tế.

## 5. Nhịp làm việc 6–8 giờ/tuần

- **2 giờ:** đọc 1–3 nguồn gốc/review; ghi chính xác điểm mạnh và giới hạn.
- **1,5 giờ:** đối chiếu claims và trích dẫn; ghi `UNKNOWN` khi thiếu bằng chứng.
- **1,5 giờ:** active recall, Feynman explanation, giải bài tập và tự kiểm tra.
- **1,5 giờ:** viết synthesis, ví dụ, liên kết chéo, mini-project.
- **0,5 giờ:** cập nhật research log, trạng thái note và kế hoạch tuần sau.

Có thể chia thành 4 phiên ngắn; ưu tiên giấc ngủ và học bền vững hơn tăng giờ học cực đoan.

## 6. Rubric kiểm tra từng note (0–4 điểm/tiêu chí)

| Tiêu chí | 0 | 2 | 4 |
| --- | --- | --- | --- |
| Độ bao phủ | Thiếu phần cốt lõi | Đủ khái niệm, thiếu tranh luận | Đủ cơ chế, ví dụ, giới hạn và câu hỏi mở |
| Provenance | Không có nguồn | Có URL nhưng claim chưa nối evidence | Claim quan trọng có nguồn và pointer kiểm tra được |
| Độ chính xác | Mâu thuẫn/lỗi nghiêm trọng | Đúng phần lớn, còn điểm chưa chắc | Diễn giải cân bằng, phân biệt loại bằng chứng |
| Khả năng học | Không có bài tập | Có câu hỏi nhớ lại | Retrieval, ứng dụng, mini-project và feedback |
| Tính liên kết | Note cô lập | Có link nhưng thiếu lý do | Link chéo có giải thích và dependency rõ |

**Ngưỡng đề xuất:** ≥16/20, không còn lỗi nguồn nghiêm trọng, và ≥80% retrieval prompts trả lời không nhìn note. Đây là **rubric đề xuất**, không phải điểm đã đo hay chứng nhận `verified`.

## 7. Rủi ro, phụ thuộc và cách xử lý

| ID | Rủi ro | Hành động |
| --- | --- | --- |
| R1 | Chỉ có tóm tắt Deep Research, thiếu 28 file thực tế | Giữ G1 BLOCKED; không tạo placeholder giả làm note hoàn chỉnh |
| R2 | Citation/DOI có thể sai hoặc không hỗ trợ claim | Review nguồn và ghi evidence pointer trước khi nâng trạng thái |
| R3 | Obsidian YAML/wikilinks không khớp AI-WORKSPACE wiki schema | Tách vault độc lập và project pointer; không bulk-copy vào wiki |
| R4 | ChatGPT Project dùng snapshot cũ | Lưu manifest ngày/commit và thay snapshot có kiểm soát |
| R5 | Bản quyền hoặc điều khoản tái sử dụng chưa rõ | Không nhập raw, không phân phối lại nội dung toàn văn khi chưa được phép |
| R6 | Chủ đề mental health/dreams dễ bị diễn giải thành lời khuyên điều trị | Giới hạn giáo dục, mô tả mức độ bằng chứng, ưu tiên an toàn |
| R7 | Kế hoạch quá dày hoặc mất động lực | Cho phép điều chỉnh 11–12 tháng, theo dõi chất lượng hơn số trang |

## 8. Next actions theo thứ tự

1. **Ngay bây giờ:** tạo context, plan, import checklist và cập nhật `projects/index.md` trên nhánh review.
2. **Sau khi nhận ZIP:** kiểm tra 28 note thực tế, xuất report diff/validation; không nói “đã nhập” trước khi làm.
3. **Sau khi xác nhận repo/vault:** nhập 28 note và tài liệu lõi vào canonical source, tạo commit riêng.
4. **Sau review nguồn:** chuẩn hóa claim, citation và trạng thái theo module.
5. **Sau chấp nhận:** tạo snapshot cho ChatGPT Project và bắt đầu tuần 1.
6. **Tùy chọn, phê duyệt riêng:** đăng ký/ingest nguồn vào AI-WORKSPACE theo đúng governance và intake gate.

## 9. Definition of done

**Project setup DONE** khi ba file metadata hiện diện, index liên kết hợp lệ và diff được duyệt/merge. **Research import DONE** chỉ khi toàn bộ artifact đã được đọc, kiểm, commit trong canonical repo và có manifest kiểm kê. **Scientific review DONE** chỉ khi có review nguồn thực tế và người duyệt chấp nhận. Các trạng thái này độc lập; không suy trạng thái sau từ trạng thái trước.

Chi tiết 28 đường dẫn và kiểm tra file: [import-checklist.md](import-checklist.md).
