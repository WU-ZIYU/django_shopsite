from django.contrib.auth import views as auth_views, logout
from .forms import LoginForm, SignupForm
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    # 使用SignupForm, 接受POST 请求内容
    form = SignupForm(request.POST or None)
    # 如果表单验证成功，保存数据
    if form.is_valid():
        form.save()
        redirect_url = 'login'
        # 获得验证后的 Email和密码
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        # 认证用户
        user = auth.authenticate(username=email, password=password)

        # 认证成功，登陆
        if user:
            auth.login(request, user)
            redirect_url = settings.LOGIN_REDIRECT_URL
        return redirect(redirect_url)
    # 表单验证不成功(包括GET请求) 显示注册模版
    ctx = {'form': form}
    return TemplateResponse(request, 'accounts/signup.html', ctx)


class NewLoginView(auth_views.LoginView):
    '''处理登陆的新视图'''
    template_name = 'accounts/login.html'
    form_class = LoginForm

@login_required
def LogoutView(request):
    logout(request)
    return TemplateResponse(request, 'accounts/login.html')