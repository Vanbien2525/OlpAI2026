# Luyện Olympic Trí tuệ nhân tạo — Buổi 08 (Bản mở rộng có giải thích)
### KNN, cây quyết định, rừng ngẫu nhiên, boosting

> Luyện Olympic Trí tuệ nhân tạo
> Buổi 08
> KNN, cây quyết định, rừng ngẫu nhiên, boosting
> Phần: Học máy cổ điển
> Phục vụ: sơ loại
> Ngày 25 tháng 8 năm 2026
> TS. Đỗ Phúc Hảo

🧠 **Bối cảnh buổi học:**
- Đây là buổi thứ 8 trong chuỗi ôn luyện Olympic AI, thuộc mảng "Học máy cổ điển" (classical ML) — đối lập với deep learning. Bốn thuật toán được học hôm nay đều **không dùng mạng nơ-ron**, mà dựa trên các nguyên lý hình học (KNN), lý thuyết thông tin (cây quyết định), và tổ hợp mô hình (rừng ngẫu nhiên, boosting).
- "Phục vụ: sơ loại" nghĩa là kiến thức này nhắm tới vòng thi loại (thường trắc nghiệm + code ngắn), chứ chưa phải vòng chung kết cần độ sâu lý thuyết cực cao.

---

## 1. Mục tiêu

> Chọn đúng mô hình cho một bảng dữ liệu lạ trong mười phút, và giải thích được lựa chọn ấy bằng số chứ
> không bằng thói quen.
>
> Buổi này cũng trả lời câu hỏi buổi 07 để lại: vì sao gộp nhiều mô hình yếu lại ra một mô hình mạnh? Câu
> trả lời ngắn: chỉ khi những mô hình yếu ấy sai khác nhau.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là triết lý xuyên suốt cả khoá: **thực chứng hơn giáo điều**. Rất nhiều người học máy nhớ các "câu thần chú" kiểu "KNN luôn cần chuẩn hoá", "cây sâu hơn luôn tốt hơn trên tập test", "rừng càng nhiều cây càng tốt" — nhưng bài giảng này liên tục đo đạc để chứng minh những câu ấy **chỉ đúng có điều kiện**.
- Câu hỏi "vì sao gộp nhiều mô hình yếu ra một mô hình mạnh" chính là bản chất của **ensemble learning**. Ẩn dụ dễ hình dung: nếu bạn hỏi 100 người *giống hệt nhau về kiến thức và cùng mắc một loại sai lầm* (ví dụ tất cả đều tin trái đất phẳng), thì lấy trung bình ý kiến của 100 người ấy vẫn ra kết quả sai — bởi vì sai lầm của họ **tương quan hoàn toàn** với nhau. Ngược lại, nếu 100 người có kiến thức khác nhau, sai ở những chỗ khác nhau (độc lập tương đối), thì lấy đa số phiếu sẽ triệt tiêu bớt nhiễu riêng của từng người, và phần "tín hiệu thật" mà đa số đồng ý sẽ nổi lên. Đây chính là nội dung mục 2.4 (rừng ngẫu nhiên) sẽ chứng minh bằng số.

---

## 2. Tóm tắt kiến thức

> Cả buổi dùng một bộ dữ liệu duy nhất: training_set.csv của tác vụ 1, 6000 dòng, nhãn 1 là câu Tơ Ma
> đúng ngữ pháp, nhãn 0 là câu bị làm hỏng. Chia 80/20 với random_state=0, và mọi con số dưới đây là
> macro-F1 trên phần 20% ấy.
>
> Bốn mô hình mới của buổi này đều làm việc trên bảng số, nên trước hết phải biến câu chữ thành bảng số.
> Tôi lấy tám đặc trưng mà một người bình thường nghĩ ra trong mười phút:

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- **"Tơ Ma"** là một ngôn ngữ nhân tạo (constructed language) được dùng xuyên suốt khoá học như bài toán benchmark — mục đích là tránh việc mô hình "ăn gian" nhờ đã học sẵn tiếng Anh/tiếng Việt từ dữ liệu huấn luyện khổng lồ trước đó. Với một ngôn ngữ hoàn toàn mới, mô hình buộc phải học *cấu trúc* thay vì *ghi nhớ từ vựng quen thuộc*.
- **Macro-F1** là trung bình cộng của F1-score trên từng lớp (không có trọng số theo số lượng mẫu), khác với micro-F1 hay accuracy thông thường. Chọn macro-F1 giúp đánh giá công bằng cả hai nhãn (0 và 1) dù chúng có thể không cân bằng tuyệt đối (ở đây gần cân bằng: 2564/4800 ≈ 53%).
- **`random_state=0`** cố định hạt giống ngẫu nhiên khi chia tập train/test — đảm bảo mọi người chạy lại đều ra đúng cùng một cách chia, phục vụ việc tái lập kết quả (reproducibility), một chủ đề được nhấn đi nhấn lại trong tài liệu (xem phần "Rừng từng cho ra hai con số khác nhau" ở mục 3).
- **Feature engineering thủ công**: khác với buổi 05 (dùng TF-IDF tự động sinh ra 2143 đặc trưng), buổi này cố tình dùng 8 đặc trưng "thô sơ" con người tự nghĩ ra, để minh hoạ rằng *chất lượng biểu diễn dữ liệu quan trọng hơn thuật toán* — một kết luận được nhấn mạnh ở cuối mục 3.

> | Cột | Nghĩa | Số giá trị khác nhau |
> |---|---|---|
> | so_tu | số từ trong câu | 7 |
> | so_ky_tu | số ký tự | 69 |
> | do_dai_tu_tb | độ dài từ trung bình | 117 |
> | tu_dai_nhat | độ dài từ dài nhất | 14 |
> | tu_ngan_nhat | độ dài từ ngắn nhất | 8 |
> | so_tu_co_gach | số từ có dấu gạch nối | 4 |
> | so_tu_khac_nhau | số từ khác nhau | 7 |
> | so_dau_gach | tổng số dấu gạch nối | 5 |

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Cột **"Số giá trị khác nhau"** (cardinality) sẽ trở lại rất quan trọng ở mục 2.6: các cột có cardinality cao (như `do_dai_tu_tb` với 117 giá trị) dễ bị cây quyết định "thiên vị" khi tính độ quan trọng theo impurity — đây là một cái bẫy kinh điển trong feature importance mà bài giảng sẽ chỉ ra bằng số liệu thực.
- Việc liệt kê cardinality ngay từ đầu là một kỹ thuật sư phạm thông minh: nó gieo hạt giống để người học tự nhớ lại về sau khi đọc tới mục 2.6, thay vì phải học lại từ đầu.

> ```python
> import numpy as np
> def dac_trung(s):
>     """Turn one sentence into eight numbers."""
>     t = s.split()
>     d = [len(x) for x in t]
>     return [len(t), len(s), float(np.mean(d)), max(d), min(d),
>             sum(1 for x in t if "-" in x), len(set(t)), s.count("-")]
> X = np.array([dac_trung(s) for s in tr["van_ban_goc"]], dtype=float)
> ```

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đọc kỹ đoạn code này: `t = s.split()` tách câu thành danh sách từ theo khoảng trắng; `d = [len(x) for x in t]` là danh sách độ dài từng từ.
- Hàm trả về đúng 8 số theo thứ tự: `len(t)` (số từ), `len(s)` (số ký tự cả câu, **bao gồm cả khoảng trắng và dấu**), `np.mean(d)` (độ dài từ trung bình), `max(d)`, `min(d)` (từ dài nhất/ngắn nhất), số từ chứa dấu `-`, `len(set(t))` (số từ **khác nhau**, tức đã loại trùng lặp), và `s.count("-")` (tổng số dấu gạch nối trong toàn câu — khác với "số từ có dấu gạch": một từ có thể chứa nhiều hơn một dấu gạch).
- Đây là ví dụ điển hình của **feature engineering dựa trên domain knowledge**: người viết code đã đoán trước rằng dấu gạch nối `-` có liên quan tới ngữ pháp (thực tế mục 2.2 sẽ xác nhận: hậu tố thì trong tiếng Tơ Ma viết sau dấu gạch).

### 2.1 KNN: không có huấn luyện, chỉ có đo khoảng cách

> KNN không học gì cả. Nó nhớ toàn bộ tập huấn luyện, và khi gặp một điểm mới thì tìm k điểm gần nhất rồi
> bỏ phiếu. Toàn bộ mô hình nằm ở hai chữ gần nhất, mà gần hay xa thì lại phụ thuộc vào đơn vị đo của từng
> cột.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- KNN (K-Nearest Neighbors) là mô hình **"lazy learning"** (học lười) — không có bước "fit" tính toán tham số như hồi quy hay cây quyết định. `.fit()` của KNN chỉ đơn giản là lưu lại dữ liệu vào bộ nhớ. Toàn bộ "trí tuệ" nằm ở bước `.predict()`: với điểm mới, tính khoảng cách (thường là Euclidean) tới **mọi** điểm trong tập huấn luyện, chọn ra k điểm gần nhất, rồi bỏ phiếu theo đa số nhãn.
- Ẩn dụ: giống như hỏi ý kiến k người hàng xóm gần nhà bạn nhất để đoán bạn thuộc "khu dân cư" nào — nếu đa số hàng xóm gần nhất là công nhân, bạn có thể được đoán là công nhân.
- Điểm mấu chốt: khái niệm "gần" hoàn toàn phụ thuộc vào **đơn vị đo**. Nếu một cột đo bằng mét và cột khác đo bằng milimét, "khoảng cách" sẽ bị chi phối gần như hoàn toàn bởi cột có con số lớn hơn — dù về mặt thông tin hai cột có thể quan trọng ngang nhau.

