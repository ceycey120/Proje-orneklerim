!pip install tensorflow scipy matplotlib

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.utils import get_file   #Bu fonksiyon kullanılarak aşağıdaki scipy.io.loadmat yükleniyor.
from scipy.io import loadmat
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
# SVHN veri setini indirme ve yükleme
def load_svhn():
  """
   Dosya URL'leri. SVHN veri setini indirir ve yükler. Verileri numpy array formatında döndürür.
  """

  train_url = 'http://ufldl.stanford.edu/housenumbers/train_32x32.mat'
  test_url = 'http://ufldl.stanford.edu/housenumbers/test_32x32.mat'

  # Dosyaları indir

  train_path = get_file('train_32x32.mat', origin=train_url)
  test_path = get_file('test_32x32.mat', origin=test_url)

  # Dosyaları yükle
  test_data = loadmat(test_path)
  train_data = loadmat(train_path)

  # Verileri ayır

  x_train = np.transpose(train_data['X'], (3, 0, 1, 2))
  y_train = train_data['y'].flatten()
  x_test = np.transpose(test_data['X'], (3, 0, 1, 2))
  y_test = test_data['y'].flatten()

  # SVHN datasetlerinde '0' sayısı 10 olarak etiketlenmiş. Bu durumu düzenleyelim.

  y_train[y_train == 10] = 0
  y_test[y_test == 10] = 0

  return (x_train, y_train), (x_test, y_test)

# Veri setini yükle

(x_train, y_train), (x_test, y_test) = load_svhn()

# Verilerin boyutları sonuçlarını yazdır

print(f'x_train shape: {x_train.shape}')
print(f'y_train shape: {y_train.shape}')
print(f'x_test shape: {x_test.shape}')
print(f'y_test shape: {y_test.shape}')
# Veri setindeki örnek görüntülerden bazılarını görselleştir

fig, axes = plt.subplots(1, 10, figsize=(20, 2))
for i in range(10):
  axes[i].imshow(x_train[i])
  axes[i].set_title(y_train[i])
  axes[i].axis('off')
plt.show()

# Verileri normalize et.
# Görüntü verileri 0-255 px arasında değişiyor. 0 ile 1 arasında ölçeklendirmek adına piksel değerini 255'e böldük.

x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Etikerleri one-hot encode et
# (kategorik verileri sayısal verilere dönüştürme tekniğidir.)

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
# Model 1: CNN Modeli oluştur

cnn_model = Sequential([ #Keras'ta model tanımlama için bu sınıf kullanılır.
    Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    #İlk konvolsüyon katman. Her biri 3x3 boyutunda 32 filtre kullanılacak, input_shape giriş görüntülerinin boyutunu belirtir.
    MaxPooling2D((2, 2)),
    #2x2 pencereler kullanılır konvolüsyon katmanından elde edilen özellik haritalarını havuzlar.
    Conv2D(64, (3, 3), activation='relu'), #ikinci konvolüsyon ve pooling katmanı. 64 filtre kullanıyoruz.
    MaxPooling2D((2, 2)),
    Flatten(), #konvolsüyon ve havuzlamadaki 2 boyutlu verileri tek boyutlu vektörlere çevirmeye yarar.
    Dense(128, activation='relu'), #Dense katmanları tam bağlantılı nöron katmanlarıdır.
    Dense(10, activation='softmax'), #Üstte 128 nöron ve relu aktivasyon fonksiyonu burada 10 nöron ve softmax aktivasyon kodu
])

# Eğitim için modeli derle. 'adam' optimizasyon algoritması, 'categorical_crossentropy' kayıp fonksiyonu, izlenecek metrik 'accuracy'

cnn_model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Modeli Eğit. Eğitim için 'fit' metodu. 10 epochs boyunca eğitiyoruz. Her epoch sonunda doğrulama yapıyoruz.

cnn_history = cnn_model.fit(x_train, y_train, epochs=10, batch_size=64, validation_data=(x_test, y_test))

