# Buổi 07 — Quá khớp, Kiểm định chéo, Tinh chỉnh siêu tham số
### (Bản mở rộng — có ẩn dụ đời thường 🧠 và đào sâu kỹ thuật 🔬)

> **Quy ước đọc file này:** Đoạn trong khung trích dẫn (bắt đầu bằng `>`) là **nguyên văn 100%** bài giảng gốc của TS. Đỗ Phúc Hảo — không thêm, không bớt, không đổi một chữ, một số, một dòng code nào. Ngay sau mỗi đoạn gốc là hai lớp giải thích của tôi:
> - **🧠 Ẩn dụ đời thường** — quy khái niệm về thứ đã quen thuộc trong đời sống, để nắm bản chất trước khi đụng vào công thức.
> - **🔬 Đào sâu kỹ thuật** — công thức, cơ chế, và những chỗ bài gốc chỉ lướt qua tên gọi mà chưa giảng kỹ.
>
> Đọc xong một đoạn gốc là thấy ngay giải thích ngay bên dưới, không cần lật lên lật xuống.

---

## Mục lục

1. [Mục tiêu](#1-mục-tiêu)
2. Tóm tắt kiến thức
   - [2.1 Chưa khớp và quá khớp](#21-chưa-khớp-và-quá-khớp)
   - [2.2 Ba tập, không phải hai](#22-ba-tập-không-phải-hai)
   - [2.3 Xác thực chéo k phần](#23-xác-thực-chéo-k-phần)
   - [2.4 Tìm siêu tham số](#24-tìm-siêu-tham-số)
   - [2.5 Rò rỉ dữ liệu](#25-rò-rỉ-dữ-liệu)
   - [2.6 Luật riêng của kỳ thi này](#26-luật-riêng-của-kỳ-thi-này)
3. Hướng dẫn
   - [3.1 Bước 1: dựng bảng sức chứa](#31-bước-1-dựng-bảng-sức-chứa)
   - [3.2 Bước 2: xác thực chéo](#32-bước-2-xác-thực-chéo)
   - [3.3 Bước 3: đo độ ổn định của chính cách đo](#33-bước-3-đo-độ-ổn-định-của-chính-cách-đo)
4. [Bài tập mẫu](#4-bài-tập-mẫu)
5. [Bài tập tự làm](#5-bài-tập-tự-làm)
6. [Chuẩn bị cho buổi sau](#chuẩn-bị-cho-buổi-sau)
7. [Tổng kết nhanh (bonus)](#7-tổng-kết-nhanh-bonus)

---

## 1. Mục tiêu

> Tự dựng một tập kiểm định đáng tin, và trả lời được câu hỏi buổi 06 để lại: tôi có hai mươi lượt nộp, làm sao dùng chúng mà không biến tập công khai thành tập huấn luyện thứ hai?

**🧠 Ẩn dụ đời thường**

Tưởng tượng bạn được thi thử **20 lần** trước kỳ thi thật, nhưng đề thi thử lấy từ đúng một ngân hàng câu hỏi nhỏ (800 câu — "tập công khai"). Nếu lần nào làm xong bạn cũng lật đáp án, ghi nhớ câu nào sai, rồi sửa bài đúng y những câu đó — thì đến lần thi thử thứ 20, bạn không còn "biết làm bài" nữa, bạn chỉ đang **học thuộc đúng 800 câu ấy**. Hôm thi thật (tập riêng — hoàn toàn câu mới), bạn sẽ ngã ngửa.

Mục tiêu buổi này là dựng cho mình một "phòng thi thử tại nhà" — một tập kiểm định riêng, tự cắt từ dữ liệu huấn luyện, không dính gì tới 800 câu công khai — để 20 lượt nộp kia được dùng đúng vai trò của nó: **xác nhận**, không phải **dò bài**.

**🔬 Đào sâu kỹ thuật**

Đây thực chất là bài toán **ước lượng không thiên lệch (unbiased estimation)** trong điều kiện tài nguyên bị giới hạn nghiêm ngặt (20 lượt nộp / 5 tiếng, rồi 5 lượt / 1 tiếng cuối, không sửa). Toàn bộ buổi 07 xoay quanh một nguyên lý duy nhất: **mỗi lần bạn dùng một tập dữ liệu để ra quyết định, tập đó mất đi tính "chưa từng thấy" (unseen) — và điểm số đo trên nó từ đó về sau không còn là ước lượng trung thực của hiệu năng thật nữa.** Đây chính là nền cho toàn bộ mục 2.2 (ba tập), 2.4 (dò siêu tham số làm mòn tập kiểm định), và 2.6 (ngân sách lượt nộp).

---

## 2. Tóm tắt kiến thức

### 2.1 Chưa khớp và quá khớp

> Chưa khớp mô hình quá nghèo để nắm được quy luật. Điểm thấp ở cả tập huấn
> luyện lẫn tập kiểm định.
>
> Quá khớp mô hình học thuộc cả nhiễu. Điểm cao ở tập huấn luyện, thấp ở tập
> kiểm định.
>
> Đo thật, ba mô hình cùng loại nhưng khác sức chứa, trên cùng một lần chia:
>
> | Sức chứa | Số đặc trưng | Tập đã học | Kiểm định | Chênh |
> |---|---|---|---|---|
> | nhỏ C=0.1, (2,3), df=5 | 696 | 0,6749 | 0,6430 | 0,0319 |
> | vừa C=4, (2,5), df=2 | 2143 | 0,7255 | 0,6888 | 0,0366 |
> | lớn C=1000, (1,8), df=1 | 3834 | 0,7299 | 0,6833 | 0,0466 |
>
> Đọc bảng này theo cột, không theo dòng
>
> Cột tập đã học chỉ đi lên: cho mô hình nhiều sức chứa hơn thì nó học thuộc tốt hơn, luôn luôn. Cột kiểm
> định thì đi lên rồi đi xuống, và đỉnh nằm ở mô hình giữa. Cột chênh lớn dần đều.
>
> Mô hình lớn nhất có nhiều hơn mô hình vừa 1691 đặc trưng, học thuộc giỏi hơn, và kém hơn trên dữ liệu
> chưa thấy. Đó là quá khớp, nhìn bằng số.

**🧠 Ẩn dụ đời thường**

Nghĩ về **sức chứa** như kích cỡ một cái ly.

- Ly quá nhỏ (chưa khớp): đổ nước vào tràn ra ngoài ngay, chẳng chứa được gì — mô hình quá đơn giản, đến quy luật rõ ràng nhất trong dữ liệu cũng không nắm nổi. Học cũng dở, thi cũng dở.
- Ly vừa (điểm ngọt — sweet spot): chứa đủ nước cần dùng, không tràn không thiếu.
- Ly quá to (quá khớp): bạn đổ cả nước lẫn... cặn trà vào, ly nào cũng chứa vừa hết — mô hình "nhớ" luôn cả nhiễu (noise), cả những đặc điểm ngẫu nhiên chỉ xuất hiện trong 800 dòng huấn luyện chứ chẳng đại diện cho quy luật chung nào. Trên đề đã học thì trông như thiên tài, ra đề mới thì trật lất.

Một ẩn dụ khác quen hơn: học sinh "học tủ" — thuộc lòng y nguyên 3834 câu hỏi ôn tập, kể cả câu nào thầy đánh máy lỗi chính tả. Gặp đúng đề cũ thì làm như máy; gặp câu hỏi diễn đạt hơi khác đi (dữ liệu kiểm định) là lúng túng ngay, vì bạn ấy chưa từng hiểu **quy luật ẩn sau** những câu hỏi đó.

**🔬 Đào sâu kỹ thuật**

*Sức chứa (capacity) là gì, chính xác?* Trong ví dụ này, "sức chứa" của mô hình bị ba tham số cùng lúc siết hoặc nới:
- `C` trong `LogisticRegression`: nghịch đảo cường độ regularization (đã học ở buổi 05) — `C` càng lớn, mô hình càng được tự do đặt trọng số lớn, càng dễ khớp sát dữ liệu huấn luyện.
- `ngram_range` trong `TfidfVectorizer`: khoảng độ dài n-gram ký tự được trích — `(1,8)` (từ 1 đến 8 ký tự) sinh ra nhiều tổ hợp hơn hẳn `(2,3)`.
- `min_df`: số dòng tối thiểu một n-gram phải xuất hiện mới được giữ làm đặc trưng — `min_df=1` giữ lại *mọi* n-gram, kể cả loại chỉ xuất hiện đúng một lần (rất dễ là nhiễu); `min_df=5` chỉ giữ n-gram đủ phổ biến.

Ba tham số này cộng hưởng ra số cột đặc trưng (feature) thực tế: 696 → 2143 → 3834. Đây chính là "kích cỡ ly" nói ở trên, đo được bằng số.

*Vì sao cột "tập đã học" chỉ đi lên, không bao giờ đi xuống?* Về nguyên tắc tối ưu hoá: mô hình có nhiều tham số hơn có một không gian giả thuyết (hypothesis space) *bao trọn* không gian giả thuyết của mô hình ít tham số hơn — nói nôm na, "nó làm được mọi thứ mô hình nhỏ làm được, và làm thêm được nữa". Vì vậy trên đúng dữ liệu đã dùng để huấn luyện, mất mát (loss) tối ưu của mô hình lớn không thể tệ hơn mô hình nhỏ. Đây là lý do mang tính toán học chắc chắn, không phải quan sát ngẫu nhiên.

*Vì sao cột "kiểm định" hình chữ U ngược (lên rồi xuống)?* Đây là hệ quả trực tiếp của phân rã **bias–variance**, công thức kinh điển cho sai số kỳ vọng trên dữ liệu mới:

```
E[(y - f̂(x))²]  =  Bias(f̂(x))²  +  Var(f̂(x))  +  σ²(nhiễu không thể giảm)
```

- Mô hình nhỏ (sức chứa thấp): **Bias cao** — nó quá cứng nhắc, giả định sai về hình dạng quy luật thật, nên dù dữ liệu có thay đổi thế nào nó vẫn đoán trật theo một kiểu cố định. → điểm thấp cả hai tập.
- Mô hình lớn (sức chứa cao): **Variance cao** — nó quá nhạy, mỗi lần đổi một chút dữ liệu huấn luyện là nó đổi hẳn cách đoán, vì nó đang bám theo nhiễu ngẫu nhiên riêng của đúng 800 dòng đó chứ không phải quy luật chung. → học thuộc giỏi, nhưng đoán sai trên dữ liệu chưa thấy.
- Mô hình vừa: tổng `Bias² + Variance` nhỏ nhất → đỉnh của cột kiểm định nằm ở đây. Đó là lý do bảng ghi "đỉnh nằm ở mô hình giữa".

*Đọc con số 1691 đặc trưng:* 3834 − 2143 = 1691. Đây là phép trừ y hệt bài gốc dùng để nhấn mạnh: "cho thêm 1691 chiều tự do", mô hình lớn học thuộc giỏi hơn (0,7299 > 0,7255) nhưng **kém hơn** trên dữ liệu chưa thấy (0,6833 < 0,6888). Nếu chỉ nhìn cột "tập đã học" mà chọn mô hình, bạn sẽ chọn nhầm mô hình *lớn* — đây chính xác là cái bẫy mà cột "Chênh" (0,0319 → 0,0366 → 0,0466, tăng dần đều) được dựng lên để cảnh báo: **chênh lệch train − validation là tín hiệu đo quá khớp trực tiếp bằng số, không cần đoán.**

---

### 2.2 Ba tập, không phải hai

> huấn luyện mô hình nhìn thấy và học
>
> kiểm định bạn nhìn, để chọn mô hình, siêu tham số, ngưỡng
>
> kiểm tra chỉ đụng một lần, ở cuối
>
> Lý do phải có ba chứ không phải hai: mỗi lần bạn nhìn một tập để quyết định điều gì đó, tập ấy mất tư
> cách làm thước đo trung thực. Nhìn mười lần thì nó thành tập huấn luyện thứ hai, chỉ khác là bạn huấn luyện
> bằng tay.

**🧠 Ẩn dụ đời thường**

Ba tập này giống hệt ba giai đoạn của việc học một môn thi:

1. **Huấn luyện (training)** = làm bài tập trong sách, có đáp án ngay bên cạnh để đối chiếu, học công thức. Nhìn bao nhiêu lần cũng được, vì mục đích của giai đoạn này là *học*, không phải *đo*.
2. **Kiểm định (validation)** = làm đề thi thử mượn từ khoá trước. Bạn được xem điểm sau mỗi lần thi thử, và **được phép** dùng điểm đó để đổi chiến thuật ôn tập, đổi phương pháp học, tăng/giảm độ khó tự luyện. Nhưng vì bạn *nhìn* đề thi thử này để ra quyết định, bộ đề thi thử ấy dần dần cũng bị "học thuộc" theo cách gián tiếp — bạn chọn phương pháp nào *ăn điểm* trên đúng bộ đề thi thử đó.
3. **Kiểm tra (test)** = đề thi thật, y hệt điều kiện phòng thi — chỉ mở phong bì **một lần duy nhất**, không có cơ hội "thi thử" thêm rồi quay lại sửa chiến thuật.

Nếu bạn gộp bước 2 và 3 làm một — tức là vừa dùng đề thi thật để chỉnh chiến thuật, vừa lấy điểm đó báo cáo là "điểm thi thật" — thì con số đó không còn ý nghĩa gì, vì bạn đã "thi thật" tới hàng chục lần trước khi lần cuối cùng được ghi nhận.

**🔬 Đào sâu kỹ thuật**

Đây là hiện tượng thống kê gọi là **rò rỉ thông tin qua việc nhìn lặp lại (information leakage via repeated peeking)**, còn gọi là bài toán **so sánh đa trọng (multiple comparisons)** hay "khu vườn của những nhánh rẽ" (*garden of forking paths* — thuật ngữ của Gelman). Bản chất toán học:

- Một phép đo hiệu năng trên một tập dữ liệu **chỉ là ước lượng không thiên lệch (unbiased)** cho hiệu năng thật nếu quyết định của bạn (chọn mô hình nào, siêu tham số nào) **không phụ thuộc** vào chính tập dữ liệu đó.
- Ngay khi bạn *chọn phương án tốt nhất trong số nhiều phương án* dựa trên điểm đo trên một tập cố định, bạn đang thực hiện một phép **chọn lọc (selection)**. Ngay cả khi không có phương án nào thực sự tốt hơn phương án khác (tất cả chỉ khác nhau do nhiễu ngẫu nhiên), phương án "thắng" trong số đó vẫn sẽ có điểm đo cao hơn trung bình một cách hệ thống — đây gọi là **"lời nguyền của kẻ chiến thắng" (winner's curse)**.
- Vì vậy tập dùng để *chọn* (validation) sẽ luôn cho điểm **lạc quan hơn** hiệu năng thật, mức độ lạc quan tăng theo **số lần** bạn nhìn nó để ra quyết định. Bài gốc diễn đạt đúng ý này: "Nhìn mười lần thì nó thành tập huấn luyện thứ hai, chỉ khác là bạn huấn luyện bằng tay" — tức là quá trình chọn siêu tham số/ngưỡng bằng mắt cũng là một dạng "huấn luyện", chỉ là con người làm thay máy.
- Tập **test** phải được giữ *trinh nguyên* (chưa từng bị nhìn để ra bất kỳ quyết định nào) để phép đo cuối cùng trên nó còn giữ được tính chất thống kê "ước lượng không thiên lệch cho hiệu năng trên dữ liệu mới".

Đây chính là lý do mà trong bối cảnh thi VOAI2026 (mục 2.6), "tập công khai" đóng vai trò *rất giống* validation set — bạn được thấy điểm sau mỗi lượt nộp — còn "tập riêng" đóng đúng vai trò test set, chỉ mở ra một lần cuối, không sửa được.

---

### 2.3 Xác thực chéo k phần

> Chia dữ liệu thành k phần bằng nhau. Lần lượt lấy một phần làm kiểm định, k − 1 phần còn lại làm huấn
> luyện. Cuối cùng lấy trung bình k điểm.
>
> Đo trên bộ dữ liệu tác vụ 1, k = 5:
>
> | | Phần 1 | Phần 2 | Phần 3 | Phần 4 | Phần 5 |
> |---|---|---|---|---|---|
> | năm điểm | 0,6862 | 0,7055 | 0,6936 | 0,6840 | 0,7064 |
>
> trung bình 0,6951
>
> độ lệch chuẩn 0,0094
>
> Và đây là con số đáng nhớ nhất của cả buổi. Đổi seed bốn lần, xem khoảng dao động của kết luận:
>
> | Cách đo | Khoảng dao động qua 4 seed |
> |---|---|
> | một lần chia 80/20 | 0,0177 |
> | trung bình 5 phần | 0,0020 |
>
> Ổn định hơn chín lần, với giá là chạy năm lần
>
> Ở buổi 03, chỉ riêng việc đổi seed đã làm điểm nhảy 0,0177. Nghĩa là mọi "cải tiến" nhỏ hơn chừng ấy
> đều không phân biệt được với nhiễu. Xác thực chéo kéo khoảng ấy xuống 0,0020, tức là bạn bắt đầu
> thấy được những cải tiến nhỏ hơn gần mười lần.
>
> Trong sáu tiếng thi, năm lần huấn luyện là đắt. Hãy dùng xác thực chéo cho những quyết định quan
> trọng và một lần chia cho những thử nghiệm nhanh, nhưng phải biết là con số một lần chia có sai số
> ±0,01.

**🧠 Ẩn dụ đời thường**

Bạn nấu một nồi súp lớn và muốn biết nó mặn nhạt ra sao.

- **Một lần chia 80/20** giống như múc **đúng một muỗng** ở một góc nồi rồi nếm. Nếu vô tình múc trúng chỗ gần miếng thịt mặn hơn, bạn sẽ kết luận "nồi súp này mặn" — trong khi thực ra chỉ góc đó mặn thôi. Kết luận của bạn phụ thuộc hên xui vào *đúng vị trí* bạn múc.
- **Xác thực chéo 5 phần** giống như múc **5 muỗng ở 5 góc khác nhau** của nồi, nếm từng muỗng, rồi lấy vị trung bình. Dù có 1 muỗng lỡ mặn hơn (Phần 2 ra 0,7055, cao hơn hẳn), 4 muỗng còn lại sẽ kéo trung bình về gần đúng vị thật của cả nồi. Kết luận cuối cùng ít phụ thuộc vào may rủi của một lần múc.

Con số "0,0177 xuống còn 0,0020" giống như: nếm 1 muỗng thì hôm nay bạn bảo "mặn", mai đổi vị trí múc bạn bảo "vừa" — dao động lớn. Nếm 5 muỗng trộn đều thì hôm nay và mai bạn đều ra kết luận gần giống nhau — dao động nhỏ hẳn. Đó là lý do xác thực chéo được xem là **"cái cân đáng tin hơn"**.

**🔬 Đào sâu kỹ thuật**

*Cơ chế k-fold, chính xác từng bước:*
1. Trộn dữ liệu, chia thành `k` phần (folds) kích thước gần bằng nhau.
2. Lặp `k` vòng: ở vòng thứ `i`, dùng phần `i` làm tập kiểm định, `k-1` phần còn lại gộp làm tập huấn luyện, huấn luyện một mô hình mới hoàn toàn từ đầu, đo điểm trên phần `i`.
3. Sau `k` vòng, bạn có `k` điểm số độc lập một phần (không hoàn toàn độc lập vì các fold huấn luyện có chồng lấn dữ liệu với nhau). Lấy trung bình làm điểm đại diện, lấy độ lệch chuẩn làm thước đo độ "rung" giữa các fold.

*Phân biệt hai loại "dao động" — đây là chỗ dễ nhầm nhất trong cả bài:*
- **Độ lệch chuẩn giữa 5 fold trong một lần chạy CV (0,0094)**: đo việc dữ liệu *không đồng nhất* — có phần dữ liệu dễ đoán hơn phần khác. Đây là "phương sai nội tại của dữ liệu" nhìn qua các fold.
- **Khoảng dao động của chính con số trung bình CV qua 4 seed khác nhau (0,0020)**: đo việc *nếu chia lại toàn bộ dữ liệu thành 5 phần theo cách khác (đổi seed của `StratifiedKFold`), thì con số trung bình cuối cùng lệch bao nhiêu*. Đây mới là con số quyết định "tôi có nên tin sự khác biệt 0,005 giữa hai mô hình hay không".

Về mặt thống kê, nếu gọi phương sai của một phép đo trên một lần chia đơn là `Var(một lần)`, thì trung bình của `k` phép đo (xấp xỉ độc lập) có phương sai giảm gần theo hệ số `1/k`:

```
Var(trung bình k fold)  ≈  Var(một lần chia) / k_hiệu_dụng
```

(không đúng chính xác `1/5` vì các fold không độc lập tuyệt đối — chúng chia sẻ phần lớn dữ liệu huấn luyện với nhau — nhưng vẫn giảm đáng kể, thực nghiệm ở đây cho thấy giảm gần **9 lần** dao động, đúng như tiêu đề "Ổn định hơn chín lần, với giá là chạy năm lần"). Đây là lý do CV luôn được ưu tiên khi *so sánh* hai lựa chọn (hai mô hình, hai bộ siêu tham số) — sự khác biệt nhỏ hơn "độ rung của thước đo" thì không có ý nghĩa, dùng thước rung ít hơn giúp bạn phân biệt được cải tiến nhỏ hơn thật sự.

*Ý nghĩa thực chiến của "±0,01" cho một lần chia:* nếu hai mô hình chênh nhau dưới khoảng này khi chỉ đo bằng một lần `train_test_split`, bạn **không có cơ sở** để nói mô hình nào tốt hơn — chênh lệch đó có thể chỉ do vận may của đúng seed đang dùng. Đây là quy tắc thực dụng rất đáng nhớ khi làm bài thi giới hạn giờ.

*`StratifiedKFold` khác `KFold` chỗ nào (đã gặp ở buổi 05, nhắc lại ở đây vì ứng dụng trực tiếp):* `StratifiedKFold` đảm bảo mỗi trong 5 phần giữ đúng tỉ lệ giữa các lớp (class) như tỉ lệ tổng thể. Nếu dùng `KFold` thường và dữ liệu mất cân bằng lớp, có thể một fold ngẫu nhiên rơi vào toàn (hoặc gần như toàn) một lớp — điểm đo ở fold đó trở nên vô nghĩa hoặc cực đoan, kéo méo cả trung bình.

---

### 2.4 Tìm siêu tham số

> Lưới thử mọi tổ hợp. Đủ dùng khi có hai tới ba tham số.
>
> Ngẫu nhiên bốc ngẫu nhiên n tổ hợp. Thắng lưới khi nhiều tham số, vì
> phần lớn tham số không quan trọng và lưới phí thời gian dò
> chúng.
>
> Tìm càng nhiều thì tập kiểm định càng mòn
>
> Thử 500 tổ hợp rồi lấy cái tốt nhất trên tập kiểm định, thì con số tốt nhất ấy đã bị chọn lọc chứ không
> còn là ước lượng trung thực. Đây là quá khớp ở tầng trên: không phải mô hình quá khớp dữ liệu, mà là
> quy trình của bạn quá khớp tập kiểm định.

**🧠 Ẩn dụ đời thường**

Bạn đang tìm công thức pha một ly trà sữa ngon nhất, có 3 biến: lượng đường, lượng đá, lượng trà.

- **Grid search (tìm theo lưới)**: thử *mọi* tổ hợp — 3 mức đường × 3 mức đá × 3 mức trà = 27 ly, nếm hết. Với 3 biến thì còn kham nổi.
- **Random search (tìm ngẫu nhiên)**: nếu bây giờ có 10 biến (thêm loại trà, loại sữa, nhiệt độ, thời gian ủ...), thử hết mọi tổ hợp là bất khả thi (hàng triệu ly). Thay vào đó, bạn bốc ngẫu nhiên, ví dụ, 50 tổ hợp trong không gian đó mà nếm. Vì trong 10 biến ấy, thường chỉ 2–3 biến thực sự quyết định vị ngon (lượng đường, loại trà), còn lại gần như không ảnh hưởng — bốc ngẫu nhiên có xu hướng "vô tình" quét đủ các mức của những biến quan trọng, trong khi lưới đầy đủ sẽ phí rất nhiều lần thử vào việc dò các mức của những biến *không quan trọng*.

Còn "tập kiểm định càng mòn" giống hệt việc: bạn có 20 người bạn nếm thử ly trà sữa, và bạn pha 500 công thức khác nhau rồi để họ chấm điểm. Công thức được điểm cao nhất trong số 500 công thức đó — **rất có thể** không phải vì nó ngon nhất một cách khách quan, mà vì đúng lúc đó khẩu vị của 20 người bạn hôm đó tình cờ hợp với nó nhất. Chấm 500 lần trên đúng 20 người, đến lần thứ 500 thì bạn không còn đang "kiểm định trên người lạ" nữa — bạn đang "học thuộc khẩu vị của 20 người bạn" thông qua việc thử liên tục.

**🔬 Đào sâu kỹ thuật**

*Vì sao random search thường thắng grid search khi số siêu tham số lớn (kết quả kinh điển của Bergstra & Bengio, 2012):* trực giác cốt lõi là **không phải mọi trục siêu tham số đều quan trọng như nhau**. Nếu một mô hình có 10 siêu tham số nhưng chỉ 2 trong số đó thực sự ảnh hưởng đến điểm số, thì:
- Grid search với, ví dụ, 3 mức mỗi trục sẽ chỉ thử được 3 giá trị *khác nhau* cho mỗi trục quan trọng (vì lưới cố định các trục còn lại), lãng phí phần lớn ngân sách tính toán vào việc dò các trục vô dụng.
- Random search với cùng ngân sách N lần thử sẽ, về kỳ vọng, thử được **gần N giá trị khác nhau** trên mỗi trục quan trọng (vì mỗi lần bốc, tất cả các trục đều nhận giá trị mới) → bao phủ tốt hơn hẳn đúng những chiều thực sự quyết định.

*Công cụ sklearn tương ứng (bài gốc chỉ nêu khái niệm, đây là phần bổ sung để lấp khoảng trống thực hành):*

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import loguniform

# Grid search: liệt kê rõ từng lưới giá trị
luoi = {
    "logisticregression__C": [0.1, 1, 10, 100],
    "tfidfvectorizer__min_df": [1, 2, 5],
}
gs = GridSearchCV(mo_hinh(), luoi, cv=cv, scoring=cham, n_jobs=-1)
gs.fit(X, y)

# Random search: cho một PHÂN PHỐI để bốc ngẫu nhiên, không phải danh sách cố định
phan_phoi = {
    "logisticregression__C": loguniform(1e-2, 1e3),   # thang nhân, giống np.logspace đã học ở buổi 05
    "tfidfvectorizer__min_df": [1, 2, 3, 4, 5],
}
rs = RandomizedSearchCV(mo_hinh(), phan_phoi, n_iter=30, cv=cv, scoring=cham, random_state=0, n_jobs=-1)
rs.fit(X, y)
```

Lưu ý cách đặt tên tham số kiểu `buoc__ten_tham_so` (hai dấu gạch dưới) — đây là quy ước bắt buộc của sklearn khi tham số nằm trong một `Pipeline`, để biết tham số đó thuộc bước nào.

*"Quá khớp ở tầng trên" — vì sao đây là một dạng overfitting riêng biệt, khác với 2.1?* Ở mục 2.1, đối tượng bị quá khớp là **mô hình** (nó ghi nhớ dữ liệu). Ở đây, đối tượng bị quá khớp là **chính quy trình tìm kiếm của bạn** — bạn không có một mô hình duy nhất bị quá khớp, mà có một *phép chọn lọc trên hàng trăm mô hình* bị quá khớp vào đúng tập kiểm định dùng để chọn. Đây là hệ quả trực tiếp của nguyên lý đã nói ở mục 2.2 (nhìn một tập nhiều lần → tập đó mất tư cách thước đo trung thực), chỉ khác là ở đây "nhìn nhiều lần" xảy ra **tự động** bên trong vòng lặp tìm kiếm siêu tham số chứ không phải do người dò bằng tay. Cách khắc phục chuẩn: dùng **nested cross-validation** (một vòng CV ngoài để đánh giá, một vòng CV trong để chọn siêu tham số) khi cần con số hoàn toàn trung thực, hoặc đơn giản hơn — như luật ở mục 2.6 — luôn giữ lại một tập kiểm định *hoàn toàn tách biệt* khỏi vòng tìm kiếm để đánh giá lần cuối.

---

### 2.5 Rò rỉ dữ liệu

> Rò rỉ là khi thông tin từ tập kiểm tra lọt vào quá trình huấn luyện. Ví dụ kinh điển: huấn luyện bộ trích đặc
> trưng trên cả hai tập.
>
> Đo thật:
>
> | | Số đặc trưng | Điểm kiểm định |
> |---|---|---|
> | chỉ học trên tập huấn luyện | 2143 | 0,6888 |
> | học trên cả tập kiểm định | 2156 | 0,6930 |
>
> Đây là một ví dụ rò rỉ nhỏ, và tôi nói rõ là nhỏ
>
> Chênh 0,0042, còn nhỏ hơn nhiễu của một lần chia. Lý do nó nhỏ: bộ trích đặc trưng ở đây chỉ học danh
> sách từ vựng, và thêm 13 mẩu ký tự thì không giúp được bao nhiêu.
>
> Nhưng đúng cùng một lỗi ấy sẽ đắt hơn nhiều khi thứ học được mang nhiều thông tin hơn: chuẩn hoá
> bằng trung bình và độ lệch chuẩn tính trên cả hai tập, chọn đặc trưng theo tương quan với nhãn, hay mã
> hoá theo giá trị nhãn. Chỗ ấy rò rỉ có thể nâng điểm vài phần trăm, và bạn sẽ tin là mình giỏi cho tới lúc
> chấm trên tập riêng.
>
> Quy tắc: mọi thứ có chữ fit chỉ được gọi trên tập huấn luyện.

**🧠 Ẩn dụ đời thường**

Rò rỉ dữ liệu giống việc **đầu bếp nếm thử trước món ăn rồi mới quyết định công thức**, trong khi lẽ ra công thức phải được chốt trước khi biết khách sẽ ăn gì. Cụ thể hơn với ví dụ "nhỏ" trong bài: giống như bạn học từ vựng tiếng Anh chủ yếu từ sách giáo khoa (tập huấn luyện), nhưng lỡ liếc qua đề thi thử (tập kiểm định) và nhặt thêm đúng 13 từ lạ xuất hiện trong đó. Vì 13 từ chỉ là một phần rất nhỏ so với cả cuốn từ điển bạn đã học, việc "liếc" này gần như không giúp ích gì — đó là lý do chênh lệch chỉ 0,0042, nhỏ hơn cả độ rung tự nhiên của một lần đo.

Nhưng nếu thay vì chỉ "liếc thêm từ vựng", bạn **liếc thẳng vào đáp án** của đề thi thử (tương đương: chuẩn hoá dữ liệu dùng thống kê tính trên cả hai tập, chọn đặc trưng theo tương quan với chính nhãn, mã hoá theo giá trị nhãn) — thì đó không còn là "liếc nhẹ" nữa, mà là **nhìn thẳng lời giải** trước khi làm bài. Điểm số khi đó sẽ tăng vọt một cách giả tạo, và bạn sẽ tưởng nhầm là mình giỏi thật — cho đến khi gặp đề hoàn toàn mới (tập riêng) không có "đáp án" nào để liếc.

**🔬 Đào sâu kỹ thuật**

*Vì sao mức độ nguy hiểm của rò rỉ phụ thuộc vào "thứ học được mang bao nhiêu thông tin"?* Trong ví dụ ở bảng, `TfidfVectorizer` khi `fit` trên cả hai tập chỉ học thêm được **danh sách từ vựng (vocabulary)** — một tập hợp các n-gram ký tự tồn tại. Việc biết thêm "có tồn tại n-gram X" gần như không tiết lộ gì về **nhãn** của các dòng trong tập kiểm định — vì vậy rò rỉ này gần như vô hại (0,0042, nằm trong mức nhiễu tự nhiên).

Ngược lại, ba ví dụ bài nêu ra đều trực tiếp hoặc gián tiếp rò rỉ **thông tin về nhãn**:
- **Chuẩn hoá (StandardScaler) tính trên cả hai tập**: trung bình và độ lệch chuẩn bị "nhiễm" bởi phân phối của tập kiểm định — mô hình gián tiếp biết trước hình dạng phân phối dữ liệu nó sẽ bị kiểm tra.
- **Chọn đặc trưng theo tương quan với nhãn** tính trên cả hai tập: đây là rò rỉ **trực tiếp nhãn** — bạn đang dùng chính câu trả lời (nhãn của tập kiểm định) để quyết định đặc trưng nào được giữ lại. Đây chính là nội dung Bài tập 4 yêu cầu tự tạo ra để cảm nhận độ nghiêm trọng.
- **Mã hoá theo giá trị nhãn (target encoding)** tính trên cả hai tập: mỗi danh mục (category) được thay bằng một con số tính từ nhãn — nếu tính luôn trên tập kiểm định, mô hình học được xấp xỉ chính đáp án cần đoán.

*Quy tắc vàng, và vì sao `Pipeline` của sklearn giải quyết được nó gần như tự động:* quy tắc "mọi thứ có chữ `fit` chỉ được gọi trên tập huấn luyện" tương đương về mặt code với:

```python
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ĐÚNG: Pipeline tự động đảm bảo fit_transform chỉ chạy trên Xh,
# còn Xk chỉ được transform (không học lại gì thêm) — không cách nào rò rỉ vô ý.
m = make_pipeline(TfidfVectorizer(...), LogisticRegression(...))
m.fit(Xh, yh)          # fit_transform bên trong chỉ thấy Xh
diem = m.score(Xk, yk)  # bên trong tự gọi .transform(Xk), KHÔNG fit lại

# SAI (rò rỉ): fit trực tiếp vectorizer trên toàn bộ X trước khi chia
vec = TfidfVectorizer(...).fit(X)          # thấy cả Xk trong bước học từ vựng
Xh_v, Xk_v = vec.transform(Xh), vec.transform(Xk)
```

Đây là lý do trong thực hành thi đấu, luôn ưu tiên nhét *toàn bộ* các bước biến đổi có `fit` (vectorizer, scaler, feature selector, encoder...) vào bên trong một `Pipeline` rồi mới `.fit()` trên tập huấn luyện — thay vì tự tay gọi `fit` trên `X` đầy đủ trước khi chia. `Pipeline` không giúp bạn tránh rò rỉ theo kiểu "thông minh đặc biệt" — nó chỉ đơn giản ép bạn *luôn luôn* gọi đúng thứ tự `fit` → `transform`, đúng đối tượng dữ liệu, khó lỡ tay sai hơn khi làm thủ công dưới áp lực thời gian thi.

---

### 2.6 Luật riêng của kỳ thi này

> - Tập công khai chỉ có 800 dòng, và bạn có 20 lượt nộp trong 5 tiếng đầu.
> - Mỗi lượt nộp cho bạn một con số, và mỗi lần bạn dùng con số ấy để quyết định thì tập công khai lại mòn
> thêm một ít.
> - Tập riêng mở ở tiếng thứ sáu với 5 lượt, và không có cơ hội sửa.
>
> Quy tắc dùng lượt nộp
>
> Mọi quyết định nội bộ (chọn mô hình, siêu tham số, ngưỡng) làm trên tập kiểm định của riêng bạn,
> cắt từ dữ liệu huấn luyện. Lượt nộp chỉ dùng để xác nhận, không dùng để dò. Nếu điểm công khai và
> điểm kiểm định của bạn lệch nhau nhiều, đó là tin tức về dữ liệu, không phải lời mời tinh chỉnh.

**🧠 Ẩn dụ đời thường**

20 lượt nộp giống 20 lần được gọi điện "phao cứu trợ" trong một gameshow — quý giá, có hạn, và **không nên** dùng để dò từng câu một ("thử đáp án A xem đúng không, sai thì thử B..."). Cách chơi khôn ngoan là: tự mình suy luận, tính toán thật kỹ ở nhà (tập kiểm định riêng) trước, rồi chỉ gọi điện phao cứu trợ để **xác nhận lần cuối** trước khi chốt đáp án, hoặc trong tình huống thực sự bế tắc.

Còn câu "nếu điểm công khai và điểm kiểm định của bạn lệch nhau nhiều, đó là tin tức về dữ liệu, không phải lời mời tinh chỉnh" giống như: nếu bạn làm bài tập ở nhà toàn 9 điểm nhưng ra phòng thi thử điểm lại tụt xuống 6, phản ứng đúng **không phải** là vội vàng sửa lại từng câu theo đúng đáp án phòng thi thử (đó là quay lại lỗi ở mục 2.2 — biến phòng thi thử thành sách bài tập thứ hai). Phản ứng đúng là đặt câu hỏi: "hay là đề ở nhà và đề phòng thi thử ra theo hai kiểu khác nhau?" — tức là đi tìm nguyên nhân (lệch phân phối dữ liệu, leakage, bug) chứ không phải đi tìm cách vá điểm số bằng mọi giá.

**🔬 Đào sâu kỹ thuật**

Xét theo khung đã dựng ở mục 2.2 và 2.3, "tập công khai" trong luật thi này đóng đúng vai trò một **validation set bị giới hạn số lần truy vấn** — mỗi lượt nộp là một lần "nhìn" vào nó, và mỗi lần nhìn để *ra quyết định* (không phải chỉ để xác nhận) đều làm nó mòn đi theo đúng cơ chế winner's curse đã nói ở 2.2. Chiến lược tối ưu về mặt thống kê là:

1. **Dựng tập kiểm định nội bộ** đáng tin (dùng đúng kỹ thuật `StratifiedKFold` ở mục 2.3) cắt từ `training_public`, để mọi thử nghiệm nhanh (đổi mô hình, đổi siêu tham số, đổi ngưỡng) được lặp lại **không giới hạn số lần** mà không đốt lượt nộp thật.
2. Dùng CV (không phải một lần chia) cho các quyết định "đắt" — vì đã đo được ở 2.3 rằng một lần chia có nhiễu ±0,01, đủ để đánh lừa một quyết định quan trọng.
3. Chỉ nộp lên tập công khai khi cần **đối chiếu** — tức là kiểm tra xem điểm kiểm định nội bộ có khớp với điểm công khai không (nếu khớp: yên tâm là không có lệch phân phối hay leakage; nếu lệch nhiều: dấu hiệu có vấn đề về dữ liệu cần điều tra, ví dụ tập công khai có phân phối lớp khác, có nhiễu khác, hoặc pipeline có lỗi ẩn) — **không** dùng lượt nộp để "quét" hàng loạt phương án và chọn cái điểm công khai cao nhất, vì đó chính là hành vi mục 2.4 gọi là "quá khớp ở tầng trên", chỉ khác là đối tượng bị quá khớp bây giờ là chính leaderboard công khai.
4. Dành ngân sách lượt nộp một cách có kế hoạch trước (đây chính là nội dung Bài tập 5) thay vì phản ứng tuỳ hứng theo diễn biến — vì mỗi lượt là tài nguyên không tái tạo, giống hệt lý do phải cân nhắc "quyết định quan trọng dùng CV, thử nhanh dùng một lần chia" đã nói ở 2.3.

---

## 3. Hướng dẫn

### 3.1 Bước 1: dựng bảng sức chứa

> ```python
> from sklearn.feature_extraction.text import TfidfVectorizer
> from sklearn.linear_model import LogisticRegression
> from sklearn.metrics import f1_score
> from sklearn.model_selection import train_test_split
> from sklearn.pipeline import make_pipeline
>
> f1 = lambda a, b: f1_score(a, b, average="macro", labels=[0, 1], zero_division=0)
> Xh, Xk, yh, yk = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
>
> for ten, C, ng, mdf in (("nho", 0.1, (2, 3), 5),
>                          ("vua", 4.0, (2, 5), 2),
>                          ("lon", 1000.0, (1, 8), 1)):
>     m = make_pipeline(
>         TfidfVectorizer(analyzer="char_wb", ngram_range=ng, min_df=mdf),
>         LogisticRegression(max_iter=4000, C=C, random_state=0))
>     m.fit(Xh, yh)
>     a, b = f1(yh, m.predict(Xh)), f1(yk, m.predict(Xk))
>     so_dt = len(m.named_steps["tfidfvectorizer"].vocabulary_)
>     print("%-4s %5d dac trung  hoc %.4f  kiem %.4f  chenh %.4f"
>           % (ten, so_dt, a, b, a - b))
> ```

**🧠 Ẩn dụ đời thường**

Đoạn code này giống một thí nghiệm khoa học có kiểm soát: bạn giữ **nguyên** một bộ đề (`Xh, Xk, yh, yk` — chia một lần y hệt nhau cho cả ba lần thử, `random_state=0` cố định), rồi lần lượt cho ba "học sinh" có sức học khác nhau (`nho`, `vua`, `lon`) học và đi thi trên đúng bộ đề đó. Vì mọi thứ khác đều giữ nguyên, chênh lệch điểm số giữa ba học sinh chỉ có thể do một nguyên nhân duy nhất: sức chứa. Đây là cách làm thí nghiệm đúng — mỗi lần chỉ đổi một biến.

**🔬 Đào sâu kỹ thuật**

Đi qua từng dòng:

- `f1 = lambda a, b: f1_score(a, b, average="macro", labels=[0, 1], zero_division=0)`: đóng gói lại `f1_score` với các tham số cố định (macro-average trên đúng 2 nhãn 0 và 1, không lỗi khi một lớp không được đoán) thành một hàm ngắn gọi lại nhiều lần — kỹ thuật quen thuộc từ buổi 05.
- `train_test_split(..., stratify=y)`: chia một lần **duy nhất**, `stratify=y` đảm bảo tỉ lệ lớp trong `Xh` và `Xk` giống tỉ lệ lớp trong `X` — nếu không có `stratify`, một lần chia ngẫu nhiên có thể vô tình dồn phần lớn một lớp vào `Xk`, làm bảng sức chứa bị nhiễu bởi yếu tố chia dữ liệu chứ không phải yếu tố sức chứa.
- Vòng `for` lặp qua đúng 3 bộ ba `(C, ngram_range, min_df)` khớp với 3 dòng trong bảng ở mục 2.1.
- `analyzer="char_wb"`: trích đặc trưng theo n-gram **ký tự trong phạm vi từ** (character n-grams within word boundaries) — khác với trích theo từ (`analyzer="word"`). Kiểu này rất hợp cho các bài toán như nhận diện ngôn ngữ (ví dụ Bana đã nhắc ở các buổi trước) vì nó bắt được đặc trưng hình thái từ (tiền tố, hậu tố, cụm phụ âm đặc trưng) thay vì phụ thuộc vào việc tách từ đúng hay sai.
- `m.named_steps["tfidfvectorizer"].vocabulary_`: sau khi `fit`, mỗi bước trong `Pipeline` có tên tự động bằng chữ thường của tên lớp (`tfidfvectorizer`). `.vocabulary_` là từ điển ánh xạ mỗi n-gram sang chỉ số cột — `len(...)` chính là số đặc trưng hiển thị trong bảng (696 / 2143 / 3834).
- `a, b = f1(yh, m.predict(Xh)), f1(yk, m.predict(Xk))`: đo điểm trên **đúng** tập đã dùng để học (`Xh`) và tập chưa từng dùng để học (`Xk`) — hai cột "Tập đã học" và "Kiểm định" trong bảng 2.1. `a - b` chính là cột "Chênh".

Chạy chính xác đoạn code này (đúng `random_state=0` ở cả `train_test_split` và `LogisticRegression`) là cách để Bài tập 2 khớp bảng "tới chữ số thập phân thứ tư".

---

### 3.2 Bước 2: xác thực chéo

> ```python
> import numpy as np
> from sklearn.metrics import make_scorer
> from sklearn.model_selection import StratifiedKFold, cross_val_score
>
> cham = make_scorer(f1_score, average="macro", labels=[0, 1], zero_division=0)
> cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
> d = cross_val_score(mo_hinh(), X, y, cv=cv, scoring=cham)
> print("nam diem:", np.round(d, 4))
> print("trung binh %.4f, do lech chuan %.4f" % (d.mean(), d.std()))
> ```
>
> StratifiedKFold giữ tỉ lệ hai lớp trong mỗi phần. Không dùng nó thì một phần có thể lệch hẳn và điểm
> của phần ấy nói dối.

**🧠 Ẩn dụ đời thường**

`cross_val_score` giống việc bạn thuê **5 giám khảo độc lập**, mỗi người chấm bài trên một góc dữ liệu khác nhau, rồi bạn thu về 5 con điểm và tự lấy trung bình — thay vì tự mình đi hỏi ý kiến một giám khảo duy nhất rồi tin tưởng tuyệt đối vào đúng người đó.

**🔬 Đào sâu kỹ thuật**

- `make_scorer(f1_score, average="macro", labels=[0, 1], zero_division=0)`: gói hàm `f1_score` cùng các đối số cố định thành một đối tượng "scorer" mà các công cụ của sklearn (như `cross_val_score`, `GridSearchCV`) có thể gọi theo đúng chữ ký hàm chuẩn `scorer(estimator, X, y)` mà chúng cần — khác với việc tự gọi hàm `f1_score(y_true, y_pred)` trực tiếp như hàm `f1` ở bước 1. Đây là điểm dễ nhầm đã có trong "debugging patterns" trước đây: nhầm chuỗi định danh sẵn có của sklearn (như `"f1_macro"`) với hàm tự định nghĩa — ở đây dùng `make_scorer` để tự bọc hàm của mình cho đúng khuôn.
- `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)`: `n_splits=5` ứng với `k=5`; `shuffle=True` xáo trộn dữ liệu trước khi chia (nếu dữ liệu gốc có thứ tự — ví dụ xếp theo nhãn hoặc theo thời gian thu thập — không xáo trộn sẽ cho ra các fold cực kỳ lệch); `random_state=0` cố định lần xáo trộn đó để tái lập được kết quả — đúng nguyên tắc reproducibility (md5 checksum) đã nhấn mạnh trong các buổi trước.
- `cross_val_score(mo_hinh(), X, y, cv=cv, scoring=cham)`: hàm này tự động thực hiện **toàn bộ vòng lặp** 5 lần huấn luyện/kiểm định mô tả ở mục 2.3 — với mỗi fold, nó gọi `mo_hinh()` để tạo một pipeline **mới hoàn toàn** (không dùng lại mô hình đã huấn luyện ở fold trước), fit trên phần huấn luyện của fold, chấm trên phần kiểm định của fold. Việc gọi `mo_hinh()` (một hàm trả về pipeline mới) thay vì truyền thẳng một đối tượng đã tồn tại là bắt buộc — nếu không, `.fit()` ở fold sau sẽ ghi đè lên trọng số đã học ở fold trước một cách không kiểm soát rõ ràng.
- `d` là mảng 5 số — đúng dòng "năm điểm" trong bảng 2.3. `d.mean()` và `d.std()` cho ra hai số "trung bình" và "độ lệch chuẩn" tương ứng.
- Câu nhắc "StratifiedKFold giữ tỉ lệ hai lớp... Không dùng nó thì một phần có thể lệch hẳn và điểm của phần ấy nói dối" chính là hệ quả trực tiếp: nếu một fold ngẫu nhiên có tỉ lệ lớp rất khác tổng thể (ví dụ toàn lớp 0), thì macro-F1 đo trên fold đó có thể tụt xuống bất thường hoặc thậm chí không xác định rõ ràng (nhờ `zero_division=0` mới không văng lỗi) — kéo méo cả giá trị trung bình cuối cùng, khiến bạn hiểu sai về hiệu năng thật.

---

### 3.3 Bước 3: đo độ ổn định của chính cách đo

> ```python
> mot_lan, nhieu_lan = [], []
> for s in (0, 1, 2, 42):
>     Xh, Xk, yh, yk = train_test_split(X, y, test_size=0.2, random_state=s, stratify=y)
>     m = mo_hinh()
>     m.fit(Xh, yh)
>     mot_lan.append(f1(yk, m.predict(Xk)))
>
>     cvs = StratifiedKFold(n_splits=5, shuffle=True, random_state=s)
>     nhieu_lan.append(cross_val_score(mo_hinh(), X, y, cv=cvs, scoring=cham).mean())
>
> print("mot lan chia: dai %.4f" % (max(mot_lan) - min(mot_lan)))
> print("CV 5 phan   : dai %.4f" % (max(nhieu_lan) - min(nhieu_lan)))
> ```
>
> Đây là bước ít ai làm, và nó đáng làm nhất
>
> Bạn vừa đo chính cái thước của mình. Trước khi tin bất cứ cải tiến nào, bạn cần biết thước ấy rung tới
> đâu. Không có con số này thì mọi so sánh đều là cảm tính.

**🧠 Ẩn dụ đời thường**

Trước khi dùng một cái cân để cân vàng, thợ kim hoàn giỏi sẽ **tự cân đi cân lại một vật đã biết chính xác trọng lượng** vài lần để xem cái cân của mình có "rung" (sai số) bao nhiêu. Nếu cân rung ±5 gram, thì việc so hai miếng vàng chênh nhau 1 gram là vô nghĩa — sai số của cân còn lớn hơn cả sự khác biệt cần đo. Đoạn code này chính là "tự cân lại cái cân" — trước khi tin vào bất kỳ con số so sánh mô hình nào, bạn cần biết chính phép đo của mình dao động bao nhiêu khi chỉ đổi mỗi *seed* (yếu tố lẽ ra không nên ảnh hưởng tới kết luận).

**🔬 Đào sâu kỹ thuật**

Đoạn code lặp qua 4 giá trị seed `(0, 1, 2, 42)`, với mỗi seed thực hiện **song song hai kiểu đo** trên cùng một dữ liệu:

1. `mot_lan`: đúng quy trình một-lần-chia (giống bước 1) — chia `Xh/Xk` theo seed `s`, fit, đo F1 trên `Xk`, gom vào danh sách.
2. `nhieu_lan`: đúng quy trình 5-fold CV (giống bước 2) — nhưng `StratifiedKFold` cũng nhận `random_state=s`, để mỗi seed cho ra một cách chia-5-phần khác nhau; lấy trung bình của 5 điểm CV, gom vào danh sách.

Cuối cùng, `max(...) - min(...)` trên mỗi danh sách 4 phần tử chính là **khoảng dao động qua 4 seed** — đúng hai con số 0,0177 và 0,0020 ở bảng mục 2.3. Đây là lý do bước này được gọi là "đo chính cái thước của mình": nó không đo mô hình nào tốt hơn mô hình nào, mà đo **độ tin cậy của chính quy trình đánh giá**, tách biệt hoàn toàn khỏi câu hỏi về mô hình. Về mặt thực hành trong 6 tiếng thi, chạy đoạn code này **một lần duy nhất** ở đầu buổi (trên bộ dữ liệu và mô hình cơ sở — baseline) sẽ cho bạn "biên độ nhiễu" dùng để diễn giải mọi so sánh sau đó: bất kỳ chênh lệch nào giữa hai phương án nhỏ hơn con số CV (0,0020 trong ví dụ này) đều nên được xem là nhiễu, không phải cải tiến thật.

---

## 4. Bài tập mẫu

> Đề. Buổi 06 tìm ra ngưỡng 0,42 bằng cách quét trên chính tập công khai và gọi đó là cái bẫy. Hãy làm lại
> cho đúng, rồi so ba con số.
>
> Quy trình đúng.
> 1. Cắt training_set.csv thành hai phần: học và kiểm định.
> 2. Huấn luyện trên phần học, quét ngưỡng trên phần kiểm định, chốt τ.
> 3. Huấn luyện lại trên toàn bộ dữ liệu huấn luyện.
> 4. Áp τ đã chốt lên tập công khai. Không quét lại.
>
> ```python
> import numpy as np
> # 1 and 2: pick the threshold on data the final model has not been scored against
> Xh, Xk, yh, yk = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
> m = mo_hinh()
> m.fit(Xh, yh)
> pk = m.predict_proba(Xk)[:, 1]
> tau = max(np.arange(0.05, 0.96, 0.01),
>           key=lambda t: f1(yk, (pk >= t).astype(int)))
>
> # 3: refit on everything, because more data is better
> m_cuoi = mo_hinh()
> m_cuoi.fit(X, y)
>
> # 4: apply the frozen threshold. No sweeping here.
> p = m_cuoi.predict_proba(de["van_ban_goc"])[:, 1]
> nhan = (p >= tau).astype(int)
> ```
>
> Kết quả. Ngưỡng chốt được là 0,41.
>
> Cách chọn ngưỡng macro-F1
>
> | Cách chọn ngưỡng | macro-F1 | Ghi chú |
> |---|---|---|
> | mặc định 0,50 | 0,7324 | không dùng dữ liệu nào để chọn |
> | chọn trên tập kiểm định riêng, τ = 0,41 | 0,7393 | cách đúng |
> | lấy trộm từ tập công khai, τ = 0,42 | 0,7409 | con số không tin được |
>
> Kết luận trung thực, không phải kết luận kịch tính
>
> Cách đúng lấy về 0,0069 trên tổng 0,0086 mà cách ăn trộm hứa hẹn, tức là tám phần mười phần lợi.
>
> Nói cách khác: làm đúng quy trình gần như không mất gì, mà được một con số bạn dám tin.
>
> Ở đây khoảng chênh giữa hai cách nhỏ, vì tập công khai khá lớn so với số lựa chọn ta quét. Đừng rút ra
> bài học "ăn trộm cũng chẳng sao". Bài học đúng là: giá của việc làm đúng thì rẻ, còn giá của việc làm
> sai thì bạn không biết trước là bao nhiêu.

**🧠 Ẩn dụ đời thường**

Đây là ẩn dụ "dời cột gôn sau khi đã sút bóng" (moving the goalposts). Buổi 06 đã sút bóng rồi mới đo xem cột gôn ở đâu là vừa khít với cú sút đó (quét ngưỡng ngay trên tập công khai) — dĩ nhiên là "vào gôn" tuyệt đối, vì cột gôn được đặt *sau khi biết* bóng bay tới đâu. Bài tập mẫu này làm lại đúng luật bóng đá thật: cột gôn (ngưỡng τ) phải được cố định *trước*, dựa trên một sân tập riêng (tập kiểm định), rồi mới đem ra sân thi đấu thật (tập công khai) sút **đúng một lần**, không được ngắm lại.

Con số "0,0069 trên tổng 0,0086 khả dĩ, tức tám phần mười" giống như: nếu gian lận hứa hẹn giúp bạn được thêm 10 điểm so với không làm gì, thì làm đúng luật vẫn giúp bạn được 8 điểm trong số đó — chỉ mất đi 2 điểm "ảo" mà đằng nào bạn cũng không nên tin. Đổi lại, bạn có một con số **thật**, không vỡ mộng khi ra tập riêng.

**🔬 Đào sâu kỹ thuật**

*Vì sao chọn ngưỡng (threshold) cũng là một dạng "tìm siêu tham số" phải tuân luật ở mục 2.4 và 2.2:* `τ` (ngưỡng phân loại) về bản chất là một tham số được **chọn dựa trên dữ liệu có nhãn**, hoàn toàn tương tự việc chọn `C` hay `min_df`. Nếu quét `τ` trực tiếp trên tập công khai (nơi lẽ ra chỉ đóng vai trò xác nhận cuối), tập công khai bị dùng để "huấn luyện" thêm một tham số nữa — đúng lỗi đã cảnh báo ở mục 2.2 và 2.4, chỉ là quy mô tìm kiếm nhỏ hơn (chỉ 1 tham số, quét trên khoảng `[0.05, 0.95]` bước `0.01`, tức 91 giá trị).

*Đọc từng dòng code:*
- `Xh, Xk, yh, yk = train_test_split(..., stratify=y)`: lần chia đầu tiên, dùng để **tách phần dữ liệu sẽ dùng riêng cho việc quét ngưỡng** — đây chính là vai trò "tập kiểm định của riêng bạn" nói ở mục 2.6, cắt ra từ `training_set.csv` chứ không đụng gì tới tập công khai.
- `m.fit(Xh, yh)` rồi `pk = m.predict_proba(Xk)[:, 1]`: huấn luyện trên phần học, lấy **xác suất dự đoán thuộc lớp 1** (cột thứ hai của `predict_proba`, vì lớp 0 và lớp 1 là hai cột, chỉ số `[:, 1]` lấy cột lớp dương) trên phần kiểm định — chú ý đây là `predict_proba`, không phải `predict`, vì quét ngưỡng cần xác suất liên tục để thử nhiều mốc cắt khác nhau (khác biệt `predict_proba` và `predict` đã học ở buổi 05).
- `tau = max(np.arange(0.05, 0.96, 0.01), key=lambda t: f1(yk, (pk >= t).astype(int)))`: đây là một phép quét ngưỡng bằng hàm `max` với `key` — với mỗi ứng viên `t` trong dải từ 0,05 đến 0,95 (bước 0,01), tính macro-F1 nếu cắt ngưỡng tại `t`, rồi chọn `t` cho F1 cao nhất. Vì phép quét này chỉ nhìn `yk` (nhãn thật của phần kiểm định riêng, **không phải** nhãn của tập công khai — mà thực ra tập công khai vốn không có nhãn để bạn nhìn), nó hợp lệ.
- `m_cuoi.fit(X, y)`: sau khi đã **chốt xong** `τ`, huấn luyện lại mô hình cuối cùng trên **toàn bộ** dữ liệu huấn luyện có nhãn (`X, y`, gộp cả `Xh` lẫn `Xk`) — nguyên tắc "càng nhiều dữ liệu càng tốt" cho mô hình *cuối cùng*, vì lúc này bạn không còn cần giữ lại phần nào để đo nữa (đã đo và chốt `τ` xong ở bước trước).
- `p = m_cuoi.predict_proba(de["van_ban_goc"])[:, 1]; nhan = (p >= tau).astype(int)`: áp đúng ngưỡng đã đóng băng (`tau`, không quét lại) lên dữ liệu đề bài thật (`de["van_ban_goc"]`) để ra nhãn dự đoán cuối cùng nộp bài.

*Diễn giải bảng kết quả bằng số học:* gọi lợi ích "hứa hẹn" của việc ăn trộm là `0,7409 - 0,7324 = 0,0085` (bài ghi tròn 0,0086, sai số làm tròn), còn lợi ích **thật sự đạt được** bằng cách làm đúng là `0,7393 - 0,7324 = 0,0069`. Tỉ lệ `0,0069 / 0,0086 ≈ 0,80` — đúng "tám phần mười phần lợi" bài đã nêu. Điểm mấu chốt: phần chênh còn lại `0,0086 - 0,0069 = 0,0017` (giữa cách đúng và cách ăn trộm) là **giá trị ảo**, sinh ra từ việc `τ = 0,42` được chọn để khớp *khéo* với đúng 800 dòng của tập công khai — nó không phản ánh gì về hiệu năng thật của mô hình, và hoàn toàn có thể đảo chiều (âm) trên tập riêng, vì tập riêng có 800 dòng *khác*, ngưỡng "khéo" cho bộ này chưa chắc khéo cho bộ kia. Đây là lý do bài kết luận: "giá của làm đúng thì rẻ (chỉ mất 0,0017 so với mức tối đa lý thuyết), còn giá của làm sai thì không biết trước là bao nhiêu" — trên một bài toán khác, với ngưỡng nhạy hơn hoặc tập công khai nhỏ hơn, khoảng chênh ảo này có thể lớn hơn nhiều.

---

## 5. Bài tập tự làm

> **Bài tập 1. Đường cong học**
>
> Huấn luyện mô hình vừa trên 10%, 25%, 50%, 75%, 100% dữ liệu, vẽ điểm huấn luyện và điểm kiểm
> định theo kích thước tập huấn luyện.
>
> Cổng kiểm
>
> Hai đường tiến lại gần nhau khi dữ liệu tăng. Rồi trả lời: nhìn hình này, thêm dữ liệu có giúp được nữa
> không, hay đã tới lúc phải đổi mô hình?

**🧠 Ẩn dụ đời thường:** đây gọi là **đường cong học (learning curve)** — giống việc theo dõi một vận động viên tập luyện: lúc đầu (ít dữ liệu) thành tích trên bài tập và thành tích thi đấu chênh nhau rất xa (thuộc lòng vài bài tập thì làm tốt, nhưng ra thi lại bỡ ngỡ); càng tập nhiều bài đa dạng hơn (nhiều dữ liệu hơn), khoảng cách giữa "làm bài tập" và "đi thi" càng thu hẹp, vì vận động viên buộc phải học *quy luật chung* thay vì thuộc lòng từng bài cụ thể.

**🔬 Đào sâu kỹ thuật — gợi ý hướng làm (không giải sẵn, vì đây là bài tự luyện):**
- sklearn có sẵn `sklearn.model_selection.learning_curve` để tự động thực hiện đúng việc "huấn luyện trên từng phần trăm dữ liệu rồi đo train/validation score" — đáng để tìm hiểu cách dùng thay vì viết vòng lặp thủ công.
- Nhớ dùng **cùng một tập kiểm định cố định** (không đổi) khi tăng dần kích thước tập huấn luyện, để trục hoành chỉ có đúng một biến thay đổi (kích thước huấn luyện), đúng nguyên tắc "mỗi lần chỉ đổi một biến" đã thấy ở mục 3.1.
- Đọc hình theo đúng khung bias–variance đã học ở mục 2.1: nếu hai đường **đã hội tụ** về gần nhau nhưng **hội tụ ở mức điểm thấp** → bias cao → thêm dữ liệu vô ích, cần đổi mô hình (mô hình phức tạp hơn, hoặc đặc trưng tốt hơn). Nếu hai đường **còn đang thu hẹp khoảng cách** nhưng chưa chạm nhau và đường kiểm định còn đang đi lên → variance vẫn cao → thêm dữ liệu còn có ích.

> **Bài tập 2. Dựng lại bảng sức chứa**
>
> Ba dòng, ba mô hình, năm cột.
>
> Cổng kiểm
>
> Khớp bảng ở mục 2.1 tới chữ số thập phân thứ tư, kể cả số đặc trưng 696, 2143, 3834.

**🧠 Ẩn dụ đời thường:** đây là bài "kiểm tra tay nghề tái lập thí nghiệm" — giống việc một sinh viên hoá học phải tự làm lại đúng thí nghiệm trong sách giáo khoa và ra đúng con số đã ghi, để chắc chắn mình hiểu quy trình chứ không chỉ đọc và tin.

**🔬 Đào sâu kỹ thuật — gợi ý:** chạy nguyên văn đoạn code ở mục 3.1. Nếu ra số khác đi dù chỉ ở chữ số thập phân thứ tư, khả năng cao là một trong các nguyên nhân: (1) `random_state` bị đặt khác ở đâu đó, (2) dữ liệu `X, y` nạp vào không giống thứ tự/nội dung, (3) phiên bản scikit-learn khác nhau đôi khi làm thay đổi cách khởi tạo mặc định của solver trong `LogisticRegression`. Nếu số đặc trưng (696/2143/3834) lệch, gần như chắc chắn là do cách tiền xử lý văn bản đầu vào (`X`) trước khi đưa vào `TfidfVectorizer` khác với bản gốc — kiểm tra lại bước đọc/làm sạch dữ liệu đầu tiên.

> **Bài tập 3. Xác thực chéo ổn định hơn bao nhiêu**
>
> Dựng lại hai con số 0,0177 và 0,0020.
>
> Cổng kiểm
>
> Hai con số khớp. Rồi thử với k = 10 và ghi lại xem nó ổn định thêm bao nhiêu, đổi lại tốn thêm bao
> nhiêu thời gian.

**🧠 Ẩn dụ đời thường:** tăng `k` từ 5 lên 10 giống như tăng số muỗng nếm nồi súp từ 5 lên 10 — nếm càng nhiều điểm, ước lượng vị trung bình càng chính xác, nhưng bạn cũng phải tốn công nếm gấp đôi số lần.

**🔬 Đào sâu kỹ thuật — gợi ý:** chạy nguyên văn code mục 3.3. Về mặt lý thuyết, tăng `k` từ 5 lên 10 làm mỗi tập huấn luyện trong từng fold lớn hơn (90% dữ liệu thay vì 80%) — mô hình mỗi fold gần với "mô hình cuối" hơn — nhưng số lần huấn luyện tăng gấp đôi (10 lần thay vì 5 lần mỗi lần chạy CV). Khi ghi lại kết quả, hãy so sánh trên **cả hai trục**: mức giảm của khoảng dao động qua 4 seed (trục "độ tin cậy") và thời gian chạy thực tế đo bằng `time.time()` (trục "chi phí") — đây chính là phép đánh đổi thực dụng bài gốc nhắc tới ở cuối mục 2.3 ("trong sáu tiếng thi, năm lần huấn luyện là đắt"): tăng `k` luôn cho thước đo ổn định hơn về mặt lý thuyết, nhưng có đáng tăng hay không phụ thuộc vào ngân sách thời gian còn lại của bạn trong phòng thi.

> **Bài tập 4. Tự tạo một vụ rò rỉ lớn**
>
> Mục 2.5 cho một ví dụ rò rỉ nhỏ. Hãy tạo một ví dụ lớn: chọn 200 đặc trưng có tương quan cao nhất với
> nhãn, tính tương quan ấy trên cả tập kiểm định, rồi mới chia tập và huấn luyện.
>
> Cổng kiểm
>
> Điểm kiểm định cao lên rõ rệt so với cách làm sạch. Ghi lại chênh lệch. Đây là hình ảnh của một bài
> nộp trông rất tốt cho tới lúc chấm trên tập riêng.

**🧠 Ẩn dụ đời thường:** đây là bài tập "tự tay làm hư cái cân" để hiểu vì sao phải giữ nó nguyên vẹn. Bạn cố tình để một chút "đáp án" (thông tin từ nhãn của tập kiểm định) rò vào bước chọn đặc trưng, rồi quan sát điểm số bị thổi phồng lên bao nhiêu — như tự tay đặt thêm quả cân giả lên đĩa cân để thấy "kim chỉ sai lệch đến mức nào" trước khi tự nhắc mình không bao giờ làm vậy thật.

**🔬 Đào sâu kỹ thuật — gợi ý hướng làm:**
- **Quy trình rò rỉ (cố tình sai, chỉ để thí nghiệm):** tính tương quan (ví dụ hệ số tương quan Pearson hoặc điểm ANOVA F-test, `sklearn.feature_selection.f_classif`) giữa từng đặc trưng và nhãn `y` trên **toàn bộ** `X` (gồm cả phần sẽ dùng làm kiểm định) → chọn ra 200 đặc trưng có tương quan cao nhất → **sau đó mới** `train_test_split` → huấn luyện và đo.
- **Quy trình sạch (đối chứng):** `train_test_split` **trước** → chỉ tính tương quan và chọn 200 đặc trưng trên `Xh` (tập huấn luyện) → dùng đúng 200 cột đã chọn đó để `transform` cả `Xh` và `Xk` → huấn luyện trên `Xh`, đo trên `Xk`.
- sklearn có sẵn `SelectKBest(score_func=f_classif, k=200)` — nếu nhét đúng cách vào bên trong một `Pipeline` (đặt trước bước mô hình), việc gọi `.fit()` trên `Xh` sẽ tự động đảm bảo bước chọn đặc trưng chỉ "nhìn thấy" `Xh`, chính là cách phòng tránh triệt để lỗi mà bài tập yêu cầu cố tình tạo ra.
- Kỳ vọng quan sát: chênh lệch điểm giữa hai quy trình ở đây sẽ **lớn hơn hẳn** 0,0042 của ví dụ nhỏ ở mục 2.5, vì lần này thông tin rò rỉ là **tương quan trực tiếp với nhãn** — mang nhiều thông tin hơn hẳn so với "chỉ thêm vài mẩu từ vựng". Con số chênh lệch cụ thể phụ thuộc vào bộ dữ liệu bạn dùng để thử — hãy tự chạy và ghi lại, đúng tinh thần "đo thật" xuyên suốt cả bài giảng này.

> **Bài tập 5. Kế hoạch hai mươi lượt nộp**
>
> Viết ra giấy, một trang: bạn sẽ dùng 20 lượt nộp của 5 tiếng đầu vào việc gì, và 5 lượt của tiếng cuối vào
> việc gì.
>
> Cổng kiểm
>
> Kế hoạch phải trả lời được: lượt nộp đầu tiên xảy ra ở phút thứ mấy, và trong trường hợp nào bạn không
> nộp dù còn lượt. Buổi 23 sẽ đem kế hoạch này ra chạy thật.

**🧠 Ẩn dụ đời thường:** đây giống việc lập **ngân sách chi tiêu** cho một chuyến du lịch có quỹ tiền mặt cố định, không rút thêm được — bạn không tiêu tuỳ hứng ngay khi vừa đến nơi, mà định trước: bao nhiêu cho ăn, bao nhiêu để dành cho tình huống khẩn cấp, và quan trọng nhất — **nguyên tắc khi nào không tiêu dù còn tiền** (ví dụ: không mua thêm gì nữa nếu giá cao bất thường), y hệt tinh thần "không dùng để dò" ở mục 2.6.

**🔬 Đào sâu kỹ thuật — khung gợi ý để tự lập kế hoạch (không thay bạn quyết định, vì đây là chiến lược cá nhân):**
- **Lượt nộp đầu tiên nên xảy ra sau khi nào?** Gợi ý theo đúng logic mục 2.6: chỉ nộp sau khi đã có một pipeline hoàn chỉnh chạy được đầu-cuối và đã tự đánh giá bằng CV nội bộ — lượt đầu tiên dùng để **kiểm tra xem điểm công khai có khớp với điểm CV nội bộ không** (một dạng "hiệu chỉnh đồng hồ" — sanity check), không phải để dò xem mô hình nào tốt hơn.
- **Phân bổ 20 lượt còn lại:** cân nhắc dành phần lớn cho các mốc "chốt giai đoạn" (ví dụ: sau khi hoàn thành baseline, sau khi thêm một nhóm đặc trưng mới, sau khi đổi họ mô hình ở buổi 08) thay vì rải đều theo thời gian — mỗi lượt nên gắn với một **câu hỏi cụ thể** cần xác nhận, đúng tinh thần "lượt nộp chỉ dùng để xác nhận, không dùng để dò".
- **Khi nào không nộp dù còn lượt?** Đây là câu hỏi cổng kiểm nhấn mạnh nhất. Gợi ý nguyên tắc: nếu một thay đổi bạn vừa thử **chưa** cho thấy cải tiến vượt qua "biên độ nhiễu" đã tự đo được ở Bài tập 3 (khoảng dao động CV) trên tập kiểm định nội bộ, thì chưa có lý do gì để tốn một lượt nộp xác nhận nó — vì gần như chắc chắn kết quả sẽ nằm trong khoảng nhiễu, không dạy bạn thêm gì mới.
- **5 lượt cuối cùng (tập riêng, không sửa được):** vì tuyệt đối không có cơ hội sửa sai, nguyên tắc hợp lý là chỉ nộp phiên bản mô hình **đã được xác nhận ổn định nhất** trong 5 tiếng đầu — tránh thử nghiệm mạo hiểm ở giai đoạn này.

---

## Chuẩn bị cho buổi sau

> Buổi 08 chuyển sang họ mô hình khác: KNN, cây quyết định, rừng ngẫu nhiên, boosting. Mang theo câu hỏi:
> vì sao gộp nhiều mô hình yếu lại cho ra một mô hình mạnh, trong khi gộp nhiều người đoán mò thì vẫn là
> đoán mò?

**🧠 Ẩn dụ đời thường:** câu hỏi này chính là bản chất của **"trí tuệ đám đông" (wisdom of the crowd)**. Nếu bạn hỏi 100 người *hoàn toàn không biết gì* về cân nặng một con bò để đoán mò hoàn toàn ngẫu nhiên, trung bình 100 câu đoán mò đó vẫn chỉ là... đoán mò, không hội tụ về đâu cả. Nhưng nếu 100 người đó *mỗi người biết một chút, sai theo những hướng khác nhau, nhưng đúng hơn tung đồng xu* — thì trung bình các dự đoán của họ có xu hướng hội tụ về giá trị đúng, vì sai số ngẫu nhiên của từng người có xu hướng triệt tiêu lẫn nhau khi gộp lại.

**🔬 Đào sâu kỹ thuật (mồi trước cho buổi 08):** điều kiện toán học để việc gộp (ensemble) nhiều mô hình yếu tạo ra mô hình mạnh hơn gồm hai vế: (1) mỗi mô hình thành phần phải **tốt hơn đoán ngẫu nhiên** một chút (weak learner, không phải random guesser — khác biệt cốt lõi trả lời thẳng câu hỏi buổi 08 đặt ra), và (2) sai số của các mô hình thành phần phải **đa dạng, không hoàn toàn tương quan** với nhau (nếu tất cả mô hình sai giống hệt nhau ở cùng một chỗ, gộp lại cũng sai y hệt vậy, không có gì để triệt tiêu). Đây chính là nguyên lý nền cho `RandomForest` (đa dạng hoá bằng cách mỗi cây chỉ thấy một phần ngẫu nhiên của dữ liệu và đặc trưng) và `Boosting` (mỗi mô hình mới cố tình tập trung sửa lỗi mà các mô hình trước đó còn mắc). Ngoài ra, nhiều kỹ thuật của buổi 07 sẽ quay lại nguyên vẹn ở buổi 08: cây quyết định càng sâu càng dễ quá khớp (đúng khung bias–variance ở mục 2.1, chỉ đổi "độ sâu cây" thay cho "C" hay "ngram_range"), và việc chọn số cây/độ sâu tối ưu vẫn phải dùng đúng xác thực chéo ở mục 2.3, không được dò trên tập kiểm tra.

---

## 7. Tổng kết nhanh (bonus)

*(Phần này không có trong bài giảng gốc — thêm vào để tiện ôn lại nhanh trước khi thi, không thay thế phần nội dung chi tiết ở trên.)*

| Khái niệm | Câu hỏi cốt lõi | Con số mấu chốt trong buổi |
|---|---|---|
| Chưa khớp / quá khớp | Chênh lệch train − validation có đang tăng dần theo sức chứa không? | 0,0319 → 0,0366 → 0,0466 |
| Ba tập | Tập này đã bị "nhìn để quyết định" bao nhiêu lần rồi? | test chỉ đụng **1 lần**, ở cuối |
| Xác thực chéo | So sánh hai phương án — chênh lệch có vượt qua độ rung của thước đo không? | 1 lần chia: ±0,0177 · CV 5-fold: ±0,0020 |
| Tìm siêu tham số | Bao nhiêu tham số? Ít → grid; nhiều → random | thử 500 tổ hợp = tập kiểm định mòn |
| Rò rỉ dữ liệu | Bước có chữ `fit` này có đang "thấy" nhãn hoặc phân phối của tập kiểm định không? | vocab rò rỉ: +0,0042 · tương quan-nhãn rò rỉ: lớn hơn nhiều |
| Luật thi | Lượt nộp này dùng để **xác nhận** hay để **dò**? | 20 lượt / 5 tiếng, 5 lượt / 1 tiếng cuối, không sửa |

Chúc Bobo ôn tập hiệu quả — hẹn buổi 08 với KNN, cây quyết định, rừng ngẫu nhiên và boosting!