> Đây là chỗ dễ nói suông nhất trong cả môn học, nên tôi dựng một ví dụ để nhìn thấy cơ chế. Hai cột: cột
> 0 có thông tin thật, thang đo cỡ 1; cột 1 là nhiễu thuần tuý, thang đo cỡ 500.
>
> | KNN k = 5 trên ví dụ dựng | macro-F1 |
> |---|---|
> | dùng cả hai cột, không chuẩn hoá | 0,5478 |
> | dùng cả hai cột, có chuẩn hoá | 0,9132 |
> | chỉ dùng cột 0 | 0,8999 |
>
> Cột nhiễu có thang đo lớn gấp 500 lần nên nó chiếm gần hết khoảng cách, và KNN thực chất đi tìm hàng
> xóm theo nhiễu. Chuẩn hoá kéo hai cột về cùng thang, và điểm nhảy từ 0,5478 lên 0,9132.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là một **thí nghiệm được dựng có chủ đích (synthetic experiment)** để cô lập hiệu ứng, khác với dữ liệu thật ở phần sau. Con số 0,5478 gần với "đoán ngẫu nhiên" (macro-F1 của một mô hình đoán hú hoạ trên bài toán 2 lớp cân bằng thường quanh 0,50), chứng tỏ khi không chuẩn hoá, mô hình gần như **hoàn toàn mù** trước tín hiệu thật ở cột 0 — vì khoảng cách Euclidean bị cột nhiễu (thang đo x500) áp đảo.
- Thú vị hơn: "chỉ dùng cột 0" (0,8999) còn **thấp hơn một chút** so với "cả hai cột + chuẩn hoá" (0,9132). Điều này gợi ý rằng cột nhiễu, sau khi đã chuẩn hoá về cùng thang đo, không hoàn toàn vô dụng — có thể nó mang một lượng thông tin rất nhỏ ngẫu nhiên trùng hợp, hoặc đơn giản là nhiễu thống kê giữa hai lần chạy. Đây là lý do bài giảng luôn nhấn mạnh việc so sánh với "dải nhiễu" (xem đoạn dưới).
- **Chuẩn hoá (standardization/normalization)** phổ biến nhất là `StandardScaler` (đưa mỗi cột về trung bình 0, độ lệch chuẩn 1) hoặc `MinMaxScaler` (đưa về khoảng [0,1]). Công thức chuẩn hoá Z-score: $z = \dfrac{x - \mu}{\sigma}$.

> Nhưng đừng đem kết luận ấy áp thẳng vào bộ dữ liệu thật
>
> Trên tám đặc trưng thật ở trên, tôi nhân cột so_ky_tu lần lượt với 0,001, 1, 10, 1000, tức là đổi đơn vị
> đo mà không đổi một chút thông tin nào:
>
> | Hệ số nhân | 0,001 | 1 | 10 | 1000 |
> |---|---|---|---|---|
> | KNN thô | 0,5731 | 0,5875 | 0,5756 | 0,5797 |
> | KNN chuẩn hoá | 0,5683 | 0,5670 | 0,5655 | 0,5663 |
>
> Cả dải dao động của dòng trên là 0,0143, tức là nhỏ hơn dải nhiễu 0,0177 mà buổi 07 đo được khi chỉ
> đổi seed. Nói cách khác: ở bộ dữ liệu này, hiệu ứng đổi thang đo chìm trong nhiễu, và chuẩn hoá còn
> làm điểm hơi tệ đi.
>
> Cơ chế là có thật, và nó có thể giết bài của bạn. Nhưng nó có xảy ra hay không thì phải đo, không suy
> ra từ câu khẩu hiệu "KNN luôn cần chuẩn hoá".

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là điểm **quan trọng nhất** của cả mục 2.1, và cũng là ví dụ mẫu mực về tư duy thực chứng: thí nghiệm dựng (synthetic) chứng minh **cơ chế tồn tại**, nhưng thí nghiệm trên dữ liệu thật cho thấy **cơ chế đó không nhất thiết chi phối kết quả cuối** — vì trên 8 đặc trưng thật, các cột vốn đã có thang đo tương đối gần nhau (không lệch x500 như thí nghiệm dựng), nên việc nhân thêm hệ số vào một cột duy nhất không đủ để một mình nó áp đảo 7 cột còn lại.
- **"Dải nhiễu" (noise band)** 0,0177 là khái niệm cực kỳ quan trọng xuất hiện xuyên suốt tài liệu: đó là mức dao động tự nhiên của điểm số **chỉ vì đổi random seed**, chưa cần đổi gì về mô hình hay dữ liệu. Nếu chênh lệch giữa hai cấu hình nhỏ hơn dải nhiễu này, ta **không được phép** kết luận cấu hình nào tốt hơn — vì có thể chênh lệch đó chỉ là may rủi ngẫu nhiên, không phải hiệu ứng thật. Đây chính là tinh thần thống kê: đừng diễn giải nhiễu như tín hiệu.
- Bài học phương pháp luận: một quy tắc kinh nghiệm ("KNN cần chuẩn hoá") có thể đúng về *nguyên lý* nhưng sai về *mức độ tác động* trong một tình huống cụ thể. Người làm khoa học dữ liệu giỏi luôn **đo trước khi áp dụng quy tắc**, thay vì áp dụng quy tắc một cách máy móc.

> Chọn k cũng vậy. Cùng tám đặc trưng ấy, có chuẩn hoá:
>
> | k | 1 | 3 | 5 | 11 | 25 | 51 |
> |---|---|---|---|---|---|---|
> | tập đã học | 0,7826 | 0,7436 | 0,7212 | 0,6807 | 0,6521 | 0,6345 |
> | kiểm định | 0,5874 | 0,5764 | 0,5670 | 0,6023 | 0,5960 | 0,6092 |
>
> Cột tập đã học giảm đều khi k tăng, và điều đó thì luôn đúng: k = 1 nghĩa là mỗi điểm huấn luyện tự
> nhận chính nó làm hàng xóm gần nhất. Nhưng cột kiểm định chỉ đi loanh quanh trong dải 0,042, phần lớn là
> nhiễu. Đổi k không cứu được một cách biểu diễn nghèo, và mục 3 sẽ cho thấy cái gì mới cứu được.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- **Vì sao k=1 luôn cho điểm "tập đã học" cao nhất (gần như tuyệt đối)?** Vì khi dự đoán trên chính tập huấn luyện, hàng xóm gần nhất của một điểm chính là **bản thân nó** (khoảng cách = 0), nên nó luôn "đoán đúng" nhãn của chính mình. Đây là dấu hiệu kinh điển của **overfitting cực đoan**: mô hình không tổng quát hoá, chỉ ghi nhớ.
- k càng lớn thì mỗi dự đoán càng "được làm mượt" (smoothed) bởi càng nhiều hàng xóm, nên đường biên quyết định càng đơn giản, ít khớp sát dữ liệu huấn luyện hơn → điểm tập học giảm dần. Đây là quan hệ **đơn điệu, luôn đúng về mặt toán học**, không phụ thuộc dữ liệu.
- Nhưng điểm kiểm định (validation) **không đơn điệu** và dao động trong khoảng hẹp (0,042) — nhỏ hơn hoặc gần bằng dải nhiễu đã nêu, cho thấy việc "tinh chỉnh siêu tham số k" trên bộ đặc trưng 8 cột này gần như **vô ích**: bài toán không nằm ở việc chọn k bao nhiêu, mà nằm ở việc 8 đặc trưng đó vốn dĩ không đủ để phân biệt hai lớp tốt hơn. Đây là một minh hoạ tuyệt vời cho nguyên lý "garbage in, garbage out" trong học máy — không có thuật toán nào (dù tinh chỉnh cỡ nào) có thể vượt qua giới hạn thông tin vốn có trong biểu diễn dữ liệu đầu vào.

---

### 2.2 Cây quyết định, và một nút gốc tính tay

> Cây hỏi từng câu hỏi dạng cột j có nhỏ hơn ngưỡng t không, rồi chia đôi dữ liệu. Nó chọn câu hỏi làm cho
> hai phần con thuần nhất có thể. Hai thước đo độ thuần:
>
> Gini(S) = 1 − ∑c p²c, &nbsp;&nbsp; H(S) = − ∑c pc log2 pc.
>
> Cả hai bằng 0 khi nút chỉ còn một lớp, và lớn nhất khi hai lớp chia đôi. Chất lượng một phép chia là độ
> giảm có trọng số:
>
> ∆ = I(S) − (|SL|/|S|) I(SL) − (|SR|/|S|) I(SR).

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- **Cây quyết định (Decision Tree)** hoạt động như trò chơi "20 câu hỏi": tại mỗi nút, nó chọn một cột và một ngưỡng sao cho câu hỏi "cột này có nhỏ hơn ngưỡng không?" chia dữ liệu thành hai nhóm càng "thuần" (chỉ chứa một loại nhãn) càng tốt.
- **Chỉ số Gini** đo "xác suất phân loại sai nếu ta gán nhãn ngẫu nhiên theo tỉ lệ hiện có trong nhóm". Với 2 lớp có xác suất $p$ và $1-p$: $Gini = 1 - p^2 - (1-p)^2 = 2p(1-p)$. Giá trị lớn nhất là 0,5 khi $p=0,5$ (hai lớp chia đôi hoàn toàn, hỗn loạn nhất); bằng 0 khi $p=0$ hoặc $p=1$ (nhóm thuần tuyệt đối).
- **Entropy** $H(S) = -\sum p_c \log_2 p_c$ xuất phát từ lý thuyết thông tin của Shannon — đo "số bit trung bình cần để mô tả nhãn của một mẫu ngẫu nhiên rút từ tập đó". Cùng logic: bằng 0 khi thuần, lớn nhất (=1 bit với 2 lớp) khi $p=0,5$.
- **Information Gain (∆)** là công thức tổng quát: độ thuần của nút cha trừ đi trung bình có trọng số (theo kích thước) độ thuần của hai nút con. Cây quyết định thử **mọi** cặp (cột, ngưỡng) có thể và chọn cặp cho ∆ lớn nhất — đây gọi là thuật toán **tham lam (greedy)**, vì nó chỉ tối ưu cục bộ tại từng nút, không nhìn trước các tầng sâu hơn (điểm này sẽ quay lại ở mục 2.3).

