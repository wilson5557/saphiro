from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Los usuarios deben de agregar un correo')
        if not username:
            raise ValueError('Los usuarios deben tener un nombre')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    email = models.EmailField(verbose_name="Correo electrónico", max_length=60, unique=True)
    username = models.CharField(verbose_name="Nombre de usuario", max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='Fecha de registro', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Último inicio de sesión', auto_now=True)
    is_active = models.BooleanField(verbose_name="Esta activo?", default=True)
    is_superuser = models.BooleanField(verbose_name="Es superusuario?", default=False)
    id_rol = models.ForeignKey('Rol', on_delete=models.DO_NOTHING, null=True)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.DO_NOTHING, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.id_rol

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


# ROLES
class Rol(models.Model):

    class RolesUsuarios(models.TextChoices):
        ADMINISTRADOR = 0, _('Administrador')
        PRESIDENTE = 1, _('Presidente')
        SECRETARIO = 2, _('Secretario/a')
        JUNTA = 3, _('Junta')
        PROPIETARIO = 4, _('Propietario')
        PORTERO = 5, _('Portero')

    id_rol = models.AutoField(primary_key=True)
    rol = models.CharField(verbose_name="Tipo de rol", max_length=20, choices=RolesUsuarios.choices, default=RolesUsuarios.ADMINISTRADOR)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


# CONFIGURACION DEL SISTEMA E IDENTIDAD DEL CONDOMINIO
class Condominio(models.Model):
    id_condominio = models.AutoField(primary_key=True)
    nombre_condominio = models.CharField(verbose_name="Nombre del condominio", max_length=255)
    rif_condominio = models.CharField(verbose_name="RIF del condominio", max_length=255)
    direccion_condominio = models.CharField(verbose_name="Direccion del condominio", max_length=255)
    saldo_edificio = models.DecimalField(verbose_name="Saldo actual en el condominio", max_digits=30, decimal_places=2, default=0)
    saldo_edificio_usd = models.DecimalField(verbose_name="Saldo actual en el condominio (USD)", max_digits=30, decimal_places=2, default=0)
    saldo_edificio_eur = models.DecimalField(verbose_name="Saldo actual en el condominio (EUR)", max_digits=30, decimal_places=2, default=0)
    tipo_condominio = models.CharField(verbose_name="Tipo de unidad condominal", max_length=20, null=True, blank=True)
    codigo_tlf_1 = models.CharField(verbose_name="Codigo de área 1", max_length=15)
    tlf_1 = models.CharField(verbose_name="Telefono 1 del condominio", max_length=255)
    codigo_tlf_2 = models.CharField(verbose_name="Codigo de área 2", max_length=15, null=True, blank=True)
    tlf_2 = models.CharField(verbose_name="Telefono 2 del condominio (opcional)", max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name="Correo electrónico del condominio", max_length=100)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.nombre_condominio

    class Meta:
        db_table = 'condominio'
        verbose_name = 'Condominio'
        verbose_name_plural = 'Condominio'

# ACTAS
class Actas(models.Model):
    id_acta = models.AutoField(primary_key=True)
    fecha = models.CharField(verbose_name="Nombre del condominio", max_length=255)
    imagen_referencial = models.CharField(verbose_name="RIF del condominio", max_length=255)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'actas'
        verbose_name = 'Acta'
        verbose_name_plural = 'Actas'

# BANCOS
class Bancos(models.Model):
    id_banco = models.AutoField(primary_key=True)

    # INFORMACIÓN DE LA CUENTA DE BANCO
    nro_cuenta = models.CharField(verbose_name="Número de cuenta bancaria", max_length=35, null=True)
    nombre_banco = models.CharField(verbose_name="Nombre del Banco", max_length=255)
    nombre_titular = models.CharField(verbose_name="Nombre del titular de la cuenta bancaria", max_length=255,
                                      null=True)
    fecha_apertura = models.DateField(verbose_name="Fecha de apertura del banco", null=True)
    tipo_dni_titular = models.CharField(verbose_name="Tipo de identificación del titular", max_length=32, null=True)
    dni_titular = models.CharField(verbose_name="Número de identificación del titular", max_length=20, null=True)
    email_titular = models.EmailField(verbose_name="Correo electrónico del titular", max_length=100)
    tlf_titular = models.CharField(verbose_name="Número de teléfono del titular", max_length=32)
    tipo_moneda = models.CharField(verbose_name="Tipo de moneda que maneja el banco", max_length=100)
    ultimo_debito = models.DateField(verbose_name="Último debito realizado al banco", null=True)
    ultimo_credito = models.DateField(verbose_name="Último credito realizado al banco", null=True)
    debitos_banco = models.DecimalField(verbose_name="Total de debitos hechos al banco", max_digits=30,
                                        decimal_places=2, default=0)
    creditos_banco = models.DecimalField(verbose_name="Total de creditos hechos al banco", max_digits=30,
                                         decimal_places=2, default=0)
    saldo_anterior = models.DecimalField(verbose_name="Saldo anterior", max_digits=30, decimal_places=2, blank=True,
                                         default=0)
    saldo_actual = models.DecimalField(verbose_name="Saldo actual en el banco", max_digits=30, decimal_places=2)
    saldo_apertura = models.DecimalField(verbose_name="Saldo actual en el banco", max_digits=30, decimal_places=2, null=True)
    tipo_banco = models.CharField(verbose_name="Tipo de banco", max_length=100, null=True)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, null=True)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'bancos'
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'


