from django import template
register = template.Library()

@register.filter
def verbose_name_field_name_filter(obj, field_name): #fieldname é str (o nome do campo)
    if obj:
        return obj.first()._meta.get_field(field_name).verbose_name
    else:
        return '-'

@register.filter
def verbose_name_field_index_filter(obj, field_index): #field_index é int (o indice dos fields e zero será 'id')
    if obj:
        return obj.first()._meta.fields[field_index].verbose_name
    else:
        return '-'

@register.filter
def verbose_name_field_filter(obj, field_index): #field_index é int (o indice dos fields e zero será 'id')
    #return obj._meta.fields[field_index].verbose_name
    #print( obj._meta.fields[field_index].verbose_name)
    if obj:
        if obj._meta.fields[field_index].verbose_name == 'ID':
            return obj._meta.fields[field_index].verbose_name + '(Código)'
        else:
            return obj._meta.fields[field_index].verbose_name
    else:
        return '-'

@register.filter
def value_field_index_filter(obj, field_index): #field_index é int (o indice dos fields e zero será 'id')
    #return getattr(obj, obj._meta.fields[field_index].name)  tanto faz
    if obj:
        return obj._meta.fields[field_index].value_from_object(obj)
    else:
        return '-'
    #https://stackoverflow.com/questions/51905712/how-to-get-the-value-of-a-django-model-field-object
    #https://stackoverflow.com/questions/2170228/iterate-over-model-instance-field-names-and-values-in-template

@register.filter
def value_field_index_filter_S_N(obj, field_index):
    if obj:
        if obj._meta.fields[field_index].value_from_object(obj) == 'S':
            return 'Sim'
        elif  obj._meta.fields[field_index].value_from_object(obj) == 'N':
            return 'Não'
    else:
        return '-'

@register.filter
def verbose_name_query_filter(obj):
    if obj:
        return obj.first()._meta.verbose_name
    else:
        return '-'

@register.filter
def verbose_name_plural_query_filter(obj):
    if obj:
        return obj.first()._meta.verbose_name_plural
    else:
        return '-'

# https://timonweb.com/posts/accessing-modelsobjects-verbose-name-in-django-template/
#A pasta tem que ter o nome templatetags sem underline
#Criar o arquivo vazio __init__.py dentro dela
#Criar este arquivo deste código dentro dela
#Remover todos os * .pyc gerados
#Reiniciar o servidor
#No template após o extends (não usar no template base pois os filtros são por aplicativos),
#para evitar conflito de nomes
#{% load minhas_tags %}

#{{ object|verbose_name_query_filter }}
#{{ object|verbose_name_plural_query_filter }}

#<span>{{ p|verbose_name_field_filter:'name' }}: {{ p.name }}</span>
#<span>{{ p|verbose_name_field_filter:'birth_date' }}: {{ p.birth_date }}</span>

#testei no shell
#https://stackoverflow.com/questions/3647805/get-models-fields-in-django
#print(Material.objects.first()._meta.fields[1].verbose_name)  com o índice
#print(Material.objects.first()._meta.fields) retorna todos os campos, a lista de campos
#campos muitos-para-muitos, precisará acessar model._meta.many_to_many
#Se você estiver usando chaves estrangeiras genéricos você também deve verificar_meta.virtual_field
#No shell
#from material.models import Material
#opts = Material.objects.first()._meta
#for f in sorted(opts.fields + opts.many_to_many):
#   print('{}-{}:{}'.format(f.name,f.verbose_name,f))