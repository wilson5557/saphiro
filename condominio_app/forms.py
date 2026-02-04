from datetime import datetime

from crispy_forms.bootstrap import FieldWithButtons
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Field, Div, Row, MultiField
from django.core.validators import RegexValidator

TIPO_CI = [('V', 'V'),
            ('J', 'J'),
            ('E', 'E'),
            ('G', 'G'),
            ('P', 'P')]

TIPO_INGRESO = [('NOTA DE CRÉDITO', 'Nota de Crédito'),
            ('NOTA DE DEBITO', 'Nota de Debito'),
            ('DEPOSITO DE APERTURA', 'Deposito de Apertura')]

TIPO_FONDO = [('RESERVA', 'Fondo de Reserva'),
            ('OPERACIONAL', 'Fondo Operacional'),
            ('OTROS FONDOS', 'Otros Fondos')]

TIPO_FONDO_MOV = [('CRÉDITO', 'Crédito'),
            ('DEBITO', 'Debito')]

TIPO_MONEDA = [('BS', 'Bolivar'), 
               ('USD', 'Dolar Americano'), 
               ('EUR', 'Euros')]

TIPO_BANCO = [('COMÚN', 'Banco Común'),
             ('FONDO', 'Banco de Fondos')]

FORMA_GASTO = [(0, 'Condominio'),
              (1, 'Cuota')]

TIPO_GASTO = [('COMÚN', 'Gasto común'),
              ('NO COMÚN', 'Gasto no común')]

TIPO_UNIDAD = [('APARTAMENTOS', 'Apartamentos'),
              ('CASAS', 'Casas'),
              ('COMERCIAL', 'Comercial')]

GENERO = [('M', 'Masculino'),
          ('F', 'Femenino'),
          ('O', 'Otro')]

TIPO_APTO = [('Apartamento', 'Apartamento'),
             ('Penthouse', 'Penthouse'),
             ('Local Comercial', 'Local Comercial')]

TIPO_POST = [('ALQUILER', 'Alquiler'),
             ('VENTA', 'Venta')]

CAT_POST = [('RESIDENCIAL', 'Alquiler Residencial'),
             ('VACACIONAL', 'Alquiler Vacacional')]