#Modelin eğitilme sürecini görselleştir. Doğruluk ve kayıp değerleri görselleştir.

plt.plot(cnn_history.history['accuracy'], label='CNN accuracy')
plt.plot(cnn_history.history['val_accuracy'], label = 'CNN val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.show()

# Modelimizi test seti üzerinde değerlendirme

cnn_test_loss, cnn_test_acc = cnn_model.evaluate(x_test, y_test, verbose=2)
print(f'Test accuracy: {test_acc}')
# Logistic Regression modelini kullanabilmek için verileri 2D forma dönüştürmemiz gerekiyor.
# Görüntülerin orijinal boyutu (32, 32, 3), bu nedenle verileri (32*32*3,) şekline dönüştürüyoruz.

x_train_flat = x_train.reshape((x_train.shape[0], -1))
x_test_flat = x_test.reshape((x_test.shape[0], -1))

# Logistic Regression modelini tanımlıyoruz ve eğitiyoruz.
logistic_model = LogisticRegression(max_iter=1000)
logistic_model.fit(x_train_flat, y_train)

# Test verilerini kullanarak tahminler yapıyoruz.
logistic_predictions = logistic_model.predict(x_test_flat)

# Logistic Regression modelinin performansını değerlendirmek için çeşitli metrikleri hesaplıyoruz.
logistic_acc = accuracy_score(y_test, logistic_predictions)
logistic_f1 = f1_score(y_test, logistic_predictions, average='weighted')
logistic_precision = precision_score(y_test, logistic_predictions, average='weighted')
logistic_recall = recall_score(y_test, logistic_predictions, average='weighted')
logistic_roc_auc = roc_auc_score(y_test, to_categorical(logistic_predictions, 10), multi_class='ovo')

# Sonuçları yazdırıyoruz.
print(f'Logistic Regression Test accuracy: {logistic_acc}')
print(f'Logistic Regression F1-Score: {logistic_f1}')
print(f'Logistic Regression Precision: {logistic_precision}')
print(f'Logistic Regression Recall: {logistic_recall}')
print(f'Logistic Regression ROC AUC: {logistic_roc_auc}')

# Random Forest modeli oluştur ve eğit

# Random Forest modeli de verilerin 2D forma dönüştürülmesini gerektirir.
# Bu nedenle aynı şekilde verileri düzleştiriyoruz.
random_forest_model = RandomForestClassifier(n_estimators=100)

# Random Forest modelini tanımlıyoruz ve eğitiyoruz.
random_forest_model.fit(x_train_flat, y_train)

# Test verilerini kullanarak tahminler yapıyoruz.
random_forest_predictions = random_forest_model.predict(x_test_flat)

# Random Forest modelinin performansını değerlendirmek için F1-Score, Precision, Recall ve ROC AUC metriklerini hesaplıyoruz.
random_forest_acc = accuracy_score(y_test, random_forest_predictions)
random_forest_f1 = f1_score(y_test, random_forest_predictions, average='weighted')
random_forest_precision = precision_score(y_test, random_forest_predictions, average='weighted')
random_forest_recall = recall_score(y_test, random_forest_predictions, average='weighted')
random_forest_roc_auc = roc_auc_score(y_test, to_categorical(random_forest_predictions, 10), multi_class='ovo')

# Sonuçları yazdırıyoruz.
print(f'Random Forest Test accuracy: {random_forest_acc}')
print(f'Random Forest F1-Score: {random_forest_f1}')
print(f'Random Forest Precision: {random_forest_precision}')
print(f'Random Forest Recall: {random_forest_recall}')
print(f'Random Forest ROC AUC: {random_forest_roc_auc}')
# ROC eğrisi Logistic Regression çizimi

# ROC eğrisini çizebilmek için False Positive Rate (FPR) ve True Positive Rate (TPR) değerlerini hesaplıyoruz.
fpr, tpr, _ = roc_curve(y_test, logistic_model.predict_proba(x_test_flat)[:, 1], pos_label=1)

# ROC eğrisini çiziyoruz.
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % logistic_roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()