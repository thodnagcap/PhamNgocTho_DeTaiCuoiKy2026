# ĐỀ TÀI DT074 — DUYỆT CHIỀU SÂU BẰNG STACK VÀ GIỮ THỨ TỰ ĐỆ QUY

HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG — CƠ SỞ TẠI TP. HỒ CHÍ MINH  
Học phần: Cấu trúc dữ liệu và Giải thuật (INT13185 — Nhóm 03)  
Giảng viên hướng dẫn: ThS. Hồ Nhựt Minh  

- **Sinh viên thực hiện**: Phạm Ngọc Thọ  
- **Mã số sinh viên (MSSV)**: N24DCDT089  
- **Lớp**: D24CQDT01-N  
- **Mã đề tài**: DT074  
- **Giáo trình tham chiếu**: Giáo trình INT1306, Chương 6, Mục 6.3.1 (Duyệt theo chiều sâu); Chương 5, Mục 5.3.5 (Khử đệ quy); Trang in 130, 142–143 (Trang PDF 142, 154–155).  
- **Ngôn ngữ lập trình**: Python 3.9+  
- **URL GitHub**: `https://github.com/phamngoctho/N24DCDT089_DT074_PhamNgocTho`  
- **SHA Commit chạy (C)**: `b7a9e2f4c1d8e3f6a5b2c9d0e1f4a7b8c3d2e1f0`  
- **Permalink thuật toán chính**: `https://github.com/phamngoctho/N24DCDT089_DT074_PhamNgocTho/blob/b7a9e2f4c1d8e3f6a5b2c9d0e1f4a7b8c3d2e1f0/dfs_dt074.py`  

---

## 1. Cấu trúc thư mục mã nguồn

```text
N24DCDT089_DT074_PhamNgocTho/
├── dfs_dt074.py                      # Module cài đặt cấu trúc dữ liệu, validator và thuật toán DFS khử đệ quy
├── test_dt074.py                     # Bộ kiểm thử tự động với 14 ca kiểm độc lập (đạt 14/14 PASS)
├── demo.py                           # Chương trình chạy 8 ca demo, khảo sát quy mô và nhập từ bàn phím
├── README.md                         # Hướng dẫn chi tiết cấu trúc bài toán và các lệnh thực thi
├── N24DCDT089_DT074_PhamNgocTho_BaoCao.docx    # Báo cáo toàn văn định dạng Word (.docx)
├── N24DCDT089_DT074_PhamNgocTho_BaoCao.pdf     # Báo cáo toàn văn định dạng PDF (.pdf)
├── N24DCDT089_DT074_PhamNgocTho_MaNguon.zip    # Gói mã nguồn ZIP nộp bài
├── N24DCDT089_DT074_PhamNgocTho_ThongTinNop.txt # Tệp thông tin nộp bài rời
└── docs/
    └── anh_ket_qua/                  # Đủ 11 ảnh minh chứng thực thi (A01 - A11)
        ├── 01_vi_du_1.png
        ├── 02_vi_du_2.png
        ├── 03_tu_thiet_ke_1.png
        ├── 04_tu_thiet_ke_2.png
        ├── 05_bien_1.png
        ├── 06_bien_2.png
        ├── 07_bien_3.png
        ├── 08_input_khong_hop_le.png
        ├── 09_tong_ket_kiem_thu.png
        ├── 10_clone_sach_chay_lai.png
        └── 11_github_repo_commit.png
```

---

## 2. Đặc tả bài toán và nguyên lý khử đệ quy (DT074)

### 2.1. Đầu vào và đầu ra
- **Đầu vào**: Đồ thị vô hướng đơn có $n$ đỉnh ($1 \le n \le 100$), các đỉnh được đánh số $1..n$, đỉnh nguồn $s$ ($1 \le s \le n$). Danh sách cạnh gồm các cặp $(u, v)$ không chứa khuyên và không chứa cạnh trùng.
- **Đầu ra**: Dãy thứ tự duyệt DFS lặp bằng Stack, trạng thái ngăn xếp qua từng bước và đối chiếu với kết quả của DFS đệ quy.

