from django import template

register = template.Library()

@register.simple_tag
def get_grade_and_percentage(score):
    # score = score * 100
    grade = ''
    if score > 80 and score <= 100:
        grade = 'A'
    elif score > 70 and score < 80:
        grade = 'B'
    elif score > 60 and score < 70:
        grade = 'C'
    elif score > 50 and score < 60:
        grade = 'D'
    else:
        grade = 'F'

    result = '{0}({1})'.format(score,grade)
    return result