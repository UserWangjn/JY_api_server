# Compiled at: 2019-06-21 03:22:47
from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, json
from io import StringIO
from io import BytesIO
from flask import make_response
import urllib.request, urllib.error, urllib.parse, re, chardet, time, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime, shutil

def yunxing_tongji(func):

    def yunxing_tongji():
        func()
        if 'ci_seven_data' in list(current_app.config.keys()):
            time_pic = int(current_app.config.get('ci_seven_data')['time'])
            timeArray = time.strftime('%Y--%m--%d', time.localtime(time_pic))
            otherStyleTime = time.strftime('%Y--%m--%d', time.localtime(time.time()))
            if timeArray != otherStyleTime:
                current_app.config.pop('ci_seven_data')
        if 'ci_today_data' in list(current_app.config.keys()):
            time_pic = int(current_app.config.get('ci_today_data')['time'])
            timeArray = time.strftime('%Y--%m--%d', time.localtime(time_pic))
            otherStyleTime = time.strftime('%Y--%m--%d', time.localtime(time.time()))
            if timeArray != otherStyleTime:
                current_app.config.pop('ci_today_data')
        if 'ci_seven_data' in list(current_app.config.keys()) and request.form['type'] == 'yewu_seven':
            if current_app.config['ci_seven_data']['all_num'] == 0:
                tongguolv = 0
            else:
                tongguolv = int(float(current_app.config['ci_seven_data']['all_pass']) / float(current_app.config['ci_seven_data']['all_num']) * 100)
            return jsonify(detail=json.dumps(current_app.config['ci_seven_data']['all_git_detail']), tongguolv=tongguolv)
        if 'ci_today_data' in list(current_app.config.keys()) and request.form['type'] == 'yewu_today':
            if current_app.config['ci_today_data']['all_num'] == 0:
                tongguolv = 0
            else:
                tongguolv = int(float(current_app.config['ci_today_data']['all_pass']) / float(current_app.config['ci_today_data']['all_num']) * 100)
            return jsonify(detail=json.dumps(current_app.config['ci_today_data']['all_git_detail']), tongguolv=tongguolv)
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu_jiekou = db_jeikou.cursor()
        git_detail = cu_jiekou.execute('select name,branch from git_detail').fetchall()
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        seven_day = int(time.mktime(time.strptime(today, '%Y-%m-%d'))) - 604800
        seven_day = time.strftime('%Y-%m-%d', time.localtime(seven_day))
        all_git_detail = []
        all_fail = 0
        all_pass = 0
        for k, i in git_detail:
            if request.form['type'] == 'yewu_seven':
                seven_detail = cu.execute('select * from ci_tongji where git_url=? and branch=? and time>?', (k, i, seven_day)).fetchall()
                this_git_detail_seven = {'name': k, 'branch': i, 'cishu_num': len(seven_detail), 'jiekou_num': 0, 'pass_num': 0, 
                   'fail_num': 0}
                max_pass = 0
                for z in seven_detail:
                    this_git_detail_seven['jiekou_num'] += int(z[4])
                    try:
                        this_git_detail_seven['pass_num'] += int(z[6])
                    except:
                        pass

                    this_git_detail_seven['fail_num'] += int(z[5])
                    max_pass = max([max_pass, float(int(z[6])) / float(int(z[6]) + int(z[5]))])

                if int(max_pass) == 1:
                    this_git_detail_seven['max_pass'] = '100%'
                else:
                    this_git_detail_seven['max_pass'] = str(int(max_pass * 100)) + '%'
                all_git_detail.append(this_git_detail_seven)
                all_fail += this_git_detail_seven['fail_num']
                all_pass += this_git_detail_seven['pass_num']
                all_num = all_fail + all_pass
                current_app.config['ci_seven_data'] = {'all_git_detail': all_git_detail, 'all_fail': all_fail, 
                   'all_pass': all_pass, 
                   'all_num': all_num, 'time': time.time()}
            elif request.form['type'] == 'yewu_today':
                today_detail = cu.execute('select * from ci_tongji where git_url=? and branch=? and time>=?', (
                 k, i, today)).fetchall()
                this_git_detail_today = {'name': k, 'branch': i, 'cishu_num': len(today_detail), 'jiekou_num': 0, 
                   'pass_num': 0, 
                   'fail_num': 0}
                max_pass = 0
                for z in today_detail:
                    this_git_detail_today['jiekou_num'] += int(z[4])
                    try:
                        this_git_detail_today['pass_num'] += int(z[6])
                    except:
                        pass

                    this_git_detail_today['fail_num'] += int(z[5])
                    max_pass = max([max_pass, float(int(z[6])) / float(int(z[6]) + int(z[5]))])

                if int(max_pass) == 1:
                    this_git_detail_today['max_pass'] = '100%'
                else:
                    this_git_detail_today['max_pass'] = str(int(max_pass * 100)) + '%'
                all_git_detail.append(this_git_detail_today)
                all_fail += this_git_detail_today['fail_num']
                all_pass += this_git_detail_today['pass_num']
                all_num = all_fail + all_pass
                current_app.config['ci_today_data'] = {'all_git_detail': all_git_detail, 'all_fail': all_fail, 'all_pass': all_pass, 
                   'all_num': all_num, 'time': time.time()}

        db.close()
        db_jeikou.close()
        if float(all_num) == 0:
            tongguolv = 0
        else:
            tongguolv = int(float(all_pass) / float(all_num) * 100)
        return jsonify(detail=json.dumps(all_git_detail), tongguolv=tongguolv)

    return yunxing_tongji


