# -*- coding: utf-8 -*-
"""
HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG - CƠ SỞ TẠI TP. HỒ CHÍ MINH
HỌC PHẦN: CẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT (INT13185 - NHÓM 03)
GIẢNG VIÊN HƯỚNG DẪN: ThS. HỒ NHỰT MINH

SINH VIÊN THỰC HIỆN: PHẠM NGỌC THỌ
MSSV: N24DCDT089
LỚP: D24CQDT01-N
MÃ ĐỀ TÀI: DT074
TÊN ĐỀ TÀI: DUYỆT CHIỀU SÂU BẰNG STACK VÀ GIỮ THỨ TỰ ĐỆ QUY
CĂN CỨ GIÁO TRÌNH: Giáo trình INT1306, Chương 6, Mục 6.3.1; Chương 5, Mục 5.3.5 Khử đệ quy
"""

import sys
from typing import List, Tuple, Dict, Any, Union

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def kiem_tra_hop_le(n: int, canh: List[Tuple[int, int]], s: int) -> Tuple[bool, str]:
    """
    Kiểm tra tính hợp lệ của dữ liệu đầu vào theo đúng đặc tả của đề tài DT074:
    - n nguyên, 1 <= n <= 100
    - Đỉnh nguồn s nguyên, 1 <= s <= n
    - Mỗi cạnh (u, v) có 1 <= u, v <= n
    - Đồ thị đơn vô hướng: không có khuyên (u == v) và không có cạnh lặp (kể cả đảo chiều)
    """
    if not isinstance(n, int) or n < 1 or n > 100:
        return False, f"Lỗi: Số đỉnh n={n} không nằm trong phạm vi cho phép [1, 100]."
    if not isinstance(s, int) or s < 1 or s > n:
        return False, f"Lỗi: Đỉnh nguồn s={s} không hợp lệ (phải thuộc [1, {n}])."
    
    da_gap_canh = set()
    for idx, c in enumerate(canh):
        if not (isinstance(c, (list, tuple)) and len(c) == 2):
            return False, f"Lỗi: Cạnh thứ {idx+1} không đúng định dạng cặp (u, v)."
        u, v = c
        if not (isinstance(u, int) and isinstance(v, int)):
            return False, f"Lỗi: Đỉnh trong cạnh ({u}, {v}) phải là số nguyên."
        if u < 1 or u > n or v < 1 or v > n:
            return False, f"Lỗi: Cạnh ({u}, {v}) chứa đỉnh ngoài phạm vi [1, {n}]."
        if u == v:
            return False, f"Lỗi: Đồ thị đơn không cho phép khuyên (cạnh tự nối {u}-{v})."
        
        pair = (min(u, v), max(u, v))
        if pair in da_gap_canh:
            return False, f"Lỗi: Phát hiện cạnh trùng lặp ({u}, {v}) trong đồ thị đơn vô hướng."
        da_gap_canh.add(pair)

    return True, "Dữ liệu hợp lệ."


def tao_danh_sach_ke(n: int, canh: List[Tuple[int, int]]) -> Dict[int, List[int]]:
    """
    Xây dựng danh sách kề cho đồ thị vô hướng đơn từ danh sách cạnh.
    Mỗi đỉnh từ 1 đến n có một danh sách riêng biệt.
    Các đỉnh láng giềng được sắp xếp tăng dần theo yêu cầu đề bài.
    """
    ke = {i: [] for i in range(1, n + 1)}
    for u, v in canh:
        if 1 <= u <= n and 1 <= v <= n:
            ke[u].append(v)
            ke[v].append(u)
    for u in ke:
        ke[u].sort()
    return ke


def in_stack(st: List[int]) -> str:
    """
    Xuất trạng thái hiện tại của ngăn xếp theo chiều từ đáy tới đỉnh.
    Phần tử st[0] là đáy, st[-1] là đỉnh ngăn xếp.
    """
    if not st:
        return "[]"
    return f"[{', '.join(map(str, st))}]"


def dfs_de_quy(ke: Dict[int, List[int]], s: int) -> List[int]:
    """
    Duyệt DFS bằng đệ quy chuẩn mực (mốc so sánh đối chứng).
    Xét các láng giềng theo thứ tự tăng dần.
    """
    visited = {u: False for u in ke}
    ket_qua = []

    def _dfs(u: int):
        visited[u] = True
        ket_qua.append(u)
        for v in ke[u]:
            if not visited[v]:
                _dfs(v)

    if s in ke:
        _dfs(s)
    return ket_qua