### 2.2. Ba quy tắc khử đệ quy cốt lõi
1. **Đẩy láng giềng theo thứ tự GIẢM DẦN**: Do cơ chế LIFO của Stack, việc đẩy phần tử lớn trước sẽ giúp phần tử nhỏ hơn nằm ở đỉnh stack và được lấy ra xử lý trước, bảo toàn thứ tự duyệt rẽ nhánh ưu tiên đỉnh nhỏ giống hệt DFS đệ quy.
2. **Đánh dấu `visited` khi LẤY RA (`pop()`)**: Tuyệt đối không đánh dấu khi đẩy vào stack nhằm bảo toàn khả năng khám phá tất cả các đường đi sâu và quay lui.
3. **Bỏ qua bản sao chờ (Duplicate Entries)**: Một đỉnh có thể được đẩy vào stack nhiều lần từ các đỉnh láng giềng khác nhau trước khi nó được lấy ra lần đầu. Khi `pop()` đỉnh $u$, nếu $u$ đã được thăm trước đó thì lập tức bỏ qua.

---

## 3. Hướng dẫn thực thi chương trình

### 3.1. Chạy hai ví dụ trong phiếu đề tài
- **Ví dụ 1**:
  ```powershell
  python demo.py --ca=1
  ```
  *Kết quả kỳ vọng*: `DFS = [1, 2, 3, 4]`. Bản sao thứ hai của đỉnh 3 bị loại bỏ ở bước 5.

- **Ví dụ 2**:
  ```powershell
  python demo.py --ca=2
  ```
  *Kết quả kỳ vọng*: `DFS = [4, 1, 2, 3]`.

### 3.2. Chạy toàn bộ 8 ca minh họa và khảo sát quy mô
```powershell
python demo.py --all
```

### 3.3. Chạy chế độ nhập dữ liệu đồ thị mới từ bàn phím
```powershell
python demo.py --nhap
```

### 3.4. Chạy bộ kiểm thử tự động toàn diện (14/14 ca độc lập)
```powershell
python test_dt074.py
```
*Kết quả*: 14 ca độc lập (2 ví dụ, 2 tự thiết kế, 3 biên, 2 ca input sai, 5 ca mở rộng) đều đạt `PASS 100%`.

---

## 4. Kiểm tra clone sạch từ GitHub

```powershell
git clone https://github.com/phamngoctho/N24DCDT089_DT074_PhamNgocTho.git kiem_tra_clone
cd kiem_tra_clone
git rev-parse HEAD
python test_dt074.py
```

---

## 5. Danh mục 11 ảnh minh chứng thực thi

| Mã ảnh | Case ID | Nội dung minh chứng | Tệp ảnh tương ứng trong repo |
|:---:|:---:|:---|:---|
| **A01** | VD01 | Ví dụ 1 phiếu đề tài ($n=4, s=1$) | `docs/anh_ket_qua/01_vi_du_1.png` |
| **A02** | VD02 | Ví dụ 2 phiếu đề tài ($n=4, s=4$) | `docs/anh_ket_qua/02_vi_du_2.png` |
| **A03** | TK01 | Ca tự thiết kế 1: Tam giác 3 đỉnh ($s=1$) | `docs/anh_ket_qua/03_tu_thiet_ke_1.png` |
| **A04** | TK02 | Ca tự thiết kế 2: Cạnh chéo nhiều nhánh ($n=5$) | `docs/anh_ket_qua/04_tu_thiet_ke_2.png` |
| **A05** | BIEN01 | Ca biên 1: Đồ thị suy biến 1 đỉnh ($n=1, s=1$) | `docs/anh_ket_qua/05_bien_1.png` |
| **A06** | BIEN02 | Ca biên 2: Đỉnh nguồn $s=4$ cô lập | `docs/anh_ket_qua/06_bien_2.png` |
| **A07** | BIEN03 | Ca biên 3: Đồ thị đường thẳng 3 đỉnh | `docs/anh_ket_qua/07_bien_3.png` |
| **A08** | LOI01 | Validator từ chối cạnh khuyên và cạnh trùng | `docs/anh_ket_qua/08_input_khong_hop_le.png` |
| **A09** | TEST_ALL | Tổng kết 14/14 ca kiểm thử đạt PASS 100% | `docs/anh_ket_qua/09_tong_ket_kiem_thu.png` |
| **A10** | CLONE | Clone sạch sang thư mục mới và chạy lại commit nộp | `docs/anh_ket_qua/10_clone_sach_chay_lai.png` |
| **A11** | GITHUB | Giao diện GitHub Repo, commit SHA C và permalink | `docs/anh_ket_qua/11_github_repo_commit.png` |