def test_image(func):

    def test_image(id):
        func(id)
        if 'seven_ci_pic' in list(current_app.config.keys()):
            time_pic = int(os.path.basename(current_app.config.get('seven_ci_pic')).split('ci_seven')[0])
        if 'seven_ci_pic' in list(current_app.config.keys()):
            time_pic = int(os.path.basename(current_app.config.get('seven_ci_pic')).split('ci_seven')[0])
            timeArray = time.strftime('%Y--%m--%d', time.localtime(time_pic))
            otherStyleTime = time.strftime('%Y--%m--%d', time.localtime(time.time()))
            if timeArray != otherStyleTime:
                current_app.config.pop('seven_ci_pic')
        if 'seven_ci_pic' not in list(current_app.config.keys()) and 'yewu_seven' in id:
            plt.figure(1, figsize=(9, 4))
            plt.rcParams['savefig.dpi'] = 500
            plt.rcParams['figure.dpi'] = 500
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
            cu_jiekou = db_jeikou.cursor()
            git_detail = cu_jiekou.execute('select name,branch from git_detail').fetchall()
            otherStyleTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            seven_day = int(time.mktime(time.strptime(otherStyleTime, '%Y-%m-%d'))) - 604800
            seven_day = time.strftime('%Y-%m-%d', time(seven_day))
            fail_list = []
            pass_list = []
            tongguolv_list = []
            beizhu_list = []
            all_zero = True
            for k, i in git_detail:
                all_fail = 0
                all_pass = 0
                all_jiekou = 0
                seven_detail = cu.execute('select * from ci_tongji where git_url=? and branch=? and time>?', (k, i, seven_day)).fetchall()
                if len(seven_detail) != 0:
                    all_zero = False
                beizhu = cu_jiekou.execute('select beizhu from  git_detail  where name=? and branch=?', (k, i)).fetchall()[0][0]
                for z in seven_detail:
                    all_jiekou += int(z[4])
                    all_pass += int(z[6])
                    all_fail += int(z[5])

                fail_list.append(all_fail)
                if float(all_pass) + float(all_fail) == 0:
                    tongguolv_list.append(0)
                else:
                    tongguolv_list.append(float(all_pass) / (float(all_pass) + float(all_fail)))
                beizhu_list.append(beizhu)
                pass_list.append(all_pass)

            tongguolv_list = [ str(int(i * 100)) + '%' for i in tongguolv_list ]
            db.close()
            db_jeikou.close()
            plt.xticks(fontsize=13)
            plt.yticks(fontsize=14)
            img = BytesIO()
            k = plt.bar(list(range(len(fail_list))), fail_list, label='fail', fc='r')
            d = plt.bar(list(range(len(fail_list))), pass_list, bottom=fail_list, label='pass', tick_label=beizhu_list, fc='y')
            for rect, a, baifenbi in zip(k, d, tongguolv_list):
                height = rect.get_height() + a.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2, height, baifenbi, ha='center', va='bottom')

            plt.legend(fontsize=14)
            pic_name = str(time.time()) + 'ci_seven.png'
            pic_path = os.path.join(current_app.config.get('LOG_FILE'), pic_name)
            plt.savefig(os.path.join(current_app.config.get('BASEDIR'), pic_name), bbox_inches='tight')
            plt.clf()
            all_path = os.path.join(current_app.config.get('BASEDIR'))
            for i in os.listdir(all_path):
                if i != pic_name and 'ci_seven' in i:
                    try:
                        os.remove(os.path.join(all_path, i))
                    except:
                        pass

            current_app.config['seven_ci_pic'] = pic_path
        return jsonify(pic_path=current_app.config['seven_ci_pic'])

    return test_image


