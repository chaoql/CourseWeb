from django import forms
from captcha.fields import CaptchaField

from apps.users.models import UserProfile


class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1'] != \
                self.cleaned_data['password2']:
            raise forms.ValidationError("密码不一致")
        return self.cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name", "gender", "birthday", "address"]


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


class LoginForm(forms.Form):
    """
    实现表单验证功能
    """
    username = forms.CharField(required=True, min_length=2)  # 变量名必须与前端name标签保持一致
    password = forms.CharField(required=True, min_length=6)


class DynamicLoginForm(forms.Form):
    # myfield = AnyOtherField()
    captcha = CaptchaField()


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    captcha = CaptchaField()
    email = forms.EmailField(required=True)  # 变量名必须与前端name标签保持一致
    password = forms.CharField(required=True, min_length=6)

    def clean_email(self):
        email = self.data.get("email")
        users = UserProfile.objects.filter(email=email)
        if users:
            raise forms.ValidationError("该邮箱已注册")
        return email
