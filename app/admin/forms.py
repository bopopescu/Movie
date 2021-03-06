from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, TextAreaField, FileField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Tag, Auth, Role


# 后台登录表单
class LoginForm(FlaskForm):
    """管理员登录表单"""
    name = StringField(
        label=u"账号",
        validators=[
            DataRequired(message=u"请输入管理员账号")
        ],
        description=u"管理员账号",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入账号"
        }
    )
    password = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"请输入密码")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
        }
    )
    submit = SubmitField(
        label=u"登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    # 验证数据库中是否有此账号
    def validate_name(self, field):
        name = field.data
        admin = Admin.query.filter_by(name=name).first()
        if admin == None:
            raise ValidationError(u"账号不存在")


# 标签表单
class TagForm(FlaskForm):
    tag_name = StringField(
        label=u"标签名称",
        validators=[
            DataRequired(message=u"请输入标签")
        ],
        description=u"标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": u"请输入标签名称"
        }
    )
    submit = SubmitField(
        label=u"添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class MovieAddForm(FlaskForm):
    title = StringField(
        label=u"电影名称",
        validators=[
            DataRequired(message=u"请输入电影名称")
        ],
        description=u"电影名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片名"
        }
    )
    url = FileField(
        label=u"文件",
        validators=[
            DataRequired(message=u"请上传文件")
        ],
        description=u"电影文件",
    )
    info = TextAreaField(
        label=u"电影简介",
        validators=[
            DataRequired(u"请输入简介")
        ],
        description="电影简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    cover = FileField(
        label=u"封面",
        validators=[
            DataRequired(u"请上传封面")
        ],
        description=u"封面",
    )

    score = StringField(
        label="评分",
        validators=[
            DataRequired(message="请填写评分")
        ],
        description=u"评分",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入评分"
        }

    )

    tag_id = SelectField(
        label=u"标签",
        validators=[
            DataRequired(u"请选择标签")
        ],
        coerce=int,
        choices=[],
        default=2,
        description=u"标签",
        render_kw={
            "class": "form-control",
        }
    )

    area = StringField(
        label=u"地区",
        validators=[
            DataRequired(message=u"请输入地区")
        ],
        description=u"地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区"
        }
    )
    length = StringField(
        label=u"片长",
        validators=[
            DataRequired(message=u"请输入片长")
        ],
        description=u"片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长"
        }
    )
    release_time = StringField(
        label=u"上映时间",
        validators=[
            DataRequired(message=u"请选择上映时间")
        ],
        description=u"上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        label=u"添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    ''' SelectField字段关联数据库，在此初始化选项value值(其中Tag 为数据库模型) '''

    def __init__(self, *args, **kwargs):
        super(MovieAddForm, self).__init__(*args, **kwargs)
        self.tag_id.choices = [(tag.id, tag.name) for tag in
                               Tag.query.all()]

    # 验证输入分数是否标准
    def validate_score(self, field):
        score = float(field.data)
        # print(score)
        if score < 0 or score > 10:
            raise ValidationError(u"请输入1-10之间的数字")


class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题"
        }
    )

    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请输上传预告封面")
        ],
        description="预告封面",
        render_kw={
            "class": "form-control",
            "placeholder": "请上传预告封面"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class PassWordForm(FlaskForm):
    old_password = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入旧密码"
        }
    )
    new_password = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入新密码",
        }
    )
    submit = SubmitField(
        "修改",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_old_password(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_password(pwd):
            raise ValidationError("旧密码错误")


class AuthForm(FlaskForm):
    name = StringField(
        label=u"权限名称",
        validators=[
            DataRequired(message=u"请输入权限名称")
        ],
        description=u"权限名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": u"请输入权限名称"
        }
    )
    url = StringField(
        label=u"权限地址",
        validators=[
            DataRequired(message=u"请输入权限地址")
        ],
        description=u"权限地址",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": u"请输入权限地址"
        }
    )
    submit = SubmitField(
        label=u"添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class RoleForm(FlaskForm):
    name = StringField(
        label=u"角色名称",
        validators=[
            DataRequired(u"请输入角色名称")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入角色名称",
            # "required": False
        }
    )

    auths = SelectMultipleField(
        label=u"权限列表",
        validators=[
            DataRequired(message=u"请选择权限列表")
        ],
        coerce=int,
        render_kw={
            "class": "form-control",
            # "required": False
        }
    )
    submit = SubmitField(
        label=u"添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )
    ''' SelectField字段关联数据库，在此初始化选项value值(其中Auth为数据库模型) '''

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.auths.choices = [(auth.id, auth.name) for auth in
                              Auth.query.all()]


class AdminForm(FlaskForm):
    name = StringField(
        label=u"管理员名称",
        validators=[
            DataRequired(message=u"请输入管理员名称")
        ],
        description=u"管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入管理员名称"
        }
    )
    password = PasswordField(
        label=u"管理员密码",
        validators=[
            DataRequired(u"请输入管理员密码")
        ],
        description=u"管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码",
        }
    )
    rep_password = PasswordField(
        label=u"管理员重复密码",
        validators=[
            DataRequired(u"管理员重复密码"),
            EqualTo('password', message=u"两次密码不一致")
        ],
        description=u"管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "管理员重复密码",
        }
    )
    role_id = SelectField(
        label=u"所属角色",
        validators=[
            DataRequired(u"请选择所属角色")
        ],
        coerce=int,
        choices=[],
        render_kw={
            "class": "form-control"
        }
    )
    submit = SubmitField(
        label=u"添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )
    ''' SelectField字段关联数据库，在此初始化选项value值(其中Auth为数据库模型) '''

    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [(role.id, role.name) for role in
                              Role.query.all()]
