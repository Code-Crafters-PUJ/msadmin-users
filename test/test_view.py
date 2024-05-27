import pytest
from django.urls import reverse
from django.test import Client
import json
# Make sure to import your models
from Account.models import Account, Credentials, Role, Permissions, Module
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def create_test_data():
    jd = {
        'name': 'John',
        'last_name': 'Doe',
        'id_card': '123456789',
        'rol': 1,  # ID del rol en la base de datos
        'email': 'test@example.com',
        'hash': 'hashed_password',
        'permissions': {
            'module1': {'nombre': 'Module 1', 'visualizar': True, 'modificar': False},
            'module2': {'nombre': 'Module 2', 'visualizar': True, 'modificar': True},
        }
    }
    # Crear la cuenta
    role_instance = Role.objects.get(idrole=jd['rol'])
    account = Account.objects.create(
        first_name=jd['name'],
        last_name=jd['last_name'],
        id_card=jd['id_card'],
        role=role_instance
    )

    # Crear las credenciales
    credentials =  Credentials.objects.create(
        email=jd['email'],
        password=make_password(jd['hash']),
        idcuenta=account
    )

    # Determinar los permisos basados en el rol
    permissions_data = jd.get('permissions', {})
    if role_instance.role_description != 'Admin':
        for key, permission_data in permissions_data.items():
            nombre = permission_data.get('nombre', '')
            visualizar = permission_data.get('visualizar', False)
            modificar = permission_data.get('modificar', False)
            module = Module.objects.get(description=nombre)
            Permissions.objects.create(
                idModule=module,
                idAccount=account,
                can_modify=modificar,
                can_view=visualizar
            )
    else:
        for key, permission_data in permissions_data.items():
            nombre = permission_data.get('nombre', '')
            module = Module.objects.get(description=nombre)
            Permissions.objects.create(
                idModule=module,
                idAccount=account,
                can_modify=True,
                can_view=True
            )

    return credentials

# Login tests


@pytest.mark.django_db
def test_valid_login(client, create_test_data):
    credentials_data = {
        'email': 'test@example.com',
        'password': 'hashed_password'
    }
    response = client.post(reverse('user:user_login'), json.dumps(
        credentials_data), content_type='application/json')
    assert response.status_code == 200
    assert 'jwt' in response.json()


