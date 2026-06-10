# Dàn Ý Slide Bảo Vệ Đề Cương

Tài liệu này dùng để làm slide PowerPoint hoặc Google Slides. Nội dung được viết ngắn, đơn giản và dễ trình bày.

## Slide 1: Tên Đề Tài

Nội dung đưa lên slide:

- Xây dựng hệ thống phát hiện xâm nhập mạng kết hợp học máy có giải thích và mô hình ngôn ngữ lớn tăng cường truy hồi hỗ trợ phân tích cảnh báo an ninh.
- Học viên: (điền tên).
- Giảng viên hướng dẫn: (điền tên giảng viên).

Lời nói gợi ý:

> Kính thưa hội đồng, em xin trình bày đề cương luận văn về hệ thống phát hiện xâm nhập mạng kết hợp học máy và mô hình ngôn ngữ lớn. Trong đề tài này, học máy dùng để phát hiện tấn công, còn mô hình ngôn ngữ dùng để giải thích cảnh báo cho dễ hiểu hơn.

Ghi chú:

- Slide này chỉ cần đơn giản, rõ tên đề tài và thông tin cá nhân.

## Slide 2: Lý Do Chọn Đề Tài

Nội dung đưa lên slide:

- IDS có thể tạo nhiều cảnh báo kỹ thuật.
- Cảnh báo thường khó hiểu với người phân tích.
- Người phân tích cần biết nguyên nhân, mức độ nguy hiểm và cách xử lý.
- LLM có thể hỗ trợ giải thích, nhưng không nên dùng để phát hiện trực tiếp.

Lời nói gợi ý:

> Trong thực tế, hệ thống phát hiện xâm nhập có thể sinh ra rất nhiều cảnh báo. Tuy nhiên, cảnh báo thường chỉ có thông tin kỹ thuật, chưa giải thích rõ vì sao nguy hiểm và nên xử lý thế nào. Vì vậy, em chọn đề tài này để kết hợp học máy cho phần phát hiện và mô hình ngôn ngữ cho phần giải thích.

Ghi chú:

- Nên nhấn mạnh: LLM chỉ hỗ trợ giải thích, không thay thế IDS.

## Slide 3: Vấn Đề Nghiên Cứu

Nội dung đưa lên slide:

- IDS thường trả lời: có đáng nghi hay không?
- Người phân tích cần thêm:
- Vì sao đáng nghi?
- Bằng chứng là gì?
- Ưu tiên xử lý ra sao?
- Nên phản ứng như thế nào?

Lời nói gợi ý:

> Vấn đề chính là khoảng cách giữa phát hiện tấn công và phân tích cảnh báo. IDS có thể nói rằng một sự kiện đáng nghi, nhưng người phân tích cần hiểu lý do và hướng xử lý. Đề tài của em tập trung vào việc làm cho cảnh báo dễ hiểu và hữu ích hơn.

Ghi chú:

- Có thể trình bày slide này dạng hai cột: `IDS cho biết` và `Người phân tích cần`.

## Slide 4: Mục Tiêu Đề Tài

Nội dung đưa lên slide:

- Xử lý dữ liệu mạng dạng CSV.
- Huấn luyện mô hình học máy để phát hiện tấn công.
- Tạo cảnh báo có bằng chứng kỹ thuật.
- Giải thích cảnh báo bằng RAG và mô hình ngôn ngữ.
- Hiển thị kết quả trên dashboard SOC.
- Xuất báo cáo để đánh giá luận văn.

Lời nói gợi ý:

> Mục tiêu của đề tài là xây dựng một prototype hoàn chỉnh ở mức nghiên cứu. Hệ thống sẽ đi từ dữ liệu mạng, xử lý dữ liệu, phát hiện tấn công, tạo cảnh báo, giải thích cảnh báo và hiển thị trên dashboard.

Ghi chú:

- Dùng từ `prototype` và giải thích là bản mẫu nghiên cứu.

## Slide 5: Phạm Vi Đề Tài

Nội dung đưa lên slide:

- Trong phạm vi:
- Dữ liệu mạng offline dạng CSV.
- Dataset chính: UNSW-NB15.
- Mô hình: Logistic Regression, Decision Tree, Random Forest.
- Dashboard demo.
- RAG dùng playbook an ninh.
- Ngoài phạm vi:
- Không bắt gói mạng realtime.
- Không tự động chặn IP.
- Không thay thế SIEM/SOAR.

Lời nói gợi ý:

> Đề tài được giới hạn ở mức nghiên cứu và demo. Em không xây dựng hệ thống production hay tự động phản ứng trong mạng thật. Việc giới hạn phạm vi giúp đề tài tập trung vào phần có thể đánh giá được là mô hình phát hiện, phần giải thích và dashboard minh họa.

