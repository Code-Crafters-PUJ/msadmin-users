import jwt
from .models import Account, role, Credentials
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from config.settings import SECRET_KEY
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .serializers import AccountSerializer
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

                Account.objects.create(
                    first_name=jd['first_name'],
                    last_name=jd['last_name'],
                    cedula=jd['cedula'],
                    role=role.objects.get(role=jd['role'])
                )
                Credentials.objects.create(
                    email=jd['email'],
                    password=make_password(jd['password']),
                    idcuenta=Account.objects.get(cedula=jd['cedula'])
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
            print(jd)
            print()
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
                'role': account.role.role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            response = JsonResponse({'jwt': token, 'role': account.role.role})
            response.set_cookie(key='jwt', value=token, httponly=True)
            account.last_login = datetime.datetime.now()
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

    def get(self, request, pk):
        try:

            token = request.headers['Authorization']
            if self.validate_token(token) == 'Token expirado':
                return JsonResponse({'message': 'Token expirado'}, status=400)
            elif self.validate_token(token) == 'Token invalido':
                return JsonResponse({'message': 'Token invalido'}, status=400)
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
            else:
                user = get_object_or_404(Account, pk=pk)
                serializer = AccountSerializer(user, data=jd)
                if not serializer.is_valid(raise_exception=True):
                    return JsonResponse({'message': serializer.errors}, status=400)
                serializer.save()
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
            else:
                user = get_object_or_404(Account, pk=pk)
                user.delete()
                return JsonResponse({'message': 'Usuario eliminado exitosamente'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
