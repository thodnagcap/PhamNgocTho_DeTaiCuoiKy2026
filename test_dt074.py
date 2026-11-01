# -*- coding: utf-8 -*-
"""
BỘ KIỂM THỬ ĐỘC LẬP TOÀN DIỆN CHO ĐỀ TÀI DT074
Sinh viên: Phạm Ngọc Thọ - MSSV: N24DCDT089
Lớp: D24CQDT01-N - Môn: INT13185 Nhóm 03

Bao gồm 14 ca kiểm thử độc lập:
- 2 ví dụ bắt buộc trong phiếu giao đề tài (VD01, VD02)
- 2 ca tự thiết kế (TK01, TK02)
- 3 ca biên bài toán (BIEN01, BIEN02, BIEN03)
- 2 ca kiểm thử validator input sai (LOI01, LOI02)
- 5 ca bổ sung kiểm tra cấu trúc đặc thù (chu trình chéo, sao, đồ thị đầy đủ K5, hai nhánh rẽ, đường dài)
"""

import sys
import unittest
from dfs_dt074 import kiem_tra_hop_le, tao_danh_sach_ke, dfs_de_quy, dfs_stack, chay_dfs

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


class TestDT074(unittest.TestCase):

    def test_KT01_VD01_phieu_giao(self):
        """KT01 (VD01): n=4, canh=[(1,2),(1,3),(2,3),(2,4)], s=1 -> Kỳ vọng: [1,2,3,4]"""
        n, canh, s = 4, [(1,2), (1,3), (2,3), (2,4)], 1
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [1, 2, 3, 4])
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])
        # Đỉnh 3 bị lặp trong stack và bị bỏ qua ở bước 5
        self.assertEqual(res["thong_ke"]["so_ban_sao_bo_qua"], 1)

    def test_KT02_VD02_phieu_giao(self):
        """KT02 (VD02): n=4, canh=[(1,2),(1,4),(2,3)], s=4 -> Kỳ vọng: [4,1,2,3]"""
        n, canh, s = 4, [(1,2), (1,4), (2,3)], 4
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [4, 1, 2, 3])
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])
        self.assertEqual(res["thong_ke"]["so_ban_sao_bo_qua"], 0)

    def test_KT03_TK01_tam_giac(self):
        """KT03 (TK01): Tam giác 3 đỉnh n=3, canh=[(1,2),(2,3),(1,3)], s=1 -> Kỳ vọng: [1,2,3]"""
        n, canh, s = 3, [(1,2), (2,3), (1,3)], 1
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [1, 2, 3])
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])
        self.assertEqual(res["thong_ke"]["so_ban_sao_bo_qua"], 1)

    def test_KT04_TK02_canh_cheo_nhieu_nhanh(self):
        """KT04 (TK02): n=5, canh=[(1,2),(1,3),(2,4),(2,5),(3,4)], s=1 -> Kỳ vọng: [1,2,4,3,5]"""
        n, canh, s = 5, [(1,2), (1,3), (2,4), (2,5), (3,4)], 1
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [1, 2, 4, 3, 5])
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])

    def test_KT05_BIEN01_mot_dinh_khong_canh(self):
        """KT05 (BIEN01): Biên nhỏ nhất n=1, không có cạnh, s=1 -> Kỳ vọng: [1]"""
        n, canh, s = 1, [], 1
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [1])
        self.assertEqual(res["thong_ke"]["so_lan_day"], 1)
        self.assertEqual(res["thong_ke"]["so_lan_lay"], 1)

    def test_KT06_BIEN02_dinh_co_lap(self):
        """KT06 (BIEN02): n=4, chỉ có cạnh (1,2), nguồn s=4 (cô lập) -> Kỳ vọng: [4]"""
        n, canh, s = 4, [(1,2)], 4
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [4])
        self.assertEqual(res["thong_ke"]["so_dinh_duyet"], 1)

    def test_KT07_BIEN03_duong_thang_3_dinh(self):
        """KT07 (BIEN03): n=3, canh=[(1,2),(2,3)], s=1 -> Kỳ vọng: [1,2,3]"""
        n, canh, s = 3, [(1,2), (2,3)], 1
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [1, 2, 3])
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])

    def test_KT08_LOI01_canh_khuyen_va_trung(self):
        """KT08 (LOI01): Input chứa khuyên (1,1) hoặc cạnh trùng -> Validator từ chối"""
        n, canh, s = 3, [(1,1), (1,2)], 1
        res = chay_dfs(n, canh, s)
        self.assertFalse(res["hop_le"])
        self.assertIn("khuyên", res["loi"])

        n2, canh2, s2 = 3, [(1,2), (2,1)], 1
        res2 = chay_dfs(n2, canh2, s2)
        self.assertFalse(res2["hop_le"])
        self.assertIn("trùng", res2["loi"])

    def test_KT09_LOI02_nguon_va_dinh_ngoai_bien(self):
        """KT09 (LOI02): n=4, s=5 (ngoài biên) hoặc cạnh chứa đỉnh 0, 5 -> Validator từ chối"""
        n, canh, s = 4, [(1,2)], 5
        res = chay_dfs(n, canh, s)
        self.assertFalse(res["hop_le"])
        self.assertIn("Đỉnh nguồn", res["loi"])

        n2, canh2, s2 = 4, [(1,5)], 1
        res2 = chay_dfs(n2, canh2, s2)
        self.assertFalse(res2["hop_le"])
        self.assertIn("phạm vi", res2["loi"])

    def test_KT10_do_thi_sao(self):
        """KT10: Đồ thị hình sao tâm 1, n=5, canh=[(1,2),(1,3),(1,4),(1,5)], s=1 -> Kỳ vọng: [1,2,3,4,5]"""
        n, canh, s = 5, [(1,2), (1,3), (1,4), (1,5)], 1
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [1, 2, 3, 4, 5])
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])

    def test_KT11_do_thi_day_du_K5(self):
        """KT11: Đồ thị đầy đủ K5 (n=5, 10 cạnh), s=1 -> Kỳ vọng: [1,2,3,4,5]"""
        n = 5
        canh = [(u, v) for u in range(1, 6) for v in range(u+1, 6)]
        s = 1
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [1, 2, 3, 4, 5])
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])
        self.assertTrue(res["thong_ke"]["so_ban_sao_bo_qua"] > 0)

    def test_KT12_duong_dai_n10(self):
        """KT12: Đồ thị đường dài n=10, 9 cạnh nối tiếp, s=10 -> Kỳ vọng: [10,9,8,7,6,5,4,3,2,1]"""
        n = 10
        canh = [(i, i+1) for i in range(1, 10)]
        s = 10
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], list(range(10, 0, -1)))
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])

    def test_KT13_hai_nhanh_uu_tien_nho(self):
        """KT13: n=6, canh=[(1,3),(1,2),(2,4),(3,5),(4,6)], s=1 -> Kỳ vọng: [1,2,4,6,3,5]"""
        n = 6
        canh = [(1,3), (1,2), (2,4), (3,5), (4,6)]
        s = 1
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [1, 2, 4, 6, 3, 5])
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])

    def test_KT14_chu_trinh_4_dinh(self):
        """KT14: Vòng chu trình 4 đỉnh n=4, canh=[(1,2),(2,3),(3,4),(4,1)], s=1 -> Kỳ vọng: [1,2,3,4]"""
        n, canh, s = 4, [(1,2), (2,3), (3,4), (4,1)], 1
        res = chay_dfs(n, canh, s)
        self.assertTrue(res["hop_le"])
        self.assertEqual(res["dfs_stack"], [1, 2, 3, 4])
        self.assertEqual(res["dfs_stack"], res["dfs_de_quy"])


def chay_tat_ca_kiem_thu():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDT074)
    runner = unittest.TextTestRunner(verbosity=2)
    print("=" * 80)
    print("CHẠY BỘ KIỂM THỬ ĐỘC LẬP TOÀN DIỆN CHO ĐỀ TÀI DT074 (14/14 CA KIỂM)")
    print("Sinh viên: Phạm Ngọc Thọ - MSSV: N24DCDT089 - Lớp: D24CQDT01-N")
    print("=" * 80)
    result = runner.run(suite)
    print("-" * 80)
    print(f"Tổng kết kiểm thử: {result.testsRun} ca chạy, {len(result.failures)} lỗi, {len(result.errors)} ngoại lệ.")
    if result.wasSuccessful():
        print("KẾT LUẬN: TẤT CẢ CÁC PHÉP KIỂM ĐÃ ĐẠT (PASS 100%)!")
    else:
        print("KẾT LUẬN: CÓ PHÉP KIỂM CHƯA ĐẠT.")
    return result.wasSuccessful()


if __name__ == "__main__":
    chay_tat_ca_kiem_thu()
