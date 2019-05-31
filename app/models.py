from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_employee(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_mgr', False)
        return self._create_user(email, password, **extra_fields)

    def create_manager(self, email, password, **extra_fields):
        extra_fields.setdefault('is_mgr', True)

        if extra_fields.get('is_mgr') is not True:
            raise ValueError('Manager must have is_mgr=True.')

        return self._create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """
    a = 'A'
    b = 'B'
    c = 'C'
    d = 'D'
    e = 'E'
    none = 'None'

    SENIORITY = [
       (a, 'A'),
       (b, 'B'),
       (c, 'C'),
       (d, 'D'),
       (e, 'E'),
       (none, 'None'),

    ]

    email = models.EmailField(
        _('Email Address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    full_name = models.CharField(_('Full Name'), max_length=150, blank=True)
    is_mgr = models.BooleanField(
        _('Manager status'),
        default=False,
        help_text=_('Designates whether the employee is a manager.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)
    seniority = models.CharField(
            max_length=1,
            choices=SENIORITY,
            blank=True, default=none
    )
    points = models.IntegerField(_('Points Accrued'), default=0)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.full_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
