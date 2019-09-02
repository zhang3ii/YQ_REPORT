from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SearchReport
from django.db.models import Count

@api_view(['GET', 'POST'])
def WordSearch(request):
    pageNum = int(request.GET.get('pageNum', '1'))
    keyword = request.GET.get('keyword', '')
    rsp = {'status': status.HTTP_200_OK, 'msg': 'ok'}
    try:
        result = searchWord(pageNum, keyword)
        rsp['data'] = result[0]
        rsp['pageNum'] = result[1]
    except Exception as reason:
        rsp['status'] = status.HTTP_400_BAD_REQUEST
        rsp['msg'] = str(reason)
    return Response(rsp)

def searchWord(pageNum, keyword):
    if not keyword:
        data = list(SearchReport.objects.all().order_by('-report_time').values())
    else:
        data = list(SearchReport.objects.filter(title__icontains=keyword).order_by('-report_time').values())
    totalPnum, begin, end = countPage(len(data), size=15, p=pageNum)
    page_nums = (len(data)//15 + 1) * 10
    if int(pageNum) <= totalPnum:
        outputData = data[begin:end]
    else:
        outputData = []
    return (outputData,page_nums)

def countPage(total, size=15, p=1):
    if total % size == 0:
        totalPnum = int(total / size)
    else:
        totalPnum = int(total / size) + 1
    begin = (p - 1) * size
    end = p * size
    return totalPnum, begin, end

@api_view(['GET', 'POST'])
def collect_api(request):
    edit_id = int(request.GET.get('edit_id', '1'))
    rsp = {'status': status.HTTP_200_OK, 'msg': 'ok'}
    try:
        update_statue(edit_id)
    except Exception as reason:
        rsp['status'] = status.HTTP_400_BAD_REQUEST
        rsp['msg'] = str(reason)
    return Response(rsp)

def update_statue(edit_id):
    dt = datetime.now()
    n = dt.strftime('%W')
    title = '第' + n + '周舆情周报'
    SearchReport.objects.filter(id=edit_id).update(collect_time=title)

@api_view(['GET', 'POST'])
def today_report(request):
    keyword = request.GET.get('report_title', '')
    rsp = {'status': status.HTTP_200_OK, 'msg': 'ok'}
    datas = list(SearchReport.objects.filter(collect_time=keyword).values())
    rsp['data'] = datas
    return Response(rsp)

#列表
@api_view(['GET', 'POST'])
def group_time(request):
    rsp = {'status': status.HTTP_200_OK, 'msg': 'ok'}
    result = list(SearchReport.objects.values('collect_time').filter(collect_time__isnull=False).annotate(dcount=Count('collect_time')))
    rsp['report_list'] = result
    return Response(rsp)

#删除周报
@api_view(['GET', 'POST'])
def delete_report(request):
    CollectTime = request.GET.get('collect_time', '1')
    rsp = {'status': status.HTTP_200_OK, 'msg': 'ok'}
    SearchReport.objects.filter(collect_time=CollectTime).update(collect_time=None)
    return Response(rsp)

#更新周报保存
@api_view(['GET', 'POST'])
def update_report(request):
    rsp = {'status': status.HTTP_200_OK, 'msg': 'ok'}
    ID = request.GET.get('id', '')
    title = request.GET.get('title', '')
    digest = request.GET.get('digest', '')
    report_time = request.GET.get('report_time', '')
    url = request.GET.get('url', '')
    source = request.GET.get('source', '')
    SearchReport.objects.filter(id=ID).update(title=title, digest=digest, report_time=report_time, url=url,source=source)
    return Response(rsp)

#删除周报
@api_view(['GET', 'POST'])
def delete_report_by_id(request):
    re_id = request.GET.get('re_id', '')
    rsp = {'status': status.HTTP_200_OK, 'msg': 'ok'}
    SearchReport.objects.filter(id=re_id).update(collect_time=None)
    return Response(rsp)

#增加数据
@api_view(['GET', 'POST'])
def add_data(request):
    collect_time = request.GET.get('collect_time', '')
    rsp = {'status': status.HTTP_200_OK, 'msg': 'ok'}
    obj = SearchReport(collect_time=collect_time)
    obj.save()
    return Response(rsp)













