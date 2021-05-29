from django.contrib.auth import forms as auth_form
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

# 登陆相关视图与验证器
def validate_email_domain(value):
    '''判断输入的email是否满足格式'''
    if not value.endswith("qq.com"):
        raise ValidationError("Enter a valid email address")


class LoginForm(auth_form.AuthenticationForm):
    '''继承并修改AuthenticationForm'''
    username = forms.EmailField(
        min_length = 6,
        widget = forms.EmailInput(
            attrs={'class': 'form-control'}
        ),
        validators=[validate_email_domain]
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )


class SignupForm(forms.ModelForm):
    # 字段名改为email
    email = forms.EmailField(
        min_length=6,
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        # 指定模型为用户模型
        model = User
        fields = ('email',)

    def save(self, request=None, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        # 设置密码
        user.set_password(password)
        if commit:
            user.save()
        return user