> Đây là nút gốc thật mà scikit-learn chọn trên 4800 dòng huấn luyện:
>
> | Nút | Số dòng | Nhãn 1 | Gini | Entropy |
> |---|---|---|---|---|
> | gốc | 4800 | 2564 | 0,497665 | 0,996629 |
> | trái so_dau_gach ≤ 0,5 | 421 | 0 | 0 | 0 |
> | phải | 4379 | 2564 | 0,485372 | |
>
> Tính lại bằng tay, nhánh trái trước:
>
> p1 = 2564/4800 = 0,534167, &nbsp; Ginigốc = 1 − 0,534167² − 0,465833² = 0,497665.
>
> Nhánh trái có 421 dòng và không có dòng nào nhãn 1, nên Gini = 0. Trọng số:
>
> (421/4800)·0 + (4379/4800)·0,485372 = 0,442801, &nbsp; ∆Gini = 0,497665 − 0,442801 = 0,054864.
>
> Với entropy thì ∆ = 0,996629 − 0,892944 = 0,103685. Hai thước cho hai con số khác nhau nhưng xếp
> hạng các phép chia gần như giống nhau, nên trong thi thì chọn cái nào cũng được.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là một ví dụ **tính tay hoàn chỉnh**, rất đáng tự làm lại từng bước bằng máy tính cầm tay để quen tay cho thi sơ loại (đề bài 2 ở mục 4 yêu cầu chính xác việc này nhưng không dùng máy tính).
- Cách đọc bảng: nút gốc có 4800 dòng, trong đó 2564 dòng nhãn 1 (~53,4%) — khá cân bằng, nên Gini gốc gần với giá trị lớn nhất có thể (0,5). Sau khi chia theo điều kiện `so_dau_gach ≤ 0,5` (tức là câu **không có dấu gạch nối nào**, vì so_dau_gach là số nguyên nên ≤0,5 tương đương =0), nhánh trái có 421 dòng và **toàn bộ đều là nhãn 0** — một sự phân chia hoàn hảo (Gini = 0, Entropy = 0)!
- Công thức trọng số hoá: nhánh trái chiếm 421/4800 (~8,77%) trọng số, nhánh phải chiếm 4379/4800 (~91,23%). Độ giảm tạp chất ∆Gini = 0,054864 nghe có vẻ nhỏ, nhưng đây là *nút gốc tốt nhất trong tất cả các cặp (cột, ngưỡng) có thể* mà scikit-learn tìm ra trên toàn bộ 8 cột — tức là cột `so_dau_gach` mang thông tin phân loại mạnh nhất trong dữ liệu.
- Chú ý một chi tiết tinh tế: entropy gốc là 0,996629 (gần 1 bit, hợp lý vì gần cân bằng 53/47), và entropy nhánh phải (0,892944) không được ghi trong bảng gốc — người viết chỉ đưa ra kết quả cuối để người học tự tính hoặc tra ở bài tập 2.

> Nhánh trái thuần tuyệt đối, và đó là ngữ pháp chứ không phải may mắn
>
> 421 câu không có dấu gạch nối nào thì cả 421 câu đều mang nhãn 0. Lý do nằm trong ngữ pháp Tơ Ma:
> động từ bắt buộc mang hậu tố thì, mà hậu tố thì viết sau dấu gạch. Câu không có dấu gạch nào thì không
> thể có động từ hợp lệ.
>
> Cây tìm ra luật ấy trong một phần nghìn giây, và nó không biết mình vừa tìm ra ngữ pháp. Đấy là cả
> điểm mạnh lẫn điểm yếu của cây: nó đọc được luật cứng, và chỉ đọc được luật nào viết được dưới dạng
> ngưỡng trên một cột.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đoạn này là **triết lý cốt lõi** của cây quyết định so với các mô hình "hộp đen": cây có thể **diễn giải được (interpretable)** — mỗi nút là một luật rõ ràng có thể đọc và hiểu bằng ngôn ngữ tự nhiên ("nếu câu không có dấu gạch nối, thì câu đó sai ngữ pháp"). Đây chính là lý do cây quyết định được ưa chuộng trong các ngành cần giải trình quyết định (y tế, tài chính, pháp lý).
- Nhưng đồng thời đây cũng là **giới hạn cố hữu**: cây chỉ có thể phát hiện những luật biểu diễn được dưới dạng "ngưỡng đơn trên một cột duy nhất" (axis-aligned split). Nếu luật thật phức tạp hơn — ví dụ phụ thuộc vào **tổ hợp phi tuyến** của nhiều cột cùng lúc (như "cột A trừ cột B lớn hơn 5") — cây quyết định đơn lẻ sẽ phải xấp xỉ luật đó bằng rất nhiều nhát cắt hình bậc thang (staircase), kém hiệu quả hơn nhiều so với mô hình có thể học ranh giới xiên hoặc cong.
- Câu "nó không biết mình vừa tìm ra ngữ pháp" nhắc một điều quan trọng: mô hình học máy **không có hiểu biết ngữ nghĩa** — nó chỉ tối ưu một hàm mục tiêu toán học (ở đây là giảm Gini). Việc luật tìm được trùng khớp với ngữ pháp thật của ngôn ngữ Tơ Ma là hệ quả của thiết kế thí nghiệm (đặc trưng `so_dau_gach` được chọn có chủ đích), không phải cây "hiểu" ngôn ngữ.

---

### 2.3 Cây quá khớp thế nào

> Cùng một cây, chỉ đổi max_depth:
>
> | Độ sâu | Tập đã học | Kiểm định | Số lá |
> |---|---|---|---|
> | 1 | 0,5277 | 0,5318 | 2 |
> | 2 | 0,6264 | 0,6086 | 3 |
> | 3 | 0,6040 | 0,5751 | 5 |
> | 5 | 0,6137 | 0,5827 | 17 |
> | 8 | 0,6622 | 0,6086 | 89 |
> | 12 | 0,7029 | 0,6007 | 357 |
> | 20 | 0,8078 | 0,5895 | 1247 |
> | không giới hạn | 0,8200 | 0,5755 | 1434 |
>
> Cột tập đã học đi lên gần như đều, đúng như buổi 07 nói. Cột kiểm định thì không: nó lên tới 0,6086 ở
> độ sâu 2, tụt xuống ở độ sâu 3, lên lại đúng 0,6086 ở độ sâu 8, rồi đi xuống.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- **`max_depth`** giới hạn số tầng câu hỏi tối đa mà cây được phép đặt ra. Độ sâu càng lớn, cây càng có nhiều "lá" (leaf nodes — các nút cuối cùng đưa ra dự đoán), và mỗi lá càng chứa ít dữ liệu hơn, càng dễ khớp sát các đặc điểm riêng (kể cả nhiễu) của tập huấn luyện.
- Quan hệ giữa độ sâu và điểm tập học là **đơn điệu tăng gần như tuyệt đối** — dễ hiểu vì cây sâu hơn có nhiều bậc tự do hơn để "ghi nhớ" dữ liệu huấn luyện. Đây là biểu hiện chuẩn mực của **overfitting**: mô hình càng phức tạp thì càng khớp tốt trên dữ liệu đã thấy.
- Nhưng điều thú vị (và là bài học phương pháp luận) nằm ở cột kiểm định: nó **không đơn điệu** — tăng từ độ sâu 1→2, giảm ở độ sâu 3, dao động lên xuống, rồi giảm dần ở các độ sâu lớn. Đây là hệ quả trực tiếp của việc cây được xây dựng theo thuật toán **tham lam**: mỗi nút tối ưu cục bộ mà không "nhìn trước" hậu quả ở các tầng sau, nên việc thêm một tầng có thể vô tình phá vỡ một cấu trúc tốt đã có ở tầng trên (chọn nhánh chia khác đi so với khi bị giới hạn độ sâu thấp hơn).

