import pytest
from django.urls import reverse
from django.test import Client
import json
# Make sure to import your models
from Account.models import Account, Credentials, role
from django.contrib.auth.models import User


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def create_test_data():
    # Create an Account instance
    account = Account.objects.create(
        first_name='First',
        last_name='Last',
        cedula='1234567890',
        role=role.objects.get(role='ADMIN')
    )

    # Create a Credentials instance associated with the created account
    credentials = Credentials.objects.create(
        email='test@example.com',
        password='hashed_password',
        idcuenta=Account.objects.get(cedula='1234567890')
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
        'first_name': 'Test',
        'last_name': 'User',
        'cedula': '1234567890',
        'email': 'test@example.com',
        'password': 'test_password',
        'role': 'ADMIN'
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
    Account.objects.create(
        first_name='First',
        last_name='Last',
        cedula='1234567890',
        role=role.objects.get(role='ADMIN')
    )

    # Create a Credentials instance associated with the created account
    Credentials.objects.create(
        email='test@example.com',
        password='hashed_password',
        idcuenta=Account.objects.get(cedula='1234567890')
    )

    # Prepare request data
    data = {
        'first_name': 'Test',
        'last_name': 'User',
        'cedula': '1234567890',
        'email': 'test@example.com',
        'password': 'test_password',
        'role': 'admin'  # Assuming 'admin' is a valid role
    }
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
    user = Account.objects.create(
        first_name='First',
        last_name='Last',
        cedula='1234567890',
        # Asegúrate de que este rol exista en tu base de datos
        role=role.objects.get(role='ADMIN')
    )

    # Crear una instancia de Credentials asociada a la cuenta creada
    Credentials.objects.create(
        email='testing@example.com',
        password='hashed_password',
        idcuenta=Account.objects.get(cedula='1234567890')
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
    user = Account.objects.create(
        first_name='First',
        last_name='Last',
        cedula='1234567890',
        role=role.objects.get(role='ADMIN')
    )

    # Create a Credentials instance associated with the created account
    Credentials.objects.create(
        email='test@example.com',
        password='hashed_password',
        idcuenta=Account.objects.get(cedula='1234567890')
    )

    # Prepare request data
    token = 'valid_jwt_token'
    headers = {'Authorization': token}
    data = {
        'first_name': 'Updated',
        'last_name': 'User'
    }
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
        role=role.objects.get(role='ADMIN')
    )

    # Create a Credentials instance associated with the created account
    Credentials.objects.create(
        email='test@example.com',
        password='hashed_password',
        idcuenta=Account.objects.get(cedula='1234567890')
    )

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
