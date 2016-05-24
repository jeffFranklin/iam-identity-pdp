import json
from resttools.dao_implementation.irws import File as IRWSFile
from resttools.dao_implementation.gws import File as GWSFile


def mock_irws_resources(conf={}):
    kwargs = dict(irws_root='/{}/v2'.format(conf.get('SERVICE_NAME')))

    resources = {}
    resources.update(mock_irws_person('user1e', display={}, **kwargs))
    resources.update(mock_irws_person('idtest55', display=dict(
        first='Dwight', middle='David', last='Adams')))
    resources.update(mock_irws_person('student', identifiers=['sdb']))
    resources.update(mock_irws_person('employee', identifiers=['hepps']))
    resources.update(mock_irws_person('studemp',
                                      identifiers=['sdb', 'hepps']))
    resources.update(mock_irws_person('nothing', identifiers=['cascadia']))

    IRWSFile._cache_db.update(resources)


def mock_gws_resources(
        admin_group='u_identity_profile_impersonators',
        publish_preview_group='u_identity_profile_publish-previewers'):
    # make user1e an admin and noone else.
    groups = [admin_group, publish_preview_group]
    gws_root = '/group_sws/v2'
    netid = 'user1e'
    effective_members = {
        '{gws_root}/group/{group}/effective_member/{netid}'.format(
            gws_root=gws_root, group=group, netid=netid): 'payload'
        for group in groups}
    GWSFile._cache_db.update(effective_members)

# we only receive one "clazz" from the registrar, so "clazz" should always
# contain just one value in the list.  Modeled in rest of application as a
# variable, not object, but comes from IRWS as object so mock is an object


def mock_irws_person(netid, irws_root='/registry-dev/v2',
                     employee_id='123456789', student_number='1234567',
                     birthdate='2001-01-01',
                     formal=dict(first='JANE', last='DOE'),
                     display=dict(first='Jane', middle='X', last='Doe'),
                     # rollup is same as display but listed separate for tests
                     rollup_name=dict(first='Jane', middle='roll', last='Doe'),
                     identifiers=('hepps', 'sdb'), system_key='123456789',
                     email='jane.doe@uw.edu', sms=None, pac='123456',
                     clazz=('Senior', 'Senior'), majors=('HCDE', 'Physics'),
                     student_phone_number=('206-123-4567', '206-123-4568'),
                     student_emails=('janey@example.com',),
                     employee_phone_number=('206-234-4567', '206-234-4568'),
                     employee_address=('4333 Brooklyn Ave NE ' +
                                       'Seattle WA 98125',),
                     employee_titles=('Specialist', 'Professor'),
                     employee_depts=('UWIT', 'Psychology'),
                     employee_emails=('jane@example.edu',
                                      'jane-test@example.com'),
                     employee_publish='Y',  # 'Y', 'N', or 'E' (default 'Y')
                     student_publish='Y',  # 'Y' or 'N', default 'Y
                     mailstop='359540', pdspreferredname='Jane PDS Doe',
                     pdsobjectclass=('uwPerson'),
                     **kwargs):

    """Return mocks of the resources needed for a given netid."""
    kwargs.update(dict(netid=netid, irws_root=irws_root,
                       employee_id=employee_id, student_number=student_number,
                       birthdate=birthdate, formal=formal, display=display,
                       rollup_name=rollup_name,
                       identifiers=identifiers, system_key=system_key,
                       email=email, sms=sms, pac=pac, clazz=clazz,
                       majors=majors,
                       student_phone_number=student_phone_number,
                       student_publish=student_publish,
                       student_emails=student_emails,
                       employee_phone_number=employee_phone_number,
                       employee_address=employee_address, mailstop=mailstop,
                       employee_titles=employee_titles,
                       employee_depts=employee_depts,
                       employee_publish=employee_publish,
                       employee_emails=employee_emails,
                       pdspreferredname=pdspreferredname,
                       pdsobjectclass=pdsobjectclass))

    irws_resources = {}
    identifier_urls = {}
    # This code generates the identifiers and relative URLS
    # that are returned when you search for a person.
    for identifier in identifiers:
        source = source_person(identifier, **kwargs)
        # grab the shortest key for our url, split out irws_root
        identifier_urls[identifier] = min(source.keys(), key=len).split(
            irws_root)[1]
        irws_resources.update(source_person(identifier, **kwargs))

    irws_person = {
        'person': [{
            'identity': {
                'regid': '0000deadbeef', 'lname': formal['last'],
                'fname': formal['first'],
                'identifiers': identifier_urls
            }
        }]
    }
    recover_contacts = [
        dict(type=ctype, value=value, validation_date='today')
        for ctype, value in (('email', email), ('sms', sms)) if value]

    f = display

    name_info = {
            "name": [{
                "validid": "0000deadbeef",
                "formal_cname": '{first} {last}'.format(**formal),
                "formal_fname": formal['first'],
                "formal_sname": formal['last'],
                'display_cname': ' '.join(display.get(x, '')
                                          for x in ('first', 'middle', 'last')
                                          if display.get(x, '')),
                'display_fname': display.get('first', ''),
                'display_mname': display.get('middle', ''),
                'display_sname': display.get('last', '')
            }]}

    rollup_name_info = {
        "name": [{
            "validid": "0000deadbeef",
            "formal_cname": '{first} {last}'.format(**formal),
            "formal_fname": formal['first'],
            "formal_sname": formal['last'],
            'display_cname': ' '.join(rollup_name.get(x, '')
                                      for x in ('first', 'middle', 'last')
                                      if rollup_name.get(x, '')),
            'display_fname': rollup_name.get('first', ''),
            'display_mname': rollup_name.get('middle', ''),
            'display_sname': rollup_name.get('last', '')
        }]}

    irws_resources.update({
        '{irws_root}/person?uwnetid={netid}': irws_person,
        '{irws_root}/name/uwnetid={netid}': name_info,
        '{irws_root}/name/uwnetid={netid}?-rollup': rollup_name_info,
        '{irws_root}/profile/validid=uwnetid={netid}': {
            "profile": [{
                "recover_contacts": recover_contacts,
                "recover_block_reasons": []}
            ]},
        '{irws_root}/pdsentry/validid=uwnetid={netid}': {
            "pdsentry": [{
                "entry": {
                    "uwPersonPreferredName": pdspreferredname,
                    "objectClass": [pdsobjectclass]
                }
            }
            ]}
    })

    resources = {key.format(**kwargs): json.dumps(value)
                 for key, value in irws_resources.items()}
    return resources