> Đường cong không đơn điệu, và đừng bịa lý do cho nó
>
> Cây được dựng tham: mỗi nút chọn phép chia tốt nhất tại chỗ, không hề tính tới việc phép chia ấy làm
> hỏng những nút bên dưới. Cho nên cây sâu hơn không nhất thiết chứa cây nông hơn, và điểm kiểm định
> có thể tụt khi bạn cho thêm một tầng.
>
> Chênh lệch giữa 0,6086 và 0,5751 là 0,0335, tức là lớn hơn dải nhiễu 0,0177 của buổi 07, nên đây không
> hoàn toàn là nhiễu. Nhưng nó cũng không lớn tới mức đáng dựng thành một câu chuyện. Cách đọc bảng
> này cho đúng: ba dòng cuối là quá khớp, còn thứ tự trong bốn dòng đầu thì không đáng tin.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Câu "cây sâu hơn không nhất thiết **chứa** cây nông hơn" là điểm rất tinh tế: người mới học dễ tưởng tượng rằng cây độ sâu 3 chỉ đơn giản là "cây độ sâu 2 cộng thêm một tầng nữa" — nhưng thực tế **không phải vậy**. Vì thuật toán tham lam quyết định phép chia tốt nhất *có tính đến* giới hạn độ sâu còn lại, nên đôi khi phép chia được chọn ở tầng 1 của cây-giới-hạn-độ-sâu-3 có thể khác với phép chia được chọn ở tầng 1 của cây-giới-hạn-độ-sâu-2. Đây là lý do đường cong kiểm định không đơn điệu.
- Đây cũng là bài học **thống kê áp dụng**: 0,0335 > dải nhiễu (0,0177) nên "có thật" theo nghĩa thống kê, nhưng tác giả vẫn thận trọng không "dựng thành câu chuyện" — nghĩa là dù chênh lệch có ý nghĩa thống kê, nó chưa đủ lớn để rút ra một quy luật tổng quát đáng tin cậy về việc "độ sâu nào là tối ưu" chỉ từ một lần chia dữ liệu duy nhất. Đây chính là động lực cho Bài tập 3 (dùng xác thực chéo 5 phần để có ước lượng đáng tin hơn).
- Kết luận thực dụng cho thi sơ loại: nhìn vào bảng, ba dòng cuối (độ sâu 12, 20, không giới hạn) rõ ràng là **quá khớp** (điểm tập học cao ngất nhưng kiểm định giảm dần) — kết luận này an toàn. Nhưng việc so sánh chi tiết độ sâu 2 vs 3 vs 5 vs 8 thì "nhiễu quá, đừng cố phân biệt".

---

### 2.4 Rừng ngẫu nhiên: sai khác nhau thì mới bù được cho nhau

> Bagging dựng n cây, mỗi cây học trên một mẫu bootstrap khác nhau và tại mỗi nút chỉ được nhìn một tập con
> các cột. Hai nguồn ngẫu nhiên ấy làm cho các cây sai ở những chỗ khác nhau, và phiếu bầu đa số triệt tiêu
> bớt phần sai riêng của từng cây.
>
> Nếu tất cả các cây sai giống hệt nhau thì bầu bao nhiêu lần cũng ra cùng một câu sai. Đó là lý do đoán
> mò tập thể vẫn là đoán mò, còn rừng thì không.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- **Bagging** (Bootstrap Aggregating) là kỹ thuật nền tảng của Random Forest. "Bootstrap sample" nghĩa là lấy mẫu **có hoàn lại (with replacement)** từ tập huấn luyện gốc, cùng kích thước với tập gốc — trung bình mỗi mẫu bootstrap chỉ chứa khoảng 63,2% số điểm dữ liệu gốc (một số điểm bị lấy lặp lại, một số điểm không được lấy lần nào — phần bị bỏ sót gọi là "out-of-bag", rất hữu ích để ước lượng lỗi mà không cần tập validation riêng).
- **"Tại mỗi nút chỉ được nhìn một tập con các cột"** là đặc trưng riêng của **Random Forest** (khác Bagging thuần tuý): ngoài việc lấy mẫu dòng ngẫu nhiên, tại mỗi nút cây chỉ được chọn ngẫu nhiên một tập con cột (thường là $\sqrt{d}$ cột với $d$ là tổng số cột) để tìm phép chia tốt nhất. Đây là nguồn ngẫu nhiên thứ hai, giúp **decorrelate** (giảm tương quan) giữa các cây — nếu không có bước này, mọi cây có thể vẫn luôn chọn cùng một cột mạnh nhất ở nút gốc, khiến các cây trở nên tương tự nhau.
- Toán học đằng sau: nếu ta có $n$ ước lượng có phương sai $\sigma^2$ mỗi cái, và chúng có tương quan đôi một trung bình $\rho$, thì phương sai của trung bình cộng $n$ ước lượng đó là:
$$\text{Var}(\bar{X}) = \rho\sigma^2 + \frac{1-\rho}{n}\sigma^2$$
  Khi $n \to \infty$, số hạng thứ hai tiến về 0, nhưng số hạng đầu $\rho\sigma^2$ **không đổi** — đây chính là lý do toán học cho câu "nếu tất cả các cây sai giống hệt nhau (ρ=1) thì bầu bao nhiêu lần cũng ra cùng một câu sai": khi $\rho=1$, công thức trở thành $\text{Var}(\bar{X}) = \sigma^2$, không giảm dù $n$ tăng bao nhiêu. Random Forest cố gắng giảm $\rho$ (độ tương quan giữa các cây) bằng hai nguồn ngẫu nhiên nói trên, để công thức phương sai thực sự giảm theo $n$.

> | Số cây | 1 | 5 | 25 | 100 | 300 | 800 |
> |---|---|---|---|---|---|---|
> | tập đã học | 0,7406 | 0,7918 | 0,8162 | 0,8176 | 0,8177 | 0,8180 |
> | kiểm định | 0,5675 | 0,5756 | 0,5862 | 0,5809 | 0,5873 | 0,5835 |
>
> Từ 1 cây lên 25 cây được 0,0186. Từ 25 cây lên 800 cây thì cả dải chỉ còn 0,0064, nhỏ hơn dải nhiễu buổi
> 07. Nghĩa là trong kỳ thi, tăng số cây từ 100 lên 800 là mua thêm thời gian chạy chứ không mua thêm điểm.
>
> Một lưu ý về cách đọc mọi hiệu số trong tài liệu này: chúng được tính từ số chưa làm tròn, nên có thể
> lệch một đơn vị ở chữ số thập phân thứ tư so với khi bạn lấy hai ô trong bảng trừ tay. Trừ tay hai ô ở trên ra
> 0,0187, còn hiệu thật là 0,0186.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là minh hoạ số học trực tiếp cho công thức phương sai ở trên: số cây tăng từ 1→25 mang lại cải thiện rõ rệt (0,0186), vì $\frac{1-\rho}{n}\sigma^2$ giảm nhanh khi $n$ còn nhỏ. Nhưng từ 25→800, lợi ích gần như bão hoà (0,0064, nhỏ hơn dải nhiễu) — đúng với dạng đường cong $1/n$: phần lớn lợi ích thu được ở những cây đầu tiên, và **lợi ích biên (marginal benefit) giảm dần**.
- Bài học thực dụng cho thi: có một "điểm bão hoà" (ở đây khoảng 100-300 cây) mà sau đó việc tăng thêm số cây chỉ tốn thời gian chạy chứ không cải thiện đáng kể độ chính xác — quan trọng khi thi có giới hạn thời gian (quy chế "20 phút" được nhắc ở mục 3).
- Chi tiết về **sai số làm tròn** là một lưu ý mang tính kỹ thuật số học nghiêm túc: khi bạn tính tay bằng cách lấy hai số đã làm tròn 4 chữ số thập phân trong bảng rồi trừ nhau, kết quả có thể lệch với hiệu số "thật" (tính trên số chưa làm tròn) ở chữ số thứ 4. Đây là một chi tiết dễ bị bỏ qua nhưng quan trọng khi kiểm tra đáp án tự động (cổng kiểm) yêu cầu độ chính xác cao.

---

### 2.5 Boosting: sửa lỗi của chính mình

> Bagging dựng các cây song song và độc lập. Boosting dựng chúng nối tiếp: cây thứ m học phần dư mà m−1
> cây trước còn làm sai. Vì thế boosting thường mạnh hơn, và cũng dễ quá khớp hơn nếu để nó chạy quá lâu.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là điểm khác biệt cốt lõi giữa hai họ ensemble: **Bagging = song song, độc lập, giảm phương sai (variance)**; **Boosting = tuần tự, phụ thuộc, giảm độ chệch (bias)**.
- Cơ chế boosting (kiểu gradient boosting): cây đầu tiên học dự đoán thô. Cây thứ hai không học lại toàn bộ bài toán từ đầu, mà học để dự đoán **phần sai số còn lại (residual)** mà cây thứ nhất chưa giải quyết được. Cây thứ ba học phần sai số còn lại sau cây 1+2, và cứ thế tiếp tục. Kết quả cuối cùng là tổng có trọng số của tất cả các cây: $F(x) = \sum_{m} \eta \cdot h_m(x)$, với $\eta$ là "learning rate" kiểm soát mức đóng góp của mỗi cây mới.
- Ẩn dụ: giống như việc sửa bài văn qua nhiều vòng — vòng 1 sửa lỗi ngữ pháp lớn, vòng 2 tập trung vào những lỗi còn sót lại sau vòng 1, vòng 3 chỉ còn sửa những chi tiết cực nhỏ còn lại. Mỗi vòng "chuyên trị" đúng phần lỗi mà các vòng trước bỏ sót.
- Vì mỗi cây mới cố tình "vá" đúng những chỗ còn sai, boosting có xu hướng đạt độ chính xác cao hơn bagging trên cùng dữ liệu — nhưng đồng thời, nếu chạy quá nhiều vòng (quá nhiều cây), nó sẽ bắt đầu "vá" cả nhiễu ngẫu nhiên trong dữ liệu huấn luyện, dẫn tới quá khớp. Đây là lý do boosting thường cần tinh chỉnh cẩn thận số vòng lặp (`n_estimators`) hoặc dùng early stopping.

