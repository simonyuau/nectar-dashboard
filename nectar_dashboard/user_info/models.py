# Copyright 2019 Australian Research Data Commons
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pickle
import re

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

# The known values of the 'affiliation' attribute as defined
# by the AAF
FACULTY = 'faculty'
STUDENT = 'student'
STAFF = 'staff'
EMPLOYEE = 'employee'
MEMBER = 'member'
AFFILIATE = 'affiliate'
ALUM = 'alum'
LIBRARY_WALK_IN = 'library-walk-in'

AFFILIATION_CHOICES = [(FACULTY, 'Faculty'),
                       (STUDENT, 'Student'),
                       (STAFF, 'Staff'),
                       (EMPLOYEE, 'Employee'),
                       (MEMBER, 'Member'),
                       (AFFILIATE, 'Affiliate'),
                       (ALUM, 'Alumnus'),
                       (LIBRARY_WALK_IN, 'Library walk-in')]

# The state field is notionally internal to rcshibboleth
STATE_NEW = 'new'
STATE_REGISTERED = 'registered'
STATE_CREATED = 'created'

STATE_CHOICES = [(STATE_NEW, STATE_NEW),
                 (STATE_REGISTERED, STATE_REGISTERED),
                 (STATE_CREATED, STATE_CREATED)]

# Mapping from names of attributes in the User class to the
# corresponding names used in the shibboleth attribute pickle.
SHIB_ATTR_MAPPING = {
    'displayname': 'fullname',
    'email': 'mail',
    'first_name': 'firstname',
    'surname': 'surname',
    'phone_number': 'telephonenumber',
    'mobile_number': 'mobilenumber',
    'home_organization': 'homeorganization',
    'orcid': 'orcid',
    'affiliation': 'affiliation'
}


def validate_phone(value):
    if not re.compile(r'^(\+[\d]+)?[\d\s]*$').match(value):
        raise ValidationError('Invalid phone number: %(value)s',
                              params={'value': value})


class PhoneField(models.CharField):
    default_validators = [validate_phone]

    def to_python(self, value):
        return value.strip() if value else None


class RCUser(models.Model):
    """Model for user information in the rcshib database

    NB this model is managed by the RCShibboleth project, and the table
    is in the "rcshib" database.  Changes to >>this<< class should track
    changes made in the RCShibboleth project.  Migrations should be
    perfomed on that side too.

    This model does have migrations, but they should be written to only
    take effect when running tests.
    """

    persistent_id = models.CharField(unique=True, max_length=250,
                                     blank=True, null=True, editable=False)
    user_id = models.CharField(max_length=64, blank=True, null=True,
                               editable=False)
    displayname = models.CharField(max_length=250, blank=True, null=True,
                                   editable=False)
    email = models.CharField(max_length=250, blank=True, null=True,
                             editable=False)
    state = models.CharField(max_length=10, blank=True, null=True,
                             editable=False, choices=STATE_CHOICES,
                             default=STATE_NEW)
    last_login = models.DateTimeField(blank=True, null=True, editable=False)
    terms_accepted_at = models.DateTimeField(blank=True, null=True,
                                             editable=False)
    shibboleth_attributes = models.BinaryField(blank=True, null=True,
                                               editable=False)
    registered_at = models.DateTimeField(blank=True, null=True,
                                         editable=False)
    terms_version = models.CharField(max_length=64, blank=True, null=True,
                                     editable=False)
    ignore_username_not_email = models.IntegerField(blank=True, null=True,
                                                    editable=False)
    first_name = models.CharField(max_length=250, blank=True, null=True,
                                  editable=False)
    surname = models.CharField(max_length=250, blank=True, null=True,
                               editable=False)
    phone_number = PhoneField('Phone number',
                              max_length=64, blank=True, null=True)
    mobile_number = PhoneField('Mobile number',
                               max_length=64, blank=True, null=True)
    home_organization = models.CharField('Home organization',
                                         max_length=250, blank=True,
                                         null=True, editable=False)
    orcid = models.CharField('ORCID identifier',
                             max_length=64, blank=True, null=True)
    affiliation = models.CharField('Affiliation',
                                   max_length=64, blank=True, null=True,
                                   choices=AFFILIATION_CHOICES,
                                   default=MEMBER,
                                   help_text="""The user's affiliation to
                                   their home organization.  This needs
                                   to be more specific than 'member'""")

    class Meta:
        managed = False
        db_table = 'user'

    @property
    def shibboleth_dict(self):
        if self.shibboleth_attributes:
            return pickle.loads(self.shibboleth_attributes)
        else:
            return {}

    def is_overridden(self, attribute):
        shib_value = self.shibboleth_dict.get(SHIB_ATTR_MAPPING[attribute])
        my_value = getattr(self.__dict__, attribute, None)
        return shib_value != my_value

    def get_absolute_url(self):
        return reverse('horizon:identity:lookup:view', args=(self.id,))