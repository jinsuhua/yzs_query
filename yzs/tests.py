
from django.test import TestCase

import os,sys
import zipfile
import hashlib
import json

import logging
logger = logging.getLogger(__name__)
print(__name__)
print(logger)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yzs.settings.dev")  # project_name 项目名称
import django
django.setup()


from tables.models import *




# ftp目录
DIR_ROOT = "d:/tmp/test/20201217"
# 解压目录
DIR_UNZIP = "D:/tmp/test/unzip/20201217"

#表操作标识
TAB_DELETE = "delete"
TAB_UPDATE = "update"
TAB_HEARTBEAT = "heartbeat"

# 表字段
TAB_COLUMNS = "columns.json"
# 建表语句
TAB_CREATE = "create.sql"
# 表样例数据
TAB_SAMPLE = "sample.json"
# 表注释
TAB_COMMENT = "remark.txt"

def main():

    # 遍历原始目录
    #os.chdir(rootdir)
    print("开始遍历ftp目录: {0}".format(DIR_ROOT))
    for file in os.listdir(DIR_ROOT):
        filepath = os.path.join(DIR_ROOT, file)
        print(file)
        if file.endswith("md5"):
            if checkMd5(filepath):
                # unzip 文件 到解压目录
                unzip_file(filepath[0:len(filepath) - 4], DIR_UNZIP)
            else:
                print("md5校验不通过---{0}".format(file))


    # 遍历解压目录， 解析库信息
    print("开始遍历解压目录: {0}".format(DIR_UNZIP))
    #os.chdir(unzipdir)
    for oneip in os.listdir(DIR_UNZIP):

        oneipdir = os.path.join(DIR_UNZIP, oneip)
        if(os.path.isdir(oneipdir)):
            for dbinfo in os.listdir(oneipdir):
                dbinfodir = os.path.join(oneipdir, dbinfo)
                print("库目录: {0}".format(dbinfodir))
                ip, port, catlog, schema = dbinfo.split("^")
                print("ip={0}, port={1}, catlog={2}, schema={3}".format(ip, port, catlog, schema))

                dbFind = DBInfo.objects.filter(db_ip=ip, db_port=port, db_name=catlog, schema_name=schema)

                if not dbFind:
                    # TODO 不存在, 计入日志, 需手工录入的db
                    print("not exisits dbinfo 需手工录入: {0}".format(dbinfo))
                    continue

                # db下的表信息
                tables = []
                if (os.path.isdir(dbinfodir)):
                    for tab in os.listdir(dbinfodir):
                        tabdir = os.path.join(dbinfodir, tab)
                        if os.path.isdir(tabdir):
                            # heartbeat 不用更新任何表的信息
                            if not os.path.exists(os.path.join(tabdir, TAB_HEARTBEAT)):
                                tables.append(tab)

                # 需要处理的表
                if len(tables) > 0:
                    parseTable(dbFind.first(), dbinfodir, tables)



def parseTable(db, dbinfodir, tables):
    """
    解析同一个db下的表文件
    :param db: db 对象
    :param dbinfodir: db基础路径
    :param tables: 需要处理的表（除heartbeat）
    :return:
    """
    # print("基础路径：{0}".format(dbinfodir))
    # print("开始处理表: \r\n{0}".format("\r\n".join(tables)))

    # 在数据库中某个db库下所有表
    qs = TabInfo.objects.filter(hdb__id = db.id)

    tabDic = {}
    for q in qs:
        tabDic[q.table_name] = q


    for tab in tables:
        print("开始处理表: {0}".format(tab))

        # 表不存在
        if not tabDic.get(tab):
            # 新表
            t = TabInfo()
            t.table_name= tab
            t.hdb = db
            t.save()
            tabDic[tab] = t

        # 待处理的table信息
        tabId = tabDic[tab].id
        tabdir = os.path.join(dbinfodir, tab)

        # 删除
        if os.path.exists(os.path.join(tabdir, TAB_DELETE)):
            print("------删除表------")
            TabInfo.objects.filter(id=tabId).delete()

        # 新增或者变更
        if os.path.exists(os.path.join(tabdir, TAB_UPDATE)):
            coldir = os.path.join(tabdir, TAB_COLUMNS)
            ddldir = os.path.join(tabdir, TAB_CREATE)
            sampdir = os.path.join(tabdir, TAB_SAMPLE)
            commentdir = os.path.join(tabdir, TAB_COMMENT)
            # 表注释
            if os.path.exists(commentdir):
                print("------更新表注释------")
                handleComment(tabDic[tab], commentdir)
            # 字段更新
            if os.path.exists(coldir):
                print("------更新表字段------")
                handleColumns(db, tabDic[tab], coldir)
            # ddl 建表语句处理
            if os.path.exists(ddldir):
                print("------更新建表语句------")
                handleDDL(db, tabDic[tab], ddldir)
            # 表样例数据更新
            if os.path.exists(sampdir):
                print("------更新表样例数据------")
                handleSamp(db, tabDic[tab], sampdir)



