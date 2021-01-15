import hashlib
import datetime
import time
import calendar
from django.shortcuts import render
import requests
import pymysql
import json
from django.http import HttpResponse, JsonResponse
# from .models import form_ShiPin_Report
# from datetime import datetime, timedelta
from django.db.models import Q
import pymysql
from .models import video_user as User
from .models import FormShipinReport as ShiPin
from .models import *
# Create your views here.


def index(request):
    db = pymysql.connect('localhost', 'root', '000000', 'v')
    cursor = db.cursor()
    name_sql = "select * from form_ShiPin_Report ORDER BY ID DESC limit 8"
    cursor.execute(name_sql)
    result = cursor.fetchall()
    db.commit()
    db.close()
    data = {'data':[]}
    for i in result:
        d1 = {
            'name': '-'.join(i[7].split('-')[3:]),
            'url': i[3]
        }
        data['data'].append(d1)
    response = HttpResponse(json.dumps(data))
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    # response["Access-Control-Allow-Headers"] = " * "
    return response


def player_video(request):
    data = {'data': []}
    player = request.GET.get('player')
    match = ShiPin.objects.filter(Q(single_line_shipinmingcheng__icontains=player))
    for i in match:
        dd = {
            'name': '-'.join(i.single_line_shipinmingcheng.split('-')[3:]),
            'url': i.url
        }
        data['data'].append(dd)
    response = HttpResponse(json.dumps(data))
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    # response["Access-Control-Allow-Headers"] = " * "
    return response


def project_video(request):
    data = {'data': []}
    match = request.GET.get('match')
    year = request.GET.get('year')
    project = request.GET.get('project')
    results = ShiPin.objects.filter(Q(single_line_shipinmingcheng__icontains=match))
    for i in results:
        n = i.single_line_shipinmingcheng.split('-')
        if n[0] == year:
            if int(n[5]) != 9 and n[4] == project:
                dd = {
                    'name': '-'.join(i.single_line_shipinmingcheng.split('-')[3:]),
                    'url': i.url
                }
                data['data'].append(dd)
    response = HttpResponse(json.dumps(data))
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    # response["Access-Control-Allow-Headers"] = " * "
    return response


