from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dòng này bắt buộc phải có để kích hoạt toàn bộ đường dẫn của app onlinecourse
    path('onlinecourse/', include('onlinecourse.urls')),
]