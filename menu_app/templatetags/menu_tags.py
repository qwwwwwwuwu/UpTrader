from django import template
from menu_app.models import MenuItem
from django.utils.html import format_html

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_path = context['request'].path

    # Получаем все пункты нужного меню одним запросом
    menu_items = (
        MenuItem.objects
        .filter(menu_name=menu_name)
        .select_related('parent')
        .order_by('order')
    )

    
    menu_dict = {}
    for item in menu_items:
        menu_dict[item.pk] = {
            'item': item,
            'children': [],
            'resolved_url': item.get_url()
        }

    root_items = []
    for item in menu_items:
        if item.parent:
            menu_dict[item.parent.pk]['children'].append(item.pk)
        else:
            root_items.append(item.pk)

    # Найдём активный элемент по текущему URL
    active_item_id = None
    for pk, data in menu_dict.items():
        if data['resolved_url'] == current_path:
            active_item_id = pk
            break

    # Собираем все ID родителей активного пункта
    expanded_ids = set()
    if active_item_id:
        current = menu_dict[active_item_id]['item']
        while current.parent:
            expanded_ids.add(current.parent.pk)
            current = current.parent
        expanded_ids.add(active_item_id)  

    def render_menu_item(item_id, level=0):
        data = menu_dict[item_id]
        item = data['item']
        url = data['resolved_url']
        is_active = item.pk == active_item_id
        is_expanded = item.pk in expanded_ids
        children_ids = data['children']

        classes = ['menu-item']
        if is_active:
            classes.append('active')
        if is_expanded:
            classes.append('expanded')

        html = f'<li class="{" ".join(classes)}">'
        html += f'<a href="{url}">{item.title}</a>'

        
        if children_ids and is_expanded and level == 0:
            html += '<ul>'
            for child_id in sorted(children_ids, key=lambda x: menu_dict[x]['item'].order):
                html += render_menu_item(child_id, level + 1)
            html += '</ul>'

        html += '</li>'
        return html

    
    menu_html = '<ul>'
    for item_id in sorted(root_items, key=lambda x: menu_dict[x]['item'].order):
        menu_html += render_menu_item(item_id)
    menu_html += '</ul>'

    return format_html(menu_html)

