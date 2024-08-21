from django.urls import path
from users import views

urlpatterns = [
    path('logout/', views.logout_page, name='logout_page'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.RegisterFormView.as_view(), name='register_page'),
    path('sending-mail/', views.SendEmailView.as_view(), name='sending_email'),
    path('success/', views.success, name='success'),
]



# <div class="col-lg-6 mb-4 mb-lg-0">
#                     {% for image in product.images.all %}
#                         <div class="swiper-slide h-100"><img class="rounded-1 fit-cover h-100 w-100"
#                                                              src="{{ image.image.url }}" alt=""/>
#                         </div>
#                     {% endfor %}
#                 </div>