import jwt
from .models import Account, role
from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.shortcuts import render
from config.settings import SECRET_KEY
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .serializers import AccountSerializer

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from django.contrib.auth.hashers import make_password


from django.db.models import Q


import datetime
import json
# Create your views here.

class RegisterAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def verriy_email(self, email):
        if Account.objects.filter(email=email).exists():
            return True
        return False
    def post(self, request):
        try:
            jd = json.loads(request.body)
            email = jd['email']
            errors = {}
            if self.verriy_email(email):
                return JsonResponse({'message': 'Email already exists'}, status=400)
            else:

                Account.objects.create(
                    first_name=jd['first_name'],
                    last_name=jd['last_name'],
                    cedula=jd['cedula'],
                    email=jd['email'],
                    password=make_password(jd['password']),
                    role=role.objects.get(role=jd['role'])
                )




                return JsonResponse({'message': 'Cuenta creada exitosamente'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


class LoginAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            jd = json.loads(request.body)
            email = jd.get('email')
            password = jd.get('password')
            if not email or not password:
                return JsonResponse({'jwt': 'Campos faltantes'})

            user = get_object_or_404(Account, email=email)
            if not check_password(password, user.password):
                return JsonResponse({'jwt': 'Contraseña incorrecta'})
            payload = {
                'cedula': user.cedula,
                'rol': user.role_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY,algorithm='HS256')
            response = JsonResponse({'jwt': token})
            response.set_cookie(key='jwt', value=token, httponly=True)
            user.last_login = datetime.datetime.now()
            user.save()
            return response

        except json.JSONDecodeError:
            return JsonResponse({'jwt': 'Error en el formato de datos'})
        except ObjectDoesNotExist:
            return JsonResponse({'jwt': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'jwt': 'Error de servidor'})


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
            jd = json.loads(request.body)
            token = jd['jwt']
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
            self.validate_token(jd['jwt'])
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
            jd = json.loads(request.body)
            token = jd['jwt']
            self.validate_token(jd['jwt'])
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
        