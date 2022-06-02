from statistics import mode
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):
        #other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('userType', '3')

        return self.create_user(email, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    userTypes = ((1, "customer"), (2, "provider"), (3, "admin"))
    deviceType = ((1, "Android"), (2, "IOS"))
    genderType = ((1, "Male"), (2, "Female"), (3, "Transgender"), (4, "Non-Binary"), (5, "Prefer Not to Answer"))
    userApprovalStatus = ((1, "pending"), (2, "approved"), (3, "disapproved"))

    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    fullName = models.CharField(max_length=255, null=True)
    mobileNo = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    dateOfBirth = models.CharField(max_length=255, null=True)
    zipCode = models.CharField(max_length=255, null=False)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)
    deviceType = models.IntegerField(choices=deviceType, null=True)
    userType = models.IntegerField(choices=userTypes, null=False, default=None)
    genderType = models.IntegerField(choices=genderType, null=True)
    deviceToken = models.CharField(max_length=255, null=True)
    profileImage = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(default=0.00, blank=True, null=True)
    lng = models.FloatField(default=0.00, blank=True, null=True)
    last_login = models.DateTimeField(default=now, editable=False)
    isAvailable = models.BooleanField(default=False)
    isApproved = models.IntegerField(
        choices=userApprovalStatus, null=False, default=1)
    createdAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'mobileNo']
    objects = CustomAccountManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class licenseType(models.Model):
    licenseTypeName = models.CharField(max_length=255, null=False)
    therapyType = models.CharField(max_length=255, null=False, default=None)
    category = models.CharField(max_length=255, null=False, default=None)
    description = models.CharField(max_length=255, null=False, default=None)
    requirment = models.CharField(max_length=500, null=False, default=None)
    createdAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)

    class Meta:
        db_table = 'license_types'


class ProviderUserAdditionalData(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='providerData', db_column='userId')
    experience = models.IntegerField(null=False, default=0)
    licenseTypeId = models.ForeignKey(
        licenseType, on_delete=models.CASCADE, db_column='licenseTypeId', related_name="licenseTypeIdData")
    licenseName = models.CharField(max_length=255, null=True, blank=True)
    licenseNumber = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'provider_user_additional_data'


class ProviderUserLicenseDocs(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='providerLicenseDoc', db_column='userId')
    providerUserDocUrl = models.CharField(max_length=255, null=False)
    createdAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)

    class Meta:
        db_table = 'provider_user_docs'
