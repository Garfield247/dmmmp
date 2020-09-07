from validator import Validator, StringField, IntegerField, EnumField


class Get_dashboards_and_archives_validator(Validator):
    upper_dmp_dashboard_archive_id = IntegerField(min_value=1, required=False)
    is_owner = EnumField(choices=[True, False], required=True)
    state = EnumField(choices=[0, 1, 2], required=False)
    name = StringField(max_length=64, required=False)