def pic_yewu_today(func):

    def pic_yewu_today(testid):
        func(testid)
        if 'today_ci_pic' in list(current_app.config.keys()):
            time_pic = int(os.path.basename(current_app.config.get('today_ci_pic')).split('ci_today')[0])
            timeArray = time.strftime('%Y--%m--%d', time.localtime(time_pic))
            otherStyleTime = time.strftime('%Y--%m--%d', time.localtime(time.time()))
            if timeArray != otherStyleTime:
                current_app.config.pop('today_ci_pic')
        if 'today_ci_pic' not in list(current_app.config.keys()) and 'yewu_today' in testid:
            plt.figure(1, figsize=(9, 4))
            if 'statu' in list(request.form.keys()):
                plt.rcParams['savefig.dpi'] = 300
                plt.rcParams['figure.dpi'] = 300
            else:
                plt.rcParams['savefig.dpi'] = 500
                plt.rcParams['figure.dpi'] = 500
            plt.rcParams['font.sans-serif'] = [
             'SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
            cu_jiekou = db_jeikou.cursor()
            git_detail = cu_jiekou.execute('select name,branch from git_detail').fetchall()
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            fail_list = []
            pass_list = []
            tongguolv_list = []
            beizhu_list = []
            all_zero = True
            for k, i in git_detail:
                all_fail = 0
                all_pass = 0
                all_jiekou = 0
                today_detail = cu.execute('select * from ci_tongji where git_url=? and branch=? and time>=?', (
                 k, i, today)).fetchall()
                if len(today_detail) != 0:
                    all_zero = False
                beizhu = cu_jiekou.execute('select beizhu from  git_detail  where name=? and branch=?', (k, i)).fetchall()[0][0]
                for z in today_detail:
                    all_jiekou += int(z[4])
                    all_pass += int(z[6])
                    all_fail += int(z[5])

                fail_list.append(all_fail)
                if float(all_pass) + float(all_fail) == 0:
                    tongguolv_list.append(0)
                else:
                    tongguolv_list.append(float(all_pass) / (float(all_pass) + float(all_fail)))
                beizhu_list.append(beizhu)
                pass_list.append(all_pass)

            if all_zero:
                return jsonify(statu='all_zero')
            tongguolv_list = [ str(int(i * 100)) + '%' for i in tongguolv_list ]
            db.close()
            db_jeikou.close()
            plt.xticks(fontsize=13)
            plt.yticks(fontsize=14)
            img = BytesIO()
            len_max = max([max(fail_list), max(pass_list)])
            k = plt.bar(list(range(len(fail_list))), fail_list, label='fail', fc='r')
            d = plt.bar(list(range(len(fail_list))), pass_list, bottom=fail_list, label='pass', tick_label=beizhu_list, fc='y')
            for rect, a, baifenbi in zip(k, d, tongguolv_list):
                height = rect.get_height() + a.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2, height, baifenbi, ha='center', va='bottom')

            plt.legend(fontsize=14)
            pic_name = str(time.time()) + 'ci_today.png'
            pic_path = os.path.join(current_app.config.get('LOG_FILE'), pic_name)
            plt.savefig(os.path.join(current_app.config.get('BASEDIR'), pic_name), bbox_inches='tight')
            plt.clf()
            all_path = os.path.join(current_app.config.get('BASEDIR'))
            for i in os.listdir(all_path):
                if i != pic_name and 'ci_today' in i:
                    try:
                        os.remove(os.path.join(all_path, i))
                    except:
                        pass

            current_app.config['today_ci_pic'] = pic_path
            plt.clf()
        return jsonify(pic_path=current_app.config['today_ci_pic'])

    return pic_yewu_today