Ghi chú:

- Nên dùng bảng hai cột: `Làm` và `Không làm`.

## Slide 6: Kiến Trúc Hệ Thống

Nội dung đưa lên slide:

```text
Dữ liệu mạng
  -> Xử lý dữ liệu
  -> Mô hình phát hiện
  -> Tạo cảnh báo
  -> Giải thích bằng RAG/LLM
  -> Dashboard và báo cáo
```

Thông điệp chính:

```text
Học máy phát hiện.
Mô hình ngôn ngữ giải thích.
Con người quyết định.
```

Lời nói gợi ý:

> Đây là kiến trúc tổng quát của hệ thống. Dữ liệu mạng được xử lý và đưa vào mô hình học máy. Sau đó hệ thống tạo cảnh báo, bổ sung bằng chứng kỹ thuật và dùng RAG/LLM để giải thích. Cuối cùng kết quả được hiển thị trên dashboard và xuất báo cáo.

Ghi chú:

- Có thể dùng sơ đồ trong `docs/architecture-diagram.md`.

## Slide 7: Phần Học Máy Phát Hiện Tấn Công

Nội dung đưa lên slide:

- Input: dữ liệu network-flow.
- Xử lý dữ liệu: làm sạch, mã hóa, chuẩn bị đặc trưng.
- Mô hình sử dụng:
- Logistic Regression.
- Decision Tree.
- Random Forest.
- Chỉ số đánh giá:
- Accuracy, Precision, Recall, F1-score, False Positive Rate.

Lời nói gợi ý:

> Phần học máy chịu trách nhiệm phát hiện tấn công. Em sử dụng các mô hình cơ bản để dễ so sánh và dễ giải thích. Kết quả sẽ được đánh giá bằng các chỉ số phổ biến trong bài toán phân loại, đặc biệt là recall và false positive rate vì hai chỉ số này rất quan trọng trong IDS.

Ghi chú:

- Nếu hội đồng hỏi vì sao dùng mô hình cơ bản, trả lời: dễ đánh giá, dễ so sánh, phù hợp giai đoạn đầu.

## Slide 8: Làm Giàu Và Giải Thích Cảnh Báo

Nội dung đưa lên slide:

- Mỗi cảnh báo có thêm:
- Loại tấn công.
- Mức độ nghiêm trọng.
- Độ tin cậy.
- Bằng chứng kỹ thuật.
- MITRE ATT&CK liên quan.
- Mức ưu tiên xử lý.
- Mục tiêu: giúp cảnh báo dễ hiểu hơn.

Lời nói gợi ý:

> Sau khi phát hiện, hệ thống không chỉ trả về nhãn tấn công. Hệ thống bổ sung thêm lý do, bằng chứng, mức độ nghiêm trọng và kỹ thuật MITRE liên quan. Nhờ đó, người phân tích có thể hiểu cảnh báo nhanh hơn.

Ghi chú:

- Ví dụ dễ nói: brute force có bằng chứng là số lần đăng nhập thất bại cao.

## Slide 9: RAG Và Mô Hình Ngôn Ngữ

Nội dung đưa lên slide:

- RAG: lấy tài liệu liên quan trước khi trả lời.
- LLM: tạo giải thích bằng ngôn ngữ dễ hiểu.
- So sánh 3 cách giải thích:
- Mẫu cố định.
- LLM không dùng RAG.
- LLM có dùng RAG.
- Mục tiêu: giảm trả lời thiếu căn cứ.

Lời nói gợi ý:

> RAG giúp hệ thống lấy playbook an ninh liên quan trước khi mô hình ngôn ngữ tạo câu trả lời. Nhờ đó, phần giải thích có thêm căn cứ thay vì chỉ dựa vào khả năng sinh văn bản của mô hình. Đề tài sẽ so sánh ba cách giải thích để xem RAG có giúp cải thiện chất lượng không.

Ghi chú:

- Giải thích đơn giản: RAG giống như mở tài liệu hướng dẫn trước khi trả lời.

## Slide 10: Kế Hoạch Đánh Giá

Nội dung đưa lên slide:

- Đánh giá IDS:
- Accuracy, Precision, Recall, F1-score, False Positive Rate.
- Đánh giá giải thích:
- Đúng với cảnh báo không?
- Có đủ thông tin không?
- Có dựa trên bằng chứng không?
- Gợi ý xử lý có rõ không?
- Có sinh thông tin sai không?

Lời nói gợi ý:

> Đề tài đánh giá hai phần. Phần phát hiện được đánh giá bằng chỉ số định lượng. Phần giải thích được đánh giá bằng tiêu chí như đúng, đủ, có căn cứ và có hữu ích cho người phân tích hay không. Em cũng sẽ chú ý đến nguy cơ mô hình ngôn ngữ sinh thông tin sai.

