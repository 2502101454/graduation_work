# -*- coding: utf-8 -*-
#公共业务类
##########
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from ..forms import LoginForm, UserUForm, UPasswordForm, SearchUserForm, SearchNewsForm
from ..models import *
import json
from util import DeanUtil
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
util = DeanUtil()

class Common(object):

    def __int__(self):
        pass

    @csrf_exempt
    def user_login(self, request):
        if request.method == 'POST':
            result = {'status': False, 'message': None}
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username'].strip()
                password = form.cleaned_data['password'].strip()
                print 'username,', username
                print 'password,', password
                try:
                    user = None
                    if username.startswith('e'):
                        user = Employee.objects.get(id=username, password=password)
                        request.session['role'] = 'e'
                    if username.startswith('m'):
                        user = Manager.objects.get(id=username, password=password)
                        request.session['role'] = 'm'
                    if username.startswith('c'):
                        user = Ceo.objects.get(id=username, password=password)
                        request.session['role'] = 'c'
                    # 上面没报错那么肯定就找到了
                    if user:
                        # 登录成功，重定向到首页，首页相关用户信息，使用session传递
                        request.session['user'] = user
                        result['status'] = True
                        return HttpResponse(json.dumps(result))
                except Exception as e:
                    print e
                    # 登录失败，定制错误消息，用户名或密码不存在
                    result['status'] = False
                    result['message'] = {'password': [{'message': '用户名或密码不存在'}]}
                    return HttpResponse(json.dumps(result))
            # 错误消息
            else:
                #直接打印errors里面是<ul>...xxx内容。
                                    # 内部json.dumps
                error_str = form.errors.as_json()
                print 'login error_str', error_str, '\n', form.errors
                # 转为python对象，将result 返回给前台
                result['message'] = json.loads(error_str)
                return HttpResponse(json.dumps(result))
        else:
            pass
        return render(request, 'oa_core/login.html')

    def go_index(self, request):
        user = request.session.get('user')
        role = request.session.get('role')
        print 'user in session,', user
        print 'user role in session,', role
        data = {}
        data['user'] = user
        data['role'] = role
        return render(request, 'oa_core/index.html', data)

    def register_success(self, request):
        code = request.session.get('register_user_code')
        return render(request, 'oa_core/assign_code.html', {'code': code})

    def logout(self, request):
        request.session.flush()
        return HttpResponseRedirect(reverse('oa_core:index'))

    def user_center(self, request, user):
        id = user.id
        user_info = {'id': user.id,
                     'name': user.name,
                     'sex': user.sex,
                     'phone': user.phone,
                     'email': user.email,
                     'photo': user.photo,
                     'register_time': '',
                     'dept': '',
                     'job': '',
                     'upper': ''
                     }
        if id.startswith('e'):
            user_info['dept'] = user.dept.name
            user_info['register_time'] = user.register_time
            user_info['job'] = user.job
            user_info['upper'] = user.dept.manager.id
        elif id.startswith('m'):
            user_info['dept'] = user.dept.name
            user_info['upper'] = user.ceo.id
        elif id.startswith('c'):
            user_info['dept'] = user.dept
        photo = user.photo
        #photo字段在数据库表字段的类型是字符串，但是读取出来的作为对象的属性时，类型是django.db.models.fields.files.ImageFieldFile
        print 'photo type', type(photo)
        # photo.name属性可以获得文件相对于MediaRoot的路径（如果数据库中没有路径那么就是空串）
        print 'photo file path', photo.name
        if photo.name == '':
            user_info['photo'] = None
        return render(request, 'oa_core/user/user_detail.html', context=user_info)


    # 更新完毕还需要更换session中的user对象
    def user_info_update(self, request):
        if request.method == 'POST':
            result = {'status': False, 'message': None}
            # 绑定表单数据
            form = UserUForm(request.POST, request.FILES)
            if form.is_valid():
                user_id = form.cleaned_data['user_id']
                username = form.cleaned_data['username']
                sex = form.cleaned_data['sex']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                photo = form.cleaned_data['photo']
                print 'user_id:', user_id
                print 'username:', username
                print 'sex:', sex
                print 'email:', email
                print 'phone:', phone
                # 直接打印photo得到文件名称
                print 'photo', photo
                print 'type of photo', type(photo)
                user = None
                if user_id.startswith('e'):
                    user = get_object_or_404(Employee, pk=user_id)
                elif user_id.startswith('m'):
                    user = get_object_or_404(Manager, pk=user_id)
                elif user_id.startswith('c'):
                    user = get_object_or_404(Ceo, pk=user_id)
                user.name = username
                if sex:
                    user.sex = sex
                user.email = email
                user.phone = phone
                if photo:
                    user.photo = photo
                print 'saving....'
                user.save()
                request.session['user'] = user
                result['status'] = True
                return HttpResponse(json.dumps(result))
            else:
                errors_str = form.errors.as_json()
                print 'errors_str', errors_str
                error_body = util.error_body(errors_str)
                result['message'] = error_body
                return HttpResponse(json.dumps(result))
        else:
            user = request.session.get('user')
            return render(request, 'oa_core/user/modify.html')

    # 更新完毕还需要更换session中的user对象
    def user_password_update(self, request):
        if request.method == 'POST':
            result = {'status': False, 'message': None}
            # 绑定表单数据
            form = UPasswordForm(request.POST)
            if form.is_valid():
                user_id = form.cleaned_data['user_id']
                original_password = form.cleaned_data['original_password']
                new_password = form.cleaned_data['new_password']
                new_password2 = form.cleaned_data['new_password2']
                print 'user_id:', user_id
                print 'original_password:', original_password
                print 'new_password:', new_password
                print 'new_password2:', new_password2
                # 直接打印photo得到文件名称
                user = None
                if user_id.startswith('e'):
                    user = get_object_or_404(Employee, pk=user_id)
                elif user_id.startswith('m'):
                    user = get_object_or_404(Manager, pk=user_id)
                elif user_id.startswith('c'):
                    user = get_object_or_404(Ceo, pk=user_id)
                user.password = new_password
                user.save()
                request.session['user'] = user
                result['status'] = True
                return HttpResponse(json.dumps(result))
            else:
                errors_str = form.errors.as_json()
                print 'errors_str', errors_str
                error_body = util.error_body(errors_str)
                result['message'] = error_body
                return HttpResponse(json.dumps(result))
        else:
            return render(request, 'oa_core/user/update_password.html')


    # 查询当前用户的所有请假单
    def all_employees(self, request):
        res_data = {}
        form = SearchUserForm(request.GET)
        if form.is_valid():
            user_id = form.cleaned_data['user_id'].strip()
            name = form.cleaned_data['name'].strip()
            page_no = form.cleaned_data['page_no']
            print 'user_id strip:', user_id
            print 'name strip:', name
            all_employees = Employee.objects.filter(id__contains=user_id, name__contains=name)
            paginator = Paginator(all_employees, 4)
            if page_no > 0:
                print 'page_no:', page_no
                try:
                    page_obj = paginator.page(page_no)
                except Exception as e:
                    print 'page has exception:', e
                    page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(1)

            print 'page_obj number :', page_obj.number
            print 'page_obj.obj_list :', page_obj.object_list
            print 'page_obj.paginator.num_pages ', page_obj.paginator.num_pages
            print 'page_obj.paginator.count ', page_obj.paginator.count

            res_data['page_obj'] = page_obj
            res_data['search_condition'] = {
                'user_id': user_id,
                'name': name,
            }
        else:
            print form.errors.as_json()
            # 默认5条数据
            paginator = Paginator([], 5)
            # 默认第一页
            page_obj = paginator.page(1)
            res_data['page_obj'] = page_obj

        return render(request, 'oa_core/user/all_employees.html', res_data)

    def user_detail(self, request, user_id):
        if user_id.startswith('e'):
            user = get_object_or_404(Employee, pk=user_id)
        if user_id.startswith('m'):
            user = get_object_or_404(Manager, pk=user_id)
        if user_id.startswith('c'):
            user = get_object_or_404(Ceo, pk=user_id)
        return self.user_center(request, user)


    def all_managers(self, request):
        res_data = {}
        form = SearchUserForm(request.GET)
        if form.is_valid():
            user_id = form.cleaned_data['user_id'].strip()
            name = form.cleaned_data['name'].strip()
            page_no = form.cleaned_data['page_no']
            print 'user_id strip:', user_id
            print 'name strip:', name
            all_employees = Manager.objects.filter(id__contains=user_id, name__contains=name)
            paginator = Paginator(all_employees, 4)
            if page_no > 0:
                print 'page_no:', page_no
                try:
                    page_obj = paginator.page(page_no)
                except Exception as e:
                    print 'page has exception:', e
                    page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(1)

            print 'page_obj number :', page_obj.number
            print 'page_obj.obj_list :', page_obj.object_list
            print 'page_obj.paginator.num_pages ', page_obj.paginator.num_pages
            print 'page_obj.paginator.count ', page_obj.paginator.count

            res_data['page_obj'] = page_obj
            res_data['search_condition'] = {
                'user_id': user_id,
                'name': name,
            }
        else:
            print form.errors.as_json()
            # 默认5条数据
            paginator = Paginator([], 5)
            # 默认第一页
            page_obj = paginator.page(1)
            res_data['page_obj'] = page_obj

        return render(request, 'oa_core/user/all_managers.html', res_data)

    def all_ceo(self, request):
        res_data = {}
        form = SearchUserForm(request.GET)
        if form.is_valid():
            user_id = form.cleaned_data['user_id'].strip()
            name = form.cleaned_data['name'].strip()
            page_no = form.cleaned_data['page_no']
            print 'user_id strip:', user_id
            print 'name strip:', name
            all_employees = Ceo.objects.filter(id__contains=user_id, name__contains=name)
            paginator = Paginator(all_employees, 4)
            if page_no > 0:
                print 'page_no:', page_no
                try:
                    page_obj = paginator.page(page_no)
                except Exception as e:
                    print 'page has exception:', e
                    page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(1)

            print 'page_obj number :', page_obj.number
            print 'page_obj.obj_list :', page_obj.object_list
            print 'page_obj.paginator.num_pages ', page_obj.paginator.num_pages
            print 'page_obj.paginator.count ', page_obj.paginator.count

            res_data['page_obj'] = page_obj
            res_data['search_condition'] = {
                'user_id': user_id,
                'name': name,
            }
        else:
            print form.errors.as_json()
            # 默认5条数据
            paginator = Paginator([], 5)
            # 默认第一页
            page_obj = paginator.page(1)
            res_data['page_obj'] = page_obj

        return render(request, 'oa_core/user/all_ceo.html', res_data)

    def company_news(self, request):
        res_data = {}
        form = SearchNewsForm(request.GET)
        if form.is_valid():
            create_date = form.cleaned_data['create_date']
            name = form.cleaned_data['name'].strip()
            page_no = form.cleaned_data['page_no']
            print 'create_date:', create_date
            print 'name strip:', name
            all_news = News.objects.filter(name__contains=name)
            if create_date:
                all_news = all_news.filter(create_date=create_date)
            paginator = Paginator(all_news, 5)
            if page_no > 0:
                print 'page_no:', page_no
                try:
                    page_obj = paginator.page(page_no)
                except Exception as e:
                    print 'page has exception:', e
                    page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(1)

            print 'page_obj number :', page_obj.number
            print 'page_obj.obj_list :', page_obj.object_list
            print 'page_obj.paginator.num_pages ', page_obj.paginator.num_pages
            print 'page_obj.paginator.count ', page_obj.paginator.count

            res_data['page_obj'] = page_obj
            res_data['search_condition'] = {
                'create_date': create_date,
                'name': name,
            }
        else:
            print form.errors.as_json()
            # 默认5条数据
            paginator = Paginator([], 5)
            # 默认第一页
            page_obj = paginator.page(1)
            res_data['page_obj'] = page_obj

        return render(request, 'oa_core/news/all_news.html', res_data)

    def show_news(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        return render(request, 'oa_core/news/news_info.html', {"news": news})