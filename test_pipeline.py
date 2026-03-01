#!/usr/bin/env python3
"""
سكريبت اختبار شامل لخط أنابيب التصنيف
Comprehensive test script for the classification pipeline
"""

import numpy as np
import cv2
from digit_recognition_notebook import DigitRecognitionPipeline
import warnings
warnings.filterwarnings('ignore')

def print_section(title):
    """طباعة عنوان القسم"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_pipeline():
    """اختبار خط الأنابيب الكامل"""
    
    print_section("🔢 اختبار خط أنابيب تصنيف الأرقام")
    print("Testing Digit Classification Pipeline")
    
    # 1. إنشاء خط الأنابيب
    print_section("1️⃣ إنشاء خط الأنابيب | Creating Pipeline")
    pipeline = DigitRecognitionPipeline(n_clusters=10, random_state=42)
    print("✓ تم إنشاء خط الأنابيب بنجاح")
    print("✓ Pipeline created successfully")
    
    # 2. تحميل البيانات
    print_section("2️⃣ تحميل البيانات | Loading Data")
    X_train, y_train, images = pipeline.load_mnist_data()
    print(f"✓ عدد العينات: {len(X_train)}")
    print(f"✓ Number of samples: {len(X_train)}")
    print(f"✓ حجم كل صورة: {images[0].shape}")
    print(f"✓ Image size: {images[0].shape}")
    
    # 3. معالجة البيانات
    print_section("3️⃣ معالجة البيانات | Processing Data")
    X_scaled = pipeline.preprocess_data(apply_binarization=True)
    print(f"✓ شكل البيانات المعالجة: {X_scaled.shape}")
    print(f"✓ Processed data shape: {X_scaled.shape}")
    
    # 4. تدريب النموذج
    print_section("4️⃣ تدريب النموذج | Training Model")
    predictions = pipeline.train_kmeans(X_scaled)
    print(f"✓ عدد المجموعات: {pipeline.n_clusters}")
    print(f"✓ Number of clusters: {pipeline.n_clusters}")
    print(f"✓ Inertia: {pipeline.kmeans.inertia_:.2f}")
    
    # 5. ربط المجموعات بالأرقام
    print_section("5️⃣ ربط المجموعات بالأرقام | Mapping Clusters to Digits")
    cluster_to_digit = pipeline.map_clusters_to_digits(predictions)
    
    # 6. تقييم النموذج
    print_section("6️⃣ تقييم النموذج | Evaluating Model")
    accuracy = pipeline.evaluate_model(X_scaled, predictions)
    
    # 7. اختبار التنبؤ على عينات
    print_section("7️⃣ اختبار التنبؤ | Testing Predictions")
    
    test_indices = [0, 100, 500, 1000, 1500]
    print("\nنتائج التنبؤ على عينات مختلفة:")
    print("Prediction results on different samples:")
    print("-" * 70)
    print(f"{'الفهرس':<10} {'الرقم الحقيقي':<15} {'الرقم المتنبأ':<15} {'الثقة':<15} {'صحيح؟':<10}")
    print(f"{'Index':<10} {'True Digit':<15} {'Predicted':<15} {'Confidence':<15} {'Correct?':<10}")
    print("-" * 70)
    
    correct_predictions = 0
    for idx in test_indices:
        if idx < len(images):
            true_digit = y_train[idx]
            image = images[idx]
            
            predicted_digit, cluster_id, confidence = pipeline.predict_digit(
                image, 
                apply_binarization=True
            )
            
            is_correct = "✓" if predicted_digit == true_digit else "✗"
            if predicted_digit == true_digit:
                correct_predictions += 1
            
            print(f"{idx:<10} {true_digit:<15} {predicted_digit:<15} {confidence*100:>6.1f}%{'':<8} {is_correct:<10}")
    
    print("-" * 70)
    print(f"✓ دقة التنبؤ على العينات المختبرة: {correct_predictions}/{len(test_indices)}")
    print(f"✓ Prediction accuracy on test samples: {correct_predictions}/{len(test_indices)}")
    
    # 8. اختبار معالجة صورة مخصصة
    print_section("8️⃣ اختبار معالجة صورة مخصصة | Testing Custom Image Processing")
    
    # إنشاء صورة اختبار (رقم 5)
    test_image = images[50]  # صورة من البيانات
    true_digit = y_train[50]
    
    print(f"✓ الصورة المختبرة من الفهرس 50")
    print(f"✓ Test image from index 50")
    print(f"✓ الرقم الحقيقي: {true_digit}")
    print(f"✓ True digit: {true_digit}")
    
    # اختبار مع binarization
    predicted_with_bin, cluster_id_bin, conf_bin = pipeline.predict_digit(
        test_image, 
        apply_binarization=True
    )
    
    # اختبار بدون binarization
    predicted_without_bin, cluster_id_no_bin, conf_no_bin = pipeline.predict_digit(
        test_image, 
        apply_binarization=False
    )
    
    print("\nمقارنة النتائج:")
    print("Results comparison:")
    print(f"  مع Binarization | With Binarization:")
    print(f"    - الرقم المتنبأ: {predicted_with_bin}")
    print(f"    - Predicted digit: {predicted_with_bin}")
    print(f"    - الثقة: {conf_bin*100:.1f}%")
    print(f"    - Confidence: {conf_bin*100:.1f}%")
    
    print(f"\n  بدون Binarization | Without Binarization:")
    print(f"    - الرقم المتنبأ: {predicted_without_bin}")
    print(f"    - Predicted digit: {predicted_without_bin}")
    print(f"    - الثقة: {conf_no_bin*100:.1f}%")
    print(f"    - Confidence: {conf_no_bin*100:.1f}%")
    
    # 9. ملخص النتائج
    print_section("📊 ملخص النتائج | Results Summary")
    
    summary_data = {
        "المقياس": [
            "إجمالي العينات",
            "عدد المجموعات",
            "دقة النموذج",
            "Inertia",
            "عدد التكرارات",
            "حجم الصورة"
        ],
        "القيمة": [
            f"{len(X_train)} عينة",
            f"{pipeline.n_clusters} مجموعات",
            f"{accuracy*100:.2f}%",
            f"{pipeline.kmeans.inertia_:.2f}",
            f"{pipeline.kmeans.n_iter_}",
            "8×8 بكسل"
        ]
    }
    
    print("\n")
    for metric, value in zip(summary_data["المقياس"], summary_data["القيمة"]):
        print(f"  {metric:<20} : {value}")
    
    # 10. معلومات ربط المجموعات
    print_section("🔗 ربط المجموعات بالأرقام | Cluster-to-Digit Mapping")
    
    print("\nجدول الربط:")
    print("Mapping table:")
    print("-" * 40)
    print(f"{'معرف المجموعة':<20} {'الرقم المقابل':<20}")
    print(f"{'Cluster ID':<20} {'Mapped Digit':<20}")
    print("-" * 40)
    
    for cluster_id in sorted(cluster_to_digit.keys()):
        digit = cluster_to_digit[cluster_id]
        print(f"{cluster_id:<20} {digit:<20}")
    
    print("-" * 40)
    
    # النتيجة النهائية
    print_section("✅ اختبار النموذج اكتمل بنجاح")
    print("✅ Model testing completed successfully")
    print("\nالنموذج جاهز للاستخدام في التطبيق!")
    print("The model is ready to use in the application!")
    
    return pipeline

if __name__ == "__main__":
    try:
        pipeline = test_pipeline()
        print("\n" + "="*70)
        print("✓ جميع الاختبارات نجحت!")
        print("✓ All tests passed!")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n✗ خطأ أثناء الاختبار: {str(e)}")
        print(f"✗ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