Ghi chú:

- Nói rõ: kết quả trên dữ liệu mẫu hiện tại chưa phải kết quả cuối cùng.

## Slide 11: Prototype Hiện Tại

Nội dung đưa lên slide:

- Đã có backend FastAPI.
- Đã có dashboard React.
- Đã có dữ liệu mẫu và cảnh báo mẫu.
- Đã có script huấn luyện mô hình.
- Đã có API giải thích cảnh báo.
- Đã có báo cáo đánh giá mẫu.

Demo nhanh:

- Dashboard.
- Danh sách cảnh báo.
- Giải thích cảnh báo.
- Bảng kết quả mô hình.

Lời nói gợi ý:

> Prototype hiện tại đã chạy được workflow cơ bản từ dữ liệu mẫu đến cảnh báo, giải thích và báo cáo. Phần này giúp chứng minh đề tài có tính khả thi. Tuy nhiên, dữ liệu mẫu chỉ dùng để kiểm thử hệ thống, chưa dùng để kết luận hiệu năng cuối cùng.

Ghi chú:

- Nếu demo: mở `http://localhost:5173` và `http://localhost:8000/docs`.

## Slide 12: Tiến Độ Thực Hiện

Nội dung đưa lên slide:

| Thời gian | Công việc |
| --- | --- |
| Tháng 1 | Hoàn thiện đề cương, đọc tài liệu, ổn định kiến trúc |
| Tháng 2 | Xử lý UNSW-NB15, huấn luyện mô hình cơ bản |
| Tháng 3 | So sánh mô hình, thử dataset phụ nếu có |
| Tháng 4 | Bổ sung giải thích và MITRE ATT&CK |
| Tháng 5 | Hoàn thiện RAG/LLM và dashboard |
| Tháng 6 | Tổng hợp kết quả, viết luận văn, chuẩn bị bảo vệ |

Lời nói gợi ý:

> Em chia kế hoạch làm 6 tháng. Giai đoạn đầu tập trung vào đề cương, tài liệu và dữ liệu. Giai đoạn giữa tập trung vào mô hình và giải thích. Giai đoạn cuối là đánh giá, viết luận văn và chuẩn bị bảo vệ.

Ghi chú:

- Slide này nên trình bày thành timeline ngang.

## Slide 13: Đóng Góp Và Kết Luận

Nội dung đưa lên slide:

- Prototype phát hiện và phân tích cảnh báo xâm nhập.
- Quy trình xử lý dữ liệu và đánh giá mô hình.
- Cảnh báo có thêm bằng chứng kỹ thuật.
- Giải thích cảnh báo bằng RAG/LLM.
- Dashboard và báo cáo phục vụ luận văn.

Thông điệp kết luận:

```text
Học máy phát hiện.
LLM giải thích.
Con người quyết định.
```

Lời nói gợi ý:

> Tóm lại, đề tài hướng đến một prototype kết hợp học máy và mô hình ngôn ngữ để hỗ trợ phân tích cảnh báo an ninh. Điểm quan trọng là mô hình ngôn ngữ không thay thế IDS, mà chỉ giúp giải thích cảnh báo rõ ràng hơn. Kết quả cuối cùng sẽ gồm hệ thống demo, báo cáo đánh giá và các phân tích phục vụ luận văn.

Ghi chú:

- Đây là slide kết thúc trước phần hỏi đáp.

## Câu Hỏi Có Thể Gặp

1. Vì sao không dùng LLM để phát hiện tấn công trực tiếp?

Trả lời ngắn:

> Vì dữ liệu IDS là dữ liệu có cấu trúc và cần đánh giá bằng chỉ số rõ ràng. LLM có thể trả lời sai hoặc khó kiểm chứng. Vì vậy, đề tài dùng học máy để phát hiện và dùng LLM để giải thích.

2. RAG có loại bỏ hoàn toàn trả lời sai không?

Trả lời ngắn:

> Không. RAG chỉ giúp giảm rủi ro bằng cách cung cấp tài liệu liên quan. Vì vậy, đề tài vẫn đánh giá nguy cơ sinh thông tin sai.

3. Kết quả trên dữ liệu mẫu có chứng minh mô hình tốt không?

Trả lời ngắn:

> Không. Dữ liệu mẫu chỉ dùng để kiểm thử pipeline. Kết luận cuối cùng phải dựa trên dataset chuẩn như UNSW-NB15.

4. Prototype có dùng được trong thực tế ngay không?

Trả lời ngắn:

> Chưa. Đây là prototype nghiên cứu, chưa phải hệ thống production.