> XGBoost có trong máy thi, nhưng có thể không có trong máy bạn
>
> Bảng thư viện chính thức của kỳ thi có xgboost và catboost. Máy tôi dùng để đo cả tập tài liệu này thì
> không có, và tôi không được phép cài thêm vì chính quy chế thi cấm pip install, nên tập luyện trong
> điều kiện ấy mới có ý nghĩa.
>
> Thay thế là HistGradientBoostingClassifier của scikit-learn: cùng họ gradient boosting trên
> histogram, cùng ý tưởng, khác cách cài đặt. Mọi con số boosting dưới đây là của nó. Khi vào phòng thi
> có xgboost thật, số sẽ khác một chút, nhưng câu kết luận thì không.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là một lưu ý thực dụng cực kỳ quan trọng cho thí sinh: **môi trường luyện tập phải mô phỏng đúng môi trường thi** — bao gồm cả những hạn chế (không được `pip install` thêm thư viện). Luyện với thư viện không có sẵn trong phòng thi sẽ tạo ra ảo giác năng lực sai lệch.
- **`HistGradientBoostingClassifier`** là cài đặt gradient boosting "cây trên histogram" có sẵn trong scikit-learn (lấy cảm hứng từ LightGBM): thay vì tìm ngưỡng chia tối ưu trên mọi giá trị liên tục của một cột (tốn kém), nó chia giá trị của mỗi cột thành các "bin" rời rạc trước (histogram), rồi chỉ xét ngưỡng chia tại ranh giới giữa các bin — nhanh hơn nhiều, đặc biệt trên dữ liệu lớn.
- Việc XGBoost/CatBoost và HistGradientBoosting **cùng họ thuật toán** nhưng khác cách cài đặt chi tiết (regularization, cách xử lý missing values, thứ tự tính toán dấu chấm động...) khiến điểm số tuyệt đối có thể chênh nhau một chút, nhưng các **kết luận định tính** (boosting > cây đơn, boosting chậm hơn cây đơn, v.v.) vẫn giữ nguyên — đây là bài học về việc phân biệt "con số chính xác" và "xu hướng/quy luật", chỉ có xu hướng/quy luật mới đáng tin cậy để mang vào phòng thi với công cụ khác.

---

### 2.6 Độ quan trọng đặc trưng, và vì sao nó hay bị đọc sai

> feature_importances_ của rừng cộng dồn độ giảm tạp chất mà mỗi cột mang lại. Có một cách khác: xáo
> trộn ngẫu nhiên một cột trên tập kiểm định rồi xem điểm tụt bao nhiêu. Cách sau đắt hơn nhiều nhưng trả lời
> đúng câu ta muốn hỏi.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Có hai cách phổ biến để đo "cột nào quan trọng":
  1. **Impurity-based importance** (`feature_importances_` mặc định của scikit-learn): với mỗi cột, cộng dồn tổng độ giảm Gini/entropy (có trọng số theo số mẫu) tại mọi nút trong rừng mà cột đó được dùng để chia. Cách này **rất rẻ** (tính luôn trong quá trình huấn luyện, không cần tính thêm) nhưng như sẽ thấy, có thể gây hiểu lầm.
  2. **Permutation importance**: sau khi mô hình đã huấn luyện xong, lấy tập kiểm định, **xáo trộn ngẫu nhiên (shuffle)** giá trị của một cột duy nhất (phá vỡ mối liên hệ giữa cột đó và nhãn, nhưng giữ nguyên phân phối của cột), rồi đo điểm số tụt bao nhiêu so với ban đầu. Nếu một cột thực sự quan trọng, việc xáo trộn nó sẽ làm điểm giảm mạnh; nếu cột không quan trọng (hoặc mô hình không thực sự dựa vào nó để dự đoán đúng), điểm gần như không đổi (thậm chí có thể tăng nhẹ do nhiễu ngẫu nhiên).
- Câu "cách sau đắt hơn nhiều nhưng trả lời đúng câu ta muốn hỏi" rất quan trọng: impurity trả lời câu hỏi "mô hình đã **dùng** cột này để chia bao nhiêu, và mỗi lần chia giảm tạp chất bao nhiêu trên tập **huấn luyện**?" — đó là câu hỏi về **hành vi nội bộ của mô hình**. Permutation trả lời câu hỏi khác hẳn: "nếu bỏ thông tin của cột này đi, mô hình có còn dự đoán đúng trên dữ liệu **mới** không?" — đó là câu hỏi về **giá trị thực sự** của cột đối với khả năng tổng quát hoá.

> | Cột | Impurity | Hoán vị | Số giá trị |
> |---|---|---|---|
> | so_tu | 0,0273 | −0,0048 | 7 |
> | so_ky_tu | 0,1743 | −0,0171 | 69 |
> | do_dai_tu_tb | 0,1857 | −0,0089 | 117 |
> | tu_dai_nhat | 0,2389 | 0,0051 | 14 |
> | tu_ngan_nhat | 0,1184 | 0,0153 | 8 |
> | so_tu_co_gach | 0,0972 | 0,0106 | 4 |
> | so_tu_khac_nhau | 0,0296 | 0,0116 | 7 |
> | so_dau_gach | 0,1286 | 0,0136 | 5 |
>
> Hai trong ba cột đứng đầu cột Impurity có hoán vị âm
>
> so_ky_tu và do_dai_tu_tb chiếm 0,36 tổng độ quan trọng theo impurity, mà xáo trộn chúng lại làm
> điểm kiểm định tăng lên. Mô hình dùng chúng nhiều, và dùng sai.
>
> Lý do đã được biết từ lâu: impurity thiên vị cột có nhiều giá trị khác nhau. Cột nào chia được thành
> nhiều ngưỡng thì có nhiều cơ hội giảm tạp chất một cách tình cờ. Cột do_dai_tu_tb có 117 giá trị khác
> nhau, còn so_dau_gach chỉ có 5.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là bảng số liệu **quan trọng bậc nhất** của cả bài, minh chứng cho một cái bẫy kinh điển trong ML mà rất nhiều người thực hành (kể cả người có kinh nghiệm) mắc phải: **tin tưởng mù quáng vào `feature_importances_` mặc định**.
- Nhìn vào cột Impurity, ba cột đứng đầu là `tu_dai_nhat` (0,2389), `do_dai_tu_tb` (0,1857), `so_ky_tu` (0,1743). Nhưng khi nhìn cột Hoán vị (permutation), `do_dai_tu_tb` có giá trị **âm** (−0,0089) và `so_ky_tu` cũng **âm** (−0,0171)! Nghĩa là nếu ta xáo trộn ngẫu nhiên hai cột này, điểm mô hình trên tập kiểm định **tăng lên** — tức là mô hình "dựa dẫm" vào hai cột này theo cách khiến nó dự đoán **tệ hơn**, không phải tốt hơn, trên dữ liệu mới!
- Giải thích cơ chế thiên vị (bias) của impurity importance: một cột có **cardinality cao** (nhiều giá trị khác nhau, ví dụ `do_dai_tu_tb` có 117 giá trị) có nhiều "cơ hội" hơn để tìm được một ngưỡng chia tình cờ giảm được tạp chất trên tập **huấn luyện cụ thể** — kể cả khi mối liên hệ đó không tồn tại thật ngoài mẫu ngẫu nhiên đó (giống hiện tượng "multiple comparison" trong thống kê: càng thử nhiều ngưỡng, càng dễ tìm được một ngưỡng "trông có vẻ tốt" chỉ vì may rủi). Ngược lại, cột cardinality thấp như `so_dau_gach` (chỉ 5 giá trị) có ít lựa chọn ngưỡng hơn, nên nếu nó vẫn cho impurity giảm đáng kể, khả năng cao đó là tín hiệu **thật** — và đúng vậy, hoán vị của `so_dau_gach` là dương (0,0136), phù hợp với việc ta đã biết nó liên quan trực tiếp tới ngữ pháp (hậu tố thì) ở mục 2.2.

> Nhưng đừng nống câu chuyện lên quá số liệu: cột đứng đầu impurity là tu_dai_nhat, và hoán vị của
> nó dương. Xu hướng thiên vị là có thật và nhìn thấy được ở hai cột dưới nó, chứ bảng này không phải
> một quy luật xếp hạng.
>
> Quy tắc dùng được: impurity nói mô hình đã dùng cột nào; hoán vị nói bỏ cột ấy đi thì mất gì. Chỉ câu
> thứ hai mới trả lời được câu hỏi "có nên giữ cột này không".

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây lại là một minh chứng nữa cho tinh thần "thực chứng, không giáo điều" của cả tài liệu: dù đã chỉ ra cơ chế thiên vị cardinality là có thật, tác giả **không** để người học rút ra kết luận cường điệu kiểu "impurity luôn sai, cardinality cao luôn overrated". Thực tế, cột đứng đầu bảng impurity (`tu_dai_nhat`, chỉ 14 giá trị) vẫn có hoán vị dương (0,0051) — tức là nó thực sự quan trọng, không bị thiên vị. Bài học: **thiên vị cardinality là một xu hướng thống kê, không phải một quy luật tuyệt đối áp dụng cho mọi cột**.
- Câu kết "impurity nói mô hình đã dùng cột nào; hoán vị nói bỏ cột ấy đi thì mất gì" là một cách diễn đạt súc tích, đáng nhớ, phân biệt rõ hai loại câu hỏi hoàn toàn khác nhau mà hai phương pháp trả lời. Trong thực hành, nếu mục tiêu là **chọn đặc trưng (feature selection)** để loại bớt cột thừa, permutation importance là công cụ đáng tin cậy hơn nhiều; impurity importance chỉ nên dùng để hiểu "mô hình đang hoạt động như thế nào ở bên trong", không nên dùng để quyết định giữ/bỏ cột nào.

---

## 3. Bài tập mẫu

