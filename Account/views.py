import jwt
from .models import Account, role, Credentials, Report, Module, Permissions
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from config.settings import SECRET_KEY
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .serializers import AccountSerializer, CredentialsSerializer, ReportSerializer
from django.contrib.auth.hashers import make_password


import datetime
import json
# Create your views here.


class RegisterAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verriy_email(self, email):
        if Credentials.objects.filter(email=email).exists():
            return True
        return False

    def post(self, request):
        try:
            jd = json.loads(request.body)
            email = jd['email']
            errors = {}
            if self.verriy_email(email):
                return JsonResponse({'message': 'El email ya esta registrado'}, status=400)
            else:
                role_name = role.objects.get(idrole=jd['rol'])
                Account.objects.create(
                    first_name=jd['name'],
                    last_name=jd['last_name'],
                    id_card=jd['id_card'],
                    role=role.objects.get(idrole=jd['rol'])
                )
                Credentials.objects.create(
                    email=jd['email'],
                    password=make_password(jd['hash']),
                    idcuenta=Account.objects.get(id_card=jd['id_card'])
                )
                if role_name.role_descripction != 'ADMIN':
                    permissions_data = jd.get('permissions', {})
                    permissions_list = []
                    for key, permission_data in permissions_data.items():
                        nombre = permission_data.get('nombre', '')
                        visualizar = permission_data.get('visualizar', False)
                        modificar = permission_data.get('modificar', False)
                        Permissions.objects.create(
                            idModule=Module.objects.get(description=nombre),
                            idAccount=Account.objects.get(
                                id_card=jd['id_card']),
                            can_modify=modificar,
                            can_view=visualizar
                        )

                else:
                    permissions_data = jd.get('permissions', {})
                    permissions_list = []
                    for key, permission_data in permissions_data.items():
                        nombre = permission_data.get('nombre', '')
                        visualizar = True
                        modificar = True
                        Permissions.objects.create(
                            idModule=Module.objects.get(description=nombre),
                            idAccount=Account.objects.get(
                                id_card=jd['id_card']),
                            can_modify=modificar,
                            can_view=visualizar
                        )
                return JsonResponse({'message': 'Cuenta creada exitosamente'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


class LoginAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        print(request)
        try:
            jd = json.loads(request.body)
            email = jd.get('email')
            password = jd.get('password')
            if not email or not password:
                return JsonResponse({'jwt': 'Campos faltantes'})
            user = get_object_or_404(Credentials, email=email)
            if not check_password(password, user.password):
                return JsonResponse({'jwt': 'ups! credenciales incorrectas'})
            account = Account.objects.get(idcuenta=user.idcuenta_id)

            payload = {
                'id': account.idcuenta,
                'role': account.role.role_descripction,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            response = JsonResponse(
                {'jwt': token, 'role': account.role.role_descripction})
            response.set_cookie(key='jwt', value=token, httponly=True)
            account.last_login = datetime.datetime.now()
            account.connected = True
            account.save()

            return response

        except json.JSONDecodeError as e:
            print("Error al decodificar JSON:", e)
            print("Cuerpo de la solicitud:", request.body)
            # Manejar el error adecuadamente, por ejemplo, devolver una respuesta de error
            return JsonResponse({'jwt': 'Error en el formato de datos'})
        except ObjectDoesNotExist:
            print("Usuario no encontrado")
            # Manejar el error adecuadamente, por ejemplo, devolver una respuesta de error
            return JsonResponse({'jwt': 'Usuario no encontrado'})
        except Exception as e:
            print("Error durante el procesamiento de la solicitud:", e)
            # Devolver una respuesta de error adecuada
            return JsonResponse({'jwt': str(e)})


class logoutAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            token = request.headers['Authorization']
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            account = Account.objects.get(idcuenta=payload['id'])
            account.connected = False
            account.save()
            return JsonResponse({'message': 'Usuario desconectado exitosamente'}, status=200)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token expirado'}, status=400)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Token invalido'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


class getAccountInfoview(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Token expirado'
        except jwt.InvalidTokenError:
            return 'Token invalido'

    def validate_role(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload['role']
        except jwt.ExpiredSignatureError:
            return 'Token expirado'
        except jwt.InvalidTokenError:
            return 'Token invalido'

    def get(self, request, pk):
        try:

            token = request.headers['Authorization']
            if self.validate_token(token) == 'Token expirado':
                return JsonResponse({'message': 'Token expirado'}, status=400)
            elif self.validate_token(token) == 'Token invalido':
                return JsonResponse({'message': 'Token invalido'}, status=400)
            elif self.validate_role(token) != 'ADMIN':
                return JsonResponse({'message': 'No tienes permisos para realizar esta accion'}, status=400)
            else:
                user = get_object_or_404(Account, pk=pk)
                return JsonResponse({'user': AccountSerializer(user).data})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

    def put(self, request, pk):
        try:
            jd = json.loads(request.body)
            token = jd['jwt']
            if self.validate_token(token) == 'Token expirado':
                return JsonResponse({'message': 'Token expirado'}, status=400)
            elif self.validate_token(token) == 'Token invalido':
                return JsonResponse({'message': 'Token invalido'}, status=400)
            elif self.validate_role(token) != 'ADMIN':
                return JsonResponse({'message': 'No tienes permisos para realizar esta accion'}, status=400)
            else:

                account = get_object_or_404(Account, pk=pk)
                account.first_name = jd.get('name', account.first_name)
                account.last_name = jd.get('last_name', account.last_name)
                account.save()
                # Actualiza el rol si se proporciona
                rol_id = jd.get('rol', None)
                if rol_id:
                    account.role = get_object_or_404(role, idrole=rol_id)
                    account.save()
                # Actualiza el email si se proporciona
                email = jd.get('email', None)
                if email:
                    credentials = get_object_or_404(
                        Credentials, idcuenta=account)
                    credentials.email = email
                    credentials.save()
                # Actualiza la contraseña si se proporciona
                hash_password = jd.get('hash', None)
                if hash_password:
                    credentials = Credentials.objects.get(idcuenta=account)
                    credentials.password = make_password(hash_password)
                    credentials.save()
                # Actualiza los permisos si se proporcionan
                permissions_data = jd.get('permissions', {})
                permissions_list = []
                for key, permission_data in permissions_data.items():
                    nombre = permission_data.get('nombre', '')
                    visualizar = permission_data.get('visualizar', False)
                    modificar = permission_data.get('modificar', False)
                    permiso = Permissions.objects.get(
                        idModule=Module.objects.get(description=nombre),
                        idAccount=account
                    )
                    permiso.can_modify = modificar
                    permiso.can_view = visualizar
                    permiso.save()
                    permissions_list.append(permiso)

                return JsonResponse({'message': 'Usuario actualizado exitosamente'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

    def delete(self, request, pk):
        try:
            token = request.headers['Authorization']
            if self.validate_token(token) == 'Token expirado':
                return JsonResponse({'message': 'Token expirado'}, status=400)
            elif self.validate_token(token) == 'Token invalido':
                return JsonResponse({'message': 'Token invalido'}, status=400)
            elif self.validate_role(token) != 'ADMIN':
                return JsonResponse({'message': 'No tienes permisos para realizar esta accion'}, status=400)
            else:
                user = get_object_or_404(Account, pk=pk)
                user.delete()
                return JsonResponse({'message': 'Usuario eliminado exitosamente'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


class getAllAccountInfoview(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Token expirado'
        except jwt.InvalidTokenError:
            return 'Token invalido'

    def validate_role(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload['role']
        except jwt.ExpiredSignatureError:
            return 'Token expirado'
        except jwt.InvalidTokenError:
            return 'Token invalido'

    def get(self, request):
        try:

            token = request.headers['Authorization']
            if self.validate_token(token) == 'Token expirado':
                return JsonResponse({'message': 'Token expirado'}, status=400)
            elif self.validate_token(token) == 'Token invalido':
                return JsonResponse({'message': 'Token invalido'}, status=400)
            elif self.validate_role(token) != 'ADMIN':
                return JsonResponse({'message': 'No tienes permisos para realizar esta accion'}, status=400)
            else:
                account_data = AccountSerializer(
                    Account.objects.all(), many=True).data

                report_data = ReportSerializer(
                    Report.objects.all(), many=True).data
                credentials_data = CredentialsSerializer(
                    Credentials.objects.all(), many=True).data
                return JsonResponse({'account': account_data, 'report': report_data, 'credentials': credentials_data})

        except ObjectDoesNotExist:
            return JsonResponse({'message': 'No hay usuarios'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
