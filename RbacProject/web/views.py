from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Count
from django.utils import timezone
from web import models, forms
from rbac.service import initial_permission
import json
import datetime


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        u = request.POST.get('userName')
        p = request.POST.get('password')
        obj = models.UserInfo.objects.filter(user__userName=u, user__password=p).first()
        # print(u, p, obj)
        if obj:
            request.session['userInfo'] = {'userName': u, 'nickName': obj.nickName, 'nid': obj.id}
            initial_permission(request, obj.user_id)
            return redirect('/index.html')
        else:
            return render(request, 'login.html')


def logout(request):
    request.session.delete(request.session.session_key)
    return HttpResponse('已成功退出！')


def index(request):
    if not request.session.get('userInfo'):
        return redirect('/login.html')
    return render(request, 'index.html')


def trouble(request):
    userId = request.session['userInfo']['nid']
    troubleList = models.Order.objects.filter(createUser_id=userId)
    request.permission_code_list.remove('LOOK')
    # request.permission_code_list.remove('POST')
    codeDict = {
        'POST': '创建报障',
        'EDIT': '修改',
        'DEL': '删除',
        'LOOK': '查看列表',
        'DETAIL': '查看详细',
    }
    codeList = [{x: codeDict[x]} for x in request.permission_code_list]
    # print(request.session['userInfo'])
    if request.permission_code == "LOOK":
        # print(request.session['userInfo']['nid'])
        # troubleList = models.Order.objects.filter(createUser_id=request.session['userInfo']['nid'])
        return render(request, 'trouble.html', {'troubleList': troubleList, 'codeList': codeList})
    elif request.permission_code == "POST":
        # print('post...trouble')
        if request.method == "GET":
            # print('trouble...get')
            return render(request, 'trouble-new.html')
        else:
            title = request.POST.get('title')
            detail = request.POST.get('detail')
            # print(title, detail, userId)
            models.Order.objects.create(title=title, detail=detail, createUser_id=userId)
            return redirect('/trouble.html')
    elif request.permission_code == "DETAIL":
        troubleId = request.GET.get('id')
        troubleDetail = models.Order.objects.filter(id=troubleId, createUser_id=userId).first()
        return render(request, 'trouble-detail.html', {'troubleDetail': troubleDetail})
    elif request.permission_code == "EDIT":
        if request.method == 'GET':
            troubleId = request.GET.get('id')
            troubleDetail = models.Order.objects.filter(id=troubleId, createUser_id=userId).first()
            return render(request, 'trouble-edit.html', {'troubleDetail': troubleDetail, 'troubleId': troubleId})
        else:
            troubleId = request.GET.get('id')
            newTitle = request.POST.get('title')
            newDetail = request.POST.get('detail')
            # print(troubleId, newTitle, newDetail, userId)
            models.Order.objects.filter(id=troubleId, createUser_id=userId).update(title=newTitle, detail=newDetail)
            return render(request, 'trouble.html', {'troubleList': troubleList})
    elif request.permission_code == "DEL":
        ret = {'code': 'success'}
        troubleId = request.GET.get('id')
        print(userId, troubleId)
        obj = models.Order.objects.filter(id=troubleId, createUser_id=userId).first()
        print(obj, userId, troubleId)
        if obj:
            obj.delete()
        else:
            ret['code'] = 'error'
        return HttpResponse(json.dumps(ret))