# MOVIMIENTOS BANCARIOS
class Movimientos_bancarios(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    fecha_movimiento = models.DateField(verbose_name="Fecha del movimiento bancario", auto_now_add=True)
    concepto_movimiento = models.CharField(verbose_name="Concepto del ingreso", max_length=255)
    descripcion_movimiento = models.TextField(verbose_name="Descripción del movimiento bancario")
    referencia_movimiento = models.CharField(verbose_name="Referencia del movimiento bancario", max_length=100, null=True)
    debito_movimiento = models.DecimalField(verbose_name="Debito", max_digits=30, decimal_places=2, null=True)
    credito_movimiento = models.DecimalField(verbose_name="Credito", max_digits=30, decimal_places=2, null=True)
    monto_movimiento = models.DecimalField(verbose_name="Monto movimiento", max_digits=30, decimal_places=2, null=True)
    banco_emisor = models.CharField(verbose_name="Banco donde se realiza el pago", max_length=255, null=True)
    estado_movimiento = models.IntegerField(verbose_name="Estado del pago", null=True)
    tipo_moneda = models.CharField(verbose_name="Moneda del pago", max_length=10, null=True)
    id_banco = models.ForeignKey('Bancos', on_delete=models.CASCADE, null=True)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.referencia_movimiento

    class Meta:
        db_table = 'movimientos'
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

# DATOS DE LA TRANSACCION
class Datos_transaccion(models.Model):
    id_transaccion = models.AutoField(primary_key=True)
    nombre_titular = models.CharField(verbose_name="Nombre del titular", max_length=30)
    codigo_area = models.CharField(verbose_name="Codigo de área", max_length=7, null=True)
    telefono_titular = models.CharField(verbose_name="Teléfono del titular", max_length=20, null=True)
    correo_titular = models.CharField(verbose_name="Correo del titular", max_length=30, null=True)
    tipo_transaccion = models.CharField(verbose_name="tipo de Transacción", max_length=10)
    dni_titular = models.CharField(verbose_name='Identificación', max_length=20, null=True)
    id_movimiento = models.ForeignKey('Movimientos_bancarios', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'datos_transaccion'
        verbose_name = 'Datos_transaccion'
        verbose_name_plural = 'Datos_transacciones'

# RECIBOS
class Recibos(models.Model):
    id_recibo = models.AutoField(primary_key=True)
    descripcion_recibo = models.TextField(verbose_name="Descripción del recibo")
    monto = models.DecimalField(verbose_name="Monto recibo", max_digits=30, decimal_places=2, null=True)
    fecha_creacion = models.DateField(verbose_name="Fecha de realizacion")
    hora_creacion = models.TimeField(verbose_name="Hora de realizacion")
    categoria_recibo = models.CharField(verbose_name="Categoria del recibo", max_length=20)
    id_movimiento = models.ForeignKey('Movimientos_bancarios', on_delete=models.CASCADE, null=True)
    id_deuda = models.ForeignKey('Deudas', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'recibos'
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'


# INGRESOS
def img_ingresos(instance, filename):
    file_path = 'ingresos/{id_condominio}/{titulo}-{filename}'.format(id_condominio=str(instance.id_movimiento.id_banco.id_condominio_id),
                                                                        titulo=str(instance.concepto_movimiento),
                                                                        filename=filename)
    return file_path


class Ingresos(models.Model):

    class MetodoPago(models.TextChoices):
        ADMINISTRADOR = 0, _('Efectivo')
        PRESIDENTE = 1, _('Pago Móvil')
        SECRETARIO = 2, _('Transferencia')
        GERENTE = 3, _('Depósito')

    id_ingreso = models.AutoField(primary_key=True)
    tipo_ingreso = models.CharField(verbose_name="Tipo de ingreso", max_length=255, null=True)
    factura = models.CharField(verbose_name="Número de Factura", max_length=10, null=True)
    metodo_pago = models.IntegerField(verbose_name="Método Pago", choices=MetodoPago.choices, null=True)
    imagen_referencial = models.ImageField(upload_to=img_ingresos, null=True, blank=True)
    id_propietario = models.ForeignKey('Propietario', on_delete=models.DO_NOTHING, null=True)
    id_movimiento = models.ForeignKey('Movimientos_bancarios', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.concepto_ingreso

    class Meta:
        db_table = 'ingresos'
        managed = True
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        
#RESERVACION
class Reservacion(models.Model):
    
    def img_reservacion(instance, filename):
        file_path = 'reservacion/{id_reservacion}/{titulo}-{filename}'.format(id_reservacion=str(instance.referenncia_bancaria),
                                                                 titulo=str(instance.cedula),
                                                                 filename=filename)
        return file_path
    
    id_reservacion = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name="Nombre del cliente", null=True)#nuevo
    apellido = models.CharField(verbose_name="Nombre del cliente", null=True)#nuevo
    cedula = models.CharField(verbose_name="cedula del cliente", null=True)
    telefono = models.CharField(verbose_name="Telefono del cliente",null=True)
    Banco = models.CharField(verbose_name="Banco del cliente", max_length=20, null=True)
    referenncia_bancaria = models.CharField(verbose_name="Referencia bancaria", null=True)
    Fecha_entrada = models.DateField(verbose_name="Fecha de entrada", null=True)
    Fecha_salida = models.DateField(verbose_name="Fecha de salida", null=True)
    id_alquiler = models.ForeignKey('Alquiler', on_delete=models.DO_NOTHING, null=True)
    estado = models.BooleanField(verbose_name="estado de reserva", null=True, default=False)#nuevo
    soporte_pago = models.ImageField(upload_to=img_reservacion, null=True)#nuevo
    
    class Meta:
         db_table = 'Reservacion'  
         verbose_name = 'Reservacion'
         verbose_name_plural = 'Reservacies'
         

# GASTOS

def img_gastos(instance, filename):
    file_path = 'gastos/{id_condominio}/{titulo}-{filename}'.format(id_condominio=str(instance.id_movimiento.id_banco.id_condominio_id),
                                                                 titulo=str(instance.concepto_movimiento),
                                                                 filename=filename)
    return file_path


class Gastos(models.Model):

    class MetodoPago(models.TextChoices):
        ADMINISTRADOR = 0, _('Efectivo')
        PRESIDENTE = 1, _('Pago Móvil')
        SECRETARIO = 2, _('Transferencia')
        GERENTE = 3, _('Depósito')

    id_gasto = models.AutoField(primary_key=True)
    imagen_referencial = models.ImageField(upload_to=img_gastos, null=True, blank=True)
    tipo_gasto = models.CharField(verbose_name="Tipo de gasto", max_length=100)
    factura = models.CharField(verbose_name="Número de Factura", max_length=10, null=True)
    metodo_pago = models.IntegerField(verbose_name="Método Pago", choices=MetodoPago.choices, null=True)
    forma_cobro = models.CharField(verbose_name="Forma de cobro", max_length=12)
    id_categoria = models.ForeignKey('Categoria', on_delete=models.DO_NOTHING)
    id_movimiento = models.ForeignKey('Movimientos_bancarios', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'gastos'
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'


#CATEGORIAS
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(verbose_name="Categoria del gasto", max_length=255)

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

#FONDOS
def img_fondos(instance, filename):
    file_path = 'fondos/{id_condominio}/{titulo}-{filename}'.format(id_condominio=str(instance.id_movimiento.id_banco.id_condominio_id),
                                                                    titulo=str(instance.concepto_movimiento),
                                                                    filename=filename)
    return file_path


class Fondos(models.Model):

    class MetodoPago(models.TextChoices):
        ADMINISTRADOR = 0, _('Efectivo')
        PRESIDENTE = 1, _('Pago Móvil')
        SECRETARIO = 2, _('Transferencia')
        GERENTE = 3, _('Depósito')

    id_fondo = models.AutoField(primary_key=True)
    tipo_fondo = models.CharField(verbose_name="Tipo de fondo", max_length=255)
    factura = models.CharField(verbose_name="Número de Factura", max_length=10, null=True)
    metodo_pago = models.IntegerField(verbose_name="Método Pago", choices=MetodoPago.choices, null=True)
    imagen_referencial = models.ImageField(upload_to=img_fondos, null=True, blank=True)
    id_movimiento = models.ForeignKey('Movimientos_bancarios', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'fondos'
        managed = True
        verbose_name = 'Fondo'
        verbose_name_plural = 'Fondos'


#CIERRE DE MES
def upload_cierres(instance, filename):
    file_path = 'cierres/{filename}'.format(filename=filename)
    return file_path


class Cierre_mes(models.Model):
    id_cierre = models.AutoField(primary_key=True)
    fecha_cierre = models.DateTimeField(auto_now_add=True, null=True)
    pdf_cierre = models.FileField(upload_to=upload_cierres, null=True)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cierre_mes'
        managed = True
        verbose_name = 'Cierre_mes'
        verbose_name_plural = 'Cierres_mes'


# CUOTA MENSUAL
class Cuota_mensual(models.Model):
    id_cuota_m = models.AutoField(primary_key=True)
    fecha_publicacion = models.DateField(verbose_name="Fecha de la publicacion de la cuota mensual de condominio")
    mes = models.TextField(verbose_name="Mes de pago")
    monto_cuota = models.DecimalField(max_digits=30, decimal_places=2)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cuota_mensual'
        managed = True
        verbose_name = 'Cuota_mensual'
        verbose_name_plural = 'Cuotas_mensuales'


#DOMICILIOS
class Domicilio(models.Model):
    id_domicilio = models.AutoField(primary_key=True)
    nombre_domicilio = models.CharField(verbose_name="Nombre del domicilio", max_length=255, null=True, blank=True)
    piso_domicilio = models.IntegerField(verbose_name="Piso del domicilio", null=True, blank=True)
    estacionamientos = models.IntegerField(verbose_name="Número de estacionamientos por domicilio", null=True, blank=True)
    tipo_domicilio = models.CharField(verbose_name="Tipo de habitación", max_length=15, null=True, blank=True)
    size_domicilio = models.CharField(verbose_name="Tamaño de apartamento (m²)", max_length=30, null=True)
    alicuota_domicilio = models.FloatField(verbose_name="Alicuota del apartamento", null=True)
    saldo = models.DecimalField(verbose_name="Saldo del propietario", max_digits=30, decimal_places=2, null=True)
    saldo_usd = models.DecimalField(verbose_name="Saldo del propietario", max_digits=30, decimal_places=2, null=True)
    saldo_eur = models.DecimalField(verbose_name="Saldo del propietario", max_digits=30, decimal_places=2, null=True)
    estado_deuda = models.BooleanField(verbose_name="Estado de cuenta en cuanto a deudas", default=False)
    id_propietario = models.ForeignKey('Propietario', on_delete=models.DO_NOTHING, related_name='prop_dom', null=True)
    id_torre = models.ForeignKey('Torre', on_delete=models.CASCADE, null=True)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, null=True)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'domicilio'
        verbose_name = 'Domicilio'
        verbose_name_plural = 'Domicilios'


# PROPIETARIOS
class Propietario(models.Model):
    
    class TipoGenero(models.TextChoices):
        MASCULINO = 'M', _('Masculino')
        FEMENINO = 'F', _('Femenino')
        OTRO = 'O', _('Otro')
    
    class TipoIdentificacion(models.TextChoices):
        VENEZOLANO = 'V', _('Venezolano')
        EXTRANJERO = 'E', _('Extranjero')
        PASAPORTE = 'P', _('Pasaporte')
        JURIDICO = 'J', _('Jurídico')
        GUBERNAMENTAL = 'G', _('Gubernamental')
        RIF = 'R', _('RIF')
        OTRO = 'O', _('Otro')
    
    id_propietario = models.AutoField(primary_key=True)

    # DATOS DEL PROPIETARIO
    nombre_propietario = models.CharField(verbose_name="Nombre completo del propietario", max_length=255)
    genero = models.CharField(verbose_name="Género del propietario", max_length=2, choices=TipoGenero.choices)
    pais_residencia = models.CharField(verbose_name="Pais donde reside", max_length=100, null=True)
    tipo_dni = models.CharField(verbose_name="Tipo de identificación", max_length=2, choices=TipoIdentificacion.choices, default=TipoIdentificacion.VENEZOLANO)
    dni = models.CharField(verbose_name="Número de identificación", max_length=50)
    codigo_tlf_hab = models.CharField(verbose_name="Codigo de Área", max_length=15, null=True)
    telefono_hab = models.CharField(verbose_name="Número de teléfono de habitación", max_length=30, null=True)
    codigo_tlf_movil = models.CharField(verbose_name="Codigo de Área", max_length=15, null=True)
    telefono_movil = models.CharField(verbose_name="Número de teléfono personal", max_length=30, null=True)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.nombre_propietario

    class Meta:
        db_table = 'propietario'
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'


# DEUDAS
class Deudas(models.Model):

    class TipoMoneda(models.TextChoices):
        BS = 'BS', _('Bolívares')
        USD = 'USD', _('Dólares')
        EUR = 'EUR', _('Euros')

    class TipoDeuda(models.TextChoices):
        CONDOMINIO = '1', _('Condominio')
        PROPIETARIO = '2', _('Propietario')
    

    id_deuda = models.AutoField(primary_key=True)
    concepto_deuda = models.CharField(verbose_name="Nombre del condominio", max_length=255, null=True, blank=True)
    descripcion_deuda = models.TextField(max_length=5000, null=False, blank=False)
    monto_deuda = models.DecimalField(verbose_name="Monto de la deuda", max_digits=30, decimal_places=2, null=True, blank=True)
    fecha_deuda = models.CharField(verbose_name="Tipo de habitación", max_length=15, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Esta activa?", default=False)
    tipo_moneda = models.CharField(verbose_name="Tipo de moneda", max_length=3, choices=TipoMoneda.choices, default=TipoMoneda.BS)
    tipo_deuda = models.CharField(verbose_name="Entidad o domicilio deudor", choices=TipoDeuda.choices, default=TipoDeuda.CONDOMINIO)
    categoria_deuda = models.CharField(verbose_name="Categoria de la deuda ingresada", max_length=15, null=True)
    is_moroso = models.BooleanField(verbose_name="Esta moroso?", default=False)
    id_domicilio = models.ForeignKey('Domicilio', on_delete=models.CASCADE, null=True)


    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.concepto_deuda 

    class Meta:
        db_table = 'deudas'
        verbose_name = 'Deuda'
        verbose_name_plural = 'Deudas'


#ESTABLECIMIENTOS DE PRECIOS
class Precios(models.Model):
    maleteros = models.DecimalField(verbose_name="Precio de los maleteros", max_digits=30, decimal_places=2, null=True, blank=True)
    salon_fiesta = models.DecimalField(verbose_name="Precio del salón de fiesta", max_digits=30, decimal_places=2, null=True, blank=True)
    otras_areas = models.DecimalField(verbose_name="Precio de otras áreas sociales", max_digits=30, decimal_places=2, null=True, blank=True)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, null=True)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "establecimiento_precios"
        verbose_name = "Establecimiento de precio"
        verbose_name_plural = "Establecimiento de precios"

#NOTICIAS
def upload_location(instance, filename):
    file_path = 'publicaciones/{autor_id}/{titulo}-{filename}'.format(autor_id=str(instance.autor.id),
                                                                      titulo=str(instance.titulo), filename=filename)
    return file_path


class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50, null=False, blank=False)
    descripcion = models.TextField(max_length=5000, null=False, blank=False)
    imagen = models.ImageField(upload_to=upload_location, null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación")
    fecha_actualizado = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizado")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = "noticia"
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"


#ALQUILER
def upload_location_prop(instance, filename):
    file_path = 'publicaciones/{id_domicilio}/{titulo}-{filename}'.format(
        id_domicilio=str(instance.id_domicilio_id),
        titulo=str(instance.titulo), filename=filename)
    return file_path


class Alquiler(models.Model):

    class TipoPost(models.TextChoices):
        ALQUILER = 0, _('Alquiler')
        VENTA = 1, _('Venta')


    class CategoriaPost(models.TextChoices):
        RESIDENCIAL = 0, _('Residencial')
        VACACIONAL = 1, _('Vacacional')
        
    

    id_alquiler = models.AutoField(primary_key=True)
    tipo_post = models.TextField(max_length=25, choices=TipoPost.choices, default=TipoPost.ALQUILER, null=True, blank=False)
    categoria_post = models.TextField(max_length=25, choices=CategoriaPost.choices, default=CategoriaPost.RESIDENCIAL, null=True, blank=False)
    estado = models.BooleanField(verbose_name="Disponibilidad el inmueble", null=True, default=False)
    titulo = models.CharField(max_length=50, null=False, blank=False)
    descripcion = models.TextField(max_length=5000, null=True, blank=False)
    imagen = models.ImageField(upload_to=upload_location_prop, null=True, blank=True)
    cod_tlf = models.CharField(verbose_name="Código de área habitación", max_length=50)
    contacto = models.CharField(verbose_name="Número teléfonico", max_length=20, null=True)
    horario_desde = models.TimeField(verbose_name="Horario para empezar a contactar")
    horario_hasta = models.TimeField(verbose_name="Horario donde finaliza el contacto")
    is_active = models.BooleanField(verbose_name="Esta activa?", default=False)
    id_domicilio = models.ForeignKey('Domicilio', on_delete=models.CASCADE, null=True)
    id_noticia = models.ForeignKey('Noticia', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "alquiler"
        verbose_name = "Alquiler"
        verbose_name_plural = "Alquileres"
    def get_id_alquiler(self):
        return self.id_alquiler  # Método para obtener el ID como entero


#RECARGOS
class Recargos_y_Descuentos(models.Model):
    recargo_moratorio = models.FloatField(verbose_name="Porcentaje de recargo por mora en pago", null=True, blank=True)
    dia_recargo = models.IntegerField(verbose_name="Día en el que se aplica el recargo moratorio", null=True, blank=True)
    descuento_pronto_pago = models.FloatField(verbose_name="Porcentaje de descuento por pronto pago", null=True, blank=True)
    dia_descuento = models.IntegerField(verbose_name="Hasta que día se aplica el descuento por pronto pago", null=True, blank=True)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, null=True)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "recargos_y_descuentos"
        verbose_name = "Recargo y Descuento"
        verbose_name_plural = "Recargos y Descuentos"


# TASAS
class Tasas(models.Model):
    id = models.AutoField(primary_key=True)
    tasa_BCV_USD = models.DecimalField(verbose_name="Tasa del día del USD por BCV", max_digits=30, decimal_places=2, null=True, blank=True)
    tasa_BCV_EUR = models.DecimalField(verbose_name="Tasa del día del EURO por BCV", max_digits=30, decimal_places=2, null=True, blank=True)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "tasas_de_cambio"
        verbose_name = "Tasa de cambio"
        verbose_name_plural = "Tasas de cambio"

#TORRES
class Torre(models.Model):
    id_torre = models.AutoField(primary_key=True)
    nombre_torre = models.CharField(verbose_name="Nombre de la torre", max_length=255, blank=True, null=True)
    pisos = models.IntegerField(verbose_name="Cantidad de pisos de la torre", blank=True, null=True)
    id_condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'torre'
        verbose_name = 'Torre'
        verbose_name_plural = 'Torres'


@receiver(post_delete, sender=Noticia)
def submission_delete(sender, instance, **kwargs):
    instance.imagen.delete(False)


def pre_save_publicacion_receiver(sender, instance, *args, **kwargs):
    fecha_publicacion = timezone.now()
    print(fecha_publicacion.strftime("%d-%m-%Y"))
    if not instance.slug:
        instance.slug = slugify(fecha_publicacion.strftime("%d-%m-%Y") + "-" + instance.titulo)


pre_save.connect(pre_save_publicacion_receiver, sender=Noticia)


# VALIDACIONES
def validate_geeks_mail(value):
    if "@gmail.com" or "@hotmail.com" in value:
        return value
    else:
        raise ValidationError("This field accepts mail id of google only")
