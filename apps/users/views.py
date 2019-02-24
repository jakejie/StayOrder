# coding:utf-8
import datetime
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import View
from .models import CrawlTaskModel, UserProfile
# 定义使用邮箱进行登陆 重载方法
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login, logout
# 完成并集查询
from django.db.models import Q
# 对数据库找出来的内容进行分页
from django.core.paginator import Paginator

try:
    from .. import log_tool
except Exception as im_err:
    try:
        import log_tool
    except Exception as im_err:
        try:
            from order import log_tool
        except Exception as im_err:
            print("users.views 包导入错误：{}".format(im_err))

PAGE_SETTING = 10


# 主页视图 只需要一个页面
class IndexView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return render(request, 'index.html', {})
        else:
            return render(request, 'login.html', {})

    # 添加预约
    @staticmethod
    def post(request):
        if request.user.is_authenticated:
            name = request.POST.get('name', '')  # 姓氏
            username = request.POST.get('username', '')  # 名字
            birthday_date = request.POST.get('birthday_date', '')  # 出生日期
            stay_num = request.POST.get('stay_num', '')  # 居留许可证号码
            stay_end_date = request.POST.get('stay_end_date', '')  # 居留许可到期时间
            town = request.POST.get('town', '')  # 镇

            start_date = request.POST.get('start_date', '')  # 开始时间
            end_date = request.POST.get('end_date', '')  # 结束时间

            access_email = request.POST.get('email', '')  # 接收预约结果的邮箱
            if all([name, username, birthday_date,
                    stay_num, stay_end_date, town,
                    start_date, end_date]):
                log_tool.product_log("接收到爬虫任务",
                                     "用户：{}".format(request.user.username),
                                     "",
                                     "姓氏:{},名字:{},出生日期:{},\
                                     居留许可证号码:{},居留许可到期时间:{},镇:{},\
                                     开始时间:{},结束时间:{},接收预约结果的邮箱:{},"
                                     .format(name, username, birthday_date,
                                             stay_num, stay_end_date, town,
                                             start_date, end_date, access_email))

                user = CrawlTaskModel.objects.create(
                    user_id=request.user.id,  # 用户

                    name=name,  # 姓氏
                    username=username,  # 名字
                    # birthday_date=time.strftime("%Y-%m-%d".format(birthday_date)),  # 出生日期
                    birthday_date=datetime.datetime.strptime("{}".format(birthday_date), "%Y-%m-%d"),  # 出生日期

                    stay_num=stay_num,  # 居留许可证号码
                    # stay_end_date=time.strftime("%Y-%m-%d".format(stay_end_date)),  # 居留许可到期时间
                    stay_end_date=datetime.datetime.strptime("{}".format(stay_end_date), "%Y-%m-%d"),  # 居留许可到期时间
                    town=town,  # 镇

                    # start_date=time.strftime("%Y-%m-%d".format(start_date)),  # 开始时间
                    start_date=datetime.datetime.strptime("{}".format(start_date), "%Y-%m-%d"),  # 开始时间
                    # end_date=time.strftime("%Y-%m-%d".format(end_date)),  # 结束时间
                    end_date=datetime.datetime.strptime("{}".format(end_date), "%Y-%m-%d"),  # 结束时间

                    order_status=0,  # 预约状态
                    access_email=access_email,
                )
                user.save()
                return render(request, 'succeed.html',
                              {"msg": "任务提交成功", })
            else:
                return render(request, 'index.html',
                              {"msg": "数据不全"})
        else:
            return render(request, 'login.html', {})


# 历史提交记录
class CommitHistoryView(View):
    @staticmethod
    def get(request):
        # 如果已经登陆 跳转到主页
        if request.user.is_authenticated:
            content = CrawlTaskModel.objects.filter(
                user_id=request.user.id).all().order_by('-add_time')
            paginator = Paginator(content, PAGE_SETTING)
            page = request.GET.get('page')
            page = page if page else 1
            contacts = paginator.get_page(page)
            return render(request, 'history.html',
                          {"contacts": contacts,
                           "count": len(content)
                           })
        else:
            return HttpResponseRedirect(reverse('login'))


# 重构 允许使用邮箱/用户名进行登陆
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print("用户登录验证异常：{}".format(e))
            return None


# 登录视图
class LoginView(View):
    @staticmethod
    def get(request):
        return render(request, 'login.html', {})

    @staticmethod
    def post(request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if all([username, password]):
            user = authenticate(username=username, password=password)
            if user:
                if UserProfile.objects.get(username=username).is_active:
                    login(request, user)
                    log_tool.test_log("用户登录",
                                      "用户名：{}".format(request.user.username),
                                      "登陆成功",
                                      "正常登录")
                    return HttpResponseRedirect(reverse('index'))
                msg = "用户未激活 请联系管理员"
                log_tool.test_log("用户登录",
                                  "用户名：{}".format("null"),
                                  "登陆失败",
                                  "用户未激活")
            else:
                msg = "用户名或密码不对"
                log_tool.test_log("用户登录",
                                  "用户名：{}".format("null"),
                                  "登陆失败",
                                  "用户名或密码不对")
        else:
            msg = "用户名或密码不能为空"
            log_tool.test_log("用户登录",
                              "用户名：{}".format("null"),
                              "登陆失败",
                              "用户名或密码为空")
        return render(request, "login.html",
                      {"msg": msg})


# 退出登陆 跳转到登陆页面
class LogoutView(View):
    @staticmethod
    def get(request):
        # 如果已经登陆 跳转到主页
        if request.user.is_authenticated:
            # 已经登陆 退出登陆
            logout(request)
        return HttpResponseRedirect(reverse('login'))
