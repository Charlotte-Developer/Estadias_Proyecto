from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid

# 1. Creamos el nuevo Manager que entiende de matrículas
class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, password=None, **extra_fields):
        if not matricula:
            raise ValueError('El usuario debe tener una matrícula')
        user = self.model(matricula=matricula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'ADMIN')

        return self.create_user(matricula, password, **extra_fields)


# 2. Tu modelo de usuario que ya tenías
class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('DOCENTE', 'Docente/Tutor'),
        ('ALUMNO', 'Alumno'),
    )
    
    username = None 
    matricula = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=150)
    rol = models.CharField(max_length=10, choices=ROLES, default='ALUMNO')

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['nombre_completo', 'rol']

    # 3. ¡IMPORTANTE! Conectamos el modelo con el nuevo Manager
    objects = UsuarioManager()

    def __str__(self):
        return f"{self.matricula} - {self.nombre_completo}"

class Taller(models.Model):
    nombre = models.CharField(max_length=100)
    tutor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'DOCENTE'})
    
    class Meta:
        verbose_name = 'Taller'
        verbose_name_plural = 'Talleres'

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_evento = models.DateField()
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.nombre

class AsistenciaTaller(models.Model):
    NIVELES = (
        ('NINGUNA', 'Ninguna (0%)'),
        ('BAJA', 'Baja (10%)'),
        ('NORMAL', 'Normal (35%)'),
        ('PERFECTA', 'Perfecta (50%)'),
    )
    # Solo los alumnos pueden tener asistencia
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'ALUMNO'})
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    nivel_asistencia = models.CharField(max_length=10, choices=NIVELES, default='NINGUNA')
    periodo = models.CharField(max_length=50) # Ej. Sep-Dic 2026

    class Meta:
        verbose_name = 'Asistencia al Taller'
        verbose_name_plural = 'Asistencias a los Talleres'

    def __str__(self):
        return f"{self.alumno.matricula} - {self.taller.nombre} - {self.nivel_asistencia}"

class EvidenciaEvento(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    )
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'ALUMNO'})
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fotografia = models.ImageField(upload_to='evidencias/')
    estado_validacion = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evidencia de Evento'
        verbose_name_plural = 'Evidencias de Eventos'

    
    def __str__(self):
        return f"{self.alumno.matricula} - {self.evento.nombre}"

class CartaLiberacion(models.Model):
    alumno = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'ALUMNO'})
    codigo_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    porcentaje_final = models.IntegerField()

    class Meta:
        verbose_name = 'Carta de Liberación'
        verbose_name_plural = 'Cartas de Liberación'

    def __str__(self):
        return f"Carta - {self.alumno.matricula}"