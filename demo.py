# -*- coding: utf-8 -*-
"""
CHƯƠNG TRÌNH MINH HỌA VÀ ĐO ĐẠC THỰC NGHIỆM ĐỀ TÀI DT074
Sinh viên: Phạm Ngọc Thọ - MSSV: N24DCDT089
Lớp: D24CQDT01-N - Môn: INT13185 Nhóm 03

Cung cấp:
1. Chạy tương tác hoặc chạy tự động 8 ca minh họa (A01 - A08)
2. Nhập dữ liệu mới từ bàn phím
3. Khảo sát thực nghiệm thời gian và số thao tác trên 3 quy mô (n=5, 20, 50)
"""

import sys
import time
from typing import List, Tuple
from dfs_dt074 import kiem_tra_hop_le, tao_danh_sach_ke, dfs_de_quy, dfs_stack, chay_dfs, in_stack

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def demo_ca(ca_id: str):
    print("=" * 80)
    if ca_id == "1":
        print("DEMO CA 1 (A01 - VÍ DỤ 1 TRÊN PHIẾU GIAO ĐỀ TÀI)")
        print("Đồ thị n=4; Cạnh: (1,2), (1,3), (2,3), (2,4); Nguồn s=1")
        chay_dfs(4, [(1,2), (1,3), (2,3), (2,4)], 1, in_vet=True)
    elif ca_id == "2":
        print("DEMO CA 2 (A02 - VÍ DỤ 2 TRÊN PHIẾU GIAO ĐỀ TÀI)")
        print("Đồ thị n=4; Cạnh: (1,2), (1,4), (2,3); Nguồn s=4")
        chay_dfs(4, [(1,2), (1,4), (2,3)], 4, in_vet=True)
    elif ca_id == "3":
        print("DEMO CA 3 (A03 - TỰ THIẾT KẾ 1: TAM GIÁC 3 ĐỈNH)")
        print("Đồ thị n=3; Cạnh: (1,2), (2,3), (1,3); Nguồn s=1")
        chay_dfs(3, [(1,2), (2,3), (1,3)], 1, in_vet=True)
    elif ca_id == "4":
        print("DEMO CA 4 (A04 - TỰ THIẾT KẾ 2: CẠNH CHÉO NHIỀU NHÁNH)")
        print("Đồ thị n=5; Cạnh: (1,2), (1,3), (2,4), (2,5), (3,4); Nguồn s=1")
        chay_dfs(5, [(1,2), (1,3), (2,4), (2,5), (3,4)], 1, in_vet=True)
    elif ca_id == "5":
        print("DEMO CA 5 (A05 - BIÊN 1: MỘT ĐỈNH KHÔNG CẠNH)")
        print("Đồ thị n=1; Cạnh: []; Nguồn s=1")
        chay_dfs(1, [], 1, in_vet=True)
    elif ca_id == "6":
        print("DEMO CA 6 (A06 - BIÊN 2: ĐỈNH CÔ LẬP)")
        print("Đồ thị n=4; Cạnh: (1,2); Nguồn s=4 (cô lập)")
        chay_dfs(4, [(1,2)], 4, in_vet=True)
    elif ca_id == "7":
        print("DEMO CA 7 (A07 - BIÊN 3: ĐƯỜNG THẲNG 3 ĐỈNH)")
        print("Đồ thị n=3; Cạnh: (1,2), (2,3); Nguồn s=1")
        chay_dfs(3, [(1,2), (2,3)], 1, in_vet=True)
    elif ca_id == "8":
        print("DEMO CA 8 (A08 - INPUT KHÔNG HỢP LỆ: TỪ CHỐI KHUYÊN VÀ CẠNH TRÙNG)")
        print("Thử nghiệm 1: Cạnh có khuyên (1,1)")
        r1 = chay_dfs(3, [(1,1), (1,2)], 1)
        print(f"-> Kết quả phản hồi: {r1['loi']}")
        print("Thử nghiệm 2: Cạnh trùng (1,2) và (2,1)")
        r2 = chay_dfs(3, [(1,2), (2,1)], 1)
        print(f"-> Kết quả phản hồi: {r2['loi']}")
    else:
        print("Mã ca không hợp lệ! Vui lòng chọn 1-8.")


def khao_sat_quy_mo():
    print("=" * 80)
    print("BẢNG 4.3: KHẢO SÁT THỰC NGHIỆM ĐỘ PHỨC TẠP TRÊN 3 QUY MÔ (ĐỒ THỊ ĐƯỜNG)")
    print(f"{'Quy mô (n)':<12} | {'Số cạnh (m)':<12} | {'Đỉnh duyệt':<12} | {'Số lần đẩy':<12} | {'Số lần lấy':<12} | {'Bản sao':<10} | {'Thời gian (ms)':<15}")
    print("-" * 95)
    
    for n in [5, 20, 50]:
        canh = [(i, i+1) for i in range(1, n)]
        m = len(canh)
        ke = tao_danh_sach_ke(n, canh)
        
        # Đo đạc thời gian chạy lặp 500 lần để lấy độ chính xác cao
        so_vong = 500
        t0 = time.perf_counter()
        for _ in range(so_vong):
            res = dfs_stack(ke, 1, in_vet=False)
        t_total = (time.perf_counter() - t0) * 1000 / so_vong
        
        print(f"{n:<12} | {m:<12} | {res['so_dinh_duyet']:<12} | {res['so_lan_day']:<12} | {res['so_lan_lay']:<12} | {res['so_ban_sao_bo_qua']:<10} | {t_total:<15.4f}")
    print("=" * 80)


def nhap_tu_ban_phim():
    print("=" * 80)
    print("NHẬP DỮ LIỆU ĐỒ THỊ MỚI TỪ BÀN PHÍM")
    try:
        n = int(input("Nhập số đỉnh n (1 <= n <= 100): "))
        m = int(input("Nhập số cạnh m: "))
        canh = []
        print("Nhập m dòng, mỗi dòng 2 số nguyên u v:")
        for i in range(m):
            u, v = map(int, input(f"Cạnh {i+1}: ").split())
            canh.append((u, v))
        s = int(input(f"Nhập đỉnh nguồn s (1 <= s <= {n}): "))
        res = chay_dfs(n, canh, s, in_vet=True)
        if not res["hop_le"]:
            print(f"Từ chối: {res['loi']}")
        else:
            print(f"Dãy DFS lặp: {res['dfs_stack']}")
            print(f"Dãy DFS đệ quy: {res['dfs_de_quy']}")
            print(f"Khớp đệ quy: {'ĐÚNG' if res['khop_de_quy'] else 'SAI'}")
    except Exception as e:
        print(f"Lỗi nhập liệu: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("--ca="):
            ca = arg.split("=")[1]
            demo_ca(ca)
        elif arg == "--khao-sat":
            khao_sat_quy_mo()
        elif arg == "--nhap":
            nhap_tu_ban_phim()
        elif arg == "--all":
            for i in range(1, 9):
                demo_ca(str(i))
                print()
            khao_sat_quy_mo()
    else:
        print("Chạy toàn bộ 8 demo và bảng khảo sát quy mô:")
        for i in range(1, 9):
            demo_ca(str(i))
            print()
        khao_sat_quy_mo()