def source_person(identifier, **kwargs):
    """
    Return the resources associated with a given source.
    Special hack to update source attributes by including an
    {identifier}_update dictionary in the kwargs.
    """
    # We make no assumption on the id. To ensure this, make the id
    # a 9-digit hash of netid and identifier. The aim is to guarantee
    # uniqueness in our resources dictionary.
    key = '{irws_root}/person/{identifier}/{hash}'.format(
        identifier=identifier,
        hash=hash(kwargs.get('netid') + identifier) % (10**9),
        **kwargs)

    resources = {}
    if identifier in ('hepps', 'uwhr'):
        person = {'person': [dict(
            validid=kwargs.get('employee_id'), regid='0000deadbeef',
            lname=kwargs['formal']['last'], fname=kwargs['formal']['first'],
            status_code='1', source_code='1', source_name='F',
            status_name='F',
            wp_publish=kwargs['employee_publish'],
            wp_phone=kwargs['employee_phone_number'],  # V2
            wp_address=kwargs['employee_address'],
            mailstop=kwargs['mailstop'],
            wp_title=kwargs['employee_titles'],
            wp_email=kwargs['employee_emails'],
            wp_department=kwargs['employee_depts']
        )]}
    elif identifier == 'sdb':
        pac = 'P' if kwargs.get('pac', None) else None
        person = {'person': [dict(
            validid=kwargs.get('system_key'), regid='0000deadbeef',
            studentid=kwargs.get('student_number'), pac=pac, branch='0',
            lname=kwargs['formal']['last'], fname=kwargs['formal']['first'],
            status_code='1', in_feed='1', categories=[{'category_code': '1'}],
            wp_title=kwargs.get('clazz'), wp_department=kwargs.get('majors'),
            wp_phone=kwargs['student_phone_number'],
            wp_publish=kwargs['student_publish'],
            wp_email=kwargs['student_emails'],
            source_code='1', status_name='F', source_name='F'
        )]}
    else:
        person = {'person': [{'status_code': '1'}]}

    if identifier + '_update' in kwargs:
        person['person'][0].update(kwargs.get(identifier + '_update'))
    resources[key] = person
    return resources
