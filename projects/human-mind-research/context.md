# Human Mind Research — Project Context

- **Project ID:** `human-mind-research`
- **Status:** `NOT_YET_SYNCED` (chưa nhập và kiểm tra bộ 28 note gốc)
- **Planning status:** `DRAFT_FOR_REVIEW`
- **Scope:** nghiên cứu liên ngành về con người, nhận thức, trí tuệ, hành vi và ý thức
- **Canonical repository/vault:** `TO_BE_CONFIRMED` — chưa xác nhận một Git repository riêng làm nguồn chân lý
- **Research export:** bản tóm tắt Deep Research do người dùng cung cấp trong hội thoại, báo cáo có gói `human-mind-research.zip` và `human-mind-research-obsidian.zip`; **nội dung 28 file chưa được nhập/đối chiếu vào repository này**
- **Requirements:** [Kế hoạch triển khai](plan.md) và [Danh mục/kiểm tra nhập liệu](import-checklist.md)
- **Last project metadata review:** 2026-11-05
- **Tech stack:** Markdown, Obsidian, Git, AI-WORKSPACE (context/pointer); ChatGPT Project là snapshot, không phải hệ thống đồng bộ
- **Current phase:** P0 — đăng ký dự án, lập kế hoạch và chờ nhập/kiểm tra artifacts
- **Source registry:** chưa có nguồn nghiên cứu nào được phê duyệt/đăng ký/ingest cho dự án này trong AI-WORKSPACE
- **Approved decisions:** chưa có quyết định nào được ghi nhận là đã phê duyệt cho dự án này

## Goals

1. Quản lý có kiểm soát **28 ghi chú nghiên cứu** chia thành 7 module, có liên kết Obsidian, metadata và nguồn tham khảo.
2. Duy trì một báo cáo tổng hợp, roadmap 40 tuần (6–8 giờ/tuần), research log, câu hỏi tự kiểm tra và capstone.
3. Phân biệt nguồn gốc khoa học, tổng thuật, diễn giải AI, giả thuyết, quan điểm triết học và phần chưa xác minh.
4. Đảm bảo khả năng rà soát thay đổi, sửa lỗi và tái sử dụng trong Obsidian/ChatGPT mà không làm mất provenance.

## Non-goals / boundaries

- Không tự động đưa 28 note vào `wiki/`, `sources/raw/` hay `sources/manifest.csv`.
- Không xem một citation/URL trong báo cáo AI là bằng chứng đã kiểm chứng, quyền sao chép hay đăng ký nguồn.
- Không tự nâng trạng thái tài liệu lên `verified`, không tạo human approval giả, không tuyên bố Ingest đã chạy.
- Không đặt toàn bộ nội dung vault nghiên cứu trong `projects/`: theo [README gốc](../../README.md), đây là nơi giữ **pointer và context**. Bộ note chi tiết nên nằm ở vault/repository độc lập được xác nhận.
- Không thay đổi trạng thái **HOLD / NOT READY** của quy trình real-source intake AI-WORKSPACE.

## Architecture & source of truth

```text
AI-WORKSPACE/
└── projects/
    ├── index.md
    └── human-mind-research/
        ├── context.md             <- pointer / current status
        ├── plan.md                <- execution roadmap
        └── import-checklist.md    <- 28-file manifest and gates

Separate canonical Human Mind Research vault/repo (PENDING):
├── 00-START-HERE.md
├── MASTER-REPORT.md
├── AI_CONTEXT.md
├── RESEARCH-ROADMAP.md
├── 01-foundations/ ... 07-integration/ (28 notes)
├── references/
├── research-log/
└── bundles/
```

**Source of truth:** vault/repo độc lập khi được xác nhận. **AI-WORKSPACE:** bối cảnh và trạng thái tích hợp. **ChatGPT Project:** snapshot cập nhật thủ công, không đồng bộ hai chiều.

## Current priorities

1. Xác nhận và tải đúng gói ZIP từ phiên Deep Research; đối chiếu 28 file với manifest.
2. Kiểm tra cấu trúc, frontmatter, wikilinks, nội dung không rỗng, trích dẫn và giấy phép; ghi lỗi và độ chắc chắn.
3. Chọn canonical vault/repository riêng; chỉ nhập bộ Markdown vào đó sau khi đã xác nhận nội dung.
4. Review khoa học theo từng module, sau đó triển khai lịch học 40 tuần.
5. Chỉ đề xuất real-source intake của AI-WORKSPACE qua luồng phê duyệt riêng.

## Open questions

- Canonical repo/vault nào sẽ chứa đầy đủ 28 note và lịch sử Git?
- Hai ZIP Deep Research có thể được cung cấp trực tiếp để kiểm tra nội dung, kích thước và file thực tế không?
- Ai là người duyệt nguồn và các tuyên bố khoa học; mức độ chi tiết/cập nhật nào là tiêu chí chấp nhận?
- Có cần tạo **ChatGPT Project** riêng qua giao diện ChatGPT hay chỉ cần thư mục dự án trong GitHub AI-WORKSPACE? Đây là hai thực thể khác nhau.

## Useful handoffs

- [Kế hoạch 40 tuần và milestones](plan.md)
- [Manifest 28 note và checklist kiểm tra](import-checklist.md)
- [Danh mục dự án](../index.md)
- [Governance](../../KNOWLEDGE_GOVERNANCE.md)
- [Source integrity](../../SOURCE_INTEGRITY.md)
- [AI-WORKSPACE schema](../../SCHEMA.md)
