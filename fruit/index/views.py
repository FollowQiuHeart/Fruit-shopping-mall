import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
# Create your views here.
def index(request):
    return render(request,"index.html")
#装饰器
def check_logging(fn):

    def wrap(request,*args,**kwargs):
        #检查当前用户是否登录
        if 'username' not in request.session or 'uid'  not in request.session:
            #有可能没有登录
            if 'username' not in request.COOKIES or 'uid' not in request.COOKIES:
                #肯定没有登录
                return HttpResponseRedirect("/user/login")
            else:
                request.session["username"] = request.COOKIES.get("username")
                request.session["uid"] = request.COOKIES.get("uid")
        return fn(request,*args,**kwargs)
    return wrap

def check_login(request):
    res = {}
    if "uname" in request.session and "uid" in request.session:
        res["login_state"] = 1
        res["uname"] = request.session["uname"]
        return JsonResponse(res)
    if "uname" in request.session and "uid" in request.COOKIES:
        res["login_state"] = 1
        res["uname"] = request.COOKIES.get("uname")
        request.session["uname"] = request.COOKIES.get("uname")
        request.session["uid"] = request.COOKIES.get("uid")
        return JsonResponse(res)
    res["login_state"] = 0
    return JsonResponse(res)

def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    if request.method == "POST":
        uname = request.POST.get('uname')
        upwd = request.POST.get("upwd")
        users = User.objects.filter(uname=uname, upwd=upwd)
        dic = {}
        if users:
            dic["login_state"] = 1
            resp = JsonResponse(dic)
            request.session["uname"] = uname
            request.session["uid"] = users[0].id
            resp.set_cookie("uname",uname,60*60*24*30)
            resp.set_cookie("uid",users[0].id,60*60*24*30)
            return resp
        else:
            dic['login_state'] = 0
            return JsonResponse(dic)

def register(request):
    if request.method == "GET":
        return render(request,"register.html")
    if request.method == "POST":
        uname = request.POST.get("uname","")
        res = {}
        if uname == "":
            res["info"] = "用户名不能为空"
            return JsonResponse(res)
        uphone = request.POST.get("uphone","")
        if uphone == "":
            res["info"] = "手机号不能为空"
            return JsonResponse(res)
        uemail = request.POST.get("uemail","")
        if uemail == "":
            res["info"] = "邮箱不能为空"
            return JsonResponse(res)
        upwd_1 = request.POST.get("upwd_one","")
        upwd_2 = request.POST.get("upwd_two","")
        if upwd_1 == "" or upwd_2 == "":
            res["info"] = "密码不能为空"
            return JsonResponse(res)
        users = User.objects.filter(uname=uname)

        if users:
            res["info"] = "用户名已注册"
            return JsonResponse(res)
        if  upwd_1 != upwd_2 :
            res["info"] = "两次密码输入不匹配！"
            return JsonResponse(res)

        user = User.objects.create(uphone=uphone,uname=uname,
                                   upwd=upwd_1,uemail=uemail,isActive=True)
        res["info"] = "注册成功"
        return JsonResponse(res)

def logout(request):
    resp = render(request,"login.html")
    del  request.session["uname"]
    del  request.session["uid"]
    resp.delete_cookie("uname")
    resp.delete_cookie("uid")
    return resp

def load_goods(request):
    #加载商品
    #[{'type':{'title':'热带水果'},'goods':[{},...]}..]
    all_list = []
    all_types = GoodsType.objects.all()
    for _type in all_types:
        data = {}
        data['type'] = {'title':_type.title}
        data['goods'] = []
        all_goods = _type.goods_set.filter(isActive=True).order_by("-created_time")[:10]
        for good in all_goods:
            d = {}
            d["title"] = good.title
            d["price"] = str(good.price)
            d["spec"]  = good.spec
            d["picture"] = str(good.picture)
            data["goods"].append(d)
        all_list.append(data)

    return HttpResponse(json.dumps(all_list),content_type="application/json")