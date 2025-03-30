from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import datetime

def read_codes_from_file(file_path):
    """
    Txt dosyasından kodları okur
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def create_pdf_from_codes(codes, output_folder="Generated PDFs"):
    """
    Kodları PDF formatında düzenler
    """
    # PDF klasörü yoksa oluştur
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # PDF dosya adını oluştur
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_filename = os.path.join(output_folder, f"codes_{current_time}.pdf")
    
    # PDF boyutlarını ayarla
    page_width, page_height = A4
    
    # PDF oluştur
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    
    # Font ve boyut ayarları
    font_name = "Helvetica"
    font_size = 12
    c.setFont(font_name, font_size)
    
    # Başlangıç koordinatları
    x_start = 50  # Sol kenar boşluğu
    y_start = page_height - 50  # Üst kenar boşluğu
    
    # Her satır ve sütun arası mesafe
    x_spacing = 150  # Yatay mesafe
    y_spacing = 30   # Dikey mesafeyi 15'ten 30'a çıkardık
    
    # Bir sayfadaki maksimum sütun ve satır sayısı
    max_columns = int((page_width - 2 * x_start) // x_spacing) + 1
    codes_per_page = max_columns * int((y_start - 50) // y_spacing)
    
    # Kodları yerleştir
    for i, code in enumerate(codes):
        # Yeni sayfa gerekiyor mu kontrol et
        if i > 0 and i % codes_per_page == 0:
            c.showPage()
            c.setFont(font_name, font_size)
            current_y = y_start
        
        # Koordinatları hesapla
        column = (i % codes_per_page) % max_columns
        row = (i % codes_per_page) // max_columns
        
        x = x_start + (column * x_spacing)
        y = y_start - (row * y_spacing)
        
        # Kodu yerleştir
        c.drawString(x, y, code)
    
    # PDF'i kaydet
    c.save()
    return pdf_filename

def main():
    try:
        # Generated codes klasöründeki en son txt dosyasını bul
        codes_folder = "Generated codes"
        if not os.path.exists(codes_folder):
            raise ValueError("'Generated codes' klasörü bulunamadı!")
        
        txt_files = [f for f in os.listdir(codes_folder) if f.endswith('.txt')]
        if not txt_files:
            raise ValueError("'Generated codes' klasöründe txt dosyası bulunamadı!")
        
        # En son oluşturulan txt dosyasını al
        latest_file = max(txt_files, key=lambda x: os.path.getctime(os.path.join(codes_folder, x)))
        file_path = os.path.join(codes_folder, latest_file)
        
        # Kodları oku
        codes = read_codes_from_file(file_path)
        
        # PDF oluştur
        pdf_path = create_pdf_from_codes(codes)
        
        print(f"PDF başarıyla oluşturuldu: {pdf_path}")
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    main() 