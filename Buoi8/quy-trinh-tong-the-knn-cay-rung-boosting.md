# Quy trình tổng thể: KNN, Cây quyết định, Rừng ngẫu nhiên, Boosting

## 0. Trả lời câu hỏi cốt lõi: có giống quy trình logistic không?

**Giống ở khung sườn, khác ở 3 bước.** Cả 5 mô hình (logistic, KNN, cây, rừng, boosting) đều đi qua đúng
8 bước chung: tải dữ liệu → chia tập → tiền xử lý → huấn luyện → dự đoán → đánh giá → tinh chỉnh siêu
tham số → đảm bảo tái lập. Cái khác nhau nằm ở:

| Bước | Logistic | KNN | Cây / Rừng / Boosting |
|---|---|---|---|
| Cần chuẩn hoá (scaling)? | **Có, gần như bắt buộc** (nếu dùng regularization) | **Có thể cần**, tuỳ dữ liệu — phải đo mới biết (xem buổi 08, mục 2.1) | **Không cần** — cây chia theo ngưỡng trên từng cột, đơn vị đo không ảnh hưởng |
| Siêu tham số chính | `C` (độ mạnh regularization) | `k` (số hàng xóm) | `max_depth`/`n_estimators`/`learning_rate` |
| Diễn giải được? | Có (hệ số hồi quy) | Không | Có (cây đơn) / hạn chế (rừng, boosting) |
| Độ nhạy với nhiễu/outlier | Trung bình | Cao (dựa hoàn toàn vào khoảng cách) | Cây đơn: cao / Rừng, boosting: thấp hơn nhờ tổ hợp |
| Cần `n_jobs=1` để tái lập? | Không | Không | **Có, với Rừng** (xem buổi 08, mục 3) |

Nói ngắn gọn: **quy trình không đổi, nhưng bước tiền xử lý và bước chọn siêu tham số phải thiết kế lại
theo từng họ mô hình**, vì bản chất toán học đằng sau chúng khác nhau (khoảng cách hình học với KNN, phép
chia ngưỡng với cây/rừng/boosting, hàm tuyến tính với logistic).

---

## 1. Quy trình chung — 8 bước, áp dụng cho mọi mô hình

```
Bước 1  Tải & khảo sát dữ liệu       (EDA: nhìn phân phối nhãn, giá trị thiếu, kiểu cột)
Bước 2  Chia tập                      (train_test_split hoặc K-fold CV, ghim random_state)
Bước 3  Feature engineering           (biến đổi văn bản/ảnh/bảng thành số)
Bước 4  Tiền xử lý riêng theo mô hình (scaling cho KNN, KHÔNG cần cho cây/rừng/boosting)
Bước 5  Khởi tạo mô hình + siêu tham số ban đầu
Bước 6  Huấn luyện                    (.fit)
Bước 7  Dự đoán                       (.predict / .predict_proba)
Bước 8  Đánh giá                      (metric phù hợp bài toán, confusion matrix)
Bước 9  Tinh chỉnh siêu tham số        (cross-validation, GridSearchCV/RandomizedSearchCV)
Bước 10 Đảm bảo tái lập & chốt kết quả (random_state, n_jobs=1, so với dải nhiễu)
```

Bốn mô hình của buổi 08 và logistic của buổi 07 đều đi qua đủ 10 bước này — khác nhau ở **nội dung** của
bước 4, 5, 9, 10.

---

## 2. Chi tiết riêng từng mô hình

### 2.1 KNN (`KNeighborsClassifier`)

```python
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

# Bước 4: tiền xử lý — LUÔN thử cả hai (có/không chuẩn hoá), đừng mặc định
# một trong hai là đúng. Đo trên chính dữ liệu của bạn (xem buổi 08, 2.1).
pipe_knn = Pipeline([
    ("scaler", StandardScaler()),      # bỏ dòng này nếu đo thấy không cần
    ("knn", KNeighborsClassifier(n_neighbors=5)),
])

# Bước 5-6: huấn luyện
pipe_knn.fit(Xh, yh)

# Bước 7: dự đoán
yk_du_doan = pipe_knn.predict(Xk)

# Bước 9: tinh chỉnh k — quét một dải, đo trên K-fold CV chứ không phải
# một lần chia (xem buổi 08, bài tập 3 — dùng đúng kỹ thuật này)
```

Lưu ý đặc thù:
- **Dùng `Pipeline`** (không tự tay `fit`/`transform` scaler) để tránh rò rỉ dữ liệu (data leakage) khi
  làm cross-validation — `Pipeline` tự đảm bảo scaler chỉ `fit` trên phần tập học của từng fold.
