import os
import json
from datetime import datetime

from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from my_web.models import Customer
from product.models import Product


@receiver(post_save, sender=Product)
def post_save_customer(sender, instance, created, *args, **kwargs):
    if created:
        subject = 'Product Created'
        message = f'{instance.name} was created successfully.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in Customer.objects.all()]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )


post_save.connect(post_save_customer, sender=Product)


# AWS =>  Amazon Web Services
# Nginx => Gunicorn

@receiver(pre_delete, sender=Product)
def save_deleted_customer(sender, instance, *args, **kwargs):
    current_date = datetime.date(datetime.now())
    current_date1 = str(current_date)

    filename = os.path.join(BASE_DIR, 'product/product_data', f'{instance.name}-{current_date1}.json')
    customer_data = {
        'name ': instance.name,
        'category': str(instance.category),
        'description': instance.description,
        'price': instance.price,
        'discount': instance.discount,
        'quantity': instance.quantity,
        'slug': instance.slug
    }
    with open(filename, mode='w') as f:
        json.dump(customer_data, f, indent=4)

    print('Product successfully deleted')
