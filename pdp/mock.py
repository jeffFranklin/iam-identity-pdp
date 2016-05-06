import re
import json
from restclients.dao_implementation.irws import File as RestClientsFile
from resttools.dao_implementation.irws import File as RestToolsFile


def mock_irws_resources(conf={}):
    kwargs = dict(irws_root='/{}/v2'.format(conf.get('SERVICE_NAME')))

    resources = {}
    resources.update(mock_irws_person('user1e', display={}, **kwargs))
    resources.update(mock_irws_person('idtest55', display=dict(
        first='Dwight', middle='David', last='Adams')))

    RestToolsFile._cache_db.update(resources)
    RestClientsFile._cache.update(resources)


def mock_irws_person(netid, irws_root='/registry-dev/v2',
                     employee_id='123456789', student_number='1234567',
                     birthdate='2001-01-01',
                     formal=dict(first='JANE', last='DOE'),
                     display=dict(first='Jane', middle='X', last='Doe'),
                     identifiers=('uwhr', 'sdb'), system_key='123456789',
                     email=None, sms=None, pac='123456',
                     clazz='Senior', majors=['HCDE'],
                     student_phone_number=['206-123-4567', '206-123-4568'],
                     employee_phone_number=['206-234-4567', '206-234-4568'],
                     **kwargs):
    """Return mocks of the resources needed for a given netid."""

    kwargs.update(dict(netid=netid, irws_root=irws_root,
                       employee_id=employee_id, student_number=student_number,
                       birthdate=birthdate, formal=formal, display=display,
                       identifiers=identifiers, system_key=system_key,
                       email=email, sms=sms, pac=pac, clazz=clazz,
                       majors=majors,
                       student_phone_number=student_phone_number,
                       employee_phone_number=employee_phone_number))

    irws_resources = {}
    identifier_urls = {}
    # This code generates the identifiers and relative URLS
    # that are returned when you search for a person
    # Currently supports only UWHR, HEPPS, and SDB sources
    for identifier in identifiers:
        source = source_person(identifier, **kwargs)
        if identifier in {'uwhr', 'hepps'}:
            identifier_urls[identifier] = '/person/{identifier}/{employee_id}'\
                .format(identifier=identifier, employee_id=employee_id)
        elif identifier == 'sdb':
            identifier_urls[identifier] = '/person/{identifier}/{system_key}'\
                .format(identifier=identifier, system_key=system_key)
        irws_resources.update(source)

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

    irws_resources.update({
        '{irws_root}/person?uwnetid={netid}': irws_person,
        '{irws_root}/name/uwnetid={netid}': {
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
            }]},
        '{irws_root}/profile/validid=uwnetid={netid}': {
            "profile": [{
                "recover_contacts": recover_contacts,
                "recover_block_reasons": []}
            ]}
    })

    resources = {key.format(**kwargs): json.dumps(value)
                 for key, value in irws_resources.items()}
    # add in v1 equivalents for restclients
    resources.update({re.sub(r'/v2/', '/v1/', key): value
                      for key, value in resources.items()})
    return resources


def source_person(identifier, **kwargs):
    key = ''
    resources = {}
    if identifier in ('hepps', 'uwhr'):
        key = '{irws_root}/person/{identifier}/{employee_id}'.format(
            irws_root=kwargs.get('irws_root'), identifier=identifier,
            employee_id=kwargs.get('employee_id'))
        person = {'person': [dict(
            validid=kwargs.get('employee_id'), regid='0000deadbeef',
            lname=kwargs['formal']['last'], fname=kwargs['formal']['first'],
            status_code='1', source_code='1', source_name='F',
            status_name='F',
            wp_phone=kwargs['employee_phone_number'],  # V2
            category_code='shhh', category_name='fff',  # remove when no v1
        )]}
    elif identifier == 'sdb':
        key = '{irws_root}/person/{identifier}/{system_key}'.format(
            irws_root=kwargs.get('irws_root'), identifier=identifier,
            system_key=kwargs.get('system_key'))
        pac = 'P' if kwargs.get('pac', None) else None
        person = {'person': [dict(
            validid=kwargs.get('system_key'), regid='0000deadbeef',
            studentid=kwargs.get('student_number'), pac=pac, branch='0',
            lname=kwargs['formal']['last'], fname=kwargs['formal']['first'],
            status_code='1', in_feed='1', categories=[{'category_code': '1'}],
            wp_title=kwargs.get('clazz'), department=kwargs.get('majors'),
            wp_phone=kwargs['student_phone_number'],  # V2
            source_code='1', status_name='F', source_name='F'
        )]}
        # TODO I think this is currently broken (mattjm 2016-05-06)
        # As far as I know setting a PAC isn't supported and the setting
        # is done via a post to the following URL
        # (URLS fixed by mattjm 2016-05-06)
        if kwargs.get('pac', None):
            # add a pac resource
            pac_key = re.sub('/{system_key}$'.format(
                system_key=kwargs.get('system_key')), '/{system_key}/pac', key
            )
            resources[pac_key] = {'exists': 'yup'}
    else:
        person = {'person': [{'status_code': '1'}]}

    if identifier + '_update' in kwargs:
        person['person'][0].update(kwargs.get(identifier + '_update'))
    resources[key] = person
    return resources
