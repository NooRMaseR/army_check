from django.db import models

# Create your models here.
class Rank(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="اسم الرتبه")
    
    class Meta:
        verbose_name = "رتبه"
        verbose_name_plural = "الرتب"
        
    def __str__(self) -> str:
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="اسم الفرع")
    
    class Meta:
        verbose_name = "فرع"
        verbose_name_plural = "الفروع"
        
    def __str__(self) -> str:
        return self.name

class ArmyPerson(models.Model):
    code = models.CharField(max_length=100, unique=True, primary_key=True, db_index=True, verbose_name="الكود")
    name = models.CharField(max_length=255, verbose_name="الاسم")
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, verbose_name="الرتبه")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="الفرع")
    
    class Meta:
        verbose_name = "عسكرى"
        verbose_name_plural = "العساكر"
    
    def __str__(self):
        return f"{self.rank} - {self.branch} - {self.name}"

class RequestStatus(models.TextChoices):
    PENDING = "انتظار"
    ACCEPTED = "موافق"
    REJECTED = "تم الرفض"

class PendingRequest(models.Model):
    user = models.OneToOneField(ArmyPerson, on_delete=models.CASCADE, related_name="request")
    accepted = models.CharField(max_length=10, choices=RequestStatus, default=RequestStatus.PENDING)
    
    def __str__(self) -> str:
        return f"{self.user} - {self.accepted}"