> Đề. Dựng bảng so sánh năm mô hình trên cùng một bộ dữ liệu, kèm thời gian huấn luyện. Rồi làm lại đúng
> bảng ấy với một cách biểu diễn khác, và so hai bảng.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Bài tập mẫu này gộp lại toàn bộ kiến thức của buổi: so sánh 5 thuật toán (KNN, cây, rừng, boosting, hồi quy logistic) trên hai cách biểu diễn dữ liệu khác nhau (8 đặc trưng tay vs. 2143 đặc trưng TF-IDF), nhằm minh hoạ luận điểm trung tâm: **cách biểu diễn dữ liệu thường quan trọng hơn việc chọn thuật toán**.

> ```python
> import time
> from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
> from sklearn.linear_model import LogisticRegression
> from sklearn.metrics import f1_score
> from sklearn.neighbors import KNeighborsClassifier
> from sklearn.tree import DecisionTreeClassifier
>
> def f1m(a, b):
>     return f1_score(a, b, average="macro", labels=[0, 1], zero_division=0)
>
> MO_HINH = [
>     ("KNN k=5", KNeighborsClassifier(n_neighbors=5)),
>     ("cay", DecisionTreeClassifier(random_state=0)),
>     ("rung 300", RandomForestClassifier(n_estimators=300, random_state=0, n_jobs=1)),
>     ("boosting", HistGradientBoostingClassifier(random_state=0)),
>     ("logistic", LogisticRegression(max_iter=2000, C=4.0, random_state=0)),
> ]
>
> for ten, m in MO_HINH:
>     t0 = time.perf_counter()
>     m.fit(Xh, yh)
>     print("%-10s hoc %.4f kiem %.4f %.1f giay"
>           % (ten, f1m(yh, m.predict(Xh)), f1m(yk, m.predict(Xk)),
>              time.perf_counter() - t0))
> ```

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đáng chú ý các siêu tham số cụ thể được ghim cứng: `n_jobs=1` cho RandomForest (lý do sẽ được giải thích ngay sau — vấn đề tái lập kết quả), `max_iter=2000, C=4.0` cho Logistic Regression (C là nghịch đảo cường độ regularization — C càng lớn thì regularization càng yếu, mô hình càng tự do khớp dữ liệu), và `zero_division=0` trong hàm F1 (tránh lỗi chia cho 0 khi một lớp không được dự đoán bao giờ).
- `time.perf_counter()` là cách đo thời gian chính xác cao trong Python (ưu tiên hơn `time.time()` cho việc benchmark, vì không bị ảnh hưởng bởi đồng hồ hệ thống bị điều chỉnh).

> Bảng A, tám đặc trưng tay.
>
> | Mô hình | Tập đã học | Kiểm định | Giây |
> |---|---|---|---|
> | KNN k = 5, không chuẩn hoá | 0,7139 | 0,5875 | 0,0 |
> | KNN k = 5, có chuẩn hoá | 0,7212 | 0,5670 | 0,0 |
> | cây, không giới hạn | 0,8200 | 0,5755 | 0,1 |
> | cây, độ sâu 5 | 0,6137 | 0,5827 | 0,0 |
> | rừng 300 cây | 0,8177 | 0,5873 | 0,6 |
> | boosting | 0,7116 | 0,6029 | 2,6 |
> | hồi quy logistic | 0,6088 | 0,6028 | 0,0 |
>
> Bảng B, TF-IDF ký tự 2143 đặc trưng (chính là cách biểu diễn của buổi 05).
>
> | Mô hình | Tập đã học | Kiểm định | Giây |
> |---|---|---|---|
> | KNN k = 5 | 0,7161 | 0,5935 | 0,0 |
> | cây quyết định | 0,9895 | 0,6999 | 4,1 |
> | rừng 300 cây | 0,9895 | 0,7587 | 10,0 |
> | boosting | 0,9416 | 0,7961 | 29,2 |
> | hồi quy logistic | 0,7255 | 0,6888 | 0,2 |
>
> Cột giây đo trên máy tôi và máy bạn sẽ ra số khác. Chỉ hai đầu của cột ấy là đáng nhớ: boosting chậm
> hơn hẳn cây đơn, còn hồi quy logistic và KNN xong dưới một giây. Mọi cách đều xong rất xa ngưỡng 20 phút
> của quy chế tái lập, nên thời gian không phải chỗ phải lo ở bài này.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- So sánh trực tiếp hai bảng cho thấy rõ hiện tượng: trên **Bảng A** (8 đặc trưng nghèo), tất cả 7 mô hình chỉ dao động trong khoảng 0,567–0,603 — gần như **không có mô hình nào vượt trội hẳn**, và một mô hình đơn giản như hồi quy logistic (0,6028) còn gần bằng boosting (0,6029), thuật toán phức tạp nhất trong danh sách! Đây là bằng chứng cho câu "đổi cách biểu diễn thường ăn hơn đổi mô hình".
- Trên **Bảng B** (2143 đặc trưng TF-IDF giàu thông tin hơn nhiều), khoảng cách giữa các mô hình **giãn ra rõ rệt**: từ 0,5935 (KNN) tới 0,7961 (boosting) — chênh lệch 0,2026! Khi biểu diễn dữ liệu đã đủ giàu thông tin, sự khác biệt về khả năng của thuật toán (khả năng nắm bắt tương tác phi tuyến, tương tác giữa các đặc trưng) mới thực sự phát huy tác dụng và tạo ra khác biệt điểm số lớn.
- Chú ý cột thời gian: boosting chậm hơn hẳn (29,2 giây so với 4,1 giây của cây đơn trên bảng B) — vì nó phải huấn luyện tuần tự nhiều cây, mỗi cây phụ thuộc kết quả của cây trước, không thể song song hoá như rừng.

> Rừng từng cho ra hai con số khác nhau trên cùng một máy
>
> Ngày 27/08/2026 cổng của buổi này trượt, và trượt theo kiểu khó chịu nhất: chạy riêng thì đạt, chạy
> trong bộ cổng thì trượt. Rừng 25 cây cho 0,5862 ở lần này và 0,5852 ở lần kia.
>
> Nguyên nhân đo được: rừng chạy với n_jobs=-1. Khi dự đoán, thư viện cộng xác suất của 25 cây lại
> theo thứ tự tuỳ số luồng đang rảnh, nên tổng dấu chấm động đổi ở chữ số cuối, và vài thể hoà ngả về bên
> khác. Hạn chế số luồng thì ra 0,5862; để máy dùng hết nhân thì ra 0,5852.
>
> Đã ghim n_jobs=1 ở mọi chỗ. Con số bây giờ giống nhau trên mọi máy.
>
> Cái giá phải trả, và nó có thật: rừng 300 cây chạy một luồng chậm hơn hẳn. Tính tái lập được mua
> bằng tốc độ, và ở kho này thì tái lập luôn được ưu tiên: một con số không lặp lại được thì nhanh cỡ nào
> cũng vô dụng.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là một **case study cực kỳ giá trị về kỹ năng debug thực chiến** mà rất ít tài liệu học máy đề cập: nguyên nhân sâu xa không nằm ở thuật toán hay dữ liệu, mà nằm ở **thứ tự cộng dấu chấm động (floating-point addition order)**. Phép cộng số thực trên máy tính **không có tính kết hợp hoàn hảo** ($ (a+b)+c $ có thể ≠ $ a+(b+c) $ ở chữ số cuối do sai số làm tròn nhị phân) — khi `n_jobs=-1` (dùng đa luồng), các luồng hoàn thành không theo thứ tự cố định, nên tổng xác suất bỏ phiếu của các cây được cộng theo thứ tự khác nhau giữa các lần chạy, dẫn tới sai khác cực nhỏ ở chữ số thập phân cuối — đủ để lật một vài trường hợp "hoà phiếu" (tie) sang bên khác, làm thay đổi nhãn dự đoán của một vài mẫu ranh giới, từ đó thay đổi điểm F1 cuối cùng.
- Bài học: **tính tái lập (reproducibility)** đôi khi đòi hỏi đánh đổi hiệu năng (ở đây là tốc độ) — và trong bối cảnh chấm thi tự động, một kết quả không lặp lại được là **vô dụng tuyệt đối** dù mô hình có "đúng" về mặt thuật toán, vì hệ thống chấm không thể xác định "đáp án đúng" là con số nào trong hai con số dao động.
- Đây cũng là lời nhắc thực dụng: khi build hệ thống production hoặc bộ test tự động, luôn cân nhắc ghim (`n_jobs=1`, `random_state`, phiên bản thư viện...) để đảm bảo tính xác định (determinism), đặc biệt trong môi trường yêu cầu kiểm tra kết quả chính xác tới nhiều chữ số thập phân.

