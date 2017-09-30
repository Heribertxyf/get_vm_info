# -*- coding:utf-8 -*-
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from get_vm_info.models import db, Site, Gpncounter

admin = Admin()


class GpncounterAdmin(ModelView):
    column_display_all_relations = True
    column_list = ['source', 'destination',
                   'delay_value', 'primary',
                   'secondary', 'update_time']


class SiteAdmin(ModelView):
    column_searchable_list = ['site_name', 'address']


admin.add_view(GpncounterAdmin(Gpncounter, db.session))
admin.add_view(SiteAdmin(Site, db.session))
