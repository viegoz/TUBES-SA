from tabulate import tabulate
import time

def brute_force_profit(Negara, harga_beli, harga_jual, harga_sewa):
    n = len(Negara)
    ronde = len(harga_jual)
    
    # Negara paling profit pada setiap ronde untuk penjualan
    print("Negara paling profit pada setiap ronde untuk penjualan:")
    penjualan_data = []
    for i in range(ronde):
        ronde_data = ["Ronde {}".format(i+1)]
        for j in range(n):
            profit = harga_jual[i][j] - harga_beli[j]
            ronde_data.append(profit)
        penjualan_data.append(ronde_data)
    headers = ["Ronde/Negara"] + Negara
    print(tabulate(penjualan_data, headers=headers, tablefmt="grid"))
    
    # Negara paling profit untuk dibeli dan dijual
    print("\nNegara paling profit untuk dibeli untuk dijual:")
    pembelian_data = []
    for i in range(ronde):
        max_profit = max(harga_jual[i][j] - harga_beli[j] for j in range(n))
        Negara_terbaik = [Negara[j] for j in range(n) if harga_jual[i][j] - harga_beli[j] == max_profit]
        pembelian_data.append(["Ronde {}".format(i+1), ", ".join(Negara_terbaik), max_profit])
    print(tabulate(pembelian_data, headers=["Ronde", "Negara Terbaik", "Profit"], tablefmt="grid"))
    
    # Negara paling profit pada setiap ronde untuk disewakan
    print("\nNegara paling profit untuk disewakan:")
    sewa_data = []
    for j in range(n):
        profit = sum(harga_sewa[i][j] for i in range(ronde)) - harga_beli[j]
        sewa_data.append([Negara[j], profit])
    print(tabulate(sewa_data, headers=["Negara", "Profit"], tablefmt="grid"))
    
    # Negara paling profit untuk dibeli dan disewakan
    print("\nNegara paling profit untuk dibeli untuk disewakan:")
    max_profit = max(sum(harga_sewa[i][j] for i in range(ronde)) - harga_beli[j] for j in range(n))
    Negara_terbaik = [Negara[j] for j in range(n) if sum(harga_sewa[i][j] for i in range(ronde)) - harga_beli[j] == max_profit]
    print(tabulate([[", ".join(Negara_terbaik), max_profit]], headers=["Negara Terbaik", "Profit"], tablefmt="grid"))

def dynamic_programming_profit(Negara, harga_beli, harga_jual, harga_sewa):
    n = len(Negara)
    ronde = len(harga_jual)

    # Matriks untuk menyimpan hasil perhitungan profit
    dp = [[0] * n for _ in range(ronde)]
    sell_choice = [[[] for _ in range(n)] for _ in range(ronde)]
    rent_choice = [[] for _ in range(n)]

    # Mengisi matriks dp dengan profit maksimum untuk setiap kombinasi ronde dan Negara
    for i in range(ronde):
        for j in range(n):
            sell_profit = harga_jual[i][j] - harga_beli[j]
            rent_profit = dp[i-1][j] + harga_sewa[i][j] - harga_beli[j] if i > 0 else 0
            
            if sell_profit > rent_profit:
                dp[i][j] = sell_profit
                sell_choice[i][j] = [Negara[j]]
            else:
                dp[i][j] = rent_profit
                sell_choice[i][j] = sell_choice[i-1][j] if i > 0 else []
                rent_choice[j] = sell_choice[i-1][j] if i > 0 else []


    # Menampilkan profit jual setiap Negara pada setiap ronde
    print("\nProfit jual setiap Negara pada setiap ronde:")
    penjualan_data = []
    for i in range(ronde):
        ronde_data = ["Ronde {}".format(i+1)]
        for j in range(n):
            profit = harga_jual[i][j] - harga_beli[j]
            ronde_data.append(profit)
        penjualan_data.append(ronde_data)
    headers = ["Ronde/Negara"] + Negara
    print(tabulate(penjualan_data, headers=headers, tablefmt="grid"))

    # Menampilkan Negara dengan profit maksimum untuk dijual pada setiap ronde
    print("\nNegara dengan profit maksimum untuk dijual pada setiap ronde:")
    pembelian_data = []
    for i in range(ronde):
        max_profit = max(dp[i])
        Negara_terbaik = [Negara[j] for j in range(n) if dp[i][j] == max_profit]
        pembelian_data.append(["Ronde {}".format(i+1), ", ".join(Negara_terbaik), max_profit])
    print(tabulate(pembelian_data, headers=["Ronde", "Negara Terbaik", "Profit"], tablefmt="grid"))

     # Menampilkan Negara dengan profit maksimum untuk disewakan
    print("\nNegara dengan profit maksimum untuk disewakan:")
    sewa_data = []
    for j in range(n):
        rent_profit = sum(harga_sewa[i][j] for i in range(ronde)) - harga_beli[j]
        sewa_data.append([Negara[j], rent_profit])
    print(tabulate(sewa_data, headers=["Negara", "Profit"], tablefmt="grid"))

    # Menampilkan Negara dengan profit sewa terbesar
    max_rent_profit = max(sum(harga_sewa[i][j] for i in range(ronde)) - harga_beli[j] for j in range(n))
    Negara_terbaik_rent = [Negara[j] for j in range(n) if sum(harga_sewa[i][j] for i in range(ronde)) - harga_beli[j] == max_rent_profit]
    print("\nNegara dengan profit sewa terbesar:")
    print(tabulate([[", ".join(Negara_terbaik_rent), max_rent_profit]], headers=["Negara Terbaik", "Profit"], tablefmt="grid"))

# Input dari pengguna
n = int(input("Masukkan jumlah Negara: "))
ronde = int(input("Masukkan jumlah ronde: "))

Negara = []
harga_beli = []
harga_jual = []
harga_sewa = []

print("Masukkan NAMA Negara dan HARGA BELI setiap Negara:")
for i in range(n):
    nama = input("Nama Negara ke-{}: ".format(i+1))
    harga = int(input("Harga beli Negara {}: ".format(nama)))
    Negara.append(nama)
    harga_beli.append(harga)

print("Masukkan HARGA JUAL setiap Negara pada SETIAP RONDE:")
for i in range(ronde):
    print("Ronde", i+1)
    harga_jual_ronde = []
    for j in range(n):
        harga = int(input("Harga jual Negara {} pada ronde {}: ".format(Negara[j], i+1)))
        harga_jual_ronde.append(harga)
    harga_jual.append(harga_jual_ronde)

print("Masukkan HARGA SEWA setiap Negara pada SETIAP RONDE:")
for i in range(ronde):
    print("Ronde", i+1)
    harga_sewa_ronde = []
    for j in range(n):
        harga = int(input("Harga sewa Negara {} pada ronde {}: ".format(Negara[j], i+1)))
        harga_sewa_ronde.append(harga)
    harga_sewa.append(harga_sewa_ronde)

start_timebf = time.time()
# Metode Brute Force
print("Metode Brute Force:")
brute_force_profit(Negara, harga_beli, harga_jual, harga_sewa)
end_timebf = time.time()
run_timebf = end_timebf - start_timebf
print("run time BF : ", run_timebf,"second")

print("\n")

start_timedp = time.time()
# Metode Dynamic Programming
print("Metode Dynamic Programming:")
dynamic_programming_profit(Negara, harga_beli, harga_jual, harga_sewa)
end_timedp = time.time()
run_timedp = end_timedp - start_timedp
print("run time DP : ", run_timedp, "second")