def dfs_stack(ke: Dict[int, List[int]], s: int, in_vet: bool = False) -> Dict[str, Any]:
    """
    Duyệt DFS bằng vòng lặp và ngăn xếp (Stack), bảo toàn cùng thứ tự duyệt với DFS đệ quy.
    
    Quy tắc cốt lõi:
    1. Khởi tạo stack chứa đỉnh nguồn s: stack = [s].
    2. Đánh dấu visited khi LẤY KHỎI STACK (pop), KHÔNG đánh dấu khi đẩy.
    3. Nếu đỉnh lấy ra đã được đánh dấu visited trước đó -> BỎ QUA (bản sao chờ).
    4. Nếu đỉnh lấy ra chưa thăm:
       - Đánh dấu visited[u] = True.
       - Ghi nhận u vào kết quả duyệt.
       - Xét các láng giềng chưa thăm của u, ĐẨY VÀO STACK THEO THỨ TỰ GIẢM DẦN.
         (Vì ngăn xếp là LIFO, đỉnh nhỏ hơn vào sau sẽ nằm ở đỉnh stack và được lấy ra trước,
          bảo đảm thứ tự rẽ nhánh ưu tiên đỉnh nhỏ giống hệt đệ quy).
    """
    visited = {u: False for u in ke}
    stack = [s]
    ket_qua = []
    so_lan_day = 1
    so_lan_lay = 0
    so_ban_sao_bo_qua = 0
    lich_su_buoc = []

    if in_vet:
        print(f"--- BẮT ĐẦU DFS DÙNG STACK TỪ NGUỒN s = {s} ---")
        print(f"Khởi tạo: Stack = {in_stack(stack)}")
        print(f"{'Bước':<6} | {'Đỉnh lấy':<10} | {'Trạng thái':<12} | {'Hành động':<38} | {'Stack sau bước (đáy->đỉnh)':<25}")
        print("-" * 100)

    buoc = 0
    while stack:
        buoc += 1
        u = stack.pop()
        so_lan_lay += 1

        if visited[u]:
            so_ban_sao_bo_qua += 1
            hanh_dong = f"Đã thăm {u} -> BỎ QUA"
            if in_vet:
                print(f"{buoc:<6} | {u:<10} | {'Đã thăm':<12} | {hanh_dong:<38} | {in_stack(stack):<25}")
            lich_su_buoc.append((buoc, u, "Đã thăm", hanh_dong, list(stack)))
            continue

        visited[u] = True
        ket_qua.append(u)

        lang_gieng_chua_tham = [v for v in ke[u] if not visited[v]]
        lang_gieng_chua_tham.sort(reverse=True)
        for v in lang_gieng_chua_tham:
            stack.append(v)
            so_lan_day += 1

        if lang_gieng_chua_tham:
            hanh_dong = f"Thăm {u}, đẩy kề giảm {lang_gieng_chua_tham}"
        else:
            hanh_dong = f"Thăm {u}, không còn kề chưa thăm"

        if in_vet:
            print(f"{buoc:<6} | {u:<10} | {'Chưa thăm':<12} | {hanh_dong:<38} | {in_stack(stack):<25}")
        lich_su_buoc.append((buoc, u, "Chưa thăm", hanh_dong, list(stack)))

    if in_vet:
        print("-" * 100)
        print(f"Kết thúc duyệt: DFS = {ket_qua}")
        print(f"Thống kê: Đẩy={so_lan_day}, Lấy={so_lan_lay}, Bỏ qua={so_ban_sao_bo_qua}, Đỉnh duyệt={len(ket_qua)}\n")

    return {
        "ket_qua": ket_qua,
        "so_lan_day": so_lan_day,
        "so_lan_lay": so_lan_lay,
        "so_ban_sao_bo_qua": so_ban_sao_bo_qua,
        "so_dinh_duyet": len(ket_qua),
        "lich_su_buoc": lich_su_buoc
    }


def chay_dfs(n: int, canh: List[Tuple[int, int]], s: int, in_vet: bool = False) -> Dict[str, Any]:
    """
    Hàm giao tiếp tổng hợp: kiểm tra hợp lệ, dựng đồ thị và thực hiện DFS.
    """
    hop_le, msg = kiem_tra_hop_le(n, canh, s)
    if not hop_le:
        return {"hop_le": False, "loi": msg}
    ke = tao_danh_sach_ke(n, canh)
    kq_dequy = dfs_de_quy(ke, s)
    res_stack = dfs_stack(ke, s, in_vet=in_vet)
    return {
        "hop_le": True,
        "n": n,
        "canh": canh,
        "s": s,
        "ke": ke,
        "dfs_de_quy": kq_dequy,
        "dfs_stack": res_stack["ket_qua"],
        "thong_ke": res_stack,
        "khop_de_quy": (kq_dequy == res_stack["ket_qua"])
    }