def troublekill(request):
    troubleList = models.Order.objects.all()
    processorId = request.session['userInfo']['nid']
    request.permission_code_list.remove('LOOK')
    codeDict = {
        # 'POST': '创建报障',
        # 'EDIT': '修改',
        # 'DEL': '删除',
        # 'LOOK': '查看列表',
        'DETAIL': '查看详细',
        'SOLVE': '抢单',
    }
    codeList = [{x: codeDict[x]} for x in request.permission_code_list]
    print(request.permission_code_list)
    if request.permission_code == "LOOK":
        return render(request, 'trouble-kill.html', {'troubleList': troubleList, 'codeList': codeList})
    elif request.permission_code == "DETAIL":
        troubleId = request.GET.get('id')
        troubleDetail = models.Order.objects.filter(id=troubleId).first()
        return render(request, 'trouble-kill-detail.html', {'troubleDetail': troubleDetail})
    elif request.permission_code == "SOLVE":
        if request.method == 'GET':
            troubleId = request.GET.get('id')
            type = request.GET.get('type')
            troubleDetail = models.Order.objects.filter(id=troubleId).first()
            print(troubleDetail.status, type)
            if type == 'undo':
                #若取消解决报障，恢复处理状态为1(未处理)，处理人为None
                troubleDetail.status = 1
                troubleDetail.processor_id = None
                troubleDetail.save()
                return redirect('/trouble_kill.html')
            if troubleDetail.status == 1:
                #若当前报障单状态为1(未处理)，表示抢单成功，须将该报障单状态修改为2(处理中)，处理人修改为当前登陆用户
                troubleDetail.status = 2
                troubleDetail.processor_id = processorId
                troubleDetail.save()
                obj = forms.OrderForm(initial={'title': troubleDetail.title, 'detail': troubleDetail.detail})
                obj.fields['title'].widget.attrs.update({'disabled': None})
                obj.fields['detail'].widget.attrs.update({'disabled': None})
                return render(request, 'trouble-kill-solve.html', {'obj': obj, 'troubleId': troubleId})
            else:
                #若该报障单已被当前登陆用户抢下，继续处理。。。
                if troubleDetail.processor_id == processorId and troubleDetail.status == 2:
                    obj = forms.OrderForm(initial={'title': troubleDetail.title, 'detail': troubleDetail.detail})
                    obj.fields['title'].widget.attrs.update({'disabled': None})
                    obj.fields['detail'].widget.attrs.update({'disabled': None})
                    return render(request, 'trouble-kill-solve.html', {'obj': obj, 'troubleId': troubleId})
                # 若该报障单已被他人处理，显示提示信息
                else:
                    return HttpResponse('该报障单正在被处理。。。或已被处理完成')
        else:
            obj = forms.OrderForm(request.POST)
            obj.fields['title'].required = False
            obj.fields['detail'].required = False
            obj.fields['status'].required = False   # 无需用户选择，提交之后更改为3(已处理)
            troubleId = request.GET.get('id')
            if obj.is_valid():
                models.Order.objects.filter(id=troubleId, processor_id=processorId).update(
                    solution=obj.cleaned_data['solution'], status=3, processTime=timezone.now())
                return redirect('/trouble_kill.html')
            else:
                print('wrong', obj.errors)
                return render(request, 'trouble-kill-solve.html', {'obj': obj, 'troubleId': troubleId})


def report(request):
    if request.permission_code == "LOOK":
        #饼图
        if request.method == 'GET':
            return render(request, 'report.html')
        else:
            pieList = models.Order.objects.filter(status=3).values_list('processor__nickName').annotate(num=Count('id'))
            print(pieList)
            lineDateList = models.Order.objects.filter(status=3).extra(select={'ymd': "strftime('%%s', strftime('%%Y-%%m-%%d', processTime))"}).values('processor_id', 'processor__nickName', 'ymd').annotate(num=Count('id'))
            lineDataDict = {}
            for data in lineDateList:
                key = data['processor_id']
                if key in lineDataDict:
                    lineDataDict[key]['data'].append([float(data['ymd'])*1000, data['num']])
                else:
                    lineDataDict[key] = {'name': data['processor__nickName'], 'data': [[float(data['ymd'])*1000, data['num']], ]}
            print(list(lineDataDict.values()))
            response = {
                'pieData': list(pieList),
                'lineData': list(lineDataDict.values())
            }
            return HttpResponse(json.dumps(response))

