def siparis_hesapla():
    print("🎉 Kıyafet Sipariş Programına Hoş Geldiniz! 🎉")
    
    # Fiyatlar
    fiyatlar = {
        'Pantolon': 1350,
        'Gömlek': 850,
        'Ayakkabı': 1500,
        'Tişört': 250,
        'Çorap': 150,
        'Mont': 850
    }

    # Sipariş listesi ve toplam tutar
    siparisler = {}
    toplam_tutar = 0

    # Ana ürünleri gösterme
    print("\n📋 Ana Kıyafet Seçenekleri:")
    for kiya in ['Pantolon', 'Gömlek', 'Ayakkabı']:
        print(f"- {kiya}: {fiyatlar[kiya]} TL")

    # Birden fazla ana ürün seçme
    ana_secimler = input("Sipariş vermek istediğiniz kıyafetleri virgülle ayırarak yazın (örn. Pantolon, Gömlek): ").strip().split(',')

    # Seçilen ana ürünlerin adetlerini alma
    for secim in ana_secimler:
        secim = secim.strip().capitalize()
        if secim in fiyatlar:
            try:
                adet = int(input(f"{secim} almak istediğiniz adedi girin (örn. 2): "))
                if adet > 0:
                    siparisler[secim] = siparisler.get(secim, 0) + adet
                    toplam_tutar += fiyatlar[secim] * adet
                    print(f"{adet} adet {secim} eklendi. Toplam tutar: {toplam_tutar} TL")
                else:
                    print("❌ Lütfen geçerli bir adet girin.")
            except ValueError:
                print("⚠️ Lütfen bir sayı girin.")
        else:
            print(f"❌ Geçersiz seçim: {secim}")

    # Ekstra ürünleri görmek isteyip istemediğini sorma
    ekstra_secim = input("\nEkstra ürünleri görmek ister misiniz? (evet/hayır): ").strip().lower()

    if ekstra_secim == 'evet':
        print("\n✨ Ekstra Kıyafet Seçeneklerimiz:")
        for ek in ['Tişört', 'Çorap', 'Mont']:
            print(f"- {ek}: {fiyatlar[ek]} TL")

        # Birden fazla ekstra ürün seçme
        ekstra_secimler = input("Hangi ekstra kıyafetleri almak istersiniz? (örn. Tişört, Mont): ").strip().split(',')

        # Seçilen ekstra ürünlerin adetlerini alma
        for ekstra_kıyafet in ekstra_secimler:
            ekstra_kıyafet = ekstra_kıyafet.strip().capitalize()
            if ekstra_kıyafet in fiyatlar:
                try:
                    adet = int(input(f"{ekstra_kıyafet} almak istediğiniz adedi girin (örn. 1): "))
                    if adet > 0:
                        siparisler[ekstra_kıyafet] = siparisler.get(ekstra_kıyafet, 0) + adet
                        toplam_tutar += fiyatlar[ekstra_kıyafet] * adet
                        print(f"{adet} adet {ekstra_kıyafet} eklendi. Toplam tutar: {toplam_tutar} TL")
                    else:
                        print("❌ Lütfen geçerli bir adet girin.")
                except ValueError:
                    print("⚠️ Lütfen bir sayı girin.")
            else:
                print(f"❌ Geçersiz seçim: {ekstra_kıyafet}")

    # Sipariş tamamlamak için son onay
    son_onay = input("\nSiparişinizi tamamlamak ister misiniz? (evet/hayır): ").strip().lower()
    if son_onay == 'evet':
        # Sipariş detayları
        print("\n🛒 Siparişiniz:")
        for urun, adet in siparisler.items():
            print(f"- {urun}: {adet} adet ({fiyatlar[urun]} TL/adet)")

        print(f"\n💰 Toplam Tutar: {toplam_tutar} TL")
        print("Teşekkürler! Siparişiniz alınmıştır.")
    else:
        # Siparişi iptal veya ekleme seçeneği
        iptal_mi_ekleme_mi = input("Siparişinizi iptal mi etmek istiyorsunuz yoksa ürün mü eklemek istiyorsunuz? (iptal/ekle): ").strip().lower()
        
        if iptal_mi_ekleme_mi == 'iptal':
            print("Siparişiniz iptal edilmiştir.")
        elif iptal_mi_ekleme_mi == 'ekle':
            print("\n📋 Tüm Ürün Seçenekleri:")
            for urun, fiyat in fiyatlar.items():
                print(f"- {urun}: {fiyat} TL")

            # Birden fazla ürün seçme
            ekleme_secimler = input("Hangi ürünleri eklemek istersiniz? (örn. Pantolon, Çorap): ").strip().split(',')

            # Seçilen ürünlerin adetlerini alma
            for urun in ekleme_secimler:
                urun = urun.strip().capitalize()
                if urun in fiyatlar:
                    try:
                        adet = int(input(f"{urun} almak istediğiniz adedi girin (örn. 1): "))
                        if adet > 0:
                            siparisler[urun] = siparisler.get(urun, 0) + adet
                            toplam_tutar += fiyatlar[urun] * adet
                            print(f"{adet} adet {urun} eklendi. Toplam tutar: {toplam_tutar} TL")
                        else:
                            print("❌ Lütfen geçerli bir adet girin.")
                    except ValueError:
                        print("⚠️ Lütfen bir sayı girin.")
                else:
                    print(f"❌ Geçersiz seçim: {urun}")

            # Siparişin son hali
            print("\n🛒 Güncellenmiş Siparişiniz:")
            for urun, adet in siparisler.items():
                print(f"- {urun}: {adet} adet ({fiyatlar[urun]} TL/adet)")

            print(f"\n💰 Toplam Tutar: {toplam_tutar} TL")
            print("Teşekkürler! Siparişiniz güncellenmiştir.")
        else:
            print("Geçersiz seçim. Sipariş iptal edilmiştir.")

# Programı çalıştır
siparis_hesapla()
