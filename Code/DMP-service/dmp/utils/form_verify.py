from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length

class DashboardForm(FlaskForm):
    """
    看板表单验证
    """
    dmp_dashboard_name = StringField("dmp_dashboard_name",
                                     validators=[DataRequired(message="看板名称不能为空"),
                                                 Length(max=50, message="看板名称最大长度不超过50")]
                                     )
    charts_position = StringField("charts_position",
                                  validators=[Length(max=65535, message="图表布局信息最大长度不超过65535")]
                                  )
    description = StringField("description",
                              validators=[Length(max=400, message="看板简介最大长度不超过400")]
                              )


class ArchiveForm(FlaskForm):
    """
    文件夹表单验证
    """
    dashboard_archive_name = StringField("dashboard_archive_name",
                                         validators=[DataRequired(message="文件夹名称不能为空"),
                                                     Length(max=50, message="文件夹名称最大长度不超过50")]
                                         )


class ChartForm(FlaskForm):
    """
    图表表单验证
    """
    chart_name = StringField("chart_name",
                             validators=[DataRequired(message="图表名称不能为空"),
                                         Length(max=50, message="图表名称最大长度不超过50")]
                             )
    chart_type = IntegerField("chart_type",
                              validators=[DataRequired(message="图表类型代码不能为空")]
                              )
    charts_position = StringField("charts_position",
                                  validators=[DataRequired(message="图表布局参数不能为空")]
                                  )
    dmp_dashboard_id = IntegerField("dmp_dashboard_id",
                                    validators=[DataRequired(message="数据看板ID不能为空")]
                                    )

