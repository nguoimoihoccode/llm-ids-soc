# Đề Cương Trình Bày Bảo Vệ Đề Cương Luận Văn

Tài liệu này dùng để chuẩn bị phần nói khi bảo vệ đề cương. Nội dung được viết theo hướng ngắn gọn, dễ hiểu và dễ trình bày trước hội đồng.

## 1. Tên Đề Tài

Tên tiếng Việt:

**Xây dựng hệ thống phát hiện xâm nhập mạng kết hợp học máy có giải thích và mô hình ngôn ngữ lớn tăng cường truy hồi hỗ trợ phân tích cảnh báo an ninh.**

Tên tiếng Anh:

**An Explainable Machine Learning and Retrieval-Augmented Large Language Model System for Network Intrusion Detection and Security Alert Analysis.**

Giải thích ngắn:

- Hệ thống phát hiện xâm nhập giúp nhận biết hành vi mạng bất thường.
- Học máy dùng để phân loại dữ liệu mạng là bình thường hay tấn công.
- Mô hình ngôn ngữ lớn dùng để giải thích cảnh báo bằng ngôn ngữ dễ hiểu.
- RAG là cách lấy thêm tài liệu liên quan trước khi mô hình ngôn ngữ tạo câu trả lời.

## 2. Lý Do Chọn Đề Tài

Hiện nay, các hệ thống phát hiện xâm nhập mạng có thể tạo ra nhiều cảnh báo. Tuy nhiên, nhiều cảnh báo chỉ có thông tin kỹ thuật như địa chỉ IP, cổng mạng, loại tấn công hoặc điểm tin cậy.

Người phân tích an ninh không chỉ cần biết có tấn công hay không. Họ còn cần biết:

- Vì sao cảnh báo này nguy hiểm?
- Bằng chứng kỹ thuật là gì?
- Cảnh báo này nên xử lý trước hay sau?
- Cần phản ứng như thế nào?

Học máy có thể giúp phát hiện tấn công trên dữ liệu có cấu trúc. Nhưng kết quả của học máy thường khó hiểu với người không trực tiếp xây dựng mô hình.

Mô hình ngôn ngữ lớn có thể giải thích bằng văn bản tự nhiên. Tuy nhiên, mô hình ngôn ngữ có thể trả lời sai nếu không được cung cấp ngữ cảnh rõ ràng. Vì vậy, đề tài không dùng mô hình ngôn ngữ để quyết định phát hiện tấn công. Đề tài chỉ dùng nó để hỗ trợ giải thích sau khi hệ thống IDS hoặc học máy đã tạo cảnh báo.

## 3. Vấn Đề Nghiên Cứu

Một hệ thống IDS thông thường thường trả lời câu hỏi:

```text
Sự kiện này có đáng nghi hay không?
```

Nhưng trong thực tế, người phân tích cần thêm các câu trả lời:

- Vì sao sự kiện này đáng nghi?
- Những đặc trưng nào làm hệ thống nghi ngờ?
- Cảnh báo này có liên quan đến kỹ thuật tấn công nào?
- Mức độ ưu tiên xử lý là gì?
- Nên kiểm tra hoặc phản ứng như thế nào?

Vấn đề của đề tài là xây dựng một hệ thống giúp nối khoảng cách giữa phát hiện tấn công và phân tích cảnh báo.

## 4. Mục Tiêu Nghiên Cứu

Mục tiêu chính của đề tài là xây dựng một prototype hỗ trợ phát hiện xâm nhập và giải thích cảnh báo an ninh.

Các mục tiêu cụ thể:

1. Xây dựng quy trình xử lý dữ liệu mạng dạng CSV.
2. Huấn luyện và so sánh một số mô hình học máy cơ bản.
3. Tạo cảnh báo có thông tin dễ hiểu hơn, gồm mức độ nghiêm trọng, độ tin cậy và đặc trưng bằng chứng.
4. Gắn cảnh báo với kỹ thuật tấn công tương ứng trong MITRE ATT&CK.
5. Dùng RAG và mô hình ngôn ngữ để giải thích cảnh báo.
6. So sánh các kiểu giải thích: mẫu cố định, không dùng RAG và có dùng RAG.
7. Xây dựng dashboard SOC để minh họa quá trình phân tích cảnh báo.
8. Xuất các báo cáo và kết quả để phục vụ đánh giá luận văn.

