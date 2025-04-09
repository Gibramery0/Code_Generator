import random
import string
import os
from datetime import datetime

def generate_random_code(digit_count):
    """
    Belirtilen basamak sayısında rastgele alfanümerik kod üretir
    (Sadece BÜYÜK HARF ve rakamlar)
    """
    # Sadece büyük harfler (A-Z) ve rakamlar (0-9)
    characters = string.ascii_uppercase + string.digits
    
    # Rastgele karakterleri seç ve birleştir
    code = ''.join(random.choice(characters) for _ in range(digit_count))
    return code

def generate_unique_codes(digit_count, code_count):
    """
    Belirtilen sayıda ve basamakta benzersiz kodlar üretir
    """
    codes = set()  # Benzersiz kodları tutmak için set kullanıyoruz
    
    # Olası maksimum kombinasyon sayısını hesapla
    max_possible = (len(string.ascii_uppercase) + len(string.digits)) ** digit_count
    
    # İstenen kod sayısı mümkün kombinasyonlardan fazlaysa hata ver
    if code_count > max_possible:
        raise ValueError(f"İstenen kod sayısı ({code_count}) mümkün olan maksimum kombinasyon sayısından ({max_possible}) fazla!")
    
    # İstenen sayıda benzersiz kod üret
    while len(codes) < code_count:
        new_code = generate_random_code(digit_count)
        codes.add(new_code)
    
    return sorted(list(codes))  # Sıralı liste olarak döndür

def save_codes_to_file(codes):
    """
    Kodları 'Generated codes' klasörü içinde tarih-saat.txt dosyasına kaydeder
    """
    # Klasör yolu
    folder_name = "Generated codes"
    
    # Klasör yoksa oluştur
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Dosya adını tarih ve saat olarak oluştur
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{current_time}.txt"
    file_path = os.path.join(folder_name, file_name)
    
    # Kodları dosyaya kaydet
    with open(file_path, 'w') as file:
        for code in codes:
            file.write(f"{code}\n")
    
    return file_path

def main():
    try:
        # Kullanıcıdan girdi al
        digit_count = int(input("Basamak sayısını giriniz: "))
        code_count = int(input("Kaç adet kod üretilsin?: "))
        
        # Değerlerin geçerliliğini kontrol et
        if digit_count <= 0 or code_count <= 0:
            raise ValueError("Basamak sayısı ve kod sayısı pozitif olmalıdır!")
        
        # Kodları üret
        codes = generate_unique_codes(digit_count, code_count)
        
        # Kodları dosyaya kaydet
        file_path = save_codes_to_file(codes)
        
        # Sonuçları yazdır
        print(f"\n{digit_count} basamaklı {code_count} adet benzersiz kod üretildi:")
        for i, code in enumerate(codes, 1):
            print(f"{i}. {code}")
        
        print(f"\nKodlar şu dosyaya kaydedildi: {file_path}")
        
    except ValueError as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    main()