def local_tongji_seven(func):

    def local_tongji_seven():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        otherStyleTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        seven_day = int(time.mktime(time.strptime(otherStyleTime, '%Y-%m-%d'))) - 604800
        seven_day = time.strftime('%Y-%m-%d', time.localtime(seven_day))
        local_detail = cu.execute('select user_team,count(distinct(name)),sum(pass_jiekou ),sum(fail_jiekou),sum(fail_case_num),sum(pass_case_num) from  local_tongji where time>=? group by user_team', (seven_day,)).fetchall()
        return jsonify(local_detail=json.dumps(local_detail))

    return local_tongji_seven


def local_seven_pic(func):

    def local_seven_pic(testid):
        func(testid)
        if 'local_seven_pic' in list(current_app.config.keys()):
            time_pic = float(os.path.basename(current_app.config.get('local_seven_pic')).split('local_seven')[0])
            timeArray = time.strftime('%Y--%m--%d', time.localtime(time_pic))
            otherStyleTime = time.strftime('%Y--%m--%d', time.localtime(time.time()))
            if timeArray != otherStyleTime:
                current_app.config.pop('local_seven_pic')
        if 'local_seven_pic' not in list(current_app.config.keys()):
            plt.rcParams['savefig.dpi'] = 150
            plt.rcParams['figure.dpi'] = 100
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
            cu_jiekou = db_jeikou.cursor()
            otherStyleTime = time.strftime('%Y-%m-%d', time.localtime(time.time() - 604800))
            local_detail = cu.execute('select user_team,count(name),sum(num ),sum(fail_jiekou),sum(fail_case_num),sum(pass_case_num) from  local_tongji where time>=? group by user_team', (
             otherStyleTime,)).fetchall()
            local_detail = [ list(i) for i in local_detail ]
            for i in local_detail:
                if i[0] == '\u65e0\u5206\u7ec4':
                    i[0] = '\u5176\u4ed6'

            db_jeikou.close()
            plt.xticks(fontsize=13)
            plt.yticks(fontsize=14)
            img = BytesIO()
            labels = [ i[0] for i in local_detail ]
            db.close()
            local_num_detail = dict(list(zip([ i[0] for i in local_detail ], [ int(i[2]) for i in local_detail ])))
            fracs = []
            for i in labels:
                if i in list(local_num_detail.keys()):
                    fracs.append(local_num_detail[i])
                else:
                    fracs.append(0)

            explode = []
            for i in fracs:
                if i == 0:
                    explode.append(0)
                else:
                    explode.append(0.1)

            plt.axes(aspect=1)
            plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%', shadow=False, labeldistance=1.1, startangle=90, pctdistance=0.6)
            pic_name = str(time.time()) + 'local_seven.png'
            pic_path = os.path.join(current_app.config.get('LOG_FILE'), pic_name)
            plt.savefig(os.path.join(current_app.config.get('BASEDIR'), pic_name), bbox_inches='tight')
            plt.clf()
            all_path = os.path.join(current_app.config.get('BASEDIR'))
            for i in os.listdir(all_path):
                if i != pic_name and 'local_seven' in i:
                    try:
                        os.remove(os.path.join(all_path, i))
                    except:
                        pass

            current_app.config['local_seven_pic'] = pic_path
        else:
            if 'local_seven_pic' in list(current_app.config.keys()) and 'local_seven_pic' in testid:
                pass
        return jsonify(pic_path=current_app.config.get('local_seven_pic'))

    return local_seven_pic


