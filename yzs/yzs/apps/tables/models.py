from django.db import models
import datetime

# Create your models here.


class BusInfo(models.Model):
    bus_name = models.CharField(max_length=100, verbose_name='业务名称', help_text='业务名称')

    class Meta:
        db_table = "tb_businfo"  # 指明数据库表名
        verbose_name = '业务信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称


# db信息
class DBInfo(models.Model):
    businfo = models.ManyToManyField(BusInfo, blank=True, null=True)
    db_ip = models.CharField(max_length=20, verbose_name='ip地址', help_text='ip地址')
    db_port = models.CharField(max_length=20, verbose_name='端口', help_text='端口')
    db_name = models.CharField(max_length=100, null=True, verbose_name='名称', help_text='名称')
    schema_name = models.CharField(max_length=100, null=True, verbose_name='schema名称', help_text='schema名称')
    db_type = models.CharField(max_length=30,  verbose_name='db类型', help_text='db类型')
    db_comment = models.CharField(max_length=100,null=True, verbose_name='db注释', help_text='db注释')
    create_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_date = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        db_table = "tb_dbinfo"  # 指明数据库表名
        verbose_name = '库信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称
        unique_together = ('db_ip', 'db_port', 'schema_name', 'db_name', 'db_type',)

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return "{}:{}".format(self.db_ip, self.db_port)



# table信息
class TabInfo(models.Model):
    hdb = models.ForeignKey(DBInfo, on_delete=models.CASCADE, verbose_name='库', help_text='库')
    table_name = models.CharField(max_length=100, verbose_name='名称', help_text='名称')
    table_comment = models.CharField(max_length=100, null=True, verbose_name='table注释', help_text='table注释')
    create_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_date = models.DateTimeField(auto_now=True, help_text='更新时间')


    class Meta:
        db_table = "tb_tabinfo"  # 指明数据库表名
        verbose_name = '表信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
         """定义每个数据对象的显示信息"""
         return self.table_name



# 表结构
class TabMeta(models.Model):
    hdb = models.ForeignKey(DBInfo, on_delete=models.CASCADE, verbose_name='库id', help_text='库id')
    htab = models.ForeignKey(TabInfo, on_delete=models.CASCADE, verbose_name='表id', help_text='表id')
    col_name = models.CharField(max_length=100, verbose_name='列名称', help_text='列名称')
    col_type = models.CharField(max_length=60, verbose_name='列类型', help_text='列类型')
    col_comment = models.CharField(max_length=1024, null=True, verbose_name='列注释', help_text='列注释')
    is_null = models.CharField(max_length=1, verbose_name='是否为空', help_text='是否为空')
    default_val = models.CharField(max_length=200, null=True, verbose_name='默认值', help_text='默认值')
    create_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_date = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        db_table = "tb_tabmeta"  # 指明数据库表名
        verbose_name = '表结构信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    # def __str__(self):
    #     """定义每个数据对象的显示信息"""
    #     return self.col_name


# 表定义
class TabDDL(models.Model):
    hdb = models.ForeignKey(DBInfo, on_delete=models.CASCADE, verbose_name='库id', help_text='库id')
    htab = models.ForeignKey(TabInfo, on_delete=models.CASCADE, verbose_name='表id', help_text='表id')
    ddl_stmt = models.TextField(verbose_name='建表语句', help_text='建表语句')
    create_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_date = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        db_table = "tb_tabddl"  # 指明数据库表名
        verbose_name = '表结构信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    # def __str__(self):
    #     """定义每个数据对象的显示信息"""
    #     return self.ddl_stmt

# 表样例数据
class TabSamp(models.Model):
    hdb = models.ForeignKey(DBInfo, on_delete=models.CASCADE, verbose_name='库id', help_text='库id')
    htab = models.ForeignKey(TabInfo, on_delete=models.CASCADE, verbose_name='表id', help_text='表id')
    row_content = models.TextField(verbose_name='行内容', help_text='行内容')
    create_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_date = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        db_table = "tb_tabsamp"  # 指明数据库表名
        verbose_name = '表样例数据'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    # def __str__(self):
    #     """定义每个数据对象的显示信息"""
    #     return self.row_content


# 表结构历史
class TabMetaHis(models.Model):
    db_id = models.BigIntegerField(verbose_name='库id', help_text='库id')
    tab_id = models.BigIntegerField(verbose_name='表id', help_text='表id')
    col_name = models.CharField(max_length=100, verbose_name='列名称', help_text='列名称')
    col_type = models.CharField(max_length=60, verbose_name='列类型', help_text='列类型')
    col_comment = models.CharField(max_length=200, null=True, verbose_name='列注释', help_text='列注释')
    is_null = models.CharField(max_length=1, verbose_name='是否为空', help_text='是否为空')
    default_val = models.CharField(max_length=200, null=True, verbose_name='默认值', help_text='默认值')
    create_date = models.DateTimeField(help_text='原始创建时间')
    update_date = models.DateTimeField(help_text='原始更新时间')
    add_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    class Meta:
        db_table = "tb_tabmeta_his"  # 指明数据库表名
        verbose_name = '表结构历史信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    # def __str__(self):
    #     """定义每个数据对象的显示信息"""
    #     return self.col_name

# 表定义历史
class TabDDLHis(models.Model):
    db_id = models.BigIntegerField(verbose_name='库id', help_text='库id')
    tab_id = models.BigIntegerField(verbose_name='表id', help_text='表id')
    ddl_stmt = models.TextField(verbose_name='建表语句', help_text='建表语句')
    create_date = models.DateTimeField(help_text='原始创建时间')
    update_date = models.DateTimeField(help_text='原始更新时间')
    add_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    class Meta:
        db_table = "tb_tabddl_his"  # 指明数据库表名
        verbose_name = '表结构历史信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    # def __str__(self):
    #     """定义每个数据对象的显示信息"""
    #     return self.ddl_stmt


# 日志表
class OperateLog(models.Model):
    """
        op_type: heartBeat/new/update/delete

    """
    db_info =  models.CharField(max_length=100, verbose_name='库信息', help_text='库信息')
    table_name = models.CharField(max_length=100, verbose_name='表名称', help_text='表名称')
    op_type = models.CharField(max_length=60, verbose_name='操作类型', help_text='操作类型')
    op_start_date = models.DateTimeField(help_text='开始时间', null=True)
    op_end_date = models.DateTimeField(help_text='结束时间', null=True)
    create_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    class Meta:
        db_table = "tb_operatelog"  # 指明数据库表名
        verbose_name = '操作日志'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称
