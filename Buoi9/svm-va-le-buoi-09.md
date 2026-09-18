# Buổi 09 — SVM và lề

*Luyện Olympic Trí tuệ nhân tạo · Học máy cổ điển · Phục vụ sơ loại*
*Ngày 25/8/2026 · Giảng viên TS. Đỗ Phúc Hảo · Bản mở rộng & trực quan hoá*

> **Quy ước đọc:** khối trích dẫn (`>`) là **nội dung gốc**, giữ nguyên 100%. Đoạn bắt đầu bằng 🧠 là phần giải thích, đào sâu, ví dụ và ẩn dụ được bổ sung thêm.

---

## Mục lục

1. [Mục tiêu](#1-mục-tiêu)
2. [2.1 Siêu phẳng và ba con số](#21-siêu-phẳng-và-ba-con-số-phải-thuộc)
3. [2.2 Vì sao lề rộng](#22-vì-sao-lề-rộng)
4. [2.3 Ví dụ tám điểm](#23-một-ví-dụ-tám-điểm-giải-bằng-mắt)
5. [2.4 Lề mềm và tham số C](#24-lề-mềm-và-tham-số-c)
6. [2.5 Kernel](#25-kernel-đổi-hình-dạng-ranh-giới-mà-không-đổi-thuật-toán)
7. [3. Bài tập mẫu](#3-bài-tập-mẫu)
8. [4. Bài tập tự làm](#4-bài-tập-tự-làm)
9. [Chuẩn bị cho buổi sau](#chuẩn-bị-cho-buổi-sau)

---

## 1. Mục tiêu

> Tính tay được dấu của $w \cdot x + b$, nói được vector hỗ trợ là gì, và trả lời được câu hỏi buổi 08 để lại: vì sao lề rộng lại tổng quát tốt hơn, trong khi cả hai đường thẳng đều chia đúng toàn bộ dữ liệu huấn luyện?
>
> Phần tính tay không phải để cho đẹp. Đề sơ loại 2025 có câu cho sẵn $w$, $b$ và một điểm, hỏi điểm ấy thuộc lớp nào, và bạn không có máy tính trong phòng thi.

🧠 **Phân tích chi tiết & Bản chất:**
- Buổi này chỉ xoay quanh một đường thẳng (hoặc một mặt phẳng, tổng quát hơn là một **siêu phẳng**) chia không gian làm hai nửa. Mọi thứ khác — vector hỗ trợ, lề, lề mềm, kernel — đều là cách trả lời cho một câu hỏi duy nhất: *trong vô số đường có thể chia đúng dữ liệu, nên chọn đường nào?*
- Hãy hình dung bạn kẻ một hàng rào giữa hai đàn cừu trên một cánh đồng. Có rất nhiều cách kẻ mà không con cừu nào lạc sang bên kia. Nhưng nếu hàng rào áp sát một con cừu đứng gần biên, chỉ cần con đó nhích một bước là "đổi phe". Hàng rào nằm giữa khoảng trống rộng nhất giữa hai đàn thì chịu được nhiều xê dịch hơn — đó là trực giác về **lề** (margin), sẽ hình thức hoá ở mục 2.2.
- Vì sao nhấn mạnh "tính tay, không máy tính"? Câu hỏi dạng "cho $w,b$ và một điểm, hỏi lớp nào" chỉ cần thay số vào một biểu thức tuyến tính rồi xem dấu — nhưng nếu không luyện phản xạ, học sinh dễ nhầm ba đại lượng rất giống nhau về hình thức: dấu, khoảng cách, bề rộng lề (mục 2.1).

---

## 2. Tóm tắt kiến thức

### 2.1 Siêu phẳng, và ba con số phải thuộc

> Một mô hình tuyến tính chia không gian bằng mặt $w \cdot x + b = 0$. Ba đại lượng, học một lần dùng cả đời:

| Đại lượng | Công thức | Đọc là |
|---|---|---|
| dấu | $\operatorname{sign}(w \cdot x + b)$ | điểm nằm phía nào |
| khoảng cách | $\dfrac{|w \cdot x + b|}{\lVert w \rVert}$ | xa mặt phân chia bao nhiêu |
| bề rộng lề | $\dfrac{2}{\lVert w \rVert}$ | khoảng trống giữa hai lớp |

> Chú ý một điều mà đề thi hay hỏi xoáy: $|w \cdot x + b|$ không phải khoảng cách. Nó chỉ tỉ lệ với khoảng cách. Nhân cả $w$ lẫn $b$ với 10 thì mặt phân chia không nhúc nhích, mọi giá trị $w \cdot x + b$ tăng mười lần, còn khoảng cách thật thì giữ nguyên vì $\lVert w \rVert$ cũng tăng mười lần.

🧠 **Phân tích chi tiết & Bản chất:**
- Cả ba đại lượng đều tính từ $f(x) = w \cdot x + b$, chỉ khác ở việc có chuẩn hoá theo $\lVert w \rVert$ hay không: **dấu** là câu trả lời thô; **khoảng cách** loại bỏ ảnh hưởng của việc "phóng to" $w$, có ý nghĩa hình học thật; **bề rộng lề** chỉ có nghĩa sau khi chuẩn hoá sao cho điểm gần nhất có $|f(x)|=1$ (quy ước dùng xuyên suốt buổi — xem mục 2.3).
- Ẩn dụ: $\lVert w \rVert$ giống "độ giãn" của một cái thước đo. Nếu ai đó kéo giãn thước gấp đôi mà không báo, số đo bạn đọc cũng tăng gấp đôi dù vật không hề lớn thêm. Muốn có số đo thật, phải chia cho độ giãn ấy.
- **Chứng minh nhanh:** gọi $x_0$ là hình chiếu vuông góc của $x$ lên mặt $w\cdot x+b=0$. Khi đó $x = x_0 + d\cdot \dfrac{w}{\lVert w\rVert}$ với $d$ là khoảng cách có dấu. Thay vào:
$$w\cdot x + b = w\cdot x_0+b + d\cdot\frac{w\cdot w}{\lVert w\rVert} = 0 + d\cdot \lVert w\rVert$$
vì $w\cdot x_0+b=0$ và $w\cdot w=\lVert w\rVert^2$. Suy ra $d = \dfrac{w\cdot x+b}{\lVert w\rVert}$ — công thức trong bảng là kết quả của một phép chiếu hình học, không phải quy ước tuỳ tiện.
- **Mẹo thi:** với cùng một $w$ cố định trong một câu hỏi, tỉ lệ $|f(x_1)|:|f(x_2)|$ vẫn đúng bằng tỉ lệ khoảng cách vì $\lVert w\rVert$ là mẫu số chung. Cái không được làm là so $|f(x)|$ giữa **hai mô hình khác nhau** như thể chúng là khoảng cách — đó là bẫy đề thi hay hỏi xoáy.

```
        lớp −1  |   lề (không có dữ liệu)   |  lớp +1
   ─────────────┆───────────┆───────────────
                x₁=1    H: w·x+b=0    x₁=3      ← ví dụ minh hoạ, xem mục 2.3
                       (khoảng cách d đo từ
                        một điểm x bất kỳ
                        tới đường H này)
```

---

### 2.2 Vì sao lề rộng

> Nếu hai lớp tách được thì có vô hạn đường thẳng chia đúng chúng. SVM chọn đường có lề rộng nhất, tức là đường ở xa cả hai lớp nhất có thể.
>
> Lý do không phải thẩm mỹ. Dữ liệu kiểm tra là dữ liệu huấn luyện cộng một chút xê dịch. Đường sát rạt vào một điểm huấn luyện sẽ đổi phía ngay khi điểm ấy xê dịch một chút; đường cách cả hai lớp một khoảng $\gamma$ thì chịu được mọi xê dịch nhỏ hơn $\gamma$. Lề chính là lượng nhiễu mà nghiệm chịu được trước khi sai.
>
> Bài toán viết ra là: cực tiểu $\dfrac{1}{2}\lVert w \rVert^2$ với ràng buộc $y_i(w \cdot x_i + b) \geq 1$ cho mọi $i$. Cực tiểu $\lVert w \rVert$ chính là cực đại $2/\lVert w \rVert$.

🧠 **Phân tích chi tiết & Bản chất:**
- Đây chính là câu trả lời cho "câu hỏi buổi 08 để lại". Hai đường cùng chia đúng 100% dữ liệu huấn luyện không có nghĩa chúng tốt như nhau trên dữ liệu mới — vì dữ liệu mới chỉ *gần giống*, được mô hình hoá đơn giản là "huấn luyện cộng một chút nhiễu".
- Ẩn dụ: một ô tô đỗ giữa khoảng trống hai xe khác. Đỗ sát một bên thì gió nhẹ hay lệch 5cm cũng va quẹt; đỗ đúng giữa thì có vùng đệm an toàn cả hai phía. Lề chính là vùng đệm đó, SVM là thuật toán "đỗ xe cẩn thận nhất có thể".
- **Vì sao thành bài toán tối ưu:** với hướng $w/\lVert w\rVert$ cố định và quy ước điểm gần nhất mỗi lớp thoả $y_i(w\cdot x_i+b)=1$, khoảng cách từ điểm gần nhất tới mặt là $1/\lVert w\rVert$ (theo công thức mục 2.1), lề hai phía là $2/\lVert w\rVert$. Lề lớn nhất ⇔ $\lVert w\rVert$ nhỏ nhất. Tối ưu $\frac12\lVert w\rVert^2$ thay vì $\lVert w\rVert$ trực tiếp vì lý do kỹ thuật: bình phương làm hàm khả vi mượt, biến bài toán thành quy hoạch toàn phương lồi — có nghiệm duy nhất, giải hiệu quả.
- **Đọc ràng buộc:** nếu $y_i=+1$, ràng buộc là $w\cdot x_i+b\ge 1$; nếu $y_i=-1$, thành $w\cdot x_i+b\le -1$ sau khi nhân $-1$. Nhân với $y_i$ là mẹo viết gọn hai trường hợp thành một bất phương trình — mẹo này lặp lại ở lề mềm (2.4).
- Liên hệ rộng hơn: đây là một dạng cụ thể của "regularization" (phạt độ lớn trọng số) như Ridge/Lasso, nhưng ở SVM phần thưởng của việc phạt $\lVert w\rVert$ có ý nghĩa hình học tường minh: lề rộng hơn.

---

### 2.3 Một ví dụ tám điểm, giải bằng mắt

> Lớp +1: $(3,1), (3,-1), (6,1), (6,-1)$. Lớp −1: $(1,0), (0,1), (0,-1), (-1,0)$.
>
> Nhìn là thấy: hai lớp cách nhau theo trục hoành, lớp âm dừng ở $x_1=1$ và lớp dương bắt đầu ở $x_1=3$. Đường ở giữa là $x_1=2$. Viết theo dạng chuẩn thì $w=(1,0)$ và $b=-2$, vì khi ấy điểm gần nhất của mỗi lớp cho đúng $y(w\cdot x+b)=1$.

```
 x2
  1 |  −(0,1)        +(3,1)        +(6,1)
    |
  0 |  +(−1,0)   ⊙(1,0)   |   ⊙(3,−1)…      x1 →
    |                     |
 −1 |  −(0,−1)            +(3,−1)       +(6,−1)
    ------------------------------------------
        x1=1(margin) x1=2(H)  x1=3(margin)

  ⊙ = vector hỗ trợ: (1,0), (3,1), (3,−1)
```

🧠 **Phân tích chi tiết & Bản chất:**
- **Vì sao nhìn ra $w=(1,0)$, $b=-2$ mà không cần giải hệ phương trình:** toạ độ $x_2$ hoàn toàn không ảnh hưởng tới phân loại (đối xứng qua trục hoành) → $w_2=0$. Còn lại là bài toán một chiều: chia đôi khoảng trống từ $x_1=1$ đến $x_1=3$, trung điểm $x_1=2$. Với $w_1=1$: $f(x)=x_1-2$, bằng $0$ tại $x_1=2$, bằng $-1$ tại $x_1=1$, bằng $+1$ tại $x_1=3$ — khớp quy ước ở mục 2.2.
- **Vector hỗ trợ, nói trần trụi:** những điểm huấn luyện nằm đúng trên đường lề ($y_if(x_i)=1$). Giống ba cái chân của một ghế đẩu — chỉ chúng "chống đỡ" siêu phẳng. Bốn điểm còn lại giống đồ vật đặt lên mặt ghế: có hay không cũng không làm ghế nghiêng.

| Đại lượng | Tính tay | SVC(kernel="linear", C=1e6) |
|---|---:|---:|
| $w_1$ | 1 | 1,000482 |
| $w_2$ | 0 | 0 |
| $b$ | −2 | −2,001124 |
| bề rộng lề | 2 | 1,999037 |
| số vector hỗ trợ | 3 | 3 |

> Ba vector hỗ trợ là $(1,0)$ của lớp âm và $(3,1), (3,-1)$ của lớp dương. Bốn điểm còn lại không tham gia: xoá cả bốn khỏi dữ liệu rồi huấn luyện lại thì nghiệm vẫn thế. Tôi đã thử, và bộ giải cho $w=(1{,}000192; 0{,}000384)$, $b=-2{,}000448$, tức là lệch ở chữ số thập phân thứ tư đúng như sai số nói ở khung dưới. Về lý thuyết thì nghiệm không đổi một chút nào. Đó là đặc điểm riêng của SVM, và cũng là lý do người ta gọi nó là máy vector hỗ trợ.

🧠 **Phân tích chi tiết & Bản chất:**
- Đây là tính chất phân biệt SVM với hồi quy logistic. Logistic dùng *tất cả* điểm để cập nhật nghiệm (mỗi điểm góp một gradient, dù nhỏ). SVM (lề cứng) thì nghiệm chỉ là hàm của các vector hỗ trợ — các điểm khác có trọng số đóng góp bằng 0 trong nghiệm đối ngẫu. Đây là lý do tên gọi "Support Vector Machine" mô tả đúng cơ chế, không phải tên tiếp thị.
- Hệ quả thực dụng: với dữ liệu phân tách rõ ràng, có thể xoá các điểm không phải vector hỗ trợ mà không đổi nghiệm — chính là điều bài giảng vừa kiểm chứng bằng thực nghiệm.

> **Cột bên phải không tròn, và đó là câu chuyện thật.**
> $C=1e6$ không phải lề cứng, nó là lề mềm với hình phạt rất lớn. Nghiệm số vì thế lệch khỏi nghiệm đúng ở chữ số thứ tư. Đừng sửa nó thành 1,000000 cho đẹp: khi bạn so kết quả của mình với kết quả bạn bên cạnh và thấy lệch $5\cdot10^{-4}$, bạn cần biết rằng đó là chuyện bình thường chứ không phải một trong hai người sai.
>
> Hệ quả sắc hơn: điểm $(2,0)$ nằm đúng trên mặt phân chia lý thuyết, nên $w\cdot x+b=0$. Mô hình đã học cho ra $-0{,}000161$, tức là nó xếp điểm ấy vào lớp âm vì một sai số làm tròn. Với điểm nằm sát mặt phân chia thì nhãn không do mô hình quyết định mà do dấu phẩy động quyết định.

🧠 **Vì sao điều này quan trọng khi đi thi và khi debug:**
1. **Bài học về số học:** mọi bộ giải số đều dừng khi sai số nhỏ hơn ngưỡng `tol`, không chạy tới sai số bằng 0 tuyệt đối. $C=10^6$ là một số hữu hạn rất lớn, không phải "vô cực" — nghiệm vẫn là nghiệm của lề *mềm*, chỉ mềm với mức phạt gần như cứng. Lệch ở chữ số thập phân thứ 3–4 là dấu hiệu solver đúng, không phải sai.
2. **Bài học về ranh giới quyết định:** với điểm có $f(x)$ lý thuyết bằng 0, bất kỳ nhiễu số học cực nhỏ nào cũng đẩy nó sang một phía. Đây không phải lỗi mô hình — toán học không có lời giải cho điểm nằm đúng trên biên, và thư viện buộc phải chọn một quy ước. Sẽ quay lại ở mục 3 với ví dụ cụ thể hơn.

---

### 2.4 Lề mềm và tham số C

> Dữ liệu thật không tách được bằng đường thẳng. Lề mềm cho phép vi phạm, mỗi vi phạm trả một khoản phạt $C$:
>
> $$\min_{w,b,\xi} \ \frac{1}{2}\lVert w \rVert^2 + C\sum_i \xi_i, \qquad y_i(w\cdot x_i+b) \ge 1-\xi_i,\ \ \xi_i \ge 0.$$
>
> $C$ nhỏ nghĩa là vi phạm rẻ, nên mô hình chọn lề rộng và chịu sai nhiều. $C$ lớn nghĩa là vi phạm đắt, nên mô hình bóp lề lại để chiều lòng từng điểm. Đo thật trên TF-IDF ký tự 2143 đặc trưng của tác vụ 1:

🧠 **Phân tích chi tiết & Bản chất:**
- **Biến $\xi_i$ là gì?** Đo mức độ điểm $i$ "phạm luật" — bao nhiêu đơn vị không đạt yêu cầu $y_if(x_i)\ge 1$. Nằm đúng phía và ngoài lề: $\xi_i=0$. Nằm trong lề nhưng vẫn đúng phía: $0<\xi_i<1$. Bị phân loại sai hẳn: $\xi_i>1$. Hàm mục tiêu cộng thêm $C\sum_i\xi_i$ — mô hình trả "hoá đơn" tỉ lệ tổng vi phạm, $C$ là đơn giá.
- Ẩn dụ: $C$ như tiền phạt vượt đèn đỏ. Phạt gần 0 ($C$ nhỏ) → tài xế vượt đèn đỏ liên tục để đi tắt (lề rộng, chấp nhận nhiều điểm sai phía). Phạt rất cao ($C$ lớn) → dừng đúng từng cột đèn (lề hẹp), dù phải đi ngoằn ngoèo (dễ quá khớp).
- $C$ đóng vai trò siêu tham số cân bằng thiên lệch–phương sai: $C$ nhỏ → thiên lệch cao, phương sai thấp; $C$ lớn → thiên lệch thấp, phương sai cao.

| C | Tập đã học | Kiểm định | Vector hỗ trợ | Tỉ lệ |
|---:|---:|---:|---:|---:|
| 0,01 | 0,3482 | 0,3482 | 4506 | 93,9% |
| 0,1 | 0,6142 | 0,6137 | 4434 | 92,4% |
| 1 | 0,7056 | 0,6898 | 3426 | 71,4% |
| 4 | 0,7131 | 0,6989 | 2988 | 62,2% |
| 10 | 0,7129 | 0,7018 | 2834 | 59,0% |
| **100** | **0,7217** | **0,7077** | **3729** | **77,7%** |

> Đọc cột vector hỗ trợ trước: $C$ càng lớn thì lề càng hẹp, càng ít điểm nằm trong lề, nên số vector hỗ trợ giảm từ 93,9% xuống 59,0%. Ở $C=0{,}01$ thì gần như cả tập huấn luyện là vector hỗ trợ, và mô hình lúc ấy chỉ đoán được 0,3482.

🧠 **Phân tích chi tiết & Bản chất:** số vector hỗ trợ là một "phong vũ biểu" cho độ rộng lề. Lề rộng (C nhỏ) "nuốt" nhiều điểm vào trong nó — mọi điểm trong lề đều có $\xi_i>0$ nên đều là vector hỗ trợ (ở lề mềm, định nghĩa mở rộng ra cả điểm vi phạm). Lề hẹp (C lớn) chỉ chạm rất ít điểm.

> Con số 0,3482 ấy không phải một điểm kém bất kỳ. Nó bằng chằn chặn điểm của bài nộp gán nhãn 1 cho mọi câu, và kiểm lại thì đúng là mô hình chỉ in ra một nhãn duy nhất. Vi phạm quá rẻ nên nghiệm tối ưu là bỏ cuộc: chịu sai một nửa còn hơn bóp lề. Khi thấy điểm của mình trùng khít điểm của mô hình sàn, hãy in thử phân bố nhãn dự đoán trước khi đi tìm lỗi ở chỗ khác.

🧠 **Vì sao 0,3482 "vừa hay" — kỹ năng chẩn đoán mô hình sàn:** "Mô hình sàn" (baseline, ví dụ luôn đoán nhãn phổ biến nhất) là điểm neo để biết mô hình có *thật sự học được gì* hay không. Khi $C$ quá nhỏ, tiền phạt sai gần bằng 0, nên nghiệm tối ưu đúng đắn về toán học (không phải lỗi code) là chọn $w\approx 0$, lề vô cùng rộng, chấp nhận đoán sai gần hết. Nếu điểm số của bạn trùng khít một mô hình "đoán mù", đừng vội soát code load dữ liệu — hãy kiểm phân bố nhãn dự đoán trước.

> **Dòng cuối đi ngược lại, và tôi không có lời giải thích chắc chắn.**
> Từ $C=10$ lên $C=100$, tỉ lệ vector hỗ trợ tăng trở lại lên 77,7%, ngược hẳn xu hướng của năm dòng trên. Điểm kiểm định cũng lên, thành cao nhất bảng.
>
> Tôi không có một lời giải thích tôi dám in ra. Giả thuyết dễ chịu nhất là bài toán ở $C$ lớn khó hội tụ hơn nên nghiệm chưa phải nghiệm tối ưu, nhưng tôi chưa kiểm được điều đó và sẽ không viết một cơ chế nghe hay để lấp chỗ trống.
>
> Điều nên rút ra: chênh lệch giữa 0,7018 và 0,7077 là 0,0058, nhỏ hơn dải nhiễu 0,0177 của buổi 07. Nghĩa là bảng này không chứng minh $C=100$ tốt hơn $C=10$. Nó chỉ chứng minh $C \le 0{,}1$ là hỏng.

🧠 **Đây là bài học quý nhất của mục 2.4, và nó không nằm ở công thức:**
- Sự trung thực khoa học ở đây đáng học hơn cả kỹ thuật SVM: khi dữ liệu không khớp giả thuyết đẹp, tác giả không "chế" ra một cơ chế nghe hợp lý để lấp khoảng trống, mà để ngỏ kèm một giả thuyết kiểm được (hội tụ số học) và lời thú nhận "chưa kiểm". Đây là tinh thần của bài tập 3 ở mục 4.
- **Dải nhiễu (noise band) là gì và vì sao quan trọng hơn bản thân con số:** huấn luyện lại cùng mô hình nhiều lần (đổi seed, đổi cách chia tập) thì điểm số dao động ngay cả khi không đổi thuật toán — dải nhiễu 0,0177 (từ buổi 07) là biên độ dao động tự nhiên ấy. Chênh lệch 0,0058 — nhỏ hơn dải nhiễu — không đủ để khẳng định "tốt hơn", chỉ là may rủi thống kê. Đây là lý do các báo cáo khoa học nghiêm túc luôn kèm độ lệch chuẩn/khoảng tin cậy bên cạnh điểm trung bình.
- Ngược lại, kết luận "$C\le 0{,}1$ là hỏng" vượt xa dải nhiễu (0,3482 và 0,6137 cách điểm ở $C=1$ rất xa) — nên là kết luận đáng tin, khác hẳn việc so 0,7018 và 0,7077.

---

### 2.5 Kernel: đổi hình dạng ranh giới mà không đổi thuật toán

> Thủ thuật kernel thay tích vô hướng $x\cdot x'$ bằng một hàm $K(x,x')$ đóng vai trò tích vô hướng trong một không gian khác, thường là không gian nhiều chiều hơn. Ranh giới vẫn là siêu phẳng ở không gian ấy, và cong khi nhìn từ không gian gốc. Cái hay là bạn không bao giờ phải dựng không gian ấy ra.

🧠 **Phân tích chi tiết & Bản chất:**
- **Vì sao cần kernel:** nhiều bài toán thật không tách được bằng đường thẳng — ví dụ kinh điển là hai lớp xếp thành hai vòng tròn đồng tâm (bài tập 4). Nhưng nếu "nâng" mỗi điểm $(x_1,x_2)$ lên 3 chiều bằng $\phi(x_1,x_2)=(x_1,x_2,x_1^2+x_2^2)$, hai vòng tròn (khác bán kính) nằm ở hai "độ cao" khác nhau theo trục thứ ba, và một mặt phẳng nằm ngang tách được chúng dễ dàng. Chiếu ngược xuống 2D, ranh giới trông cong — đó là một đường tròn.
- **Kernel trick tiết kiệm được gì:** biến đổi trực tiếp từng điểm sang không gian mới có thể bùng nổ chi phí khi không gian đó có hàng nghìn, thậm chí vô hạn chiều (như RBF). Toàn bộ thuật toán SVM chỉ cần biết *tích vô hướng* giữa các cặp điểm, không cần toạ độ cụ thể trong không gian mới. Hàm $K(x,x')$ tính thẳng ra tích vô hướng ấy mà không cần dựng không gian đó — ví dụ $K(x,x')=(x\cdot x'+c)^2$ cho kết quả tương đương không gian đặc trưng chứa mọi tích của hai đặc trưng gốc, chỉ bằng vài phép nhân trên không gian gốc.

| Kernel, C = 4 | Tập đã học | Kiểm định | Vector hỗ trợ |
|---|---:|---:|---:|
| tuyến tính | 0,7131 | 0,6989 | 2988 |
| **đa thức bậc 2** | **0,9566** | **0,7353** | **3294** |
| đa thức bậc 3 | 0,9857 | 0,6892 | 4121 |
| RBF | 0,9765 | 0,7327 | 3901 |
| sigmoid | 0,5238 | 0,6615 | 2809 |

> Kernel đa thức bậc 2 được 0,7353, hơn tuyến tính 0,0365, tức gấp đôi dải nhiễu nên là chênh lệch thật. Nó cũng vượt hồi quy logistic của buổi 05 (0,6888) một khoảng rõ rệt, nhưng vẫn thua boosting của buổi 08 (0,7961).
>
> Bậc 3 thì học thuộc giỏi hơn bậc 2 (0,9857 so với 0,9566) và kiểm định kém hơn 0,0461. Đây đúng là hình ảnh quá khớp mà buổi 07 mô tả, lần này do sức chứa của kernel chứ không phải do số đặc trưng.
>
> Dòng sigmoid đáng chú ý theo hướng ngược: điểm huấn luyện 0,5238 thấp hơn điểm kiểm định 0,6615. Khi thấy cảnh ấy thì đừng mừng, hãy nghi: đó là dấu hiệu mô hình chưa khớp nổi dữ liệu chứ không phải nó tổng quát giỏi.

🧠 **Phân tích chi tiết & Bản chất:**
- **Đa thức bậc 2 thắng thật** vì chênh lệch (0,0365) lớn hơn hẳn dải nhiễu 0,0177 — cùng tiêu chuẩn đã học ở mục 2.4.
- **Bậc 3 là quá khớp giáo khoa:** điểm huấn luyện tăng, điểm kiểm định giảm. Khoảng cách giữa hai cột này ("khoảng hở quá khớp") đo trực tiếp mức độ mô hình "học thuộc lòng" thay vì "hiểu quy luật". Không gian đặc trưng bậc 3 giàu chiều hơn bậc 2 rất nhiều, đủ "chỗ" để vẽ ranh giới ngoằn ngoèo len lỏi qua từng điểm huấn luyện, kể cả điểm nhiễu.
- **Sigmoid là dưới khớp (underfitting):** điểm huấn luyện còn thấp hơn điểm kiểm định — dấu hiệu mô hình quá đơn giản (hoặc kernel không hợp lệ theo nghĩa Mercer, hành xử thất thường) đến mức không "học thuộc" nổi cả tập huấn luyện; điểm kiểm định cao hơn chỉ là may rủi trên mẫu nhỏ. Quy tắc chung: điểm kiểm định không thể phản ánh "tổng quát hoá tốt" nếu mô hình chưa khớp nổi cả dữ liệu đã thấy.

> **Trong sáu tiếng thi thì thời gian là một ràng buộc thật.**
> Mỗi dòng trong hai bảng trên tốn từ 14 tới 36 giây. Quét cả hai bảng là hơn bốn phút, và đó mới chỉ là hai tham số.
>
> LinearSVC giải cùng bài toán tuyến tính bằng thuật toán khác: hơn hai mươi giây rút xuống 0,2 giây, mà được 0,6903 so với 0,6898 của `SVC(kernel="linear", C=1)`. Chênh lệch 0,0005, tức là không phân biệt được.
>
> Quy tắc: dò tham số bằng LinearSVC, chỉ gọi SVC khi thật sự cần kernel.

🧠 **Vì sao hai công cụ cho gần cùng kết quả lại khác tốc độ hàng trăm lần:** `SVC(kernel="linear")` giải bài toán đối ngẫu tổng quát — có thể cắm bất kỳ kernel nào, kể cả kernel làm không gian vô hạn chiều như RBF — nên không tận dụng được cấu trúc đặc biệt của trường hợp tuyến tính. `LinearSVC` được viết chuyên biệt cho đúng bài toán tuyến tính, dùng thuật toán tối ưu khác tận dụng việc không cần kernel. Đây là minh hoạ cho nguyên tắc chung: công cụ càng tổng quát, càng trả giá về tốc độ cho trường hợp đặc biệt (dù phổ biến). **Mẹo:** dò siêu tham số $C$ bằng `LinearSVC` trước để thu hẹp phạm vi, chỉ chuyển sang `SVC` khi cần kernel phi tuyến hoặc các thuộc tính riêng như `predict_proba`.

---

## 3. Bài tập mẫu

> **Đề.** Cho $w=(0{,}4;-0{,}7)$ và $b=0{,}1$. Điểm $x=(2,1)$ thuộc lớp nào, cách siêu phẳng bao xa, và lề rộng bao nhiêu?
>
> **Bước 1, dấu.**
> $$w\cdot x+b = 0{,}4\cdot 2 + (-0{,}7)\cdot 1 + 0{,}1 = 0{,}8-0{,}7+0{,}1 = 0{,}2 > 0 \Rightarrow \text{lớp} +1.$$
>
> **Bước 2, khoảng cách.** $\lVert w\rVert = \sqrt{0{,}16+0{,}49}=\sqrt{0{,}65}\approx 0{,}806226$, nên
> $$d = \frac{|0{,}2|}{0{,}806226} \approx 0{,}248069.$$
>
> **Bước 3, lề.** $2/\lVert w\rVert \approx 2{,}480695$.
>
> Ba con số ấy trả lời ba câu hỏi khác nhau, và đề thi hay trộn chúng vào một câu để xem thí sinh có phân biệt được không.

```python
import numpy as np
w, b, x = np.array([0.4, -0.7]), 0.1, np.array([2.0, 1.0])
f = float(np.dot(w, x) + b)
print("f = %.4f, lop %s" % (f, "+1" if f > 0 else "-1"))
print("khoang cach = %.6f" % (abs(f) / np.linalg.norm(w)))
print("be rong le = %.6f" % (2.0 / np.linalg.norm(w)))
```

🧠 **Phân tích chi tiết & Bản chất — cách làm nhanh không máy tính:**
1. **Dấu:** chỉ cộng trừ nhân, không cần căn bậc hai. Làm trước vì rẻ nhất và trả lời ngay "thuộc lớp nào".
2. **Khoảng cách:** cần $\lVert w\rVert=\sqrt{w_1^2+w_2^2}$ — bước duy nhất cần khai căn. Mẹo nhẩm nhanh: $\sqrt{0{,}65}$ nằm giữa $\sqrt{0{,}64}=0{,}8$ và $\sqrt{0{,}81}=0{,}9$, gần $0,8$ hơn — ước lượng $0,806$ hợp lý chỉ bằng nhẩm.
3. **Lề:** nhân đôi nghịch đảo của $\lVert w\rVert$ đã tính ở bước 2, không tính lại từ đầu — nên tính khoảng cách trước, lề sau.

**Bẫy thường gặp:** nhầm bước 2 và 3 vì cả hai chia cho $\lVert w\rVert$. Ghi nhớ: khoảng cách dùng giá trị cụ thể tại điểm $x$ ($|w\cdot x+b|$) ở tử số — phụ thuộc điểm đang xét. Lề không phụ thuộc điểm nào, tử số luôn là hằng số 2 — lề là thuộc tính của *mô hình*, không phải của một điểm dữ liệu.

> **Một điểm rơi đúng lên siêu phẳng thì thuộc lớp nào?**
>
> Trong bộ hai mươi bài của buổi này có đúng một câu mà $w\cdot x+b=0$ chằn chặn: $w=(0{,}5;0{,}5;-1)$, $b=0$, $x=(2,2,2)$.
>
> Toán học không trả lời được câu ấy, vì điểm nằm trên chính ranh giới. Thư viện thì phải trả lời, và scikit-learn xếp nó vào lớp âm: ngưỡng của nó là $f>0$ chứ không phải $f\ge 0$. Tôi đã kiểm điều này bằng một mô hình có $f$ đúng bằng 0 tại điểm ấy chứ không chép lại từ tài liệu.
>
> Bài học không phải là con số, mà là: khi kết quả phụ thuộc vào quy ước ngưỡng, hãy tìm ra quy ước ấy bằng thí nghiệm, đừng đoán.

🧠 **Phân tích chi tiết & Bản chất:**
- Xác nhận nhanh: $0{,}5\cdot 2+0{,}5\cdot 2-1\cdot 2 = 1+1-2=0$ — đúng, điểm nằm chằn chặn trên siêu phẳng.
- Tập $\{x : w\cdot x+b=0\}$ chính là ranh giới, và một hàm phân loại nhị phân buộc phải gán nó cho *một trong hai* phía — không có "phía thứ ba". Đây là quyết định kỹ thuật của người viết thư viện, không phải định lý toán học. Bài học phương pháp luận: **đừng đoán một quy ước — hãy đo nó.** Kỹ thuật gợi ý (dựng mô hình có $f$ đúng bằng 0 rồi gọi `predict`) áp dụng được cho bất kỳ hành vi không tài liệu hoá rõ ràng nào ở điểm biên.
- Đây chính xác là loại câu hỏi bẫy hay gặp: nếu đề cho điểm có $f(x)=0$ và hỏi "lớp nào theo scikit-learn", câu trả lời dựa trên quy ước cụ thể của thư viện (lớp âm, vì ngưỡng $f>0$), không phải một suy luận toán học trừu tượng.

---

## 4. Bài tập tự làm

### Bài tập 1 — Hai mươi bài tính tay

> File `bai-tap-tinh-tay.py` trong thư mục buổi này in ra đề gồm mười câu hỏi dấu, năm câu khoảng cách, ba câu bề rộng lề và hai câu vector hỗ trợ.

```
# print the worksheet, then the key, then check the key itself
# python bai-tap-tinh-tay.py
# python bai-tap-tinh-tay.py --dap-an
# python bai-tap-tinh-tay.py --kiem
```

**Cổng kiểm**
> Làm hết trong 20 phút, không dùng máy tính, rồi mới mở đáp án. Sai một câu là chưa qua.
>
> Chế độ `--kiem` không chấm bài bạn, nó chấm đáp án: đối chiếu từng câu bằng một đường tính khác, và kiểm cả hai điều kiện dễ quên là đề phải có đủ hai lớp và phải có đúng một câu rơi lên siêu phẳng.

🧠 **Gợi ý luyện tập:** 20 phút cho 20 câu là 1 phút/câu — đúng nhịp độ cần có trong phòng thi thật. Làm theo đúng thứ tự đã dạy ở mục 3: dấu trước (rẻ nhất), rồi khoảng cách, rồi lề (dùng lại $\lVert w\rVert$ đã tính). Với câu vector hỗ trợ, nhớ tiêu chí mục 2.3: một điểm là vector hỗ trợ khi và chỉ khi thoả đúng $yf(x)=1$ (lề cứng) hoặc có $\xi_i>0$ (lề mềm).

### Bài tập 2 — Dựng lại bảng C

> Sáu dòng, bốn cột, kể cả cột vector hỗ trợ.

**Cổng kiểm**
> Khớp tới chữ số thập phân thứ tư. Rồi trả lời: tỉ lệ vector hỗ trợ ở $C=0{,}01$ là 93,9% nói lên điều gì về lề lúc ấy?

🧠 **Gợi ý luyện tập:** câu hỏi phụ đang kiểm liên hệ ở mục 2.4 — tỉ lệ vector hỗ trợ cao nghĩa là lề rất rộng, gần như "nuốt" trọn tập huấn luyện — dấu hiệu mô hình gần như bỏ cuộc, chấp nhận vi phạm tràn lan vì $C$ quá nhỏ khiến vi phạm gần như miễn phí.

### Bài tập 3 — Kiểm lại giả thuyết mà tôi bỏ ngỏ

> Mục 2.4 để ngỏ vì sao $C=100$ lại có nhiều vector hỗ trợ hơn $C=10$. Hãy kiểm giả thuyết hội tụ: chạy lại $C=100$ với `max_iter` lớn hơn hẳn và `tol` nhỏ hơn hẳn, xem số vector hỗ trợ có đổi không.

**Cổng kiểm**
> Trả lời bằng số, và chấp nhận cả hai kết cục. Nếu số vector hỗ trợ không đổi thì giả thuyết của tôi sai, và bạn vừa loại được một cách giải thích. Đó cũng là một kết quả.

🧠 **Gợi ý luyện tập:** hiếm hoi bài tập mà "không tìm ra hiệu ứng" vẫn là hoàn thành tốt — mục tiêu là kiểm định giả thuyết, không phải xác nhận nó. Nếu tăng `max_iter`, giảm `tol` mà số vector hỗ trợ không đổi, bạn đã loại trừ nguyên nhân "hội tụ chưa xong" — câu hỏi thật sự vẫn còn mở, y như tác giả đã thừa nhận ở mục 2.4.

### Bài tập 4 — Kernel nào cho ranh giới nào

> Dựng 200 điểm hai chiều xếp thành hai vòng tròn đồng tâm. Huấn luyện SVM tuyến tính và SVM RBF, vẽ ranh giới quyết định của cả hai.

**Cổng kiểm**
> Tuyến tính không thể tách hai vòng tròn, và hình vẽ phải cho thấy điều đó chứ không phải chỉ có điểm số nói. Ghi lại macro-F1 của cả hai.

🧠 **Gợi ý luyện tập:** minh hoạ thực nghiệm cho ví dụ "nâng chiều" ở mục 2.5. Hai vòng tròn đồng tâm không tách được bằng đường thẳng trong 2D, nhưng RBF ánh xạ ngầm dữ liệu sang không gian mà việc tách trở nên khả thi. Khi vẽ, ranh giới tuyến tính sẽ gần như vô nghĩa (đường thẳng cắt ngang cả hai vòng), còn RBF cho đường cong khép kín bám theo vòng tròn trong.

### Bài tập 5 — Lề chịu được bao nhiêu nhiễu

> Lấy ví dụ tám điểm ở mục 2.3. Thêm nhiễu Gauss độ lệch chuẩn $\sigma$ vào tất cả các điểm, huấn luyện lại, và tăng dần $\sigma$ cho tới khi nghiệm đổi hẳn.

**Cổng kiểm**
> Tìm ngưỡng $\sigma$ ấy và so với bề rộng lề bằng 2. Đây là cách kiểm bằng thực nghiệm câu khẳng định ở mục 2.2: lề chính là lượng nhiễu mà nghiệm chịu được.

🧠 **Gợi ý luyện tập:** đóng vòng lặp với ẩn dụ "đỗ xe giữa khoảng trống" ở mục 2.2. Nếu lý thuyết đúng, ngưỡng $\sigma$ mà nghiệm bắt đầu đổi phải cùng bậc độ lớn với nửa bề rộng lề (xấp xỉ 1, vì lề toàn phần là 2) — khoảng cách từ vector hỗ trợ tới mặt phân chia. Nếu số đo lệch quá xa, đáng nghi cách thêm nhiễu (nhiễu vào cả tám điểm cùng lúc có thể dịch chuyển cả "trung điểm tối ưu", không chỉ kiểm độ nhạy của một vector hỗ trợ).

---

## Chuẩn bị cho buổi sau

> Buổi 10 rời hẳn học có giám sát: K-Means, PCA, t-SNE, DBSCAN. Mang theo câu hỏi: khi không có nhãn thì lấy gì làm thước đo đúng sai?

🧠 **Cầu nối sang buổi sau:** toàn bộ buổi 09 xoay quanh tối ưu một hàm mục tiêu có "đáp án đúng" rõ ràng ở mỗi điểm — nhãn $y_i$. Buổi 10 rút mất chiếc neo ấy: không có nhãn để so sánh, "đúng" và "sai" không còn là khái niệm có sẵn. Câu hỏi đáng suy nghĩ trước khi tới lớp: không có nhãn để tính độ chính xác, bạn dùng gì để nói mô hình phân cụm này "tốt hơn" mô hình phân cụm kia? *(Gợi ý nhẹ: nghĩ về những đại lượng chỉ cần biết vị trí các điểm, không cần biết nhãn — ví dụ khoảng cách trong cụm so với khoảng cách giữa các cụm.)*

---

*Buổi 09 — SVM và lề · TS. Đỗ Phúc Hảo · Luyện Olympic Trí tuệ nhân tạo. Bản trình bày này giữ nguyên toàn bộ nội dung gốc (khối trích dẫn) và bổ sung phần giải thích, ẩn dụ, ví dụ (khối 🧠) để đào sâu kiến thức.*