## 5. Câu Hỏi Nghiên Cứu

Đề tài tập trung vào bốn câu hỏi:

1. Các mô hình học máy cơ bản phát hiện tấn công trên dữ liệu mạng tốt đến mức nào?
2. Việc thêm bằng chứng kỹ thuật, mức độ nghiêm trọng và MITRE ATT&CK có làm cảnh báo dễ hiểu hơn không?
3. Giải thích có dùng RAG có tốt hơn giải thích không dùng RAG không?
4. Prototype có thể mô phỏng được quy trình làm việc của một hệ thống SOC ở mức nghiên cứu không?

## 6. Phạm Vi Đề Tài

Trong phạm vi:

- Dữ liệu mạng dạng CSV, xử lý offline.
- Dataset chính dự kiến là UNSW-NB15.
- Dataset phụ có thể dùng là CICIDS2017 hoặc CSE-CIC-IDS2018 nếu đủ thời gian.
- Mô hình học máy cơ bản gồm Logistic Regression, Decision Tree và Random Forest.
- Dashboard dùng để minh họa cảnh báo, kết quả mô hình và phần giải thích.
- RAG dùng tài liệu playbook an ninh cục bộ.

Ngoài phạm vi:

- Không bắt gói mạng realtime.
- Không tự động chặn IP trong mạng thật.
- Không thay thế hệ thống SIEM/SOAR.
- Không fine-tune mô hình ngôn ngữ.
- Không xem mô hình ngôn ngữ là bộ phát hiện tấn công chính.

## 7. Dữ Liệu Nghiên Cứu

Dữ liệu đầu vào là dữ liệu network-flow. Đây là dữ liệu mô tả luồng mạng, ví dụ:

- Địa chỉ IP nguồn và đích.
- Cổng nguồn và cổng đích.
- Giao thức mạng.
- Số lượng gói tin.
- Tốc độ truyền dữ liệu.
- Số lần đăng nhập thất bại.
- Nhãn bình thường hoặc tấn công.

Các nguồn dữ liệu dự kiến:

- Dữ liệu mẫu nhỏ để demo và kiểm thử.
- UNSW-NB15 cho thực nghiệm chính.
- CICIDS2017 hoặc CSE-CIC-IDS2018 nếu còn thời gian.

## 8. Phương Pháp Thực Hiện

### 8.1 Xử Lý Dữ Liệu

Hệ thống sẽ đọc dữ liệu CSV, làm sạch dữ liệu, xử lý giá trị thiếu và chuyển dữ liệu về dạng phù hợp cho học máy.

Kết quả của bước này là file dữ liệu đã xử lý, có thể dùng lại để huấn luyện mô hình.

### 8.2 Huấn Luyện Mô Hình

Đề tài sẽ huấn luyện các mô hình học máy cơ bản:

- Logistic Regression.
- Decision Tree.
- Random Forest.

Các mô hình được đánh giá bằng các chỉ số:

- Accuracy: tỷ lệ dự đoán đúng.
- Precision: trong các cảnh báo tấn công, có bao nhiêu cảnh báo đúng.
- Recall: trong các tấn công thật, hệ thống phát hiện được bao nhiêu.
- F1-score: chỉ số cân bằng giữa precision và recall.
- False positive rate: tỷ lệ cảnh báo nhầm.
- Confusion matrix: bảng cho biết mô hình đúng và sai ở đâu.

### 8.3 Làm Giàu Cảnh Báo

Sau khi phát hiện, hệ thống tạo cảnh báo có thêm thông tin:

- Loại tấn công.
- Mức độ nghiêm trọng.
- Độ tin cậy.
- Lý do kỹ thuật.
- Các đặc trưng quan trọng.
- Kỹ thuật MITRE ATT&CK liên quan.
- Mức ưu tiên xử lý.

Mục tiêu là giúp cảnh báo dễ hiểu hơn so với chỉ có nhãn tấn công.

### 8.4 Giải Thích Bằng RAG Và Mô Hình Ngôn Ngữ

