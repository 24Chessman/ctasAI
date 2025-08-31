# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
# from sklearn.utils.class_weight import compute_class_weight
# import matplotlib.pyplot as plt
# import seaborn as sns
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# # Load the data
# df = pd.read_csv('buoy_labeled.csv')

# # 1. Preprocess the data with time series structure
# df['date'] = pd.to_datetime(df['date'])
# df['hour'] = df['date'].dt.hour
# df['day_of_year'] = df['date'].dt.dayofyear
# df['month'] = df['date'].dt.month

# # Encode the target variable
# df['label_encoded'] = df['label'].map({'NORMAL': 0, 'CYCLONE': 1})

# # Select features and target
# features = ['wind_speed', 'pressure', 'wave_height', 'water_level', 'hour', 'day_of_year', 'month']
# X = df[features]
# y = df['label_encoded']

# # Scale the features
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# # 2. Create time series sequences
# def create_sequences(X, y, time_steps=24):
#     Xs, ys = [], []
#     for i in range(len(X) - time_steps):
#         Xs.append(X[i:(i + time_steps)])
#         ys.append(y[i + time_steps])
#     return np.array(Xs), np.array(ys)

# TIME_STEPS = 24  # Use 24 hours of data to predict next label
# X_sequences, y_sequences = create_sequences(X_scaled, y.values, TIME_STEPS)

# # 3. Split the data respecting time order
# train_size = int(0.7 * len(X_sequences))
# val_size = int(0.15 * len(X_sequences))

# X_train, X_temp, y_train, y_temp = X_sequences[:train_size], X_sequences[train_size:], y_sequences[:train_size], y_sequences[train_size:]
# X_val, X_test, y_val, y_test = X_temp[:val_size], X_temp[val_size:], y_temp[:val_size], y_temp[val_size:]

# print(f"Training set size: {len(X_train)}")
# print(f"Validation set size: {len(X_val)}")
# print(f"Test set size: {len(X_test)}")
# print(f"Class distribution in training set: {np.bincount(y_train)}")

# # 4. Calculate class weights for imbalanced data
# class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
# class_weight_dict = {i: class_weights[i] for i in range(len(class_weights))}

# # 5. Build LSTM model
# model = Sequential([
#     LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
#     BatchNormalization(),
#     Dropout(0.3),
    
#     LSTM(32, return_sequences=False),
#     BatchNormalization(),
#     Dropout(0.3),
    
#     Dense(16, activation='relu'),
#     Dropout(0.2),
#     Dense(1, activation='sigmoid')
# ])

# model.compile(
#     optimizer=Adam(learning_rate=0.001),
#     loss='binary_crossentropy',
#     metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
# )

# # 6. Define callbacks
# early_stopping = EarlyStopping(monitor='val_auc', patience=10, restore_best_weights=True, mode='max')
# reduce_lr = ReduceLROnPlateau(monitor='val_auc', factor=0.5, patience=5, min_lr=1e-7, mode='max')

# # 7. Train the model
# history = model.fit(
#     X_train, y_train,
#     batch_size=32,
#     epochs=50,
#     validation_data=(X_val, y_val),
#     class_weight=class_weight_dict,
#     callbacks=[early_stopping, reduce_lr],
#     verbose=1
# )

# # 8. Evaluate on validation set
# y_val_pred = (model.predict(X_val) > 0.5).astype(int)
# y_val_prob = model.predict(X_val)

# print("Validation Set Performance:")
# print(classification_report(y_val, y_val_pred))
# print(f"Validation ROC-AUC: {roc_auc_score(y_val, y_val_prob):.4f}")

# # 9. Final evaluation on test set
# y_test_pred = (model.predict(X_test) > 0.5).astype(int)
# y_test_prob = model.predict(X_test)

# print("\nTest Set Performance:")
# print(classification_report(y_test, y_test_pred))
# print(f"Test ROC-AUC: {roc_auc_score(y_test, y_test_prob):.4f}")

# # 10. Confusion matrix
# cm = confusion_matrix(y_test, y_test_pred)
# plt.figure(figsize=(8, 6))
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
#             xticklabels=['NORMAL', 'CYCLONE'], 
#             yticklabels=['NORMAL', 'CYCLONE'])
# plt.title('Confusion Matrix')
# plt.ylabel('True Label')
# plt.xlabel('Predicted Label')
# plt.show()

# # 11. Plot training history
# plt.figure(figsize=(12, 4))
# plt.subplot(1, 2, 1)
# plt.plot(history.history['accuracy'], label='Training Accuracy')
# plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
# plt.title('Model Accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.legend()

# plt.subplot(1, 2, 2)
# plt.plot(history.history['loss'], label='Training Loss')
# plt.plot(history.history['val_loss'], label='Validation Loss')
# plt.title('Model Loss')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.legend()
# plt.tight_layout()
# plt.show()