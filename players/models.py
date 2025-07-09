from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Player(models.Model):
    """نموذج اللاعب"""
    
    POSITION_CHOICES = [
        ('حارس مرمى', 'حارس مرمى'),
        ('مدافع', 'مدافع'),
        ('وسط', 'وسط'),
        ('مهاجم', 'مهاجم'),
    ]
    
    NATIONALITY_CHOICES = [
        ('سعودي', 'سعودي'),
        ('أجنبي', 'أجنبي'),
        ('مواليد السعودية', 'مواليد السعودية'),
    ]
    
    CITY_CHOICES = [
        ('الرياض', 'الرياض'),
        ('جدة', 'جدة'),
        ('مكة المكرمة', 'مكة المكرمة'),
        ('المدينة المنورة', 'المدينة المنورة'),
        ('الدمام', 'الدمام'),
        ('الخبر', 'الخبر'),
        ('الظهران', 'الظهران'),
        ('الأحساء', 'الأحساء'),
        ('الطائف', 'الطائف'),
        ('جازان', 'جازان'),
        ('بريدة', 'بريدة'),
        ('تبوك', 'تبوك'),
        ('القطيف', 'القطيف'),
        ('خميس مشيط', 'خميس مشيط'),
        ('حفر الباطن', 'حفر الباطن'),
        ('الجبيل', 'الجبيل'),
        ('الخرج', 'الخرج'),
        ('أبها', 'أبها'),
        ('حائل', 'حائل'),
        ('نجران', 'نجران'),
        ('ينبع', 'ينبع'),
        ('صبيا', 'صبيا'),
        ('الباحة', 'الباحة'),
        ('سكاكا', 'سكاكا'),
        ('عرعر', 'عرعر'),
        ('عنيزة', 'عنيزة'),
        ('القريات', 'القريات'),
        ('أخرى', 'أخرى'),
    ]

    # معلومات أساسية
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='players',
        verbose_name="المستخدم"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="اسم اللاعب"
    )
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        verbose_name="المركز"
    )
    birth_year = models.IntegerField(
        validators=[MinValueValidator(2003), MaxValueValidator(2014)],
        verbose_name="سنة الميلاد"
    )
    city = models.CharField(
        max_length=50,
        choices=CITY_CHOICES,
        verbose_name="المدينة"
    )
    nationality = models.CharField(
        max_length=20,
        choices=NATIONALITY_CHOICES,
        verbose_name="الجنسية"
    )
    phone = models.CharField(
        max_length=15,
        verbose_name="رقم الهاتف"
    )
    
    # معلومات إضافية
    previous_clubs = models.TextField(
        blank=True,
        verbose_name="الأندية السابقة",
        help_text="اكتب أسماء الأندية السابقة وعدد السنوات"
    )
    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )
    
    # ملف الفيديو
    video = models.FileField(
        upload_to='player_videos/',
        blank=True,
        null=True,
        verbose_name="مقطع فيديو",
        help_text="مقطع فيديو يعرض مهارات اللاعب (بحد أقصى 120 ثانية)"
    )
    
    # معلومات النظام
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التحديث"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )

    class Meta:
        verbose_name = "لاعب"
        verbose_name_plural = "اللاعبون"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.position}"

    def get_age(self):
        """حساب عمر اللاعب"""
        from datetime import datetime
        current_year = datetime.now().year
        return current_year - self.birth_year

    def get_user_ads_count(self):
        """عدد إعلانات المستخدم"""
        return Player.objects.filter(user=self.user, is_active=True).count()

    def can_user_add_more_ads(self):
        """التحقق من إمكانية إضافة المزيد من الإعلانات (الحد الأقصى 3)"""
        if self.user.is_admin:
            return True
        return self.get_user_ads_count() < 3

