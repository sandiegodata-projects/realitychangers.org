""" Example pylib functions"""


def accepted_students(resource, doc, env, *args, **kwargs):
    """ An example row generator function.

    Reference this function in a Metatab file as the value of a Datafile:

            Datafile: python:pylib#row_generator

    The function must yield rows, with the first being headers, and subsequenct rows being data.

    :param resource: The Datafile term being processed
    :param doc: The Metatab document that contains the term being processed
    :param args: Positional arguments passed to the generator
    :param kwargs: Keyword arguments passed to the generator
    :return:


    The env argument is a dict with these environmental keys:

    * CACHE_DIR
    * RESOURCE_NAME
    * RESOLVED_URL
    * WORKING_DIR
    * METATAB_DOC
    * METATAB_WORKING_DIR
    * METATAB_PACKAGE

    It also contains key/value pairs for all of the properties of the resource.

    """
    from nameparser import HumanName
    
    yield "year school last first middle name_key".split()
    
    for i, rp in enumerate(doc.reference('accepted_students_source').iterrowproxy()):

        name = HumanName(rp.Name)
        
        hn = HumanName(rp.Name)
        
        yield (rp.Year, rp.School, name.last, name.first, name.middle, 
              (hn.first+hn.middle+hn.last.replace(' ','')).lower().replace(' ',''))

def all_students(resource, doc, env, *args, **kwargs):
    import petl 
    from nameparser import HumanName
    
    r = doc.reference('all_students_source')

    def full_name(rec):
        name =  (rec['first_name'] or '') + ' ' + (rec['last_name'] or '')

        return name

    def name_key(rec):
        
        hn = HumanName(full_name(rec))
        
        return (hn.first+hn.middle+hn.last.replace(' ','')).lower().replace(' ','')

    yield from petl\
        .rename(r, {'cd re':'school', 
                    'Last Name':'last_name',
                    'First Name':'first_name',
                    '1st Assembly':'1st_assembly'})\
        .addfield('full_name', index=2, value=lambda rec: full_name(rec) )\
        .convert('last_name', lambda v, rec: HumanName(rec.full_name).last, pass_row=True  )\
        .addfield('middle_name', index=5, value=lambda rec: HumanName(rec.full_name).middle)\
        .convert('first_name', lambda v, rec: HumanName(rec.full_name).first, pass_row=True  )\
        .addfield('name_key', name_key, index=6)\
        .cutout('full_name')