> Và một thứ tôi đã thôi không chốt nữa. Thứ tự nhanh chậm giữa rừng và boosting đã lật ba lần:
>
> | Lần | Cấu hình | Đo được |
> |---|---|---|
> | 1 | rừng n_jobs=-1, máy bận | rừng 3,3 giây nhanh hơn cây 4,3 |
> | 2 | rừng n_jobs=1, máy bận | boosting 53,8 chậm hơn rừng 41,6 |
> | 3 | rừng n_jobs=1, máy rảnh | boosting 12,8 nhanh hơn rừng 19,0 |
>
> Ba lần, ba kết luận khác nhau, cùng một đoạn mã. Nên thứ tự ấy không phải một sự thật ổn định: nó
> đo tài nguyên máy chứ không đo thuật toán. Chốt nó lại là dựng một phép kiểm sẽ trượt trên máy người
> khác, và tôi đã trượt đúng ba lần trước khi chịu nhận điều đó.
>
> Cổng bây giờ chỉ chốt những quan hệ đã đúng ở cả ba lần: boosting chậm hơn hẳn cây đơn, còn logistic
> và KNN xong dưới một giây. Thời gian của rừng vẫn được in ra mỗi lần chạy, nhưng không ai chốt nó.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là bài học **khiêm tốn khoa học** hiếm gặp trong tài liệu giảng dạy: tác giả công khai thừa nhận đã "trượt đúng ba lần" trước khi rút ra bài học đúng. Điều này dạy một kỹ năng meta quan trọng hơn cả nội dung ML: **biết phân biệt cái gì là thuộc tính ổn định của thuật toán (đáng chốt thành quy luật) và cái gì chỉ là nhiễu do môi trường đo (không nên chốt)**.
- Nguyên nhân gốc rễ: thời gian chạy của Random Forest (đặc biệt khi `n_jobs` liên quan tới đa luồng) phụ thuộc mạnh vào **tải hệ thống tại thời điểm đo** (máy bận hay rảnh, bao nhiêu lõi CPU khả dụng thực tế) — một yếu tố hoàn toàn ngoài kiểm soát của thuật toán. Ngược lại, quan hệ "boosting chậm hơn cây đơn" là **ổn định qua cả ba lần đo** bất kể tải máy, vì nó phản ánh đúng bản chất thuật toán (boosting phải chạy tuần tự nhiều vòng, không thể song song hoá theo cây như rừng).
- Đây là ví dụ thực tế của khái niệm thống kê "confounding variable" (biến gây nhiễu) — tải máy là biến gây nhiễu che khuất mối quan hệ thật giữa thuật toán và tốc độ, và chỉ khi đo lặp lại nhiều lần trong nhiều điều kiện khác nhau mới tách được cái gì là "tín hiệu" (invariant across conditions) và cái gì là "nhiễu" (varies with confounders).

> Đây là con số đáng nhớ nhất của cả buổi
>
> Trên tám đặc trưng tay, năm mô hình xúm lại trong dải 0,5670 tới 0,6029. Chênh lệch giữa mô hình tốt
> nhất và tệ nhất là 0,0358, tức chỉ gấp đôi dải nhiễu.
>
> Đổi cách biểu diễn, cùng những mô hình ấy, boosting lên 0,7961. Bước nhảy là 0,1932, tức hơn năm
> lần khoảng cách giữa mọi mô hình trong bảng A.
>
> Và đây là con số tốt nhất mà cả khoá học đạt được cho tới lúc này: buổi 05 dừng ở 0,6888 với hồi quy
> logistic trên đúng 2143 đặc trưng ấy. Cùng dữ liệu, cùng đặc trưng, chỉ đổi mô hình, được thêm 0,1072.
>
> Hai kết luận không mâu thuẫn nhau: đổi cách biểu diễn thường ăn hơn đổi mô hình, và khi cách biểu
> diễn đã đủ giàu thì đổi mô hình mới bắt đầu có tác dụng. Ở bảng A không mô hình nào cứu nổi tám con
> số nghèo nàn; ở bảng B thì khoảng cách giữa KNN và boosting là 0,2026.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây chính là **kết luận trung tâm quan trọng nhất của toàn bộ buổi học**, đáng được ghi nhớ dưới dạng một câu ngắn gọn: *"Biểu diễn dữ liệu quyết định trần giới hạn (ceiling) của hiệu năng; thuật toán quyết định bạn tiệm cận trần đó gần tới đâu."*
- Con số 0,1932 (bước nhảy khi đổi biểu diễn cho boosting) so với 0,0358 (chênh lệch lớn nhất khi chỉ đổi thuật toán trên biểu diễn nghèo) — tỉ lệ hơn 5 lần — là một minh chứng định lượng thuyết phục cho nguyên lý "garbage in, garbage out": không thuật toán tinh vi nào, dù hiện đại đến đâu, có thể "cứu" một biểu diễn dữ liệu thiếu thông tin.
- Đồng thời, câu chuyện không dừng ở "chỉ biểu diễn mới quan trọng" — khoảng cách 0,2026 giữa KNN và boosting **trên cùng biểu diễn giàu (Bảng B)** cho thấy khi dữ liệu đã đủ thông tin, việc chọn đúng thuật toán mới thực sự "unlock" được tiềm năng đó. Đây là lý do hai kết luận "không mâu thuẫn nhau" — chúng bổ sung cho nhau theo trình tự ưu tiên: **trước tiên đầu tư vào biểu diễn dữ liệu tốt, sau đó mới tối ưu lựa chọn/tinh chỉnh mô hình**.
- Với người luyện thi Olympic AI, đây là chiến lược phân bổ thời gian thực dụng: nếu điểm số thấp và thời gian có hạn, hãy tự hỏi "mình đang bị giới hạn bởi biểu diễn dữ liệu hay bởi thuật toán?" trước khi lao vào tinh chỉnh siêu tham số.

> Cây và rừng cùng học thuộc 0,9895, nhưng khác nhau 0,0588 khi kiểm định
>
> Hai dòng giữa bảng B đáng nhìn kỹ. Cây đơn và rừng 300 cây cùng đạt 0,9895 trên tập đã học, con số
> ấy không phân biệt được chúng chút nào. Trên tập kiểm định thì cây được 0,6999 còn rừng được 0,7587.
>
> Nếu bạn chọn mô hình bằng điểm huấn luyện, bạn sẽ tung đồng xu giữa hai mô hình hơn kém nhau
> 0,0588. Buổi 07 đã nói điều này bằng lời; đây là nó bằng số.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là minh chứng số học **không thể chối cãi** cho nguyên tắc cơ bản nhất (nhưng cũng hay bị vi phạm nhất) trong học máy: **không bao giờ chọn mô hình dựa trên điểm số tập huấn luyện**. Cây đơn và rừng 300 cây đạt điểm huấn luyện **giống hệt nhau đến 4 chữ số thập phân** (0,9895) — nếu chỉ nhìn con số này, ta hoàn toàn không có cơ sở để phân biệt chúng, và có thể chọn nhầm cây đơn (đơn giản hơn, tưởng "vừa đủ tốt") mà bỏ lỡ khoảng cách 0,0588 lợi thế thực sự của rừng khi áp dụng lên dữ liệu mới.
- Vì sao hai mô hình có điểm huấn luyện giống hệt nhau nhưng khả năng tổng quát hoá khác biệt lớn? Vì điểm huấn luyện chỉ đo khả năng **ghi nhớ** dữ liệu đã thấy — cả cây đơn không giới hạn độ sâu lẫn rừng đều đủ "mạnh" để gần như ghi nhớ hoàn hảo 4800 dòng huấn luyện. Nhưng cách chúng **tổng quát hoá** ra ngoài dữ liệu đã thấy lại rất khác nhau: cây đơn dễ bị nhiễu (variance cao vì phụ thuộc hoàn toàn vào một cấu trúc phân chia duy nhất), trong khi rừng lấy trung bình 300 cây độc lập tương đối, triệt tiêu bớt phần "ghi nhớ nhiễu" riêng của từng cây — đúng như cơ chế đã giải thích ở mục 2.4.

---

## 4. Bài tập tự làm

> **Bài tập 1.** Dựng lại cả hai bảng
>
> Bảng A bảy dòng, bảng B năm dòng, cột kiểm định khớp tới chữ số thập phân thứ tư.
>
> Cổng kiểm
>
> Khớp cả hai bảng. Cột giây thì không cần khớp, nhưng thứ tự nhanh chậm phải giữ nguyên: boosting
> chậm hơn hẳn cây đơn, hồi quy logistic và KNN nhanh nhất.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Bài tập thực hành chuẩn: viết lại đúng đoạn code ở mục 3, tự tay chạy và đối chiếu số liệu tới 4 chữ số thập phân. Đây rèn kỹ năng **tái lập kết quả nghiên cứu (reproducibility)** — một kỹ năng bị đánh giá thấp nhưng cực kỳ quan trọng: nếu bạn không thể tái lập đúng bảng số của chính mình (hoặc của người khác), bạn không thể tin tưởng bất kỳ kết luận nào rút ra từ nó.
- Gợi ý thực hành: nhớ ghim `random_state=0` ở mọi nơi có tham số ngẫu nhiên (train_test_split, DecisionTreeClassifier, RandomForestClassifier, LogisticRegression), và dùng `n_jobs=1` cho RandomForest như bài học ở mục 3 đã chỉ ra.