def playercn_info(request):
    data = {}
    player = request.GET.get('player')
    xinxi = [player, 0, 0, 0, 0, 0, 0, 0, 0]
    playerid = FormYundongyuanReport.objects.filter(single_line_zhongwenming=player)[0].id
    player_yingwenming = FormYundongyuanReport.objects.filter(single_line_zhongwenming=player)[0].single_line_yingwenming
    res_sjpm = FormPaiming.objects.filter(Q(form_yundongyuan_id=playerid) & Q(dropdown_paimingfenlei='世界排名'))
    sjpms = []
    for i in res_sjpm:
        pmri = int(i.formula_riqi)
        pm = i.number_paiming
        sjpms.append([pmri, pm])
    sjpms.sort(key=lambda x:x[0], reverse=True)
    sjpm = sjpms[0][1]

    res_zjspm = FormPaiming.objects.filter(Q(form_yundongyuan_id=playerid) & Q(dropdown_paimingfenlei='总决赛排名'))
    zjspms = []
    for i in res_zjspm:
        pmri = int(i.formula_riqi)
        pm = i.number_paiming
        zjspms.append([pmri, pm])
    zjspms.sort(key=lambda x: x[0], reverse=True)
    zjspm = zjspms[0][1]

    res_jf_2020 = FormJifen.objects.filter(Q(form_yundongyuan=player_yingwenming) & Q(number_nian='2020'))
    mc_2020_1 = 0
    mc_2020_2 = 0
    mc_2020_3 = 0
    for i in res_jf_2020:
        if i.dropdown_mingci == '1':
            mc_2020_1 += 1
        elif i.dropdown_mingci == '2':
            mc_2020_2 += 1
        elif i.dropdown_mingci == '3/4':
            mc_2020_3 += 1

    res_jf_2021 = FormJifen.objects.filter(Q(form_yundongyuan=player_yingwenming) & Q(number_nian='2021'))
    mc_2021_1 = 0
    mc_2021_2 = 0
    mc_2021_3 = 0
    for i in res_jf_2021:
        if i.dropdown_mingci == '1':
            mc_2021_1 += 1
        elif i.dropdown_mingci == '2':
            mc_2021_2 += 1
        elif i.dropdown_mingci == '3/4':
            mc_2021_3 += 1
    xinxi[1] = sjpm
    xinxi[2] = zjspm
    xinxi[3] = mc_2021_1
    xinxi[4] = mc_2021_2
    xinxi[5] = mc_2021_3
    xinxi[6] = mc_2020_1
    xinxi[7] = mc_2020_2
    xinxi[8] = mc_2020_3

    jctn = [Form3000M, Form30M, FormBmi, FormWotuiMax, FormZuoweitiqianqu, FormChuizhizongtiao, FormYintixiangshang, FormShendunMax, FormBeijinaili, FormFujinaili]
    zxtn = [Form400Mx5, FormLidingtiaoyuan, FormYuandierjitiaoZuo, FormYuandierjitiaoYou, Form5000M, FormShendun90Kg, FormShuangyao1500, FormSijiaopao20]
    pinfen_jctn = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    pinfen_zxtn = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    pinfen_fms = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    times_jctn = []
    data_jctn = []
    for i in jctn:
        result = i.objects.filter(form_yundongyuan=player)
        for j in result:
            # print(j)
            try:
                t1_cs = j.date_field_ceshi.split('-')
            except Exception as e:
                t1_cs = j.date_field_ceshiriqi.split('-')
            y = str(t1_cs[2])
            m = str(list(calendar.month_abbr).index(t1_cs[1])).zfill(2)
            d = str(t1_cs[0])
            t1 = int(y + m + d)
            if t1 not in times_jctn:
                times_jctn.append(t1)
            try:
                d1 = [t1, str(i).split("'")[1].split('.')[2], j.dropdown_pingfen]
            except Exception as e:
                d1 = [t1, str(i).split("'")[1].split('.')[2], j.number_pingfen]
            if d1 not in data_jctn:
                data_jctn.append(d1)
    times_jctn.sort(reverse=True)
    times_jctn = times_jctn[:6]
    for t_jctn in times_jctn:
        n = times_jctn.index(t_jctn)
        for j in data_jctn:
            if j[2] != '':
                pf_jctn = int(j[2])
            else:
                pf_jctn = 0
            if t_jctn == j[0]:
                if j[1] == 'Form3000M':
                    pinfen_jctn[n][0] = pf_jctn
                elif j[1] == 'Form30M':
                    pinfen_jctn[n][1] = pf_jctn
                elif j[1] == 'FormBmi':
                    pinfen_jctn[n][2] = pf_jctn
                elif j[1] == 'FormWotuiMax':
                    pinfen_jctn[n][3] = pf_jctn
                elif j[1] == 'FormZuoweitiqianqu':
                    pinfen_jctn[n][4] = pf_jctn
                elif j[1] == 'FormChuizhizongtiao':
                    pinfen_jctn[n][5] = pf_jctn
                elif j[1] == 'FormYintixiangshang':
                    pinfen_jctn[n][6] = pf_jctn
                elif j[1] == 'FormShendunMax':
                    pinfen_jctn[n][7] = pf_jctn
                elif j[1] == 'FormBeijinaili':
                    pinfen_jctn[n][8] = pf_jctn
                elif j[1] == 'FormFujinaili':
                    pinfen_jctn[n][9] = pf_jctn
    times_zxtn = []
    data_zxtn = []
    for i in zxtn:
        result = i.objects.filter(form_yundongyuan=player)
        pf = []
        for j in result:
            # print(j)
            try:
                t1_cs = j.date_field_ceshi.split('-')
            except Exception as e:
                t1_cs = j.date_field_ceshiriqi.split('-')
            y = str(t1_cs[2])
            m = str(list(calendar.month_abbr).index(t1_cs[1])).zfill(2)
            d = str(t1_cs[0])
            t1 = int(y + m + d)
            if t1 not in times_zxtn:
                times_zxtn.append(t1)
            try:
                d1 = [t1, str(i).split("'")[1].split('.')[2], j.dropdown_pingfen]
            except Exception as e:
                d1 = [t1, str(i).split("'")[1].split('.')[2], j.number_pingfen]
            if d1 not in data_zxtn:
                data_zxtn.append(d1)
    times_zxtn.sort(reverse=True)
    times_zxtn = times_zxtn[:6]
    for t_zxtn in times_zxtn:
        n = times_zxtn.index(t_zxtn)
        for j in data_zxtn:
            if j[2] != '':
                pf_zxtn = int(j[2])
            else:
                pf_zxtn = 0
            if t_zxtn == j[0]:
                if j[1] == 'Form400Mx5':
                    pinfen_zxtn[n][0] = pf_zxtn
                elif j[1] == 'FormLidingtiaoyuan':
                    pinfen_zxtn[n][1] = pf_zxtn
                elif j[1] == 'FormYuandierjitiaoZuo':
                    pinfen_zxtn[n][2] = pf_zxtn
                elif j[1] == 'FormYuandierjitiaoYou':
                    pinfen_zxtn[n][3] = pf_zxtn
                elif j[1] == 'Form5000M':
                    pinfen_zxtn[n][4] = pf_zxtn
                elif j[1] == 'FormShendun90Kg':
                    pinfen_zxtn[n][5] = pf_zxtn
                elif j[1] == 'FormShuangyao1500':
                    pinfen_zxtn[n][6] = pf_zxtn
                elif j[1] == 'FormSijiaopao20':
                    pinfen_zxtn[n][7] = pf_zxtn


    times_fms = []
    data_fms = []
    fms = ['上踏步（左）', '上踏步（右）', '直线弓箭步（左）', '直线弓箭步（右）', '肩部灵活性（左）', '肩部灵活性（右）', '直腿主动上抬（左）', '直腿主动上抬（右）', '深蹲',
           '躯干稳定俯卧撑', '扭转稳定性（左）', '扭转稳定性（右）']
    for i in fms:
        result = Fms.objects.filter(Q(form_yundongyuan=player) & Q(dropdown_dongzuo=i))
        for j in result:
            try:
                t1_cs = j.date_field_ceshi.split('-')
            except Exception as e:
                t1_cs = j.date_field_ceshiriqi.split('-')
            y = str(t1_cs[2])
            m = str(list(calendar.month_abbr).index(t1_cs[1])).zfill(2)
            d = str(t1_cs[0])
            t1 = int(y + m + d)
            if t1 not in times_fms:
                times_fms.append(t1)
            d1 = [t1, i, j.number_pingfen]
            if d1 not in data_fms:
                data_fms.append(d1)
    times_fms.sort(reverse=True)
    times_fms = times_fms[:6]
    for t_fms in times_fms:
        n = times_fms.index(t_fms)
        for j in data_fms:
            if j[2] != '':
                pf_fms = int(j[2])
            else:
                pf_fms = 0
            if t_fms == j[0]:
                if j[1] == '上踏步（左）':
                    pinfen_fms[n][0] = pf_fms
                elif j[1] == '上踏步（右）':
                    pinfen_fms[n][1] = pf_fms
                elif j[1] == '直线弓箭步（左）':
                    pinfen_fms[n][2] = pf_fms
                elif j[1] == '直线弓箭步（右）':
                    pinfen_fms[n][3] = pf_fms
                elif j[1] == '肩部灵活性（左）':
                    pinfen_fms[n][4] = pf_fms
                elif j[1] == '肩部灵活性（右）':
                    pinfen_fms[n][5] = pf_fms
                elif j[1] == '直腿主动上抬（左）':
                    pinfen_fms[n][6] = pf_fms
                elif j[1] == '直腿主动上抬（右）':
                    pinfen_fms[n][7] = pf_fms
                elif j[1] == '深蹲':
                    pinfen_fms[n][8] = pf_fms
                elif j[1] == '躯干稳定俯卧撑':
                    pinfen_fms[n][9] = pf_fms
                elif j[1] == '扭转稳定性（左）':
                    pinfen_fms[n][10] = pf_fms
                elif j[1] == '扭转稳定性（右）':
                    pinfen_fms[n][11] = pf_fms

    res_xxl = FormXunlianliang.objects.filter(form_yundongyuan=player)
    result_xxl = []
    keys = []
    for i in res_xxl:
        xx_time = i.date_field_xunlianriqi.split('-')
        y = str(xx_time[2])
        m = str(list(calendar.month_abbr).index(xx_time[1])).zfill(2)
        d = str(xx_time[0])
        t1 = y+'-'+m+'-'+d
        t2 = int(y+m+d)
        result_xxl.append([t2, i.dropdown_xunliankemu, int(i.number_xunlianshichang)])
        if t1 not in keys:
            keys.append(t1)
    keys.sort(reverse=True)
    max_time = keys[0]
    # max_time2 = keys[7]
    # max_time3 = keys[14]
    # max_time4 = keys[21]
    # max_time5 = keys[28]
    # max_time6 = keys[35]
    # print(keys)
    # print(max_time1, max_time2, max_time3, max_time4, max_time5, max_time6)
    key_list = []
    ind = 1
    keys.append('2200-01-01')
    while ind < len(keys)-1:
        # print(int(time.mktime(time.strptime(keys[ind], '%Y-%m-%d')))-int(time.mktime(time.strptime(keys[ind-1], '%Y-%m-%d'))))
        # print(int(time.mktime(time.strptime(keys[ind-1], '%Y-%m-%d'))))
        if int(time.mktime(time.strptime(keys[ind], '%Y-%m-%d'))) - int(time.mktime(time.strptime(keys[ind-1], '%Y-%m-%d'))) == -86400:
            start = ind - 1
            while int(time.mktime(time.strptime(keys[ind], '%Y-%m-%d'))) - int(time.mktime(time.strptime(keys[ind-1], '%Y-%m-%d'))) == -86400:
                ind += 1
            k1 = int(''.join(keys[start].split('-')))
            key_list.append(k1)
        else:
            ind += 1
    # for i in keys:
    #     format_time = int(time.mktime(time.strptime(i, '%Y-%m-%d')))
    shichang_xxl = []
    for i in key_list:
        shichang = [0, 0, 0, 0]
        jzs = []
        xjs = []
        tnzx = []
        tnll = []
        for j in result_xxl:
            if i-6 <= j[0] <= i:
                if j[1] == '技术（技战术）':
                    jzs.append(j[2])
                    # shichang[0] = j[2]
                elif j[1] == '技术（小技术）':
                    xjs.append(j[2])
                    # shichang[1] = j[2]
                elif j[1] == '体能（专项）':
                    tnzx.append(j[2])
                    # shichang[2] = j[2]
                elif j[1] == '体能（力量）':
                    tnll.append(j[2])
                    # shichang[3] = j[2]
        shichang[0] = sum(jzs)
        shichang[1] = sum(xjs)
        shichang[2] = sum(tnzx)
        shichang[3] = sum(tnll)
        shichang_xxl.append(shichang)
    while len(shichang_xxl) < 6:
        shichang_xxl.append([0, 0, 0, 0])
    res_slsh = FormShenglishenghua.objects.filter(form_yundongyuan=player)
    result_slsh = []
    t_list = []
    for i in res_slsh:
        xx_time = i.date_field_ceshiriqi.split('-')
        y = str(xx_time[2])
        m = str(list(calendar.month_abbr).index(xx_time[1])).zfill(2)
        d = str(xx_time[0])
        t1 = int(y + m + d)
        result_slsh.append([t1, i.formula_ceshixiangmu, float(i.decimal_ceshijieguo)])
        if t1 not in t_list:
            t_list.append(t1)
    t_list.sort(reverse=True)
    t_list = t_list[:6]
    slsh_t = []
    for i in t_list:
        ts1 = str(i)
        ts2 = ts1[:4] + '-' + ts1[4:6] + '-' + ts1[6:8]
        slsh_t.append(ts2)
    r1_slsh = []
    for i in result_slsh:
        if i[0] in t_list:
            r1_slsh.append(i)
    # r1_slsh.sort(key=lambda x:x[0], reverse=True)
    csjg_slsh = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    bxb = []
    pzc = []
    gt = []
    hxb = []
    jsjm = []
    xns = []
    xqyj = []
    xhdb = []
    for i in r1_slsh:
        if i[1] == '白细胞':
            bxb.append(i)
        elif i[1] == '皮质醇':
            pzc.append(i)
        elif i[1] == '睾酮':
            gt.append(i)
        elif i[1] == '红细胞':
            hxb.append(i)
        elif i[1] == '肌酸激酶':
            jsjm.append(i)
        elif i[1] == '血尿素':
            xns.append(i)
        elif i[1] == '血球压积':
            xqyj.append(i)
        elif i[1] == '血红蛋白':
            xhdb.append(i)
    slsh_all = [bxb, pzc, gt, hxb, jsjm, xns, xqyj, xhdb]
    for o in slsh_all:
        m = slsh_all.index(o)
        for i in o:
            for t in t_list:
                n = t_list.index(t)
                if i[0] == t:
                    csjg_slsh[m][n] = i[2]
    jc_times = []
    zx_times = []
    fms_times = []
    xxl_times = []
    for jc in times_jctn:
        tt1 = str(jc)
        tt2 = tt1[:4] + '-' + tt1[4:6] + '-' + tt1[6:8]
        jc_times.append(tt2)
    for zx in times_zxtn:
        tt1 = str(zx)
        tt2 = tt1[:4] + '-' + tt1[4:6] + '-' + tt1[6:8]
        zx_times.append(tt2)
    for ft in times_fms:
        tt1 = str(ft)
        tt2 = tt1[:4] + '-' + tt1[4:6] + '-' + tt1[6:8]
        fms_times.append(tt2)
    for xt in key_list:
        tt1 = str(xt)
        tt2 = datetime.date(int(tt1[:4]), int(tt1[4:6]), int(tt1[6:8])).isocalendar()
        tt3 = str(tt2[0]) + '年' + str(tt2[1]) + '周'
        xxl_times.append(tt3)
    while len(jc_times) < 6:
        jc_times.append(['-'])
    while len(zx_times) < 6:
        zx_times.append(['-'])
    while len(fms_times) < 6:
        fms_times.append(['-'])
    while len(xxl_times) < 6:
        xxl_times.append(['-'])
    while len(slsh_t) < 6:
        slsh_t.append(['-'])

    res_shenglvdanda = ShenglvDanda.objects.filter(form_yundongyuan_single_line_zhongwenming=player)
    res_shenglvzuhe = ShenglvZuhe.objects.filter(form_shuangdazuhe_zhongguo_single_line1__contains=player)
    wgqy = []
    shenglv = []
    for i in res_shenglvdanda:
        ds = i.form_yundongyuan_8_single_line_zhongwenming
        sl = i.percent_shenglv
        wgqy.append({'name': ds, 'max': 100})
        shenglv.append(sl)
    for i in res_shenglvzuhe:
        ds = i.form_shuangdazuhe_8_single_line1
        sl = i.percent_shenglv
        wgqy.append({'name': ds, 'max': 100})
        shenglv.append(sl)

    res_shipin = FormShipinReport.objects.filter(single_line_shipinmingcheng__contains=player)
    shipin_list = []
    for i in res_shipin:
        spmc = '-'.join(i.single_line_shipinmingcheng.split('-')[6:])
        ss = i.query_saishimingcheng
        lunci = i.dropdown_lunci
        zbf = i.dropdown_bisaijieguo
        mjbf = i.single_line_bifen
        shipin = [spmc, ss, lunci, zbf, mjbf]
        shipin_list.append(shipin)

    data['xinxi'] = xinxi
    data['jctn_time'] = jc_times
    data['jctn'] = pinfen_jctn
    data['zxtn_time'] = zx_times
    data['zxtn'] = pinfen_zxtn
    data['fms_time'] = fms_times
    data['fms'] = pinfen_fms
    data['xxl_time'] = xxl_times
    data['xxl'] = shichang_xxl
    data['slsh_time'] = slsh_t
    data['slsh'] = csjg_slsh
    data['wgqy'] = wgqy
    data['shenglv'] = shenglv
    data['shipin'] = shipin_list
    # response = HttpResponse(json.dumps(data))
    response = HttpResponse(json.dumps(data))
    return response


def search(request):
    if request.method == 'POST':
        a = request.POST.get('data')
        data = {'data': 1}
        response = HttpResponse(json.dumps(data))
        # response["Access-Control-Allow-Origin"] = "*"
        # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        # response["Access-Control-Max-Age"] = "1000"
        # response["Access-Control-Allow-Headers"] = " * "
        return response


def login(request):
    if request.method == 'POST':
        name = request.POST.get('user')
        pwd = request.POST.get('pwd')
        # result = User.objects.filter(username=name)[0]
        if '111' == pwd:
            data = {'data': name}
        else:
            data = {'data': ''}
        # if name == 'my':
        # request.session['name'] = name
        # response = HttpResponse('set cookie')

        # data = {'data': name}
        response = HttpResponse(json.dumps(data))

        # response.set_cookie("name", 'my')
        # response["Access-Control-Allow-Origin"] = "null"
        # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        # response["Access-Control-Max-Age"] = "1000"
        # response["Access-Control-Allow-Headers"] = " * "
        return response






