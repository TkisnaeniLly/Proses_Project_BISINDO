graph TD
    Start([User Mengakses Aplikasi]) --> Auth{Sudah Login?}
    
    Auth -->|Belum| Register[Registrasi Akun]
    Auth -->|Sudah| Home[Homepage/Katalog]
    
    Register --> FillProfile[Lengkapi Profil Customer]
    FillProfile --> AddAddress[Tambah Alamat Pengiriman]
    AddAddress --> Home
    
    Home --> Browse{Aktivitas User}
    
    Browse -->|Cari Produk| Search[Pencarian Produk]
    Browse -->|Lihat Kategori| Category[Filter Kategori/Brand]
    Browse -->|Produk Populer| Popular[Lihat Produk Popular]
    
    Search --> ProductList[List Produk]
    Category --> ProductList
    Popular --> ProductList
    
    ProductList --> ProductDetail[Detail Produk]
    
    ProductDetail --> CheckStock{Cek Stok}
    CheckStock -->|Stok Tersedia| Action{Pilih Aksi}
    CheckStock -->|Stok Habis| Wishlist[Tambah ke Wishlist]
    
    Action -->|Favorit| Wishlist
    Action -->|Beli Nanti| Cart[Tambah ke Keranjang]
    Action -->|Beli Sekarang| BuyNow[Buy Now]
    
    Wishlist --> Browse
    
    Cart --> UpdateCart[Update Qty/Item]
    UpdateCart --> CartPage[Halaman Keranjang]
    
    BuyNow --> Checkout[Proses Checkout]
    CartPage --> Checkout
    
    Checkout --> SelectAddress[Pilih Alamat Pengiriman]
    SelectAddress --> SelectShipping[Pilih Jasa Pengiriman]
    SelectShipping --> ApplyPromo{Gunakan Promo?}
    
    ApplyPromo -->|Ya| ValidatePromo[Validasi & Klaim Promo]
    ApplyPromo -->|Tidak| SelectPayment[Pilih Metode Pembayaran]
    ValidatePromo --> SelectPayment
    
    SelectPayment --> CreateOrder[Buat Pesanan]
    CreateOrder --> Payment[Proses Pembayaran]
    
    Payment --> PaymentStatus{Status Pembayaran}
    
    PaymentStatus -->|Berhasil| OrderConfirm[Konfirmasi Pesanan]
    PaymentStatus -->|Gagal| PaymentRetry{Coba Lagi?}
    
    PaymentRetry -->|Ya| Payment
    PaymentRetry -->|Tidak| OrderCancel[Pesanan Dibatalkan]
    
    OrderConfirm --> Shipping[Proses Pengiriman]
    Shipping --> Tracking[Tracking Paket]
    
    Tracking --> DeliveryStatus{Status Pengiriman}
    
    DeliveryStatus -->|Dalam Perjalanan| Tracking
    DeliveryStatus -->|Sampai| Received[Pesanan Diterima]
    
    Received --> Review[Berikan Review & Rating]
    Received --> ReturnOption{Perlu Retur?}
    
    ReturnOption -->|Ya| Return[Ajukan Return]
    ReturnOption -->|Tidak| Done([Selesai])
    
    Review --> Done
    Return --> ReturnProcess[Proses Return]
    ReturnProcess --> Done
    
    OrderCancel --> Done
    
    style Start fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Done fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style Register fill:#2196F3,stroke:#1565C0,color:#fff
    style FillProfile fill:#2196F3,stroke:#1565C0,color:#fff
    style AddAddress fill:#2196F3,stroke:#1565C0,color:#fff
    
    style Search fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Category fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Popular fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style ProductList fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style ProductDetail fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style Cart fill:#FF9800,stroke:#E65100,color:#fff
    style BuyNow fill:#FF9800,stroke:#E65100,color:#fff
    style UpdateCart fill:#FF9800,stroke:#E65100,color:#fff
    style CartPage fill:#FF9800,stroke:#E65100,color:#fff
    
    style Checkout fill:#F44336,stroke:#C62828,color:#fff
    style SelectAddress fill:#F44336,stroke:#C62828,color:#fff
    style SelectShipping fill:#F44336,stroke:#C62828,color:#fff
    style ValidatePromo fill:#F44336,stroke:#C62828,color:#fff
    style SelectPayment fill:#F44336,stroke:#C62828,color:#fff
    style CreateOrder fill:#F44336,stroke:#C62828,color:#fff
    
    style Payment fill:#E91E63,stroke:#AD1457,color:#fff
    style OrderConfirm fill:#E91E63,stroke:#AD1457,color:#fff
    
    style Shipping fill:#00BCD4,stroke:#00838F,color:#fff
    style Tracking fill:#00BCD4,stroke:#00838F,color:#fff
    style Received fill:#00BCD4,stroke:#00838F,color:#fff
    
    style Review fill:#8BC34A,stroke:#558B2F,color:#fff
    style Return fill:#795548,stroke:#4E342E,color:#fff
    style ReturnProcess fill:#795548,stroke:#4E342E,color:#fff
    
    style Wishlist fill:#673AB7,stroke:#4527A0,color:#fff
    style OrderCancel fill:#607D8B,stroke:#37474F,color:#fff
