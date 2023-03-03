from admins.models import Languages, Translations
from .serializers import BasedModelSerializer

def translator(word: str, lang: str = None):
    if lang:
        lng_code = lang
    else:
        lng_code = Languages.objects.filter(active=True).filter(default=True).first().code

    
    for lng in Languages.objects.filter(active=True):
        trarnsl = Translations.objects.filter(value__contains=f"{ lng.code }:{ word }")
        if trarnsl.exists():
            translation = trarnsl.first().value.get(lng_code)

            return translation

    
# search for api
def search_func(q, field, queryset, fields, image_fields, request, product=False):
    langs = Languages.objects.filter(active=True)
    results = []

    for lang in langs:
        for item in queryset:
            dct = item.__dict__
            if product:
                src_field = item.product.__dict__.get(field).get(lang.code)
                if item.product.name:
                    dct['name'] = item.product.name.get(lang.code, None)
                if item.product.description:
                    dct['description'] = item.product.description.get(lang.code, None)
            else:
                src_field = item.__dict__.get(field).get(lang.code)
                
            

            if str(src_field).lower().startswith(str(q).lower()):
                serializer = BasedModelSerializer(instance=dct, context={"lang": lang.code, 'fields': fields, 'image_fields': image_fields, 'request': request})
                print(serializer.data)
                results.append(serializer.data)
                

    return results
                
        