> **Bài tập 2.** Tính tay một phép chia
>
> Không dùng máy: một nút có 4800 dòng, trong đó 2564 dòng nhãn 1. Chia thành nhánh trái 421 dòng
> toàn nhãn 0 và nhánh phải 4379 dòng.
>
> 1. Tính Gini của nút gốc.
> 2. Tính Gini của nhánh phải.
> 3. Tính độ giảm Gini có trọng số.
> 4. Làm lại cả ba câu với entropy.
>
> Cổng kiểm
>
> Đáp số: 0,497665, 0,485372, 0,054864; và với entropy là 0,996629, 0,978792, 0,103685. Sai số cho
> phép là chữ số thứ sáu sau dấu phẩy. Dạng câu hỏi này đã xuất hiện trong đề sơ loại, và ở đó bạn không
> có máy tính.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là bài tập **tính tay không máy tính** — mô phỏng chính xác điều kiện thi sơ loại thực tế được nhắc tới ở phần "cổng kiểm". Cách làm gợi ý:
  1. Tính $p_1 = 2564/4800$, rồi $Gini_{gốc} = 1 - p_1^2 - (1-p_1)^2$.
  2. Nhánh phải có 4379 dòng, trong đó nhãn 1 vẫn là 2564 (vì toàn bộ 2564 dòng nhãn 1 đều nằm ở nhánh phải — nhánh trái toàn nhãn 0). Tính $p_1' = 2564/4379$, rồi $Gini_{phải} = 1 - p_1'^2 - (1-p_1')^2$.
  3. Trọng số hoá: $\Delta Gini = Gini_{gốc} - \frac{421}{4800}\cdot 0 - \frac{4379}{4800}\cdot Gini_{phải}$.
  4. Tương tự với entropy: $H = -p\log_2 p - (1-p)\log_2(1-p)$, chú ý $\log_2 x = \ln x / \ln 2$ nếu máy tính tay chỉ có hàm ln.
- Mẹo tính tay nhanh: vì nhánh trái có Gini và Entropy đều bằng 0 (thuần tuyệt đối), công thức trọng số hoá chỉ còn một số hạng — giúp tiết kiệm thời gian đáng kể trong phòng thi có giới hạn thời gian nghiêm ngặt.

> **Bài tập 3.** Đường cong độ sâu, nhưng có xác thực chéo
>
> Bảng độ sâu ở mục 2.3 dùng một lần chia, và ta đã biết một lần chia dao động 0,0177. Làm lại nó bằng
> xác thực chéo 5 phần của buổi 07.
>
> Cổng kiểm
>
> Trả lời bằng số: sau khi có thanh sai số, còn bao nhiêu trong tám dòng thực sự phân biệt được với nhau?
> Và độ sâu 2 có còn thắng độ sâu 8 không?

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- **Xác thực chéo 5 phần (5-fold cross-validation)**: chia dữ liệu thành 5 phần bằng nhau, lần lượt dùng 4 phần để huấn luyện và 1 phần còn lại để kiểm định, lặp lại 5 lần sao cho mỗi phần đều được dùng làm tập kiểm định đúng một lần, rồi lấy trung bình (và độ lệch chuẩn) của 5 điểm số. Kỹ thuật này cho ước lượng **đáng tin cậy hơn nhiều** so với một lần chia 80/20 duy nhất, vì nó giảm phụ thuộc vào việc "may hay rủi" của một cách chia cụ thể.
- Bài tập yêu cầu tính "thanh sai số" (error bar, thường là độ lệch chuẩn hoặc khoảng tin cậy của 5 điểm số CV) cho mỗi độ sâu, sau đó kiểm tra xem khoảng dao động (được suy ra từ thanh sai số) của các độ sâu khác nhau có **chồng lấn (overlap)** hay không. Nếu hai độ sâu có khoảng tin cậy chồng lấn nhau, ta không thể tự tin khẳng định độ sâu nào tốt hơn — về bản chất, đây là một dạng đơn giản hoá của kiểm định giả thuyết thống kê (statistical hypothesis testing) áp dụng vào so sánh mô hình.
- Đây là bài tập trực tiếp nối tiếp bài học ở mục 2.3 ("đừng bịa lý do cho đường cong không đơn điệu") — bằng cách tự thực hiện CV, người học sẽ tự mình cảm nhận được có bao nhiêu trong "8 dòng" bảng độ sâu thực sự phân biệt được với độ tin cậy thống kê, thay vì chỉ tin vào lời khẳng định của giảng viên.

> **Bài tập 4.** Hoán vị nói ngược lại impurity
>
> Dựng lại bảng độ quan trọng. Rồi bỏ hẳn hai cột có hoán vị âm là so_ky_tu và do_dai_tu_tb, huấn
> luyện lại rừng, và ghi lại điểm kiểm định.
>
> Cổng kiểm
>
> Nói rõ điểm lên hay xuống, và bao nhiêu. Nếu độ lệch nhỏ hơn 0,0177 thì kết luận đúng là "không phân
> biệt được", chứ không phải "bỏ hai cột ấy có lợi".

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Bài tập này là **thử nghiệm trực tiếp giả thuyết** được nêu ra ở mục 2.6: nếu `so_ky_tu` và `do_dai_tu_tb` thực sự "gây hại" (permutation âm), thì loại bỏ chúng hoàn toàn khỏi tập đặc trưng và huấn luyện lại có thể cải thiện điểm kiểm định.
- Lưu ý cách đặt "cổng kiểm" một lần nữa nhắc lại kỷ luật thống kê nhất quán xuyên suốt tài liệu: dù kết quả có lên (như kỳ vọng từ permutation âm), người học vẫn phải so sánh mức tăng đó với dải nhiễu chuẩn (0,0177) trước khi dám kết luận "bỏ hai cột này có lợi" — tránh việc quá tự tin diễn giải một kết quả nằm trong biên độ nhiễu tự nhiên thành một "phát hiện" có ý nghĩa.
- Đây cũng là minh hoạ thực tế cho khái niệm **feature selection dựa trên permutation importance** — một quy trình chuẩn trong thực hành ML production: loại các cột có permutation importance âm hoặc gần 0, giữ lại các cột có đóng góp dương rõ rệt, giúp mô hình đơn giản hơn, nhanh hơn, và đôi khi tổng quát hoá tốt hơn.

> **Bài tập 5.** Hai mươi câu chọn mô hình
>
> Viết 20 câu hỏi trắc nghiệm cho chính bạn, mười câu dạng chọn mô hình và mười câu dạng tính tay. Mỗi
> câu bốn phương án, một đáp án đúng, kèm một dòng giải thích.
>
> Cổng kiểm
>
> Nhờ một bạn khác làm bộ câu hỏi của bạn. Câu nào bạn ấy làm sai vì đề mơ hồ chứ không vì thiếu kiến
> thức thì phải viết lại. Bộ câu hỏi này sẽ dùng lại ở buổi 22 khi luyện tốc độ làm phần sơ loại.

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Đây là kỹ thuật học tập **"học bằng cách dạy / học bằng cách ra đề" (learning by teaching / testing effect)** — một trong những phương pháp được chứng minh hiệu quả nhất trong khoa học về trí nhớ và học tập (metacognition). Việc tự soạn câu hỏi buộc người học phải hiểu đủ sâu để **nhìn ra được điểm gây nhầm lẫn** — điều mà chỉ đọc/nghe giảng thụ động không làm được.
- Cơ chế kiểm tra chéo với "một bạn khác" rất tinh tế: nó phân biệt được hai loại lỗi — lỗi do **người làm bài chưa vững kiến thức** (chấp nhận được, đó là mục đích luyện tập) và lỗi do **đề bài mơ hồ/thiếu rõ ràng** (đây là lỗi của người ra đề, cần sửa). Đây chính là quy trình chuẩn hoá đề thi (item validation) mà các tổ chức khảo thí chuyên nghiệp vẫn áp dụng.
- Việc "bộ câu hỏi này sẽ dùng lại ở buổi 22" cho thấy đây không phải bài tập một lần rồi bỏ — nó là một khoản đầu tư tích luỹ dần qua các buổi học, xây dựng thành một ngân hàng câu hỏi cá nhân hoá phục vụ ôn luyện tốc độ trước kỳ thi thật.

---

## Chuẩn bị cho buổi sau

> Buổi 09 làm SVM và lề, trong đó có phần tính tay dấu của w · x + b đúng như dạng câu hỏi cuối đề sơ loại
> 2025. Mang theo câu hỏi: vì sao lề rộng lại tổng quát tốt hơn, trong khi cả hai đường thẳng đều chia đúng
> toàn bộ dữ liệu huấn luyện?

🧠 **Phân tích chi tiết & Bản chất (Intuition):**
- Buổi tiếp theo chuyển sang **Support Vector Machine (SVM)**, một họ mô hình hoàn toàn khác về triết lý: thay vì tối ưu độ thuần khiết như cây, SVM tìm **siêu phẳng phân tách (hyperplane)** $w \cdot x + b = 0$ sao cho **lề (margin)** — khoảng cách từ siêu phẳng tới điểm gần nhất của mỗi lớp — là lớn nhất có thể.
- Câu hỏi gợi mở "vì sao lề rộng lại tổng quát tốt hơn dù cả hai đường thẳng đều chia đúng toàn bộ dữ liệu huấn luyện" chính là bài toán y hệt tinh thần của buổi 08: hai mô hình có thể **cùng đạt điểm huấn luyện hoàn hảo (100% đúng)** nhưng khác nhau về khả năng tổng quát hoá — giống hệt câu chuyện "cây và rừng cùng học thuộc 0,9895 nhưng khác 0,0588 khi kiểm định" ở mục 3. Trực giác SVM: một đường phân chia "sát mép" dữ liệu (lề hẹp) rất nhạy cảm với những điểm dữ liệu mới nằm gần ranh giới — chỉ cần nhiễu nhỏ, điểm mới có thể rơi sang phía sai. Đường phân chia có lề rộng tạo ra "vùng đệm an toàn" lớn hơn, nên ít bị ảnh hưởng bởi nhiễu của dữ liệu mới — đây chính là sợi dây liên kết giữa hai buổi học, và sẽ được chứng minh chặt chẽ bằng lý thuyết margin/VC-dimension ở buổi 09.

---

*Tài liệu mở rộng dựa trên nguyên bản của TS. Đỗ Phúc Hảo — Luyện Olympic Trí tuệ nhân tạo, Buổi 08, 25/08/2026. Phần giải thích 🧠 do trợ lý bổ sung, không thay thế cho việc đọc kỹ và tự làm bài tập gốc.*
