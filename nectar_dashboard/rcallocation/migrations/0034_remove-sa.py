# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-07-15 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcallocation', '0033_start_date_part2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocationrequest',
            name='allocation_home',
            field=models.CharField(blank=True, choices=[('nci', 'Australian Capital Territory (NCI)'), ('intersect', 'New South Wales (Intersect)'), ('qcif', 'Queensland (QCIF)'), ('tpac', 'Tasmania (TPAC)'), ('uom', 'Victoria (Melbourne)'), ('monash', 'Victoria (Monash)'), ('swinburne', 'Victoria (Swinburne)'), ('auckland', 'Auckland Uni (New Zealand)'), ('national', 'National')], help_text='Allocation home of the allocation', max_length=128, null=True, verbose_name='Allocation Home'),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='requested_allocation_home',
            field=models.CharField(choices=[('unassigned', 'Unassigned'), ('nci', 'Australian Capital Territory (NCI)'), ('intersect', 'New South Wales (Intersect)'), ('qcif', 'Queensland (QCIF)'), ('tpac', 'Tasmania (TPAC)'), ('uom', 'Victoria (Melbourne)'), ('monash', 'Victoria (Monash)'), ('swinburne', 'Victoria (Swinburne)'), ('auckland', 'Auckland Uni (New Zealand)'), ('national', 'National')], default='national', help_text='You can provide a primary location where you expect to\n                use most resources, effectively the main Nectar site for your\n                allocation. Use of other locations is still possible.\n                This can also indicate a specific arrangement with a\n                Nectar site, for example where you obtain support, or if\n                your institution is a supporting member of that site.\n                Select unassigned if you have no preference.\n                ', max_length=128, verbose_name='Allocation home location'),
        ),
    ]