PAISES = [
    ('Estados Unidos', 'Estados Unidos'),
    ('Afganistán', 'Afganistán'),
    ('Albania', 'Albania'),
    ('Algeria', 'Algeria'),
    ('Samoa Americana', 'Samoa Americana'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Anguilla', 'Anguilla'),
    ('Antarctica', 'Antarctica'),
    ('Antigua y Barbuda', 'Antigua y Barbuda'),
    ('Argentina', 'Argentina'),
    ('Armenia', 'Armenia'),
    ('Aruba', 'Aruba'),
    ('Australia', 'Australia'),
    ('Austria', 'Austria'),
    ('Azerbaiyán', 'Azerbaiyán'),
    ('Bahamas', 'Bahamas'),
    ('Bahrein', 'Bahrein'),
    ('Bangladesh', 'Bangladesh'),
    ('Barbados', 'Barbados'),
    ('Bielorrusia', 'Bielorrusia'),
    ('Bélgica', 'Bélgica'),
    ('Belice', 'Belice'),
    ('Benin', 'Benin'),
    ('Bermuda', 'Bermuda'),
    ('Bután', 'Bután'),
    ('Bolivia', 'Bolivia'),
    ('Bosnia y Herzegovina', 'Bosnia y Herzegovina'),
    ('Botswana', 'Botswana'),
    ('Isla Bouvet', 'Isla Bouvet'),
    ('Brazil', 'Brazil'),
    ('Brunei', 'Brunei'),
    ('Bulgaria', 'Bulgaria'),
    ('Burkina Faso', 'Burkina Faso'),
    ('Burundi', 'Burundi'),
    ('Camboya', 'Camboya'),
    ('Camerún', 'Camerún'),
    ('Canadá', 'Canadá'),
    ('Cabo Verde', 'Cabo Verde'),
    ('Islas Caimán', 'Islas Caimán'),
    ('República Centroafricana', 'República Centroafricana'),
    ('Chad', 'Chad'),
    ('Chile', 'Chile'),
    ('China', 'China'),
    ('Isla de Navidad', 'Isla de Navidad'),
    ('Islas Cocos', 'Islas Cocos'),
    ('Colombia', 'Colombia'),
    ('Comoros', 'Comoros'),
    ('Congo', 'Congo'),
    ('Islas Cook', 'Islas Cook'),
    ('Costa Rica', 'Costa Rica'),
    ('Costa de Marfil', 'Costa de Marfil'),
    ('Croacia', 'Croacia'),
    ('Cuba', 'Cuba'),
    ('Cyprus', 'Cyprus'),
    ('República Checa', 'República Checa'),
    ('Dinamarca', 'Dinamarca'),
    ('Djibouti', 'Djibouti'),
    ('Dominica', 'Dominica'),
    ('República Dominicana', 'República Dominicana'),
    ('Timor Oriental', 'Timor Oriental'),
    ('Ecuador', 'Ecuador'),
    ('Egipto', 'Egipto'),
    ('El Salvador', 'El Salvador'),
    ('Guinea Ecuatorial', 'Guinea Ecuatorial'),
    ('Eritrea', 'Eritrea'),
    ('Estonia', 'Estonia'),
    ('Etiopía', 'Etiopía'),
    ('Islas Malvinas', 'Islas Malvinas'),
    ('Islas Feroe', 'Islas Feroe'),
    ('Fiyi', 'Fiyi'),
    ('Finlandia', 'Finlandia'),
    ('Francia', 'Francia'),
    ('Guayana Francesa', 'Guayana Francesa'),
    ('Polinesia Francesa', 'Polinesia Francesa'),
    ('Gabón', 'Gabón'),
    ('Gambia', 'Gambia'),
    ('Georgia', 'Georgia'),
    ('Alemania', 'Alemania'),
    ('Ghana', 'Ghana'),
    ('Gibraltar', 'Gibraltar'),
    ('Grecia', 'Grecia'),
    ('Groenlandia', 'Groenlandia'),
    ('Grenada', 'Grenada'),
    ('Guadalupe', 'Guadalupe'),
    ('Guam', 'Guam'),
    ('Guatemala', 'Guatemala'),
    ('Guinea', 'Guinea'),
    ('Guinea-bissau', 'Guinea-bissau'),
    ('Guyana', 'Guyana'),
    ('Haití', 'Haití'),
    ('Honduras', 'Honduras'),
    ('Hong Kong', 'Hong Kong'),
    ('Hungary', 'Hungary'),
    ('Iceland', 'Iceland'),
    ('India', 'India'),
    ('Indonesia', 'Indonesia'),
    ('Irán', 'Irán'),
    ('Iraq', 'Iraq'),
    ('Irlanda', 'Irlanda'),
    ('Israel', 'Israel'),
    ('Italia', 'Italia'),
    ('Jamaica', 'Jamaica'),
    ('Japón', 'Japón'),
    ('Jordania', 'Jordania'),
    ('Kazajistán', 'Kazajistán'),
    ('Kenia', 'Kenia'),
    ('Kiribati', 'Kiribati'),
    ('Corea del Norte', 'Corea del Norte'),
    ('Corea del Sur', 'Corea del Sur'),
    ('Kuwait', 'Kuwait'),
    ('Kirguistán', 'Kirguistán'),
    ('Laos', 'Laos'),
    ('Letonia', 'Letonia'),
    ('Líbano', 'Líbano'),
    ('Lesoto', 'Lesoto'),
    ('Liberia', 'Liberia'),
    ('Libia', 'Libia'),
    ('Liechtenstein', 'Liechtenstein'),
    ('Lituania', 'Lituania'),
    ('Luxemburgo', 'Luxemburgo'),
    ('Macao', 'Macao'),
    ('Macedonia', 'Macedonia'),
    ('Madagascar', 'Madagascar'),
    ('Malawi', 'Malawi'),
    ('Malasia', 'Malasia'),
    ('Maldivas', 'Maldivas'),
    ('Mali', 'Mali'),
    ('Malta', 'Malta'),
    ('Islas Marshall', 'Islas Marshall'),
    ('Martinica', 'Martinica'),
    ('Mauritania', 'Mauritania'),
    ('Mauricio', 'Mauricio'),
    ('Mayotte', 'Mayotte'),
    ('México', 'México'),
    ('Micronesia', 'Micronesia'),
    ('Moldavia', 'Moldavia'),
    ('Mónaco', 'Mónaco'),
    ('Mongolia', 'Mongolia'),
    ('Montserrat', 'Montserrat'),
    ('Marruecos', 'Marruecos'),
    ('Mozambique', 'Mozambique'),
    ('Myanmar', 'Myanmar'),
    ('Namibia', 'Namibia'),
    ('Nauru', 'Nauru'),
    ('Nepal', 'Nepal'),
    ('Países Bajos', 'Países Bajos'),
    ('Antillas Neerlandesas', 'Antillas Neerlandesas'),
    ('Nueva Caledonia', 'Nueva Caledonia'),
    ('Nueva Zelanda', 'Nueva Zelanda'),
    ('Nicaragua', 'Nicaragua'),
    ('Níger', 'Níger'),
    ('Nigeria', 'Nigeria'),
    ('Niue', 'Niue'),
    ('Isla Norfolk', 'Isla Norfolk'),
    ('Islas Marianas del Norte', 'Islas Marianas del Norte'),
    ('Noruega', 'Noruega'),
    ('Omán', 'Omán'),
    ('Pakistán', 'Pakistán'),
    ('Palau', 'Palau'),
    ('Panamá', 'Panamá'),
    ('Papúa Nueva Guinea', 'Papúa Nueva Guinea'),
    ('Paraguay', 'Paraguay'),
    ('Peru', 'Peru'),
    ('Filipinas', 'Filipinas'),
    ('Pitcairn', 'Pitcairn'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Puerto Rico', 'Puerto Rico'),
    ('Catar', 'Catar'),
    ('Reunion', 'Reunion'),
    ('Romania', 'Romania'),
    ('Rusia', 'Rusia'),
    ('Rwanda', 'Rwanda'),
    ('San Cristóbal y Nieves', 'San Cristóbal y Nieves'),
    ('Santa Lucia', 'Santa Lucia'),
    ('San Vicente y las Granadinas', 'San Vicente y las Granadinas'),
    ('Samoa', 'Samoa'),
    ('San Marino', 'San Marino'),
    ('Santo Tomé y Príncipe', 'Santo Tomé y Príncipe'),
    ('Arabia Saudita', 'Arabia Saudita'),
    ('Senegal', 'Senegal'),
    ('Seychelles', 'Seychelles'),
    ('Sierra Leona', 'Sierra Leona'),
    ('Singapur', 'Singapur'),
    ('Eslovaquia', 'Eslovaquia'),
    ('Eslovenia', 'Eslovenia'),
    ('Islas Salomón', 'Islas Salomón'),
    ('Somalia', 'Somalia'),
    ('Sudáfrica', 'Sudáfrica'),
    ('España', 'España'),
    ('Sri Lanka', 'Sri Lanka'),
    ('Santa  Helena', 'Santa  Helena'),
    ('San Pierre', 'San Pierre'),
    ('Sudán', 'Sudán'),
    ('Surinam', 'Surinam'),
    ('Eswatini', 'Eswatini'),
    ('Suecia', 'Suecia'),
    ('Suiza', 'Suiza'),
    ('Siria', 'Siria'),
    ('Taiwán', 'Taiwán'),
    ('Tajikistán', 'Tajikistán'),
    ('Tanzania', 'Tanzania'),
    ('Tailandia', 'Tailandia'),
    ('Togo', 'Togo'),
    ('Tokelau', 'Tokelau'),
    ('Tonga', 'Tonga'),
    ('Trinidad y Tobago', 'Trinidad y Tobago'),
    ('Túnez', 'Túnez'),
    ('Turquía', 'Turquía'),
    ('Turkmenistán', 'Turkmenistán'),
    ('Tuvalu', 'Tuvalu'),
    ('Uganda', 'Uganda'),
    ('Ucrania', 'Ucrania'),
    ('Emiratos Árabes Unidos', 'Emiratos Árabes Unidos'),
    ('Reino Unido', 'Reino Unido'),
    ('Uruguay', 'Uruguay'),
    ('Uzbekistán', 'Uzbekistán'),
    ('Vanuatu', 'Vanuatu'),
    ('Ciudad del Vaticano', 'Ciudad del Vaticano'),
    ('Venezuela', 'Venezuela'),
    ('Vietnam', 'Vietnam'),
    ('Islas Vírgenes Británicas', 'Islas Vírgenes Británicas'),
    ('Islas Vírgenes Americanas', 'Islas Vírgenes Americanas'),
    ('Sahara Occidental', 'Sahara Occidental'),
    ('Yemen', 'Yemen'),
    ('República Democrática del Congo', 'República Democrática del Congo'),
    ('Zambia', 'Zambia'),
    ('Zimbabwe', 'Zimbabwe')
]

CODIGO_AREA = [('+213', 'Algeria (+213)'),
              ('+376', 'Andorra (+376)'),
              ('+244', 'Angola (+244)'),
              ('+1264', 'Anguilla (+1264)'),
              ('+1268', 'Antigua & Barbuda (+1268)'),
              ('+54', 'Argentina (+54)'),
              ('+374', 'Armenia (+374)'),
              ('+297', 'Aruba (+297)'),
              ('+61', 'Australia (+61)'),
              ('+43', 'Austria (+43)'),
              ('+994', 'Azerbaiyán (+994)'),
              ('+1242', 'Bahamas (+1242)'),
              ('+973', 'Bahrein (+973)'),
              ('+880', 'Bangladesh (+880)'),
              ('+1246', 'Barbados (+1246)'),
              ('+375', 'Bielorrusia (+375)'),
              ('+32', 'Bélgica (+32)'),
              ('+501', 'Belice (+501)'),
              ('+229', 'Benin (+229)'),
              ('+1441', 'Bermuda (+1441)'),
              ('+975', 'Bután (+975)'),
              ('+591', 'Bolivia (+591)'),
              ('+387', 'Bosnia y Herzegovina (+387)'),
              ('+267', 'Botswana (+267)'),
              ('+55', 'Brasil (+55)'),
              ('+673', 'Brunéi (+673)'),
              ('+359', 'Bulgaria (+359)'),
              ('+226', 'Burkina Faso (+226)'),
              ('+257', 'Burundi (+257)'),
              ('+855', 'Camboya (+855)'),
              ('+237', 'Camerún (+237)'),
              ('+1', 'Canadá (+1)'),
              ('+238', 'Cabo Verde (+238)'),
              ('+1345', 'Islas Caimán (+1345)'),
              ('+236', 'República Centroafricana (+236)'),
              ('+56', 'Chile (+56)'),
              ('+86', 'China (+86)'),
              ('+57', 'Colombia (+57)'),
              ('+269', 'Comoras (+269)'),
              ('+242', 'Congo (+242)'),
              ('+682', 'Islas Cook (+682)'),
              ('+506', 'Costa Rica (+506)'),
              ('+385', 'Croacia (+385)'),
              ('+53', 'Cuba (+53)'),
              ('+357', 'Chipre (+357)'),
              ('+42', 'República Checa (+42)'),
              ('+45', 'Dinamarca (+45)'),
              ('+253', 'Djibouti (+253)'),
              ('+1809', 'Dominica (+1809)'),
              ('+1809', 'República Dominicana (+1809)'),
              ('+593', 'Ecuador (+593)'),
              ('+20', 'Egipto (+20)'),
              ('+503', 'El Salvador (+503)'),
              ('+240', 'Guinea Ecuatorial (+240)'),
              ('+291', 'Eritrea (+291)'),
              ('+372', 'Estonia (+372)'),
              ('+251', 'Ethiopia (+251)'),
              ('+500', 'Malvinas (+500)'),
              ('+298', 'Islas Feroe (+298)'),
              ('+679', 'Fiyi (+679)'),
              ('+358', 'Finlandia (+358)'),
              ('+33', 'Francia (+33)'),
              ('+594', 'Guayana Francesa (+594)'),
              ('+689', 'Polinesia Francesa (+689)'),
              ('+241', 'Gabón (+241)'),
              ('+220', 'Gambia (+220)'),
              ('+7880', 'Georgia (+7880)'),
              ('+49', 'Alemania (+49)'),
              ('+233', 'Ghana (+233)'),
              ('+350', 'Gibraltar (+350)'),
              ('+30', 'Grecia (+30)'),
              ('+299', 'Groenlandia (+299)'),
              ('+1473', 'Grenada (+1473)'),
              ('+590', 'Guadeloupe (+590)'),
              ('+671', 'Guam (+671)'),
              ('+502', 'Guatemala (+502)'),
              ('+224', 'Guinea (+224)'),
              ('+245', 'Guinea - Bissau (+245)'),
              ('+592', 'Guyana (+592)'),
              ('+509', 'Haití (+509)'),
              ('+504', 'Honduras (+504)'),
              ('+852', 'Hong Kong (+852)'),
              ('+36', 'Hungría (+36)'),
              ('+354', 'Islandia (+354)'),
              ('+91', 'India (+91)'),
              ('+62', 'Indonesia (+62)'),
              ('+98', 'Irán (+98)'),
              ('+964', 'Iraq (+964)'),
              ('+353', 'Irlanda (+353)'),
              ('+972', 'Israel (+972)'),
              ('+39', 'Italia (+39)'),
              ('+1876', 'Jamaica (+1876)'),
              ('+81', 'Japón (+81)'),
              ('+962', 'Jordania (+962)'),
              ('+7', 'Kazajistán (+7)'),
              ('+254', 'Kenia (+254)'),
              ('+686', 'Kiribati (+686)'),
              ('+850', 'Corea del Norte (+850)'),
              ('+82', 'Corea del Sur (+82)'),
              ('+965', 'Kuwait (+965)'),
              ('+996', 'Kirguistán (+996)'),
              ('+856', 'Laos (+856)'),
              ('+371', 'Letonia (+371)'),
              ('+961', 'Líbano (+961)'),
              ('+266', 'Lesoto (+266)'),
              ('+231', 'Liberia (+231)'),
              ('+218', 'Libia (+218)'),
              ('+417', 'Liechtenstein (+417)'),
              ('+370', 'Lituania (+370)'),
              ('+352', 'Luxemburgo (+352)'),
              ('+853', 'Macao (+853)'),
              ('+389', 'Macedonia (+389)'),
              ('+261', 'Madagascar (+261)'),
              ('+265', 'Malawi (+265)'),
              ('+60', 'Malasia (+60)'),
              ('+960', 'Maldivas (+960)'),
              ('+223', 'Mali (+223)'),
              ('+356', 'Malta (+356)'),
              ('+692', 'Islas Marshall (+692)'),
              ('+596', 'Martinica (+596)'),
              ('+222', 'Mauritania (+222)'),
              ('+269', 'Mayotte (+269)'),
              ('+52', 'México (+52)'),
              ('+691', 'Micronesia (+691)'),
              ('+373', 'Moldavia (+373)'),
              ('+377', 'Mónaco (+377)'),
              ('+976', 'Mongolia (+976)'),
              ('+1664', 'Montserrat (+1664)'),
              ('+212', 'Marruecos (+212)'),
              ('+258', 'Mozambique (+258)'),
              ('+95', 'Myanmar (+95)'),
              ('+264', 'Namibia (+264)'),
              ('+674', 'Nauru (+674)'),
              ('+977', 'Nepal (+977)'),
              ('+31', 'Países (+31)'),
              ('+687', 'Nueva Caledonia (+687)'),
              ('+64', 'Nueva Zelanda (+64)'),
              ('+505', 'Nicaragua (+505)'),
              ('+227', 'Níger (+227)'),
              ('+234', 'Nigeria (+234)'),
              ('+683', 'Niue (+683)'),
              ('+672', 'Norfolk Islands (+672)'),
              ('+670', 'Marianas del Norte (+670)'),
              ('+47', 'Noruega (+47)'),
              ('+968', 'Omán (+968)'),
              ('+680', 'Palau (+680)'),
              ('+507', 'Panamá (+507)'),
              ('+675', 'Papúa Nueva Guinea (+675)'),
              ('+595', 'Paraguay (+595)'),
              ('+51', 'Perú (+51)'),
              ('+63', 'Filipinas (+63)'),
              ('+48', 'Polonia (+48)'),
              ('+351', 'Portugal (+351)'),
              ('+1787', 'Puerto Rico (+1787)'),
              ('+974', 'Catar (+974)'),
              ('+262', 'Reunion (+262)'),
              ('+40', 'Romania (+40)'),
              ('+7', 'Rusia (+7)'),
              ('+250', 'Rwanda (+250)'),
              ('+378', 'San Marino (+378)'),
              ('+239', 'Santo Tome & Principe (+239)'),
              ('+966', 'Arabia Saudita (+966)'),
              ('+221', 'Senegal (+221)'),
              ('+381', 'Serbia (+381)'),
              ('+248', 'Seychelles (+248)'),
              ('+232', 'Sierra Leona (+232)'),
              ('+65', 'Singapur (+65)'),
              ('+421', 'Eslovaquia Republic (+421)'),
              ('+386', 'Eslovenia (+386)'),
              ('+677', 'Islas Salomón (+677)'),
              ('+252', 'Somalia (+252)'),
              ('+27', 'Sudáfrica (+27)'),
              ('+34', 'España (+34)'),
              ('+94', 'Sri Lanka (+94)'),
              ('+290', 'Santa Helena (+290)'),
              ('+1869', 'San Cristóbal (+1869)'),
              ('+1758', 'Santa Lucia (+1758)'),
              ('+249', 'Sudán (+249)'),
              ('+597', 'Surinam (+597)'),
              ('+268', 'Eswatini (+268)'),
              ('+46', 'Suecia (+46)'),
              ('+41', 'Suiza (+41)'),
              ('+963', 'Siria (+963)'),
              ('+886', 'Taiwán (+886)'),
              ('+7', 'Tajikstán (+7)'),
              ('+66', 'Tailandia (+66)'),
              ('+228', 'Togo (+228)'),
              ('+676', 'Tonga (+676)'),
              ('+1868', 'Trinidad y Tobago (+1868)'),
              ('+216', 'Túnez (+216)'),
              ('+90', 'Turquía (+90)'),
              ('+7', '>Turkmenistán (+7)'),
              ('+993', 'Turkmenistán (+993)'),
              ('+1649', 'Turcos & Caicos Islands (+1649)'),
              ('+688', 'Tuvalu (+688)'),
              ('+256', 'Uganda (+256)'),
              ('+44', 'Reino Unido (+44)'),
              ('+380', 'Ucrania (+380)'),
              ('+971', 'Emiratos Árabes Unidos (+971)'),
              ('+598', 'Uruguay (+598)'),
              ('+1', 'USA (+1)'),
              ('+7', 'Uzbekistán (+7)'),
              ('+678', 'Vanuatu (+678)'),
              ('+379', 'Ciudad del Vaticano (+379)'),
              ('+58', 'Venezuela (+58)'),
              ('+84', 'Vietnam (+84)'),
              ('+84', 'Islas Vírgenes Británicas (+1284)'),
              ('+84', 'Islas Vírgenes Americanas (+1340)'),
              ('+681', 'Wallis & Futuna (+681)'),
              ('+969', 'Yemen Norte (+969)'),
              ('+967', 'Yemen Sur (+967)'),
              ('+260', 'Zambia (+260)'),
              ('+263', 'Zimbabwe (+263)')]

# VALIDATORS
# creating a validator function
def validate_mail(value):
    if "@gmail.com" in value:
        return value
    else:
        raise forms.ValidationError("En este campo solamente se aceptan los correos que terminen en @gmail.com")

# -------------------------------------------------------------------------------------------------------------------------------------------------
class BancosForm(forms.ModelForm):
  nro_cuenta        = forms.CharField(label='Número de Cuenta', max_length=35, required=False)
  nombre_banco      = forms.CharField(label='Nombre del Banco', max_length=255)
  nombre_titular    = forms.CharField(label='Nombre del titular de la cuenta', max_length=255, required=True)
  fecha_apertura    = forms.DateField(label="Fecha de apertura del banco", widget = forms.SelectDateWidget(attrs=({'style': 'width: 30%; display: inline-block;'})), required=True)
  tipo_dni_titular  = forms.ChoiceField(choices=TIPO_CI, widget=forms.Select(attrs={'class': 'form-control'}))
  dni_titular       = forms.CharField(label='Identificación', max_length=20, required=True)
  email_titular     = forms.EmailField(label='Correo electrónico del titular', max_length=100)
  cod_tlf           = forms.ChoiceField(label="Código del teléfono del titular", required=False, choices=CODIGO_AREA, widget=forms.Select(attrs={'class': 'form-control'}))
  tlf_titular       = forms.CharField(label='Teléfono del titular', max_length=20)
  tipo_moneda       = forms.CharField(label="Tipo de moneda", widget=forms.RadioSelect(choices=TIPO_MONEDA, attrs={'class': 'from-check-input tipo_moneda', 'id': 'tipo_moneda'}))
  tipo_banco        = forms.CharField(label="Tipo de banco", widget=forms.Select(choices=TIPO_BANCO, attrs={'class': 'from-check-input', 'id': 'tipo_banco'}))
  saldo_actual      = forms.DecimalField(label="Saldo de apertura del banco", max_digits=30, decimal_places=2)
  imagen_referencial = forms.ImageField(label="Imagen referencial", required=False)

  class Meta:
    model = Bancos
    fields = ('tipo_moneda', 'tipo_banco', 'nro_cuenta', 'nombre_banco', 'nombre_titular', 'fecha_apertura', 'tipo_dni_titular', 'dni_titular', 'email_titular', 'tlf_titular', 'saldo_actual', 'imagen_referencial')
    exclude = ('ultimo_debito', 'ultimo_credito', 'debitos_banco', 'creditos_banco')

  def clean_tipo_moneda(self):
    self.tipo_moneda = self.cleaned_data.get('tipo_moneda')
    return self.tipo_moneda

  def clean_nro_cuenta(self):
    nro_cuenta = self.cleaned_data.get('nro_cuenta')
    if self.tipo_moneda == "BS":
        if not nro_cuenta.isdigit():
          raise forms.ValidationError("Por favor ingrese solamente números en este campo")
        else:
          return nro_cuenta
    else:
        return nro_cuenta

  # def clean_tlf_titular(self):
  #   tlf_titular = self.cleaned_data.get('tlf_titular')
  #   if not tlf_titular.isdigit():
  #     raise forms.ValidationError("Por favor ingrese solamente números en este campo")
  #   else:
  #     return tlf_titular

  def save(self, commit=True):
    banco = super(BancosForm, self).save()
    if banco:
      ref = str(timezone.now())
      fecha_apertura = timezone.now().date()
      referencia_apertura = ref.replace('-', '').replace(':', '').replace('.', '').replace('+', '').replace(
          ' ', '').replace(" ", "")

      Movimientos_bancarios.objects.get_or_create(fecha_movimiento=fecha_apertura,
                                                  descripcion_movimiento="Saldo de Apertura",
                                                  referencia_movimiento=referencia_apertura,
                                                  debito_movimiento=0,
                                                  credito_movimiento=0,
                                                  monto_movimiento=self.instance.saldo_actual,
                                                  id_banco=self.instance,
                                                  created_at=datetime.now(), updated_at=datetime.now())

    return banco

# -------------------------------------------------------------------------------------------------------------------------------------------------
class MovimientoForm(forms.ModelForm):
  concepto_movimiento = forms.CharField(label="Concepto del ingreso", max_length=255)
  descripcion_movimiento = forms.CharField(label="Descripción del movimiento bancario", widget=forms.Textarea)
  referencia_movimiento = forms.CharField(label="Referencia del movimiento bancario", max_length=100, required=False)
  monto_movimiento = forms.DecimalField(label="Monto movimiento", max_digits=30, decimal_places=2, required=True)
  banco_emisor = forms.CharField(label="Banco donde se realiza el pago", max_length=255, required=False)

  class Meta:
    model = Movimientos_bancarios
    fields = ('concepto_movimiento', 'descripcion_movimiento', 'referencia_movimiento', 'monto_movimiento')

  def save(self, commit=True):
    mov = super(MovimientoForm, self).save()
    if mov:
        return mov


# -------------------------------------------------------------------------------------------------------------------------------------------------
class DatosMovimientoForm(forms.ModelForm):
  nombre_titular = forms.CharField(label='Nombre del titular de la cuenta', max_length=255, required=True)
  codigo_area = forms.ChoiceField(label="Código del teléfono del titular", required=False, choices=CODIGO_AREA, widget=forms.Select(attrs={'class': 'form-control'}))
  telefono_titular = forms.CharField(label='Teléfono del titular', max_length=20)
  correo_titular = forms.EmailField(label='Correo electrónico del titular', max_length=100, required=False)
  tipo_dni_titular = forms.ChoiceField(choices=TIPO_CI, widget=forms.Select(attrs={'class': 'form-control'}))
  dni_titular = forms.CharField(label='Identificación', max_length=20, required=True)

  class Meta:
    model = Datos_transaccion
    fields = ('nombre_titular', 'codigo_area', 'telefono_titular', 'correo_titular', 'dni_titular')

# -------------------------------------------------------------------------------------------------------------------------------------------------
class GastosForm(forms.ModelForm):
  tipo_gasto        = forms.ChoiceField(label="Tipo de gasto", choices=TIPO_GASTO, widget=forms.Select(attrs={'class': 'form-control'}))
  factura           = forms.CharField(label="Número de Factura", max_length=10, validators=[RegexValidator(regex=r'^\d+$',message='El número de factura debe contener solo números.') ], required=False)
  forma_cobro       = forms.ChoiceField(label="¿Como desea registrar el gasto?", choices=FORMA_GASTO, widget=forms.Select(attrs={'class': 'form-control'}))
  metodo_pago       = forms.ChoiceField(label="Método Pago", choices=[(0, "Efectivo"), (1, "Pago Móvil"), (2, "Transferencia"), (3, "Depósito")])

  class Meta:
    model = Gastos
    fields = ('tipo_gasto', 'factura', 'metodo_pago', 'forma_cobro')

# -------------------------------------------------------------------------------------------------------------------------------------------------
class IngresosForm(forms.ModelForm):
  tipo_ingreso      = forms.ChoiceField(choices=TIPO_INGRESO, widget=forms.Select(attrs={'class': 'form-control'}))
  factura           = forms.CharField(label="Número de Factura", max_length=10, validators=[RegexValidator(regex=r'^\d+$',message='El número de factura debe contener solo números.') ], required=False)
  metodo_pago       = forms.ChoiceField(label="Método Pago", choices=[(0, "Efectivo"), (1, "Pago Móvil"), (2, "Transferencia"), (3, "Depósito")])

  class Meta:
    model = Ingresos
    fields = ('tipo_ingreso', 'factura', 'metodo_pago')

# -------------------------------------------------------------------------------------------------------------------------------------------------
class ReservacionForm(forms.ModelForm):
  
  cedula                = forms.IntegerField(label= "Cedula del cliente")
  telefono              = forms.IntegerField(label= "Telefono del cliente")
  Banco                 = forms.CharField(label="Banco emisor", max_length=20)
  referenncia_bancaria  = forms.IntegerField(label="Referencia bancaria")
  fecha_entrada         = forms.DateField(label="Fecha de entrada")
  fecha_salida         = forms.DateField(label="Fecha de salida")
  
  class Meta: 
    model = Reservacion
    fields = ('cedula', 'telefono', 'Banco', 'referenncia_bancaria', 'fecha_entrada', 'fecha_salida')
# -------------------------------------------------------------------------------------------------------------------------------------------------

class FondosForm(forms.ModelForm):
  tipo_fondo        = forms.ChoiceField(label="Tipo de fondo", choices=TIPO_FONDO, widget=forms.Select(attrs={'class': 'form-control'}))
  factura           = forms.CharField(label="Número de Factura", max_length=10, validators=[RegexValidator(regex=r'^\d+$',message='El número de factura debe contener solo números.') ], required=False)
  metodo_pago       = forms.ChoiceField(label="Método Pago", choices=[(0, "Efectivo"), (1, "Pago Móvil"), (2, "Transferencia"), (3, "Depósito")])

  class Meta:
    model = Fondos
    fields = ('tipo_fondo',)

# -------------------------------------------------------------------------------------------------------------------------------------------------
class PropietariosForm(forms.ModelForm):
  nombre_propietario    = forms.CharField(label="Nombre completo del propietario",  max_length=255,                                                       required=True)
  genero                = forms.ChoiceField(label="Género", choices=Propietario.TipoGenero.choices, widget=forms.Select(attrs={'class': 'form-control'}))
  pais_residencia       = forms.ChoiceField(label="Pais de residencia", choices=PAISES, widget=forms.Select(attrs={'class': 'form-control'}))
  tipo_dni              = forms.ChoiceField(label="Tipo de documento", choices=Propietario.TipoIdentificacion.choices, widget=forms.Select(attrs={'class': 'form-control'}))
  dni                   = forms.CharField(label='Número de identificación',         max_length=20,                                                        required=True)
  codigo_tlf_hab        = forms.ChoiceField(label="Código de área habitación", choices=CODIGO_AREA, widget=forms.Select(attrs={'class': 'form-control'}))
  telefono_hab          = forms.CharField(label="Teléfono de habitación", max_length=24, required=False)
  codigo_tlf_movil      = forms.ChoiceField(label="Código de área móvil", choices=CODIGO_AREA, widget=forms.Select(attrs={'class': 'form-control'}))
  telefono_movil        = forms.CharField(label="Teléfono móvil",                   max_length=24,                                                        required=False)

  class Meta:
    model = Propietario
    fields = ('nombre_propietario', 'genero', 'pais_residencia', 'tipo_dni', 'dni', 'codigo_tlf_hab', 'telefono_hab', 'codigo_tlf_movil', 'telefono_movil')
 
  def clean_dni(self):
    dni = self.cleaned_data.get('dni')
    if not dni.isdigit():
      raise forms.ValidationError("Por favor ingrese solamente números en este campo")
    if self.instance and self.instance.pk:
      if Propietario.objects.filter(dni=dni).exclude(pk=self.instance.pk).exists():
        raise forms.ValidationError("Este número de identificación ya está registrado")
    else:
      if Propietario.objects.filter(dni=dni).exists():
        raise forms.ValidationError("Este número de identificación ya está registrado")
    return dni
    
  def clean_telefono_movil(self):
    telefono_movil = self.cleaned_data.get('telefono_movil')
    if telefono_movil is None or telefono_movil == '':
      return telefono_movil
    telefono_movil = str(telefono_movil).strip()
    if not telefono_movil.isdigit():
      raise forms.ValidationError("Por favor ingrese solamente números en este campo")
    return telefono_movil

  def clean_piso(self):
    piso = self.cleaned_data.get('piso')
    if not piso.isdigit():
      raise forms.ValidationError("Por favor ingrese solamente números en este campo")
    else:
      return piso

  def clean_tipo_dni(self):
    tipo_dni = self.cleaned_data.get('tipo_dni')
    if tipo_dni == '':
      raise forms.ValidationError("Por favor escoja un tipo de documento")
    else:
      return tipo_dni

  def save(self, commit=True):
        prop = super(PropietariosForm, self).save()
        prueba = PropietariosForm

        if prop:
            # user = Usuario()
            # user.username = self.instance.dni
            # print('xd')
            # print('xd')
            # print('xd')
            # print(self.cleaned_data.get('correo'))
            # print('xd')
            # print('xd')
            # print('xd')
            # user.email = self.cleaned_data['correo']
            # user.set_password(self.instance.dni)
            # user.id_condominio_id = self.cleaned_data['condominio']
            # user.save()

            # self.instance.id_usuario = user
            # prop.save()
            return prop

# -------------------------------------------------------------------------------------------------------------------------------------------------
class PublicacionesForm(forms.ModelForm):
    tipo_post = forms.ChoiceField(label="Tipo de publicación:", choices=TIPO_POST, widget=forms.Select(attrs={'class': 'form-control'}))
    categoria_post = forms.ChoiceField(label="Categoría:", choices=CAT_POST, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    titulo = forms.CharField(label="Titulo:", max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese el titulo de la publicación'}))
    descripcion = forms.CharField(max_length=5000, widget=forms.TextInput(attrs={'placeholder': 'Ingrese la descripción de la publicación'}))
    cod_tlf = forms.ChoiceField(label="Codigo de telefono móvil:", choices=CODIGO_AREA, widget=forms.Select(attrs={'class': 'form-control'}))
    contacto = forms.CharField(label="Numero de telefono", widget=forms.TextInput(attrs={'placeholder': 'Ej. 04141111234','class': 'form-control'}), required=True)
    horario_desde = forms.DateTimeField(label="Fecha de donde inicia el contacto:", widget=forms.TimeInput(attrs={'type': 'time'}), required=True)
    horario_hasta = forms.DateTimeField(label="Horario donde finaliza el contacto:", widget=forms.TimeInput(attrs={'type': 'time'}), required=True)
    imagen = forms.ImageField(label="Imagén del inmueble:", widget=forms.FileInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Alquiler
        fields = ('tipo_post', 'categoria_post', 'titulo', 'descripcion', 'cod_tlf','contacto', 'imagen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class= "col-sm-3 col-form-label text-dark"
        self.helper.field_class = "col-sm-8 text-dark"
        self.helper.form_id = "NewPublicacion"
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(*[Field(name, wrapper_class="form-group row mt-4") if name != "contacto" else None for name, field in self.fields.items()],
        HTML("""<div class="form-group row mt-4" id="dom">
                          <label for="domicilio" class="col-sm-3 col-form-label text-dark">Inmuebles del propietario:</label>
                          <div class="col-sm-8">
                              <select name="domicilio" id="domicilio" class="form-control" required>
                                  <option value="" selected disabled>Seleccione un inmueble...</option>
                                  {% for domicilio in domicilios %}
                                  <option value={{domicilio.id_domicilio}}>{{domicilio.nombre_domicilio}}</option>
                                  {% endfor %}
                              </select>
                          </div>
                      </div>
                      <div class="form-group row mt-4 d-none" id="datos_domicilio">
                            <div class="col-sm-11 text-center">
                                <strong>Información del inmueble</strong>
                            </div>
                            <div class="col-sm-11">
                                <table id="tabla_datos" width="100%" style="font-size: 14px;"
                                       class="table table-hover mt-3 table-responsive-xl table-responsive-lg table-responsive-md tabla_datos">
                                    <thead class="table-header-prop">
                                    <tr>
                                        <th style="font-weight: 400;" width="20%">Inmueble</th>
                                        <th style="font-weight: 400;" width="20%">Piso</th>
                                        <th style="font-weight: 400;" width="30%">Tipo</th>
                                        <th style="font-weight: 400;">Estacionamientos</th>
                                        <th style="font-weight: 400;">Alicuota</th>
                                        <th style="font-weight: 400;">Tamaño</th>
                                        <th style="font-weight: 400;" width="50%">Ubicado en la torre</th>
                                        <!-- Agrega las columnas adicionales necesarias -->
                                    </tr>
                                    </thead>
                                    <tbody style="background-color: white;">
                                    </tbody>
                                </table>
                            </div>
                      </div>
                      <div class="justify-content-center d-flex mb-2">
                          <button type="submit" id="btn_publicar" class="btn btn-disabled col-sm-4 mt-3 move-up" data-toggle="popover" data-content="Haz click aquí para publicar" disabled><i class="fa fa-check pr-1"></i> Aceptar</button>
                          <a href="{% url "condominio_app:propietarios_publicaciones" %}" class="btn btn-danger col-sm-2 mt-3 ml-3 move-up"><i class="fa fa-times pr-1"></i> Cancelar</a>
                      </div>""")
        )

# -------------------------------------------------------------------------------------------------------------------------------------------------
class DeudasForm(forms.ModelForm):
    tipo_deuda          = forms.ChoiceField(choices=Deudas.TipoDeuda.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_moneda         = forms.ChoiceField(label="Moneda a cobrar", choices=Deudas.TipoMoneda.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    concepto_deuda      = forms.CharField(label="Concepto", max_length=255, required=True)
    descripcion_deuda   = forms.CharField(label="Descripcion", widget=forms.Textarea, required=True)
    fecha_deuda         = forms.DateField(label="Fecha de la deuda", widget = forms.SelectDateWidget(attrs=({'style': 'width: 30%; display: inline-block;'})), required=True)
    monto_deuda         = forms.DecimalField(label="Monto correspondiente a la deuda", max_digits=30, decimal_places=2, required=True)

    class Meta:
        model = Deudas
        fields = ('concepto_deuda', 'descripcion_deuda', 'monto_deuda', 'fecha_deuda')


class MyDateInput(forms.widgets.DateInput):
      input_type = 'date'

class DeudasUpdateForm(forms.ModelForm):
    tipo_deuda          = forms.ChoiceField(label="Tipo de Deuda",choices=Deudas.TipoDeuda.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    concepto_deuda      = forms.CharField(label="Concepto de la Deuda", max_length=255, required=True)
    descripcion_deuda   = forms.CharField(label="Motivo de la Deuda", widget=forms.Textarea, required=True)
    fecha_deuda         = forms.DateField(label="Fecha de la Deuda", widget = MyDateInput(), required=True)
    monto_deuda         = forms.DecimalField(label="Monto correspondiente a la deuda", max_digits=30, decimal_places=2, required=True)
    
    class Meta:
        model = Deudas
        fields = ('tipo_deuda', 'monto_deuda', 'fecha_deuda', 'concepto_deuda', 'descripcion_deuda')

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.label_class= "col-sm-3 col-form-label text-dark"
            self.helper.field_class = "col-sm-8 text-dark"
            self.helper.form_id = "AgregarDeudas"
            self.helper.layout = Layout(
              *[Field(name, wrapper_class="form-group row mt-4") for name, field in self.fields.items()],
              HTML("""<div class="justify-content-center d-flex mt-4">
                   <button type="submit" class="btn btn-success col-sm-4 mt-3 move-up" data-toggle="popover" data-content="Haz click aquí para completar la edición de la deuda"><i class="fa fa-check pr-1"></i> Aceptar</button>
                   <a href="{% url "condominio_app:admin_deudas" %}" class="btn btn-danger col-sm-2 mt-3 ml-3 move-up"><i class="fa fa-times pr-1"></i> Cancelar</a>
                   </div>"""),
            )

# -------------------------------------------------------------------------------------------------------------------------------------------------
class RegistrationForm(UserCreationForm):
  username = forms.CharField(max_length=60)
  email = forms.CharField(label="Correo electrónico", max_length=100, required=True)

  def __init__(self, *args, **kwargs):
    super(UserCreationForm, self).__init__(*args, **kwargs)
    del self.fields['password2']
  
  def clean_username(self):
    username = self.cleaned_data.get('username')
    if Usuario.objects.filter(username=username).exists():
      raise forms.ValidationError("La cédula del usuario ya existe. Por favor, elija otra.")
    return username

    def save(self, commit=True):
        usuario = super(PropietariosForm, self).save()
        if usuario:
            return usuario
        else:
            raise forms.ValidationError("El usuario no pudo ser registrado.")
    
  class Meta:
    model = Usuario
    fields = ('username', 'email')
    exclude = ('password1', )

class Rol(forms.ModelForm):
    rol = forms.ChoiceField(label="Tipo de rol ", choices=Rol.RolesUsuarios.choices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Rol
        fields = ('rol',)


class AccountAuthenticationForm(forms.ModelForm):
  password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

  class Meta:
    model = Usuario
    fields = ('username', 'password')

  def clean(self):
    if self.is_valid():
      username = self.cleaned_data['username']
      password = self.cleaned_data['password']
      if not authenticate(username=username, password=password):
        raise forms.ValidationError("Usuario y/o contraseña incorrecta. Verifique e intente de nuevo")

# -------------------------------------------------------------------------------------------------------------------------------------------------
class CreateBlogPostForm(forms.ModelForm):
  
  class Meta:
    model = Noticia
    fields = ('titulo', 'descripcion', 'imagen')

class UpdateBlogPostForm(forms.ModelForm):

  class Meta:
    model = Noticia
    fields = ('titulo', 'descripcion', 'imagen')

  def save(self, commit=True):
    noticia = self.instance
    noticia.titulo = self.cleaned_data['titulo']
    noticia.descripcion = self.cleaned_data['descripcion']

    if self.cleaned_data['imagen']:
      noticia.imagen = self.cleaned_data['imagen']

    if commit:
      noticia.save()
    return noticia

class CondominioForm(forms.ModelForm):
  nombre_condominio     = forms.CharField(   label="Nombre del condominio",   max_length=255,                                                       required=True)
  rif_condominio        = forms.CharField(   label="RIF del condominio",      max_length=255,                                                       required=True)
  codigo_tlf_1          = forms.ChoiceField( label="Código de área de teléfono 1", choices=CODIGO_AREA, widget=forms.Select(attrs={'class': 'form-control'}), required=True)
  tlf_1                 = forms.CharField(   label="Teléfono #1",             max_length=24,                                                        required=True)
  codigo_tlf_2          = forms.ChoiceField( label="Código de área de teléfono 2", choices=CODIGO_AREA, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
  tlf_2                 = forms.CharField(   label="Teléfono #2",             max_length=24,                                                        required=False)
  direccion_condominio  = forms.CharField(   label="Dirección",               max_length=255,                                                       required=True)
  email                 = forms.CharField(   label="Correo electrónico",      max_length=100,                                                       required=True)
  saldo_edificio        = forms.DecimalField(label="Saldo del condominio (BS)",    max_digits=30, decimal_places=2, required=True)
  saldo_edificio_usd    = forms.DecimalField(label="Saldo del condominio (USD)", max_digits=30, decimal_places=2, required=True)
  saldo_edificio_eur    = forms.DecimalField(label="Saldo del condominio (EUR)", max_digits=30, decimal_places=2, required=True)

  tipo_condominio       = forms.ChoiceField(label="Tipo de condominio", choices=TIPO_UNIDAD)

  recargo_moratorio     = forms.IntegerField(label="Porcentaje de recargo por mora",          max_value=100,  min_value=1,                          required=False)
  dia_recargo           = forms.IntegerField(label="Día en el que el recargo se aplica",      max_value=31,   min_value=1,                          required=False)
  descuento_pronto_pago = forms.IntegerField(label="Porcentaje de descuento por pronto pago", max_value=100,  min_value=1,                          required=False)
  dia_descuento         = forms.IntegerField(label="Día hasta el que el descuento es válido", max_value=31,   min_value=1,                          required=False)

  class Meta:
    model = Condominio
    fields = ('nombre_condominio', 'rif_condominio', 'codigo_tlf_1', 'tlf_1', 'codigo_tlf_2', 'tlf_2', 'direccion_condominio', 'email', 'saldo_edificio', 'saldo_edificio_usd', 'saldo_edificio_eur', 'tipo_condominio')

  def clean_rif(self):
    rif = self.cleaned_data.get('rif')
    if not rif.isdigit():
      raise forms.ValidationError("Por favor ingrese solamente números en este campo.")
    else:
      return rif

  def clean_tlf_1(self):
    tlf_1 = self.cleaned_data.get('tlf_1')
    if not tlf_1.isdigit():
      raise forms.ValidationError("Por favor ingrese solamente números en este campo.")
    elif tlf_1 == '':
      raise forms.ValidationError("Por favor ingrese un número de teléfono en este campo.")
    else:
      return tlf_1
    
  def clean_tlf_2(self):
    tlf_2 = self.cleaned_data.get('tlf_2')
    if tlf_2 == '':
      return tlf_2 or None

    if not tlf_2.isdigit():
      raise forms.ValidationError("Por favor ingrese solamente números en este campo.")
    else:
      return tlf_2 or None

  def clean_nro_aptos(self):
    nro_aptos = self.cleaned_data.get('total_domicilios')
    if not nro_aptos.isdigit():
      raise forms.ValidationError("Por favor ingrese solamente números en este campo.")
    else:
      return nro_aptos

  def save(self, commit=True):
      condominio = super(CondominioForm, self).save()
      if condominio:
          print(self.instance)

class TorreForm(forms.ModelForm):
    nombre_torre = forms.CharField(label="Nombre de la torre", max_length=255)
    pisos = forms.IntegerField(label="Cantidad de pisos de la torre")

    class Meta:
        model = Torre
        fields = ('nombre_torre', 'pisos')

class DomicilioForm(forms.ModelForm):
    nombre_domicilio = forms.CharField(label="Nombre del inmueble", max_length=255)
    piso_domicilio = forms.IntegerField(label="Piso del inmueble", required=False)
    estacionamientos = forms.IntegerField(label="Número de estacionamientos del inmueble")
    tipo_domicilio = forms.ChoiceField( label="Tipo de inmueble", choices=TIPO_APTO, widget=forms.Select(attrs={'class': 'form-control'}))
    size_domicilio = forms.CharField(label="Tamaño del inmueble (m²)", max_length=30)
    alicuota_domicilio = forms.FloatField(label="Alicuota del inmueble")
    saldo = forms.DecimalField(label="BS", max_digits=30, decimal_places=2, required=True)
    saldo_usd = forms.DecimalField(label="USD", max_digits=30, decimal_places=2, required=True)
    saldo_eur = forms.DecimalField(label="EUR", max_digits=30, decimal_places=2, required=True)

    class Meta:
        model = Domicilio
        fields = ('nombre_domicilio', 'piso_domicilio', 'estacionamientos', 'tipo_domicilio', 'size_domicilio', 'alicuota_domicilio', 'saldo', 'saldo_usd', 'saldo_eur')

    def save(self, commit=True):
        dom = super(DomicilioForm, self).save()
        if dom:
            return self.instance

class Recargos_y_DescuentosForm(forms.ModelForm):
  recargo_moratorio     = forms.IntegerField(label="Porcentaje de recargo por mora",          max_value=100,  min_value=0,                          required=False)
  dia_recargo           = forms.IntegerField(label="Día en el que el recargo se aplica",      max_value=31,   min_value=1,                          required=False)
  descuento_pronto_pago = forms.IntegerField(label="Porcentaje de descuento por pronto pago", max_value=100,  min_value=0,                          required=False)
  dia_descuento         = forms.IntegerField(label="Día hasta el que el descuento es válido", max_value=31,   min_value=1,                          required=False)

  class Meta:
    model   = Recargos_y_Descuentos
    fields  = ('recargo_moratorio', 'dia_recargo', 'descuento_pronto_pago', 'dia_descuento')

class Tasas_de_cambioForm(forms.ModelForm):
  tasa_BCV_USD      = forms.DecimalField(label="Tasa de cambio Bs/USD",   max_digits=30, decimal_places=2, required=False)
  tasa_BCV_EUR      = forms.DecimalField(label="Tasa de cambio Bs/EUR",   max_digits=30, decimal_places=2, required=False)

  class Meta:
    model   = Tasas
    fields  = ('tasa_BCV_USD', 'tasa_BCV_EUR')

class Establecimiento_preciosForm(forms.ModelForm):
  maleteros                 = forms.DecimalField(label="Precio de los maleteros",                   max_digits=30, decimal_places=2, required=False)
  salon_fiesta              = forms.DecimalField(label="Precio del salón de fiesta", max_digits=30, decimal_places=2, required=False)
  otras_areas               = forms.DecimalField(label="Precio de otras áreas sociales",                   max_digits=30, decimal_places=2, required=False)

  class Meta:
    model = Precios
    fields = ('maleteros', 'salon_fiesta', 'otras_areas')
