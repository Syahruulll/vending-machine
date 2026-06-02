import os
import random
from datetime import datetime
import hashlib
FILE_DB = "items.txt"
FILE_LOG = "transaksi.txt"
FILE_REPORT = "laporan.txt"

ADMIN_CODE = "ADMIN123"
ADMIN_PIN_HASH = "f379fb046ad28c2b406d045ac2342345238b94433542fb210933d79b7da328ce"


# =========================
# DATABASE
# =========================
def init_db():
    if not os.path.exists(FILE_DB):
        with open(FILE_DB, "w", encoding="utf-8") as f:
            f.write("A1,Coca-Cola,7000,10\n")
            f.write("A2,Fanta,7000,10\n")
            f.write("A3,Sprite,7000,10\n")
            f.write("B1,Aqua,3000,15\n")
            f.write("B2,Le Minerale,4000,15\n")
            f.write("C1,Chitato,10000,8\n")
            f.write("C2,Chiki Balls,5000,8\n")


def load_products():
    products = {}

    if os.path.exists(FILE_DB):
        with open(FILE_DB, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    kode, nama, harga, stok = line.strip().split(",")

                    products[kode] = {
                        "nama": nama,
                        "harga": int(harga),
                        "stok": int(stok)
                    }

    return products


def save_products(products):

    with open(FILE_DB, "w", encoding="utf-8") as f:

        for kode, p in products.items():

            f.write(
                f"{kode},{p['nama']},"
                f"{p['harga']},"
                f"{p['stok']}\n"
            )


# =========================
# TRANSAKSI
# =========================
def log_transaction(kode, nama, harga):

    trx = random.randint(100000, 999999)

    waktu = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(FILE_LOG, "a", encoding="utf-8") as f:

        f.write(
            f"{trx},"
            f"{waktu},"
            f"{kode},"
            f"{nama},"
            f"{harga}\n"
        )


# =========================
# TAMPIL PRODUK
# =========================
def tampil_produk(products):

    print("\n" + "=" * 70)
    print("DAFTAR PRODUK")
    print("=" * 70)

    for kode, p in products.items():

        if p["stok"] == 0:
            status = "HABIS"

        elif p["stok"] <= 2:
            status = f"TINGGAL {p['stok']}"

        else:
            status = f"STOK {p['stok']}"

        print(
            f"{kode:<5} | "
            f"{p['nama']:<20} | "
            f"Rp{p['harga']:<8} | "
            f"{status}"
        )

    print("=" * 70)


# =========================
# SEARCH
# =========================
def cari_produk(products):

    keyword = input(
        "Masukkan nama produk: "
    ).lower()

    ditemukan = False

    for kode, p in products.items():

        if keyword in p["nama"].lower():

            print(
                f"{kode} - "
                f"{p['nama']} - "
                f"Rp{p['harga']} - "
                f"Stok {p['stok']}"
            )

            ditemukan = True

    if not ditemukan:
        print("Produk tidak ditemukan.")


# =========================
# SORTING
# =========================
def sort_produk(products):

    hasil = sorted(
        products.items(),
        key=lambda x: x[1]["harga"]
    )

    print("\n=== PRODUK TERMURAH ===")

    for kode, p in hasil:

        print(
            f"{kode} - "
            f"{p['nama']} - "
            f"Rp{p['harga']}"
        )


# =========================
# KEMBALIAN
# =========================
def hitung_kembalian(uang):

    pecahan = [
        100000,
        50000,
        20000,
        10000,
        5000,
        2000,
        1000
    ]

    print("\nRincian Kembalian")

    for p in pecahan:

        jumlah = uang // p

        if jumlah > 0:

            print(
                f"{jumlah} x Rp{p}"
            )

        uang %= p


# =========================
# LAPORAN
# =========================
def laporan_penjualan():

    total = 0
    jumlah = 0

    if not os.path.exists(FILE_LOG):

        print("Belum ada transaksi.")
        return

    with open(FILE_LOG, "r", encoding="utf-8") as f:

        for line in f:

            data = line.strip().split(",")

            total += int(data[4])
            jumlah += 1

    print("\n=== LAPORAN ===")

    print(
        f"Jumlah Transaksi : {jumlah}"
    )

    print(
        f"Total Pendapatan : Rp{total}"
    )

    with open(FILE_REPORT, "w") as f:

        f.write(
            f"Jumlah Transaksi : "
            f"{jumlah}\n"
        )

        f.write(
            f"Total Pendapatan : "
            f"Rp{total}\n"
        )

    print(
        "Laporan disimpan ke laporan.txt"
    )


# =========================
# PRODUK TERLARIS
# =========================
def produk_terlaris():

    if not os.path.exists(FILE_LOG):

        print("Belum ada transaksi.")
        return

    data = {}

    with open(FILE_LOG, "r") as f:

        for line in f:

            row = line.strip().split(",")

            kode = row[2]

            data[kode] = (
                data.get(kode, 0) + 1
            )

    terlaris = max(
        data,
        key=data.get
    )

    print(
        f"Produk Terlaris : "
        f"{terlaris} "
        f"({data[terlaris]} terjual)"
    )


# =========================
# ADMIN
# =========================
def menu_admin():

    kesempatan = 3
    login_berhasil = False

    while kesempatan > 0:

        pin = input(
            "Masukkan PIN Admin: "
        )

        if verify_admin_pin(pin):

            login_berhasil = True
            print("Login Admin Berhasil!")
            break

        kesempatan -= 1

        print(
            f"PIN salah! "
            f"Sisa percobaan: {kesempatan}"
        )

    if not login_berhasil:

        print(
            "Akses admin ditolak."
        )

        return

    while True:

        products = load_products()

        print("\n=== MENU ADMIN ===")
        print("1. Lihat Produk")
        print("2. Tambah Produk")
        print("3. Hapus Produk")
        print("4. Restock Produk")
        print("5. Ubah Harga")
        print("6. Laporan")
        print("7. Produk Terlaris")
        print("0. Keluar")

        pilih = input("Pilih: ")

        if pilih == "1":
            tampil_produk(products)

        elif pilih == "2":

            kode = input(
                "Kode Produk: "
            ).upper()

            nama = input(
                "Nama Produk: "
            )

            harga = int(
                input("Harga: ")
            )

            stok = int(
                input("Stok: ")
            )

            products[kode] = {
                "nama": nama,
                "harga": harga,
                "stok": stok
            }

            save_products(products)

            print(
                "Produk berhasil ditambah."
            )

        elif pilih == "3":

            kode = input(
                "Kode Produk: "
            ).upper()

            if kode in products:

                del products[kode]

                save_products(products)

                print(
                    "Produk dihapus."
                )

        elif pilih == "4":

            kode = input(
                "Kode Produk: "
            ).upper()

            if kode in products:

                tambah = int(
                    input(
                        "Tambah Stok: "
                    )
                )

                products[kode]["stok"] += tambah

                save_products(products)

                print(
                    "Restock berhasil."
                )

        elif pilih == "5":

            kode = input(
                "Kode Produk: "
            ).upper()

            if kode in products:

                harga = int(
                    input(
                        "Harga Baru: "
                    )
                )

                products[kode]["harga"] = harga

                save_products(products)

                print(
                    "Harga diperbarui."
                )

        elif pilih == "6":
            laporan_penjualan()

        elif pilih == "7":
            produk_terlaris()

        elif pilih == "0":
            break

        else:
            print("Menu tidak tersedia.")
        
def verify_admin_pin(pin):

    hashed = hashlib.sha256(
        pin.encode()
    ).hexdigest()

    return hashed == ADMIN_PIN_HASH


# =========================
# USER
# =========================
def menu_user():

    saldo = 0
    keranjang = []

    while True:

        products = load_products()

        print("\n=== SMART VENDING MACHINE ===")
        print(f"Saldo Anda : Rp{saldo}")
        print("1. Isi Saldo")
        print("2. Lihat Produk")
        print("3. Cari Produk")
        print("4. Sort Produk")
        print("5. Tambah ke Keranjang")
        print("6. Lihat Keranjang")
        print("7. Checkout")
        print("0. Keluar")

        pilih = input(
            "Pilih Menu: "
        ).strip()

        # ADMIN TERSEMBUNYI
        if pilih.upper() == ADMIN_CODE:

            menu_admin()

            continue

        if pilih == "1":

            try:

                uang = int(
                    input(
                        "Masukkan uang: Rp"
                    )
                )

                if uang > 0:

                    saldo += uang

            except:
                print("Input salah")

        elif pilih == "2":

            tampil_produk(products)

        elif pilih == "3":

            cari_produk(products)

        elif pilih == "4":

            sort_produk(products)

        elif pilih == "5":

            tampil_produk(products)

            kode = input(
                "Kode Produk: "
            ).upper()

            if kode not in products:

                print(
                    "Produk tidak ditemukan."
                )

                continue

            if products[kode]["stok"] <= 0:

                print(
                    "Produk habis."
                )

                continue

            keranjang.append(kode)

            print(
                f"{products[kode]['nama']} "
                "ditambahkan."
            )

        elif pilih == "6":

            total = 0

            print("\n=== KERANJANG ===")

            if not keranjang:

                print("Kosong")

            for item in keranjang:

                print(
                    products[item]["nama"]
                )

                total += products[item][
                    "harga"
                ]

            print(
                f"Total : Rp{total}"
            )

        elif pilih == "7":

            if not keranjang:

                print(
                    "Keranjang kosong."
                )

                continue

            total = sum(
                products[k]["harga"]
                for k in keranjang
            )

            if saldo < total:

                print(
                    f"Saldo kurang "
                    f"Rp{total-saldo}"
                )

                continue

            saldo -= total

            print("\n" + "=" * 50)
            print("STRUK PEMBELIAN")
            print("=" * 50)

            trx = random.randint(
                100000,
                999999
            )

            print(
                f"No Transaksi : "
                f"{trx}"
            )

            print(
                f"Tanggal : "
                f"{datetime.now()}"
            )

            print("-" * 50)

            for item in keranjang:

                products[item]["stok"] -= 1

                print(
                    f"{products[item]['nama']} "
                    f"Rp{products[item]['harga']}"
                )

                log_transaction(
                    item,
                    products[item]["nama"],
                    products[item]["harga"]
                )

            save_products(products)

            print("-" * 50)

            print(
                f"TOTAL : Rp{total}"
            )

            print(
                f"SISA SALDO : Rp{saldo}"
            )

            print("=" * 50)

            keranjang.clear()

        elif pilih == "0":

            if saldo > 0:

                print(
                    f"\nKembalian "
                    f"Rp{saldo}"
                )

                hitung_kembalian(
                    saldo
                )

            print(
                "\nTerima kasih "
                "telah menggunakan "
                "vending machine."
            )

            break

        else:

            print(
                "Menu tidak tersedia."
            )


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    init_db()

    menu_user()
