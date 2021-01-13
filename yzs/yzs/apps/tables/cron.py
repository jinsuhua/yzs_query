
import os,sys
import zipfile
import hashlib
import json
import logging
logger = logging.getLogger("django")

# 设置能找到model
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yzs.yzs.settings.dev")
import django
django.setup()

from tables.models import *
from config import *
from datetime import datetime
import copy




def main():

    # 遍历原始目录
    #os.chdir(rootdir)
    logger.info("开始遍历ftp目录: {0}".format(DIR_ROOT))
    for file in os.listdir(DIR_ROOT):
        filepath = os.path.join(DIR_ROOT, file)
        #print(file)
        if file.endswith("md5"):
            if checkMd5(filepath):
                # unzip 文件 到解压目录
                unzip_file(filepath[0:len(filepath) - 4], DIR_UNZIP)
            else:
                logger.error("md5校验不通过---{0}".format(file))


    # 遍历解压目录， 解析库信息
    logger.info("开始遍历解压目录: {0}".format(DIR_UNZIP))
    #os.chdir(unzipdir)
    for oneip in os.listdir(DIR_UNZIP):

        oneipdir = os.path.join(DIR_UNZIP, oneip)
        if(os.path.isdir(oneipdir)):
            for dbinfo in os.listdir(oneipdir):
                dbinfodir = os.path.join(oneipdir, dbinfo)
                logger.info("库目录: {0}".format(dbinfodir))
                ip, port, catlog, schema = dbinfo.split("^")
                logger.info("ip={0}, port={1}, catlog={2}, schema={3}".format(ip, port, catlog, schema))

                dbFind = DBInfo.objects.filter(db_ip=ip, db_port=port, db_name=catlog, schema_name=schema)

                if not dbFind:
                    # TODO 不存在, 计入日志, 需手工录入的db
                    logger.error("not exisits dbinfo 需手工录入: {0}".format(dbinfo))
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
                            else:
                                # 计入操作日志
                                opLog(dbinfo, tab, OP_TYPE_HEARTBEAT, datetime.now(), datetime.now())

                # 需要处理的表
                if len(tables) > 0:
                    parseTable(dbinfo, dbFind.first(), dbinfodir, tables)



def parseTable(dbinfo, db, dbinfodir, tables):
    """
    解析同一个db下的表文件
    :param dbinfo: db信息字符串
    :param db: db 对象
    :param dbinfodir: db基础路径
    :param tables: 需要处理的表（除heartbeat）
    :return:
    """
    # 在数据库中某个db库下所有表
    qs = TabInfo.objects.filter(hdb__id = db.id)

    tabDic = {}
    for q in qs:
        tabDic[q.table_name] = q

    for tab in tables:
        logger.info("开始处理表: {0}".format(tab))

        op_start_date = datetime.now()
        op_type = OP_TYPE_UPDATE

        # 表不存在
        if not tabDic.get(tab):
            # 新表
            t = TabInfo()
            t.table_name= tab
            t.hdb = db
            t.save()
            tabDic[tab] = t
            op_type = OP_TYPE_NEW


        # 待处理的table信息
        tabId = tabDic[tab].id
        tabdir = os.path.join(dbinfodir, tab)

        # 删除
        if os.path.exists(os.path.join(tabdir, TAB_DELETE)):
            op_type = OP_TYPE_DELETE
            logger.info("删除表【TableId:{}, optype:{}】".format(tabId, op_type))
            doDelete(tabId)


        # 新增或者变更
        elif os.path.exists(os.path.join(tabdir, TAB_UPDATE)):
            coldir = os.path.join(tabdir, TAB_COLUMNS)
            ddldir = os.path.join(tabdir, TAB_CREATE)
            sampdir = os.path.join(tabdir, TAB_SAMPLE)
            commentdir = os.path.join(tabdir, TAB_COMMENT)
            # 表注释
            if os.path.exists(commentdir):
                logger.info("TableId:{}, optype:{}".format(tabId, op_type))
                handleComment(tabDic[tab], commentdir)
            # 字段更新
            if os.path.exists(coldir):
                logger.info("表字段【TableId:{}, optype:{}】".format(tabId, op_type))
                handleColumns(db, tabDic[tab], coldir)
            # ddl 建表语句处理
            if os.path.exists(ddldir):
                logger.info("建表语句【TableId:{}, optype:{}】".format(tabId, op_type))
                handleDDL(db, tabDic[tab], ddldir)
            # 表样例数据更新
            if os.path.exists(sampdir):
                logger.info("表样例数据【TableId:{}, optype:{}】".format(tabId, op_type))
                handleSamp(db, tabDic[tab], sampdir)

        opLog(dbinfo, tab, op_type, op_start_date, datetime.now())


def modelCopy(model_a, model_b):
    """
    复制模型对象的属性
    :param model_a:
    :param model_b:
    :return:
    """
    #print(model_a._meta.fields)
    for field in model_a._meta.fields:
        if field.name not in ['id', 'hdb', 'htab'] :
            setattr(model_b, field.name, getattr(model_a, field.name))
        if field.name == 'hdb':
            setattr(model_b, 'db_id', getattr(model_a, field.name).id)
        if field.name == 'htab':
            setattr(model_b, 'tab_id', getattr(model_a, field.name).id)
    return model_b


def doDelete(tabId):
    """
    删除操作，记录历史表
    :param tabId:
    :return:
    """
    # 删除前记录历史表  meta和 ddl
    metas = TabMeta.objects.filter(htab__id=tabId)
    for m in metas:
        metahis = TabMetaHis()
        metahis = modelCopy(m, metahis)
        metahis.save()

    ddl = TabDDL.objects.filter(htab__id=tabId)
    for m in ddl:
        ddlhis = TabDDLHis()
        ddlhis = modelCopy(m, ddlhis)
        ddlhis.save()

    TabInfo.objects.filter(id=tabId).delete()


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
    return True


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


def opLog(dbinfo, table_name, op_type, start_date, end_date):
    """
    操作日志记录
    :param dbinfo:
    :param table_name:
    :param op_type:
    :param start_date:
    :param end_date:
    :return:
    """
    op = OperateLog()
    op.db_info = dbinfo
    op.table_name = table_name
    op.op_type = op_type
    op.op_start_date = start_date
    op.op_end_date = end_date
    op.save()






if __name__ == '__main__':
    main()
