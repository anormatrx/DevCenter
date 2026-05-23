---
name: android-build
description: بناء Android: Gradle, APK, AAB, signing, CI/CD
---

# مهارة بناء Android

سير عمل كامل لبناء وتوقيع ونشر تطبيقات Android.

---

## 1. أوامر Gradle الأساسية

```bash
# تنظيف
./gradlew clean

# بناء Debug
./gradlew assembleDebug

# بناء Release
./gradlew assembleRelease

# اختبارات
./gradlew test

# اختبارات Android
./gradlew connectedAndroidTest

# تقرير الـ lint
./gradlew lint

# تحليل التبعيات
./gradlew app:dependencies
```

---

## 2. توقيع التطبيق (Signing)

### app/build.gradle.kts:
```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file("keystore.jks")
            storePassword = System.getenv("STORE_PASSWORD")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

### إنشاء Keystore:
```bash
keytool -genkey -v -keystore keystore.jks \
  -alias myalias -keyalg RSA -keysize 2048 \
  -validity 10000
```

---

## 3. إصدارات APK و AAB

```bash
# APK
./gradlew assembleRelease
# app/build/outputs/apk/release/app-release.apk

# AAB (Google Play)
./gradlew bundleRelease
# app/build/outputs/bundle/release/app-release.aab
```

---

## 4. قواعد ProGuard

### proguard-rules.pro:
```
# احتفظ بالنماذج
-keep class com.myapp.models.** { *; }

# إزالة الـ logging في الإصدار
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
}

# Retrofit
-keepattributes Signature
-keep class retrofit2.** { *; }
```

---

## 5. متغيرات البيئة

### gradle.properties (لا ترفع على Git):
```properties
MYAPP_UPLOAD_STORE_PASSWORD=***
MYAPP_UPLOAD_KEY_PASSWORD=***
MYAPP_UPLOAD_KEY_ALIAS=myalias
```

---

## 6. رفع الأرقام تلقائياً

### app/build.gradle.kts:
```kotlin
android {
    defaultConfig {
        versionCode = System.getenv("CI_PIPELINE_ID")?.toInt() ?: 1
        versionName = "1.0.${versionCode}"
    }
}
```

---

## 7. CI/CD مع GitHub Actions

### .github/workflows/android.yml:
```yaml
name: Android CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: 17
      - run: chmod +x gradlew
      - run: ./gradlew lint
      - run: ./gradlew test
      - run: ./gradlew assembleDebug
      - uses: actions/upload-artifact@v4
        with:
          name: app-debug
          path: app/build/outputs/apk/debug/
```

---

## 8. رفع إلى Google Play

```bash
# يتطلب: service account + publisher API
# استخدم GitHub Action: r0adkll/upload-google-play
```

### GitHub Actions (رفع تلقائي):
```yaml
- uses: r0adkll/upload-google-play@v1
  with:
    serviceAccountJsonPlainText: ${{ secrets.SERVICE_ACCOUNT_JSON }}
    packageName: com.myapp
    releaseFiles: app/build/outputs/bundle/release/app-release.aab
    track: production
```