def local_tongji_today(func):

    def local_tongji_today():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        local_detail = cu.execute('select user_team,count(distinct(name)),sum(pass_jiekou ),sum(fail_jiekou),sum(fail_case_num),sum(pass_case_num) from  local_tongji where time>=? group by user_team', (today,)).fetchall()
        return jsonify(local_detail=json.dumps(local_detail))

    return local_tongji_today


def local_today_pic(func):

    def local_today_pic(testid):
        func(testid)
        if 'local_today_pic' in list(current_app.config.keys()):
            time_pic = int(os.path.basename(current_app.config.get('local_today_pic')).split('local_today')[0])
            timeArray = time.strftime('%Y--%m--%d', time.localtime(time_pic))
            otherStyleTime = time.strftime('%Y--%m--%d', time.localtime(time.time()))
            if timeArray != otherStyleTime:
                current_app.config.pop('local_today_pic')
        if 'local_today_pic' not in list(current_app.config.keys()):
            plt.rcParams['savefig.dpi'] = 150
            plt.rcParams['figure.dpi'] = 200
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
            cu_jiekou = db_jeikou.cursor()
            today_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            local_detail = cu.execute('select user_team,count(name),sum(pass_jiekou ),sum(fail_jiekou),sum(fail_case_num),sum(pass_case_num) from  local_tongji where time>=? group by user_team', (
             today_day,)).fetchall()
            if len(local_detail) == 0:
                return jsonify(statu='all_zero')
            local_detail = [ list(i) for i in local_detail ]
            for i in local_detail:
                if i[0] == '\u65e0\u5206\u7ec4':
                    i[0] = '\u5176\u4ed6'

            db_jeikou.close()
            plt.xticks(fontsize=13)
            plt.yticks(fontsize=14)
            img = BytesIO()
            labels = [ i[0] for i in local_detail ]
            db.close()
            local_num_detail = dict(list(zip([ i[0] for i in local_detail ], [ int(i[2]) for i in local_detail ])))
            fracs = []
            for i in labels:
                if i in list(local_num_detail.keys()):
                    fracs.append(local_num_detail[i])
                else:
                    fracs.append(0)

            explode = []
            for i in fracs:
                if i == 0:
                    explode.append(0)
                else:
                    explode.append(0.1)

            plt.axes(aspect=1)
            plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%', shadow=False, labeldistance=1.1, startangle=90, pctdistance=0.6)
            pic_name = str(time.time()) + 'local_today.png'
            pic_path = os.path.join(current_app.config.get('LOG_FILE'), pic_name)
            plt.savefig(os.path.join(current_app.config.get('BASEDIR'), pic_name), bbox_inches='tight')
            plt.clf()
            all_path = os.path.join(current_app.config.get('BASEDIR'))
            for i in os.listdir(all_path):
                if i != pic_name and 'local_today' in i:
                    try:
                        os.remove(os.path.join(all_path, i))
                    except:
                        pass

            current_app.config['local_today_pic'] = pic_path
        else:
            if 'local_today_pic' in list(current_app.config.keys()) and 'local_today_pic' in testid:
                response = current_app.config['local_today_pic']
        return jsonify(pic_path=current_app.config.get('local_today_pic'))

    return local_today_pic


