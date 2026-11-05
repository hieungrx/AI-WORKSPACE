# Human Mind Research — Project Context

- **Project ID:** `human-mind-research`
- **Status:** `NOT_YET_SYNCED` — báo cáo nghiên cứu Markdown chưa được cung cấp để đọc/kiểm trong workspace này
- **Planning status:** `DRAFT_FOR_REVIEW`
- **Scope:** nghiên cứu liên ngành về con người, nhận thức, trí tuệ, hành vi và ý thức (28 chủ đề, 7 nhóm)
- **Input thực tế do người dùng xác nhận:** **một báo cáo Deep Research định dạng `.md`**; chưa có file ZIP nào được xác nhận
- **Canonical source:** bản báo cáo Markdown gốc của người dùng, chờ đính kèm/định vị; không suy rằng 28 ghi chú Markdown riêng đã tồn tại
- **Canonical vault/repo cho ghi chú phát triển:** `TO_BE_CONFIRMED` — tùy chọn sau khi đọc báo cáo
- **Requirements:** [Kế hoạch](plan.md) và [Checklist tiếp nhận báo cáo, danh mục 28 chủ đề](import-checklist.md)
- **Last metadata review:** 2026-11-05
- **Current phase:** P0 — đăng ký project và chờ bản `.md` để rà soát, sau đó lên kế hoạch học
- **Source registry:** chưa có nguồn nghiên cứu được phê duyệt/đăng ký/Ingest cho project này trong AI-WORKSPACE
- **Approved decisions:** chưa có quyết định nào được ghi nhận đã phê duyệt

## Goals

1. Đọc và quản lý **báo cáo Markdown thực tế** của Deep Research như một tài liệu đầu vào, giữ nguyên bản gốc và provenance.
2. Lập kế hoạch 40 tuần (6–8 giờ/tuần) cho 28 chủ đề, có checkpoints, nghiên cứu khoa học, câu hỏi tự kiểm tra và capstone.
3. Đối chiếu xem báo cáo `.md` thực sự có nội dung nào: 28 phần, nguồn tham khảo, lộ trình, bài tập, hay chỉ là bản tổng hợp. Không suy đoán các file riêng.
4. Chỉ khi có nhu cầu và đủ nội dung, **đề xuất** tách thành 28 ghi chú Obsidian; mọi ghi chú tạo mới được gắn `derived draft` và truy ngược đến báo cáo gốc.
5. Phân biệt `FACT`, `INTERPRETATION`, `HYPOTHESIS`, `UNKNOWN` và giữ tình trạng kiểm chứng nguồn.

## Non-goals / boundaries

- Không khẳng định có ZIP, bundles, 28 file riêng, hoặc tài liệu đã được nhập khi chưa thấy artifact thật.
- Không tự động đưa báo cáo hoặc ghi chú vào `wiki/`, `sources/raw/`, `sources/manifest.csv`.
- Không coi citation/URL trong báo cáo AI là bằng chứng đã kiểm chứng, license hay quyền tái phân phối.
- Không nâng trạng thái tri thức lên `verified`, không tạo human approval giả, không tuyên bố Ingest đã chạy.
- Không thay đổi các rào cản real-source intake hiện hành của AI-WORKSPACE.

## Architecture & source of truth

```text
AI-WORKSPACE/
└── projects/
    ├── index.md
    └── human-mind-research/
        ├── context.md             <- project pointer / status
        ├── plan.md                <- learning & review roadmap
        └── import-checklist.md    <- Markdown intake & 28-topic outline

User-provided Deep Research report (PENDING):
└── report.md                      <- original file name to be confirmed

Optional derived Obsidian vault/repo (NOT CREATED):
├── 00-START-HERE.md
├── 01-foundations/ ... 07-integration/  <- up to 28 derived notes
└── references/ and research-log/
```

**Source of truth:** báo cáo `.md` gốc cho nội dung Deep Research; bản tách note chỉ là sản phẩm phái sinh có thể kiểm tra lại. **AI-WORKSPACE:** context/pointer, không phải kho chứa toàn bộ tài liệu. **ChatGPT Project:** snapshot thủ công nếu được tạo, không phải đồng bộ GitHub.

## Current priorities

1. Nhận đúng **file báo cáo `.md`** do người dùng lưu, không yêu cầu ZIP.
2. Đọc/kiểm thực tế cấu trúc, 28 chủ đề, nguồn, trích dẫn, mức độ chi tiết và nội dung còn thiếu.
3. Điều chỉnh kế hoạch 40 tuần theo nội dung báo cáo; lập backlog cho những phần chưa có.
4. Nếu người dùng muốn Obsidian, xin xác nhận repo/vault rồi tách note từ báo cáo với provenance rõ ràng.
5. Chỉ đề xuất source intake vào AI-WORKSPACE bằng quy trình phê duyệt riêng.

## Open questions

- Người dùng có thể đính kèm file báo cáo `.md` vào hội thoại này không?
- Báo cáo có 28 phần riêng hay chỉ có roadmap/tổng hợp? Cần đọc file mới xác định được.
- Người dùng muốn chỉ quản lý trong GitHub `projects/` hay còn tạo ChatGPT Project qua UI?
- Nếu cần Obsidian, canonical repo/vault độc lập nào sẽ được chọn?

## Useful handoffs

- [Kế hoạch 40 tuần](plan.md)
- [Checklist báo cáo và danh mục 28 chủ đề](import-checklist.md)
- [Danh mục dự án](../index.md)
- [Governance](../../KNOWLEDGE_GOVERNANCE.md)
- [Source integrity](../../SOURCE_INTEGRITY.md)
- [AI-WORKSPACE schema](../../SCHEMA.md)