def handleComment(table, commentdir):
    """
    更新表注释
    :param table:
    :param commentdir:
    :return:
    """
    with open(commentdir, encoding='utf-8') as f:
        cmt = f.read()
    if cmt and len(cmt) > 0:
        t = table
        t.table_comment = cmt
        t.save()


def handleColumns(db, table, coldir):
    """
    更新表结构
    :param table:
    :param coldir:
    :return:
    """
    TabMeta.objects.filter(htab__id=table.id).delete()
    # 读取json文件：
    with open(coldir, encoding='utf-8') as f:
        fdata = f.read()

    # json文件解析出来的表字段
    collist = json.loads(fdata)
    # 需要插入的表字段list
    tmlist = []

    if len(collist) > 0:
        for col in collist:
            col_name = col.get("columnName")
            col_type = col.get("columnType")
            col_comment = col.get("columnRemark")
            is_null = "1" if col.get("nullable") == True else "0"
            default_val = col.get("defaultValue")
            tm = TabMeta()
            tm.hdb = db
            tm.htab = table

            tm.col_name = col_name
            tm.col_type = col_type
            tm.col_comment = col_comment
            tm.is_null = is_null
            tm.default_val = default_val
            tmlist.append(tm)

    if len(tmlist) > 0:
        TabMeta.objects.bulk_create(tmlist)


def handleDDL(db, table, ddldir):
    """
    建表语句更新
    :param table:
    :param tabledir:
    :return:
    """
    tddl_qs = TabDDL.objects.filter(htab__id=table.id)
    if not tddl_qs:
        # ddl语句不存在
        tddl = TabDDL()
        tddl.hdb = db
        tddl.htab = table
    else:
        # ddl语句已存在
        tddl = tddl_qs.first()

    # 更新建表语句：
    with open(ddldir, encoding='utf-8') as f:
        ddlsql = f.read()

    tddl.ddl_stmt = ddlsql
    tddl.save()


def handleSamp(db, table, sampdir):
    """
    表样例更新数据
    :param table:
    :param sampdir:
    :return:
    """
    tsamp_qs = TabSamp.objects.filter(htab__id=table.id)
    if not tsamp_qs:
        # ddl语句不存在
        tsamp = TabSamp()
        tsamp.hdb = db
        tsamp.htab = table
    else:
        # ddl语句已存在
        tsamp = tsamp_qs.first()

    # 更新建表语句：
    with open(sampdir, encoding='utf-8') as f:
        sampdata = f.read()

    tsamp.row_content = sampdata
    tsamp.save()






def unzip_file(fz_name, path):
    """
    解压缩文件
    :param fz_name: zip文件
    :param path: 解压缩路径
    :return:
    """
    flag = False

    if zipfile.is_zipfile(fz_name):  # 检查是否为zip文件
        with zipfile.ZipFile(fz_name, 'r') as zipf:
            zipf.extractall(path)
            # for p in zipf.namelist():
            #     # 使用cp437对文件名进行解码还原， win下一般使用的是gbk编码
            #     p = p.encode('cp437').decode('gbk')  # 解决中文乱码
            #     print(fz_name, p,path)
            flag = True

    return {'file_name': fz_name, 'flag': flag}



def checkMd5(md5File):
    """
    校验md5是否相等
    :param md5File: md5文件绝对路径
    :return:
    """
    for line in open(md5File):
        md51 = line
    zipFile = md5File[0:len(md5File) - 4]
    md52 = md5sum(zipFile)
    if md51 == md52:
        return True
    return False


def md5sum(filename):
    """
    md5sum filename
    :param filename: 文件的绝对路径
    :return:
    """
    file_object = open(filename, 'rb')
    file_content = file_object.read()
    file_object.close()
    file_md5 = hashlib.md5(file_content)
    return file_md5.hexdigest()




if __name__ == '__main__':
    main()
