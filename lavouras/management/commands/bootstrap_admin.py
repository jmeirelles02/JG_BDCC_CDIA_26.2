import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.db import transaction


class Command(BaseCommand):
    help = "Cria o administrador inicial usando as variáveis DJANGO_SUPERUSER_*."

    def handle(self, *args, **options):
        names = (
            "DJANGO_SUPERUSER_USERNAME",
            "DJANGO_SUPERUSER_EMAIL",
            "DJANGO_SUPERUSER_PASSWORD",
        )
        values = {name: os.environ.get(name, "") for name in names}
        if not any(values.values()):
            self.stdout.write("Criação do administrador desativada: variáveis ausentes.")
            return

        username = values[names[0]].strip()
        if not username:
            raise CommandError("Defina DJANGO_SUPERUSER_USERNAME.")

        User = get_user_model()
        with transaction.atomic():
            if User.objects.filter(username=username).exists():
                self.stdout.write("Usuário já existe; conta e senha foram preservadas.")
                return

            email = values[names[1]].strip()
            password = values[names[2]]
            if not password:
                raise CommandError(
                    "Defina DJANGO_SUPERUSER_PASSWORD "
                    "para criar o administrador."
                )
            user = User(username=username, email=email, is_staff=True, is_superuser=True)
            try:
                user.full_clean(exclude=["password"])
                if email:
                    validate_email(email)
                validate_password(password, user=user)
            except ValidationError:
                # Não incluir valores das variáveis nem a senha nos logs do deploy.
                raise CommandError(
                    "Credenciais inválidas: confira o usuário, o e-mail e use uma senha "
                    "forte, com pelo menos 8 caracteres, não comum, não apenas numérica "
                    "e diferente do usuário/e-mail."
                ) from None

            User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS("Administrador criado com sucesso."))