Hệ thống sẽ so sánh ba cách giải thích:

- Giải thích theo mẫu cố định.
- Giải thích bằng mô hình ngôn ngữ nhưng không dùng tài liệu truy hồi.
- Giải thích bằng mô hình ngôn ngữ có dùng RAG.

RAG sẽ lấy tài liệu playbook phù hợp, ví dụ playbook về brute force, DDoS hoặc port scan. Sau đó mô hình ngôn ngữ dùng thông tin cảnh báo và tài liệu này để tạo giải thích.

## 9. Kiến Trúc Hệ Thống

Luồng xử lý chính:

```text
Dữ liệu mạng
  -> Xử lý dữ liệu
  -> Mô hình phát hiện tấn công
  -> Tạo cảnh báo
  -> Bổ sung bằng chứng và mức ưu tiên
  -> Lấy tài liệu liên quan bằng RAG
  -> Giải thích bằng mô hình ngôn ngữ
  -> Hiển thị trên dashboard
  -> Xuất báo cáo đánh giá
```

Các thành phần chính:

- Backend FastAPI: cung cấp API cho dữ liệu, cảnh báo, giải thích và kết quả đánh giá.
- Frontend React: hiển thị dashboard SOC.
- Scripts: dùng để xử lý dữ liệu, huấn luyện mô hình và xuất báo cáo.
- Knowledge base: chứa các playbook an ninh.
- Reports: chứa kết quả đánh giá và báo cáo phục vụ luận văn.

Thông điệp quan trọng của kiến trúc:

```text
IDS/học máy phát hiện.
RAG/mô hình ngôn ngữ giải thích.
Con người ra quyết định cuối cùng.
```

## 10. Prototype Hiện Tại

Hiện tại project đã có:

- Backend FastAPI.
- Dashboard React.
- Dữ liệu mẫu.
- API danh sách dataset.
- Script xử lý dữ liệu mẫu theo cấu trúc UNSW-NB15.
- Script huấn luyện Logistic Regression, Decision Tree và Random Forest.
- Xuất kết quả đánh giá mô hình.
- Xuất confusion matrix.
- Xuất feature importance.
- Cảnh báo có mức độ nghiêm trọng, độ tin cậy, đặc trưng bằng chứng và MITRE mapping.
- Playbook an ninh cục bộ.
- API giải thích cảnh báo.
- API so sánh các kiểu giải thích.
- Báo cáo đánh giá LLM/RAG.
- Demo script và bộ câu hỏi trả lời khi bảo vệ.

Lưu ý khi trình bày:

Kết quả hiện tại chủ yếu dùng dữ liệu mẫu nhỏ để chứng minh hệ thống chạy được từ đầu đến cuối. Đây chưa phải là kết quả thực nghiệm cuối cùng.

## 11. Kế Hoạch Đánh Giá

### 11.1 Đánh Giá Phần Phát Hiện Tấn Công

Đánh giá mô hình trên dataset chính và dataset phụ nếu có.

Kết quả cần có:

- Bảng so sánh mô hình.
- Confusion matrix.
- Các chỉ số accuracy, precision, recall, F1-score và false positive rate.

### 11.2 Đánh Giá Phần Giải Thích

Đánh giá xem cảnh báo có dễ hiểu hơn không khi có:

- Đặc trưng quan trọng.
- Lý do kỹ thuật.
- MITRE ATT&CK.
- Mức ưu tiên xử lý.

### 11.3 Đánh Giá RAG Và Mô Hình Ngôn Ngữ

So sánh ba kiểu giải thích:

- Mẫu cố định.
- Không dùng RAG.
- Có dùng RAG.

Tiêu chí đánh giá:

- Giải thích có đúng với cảnh báo không?
- Giải thích có đủ thông tin không?
- Giải thích có dựa trên bằng chứng không?
- Gợi ý xử lý có cụ thể không?
- Có sinh thông tin không có căn cứ không?
- Thời gian trả lời có chấp nhận được không?

## 12. Kết Quả Dự Kiến

Kết quả kỹ thuật:

