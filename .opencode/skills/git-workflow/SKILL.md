---
name: git-workflow
description: إدارة سير عمل Git كاملة (commits, branches, merge, rebase, حل تعارضات)
---

# مهارة Git الشاملة

إرشادات كاملة للتعامل مع Git في المشروع.

---

## 1. الـ Commits

### كتابة رسائل commit واضحة:
```
- النمط: `type(scope): رسالة مختصرة`
- type: feat, fix, docs, style, refactor, test, chore
- scope: اسم المكون (اختياري)
```

**أمثلة:**
```
feat(chat): إضافة إرسال الصور في الدردشة
fix(auth): إصلاح خطأ تسجيل الدخول بالبريد الإلكتروني
docs: تحديث README.md
```

### سير العمل قبل الـ commit:
```bash
git status              # تعرف وين التغييرات
git diff                # راجع التغييرات بالتفصيل
git add <file>          # أضف ملف معين
git add -p              # أضف أجزاء محددة (أفضل)
git commit -m "type: رسالة"
```

---

## 2. الفروع (Branches)

### نظام التسمية:
```
feature/   → feature/add-login-page
fix/       → fix/null-pointer-error
docs/      → docs/api-docs
refactor/  → refactor/user-service
test/      → test/chat-api
release/   → release/v1.2.0
```

### الأوامر الأساسية:
```bash
git branch                     # شوف الفروع
git checkout -b feature/xxx    # أنشئ فرع جديد وانتقل له
git switch feature/xxx         # انتقل لفرع (أحدث من checkout)
git branch -d feature/xxx      # احذف فرع (بعد الدمج)
git push -u origin feature/xxx # ارفع الفرع للـ remote
```

---

## 3. الدمج (Merge) وإعادة التنظيم (Rebase)

### Merge (دمج عادي):
```bash
git checkout main
git merge feature/xxx          # ادمج الفرع مع main
```

### Rebase (إعادة تنظيم - تاريخ نظيف):
```bash
git checkout feature/xxx
git rebase main                # ضع تغييراتك فوق main
git checkout main
git merge feature/xxx          # Fast-forward merge
```

### متى تستخدم كل واحد؟
- **Merge**: للفروع الطويلة، الفرق الكبيرة
- **Rebase**: للفروع القصيرة، التحديثات البسيطة
- **Squash**: دمج عدة commits في commit واحد قبل الـ merge

---

## 4. حل تعارضات الدمج (Merge Conflicts)

### عند حدوث تعارض:
```bash
# 1. شوف الملفات المتعارضة
git status

# 2. افتح كل ملف وابحث عن:
<<<<<<< HEAD
# هذا الكود من الفرع الحالي
=======
# هذا الكود من الفرع المندمج
>>>>>>> feature/xxx

# 3. اختر الكود الصحيح واحذف العلامات
# 4. أضف الملفات بعد الحل:
git add <file>
git commit                 # Git يكمل الـ merge تلقائياً
```

### نصائح:
- استخدم `git mergetool` إذا تريد واجهة رسومية
- لا تخف من التعارضات — هي طبيعية
- اتصل بفريقك إذا التعارض كبير

---

## 5. التراجع والإصلاح

```bash
# تراجع عن آخر commit (وخلي التغييرات في staging)
git reset --soft HEAD~1

# تراجع عن آخر commit (وخلي التغييرات في working directory)
git reset --mixed HEAD~1

# تراجع نهائي (احذف التغييرات)
git reset --hard HEAD~1

# تراجع عن ملف معين لآخر commit
git checkout -- <file>

# عدّل رسالة آخر commit
git commit --amend -m "رسالة جديدة"
```

---

## 6. الـ Tags

```bash
git tag v1.0.0                    # أنشئ tag
git tag -a v1.0.0 -m "الإصدار الأول"  # tag مع رسالة
git push origin v1.0.0            # ارفع tag
git tag                           # شوف كل الـ tags
git push --tags                   # ارفع كل الـ tags
```

---

## 7. رفع وسحب التغييرات

```bash
git pull --rebase         # اسحب التغييرات مع rebase (أنظف)
git push                  # ارفع التغييرات
git push --force-with-lease  # ارفع قسرياً (آمن من force push)
```

### تحذيرات:
- **لا تستخدم `git push --force`** على الفروع المشتركة
- استخدم `--force-with-lease` بدلاً منه (يتأكد أنك ما تمسح تغييرات أحد)
- اسحب التغييرات قبل الرفع عشان تتجنب التعارضات

---

## 8. استراتيجيات متقدمة

### Cherry-pick (اختيار commit معين):
```bash
git cherry-pick <commit-hash>     # خذ commit من فرع آخر
```

### Stash (حفظ التغييرات المؤقتة):
```bash
git stash                         # احفظ التغييرات مؤقتاً
git stash pop                     # استرجعها واحذف من stash
git stash list                    # شوف المحفوظات
git stash drop                    # احذف آخر stash
```

### Bisect (البحث عن commit سبب خطأ):
```bash
git bisect start
git bisect bad HEAD               # هذا commit فيه خطأ
git bisect good v1.0.0            # هذا commit كان شغال
# Git يبحث تلقائياً: جرب كل commit وقل good/bad
git bisect reset                  # ارجع للوضع الطبيعي
```

---

## 9. سير العمل اليومي المقترح

```bash
# بداية اليوم
git checkout main
git pull --rebase

# ابدأ شغل جديد
git checkout -b feature/my-task

# ... اشتغل على الكود ...

# قبل الـ commit
git diff
git add -p
git commit -m "feat: خلصت المهمة"

# ارفع التغييرات
git pull --rebase origin main     # تأكد أنك محدث
git push -u origin feature/my-task

# اسوي Pull Request (على GitHub/GitLab)
```

---

## 10. حل المشاكل الشائعة

| المشكلة | الحل |
|---------|------|
| `commit --amend` فتح vim وأنا ما أعرف vim | `git config --global core.editor "code --wait"` |
| نسيت أضيف ملف في آخر commit | `git add <file>` ثم `git commit --amend --no-edit` |
| أبي ألغي push آخر | `git revert HEAD~1` (آمن) |
| تعارض كبير وأبي ألغي الـ merge | `git merge --abort` |
| سويت rebase خطأ | `git rebase --abort` |
| فقدت commits بعد reset | `git reflog` → `git reset --hard <hash>` |

---

## 11. إعدادات Git مفيدة

```bash
# محرر النصوص
git config --global core.editor "code --wait"

# أسماء الفروع
git config --global init.defaultBranch main

# تذكر كلمة المرور
git config --global credential.helper store

# aliases مفيدة
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.st status
git config --global alias.last 'log -1 HEAD'
```