def pic_yewu_email(testid):
    plt.figure(1, figsize=(9, 4))
    plt.rcParams['savefig.dpi'] = 120
    plt.rcParams['figure.dpi'] = 120
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    while True:
        if 'take_result' in list(session.keys()):
            run_detail = session['take_result']
            break
        else:
            time.sleep(1)

    git_detail = list(run_detail.keys())
    pass_list = [ run_detail[i]['success'] for i in git_detail ]
    fail_list = [ run_detail[i]['fail'] for i in git_detail ]
    count = [ run_detail[i]['count'] for i in git_detail ]
    tongguolv_list = [ float(pass_list[k]) / count[k] for k, i in enumerate(pass_list) ]
    tongguolv_list = [ str(int(i * 100)) + '%' for i in tongguolv_list ]
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=14)
    img = BytesIO()
    if len(fail_list) < 3:
        for i in range(3 - len(fail_list)):
            fail_list.append(0)
            pass_list.append(0)
            git_detail.append('')

    if len(fail_list) >= 3:
        width = 0.5
    else:
        if len(fail_list) == 2:
            width = 0.9
        else:
            if en(fail_list) == 1:
                width = 0.9
    len_max = max([max(fail_list), max(pass_list)])
    plt.ylabel('case\u6570')
    k = plt.bar(list(range(len(fail_list))), fail_list, label='fail', fc='r', width=0.2)
    d = plt.bar(list(range(len(fail_list))), pass_list, bottom=fail_list, label='pass', tick_label=git_detail, fc='#66CC66', width=0.2)
    for rect, a, baifenbi in zip(k, d, tongguolv_list):
        height = rect.get_height() + a.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, baifenbi, ha='center', va='bottom')

    for a, b, c in zip(list(range(len(fail_list))), pass_list, fail_list):
        if b == 0 and c == 0:
            continue
        if a < 5:
            plt.text(a + 0.16, c, 'F:' + str(c), ha='center', va='bottom', fontsize=10)
            plt.text(a + 0.16, b + c, 'P:' + str(b), ha='center', va='bottom', fontsize=10)
        else:
            if b < 2:
                len_num = 3
            else:
                len_num = 1
            if b + c - 8 - c < 3:
                len_num = b + c - 10
            plt.text(a + 0.16, c - len_num, 'F:' + str(c), ha='center', va='bottom', fontsize=10)
            plt.text(a + 0.16, b + c - 8, 'P:' + str(b), ha='center', va='bottom', fontsize=10)

    plt.legend(fontsize=14)
    plt.savefig(os.path.join(current_app.config.get('RESULT_PICT_SAVE'), str(testid) + '.png'), bbox_inches='tight')
    plt.savefig(img, bbox_inches='tight', format='png')
    img.seek(0)
    response = make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/png'
    img.truncate()
    img.close()
    plt.clf()


def tongji_mail(func):

    def tongji_mail():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu_jiekou = db_jeikou.cursor()
        git_detail = [ list(i) for i in cu_jiekou.execute('select * from git_detail  ').fetchall() ]
        team_detail = [ i[0] for i in cu.execute('select team from team').fetchall() if i[0].strip() != '' ]
        team_detail.append('\u65e0\u5206\u7ec4')
        team_tongji = {}
        for i in team_detail:
            team_tongji[i] = {'num_user': [], 'all_jiekou': 0, 'all_case': 0, 'pass_case': 0, 'num': 0}

        db.close()
        db_jeikou.close()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        seven_day = int(time.mktime(time.strptime(today, '%Y-%m-%d'))) - 604800
        seven_day = time.strftime('%Y-%m-%d', time.localtime(seven_day))
        git_detail = cu.execute('select * from local_tongji  where time>"%s"' % seven_day).fetchall()
        print(99999999999999999999999999999999999999999999999)
        print(seven_day)
        all_ci_num = 0
        for i in git_detail:
            try:
                i[1].strip() not in team_tongji[i[7]]['num_user']
            except:
                pass

            if i[1].strip() not in team_tongji[i[7]]['num_user']:
                team_tongji[i[7]]['num_user'].append(i[1])
            team_tongji[i[7]]['all_jiekou'] = team_tongji[i[7]]['all_jiekou'] + int(i[3]) + int(i[4])
            team_tongji[i[7]]['all_case'] = team_tongji[i[7]]['all_case'] + int(i[5]) + int(i[6])
            team_tongji[i[7]]['pass_case'] = team_tongji[i[7]]['pass_case'] + int(i[6])
            team_tongji[i[7]]['num'] = team_tongji[i[7]]['num'] + int(i[8])
            all_ci_num = all_ci_num + int(i[8])

        team_tongji['\u5176\u4ed6'] = team_tongji['\u65e0\u5206\u7ec4']
        team_tongji.pop('\u65e0\u5206\u7ec4')
        for i in team_tongji:
            if team_tongji[i]['num'] != 0:
                tongguolv = float(team_tongji[i]['num'] * 100) / all_ci_num
                if tongguolv < 1:
                    tongguolv = 1
                team_tongji[i]['num'] = str(tongguolv)[:4].split('.')[0]
            else:
                team_tongji[i]['num'] = '0'

        db.close()
        db_jeikou.close()
        for i in list(team_tongji.keys()):
            team_tongji[i]['num_user'] = len(team_tongji[i]['num_user'])

        if len(list(request.args.keys())) == 0:
            name = str(int(time.time()))
        else:
            name = request.args.get('name')
        pic_path = pic_local_eamil_simple(name)
        return render_template('/hualala/jiekou_test/tongji_email.html', team_detail=team_tongji)

    return tongji_mail


