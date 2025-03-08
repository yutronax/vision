import cv2
import numpy as np
from ultralytics import YOLO

# Modeli yükle
model = YOLO("runs/detect/apple/weights/best.pt")

# Kamerayı aç
cap = cv2.VideoCapture("elma.mp4")

# Mermi sayısı
mermi = 200

# Confidence Threshold (Eşik Değeri)q
confidence_threshold = 0.7

system, manuel = False, False

while True:
    # Kameradan görüntü al
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntü üzerinde tahmin yap
    results = model(frame)
    annotated_image = results[0].plot()

    boxes = results[0].boxes.xyxy  
    class_ids = results[0].boxes.cls.cpu().numpy() 
    names = results[0].names  
    confidences = results[0].boxes.conf.cpu().numpy()  

    enemy_class_name = "dusman"  
    enemy_class_id = next((k for k, v in names.items() if v == enemy_class_name), None)
    if enemy_class_id is None:
        print(f"Hata: '{enemy_class_name}' sınıfı modelde bulunamadı!")
        enemy_class_id = -1  

    # Tuş girişlerini oku (döngünün SONUNDA olmalı)
    tus = cv2.waitKey(10)

    # Mod değişiklikleri
    if tus == ord("o"):
        system = True
    elif tus == ord("y"):
        system = not system
    elif tus == ord("m"):
        system = False
        manuel = True

    if system or manuel:
        dusman_sayisi = sum((class_ids == enemy_class_id) & (confidences >= confidence_threshold))

        # Mermiyi düşman sayısına göre azalt
        mermi = max(0, mermi - dusman_sayisi)

        # X işareti ve kutular çiz
        for i, box in enumerate(boxes):
            if class_ids[i] == enemy_class_id and confidences[i] >= confidence_threshold:
                x_min, y_min, x_max, y_max = map(int, box)
                center_x, center_y = (x_min + x_max) // 2, (y_min + y_max) // 2

                cv2.line(annotated_image, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20), (0, 0, 255), 3)
                cv2.line(annotated_image, (center_x + 20, center_y - 20), (center_x - 20, center_y + 20), (0, 0, 255), 3)
                cv2.rectangle(annotated_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # Mermi sayısını göster
        cv2.putText(annotated_image, f"Mermi: {mermi}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        manuel = False

    # Mermi bittiyse uyarı ver
    if mermi <= 0:
        cv2.putText(annotated_image, "Mermi bitti!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        break
    # Görüntüyü göster
    cv2.imshow("Real-Time Detection",annotated_image)

    # Çıkış için 'q' tuşuna basıldığında döngüden çık
    if tus == ord('q'):
        break

# Kamerayı ve pencereyi kapat
cap.release()
cv2.destroyAllWindows()
