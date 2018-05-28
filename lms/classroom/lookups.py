from ajax_select import register, LookupChannel
from accounts.models import User
from .models import Course
from django.utils.html import escape


@register('instructors')
class InstructorLookup(LookupChannel):
    model = User

    def get_query(self, request):
        # print('akoh')
        return self.model.objects.filter(user_type='IN').order_by('first_name')

    # def format_item_display(self, item):
    #     return u'<span class="tag">%s</span>' %item.first_name
    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))
        # return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))