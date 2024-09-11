import os
import json
from datetime import datetime

from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from my_web.models import Customer


@receiver(post_save, sender=Customer)
def post_save_customer(sender, instance, created, *args, **kwargs):
    if created:
        subject = 'Customer Created'
        message = f'{instance.full_name} was created successfully.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in Customer.objects.all()]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )


post_save.connect(post_save_customer, sender=Customer)


# AWS =>  Amazon Web Services
# Nginx => Gunicorn

@receiver(pre_delete, sender=Customer)
def save_deleted_customer(sender, instance, *args, **kwargs):
    current_date = datetime.date(datetime.now())
    current_date1 = str(current_date)
    filename = os.path.join(BASE_DIR, 'my_web/customer_data', f'{instance.slug}-{current_date1}.json')
    customer_data = {
        'id ': instance.id,
        'full_name': instance.full_name,
        'email': instance.email,
        'phone': instance.phone,
        'address': instance.address,
        'image': str(instance.image),
        'slug': instance.slug
    }
    with open(filename, mode='w') as f:
        json.dump(customer_data, f, indent=4)

    print('Customer successfully deleted')
