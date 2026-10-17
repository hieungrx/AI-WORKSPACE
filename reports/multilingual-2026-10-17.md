# Multilingual readiness — observed synthetic retrieval results

TEST_ONLY: these results concern artificial fixtures, not real project knowledge.
Method: scoped deterministic lexical matching with curated aliases; no semantic retrieval. Python: 3.13.0.

Observed: 25 pairs / 50 queries; 50 met expected outcomes, 0 failed.

Passing a negative case means NOT_FOUND or MISSING_EVIDENCE was returned as expected; it does not mean every query found a source.

## Observed categories

- exact_keyword: 10/10 expected outcomes.
- bilingual_aliases: 10/10 expected outcomes.
- cross_language: 10/10 expected outcomes.
- project_scope: 10/10 expected outcomes.
- missing_evidence: 10/10 expected outcomes.

## Actual search outcomes

- FOUND: 36
- NOT_FOUND: 6
- MISSING_EVIDENCE: 8

## Pair details

### P01 — exact_keyword

- vi: Giải thích GET /api/listings → FOUND; scope=demo-a; paths=wiki/listing-route.md; expected=FOUND; checks=PASS.
- en: Explain GET /api/listings → FOUND; scope=demo-a; paths=wiki/listing-route.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-101](../tests/fixtures/multilingual/sources/raw/synthetic.md#listing-route).

### P02 — exact_keyword

- vi: Giải thích reserveListing() → FOUND; scope=demo-a; paths=wiki/reserve-function.md; expected=FOUND; checks=PASS.
- en: Explain reserveListing() → FOUND; scope=demo-a; paths=wiki/reserve-function.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-102](../tests/fixtures/multilingual/sources/raw/synthetic.md#reserve-function).

### P03 — exact_keyword

- vi: Giải thích checkout.service.ts → FOUND; scope=demo-a; paths=wiki/checkout-file.md; expected=FOUND; checks=PASS.
- en: Explain checkout.service.ts → FOUND; scope=demo-a; paths=wiki/checkout-file.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-103](../tests/fixtures/multilingual/sources/raw/synthetic.md#checkout-file).

### P04 — exact_keyword

- vi: Giải thích SELECT FOR UPDATE → FOUND; scope=demo-a; paths=wiki/row-lock.md; expected=FOUND; checks=PASS.
- en: Explain SELECT FOR UPDATE → FOUND; scope=demo-a; paths=wiki/row-lock.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-104](../tests/fixtures/multilingual/sources/raw/synthetic.md#row-lock).

### P05 — exact_keyword

- vi: Giải thích HTTP 409 → FOUND; scope=demo-a; paths=wiki/conflict-status.md; expected=FOUND; checks=PASS.
- en: Explain HTTP 409 → FOUND; scope=demo-a; paths=wiki/conflict-status.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-105](../tests/fixtures/multilingual/sources/raw/synthetic.md#conflict-status).

### P06 — bilingual_aliases

- vi: Hỏi về đăng nhập → FOUND; scope=demo-a; paths=wiki/authentication.md; expected=FOUND; checks=PASS.
- Added terms: authentication
- en: Explain authentication → FOUND; scope=demo-a; paths=wiki/authentication.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-106](../tests/fixtures/multilingual/sources/raw/synthetic.md#authentication).

### P07 — bilingual_aliases

- vi: kiểm tra quyền → FOUND; scope=demo-a; paths=wiki/authorization.md; expected=FOUND; checks=PASS.
- Added terms: authorization
- en: authorization → FOUND; scope=demo-a; paths=wiki/authorization.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-107](../tests/fixtures/multilingual/sources/raw/synthetic.md#authorization).

### P08 — bilingual_aliases

- vi: chống xử lý lặp → FOUND; scope=demo-a; paths=wiki/idempotency.md; expected=FOUND; checks=PASS.
- Added terms: idempotency
- en: idempotency → FOUND; scope=demo-a; paths=wiki/idempotency.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-108](../tests/fixtures/multilingual/sources/raw/synthetic.md#idempotency).

### P09 — bilingual_aliases

- vi: Chính sách thử lại → FOUND; scope=demo-a; paths=wiki/retry.md; expected=FOUND; checks=PASS.
- Added terms: retry policy
- en: retry policy → FOUND; scope=demo-a; paths=wiki/retry.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-109](../tests/fixtures/multilingual/sources/raw/synthetic.md#retry).

### P10 — bilingual_aliases

- vi: chia trang → FOUND; scope=demo-a; paths=wiki/pagination.md; expected=FOUND; checks=PASS.
- Added terms: pagination
- en: pagination → FOUND; scope=demo-a; paths=wiki/pagination.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-110](../tests/fixtures/multilingual/sources/raw/synthetic.md#pagination).

### P11 — cross_language

- vi: Hệ thống dùng giao dịch cơ sở dữ liệu thế nào? → FOUND; scope=demo-a; paths=wiki/transaction.md; expected=FOUND; checks=PASS.
- Added terms: database transaction
- en: How does a database transaction work? → FOUND; scope=demo-a; paths=wiki/transaction.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-111](../tests/fixtures/multilingual/sources/raw/synthetic.md#transaction).

### P12 — cross_language

- vi: Khi nào cần hoàn tác giao dịch? → FOUND; scope=demo-a; paths=wiki/rollback.md; expected=FOUND; checks=PASS.
- Added terms: transaction rollback
- en: When is transaction rollback needed? → FOUND; scope=demo-a; paths=wiki/rollback.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-112](../tests/fixtures/multilingual/sources/raw/synthetic.md#rollback).

### P13 — cross_language

- vi: Xử lý bế tắc thế nào? → FOUND; scope=demo-a; paths=wiki/deadlock.md; expected=FOUND; checks=PASS.
- Added terms: deadlock
- en: How is deadlock handled? → FOUND; scope=demo-a; paths=wiki/deadlock.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-113](../tests/fixtures/multilingual/sources/raw/synthetic.md#deadlock).

### P14 — cross_language

- vi: Khi nào vô hiệu hóa bộ nhớ đệm? → FOUND; scope=demo-a; paths=wiki/cache.md; expected=FOUND; checks=PASS.
- Added terms: cache invalidation
- en: When is cache invalidation needed? → FOUND; scope=demo-a; paths=wiki/cache.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-114](../tests/fixtures/multilingual/sources/raw/synthetic.md#cache).

### P15 — cross_language

- vi: Hệ thống dùng khóa lạc quan ra sao? → FOUND; scope=demo-a; paths=wiki/optimistic.md; expected=FOUND; checks=PASS.
- Added terms: optimistic locking
- en: How does optimistic locking work? → FOUND; scope=demo-a; paths=wiki/optimistic.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-115](../tests/fixtures/multilingual/sources/raw/synthetic.md#optimistic).

### P16 — project_scope

- vi: thời gian chờ → FOUND; scope=demo-a; paths=wiki/timeout-a.md; expected=FOUND; checks=PASS.
- Added terms: request timeout
- en: request timeout → FOUND; scope=demo-a; paths=wiki/timeout-a.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-116](../tests/fixtures/multilingual/sources/raw/synthetic.md#timeout-a).

### P17 — project_scope

- vi: thời gian chờ → FOUND; scope=demo-b; paths=wiki/timeout-b.md; expected=FOUND; checks=PASS.
- Added terms: request timeout
- en: request timeout → FOUND; scope=demo-b; paths=wiki/timeout-b.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-117](../tests/fixtures/multilingual/sources/raw/synthetic.md#timeout-b).

### P18 — project_scope

- vi: thời gian chờ → NOT_FOUND; scope=demo-c; paths=none; expected=NOT_FOUND; checks=PASS.
- en: request timeout → NOT_FOUND; scope=demo-c; paths=none; expected=NOT_FOUND; checks=PASS.

### P19 — project_scope

- vi: đổi kích thước ảnh → NOT_FOUND; scope=demo-a; paths=none; expected=NOT_FOUND; checks=PASS.
- en: image resizing → NOT_FOUND; scope=demo-a; paths=none; expected=NOT_FOUND; checks=PASS.

### P20 — project_scope

- vi: Giải thích Legacy checksum → FOUND; scope=unscoped; paths=wiki/legacy.md; expected=FOUND; checks=PASS.
- en: Explain Legacy checksum → FOUND; scope=unscoped; paths=wiki/legacy.md; expected=FOUND; checks=PASS.
- Fixture evidence: [SRC-20261017-119](../tests/fixtures/multilingual/sources/raw/synthetic.md#legacy).

### P21 — missing_evidence

- vi: tồn kho lượng tử → NOT_FOUND; scope=demo-a; paths=none; expected=NOT_FOUND; checks=PASS.
- en: quantum inventory → NOT_FOUND; scope=demo-a; paths=none; expected=NOT_FOUND; checks=PASS.

### P22 — missing_evidence

- vi: đối soát chi trả → MISSING_EVIDENCE; scope=demo-a; paths=wiki/no-evidence.md; expected=MISSING_EVIDENCE; checks=PASS.
- Added terms: payout reconciliation
- en: payout reconciliation → MISSING_EVIDENCE; scope=demo-a; paths=wiki/no-evidence.md; expected=MISSING_EVIDENCE; checks=PASS.

### P23 — missing_evidence

- vi: theo dõi hoàn tiền → MISSING_EVIDENCE; scope=demo-a; paths=wiki/unknown-id.md; expected=MISSING_EVIDENCE; checks=PASS.
- Added terms: refund tracing
- en: refund tracing → MISSING_EVIDENCE; scope=demo-a; paths=wiki/unknown-id.md; expected=MISSING_EVIDENCE; checks=PASS.

### P24 — missing_evidence

- vi: bàn giao tranh chấp → MISSING_EVIDENCE; scope=demo-a; paths=wiki/missing-file.md; expected=MISSING_EVIDENCE; checks=PASS.
- Added terms: dispute handoff
- en: dispute handoff → MISSING_EVIDENCE; scope=demo-a; paths=wiki/missing-file.md; expected=MISSING_EVIDENCE; checks=PASS.

### P25 — missing_evidence

- vi: xuất kiểm toán → MISSING_EVIDENCE; scope=demo-a; paths=wiki/metadata-only.md; expected=MISSING_EVIDENCE; checks=PASS.
- Added terms: audit export
- en: audit export → MISSING_EVIDENCE; scope=demo-a; paths=wiki/metadata-only.md; expected=MISSING_EVIDENCE; checks=PASS.

## Limits and next step

This measures the declared lexical rules on curated examples. It does not establish semantic recall, performance on unseen paraphrases, factual correctness, approval or live Obsidian behavior. No live raw source was added, read, translated or rewritten by the retrieval runner. The proposed upgrade path remains in MULTILINGUAL.md; no QMD, RAG or vector store was implemented.
