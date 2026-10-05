mo = mang(d_an, dropout, seed)
opt = torch.optim.Adam(mo.parameters(), lr=buoc, weight_decay=phat)
mat = torch.nn.BCEWithLogitsLoss()

for vong in range(so_vong):
    mo.train()
    thu_tu = torch.randperm(n) # 1. X xáo trộn mini-batch
    for i in range(0, n, co_batch):
        idx = thu_tu[i:i + co_batch]
        opt.zero_grad()         # 2. Xoá gradient cũ
        mat(mo(Xh[idx]).ravel(), yh[idx]).backward()
        opt.step()
    
    mo.eval()                   # 3. Chuyển sang chế độ đánh giá
    with torch.no_grad():       # 4. Tắt đồ thị đạo hàm
        d = f1m(yk.numpy(), (mo(Xk).ravel() > 0).numpy().astype(int))
        
        
import random
torch.set_num_threads(1) # buoi 13: thread count changes the result
def dat_hat_giong(seed=0):
"""Everything the exam asks to pin, in one place."""
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)