- Một backend API hoạt động được.
- Một dashboard SOC để demo.
- Pipeline xử lý dữ liệu và huấn luyện mô hình.
- Bảng kết quả so sánh mô hình.
- Báo cáo confusion matrix và feature importance.
- Chức năng giải thích cảnh báo bằng RAG/mô hình ngôn ngữ.
- Báo cáo so sánh các kiểu giải thích.

Kết quả nghiên cứu:

- Chứng minh tính khả thi của việc kết hợp IDS/học máy với RAG/mô hình ngôn ngữ.
- Cho thấy RAG có thể giúp phần giải thích có căn cứ hơn.
- Chỉ ra giới hạn của prototype và hướng phát triển tiếp theo.

## 13. Đóng Góp Dự Kiến

Đề tài dự kiến có các đóng góp:

1. Một prototype phát hiện và phân tích cảnh báo xâm nhập mạng.
2. Một quy trình xử lý dữ liệu, huấn luyện và đánh giá mô hình có thể tái lập.
3. Một cách làm giàu cảnh báo bằng bằng chứng kỹ thuật và MITRE ATT&CK.
4. Một cách dùng RAG/mô hình ngôn ngữ để giải thích cảnh báo.
5. Một dashboard và bộ báo cáo hỗ trợ trình bày kết quả luận văn.

## 14. Kế Hoạch Thực Hiện

| Thời gian | Công việc chính | Kết quả dự kiến |
| --- | --- | --- |
| Tháng 1 | Hoàn thiện đề cương, đọc tài liệu, ổn định kiến trúc | Đề cương, sơ đồ hệ thống, demo mẫu |
| Tháng 2 | Xử lý UNSW-NB15, huấn luyện mô hình cơ bản | Dữ liệu đã xử lý, kết quả baseline |
| Tháng 3 | So sánh mô hình, thử dataset phụ nếu có | Bảng so sánh mô hình, confusion matrix |
| Tháng 4 | Bổ sung giải thích và làm giàu cảnh báo | Top features, MITRE mapping, mức ưu tiên |
| Tháng 5 | Hoàn thiện RAG/LLM và dashboard | API giải thích, dashboard demo, báo cáo đánh giá |
| Tháng 6 | Tổng hợp kết quả, viết luận văn, chuẩn bị bảo vệ | Luận văn, slide, demo script |

## 15. Rủi Ro Và Cách Xử Lý

| Rủi ro | Cách xử lý |
| --- | --- |
| Dataset lớn hoặc khó xử lý | Dùng subset có kiểm soát, ưu tiên UNSW-NB15 trước |
| Kết quả mô hình chưa tốt | So sánh nhiều mô hình và phân tích rõ nguyên nhân |
| Mô hình ngôn ngữ trả lời sai | Dùng RAG, giới hạn ngữ cảnh và đánh giá lỗi sinh thông tin sai |
| Phạm vi quá rộng | Không làm realtime, không làm production SIEM/SOAR |
| Không đủ thời gian tích hợp LLM thật | Dùng template hoặc mô hình cục bộ để đảm bảo demo ổn định |

## 16. Lời Mở Đầu Gợi Ý

Kính thưa hội đồng, đề tài của em tập trung vào bài toán phát hiện xâm nhập mạng và hỗ trợ phân tích cảnh báo an ninh. Trong thực tế, hệ thống IDS hoặc mô hình học máy có thể phát hiện sự kiện đáng nghi, nhưng cảnh báo thường khó hiểu và cần thêm ngữ cảnh để xử lý. Vì vậy, em đề xuất một hệ thống kết hợp học máy với RAG và mô hình ngôn ngữ lớn. Trong hệ thống này, học máy chịu trách nhiệm phát hiện, còn mô hình ngôn ngữ chỉ hỗ trợ giải thích và đề xuất hướng xử lý.

## 17. Lời Kết Thúc Gợi Ý

Tóm lại, đề tài hướng đến một prototype có thể đi từ dữ liệu mạng, phát hiện tấn công, tạo cảnh báo, giải thích cảnh báo và hiển thị trên dashboard SOC. Điểm quan trọng là hệ thống không dùng mô hình ngôn ngữ để thay thế IDS. Mô hình ngôn ngữ chỉ đóng vai trò hỗ trợ người phân tích hiểu cảnh báo nhanh hơn và có căn cứ hơn.