def pic_yewu_today_email(func):

    def pic_yewu_today_email():
        func()
        plt.figure(1, figsize=(3, 3))
        plt.rcParams['savefig.dpi'] = 300
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu_jiekou = db_jeikou.cursor()
        git_detail = cu_jiekou.execute('select name,branch from git_detail').fetchall()
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fail_list = []
        pass_list = []
        tongguolv_list = []
        beizhu_list = []
        all_zero = True
        for k, i in git_detail:
            all_fail = 0
            all_pass = 0
            all_jiekou = 0
            today_detail = cu.execute('select * from ci_tongji where git_url=? and branch=? and time>=?', (
             k, i, today)).fetchall()
            if len(today_detail) != 0:
                all_zero = False
            beizhu = cu_jiekou.execute('select beizhu from  git_detail  where name=? and branch=?', (
             k, i)).fetchall()[0][0]
            for z in today_detail:
                all_jiekou += int(z[4])
                all_pass += int(z[6])
                all_fail += int(z[5])

            fail_list.append(all_fail)
            if float(all_pass) + float(all_fail) == 0:
                tongguolv_list.append(0)
            else:
                tongguolv_list.append(float(all_pass) / (float(all_pass) + float(all_fail)))
            beizhu_list.append(beizhu)
            pass_list.append(all_pass)

        plt.title('ci\u672c\u65e5\u7edf\u8ba1\u67f1\u72b6\u56fe', loc='left')
        tongguolv_list = [ str(int(i * 100)) + '%' for i in tongguolv_list ]
        db.close()
        db_jeikou.close()
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=14)
        img = BytesIO()
        len_max = max([max(fail_list), max(pass_list)])
        k = plt.bar(list(range(len(fail_list))), fail_list, label='fail', fc='r')
        d = plt.bar(list(range(len(fail_list))), pass_list, bottom=fail_list, label='pass', tick_label=beizhu_list, fc='y')
        for rect, a, baifenbi in zip(k, d, tongguolv_list):
            height = rect.get_height() + a.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height, baifenbi, ha='center', va='bottom')

        plt.legend(fontsize=14)
        pic_name = str(time.time()) + 'ci_today_email.png'
        pic_path = os.path.join(current_app.config.get('LOG_FILE'), pic_name)
        plt.savefig(os.path.join(current_app.config.get('BASEDIR'), pic_name), bbox_inches='tight')
        all_path = os.path.join(current_app.config.get('BASEDIR'))
        for i in os.listdir(all_path):
            if i != pic_name and 'ci_today_email' in i:
                try:
                    os.remove(os.path.join(all_path, i))
                except:
                    pass

        all_path = os.path.join(current_app.config.get('BASEDIR'))
        plt.clf()
        plt.rcParams['savefig.dpi'] = 150
        plt.rcParams['figure.dpi'] = 200
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu_jiekou = db_jeikou.cursor()
        today_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        local_detail = cu.execute('select user_team,count(name),sum(pass_jiekou ),sum(fail_jiekou),sum(fail_case_num),sum(pass_case_num) from  local_tongji where time>=? group by user_team', (
         today_day,)).fetchall()
        local_detail = [ list(i) for i in local_detail ]
        for i in local_detail:
            if i[0] == '\u65e0\u5206\u7ec4':
                i[0] = '\u5176\u4ed6'

        db_jeikou.close()
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=14)
        img = BytesIO()
        labels = [ i[0] for i in local_detail ]
        db.close()
        local_num_detail = dict(list(zip([ i[0] for i in local_detail ], [ int(i[2]) for i in local_detail ])))
        fracs = []
        for i in labels:
            if i in list(local_num_detail.keys()):
                fracs.append(local_num_detail[i])
            else:
                fracs.append(0)

        explode = []
        for i in fracs:
            if i == 0:
                explode.append(0)
            else:
                explode.append(0.1)

        plt.axes(aspect=1)
        plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%', shadow=False, labeldistance=1.1, startangle=90, pctdistance=0.6)
        pic_name = str(time.time()) + 'local_today_email.png'
        pic_path_local = os.path.join(current_app.config.get('LOG_FILE'), pic_name)
        plt.savefig(os.path.join(current_app.config.get('BASEDIR'), pic_name), bbox_inches='tight')
        plt.clf()
        all_path = os.path.join(current_app.config.get('BASEDIR'))
        for i in os.listdir(all_path):
            if i != pic_name and 'local_today_email' in i:
                try:
                    os.remove(os.path.join(all_path, i))
                except:
                    pass

        all_path = os.path.join(current_app.config.get('BASEDIR'))
        return jsonify(pic_path=pic_path, pic_path_local=pic_path_local)

    return pic_yewu_today_email


