from django.contrib import admin
from .models import Usuario, Taller, Evento, AsistenciaTaller, EvidenciaEvento, CartaLiberacion

admin.site.register(Usuario)
admin.site.register(Taller)
admin.site.register(Evento)
admin.site.register(AsistenciaTaller)
admin.site.register(EvidenciaEvento)
admin.site.register(CartaLiberacion)