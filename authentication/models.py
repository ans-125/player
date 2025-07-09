from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """نموذج مستخدم مخصص يتضمن حقول إضافية"""
    
    phone = models.CharField(
        max_length=15, 
        unique=True, 
        verbose_name="رقم الهاتف",
        help_text="رقم الهاتف يجب أن يكون فريداً"
    )
    birth_year = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="سنة الميلاد"
    )
    city = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="المدينة"
    )
    is_admin = models.BooleanField(
        default=False, 
        verbose_name="مدير النظام"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="تاريخ الإنشاء"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="تاريخ التحديث"
    )

    # استخدام رقم الهاتف كحقل تسجيل الدخول بدلاً من اسم المستخدم
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'first_name']

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"

    def __str__(self):
        return f"{self.first_name} ({self.phone})" if self.first_name else self.phone

    def get_full_name(self):
        """إرجاع الاسم الكامل للمستخدم"""
        return f"{self.first_name} {self.last_name}".strip() or self.phone

    def get_short_name(self):
        """إرجاع الاسم المختصر للمستخدم"""
        return self.first_name or self.phone