def pic_local_eamil_simple(name):
    plt.figure(1, figsize=(3, 3))
    plt.rcParams['savefig.dpi'] = 150
    plt.rcParams['figure.dpi'] = 200
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
    cu_jiekou = db_jeikou.cursor()
    today_day = time.strftime('%Y-%m-%d', time.localtime(time.time() - 604800))
    local_detail = cu.execute('select user_team,count(name),sum(pass_jiekou ),sum(fail_jiekou),sum(fail_case_num),sum(pass_case_num) from  local_tongji where time>=? group by user_team', (
     today_day,)).fetchall()
    local_detail = [ list(i) for i in local_detail ]
    for i in local_detail:
        if i[0] == '\u65e0\u5206\u7ec4':
            i[0] = '\u5176\u4ed6'

    db_jeikou.close()
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=14)
    img = BytesIO()
    labels = [ i[0] for i in local_detail ]
    db.close()
    local_num_detail = dict(list(zip([ i[0] for i in local_detail ], [ int(i[2]) for i in local_detail ])))
    fracs = []
    for i in labels:
        if i in list(local_num_detail.keys()):
            fracs.append(local_num_detail[i])
        else:
            fracs.append(0)

    explode = []
    for i in fracs:
        if i == 0:
            explode.append(0)
        else:
            explode.append(0.1)

    plt.axes(aspect=1)
    plt.pie(x=fracs, labels=labels, explode=explode, shadow=False, labeldistance=1.1, startangle=90, pctdistance=0.6)
    pic_name = name + 'local_today_email.png'
    pic_path_local = os.path.join(current_app.config.get('LOG_FILE'), pic_name)
    plt.savefig(os.path.join(current_app.config.get('BASEDIR'), pic_name), bbox_inches='tight')
    plt.clf()
    all_path = os.path.join(current_app.config.get('BASEDIR'))
    for i in os.listdir(all_path):
        if i != pic_name and 'local_today_email' in i:
            try:
                os.remove(os.path.join(all_path, i))
            except:
                pass

    all_path = os.path.join(current_app.config.get('BASEDIR'))
    return pic_path_local