- KNN không có bước "huấn luyện" thật sự (`.fit()` chỉ lưu dữ liệu) — chi phí tính toán dồn hết vào lúc
  `.predict()`, nên nếu tập dữ liệu lớn, `.predict()` có thể chậm hơn nhiều mô hình khác dù `.fit()` cực
  nhanh.
- Không có khái niệm "feature importance" tự nhiên cho KNN — nếu cần, phải dùng permutation importance
  thủ công (`sklearn.inspection.permutation_importance`).

### 2.2 Cây quyết định (`DecisionTreeClassifier`)

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Bước 4: KHÔNG cần chuẩn hoá — cây chia theo ngưỡng trên từng cột riêng lẻ,
# đổi đơn vị đo một cột không ảnh hưởng tới cột nào khác.
cay = DecisionTreeClassifier(
    max_depth=None,          # hoặc giới hạn để tránh quá khớp (xem buổi 08, 2.3)
    min_samples_leaf=1,      # cách giới hạn quá khớp thay thế, đáng thử song song
    criterion="gini",        # hoặc "entropy" — xếp hạng phép chia gần như giống nhau
    random_state=0,
)
cay.fit(Xh, yh)

# Bước 8 mở rộng: cây cho phép "đọc luật" trực tiếp — hữu ích để giải thích
# mô hình, không chỉ để dự đoán.
print(cay.feature_importances_)          # độ quan trọng theo impurity
# plot_tree(cay, feature_names=ten_cot, class_names=["0","1"], filled=True)
```

Lưu ý đặc thù:
- Siêu tham số kiểm soát quá khớp có **nhiều lựa chọn độc lập**: `max_depth`, `min_samples_leaf`,
  `min_samples_split`, `max_leaf_nodes`, `ccp_alpha` (cost-complexity pruning). Buổi 08 chỉ demo
  `max_depth`; thực hành nên thử thêm `min_samples_leaf` (đã có gợi ý ở bài tập luyện thêm số 4).
- Đường cong độ sâu **không đơn điệu** trên tập kiểm định — luôn dùng cross-validation (bước 9) trước khi
  chốt một độ sâu, không tin vào một lần chia duy nhất.
- `feature_importances_` mặc định (impurity-based) **thiên vị cột nhiều giá trị khác nhau** — luôn đối
  chiếu với `permutation_importance` trước khi dùng để loại bỏ cột (xem buổi 08, mục 2.6).

### 2.3 Rừng ngẫu nhiên (`RandomForestClassifier`)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance

rung = RandomForestClassifier(
    n_estimators=300,        # đủ để bão hoà; hơn nữa chỉ tốn thời gian chạy
    max_features="sqrt",     # nguồn ngẫu nhiên thứ hai, giảm tương quan giữa các cây
    random_state=0,
    n_jobs=1,                 # QUAN TRỌNG: giữ =1 để kết quả tái lập được y hệt
)                              # giữa các máy (xem buổi 08, mục 3 — vấn đề cộng
                               # dấu chấm động đa luồng)
rung.fit(Xh, yh)

# Bước 8 mở rộng: luôn tính CẢ HAI loại độ quan trọng, không chỉ một
impurity_imp = rung.feature_importances_
perm = permutation_importance(rung, Xk, yk, n_repeats=10, random_state=0)
perm_imp = perm.importances_mean
```

Lưu ý đặc thù:
- `n_jobs=1` không phải tuỳ chọn — đó là điều kiện **bắt buộc nếu cần kết quả tái lập được tới 4 chữ số
  thập phân**, đổi lấy thời gian chạy lâu hơn (đã đo và giải thích trong buổi 08).
- Số cây (`n_estimators`) nên được xác định bằng cách quan sát điểm bão hoà (như bảng ở mục 2.4 buổi 08),
  không cần grid-search tốn kém cho riêng siêu tham số này.
- `max_features` là siêu tham số dễ bị bỏ quên nhưng ảnh hưởng trực tiếp tới độ tương quan giữa các cây —
  đáng đưa vào vòng tinh chỉnh (bước 9), không chỉ dùng giá trị mặc định.

### 2.4 Boosting (`HistGradientBoostingClassifier` / XGBoost / CatBoost)

```python
from sklearn.ensemble import HistGradientBoostingClassifier

boost = HistGradientBoostingClassifier(
    max_iter=200,             # số cây tuần tự (tương đương n_estimators)
    learning_rate=0.1,        # càng nhỏ càng cần nhiều cây hơn nhưng ổn định hơn
    random_state=0,
    early_stopping=True,      # dừng sớm nếu tập validation nội bộ không cải thiện
)
boost.fit(Xh, yh)
```

