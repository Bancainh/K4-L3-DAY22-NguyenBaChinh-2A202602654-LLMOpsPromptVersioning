# Day 22 — Kết quả lab

Project LangSmith: https://smith.langchain.com/o/ada28667-c5b9-4781-baf5-3ee9c65cddf6/projects/p/ce745db0-89a6-49bc-b4fc-bd72125cf248

## Tracing và Prompt Hub

- Knowledge base được chia thành 107 chunks, index bằng FAISS; mỗi câu hỏi truy xuất 3 chunks rồi trả lời qua LCEL chain.
- LangSmith API ghi nhận 100 root traces `rag-query` và 50 root traces `ab-rag-query` khi kiểm tra. Mỗi lượt có đầu vào, các run truy xuất và đầu ra.
- Hai prompt `nguyen-ba-chinh-day22-rag-v1` và `nguyen-ba-chinh-day22-rag-v2` được push và pull thành công từ Prompt Hub. Định tuyến MD5 theo `request_id` cho 19 câu V1 và 31 câu V2.

## So sánh RAGAS

Mỗi prompt xử lý đủ 50 cặp câu hỏi và đáp án chuẩn. Các điểm trung bình trong `03_ragas_report.json`:

| Metric | V1 | V2 |
|---|---:|---:|
| Faithfulness | 0.9780 | 0.9516 |
| Answer relevancy | 0.9169 | 0.8929 |
| Context recall | 1.0000 | 1.0000 |
| Context precision | 0.9450 | 0.9417 |

V1 trả lời ngắn gọn và đạt faithfulness, answer relevancy cao hơn V2 trong lần đo này. Một cách giải thích có thể là câu trả lời dài, có cấu trúc của V2 tạo thêm các mệnh đề để metric kiểm tra. Hai phiên bản dùng cùng retriever và `k=3`, nên context recall bằng nhau; context precision rất gần nhau. Đây là nhận định từ một lần đo, không khẳng định prompt V1 luôn tốt hơn.

Lần chấm V2 đầu có một timeout khiến faithfulness thành `NaN`, nên đã chấm lại V2. Trong lần chấm lại, 2 lượt faithfulness lỗi kết nối/timeout được bỏ qua khi tính trung bình; log `03_ragas_v2_retry_log.txt` ghi rõ việc này. Cả 50 câu vẫn được chạy qua RAG trước khi chấm.

## Guardrails

`PIIDetector` che email, số điện thoại, SSN và thẻ tín dụng bằng `FailResult(fix_value=...)`; đầu vào sạch được giữ nguyên. `JSONFormatter` gỡ markdown fences, sửa nháy đơn và dấu phẩy cuối, hoặc trả JSON dự phòng khi không sửa được. Hai log demo có 6 case PII và 5 case JSON.
