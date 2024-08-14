from django.db import models
from django.utils.text import slugify


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    full_name: str = models.CharField(max_length=100)
    slug: str = models.SlugField(null=True, blank=True)
    email: str = models.EmailField()
    phone: str = models.CharField(max_length=100)
    address: str = models.CharField(max_length=100)
    image: str = models.ImageField(upload_to='customer_image', null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.full_name)
        super(Customer, self).save(*args, **kwargs)

    @property
    def joined(self):
        return self.created_at.strftime("%d/%m/%Y")

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    class Meta:
        db_table = 'customer'
        verbose_name_plural = 'Customers'
