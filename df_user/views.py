# coding=utf-8
from django.shortcuts import render
from django.shortcuts import redirect
from hashlib import sha1
from .models import UserInfo
from . import user_decorator
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect


def register(request):
    context = {'title': '用户注册'}
    return render(request,'df_user/register.html',context)

def register_handle(request):
    #接收用户传过来的值
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))     # 指定编码格式，否则会报错
    upwd3 = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功，转向登录页面
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname = uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    '''接收登录请求信息'''
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)  # 是否记住用户
    #根据用户名查询对象
    users = UserInfo.objects.filter(uname = uname)
    print(uname)
    #判断：如果未查到则用户名错，如果查到则判断密码是否正确，正确则转到用户中心去
    if len(users)==1:
        s1=sha1()
        s1.update(upwd.encode('utf-8'))
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)
            #记住用户名
            if jizhu != 0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            request.session.set_expiry(0)
            return  red
        else:
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    else:
        context = {'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

def logout(request):
    request.session.flush()
    return redirect('/')

@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    user_address = UserInfo.objects.get(id=request.session['user_id']).uaddress
    #最近浏览
    goods_ids = request.COOKIES.get('goods_ids','1')
    goods_ids1 = goods_ids.split(',')
    goods_list =[]
    for goods_id in goods_ids1:
        print("----info----")
        print(goods_ids1)
        print("--------")
        goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title':'用户中心',
               'page_name': 1,
               'user_email':user_email,
               'user_name':request.session['user_name'],
               'user_uaddress':user_address,
               'goods_list':goods_list}
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request):
    uid = request.session['user_id']
    order_list = OrderInfo.objects.filter(user_id =uid).order_by('oIsPay','-oid')
    context = {'title': '用户中心',
               'page_name':1,
               'user_name': request.session['user_name'],
               'order_list':order_list,}
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    context = {'title': '用户中心',
               'page_name': 1,
               'user': user,
               'user_name': request.session['user_name']}
    return render(request,'df_user/user_center_site.html',context)

@user_decorator.login
def add_site(request):
    get = request.GET
    ushou = get.get('ushou')
    uaddress = get.get('uaddress')
    uyoubian = get.get('uyoubian')
    uphone = get.get('uphone')

    user = UserInfo.objects.get(id=request.session['user_id'])
    user.ushou = ushou
    user.uaddress = uaddress
    user.uyoubian = uyoubian
    user.uphone = uphone
    user.save()

    return redirect('/user/info/site/')

