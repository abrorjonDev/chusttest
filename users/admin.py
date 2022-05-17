from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from import_export.resources import ModelResource
from import_export.admin import ImportExportModelAdmin
#local imports
from .models import User, UserDocs, UserFileModel

class UserResource(ModelResource):
    class Meta:
        model = User
     


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'username', 'password',
            'first_name', 'last_name',
            'is_superuser',
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class DocsInline(admin.StackedInline):
    model = UserDocs
    extra = 0
    fk_name = "user"

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, DjangoUserAdmin):
    resource_class = UserResource
    list_display = ('username', 'first_name', 'last_name', 'is_superuser', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')
    add_form = UserCreationForm
    form = UserChangeForm


    fieldsets = (
        (None, {'fields':('username', 'password')}),
        ('', {'fields':('email', 'first_name', 'last_name')}),
        ('PERMISSIONS', {
            'fields':('is_superuser', 'is_staff', 'is_active')
        }),
        ('IMPORTANT', {
            'fields':('date_joined', 'last_login')
        })
        
    )
    inlines = [DocsInline]


@admin.register(UserFileModel)
class UserFileAdmin(admin.ModelAdmin):
    list_filter = ('file', 'created_by', 'modified_by','date_created')
    