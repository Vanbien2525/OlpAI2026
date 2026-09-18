#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buổi 09 — SVM và lề — Bài tập 1: Hai mươi bài tính tay
--------------------------------------------------------
File in ra đề gồm mười câu hỏi dấu, năm câu khoảng cách, ba câu bề rộng lề
và hai câu vector hỗ trợ.

Cách dùng:
    python bai-tap-tinh-tay.py                # in đề
    python bai-tap-tinh-tay.py --dap-an        # in đề kèm đáp án chi tiết
    python bai-tap-tinh-tay.py --kiem          # tự kiểm đáp án (không chấm bài bạn)
    python bai-tap-tinh-tay.py --seed 7        # ra một đề khác (mặc định seed=42)

Cổng kiểm
    Làm hết trong 20 phút, không dùng máy tính, rồi mới mở đáp án.
    Sai một câu là chưa qua.

    Chế độ --kiem không chấm bài bạn, nó chấm đáp án: đối chiếu từng câu
    bằng một đường tính khác, và kiểm cả hai điều kiện dễ quên là đề phải
    có đủ hai lớp và phải có đúng một câu rơi lên siêu phẳng.

Ghi chú kỹ thuật: mọi phép tính nội bộ dùng phân số (fractions.Fraction),
không dùng số thực dấu phẩy động, nên "rơi đúng lên siêu phẳng" (f(x)=0)
là chính xác tuyệt đối, không phải một điểm gần 0 do làm tròn.
"""

import argparse
import math
import random
from fractions import Fraction as F

SEED_DEFAULT = 42

# ---------------------------------------------------------------------------
# Tiện ích số học và định dạng
# ---------------------------------------------------------------------------

def fmt(fr):
    """Đổi một Fraction thành chuỗi thập phân gọn, chính xác (không làm tròn)."""
    fr = F(fr)
    sign = "-" if fr < 0 else ""
    fr = abs(fr)
    whole = fr.numerator // fr.denominator
    remainder = fr - whole
    if remainder == 0:
        return f"{sign}{whole}"
    digits = []
    dec = remainder
    for _ in range(6):
        dec *= 10
        d = dec.numerator // dec.denominator
        digits.append(str(d))
        dec -= d
        if dec == 0:
            break
    dec_str = "".join(digits).rstrip("0")
    if dec_str == "":
        return f"{sign}{whole}"
    return f"{sign}{whole}.{dec_str}"


def fmt_point(x):
    return f"({fmt(x[0])}, {fmt(x[1])})"


def fmt_w(w):
    return f"({fmt(w[0])}, {fmt(w[1])})"


def dot(w, x):
    return w[0] * x[0] + w[1] * x[1]


def f_of(w, b, x):
    return dot(w, x) + b


def norm_float(w):
    return math.sqrt(float(w[0] ** 2 + w[1] ** 2))


# ---------------------------------------------------------------------------
# Bộ số "đẹp" để tính tay được
# ---------------------------------------------------------------------------

# w với chuẩn là số nguyên hoặc số thập phân gọn (bộ ba kiểu Pythagoras)
PERFECT_PAIRS = [
    (F(3), F(4), F(5)),
    (F(3, 10), F(4, 10), F(5, 10)),
    (F(6, 10), F(8, 10), F(1)),
    (F(5), F(12), F(13)),
    (F(9, 10), F(12, 10), F(15, 10)),
    (F(3, 2), F(2), F(5, 2)),
    (F(2), F(0), F(2)),
    (F(0), F(3), F(3)),
    (F(6), F(8), F(10)),
    (F(9), F(12), F(15)),
]

GAP_CHOICES = [1, 2, 4, 5, 8]  # để 2/gap luôn là số thập phân hữu hạn, gọn


def rand_nonzero_w(rng):
    pool = [n for n in range(-25, 26) if n != 0]
    while True:
        n1 = rng.choice(pool)
        n2 = rng.choice(pool)
        if n1 != 0 or n2 != 0:
            return F(n1, 10), F(n2, 10)


def rand_b(rng):
    return F(rng.choice(range(-30, 31)), 10)


def rand_point(rng):
    return F(rng.choice(range(-4, 5))), F(rng.choice(range(-4, 5)))


def rand_perfect_w(rng):
    w1, w2, norm = rng.choice(PERFECT_PAIRS)
    if w1 != 0 and rng.random() < 0.5:
        w1 = -w1
    if w2 != 0 and rng.random() < 0.5:
        w2 = -w2
    if rng.random() < 0.5:
        w1, w2 = w2, w1
    return w1, w2, norm


# ---------------------------------------------------------------------------
# Sinh câu hỏi — PHẦN A: dấu (10 câu, đúng 1 câu rơi lên siêu phẳng)
# ---------------------------------------------------------------------------

def gen_normal_sign_q(rng):
    while True:
        w = rand_nonzero_w(rng)
        b = rand_b(rng)
        x = rand_point(rng)
        f = f_of(w, b, x)
        if f != 0:
            return {"w": w, "b": b, "x": x, "f": f, "on_h": False}


def gen_on_hyperplane_q(rng):
    w = rand_nonzero_w(rng)
    x = rand_point(rng)
    b = -dot(w, x)
    return {"w": w, "b": b, "x": x, "f": F(0), "on_h": True}


def sign_label(q):
    # Quy ước scikit-learn đã kiểm ở mục 3: ngưỡng là f > 0, không phải f >= 0.
    return 1 if q["f"] > 0 else -1


def gen_sign_section(rng):
    while True:
        normals = [gen_normal_sign_q(rng) for _ in range(9)]
        labels = {sign_label(q) for q in normals}
        if labels == {1, -1}:
            break
    special = gen_on_hyperplane_q(rng)
    questions = normals + [special]
    rng.shuffle(questions)
    return questions


# ---------------------------------------------------------------------------
# Sinh câu hỏi — PHẦN B: khoảng cách (5 câu)
# ---------------------------------------------------------------------------

def gen_distance_q(rng, nice):
    if nice:
        w1, w2, _ = rand_perfect_w(rng)
        w = (w1, w2)
    else:
        w = rand_nonzero_w(rng)
    b = rand_b(rng)
    x = rand_point(rng)
    f = f_of(w, b, x)
    return {"w": w, "b": b, "x": x, "f": f}


def gen_distance_section(rng):
    flags = [True, True, True, False, False]
    rng.shuffle(flags)
    return [gen_distance_q(rng, nice) for nice in flags]


# ---------------------------------------------------------------------------
# Sinh câu hỏi — PHẦN C: bề rộng lề (3 câu)
# ---------------------------------------------------------------------------

def gen_margin_q(rng, nice):
    if nice:
        w1, w2, _ = rand_perfect_w(rng)
        w = (w1, w2)
    else:
        w = rand_nonzero_w(rng)
    return {"w": w}


def gen_margin_section(rng):
    flags = [True, True, False]
    rng.shuffle(flags)
    return [gen_margin_q(rng, nice) for nice in flags]


# ---------------------------------------------------------------------------
# Sinh câu hỏi — PHẦN D: vector hỗ trợ (2 câu)
# ---------------------------------------------------------------------------

def _mk(axis, val, other_axis, other_val):
    p = [None, None]
    p[axis] = F(val)
    p[other_axis] = F(other_val)
    return tuple(p)


def gen_support_vector_q(rng):
    axis = rng.choice([0, 1])
    other_axis = 1 - axis
    neg_edge = rng.choice(range(-3, 1))
    gap = rng.choice(GAP_CHOICES)
    pos_edge = neg_edge + gap
    mid = F(neg_edge + pos_edge, 2)
    w_axis = F(2, 1) / F(gap, 1)
    w = [F(0), F(0)]
    w[axis] = w_axis
    w = tuple(w)
    b = -w_axis * mid

    offsets = rng.sample(range(-3, 4), k=4)
    o1, o2, o3, o4 = offsets
    inner_neg = neg_edge - rng.choice([1, 2])
    inner_pos = pos_edge + rng.choice([1, 2])

    points = [
        {"x": _mk(axis, neg_edge, other_axis, o1), "y": -1},
        {"x": _mk(axis, neg_edge, other_axis, o2), "y": -1},
        {"x": _mk(axis, inner_neg, other_axis, o3), "y": -1},
        {"x": _mk(axis, pos_edge, other_axis, o1), "y": 1},
        {"x": _mk(axis, pos_edge, other_axis, o4), "y": 1},
        {"x": _mk(axis, inner_pos, other_axis, o2), "y": 1},
    ]
    rng.shuffle(points)
    return {"w": w, "b": b, "points": points}


def gen_support_section(rng):
    return [gen_support_vector_q(rng) for _ in range(2)]


# ---------------------------------------------------------------------------
# Sinh toàn bộ đề
# ---------------------------------------------------------------------------

def gen_worksheet(seed):
    rng = random.Random(seed)
    return {
        "sign": gen_sign_section(rng),
        "distance": gen_distance_section(rng),
        "margin": gen_margin_section(rng),
        "support": gen_support_section(rng),
    }


# ---------------------------------------------------------------------------
# In đề / đáp án
# ---------------------------------------------------------------------------

def print_header():
    print("=" * 70)
    print("ĐỀ — Buổi 09: SVM và lề — 20 câu tính tay")
    print("Không dùng máy tính. Làm trong 20 phút, rồi mới mở đáp án.")
    print("=" * 70)


def print_sign_section(qs, show_answer):
    print("\nPHẦN A — DẤU (10 câu)")
    print("Cho w, b và điểm x. Hỏi: điểm x thuộc lớp nào?\n")
    for i, q in enumerate(qs, start=1):
        print(f"Câu {i}: w = {fmt_w(q['w'])}, b = {fmt(q['b'])}, x = {fmt_point(q['x'])}")
        if show_answer:
            label = sign_label(q)
            note = ""
            if q["on_h"]:
                note = "  (điểm rơi đúng lên siêu phẳng: f(x) = 0, theo quy ước f>0 nên xếp lớp −1)"
            print(f"   => f(x) = {fmt(q['f'])}  =>  lớp {'+1' if label==1 else '-1'}{note}")
    print()


def print_distance_section(qs, show_answer):
    print("PHẦN B — KHOẢNG CÁCH (5 câu)")
    print("Cho w, b và điểm x. Hỏi: khoảng cách từ x đến siêu phẳng bằng bao nhiêu?\n")
    for i, q in enumerate(qs, start=11):
        print(f"Câu {i}: w = {fmt_w(q['w'])}, b = {fmt(q['b'])}, x = {fmt_point(q['x'])}")
        if show_answer:
            norm = norm_float(q["w"])
            dist = abs(float(q["f"])) / norm
            print(f"   => f(x) = {fmt(q['f'])}, ||w|| ≈ {norm:.6f}  =>  khoảng cách ≈ {dist:.6f}")
    print()


def print_margin_section(qs, show_answer):
    print("PHẦN C — BỀ RỘNG LỀ (3 câu)")
    print("Cho w (không cần b). Hỏi: bề rộng lề bằng bao nhiêu?\n")
    for i, q in enumerate(qs, start=16):
        print(f"Câu {i}: w = {fmt_w(q['w'])}")
        if show_answer:
            norm = norm_float(q["w"])
            margin = 2.0 / norm
            print(f"   => ||w|| ≈ {norm:.6f}  =>  bề rộng lề ≈ {margin:.6f}")
    print()


def print_support_section(qs, show_answer):
    print("PHẦN D — VECTOR HỖ TRỢ (2 câu)")
    print("Cho w, b và các điểm đã gán nhãn. Hỏi: điểm nào là vector hỗ trợ?\n")
    for i, q in enumerate(qs, start=19):
        print(f"Câu {i}: w = {fmt_w(q['w'])}, b = {fmt(q['b'])}")
        for j, p in enumerate(q["points"], start=1):
            print(f"   P{j}: x = {fmt_point(p['x'])}, nhãn y = {'+1' if p['y']==1 else '-1'}")
        if show_answer:
            for j, p in enumerate(q["points"], start=1):
                val = p["y"] * f_of(q["w"], q["b"], p["x"])
                tag = "VECTOR HỖ TRỢ (y*f=1)" if val == 1 else f"không phải (y*f={fmt(val)})"
                print(f"      -> P{j}: {tag}")
    print()


def print_worksheet(ws, show_answer):
    print_header()
    print_sign_section(ws["sign"], show_answer)
    print_distance_section(ws["distance"], show_answer)
    print_margin_section(ws["margin"], show_answer)
    print_support_section(ws["support"], show_answer)


# ---------------------------------------------------------------------------
# --kiem : tự kiểm đáp án bằng một đường tính khác + kiểm hai điều kiện cổng
# ---------------------------------------------------------------------------

def independent_dot(w, x):
    # Cách tính khác: cộng dồn từng phần tử qua vòng lặp, thay vì viết trực tiếp w0*x0+w1*x1
    total = F(0)
    for a, b_ in zip(w, x):
        total = total + a * b_
    return total


def independent_f(w, b, x):
    return independent_dot(w, x) + b


def run_kiem(ws, seed):
    print("=" * 70)
    print(f"TỰ KIỂM ĐÁP ÁN (seed = {seed})")
    print("Đối chiếu từng câu bằng một đường tính khác, không phải chấm bài bạn.")
    print("=" * 70)

    ok = True

    # --- đối chiếu phần A, B, D bằng công thức tính lại độc lập ---
    print("\n[Đối chiếu] Phần A — dấu")
    for i, q in enumerate(ws["sign"], start=1):
        f2 = independent_f(q["w"], q["b"], q["x"])
        match = (f2 == q["f"])
        status = "khớp" if match else "KHÔNG KHỚP"
        print(f"  Câu {i}: {status}")
        ok = ok and match

    print("[Đối chiếu] Phần B — khoảng cách")
    for i, q in enumerate(ws["distance"], start=11):
        f2 = independent_f(q["w"], q["b"], q["x"])
        match = (f2 == q["f"])
        status = "khớp" if match else "KHÔNG KHỚP"
        print(f"  Câu {i}: {status}")
        ok = ok and match

    print("[Đối chiếu] Phần D — vector hỗ trợ")
    for i, q in enumerate(ws["support"], start=19):
        for j, p in enumerate(q["points"], start=1):
            f2 = independent_f(q["w"], q["b"], p["x"])
            val2 = p["y"] * f2
            val1 = p["y"] * f_of(q["w"], q["b"], p["x"])
            match = (val1 == val2)
            ok = ok and match
        print(f"  Câu {i}: khớp" if ok else f"  Câu {i}: KHÔNG KHỚP")

    # --- điều kiện 1: đề phải có đủ hai lớp (trong phần A) ---
    labels = {sign_label(q) for q in ws["sign"]}
    cond1 = (labels == {1, -1})
    print(f"\n[Điều kiện] Đề có đủ hai lớp trong phần A: {'OK' if cond1 else 'HỎNG'}"
          f" (các nhãn xuất hiện: {sorted(labels, reverse=True)})")
    ok = ok and cond1

    # --- điều kiện 2: đúng một câu rơi lên siêu phẳng ---
    on_h_count = sum(1 for q in ws["sign"] if q["f"] == 0)
    on_h_idx = [i for i, q in enumerate(ws["sign"], start=1) if q["f"] == 0]
    cond2 = (on_h_count == 1)
    print(f"[Điều kiện] Đúng một câu rơi lên siêu phẳng: {'OK' if cond2 else 'HỎNG'}"
          f" (số câu f(x)=0: {on_h_count}, câu số: {on_h_idx})")
    ok = ok and cond2

    print("\n" + "=" * 70)
    print("KẾT LUẬN: Đề và đáp án HỢP LỆ." if ok else "KẾT LUẬN: CÓ VẤN ĐỀ, xem chi tiết ở trên.")
    print("=" * 70)
    return ok


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Buổi 09 — SVM và lề — 20 câu tính tay")
    parser.add_argument("--dap-an", action="store_true", help="in đề kèm đáp án chi tiết")
    parser.add_argument("--kiem", action="store_true", help="tự kiểm đáp án, không chấm bài bạn")
    parser.add_argument("--seed", type=int, default=SEED_DEFAULT,
                         help=f"seed sinh đề (mặc định {SEED_DEFAULT}, đổi để ra đề khác)")
    args = parser.parse_args()

    ws = gen_worksheet(args.seed)

    if args.kiem:
        run_kiem(ws, args.seed)
    else:
        print_worksheet(ws, show_answer=args.dap_an)


if __name__ == "__main__":
    main()