@pytest.mark.django_db
def test_missing_fields(client):
    invalid_credentials = {
        'email': 'test@example.com'
    }
    response = client.post(reverse('user:user_login'), json.dumps(
        invalid_credentials), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['jwt'] == 'Campos faltantes'


@pytest.mark.django_db
def test_invalid_password(client, create_test_data):
    invalid_credentials = {
        'email': 'test@example.com',
        'password': 'wrong_password'
    }
    response = client.post(reverse('user:user_login'), json.dumps(
        invalid_credentials), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['jwt'] == 'Contraseña incorrecta'


# Register tests
@pytest.mark.django_db
def test_register_account_view_success():
    # Prepare request data
    data = {
        'name': 'John',
        'last_name': 'Doe',
        'id_card': '123456789',
        'rol': 1,  # ID del rol en la base de datos
        'email': 'test@example.com',
        'hash': 'hashed_password',
        'permissions': {
            'module1': {'nombre': 'Module 1', 'visualizar': True, 'modificar': False},
            'module2': {'nombre': 'Module 2', 'visualizar': True, 'modificar': True},
        }
    }
    client = Client()

    # Send POST request to register endpoint
    response = client.post(reverse('user:user_register'), data=json.dumps(
        data), content_type='application/json')

    # Check response status code
    # Assuming successful creation returns 201 status code
    assert response.status_code == 201

    # Check if message is present in response
    assert 'message' in response.json()

    assert response.json()['message'] == 'Cuenta creada exitosamente'


@pytest.mark.django_db
def test_register_account_view_email_already_exists():
    # Create a user with the same email to simulate email already exists scenario
    

    # Prepare request data
    jd = {
        'name': 'John',
        'last_name': 'Doe',
        'id_card': '123456789',
        'rol': 1,  # ID del rol en la base de datos
        'email': 'test@example.com',
        'hash': 'hashed_password',
        'permissions': {
            'module1': {'nombre': 'Module 1', 'visualizar': True, 'modificar': False},
            'module2': {'nombre': 'Module 2', 'visualizar': True, 'modificar': True},
        }
    }

    role_instance = Role.objects.get(idrole=jd['rol'])
    account = Account.objects.create(
        first_name=jd['name'],
        last_name=jd['last_name'],
        id_card=jd['id_card'],
        role=role_instance
    )

    # Crear las credenciales
    credentials = Credentials.objects.create(
        email=jd['email'],
        password=make_password(jd['hash']),
        idcuenta=account
    )

    # Determinar los permisos basados en el rol
    permissions_data = jd.get('permissions', {})
    if role_instance.role_description != 'Admin':
        for key, permission_data in permissions_data.items():
            nombre = permission_data.get('nombre', '')
            visualizar = permission_data.get('visualizar', False)
            modificar = permission_data.get('modificar', False)
            module = Module.objects.get(description=nombre)
            Permissions.objects.create(
                idModule=module,
                idAccount=account,
                can_modify=modificar,
                can_view=visualizar
            )
    else:
        for key, permission_data in permissions_data.items():
            nombre = permission_data.get('nombre', '')
            module = Module.objects.get(description=nombre)
            Permissions.objects.create(
                idModule=module,
                idAccount=account,
                can_modify=True,
                can_view=True
            )


    client = Client()

    # Send POST request to register endpoint
    response = client.post(reverse('user:user_register'), data=json.dumps(
        data), content_type='application/json')

    # Check response status code
    # Assuming email already exists returns 400 status code
    assert response.status_code == 400

    # Check if message is present in response
    assert 'message' in response.json()

    assert response.json()['message'] == 'El email ya esta registrado'


@pytest.mark.django_db
def test_register_account_view_invalid_data():
    # Prepare request data with missing fields
    data = {
        'first_name': 'Test',
        'last_name': 'User',
        # Missing 'email', 'password', and 'role'
    }
    client = Client()

    # Send POST request to register endpoint
    response = client.post(reverse('user:user_register'), data=json.dumps(
        data), content_type='application/json')

    # Check response status code
    # Assuming invalid data returns 400 status code
    assert response.status_code == 400

    # Check if message is present in response
    assert 'message' in response.json()


# account_info tests

@pytest.mark.django_db
def test_get_account_info_view_success():
    # Crear un usuario para obtener información
    jd = {
        'name': 'John',
        'last_name': 'Doe',
        'id_card': '123456789',
        'rol': 1,  # ID del rol en la base de datos
        'email': 'test@example.com',
        'hash': 'hashed_password',
        'permissions': {
            'module1': {'nombre': 'Module 1', 'visualizar': True, 'modificar': False},
            'module2': {'nombre': 'Module 2', 'visualizar': True, 'modificar': True},
        }
    }
    role_instance = Role.objects.get(idrole=jd['rol'])
    user = Account.objects.create(
        first_name=jd['name'],
        last_name=jd['last_name'],
        id_card=jd['id_card'],
        role=role_instance
    )

    # Crear las credenciales
    credentials = Credentials.objects.create(
        email=jd['email'],
        password=make_password(jd['hash']),
        idcuenta=user
    )

    # Determinar los permisos basados en el rol
    permissions_data = jd.get('permissions', {})
    if role_instance.role_description != 'Admin':
        for key, permission_data in permissions_data.items():
            nombre = permission_data.get('nombre', '')
            visualizar = permission_data.get('visualizar', False)
            modificar = permission_data.get('modificar', False)
            module = Module.objects.get(description=nombre)
            Permissions.objects.create(
                idModule=module,
                idAccount=user,
                can_modify=modificar,
                can_view=visualizar
            )
    else:
        for key, permission_data in permissions_data.items():
            nombre = permission_data.get('nombre', '')
            module = Module.objects.get(description=nombre)
            Permissions.objects.create(
                idModule=module,
                idAccount=user,
                can_modify=True,
                can_view=True
            )

    # Preparar datos de inicio de sesión
    client = Client()
    credentials_data = {
        'email': 'test@example.com',
        'password': 'hashed_password'
    }
    response = client.post(reverse('user:user_login'), json.dumps(
        credentials_data), content_type='application/json')
    # Asumiendo que un inicio de sesión exitoso devuelve un código de estado 200
    assert response.status_code == 200
    print(response.json())

    token = response.json().get('jwt')

    # Verificar que se obtenga el token JWT
    assert token is not None

    # Configurar las cabeceras con el token JWT para la solicitud GET
    headers = {'Authorization': f'Bearer {token}'}

    # Enviar solicitud GET para obtener la información de la cuenta del usuario autenticado
    response = client.get(
        reverse('user:account_info', kwargs={'pk': user.pk}), **headers)

    # Verificar el código de estado de la respuesta
    assert response.status_code == 200

    # Verificar si los datos del usuario están presentes en la respuesta
    assert 'user' in response.json()


@pytest.mark.django_db
def test_update_account_info_view_success():
    # Create a user to update information
    jd = {
        'name': 'John',
        'last_name': 'Doe',
        'id_card': '123456789',
        'rol': 1,  # ID del rol en la base de datos
        'email': 'test@example.com',
        'hash': 'hashed_password',
        'permissions': {
            'module1': {'nombre': 'Module 1', 'visualizar': True, 'modificar': False},
            'module2': {'nombre': 'Module 2', 'visualizar': True, 'modificar': True},
        }
    }
    role_instance = Role.objects.get(idrole=jd['rol'])
    user = Account.objects.create(
        first_name=jd['name'],
        last_name=jd['last_name'],
        id_card=jd['id_card'],
        role=role_instance
    )

    # Crear las credenciales
    credentials = Credentials.objects.create(
        email=jd['email'],
        password=make_password(jd['hash']),
        idcuenta=user
    )

    # Determinar los permisos basados en el rol
    permissions_data = jd.get('permissions', {})
    if role_instance.role_description != 'Admin':
        for key, permission_data in permissions_data.items():
            nombre = permission_data.get('nombre', '')
            visualizar = permission_data.get('visualizar', False)
            modificar = permission_data.get('modificar', False)
            module = Module.objects.get(description=nombre)
            Permissions.objects.create(
                idModule=module,
                idAccount=user,
                can_modify=modificar,
                can_view=visualizar
            )
    else:
        for key, permission_data in permissions_data.items():
            nombre = permission_data.get('nombre', '')
            module = Module.objects.get(description=nombre)
            Permissions.objects.create(
                idModule=module,
                idAccount=user,
                can_modify=True,
                can_view=True
            )
    client = Client()

    # Send PUT request to update user information
    response = client.put(reverse('user:account_info', kwargs={
                          'pk': user.pk}), data=json.dumps(data), content_type='application/json', **headers)

    # Check response status code
    # Assuming successful update returns 200 status code
    assert response.status_code == 200

    # Check if success message is present in response
    assert 'message' in response.json()


@pytest.mark.django_db
def test_delete_account_info_view_success():
    # Create a user to delete
    user = Account.objects.create(
        first_name='First',
        last_name='Last',
        cedula='1234567890',
        role=Role.objects.get(role='ADMIN')
    )

    # Create a Credentials instance associated with the created account
    Credentials.objects.create(
        email='test@example.com',
        password='hashed_password',
        idcuenta=Account.objects.get(cedula='1234567890')
    )

    credentials_data = {
        'email': 'test@example.com',
        'password': 'hashed_password'
    }
    response = client.post(reverse('user:user_login'), json.dumps(
        credentials_data), content_type='application/json')
    # Asumiendo que un inicio de sesión exitoso devuelve un código de estado 200
    assert response.status_code == 200
    print(response.json())

    token = response.json().get('jwt')

    # Prepare request data
    headers = {'Authorization': token}

    client = Client()

    # Send DELETE request to delete user
    response = client.delete(
        reverse('user:account_info', kwargs={'pk': user.pk}), **headers)

    # Check response status code
    # Assuming successful deletion returns 200 status code
    assert response.status_code == 200

    # Check if success message is present in response
    assert 'message' in response.json()
