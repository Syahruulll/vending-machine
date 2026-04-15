import json

DATA_FILE = "items.txt"

def load_items():
    items = {}
    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                name, price, stock = line.strip().split(",")
                items[name] = {
                    "price": int(price),
                    "stock": int(stock)
                }
    except:
        print("File tidak ditemukan")
    return items

def save_items(items):
    with open(DATA_FILE, "w") as f:
        for name, info in items.items():
            f.write(f"{name},{info['price']},{info['stock']}\n")

def show_items(items):
    print("\nDaftar Barang:")
    for i, (name, info) in enumerate(items.items(), 1):
        print(f"{i}. {name} - Rp{info['price']} (Stok: {info['stock']})")

def main():
    items = load_items()
    if not items:
        return

    show_items(items)

    try:
        pilihan = int(input("Pilih nomor barang: "))
        item_list = list(items.items())

        nama_barang = item_list[pilihan - 1][0]
        info = items[nama_barang]

        if info["stock"] <= 0:
            print("Stok habis")
            return

        uang = int(input("Masukkan uang: "))

        if uang < info["price"]:
            print("Uang tidak cukup")
            return

        # UPDATE stok
        items[nama_barang]["stock"] -= 1
        save_items(items)

        print("Berhasil beli", nama_barang)

    except:
        print("Input salah")

if __name__ == "__main__":
    main()