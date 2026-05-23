---
name: data-analysis
description: تحليل البيانات: pandas, matplotlib, numpy, scikit-learn, reports
---

# مهارة تحليل البيانات

سير عمل كامل لتحليل البيانات باستخدام Python.

---

## 1. المكتبات الأساسية

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')
```

### التثبيت:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
```

---

## 2. قراءة البيانات

```python
# CSV
df = pd.read_csv("data.csv", encoding="utf-8")

# Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# JSON
df = pd.read_json("data.json")

# قاعدة بيانات
import sqlite3
conn = sqlite3.connect("database.db")
df = pd.read_sql("SELECT * FROM users", conn)
```

---

## 3. استكشاف البيانات (Exploratory Analysis)

```python
# نظرة سريعة
print(df.head())          # أول 5 صفوف
print(df.info())          # أنواع البيانات
print(df.describe())      # إحصائيات عامة
print(df.isnull().sum())  # القيم المفقودة
print(df.duplicated().sum())  # الصفوف المكررة

# توزيع القيم
print(df['column'].value_counts())
print(df['column'].value_counts(normalize=True))  # نسب مئوية
```

---

## 4. تنظيف البيانات

```python
# تعبئة القيم المفقودة
df['age'].fillna(df['age'].median(), inplace=True)
df['name'].fillna("غير معروف", inplace=True)

# إزالة المكررات
df.drop_duplicates(inplace=True)

# تحويل أنواع البيانات
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)

# إزالة القيم الشاذة (outliers)
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['salary'] >= Q1 - 1.5*IQR) & (df['salary'] <= Q3 + 1.5*IQR)]
```

---

## 5. التحليل (Analysis)

```python
# تجميع
df.groupby('category')['price'].agg(['mean', 'sum', 'count'])

# دمج جداول
merged = pd.merge(df1, df2, on='user_id', how='left')

# دوال متقدمة
df['total'] = df['quantity'] * df['price']
df['is_high'] = df['total'] > df['total'].median()

# Pivot Table
pivot = df.pivot_table(
    values='price',
    index='category',
    columns='region',
    aggfunc='mean'
)
```

---

## 6. التصور (Visualization)

```python
# رسم بياني خطي
plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['sales'], marker='o')
plt.title("المبيعات عبر الوقت")
plt.xlabel("التاريخ")
plt.ylabel("المبيعات")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/sales_trend.png")
plt.show()

# رسم أعمدة
df.groupby('category')['price'].sum().plot(kind='bar')
plt.title("المبيعات حسب الفئة")
plt.tight_layout()
plt.savefig("outputs/sales_by_category.png")

# Heatmap (ارتباط المتغيرات)
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title("مصفوفة الارتباط")
plt.tight_layout()
plt.savefig("outputs/correlation.png")
```

---

## 7. نماذج تعلم الآلة (اختياري)

```python
# تجهيز البيانات
X = df[['age', 'salary', 'purchases']]
y = df['is_premium']

# تقسيم
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# نموذج
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# تقييم
accuracy = model.score(X_test, y_test)
print(f"دقة النموذج: {accuracy:.2%}")

# أهمية المتغيرات
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print(importance)
```

---

## 8. حفظ النتائج

```python
# إلى CSV
df.to_csv("outputs/result.csv", index=False, encoding="utf-8")

# إلى Excel مع عدة sheets
with pd.ExcelWriter("outputs/report.xlsx") as writer:
    df.to_excel(writer, sheet_name="بيانات", index=False)
    importance.to_excel(writer, sheet_name="أهمية المتغيرات")

# حفظ الرسوم
# استخدم plt.savefig() بعد كل رسم
```

---

## 9. سير العمل الكامل

```python
import pandas as pd
import matplotlib.pyplot as plt

# 1. قراءة
df = pd.read_csv("data.csv")

# 2. فحص
print(df.info())
print(df.describe())

# 3. تنظيف
df.dropna(inplace=True)

# 4. تحليل
result = df.groupby('category')['sales'].sum()

# 5. رسم
result.plot(kind='bar')
plt.savefig("outputs/chart.png")

# 6. حفظ
df.to_csv("outputs/cleaned_data.csv", index=False)
```