Lưu ý đặc thù:
- Boosting **luôn cần theo dõi quá khớp** chặt hơn cây/rừng, vì mỗi vòng cố tình sửa lỗi vòng trước —
  chạy quá lâu (`max_iter` lớn, `learning_rate` lớn) sẽ bắt đầu học cả nhiễu. Dùng `early_stopping=True`
  hoặc tự vẽ đường cong theo `max_iter` như bài luyện thêm số 3 (buổi trước).
- Thời gian huấn luyện chậm hơn hẳn cây/rừng do tính tuần tự, không song song hoá được giữa các cây — cần
  tính vào ngân sách thời gian khi thi.
- Nếu dùng XGBoost/CatBoost (có trong phòng thi) thay vì `HistGradientBoostingClassifier`, cú pháp
  `.fit()`/`.predict()` gần như giống hệt (đều theo chuẩn scikit-learn), chỉ khác tên siêu tham số
  (`n_estimators` thay vì `max_iter`, v.v.) — luôn tra tài liệu thư viện cụ thể trước khi vào thi nếu chưa
  quen.

---

## 3. Khung code tổng quát dùng chung cho cả 5 mô hình

```python
import time
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

RANDOM_STATE = 0

def f1m(a, b):
    return f1_score(a, b, average="macro", labels=[0, 1], zero_division=0)

def quy_trinh_chuan(X, y, mo_hinh, can_chuan_hoa=False, test_size=0.2):
    """Chay du 10 buoc cho MOT mo hinh, tra ve dict ket qua."""
    # Buoc 2: chia tap
    Xh, Xk, yh, yk = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y)

    # Buoc 4-5: dong goi tien xu ly + mo hinh trong 1 Pipeline
    buoc = [("model", mo_hinh)]
    if can_chuan_hoa:
        buoc.insert(0, ("scaler", StandardScaler()))
    pipe = Pipeline(buoc)

    # Buoc 6: huan luyen, co do thoi gian
    t0 = time.perf_counter()
    pipe.fit(Xh, yh)
    giay = time.perf_counter() - t0

    # Buoc 7: du doan
    yh_du_doan = pipe.predict(Xh)
    yk_du_doan = pipe.predict(Xk)

    # Buoc 8: danh gia
    ket_qua = {
        "f1_hoc": f1m(yh, yh_du_doan),
        "f1_kiem": f1m(yk, yk_du_doan),
        "giay": giay,
        "ma_tran_nham_lan": confusion_matrix(yk, yk_du_doan),
    }

    # Buoc 9: tinh chinh (vi du toi thieu — thay bang GridSearchCV khi can
    # quet nhieu sieu tham so cung luc)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    diem_cv = cross_val_score(pipe, X, y, cv=cv, scoring="f1_macro")
    ket_qua["cv_trung_binh"] = diem_cv.mean()
    ket_qua["cv_do_lech_chuan"] = diem_cv.std(ddof=1)

    return ket_qua
```

Gọi hàm này cho cả 5 mô hình sẽ cho ra đúng dạng bảng so sánh như Bảng A/B trong buổi 08 — chỉ cần đổi
tham số `mo_hinh` và `can_chuan_hoa`.

---

## 4. Checklist trước khi chốt kết quả (dùng cho cả thi lẫn làm dự án)

- [ ] Đã ghim `random_state` ở **mọi** nơi có tham số ngẫu nhiên (split, model, CV)?
- [ ] Với `RandomForestClassifier`: đã đặt `n_jobs=1` nếu cần kết quả tái lập chính xác?
- [ ] Đã thử **cả hai** phương án chuẩn hoá cho KNN và đo, thay vì mặc định theo "quy tắc chung"?
- [ ] Mọi so sánh điểm số đã đối chiếu với **dải nhiễu** (đo bằng cách đổi seed hoặc CV), chưa vội kết
      luận "mô hình A tốt hơn B" khi chênh lệch nhỏ hơn dải nhiễu?
- [ ] Đường cong theo siêu tham số (độ sâu, số cây, learning rate) đã được đo bằng **cross-validation**,
      không chỉ một lần chia?
- [ ] Nếu dùng `feature_importances_`, đã đối chiếu với `permutation_importance` trước khi kết luận cột
      nào quan trọng?
- [ ] Thời gian chạy đã nằm trong giới hạn cho phép của đề thi/hệ thống chấm?
- [ ] Điểm số cuối cùng đã được tính trên tập kiểm định/kiểm định chéo, không phải tập huấn luyện?

---

*Tài liệu tổng hợp quy trình chuẩn cho KNN, cây quyết định, rừng ngẫu nhiên, boosting — đối chiếu với quy
trình hồi quy logistic, dựa trên nội dung Buổi 07-08 khoá Luyện Olympic Trí tuệ nhân tạo.*
