# Generated by Django 3.0.14 on 2021-09-16 14:49

import core.fields
import datetime
from django.db import migrations, models
import product.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('validity_from', core.fields.DateTimeField(db_column='ValidityFrom', default=datetime.datetime.now)),
                ('validity_to', core.fields.DateTimeField(blank=True, db_column='ValidityTo', null=True)),
                ('legacy_id', models.IntegerField(blank=True, db_column='LegacyID', null=True)),
                ('id', models.AutoField(db_column='ProdID', primary_key=True, serialize=False)),
                ('uuid', models.CharField(db_column='ProdUUID', default=uuid.uuid4, max_length=36, unique=True)),
                ('code', models.CharField(db_column='ProductCode', max_length=8)),
                ('name', models.CharField(db_column='ProductName', max_length=100)),
                ('date_from', models.DateTimeField(db_column='DateFrom')),
                ('date_to', models.DateTimeField(db_column='DateTo')),
                ('insurance_period', models.SmallIntegerField(db_column='InsurancePeriod')),
                ('administration_period', models.IntegerField(blank=True, db_column='AdministrationPeriod', null=True)),
                ('lump_sum', models.DecimalField(db_column='LumpSum', decimal_places=2, max_digits=18)),
                ('max_members', models.SmallIntegerField(db_column='MemberCount')),
                ('max_installments', models.IntegerField(blank=True, db_column='MaxInstallments', null=True)),
                ('threshold', models.IntegerField(blank=True, db_column='Threshold', null=True)),
                ('recurrence', models.IntegerField(blank=True, db_column='Recurrence', null=True)),
                ('premium_adult', models.DecimalField(blank=True, db_column='PremiumAdult', decimal_places=2, max_digits=18, null=True)),
                ('premium_child', models.DecimalField(blank=True, db_column='PremiumChild', decimal_places=2, max_digits=18, null=True)),
                ('ded_insuree', models.DecimalField(blank=True, db_column='DedInsuree', decimal_places=2, max_digits=18, null=True)),
                ('ded_op_insuree', models.DecimalField(blank=True, db_column='DedOPInsuree', decimal_places=2, max_digits=18, null=True)),
                ('ded_ip_insuree', models.DecimalField(blank=True, db_column='DedIPInsuree', decimal_places=2, max_digits=18, null=True)),
                ('max_insuree', models.DecimalField(blank=True, db_column='MaxInsuree', decimal_places=2, max_digits=18, null=True)),
                ('max_op_insuree', models.DecimalField(blank=True, db_column='MaxOPInsuree', decimal_places=2, max_digits=18, null=True)),
                ('max_ip_insuree', models.DecimalField(blank=True, db_column='MaxIPInsuree', decimal_places=2, max_digits=18, null=True)),
                ('period_rel_prices', models.CharField(blank=True, db_column='PeriodRelPrices', max_length=1, null=True)),
                ('period_rel_prices_op', models.CharField(blank=True, db_column='PeriodRelPricesOP', max_length=1, null=True)),
                ('period_rel_prices_ip', models.CharField(blank=True, db_column='PeriodRelPricesIP', max_length=1, null=True)),
                ('acc_code_premiums', models.CharField(blank=True, db_column='AccCodePremiums', max_length=25, null=True)),
                ('acc_code_remuneration', models.CharField(blank=True, db_column='AccCodeRemuneration', max_length=25, null=True)),
                ('ded_treatment', models.DecimalField(blank=True, db_column='DedTreatment', decimal_places=2, max_digits=18, null=True)),
                ('ded_op_treatment', models.DecimalField(blank=True, db_column='DedOPTreatment', decimal_places=2, max_digits=18, null=True)),
                ('ded_ip_treatment', models.DecimalField(blank=True, db_column='DedIPTreatment', decimal_places=2, max_digits=18, null=True)),
                ('max_treatment', models.DecimalField(blank=True, db_column='MaxTreatment', decimal_places=2, max_digits=18, null=True)),
                ('max_op_treatment', models.DecimalField(blank=True, db_column='MaxOPTreatment', decimal_places=2, max_digits=18, null=True)),
                ('max_ip_treatment', models.DecimalField(blank=True, db_column='MaxIPTreatment', decimal_places=2, max_digits=18, null=True)),
                ('ded_policy', models.DecimalField(blank=True, db_column='DedPolicy', decimal_places=2, max_digits=18, null=True)),
                ('ded_op_policy', models.DecimalField(blank=True, db_column='DedOPPolicy', decimal_places=2, max_digits=18, null=True)),
                ('ded_ip_policy', models.DecimalField(blank=True, db_column='DedIPPolicy', decimal_places=2, max_digits=18, null=True)),
                ('max_policy', models.DecimalField(blank=True, db_column='MaxPolicy', decimal_places=2, max_digits=18, null=True)),
                ('max_op_policy', models.DecimalField(blank=True, db_column='MaxOPPolicy', decimal_places=2, max_digits=18, null=True)),
                ('max_ip_policy', models.DecimalField(blank=True, db_column='MaxIPPolicy', decimal_places=2, max_digits=18, null=True)),
                ('audit_user_id', models.IntegerField(db_column='AuditUserID')),
                ('grace_period_enrolment', models.IntegerField(db_column='GracePeriod')),
                ('grace_period_payment', models.IntegerField(blank=True, db_column='WaitingPeriod', null=True)),
                ('grace_period_renewal', models.IntegerField(blank=True, db_column='GracePeriodRenewal', null=True)),
                ('registration_lump_sum', models.DecimalField(blank=True, db_column='RegistrationLumpSum', decimal_places=2, max_digits=18, null=True)),
                ('registration_fee', models.DecimalField(blank=True, db_column='RegistrationFee', decimal_places=2, max_digits=18, null=True)),
                ('general_assembly_lump_sum', models.DecimalField(blank=True, db_column='GeneralAssemblyLumpSum', decimal_places=2, max_digits=18, null=True)),
                ('general_assembly_fee', models.DecimalField(blank=True, db_column='GeneralAssemblyFee', decimal_places=2, max_digits=18, null=True)),
                ('start_cycle_1', models.CharField(blank=True, db_column='StartCycle1', max_length=5, null=True)),
                ('start_cycle_2', models.CharField(blank=True, db_column='StartCycle2', max_length=5, null=True)),
                ('start_cycle_3', models.CharField(blank=True, db_column='StartCycle3', max_length=5, null=True)),
                ('start_cycle_4', models.CharField(blank=True, db_column='StartCycle4', max_length=5, null=True)),
                ('max_no_consultation', models.IntegerField(blank=True, db_column='MaxNoConsultation', null=True)),
                ('max_no_surgery', models.IntegerField(blank=True, db_column='MaxNoSurgery', null=True)),
                ('max_no_delivery', models.IntegerField(blank=True, db_column='MaxNoDelivery', null=True)),
                ('max_no_hospitalization', models.IntegerField(blank=True, db_column='MaxNoHospitalizaion', null=True)),
                ('max_no_visits', models.IntegerField(blank=True, db_column='MaxNoVisits', null=True)),
                ('max_amount_consultation', models.DecimalField(blank=True, db_column='MaxAmountConsultation', decimal_places=2, max_digits=18, null=True)),
                ('max_amount_surgery', models.DecimalField(blank=True, db_column='MaxAmountSurgery', decimal_places=2, max_digits=18, null=True)),
                ('max_amount_delivery', models.DecimalField(blank=True, db_column='MaxAmountDelivery', decimal_places=2, max_digits=18, null=True)),
                ('max_amount_hospitalization', models.DecimalField(blank=True, db_column='MaxAmountHospitalization', decimal_places=2, max_digits=18, null=True)),
                ('renewal_discount_perc', models.IntegerField(blank=True, db_column='RenewalDiscountPerc', null=True)),
                ('renewal_discount_period', models.IntegerField(blank=True, db_column='RenewalDiscountPeriod', null=True)),
                ('enrolment_discount_perc', models.IntegerField(blank=True, db_column='EnrolmentDiscountPerc', null=True)),
                ('enrolment_discount_period', models.IntegerField(blank=True, db_column='EnrolmentDiscountPeriod', null=True)),
                ('share_contribution', models.DecimalField(blank=True, db_column='ShareContribution', decimal_places=2, max_digits=5, null=True)),
                ('max_policy_extra_member', models.DecimalField(blank=True, db_column='MaxPolicyExtraMember', decimal_places=2, max_digits=18, null=True)),
                ('max_policy_extra_member_ip', models.DecimalField(blank=True, db_column='MaxPolicyExtraMemberIP', decimal_places=2, max_digits=18, null=True)),
                ('max_policy_extra_member_op', models.DecimalField(blank=True, db_column='MaxPolicyExtraMemberOP', decimal_places=2, max_digits=18, null=True)),
                ('max_ceiling_policy', models.DecimalField(blank=True, db_column='MaxCeilingPolicy', decimal_places=2, max_digits=18, null=True)),
                ('max_ceiling_policy_ip', models.DecimalField(blank=True, db_column='MaxCeilingPolicyIP', decimal_places=2, max_digits=18, null=True)),
                ('max_ceiling_policy_op', models.DecimalField(blank=True, db_column='MaxCeilingPolicyOP', decimal_places=2, max_digits=18, null=True)),
                ('max_amount_antenatal', models.DecimalField(blank=True, db_column='MaxAmountAntenatal', decimal_places=2, max_digits=18, null=True)),
                ('max_no_antenatal', models.IntegerField(blank=True, db_column='MaxNoAntenatal', null=True)),
                ('ceiling_interpretation', models.CharField(blank=True, db_column='CeilingInterpretation', max_length=1, null=True)),
                ('capitation_level_1', models.CharField(blank=True, db_column='Level1', max_length=1, null=True)),
                ('capitation_level_2', models.CharField(blank=True, db_column='Level2', max_length=1, null=True)),
                ('capitation_level_3', models.CharField(blank=True, db_column='Level3', max_length=1, null=True)),
                ('capitation_level_4', models.CharField(blank=True, db_column='Level4', max_length=1, null=True)),
                ('weight_population', models.DecimalField(blank=True, db_column='WeightPopulation', decimal_places=2, max_digits=5, null=True)),
                ('weight_nb_families', models.DecimalField(blank=True, db_column='WeightNumberFamilies', decimal_places=2, max_digits=5, null=True)),
                ('weight_insured_population', models.DecimalField(blank=True, db_column='WeightInsuredPopulation', decimal_places=2, max_digits=5, null=True)),
                ('weight_nb_insured_families', models.DecimalField(blank=True, db_column='WeightNumberInsuredFamilies', decimal_places=2, max_digits=5, null=True)),
                ('weight_nb_visits', models.DecimalField(blank=True, db_column='WeightNumberVisits', decimal_places=2, max_digits=5, null=True)),
                ('weight_adjusted_amount', models.DecimalField(blank=True, db_column='WeightAdjustedAmount', decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'db_table': 'tblProduct',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('validity_from', core.fields.DateTimeField(db_column='ValidityFrom', default=datetime.datetime.now)),
                ('validity_to', core.fields.DateTimeField(blank=True, db_column='ValidityTo', null=True)),
                ('legacy_id', models.IntegerField(blank=True, db_column='LegacyID', null=True)),
                ('id', models.AutoField(db_column='ProdItemID', primary_key=True, serialize=False)),
                ('limitation_type', models.CharField(blank=True, db_column='LimitationType', max_length=1, null=True)),
                ('price_origin', models.CharField(blank=True, db_column='PriceOrigin', max_length=1, null=True)),
                ('limit_adult', models.DecimalField(blank=True, db_column='LimitAdult', decimal_places=2, max_digits=18, null=True)),
                ('limit_child', models.DecimalField(blank=True, db_column='LimitChild', decimal_places=2, max_digits=18, null=True)),
                ('waiting_period_adult', models.IntegerField(blank=True, db_column='WaitingPeriodAdult', null=True)),
                ('waiting_period_child', models.IntegerField(blank=True, db_column='WaitingPeriodChild', null=True)),
                ('limit_no_adult', models.IntegerField(blank=True, db_column='LimitNoAdult', null=True)),
                ('limit_no_child', models.IntegerField(blank=True, db_column='LimitNoChild', null=True)),
                ('limitation_type_r', models.CharField(blank=True, db_column='LimitationTypeR', max_length=1, null=True)),
                ('limitation_type_e', models.CharField(blank=True, db_column='LimitationTypeE', max_length=1, null=True)),
                ('limit_adult_r', models.DecimalField(blank=True, db_column='LimitAdultR', decimal_places=2, max_digits=18, null=True)),
                ('limit_adult_e', models.DecimalField(blank=True, db_column='LimitAdultE', decimal_places=2, max_digits=18, null=True)),
                ('limit_child_r', models.DecimalField(blank=True, db_column='LimitChildR', decimal_places=2, max_digits=18, null=True)),
                ('limit_child_e', models.DecimalField(blank=True, db_column='LimitChildE', decimal_places=2, max_digits=18, null=True)),
                ('ceiling_exclusion_adult', models.CharField(blank=True, db_column='CeilingExclusionAdult', max_length=1, null=True)),
                ('ceiling_exclusion_child', models.CharField(blank=True, db_column='CeilingExclusionChild', max_length=1, null=True)),
                ('audit_user_id', models.IntegerField(db_column='AuditUserID')),
            ],
            options={
                'db_table': 'tblProductItems',
                'managed': False,
            },
            bases=(models.Model, product.models.ProductItemOrService),
        ),
        migrations.CreateModel(
            name='ProductService',
            fields=[
                ('validity_from', core.fields.DateTimeField(db_column='ValidityFrom', default=datetime.datetime.now)),
                ('validity_to', core.fields.DateTimeField(blank=True, db_column='ValidityTo', null=True)),
                ('legacy_id', models.IntegerField(blank=True, db_column='LegacyID', null=True)),
                ('id', models.AutoField(db_column='ProdServiceID', primary_key=True, serialize=False)),
                ('limitation_type', models.CharField(db_column='LimitationType', max_length=1)),
                ('price_origin', models.CharField(db_column='PriceOrigin', max_length=1)),
                ('limit_adult', models.DecimalField(blank=True, db_column='LimitAdult', decimal_places=2, max_digits=18, null=True)),
                ('limit_child', models.DecimalField(blank=True, db_column='LimitChild', decimal_places=2, max_digits=18, null=True)),
                ('waiting_period_adult', models.IntegerField(blank=True, db_column='WaitingPeriodAdult', null=True)),
                ('waiting_period_child', models.IntegerField(blank=True, db_column='WaitingPeriodChild', null=True)),
                ('limit_no_adult', models.IntegerField(blank=True, db_column='LimitNoAdult', null=True)),
                ('limit_no_child', models.IntegerField(blank=True, db_column='LimitNoChild', null=True)),
                ('limitation_type_r', models.CharField(blank=True, db_column='LimitationTypeR', max_length=1, null=True)),
                ('limitation_type_e', models.CharField(blank=True, db_column='LimitationTypeE', max_length=1, null=True)),
                ('limit_adult_r', models.DecimalField(blank=True, db_column='LimitAdultR', decimal_places=2, max_digits=18, null=True)),
                ('limit_adult_e', models.DecimalField(blank=True, db_column='LimitAdultE', decimal_places=2, max_digits=18, null=True)),
                ('limit_child_r', models.DecimalField(blank=True, db_column='LimitChildR', decimal_places=2, max_digits=18, null=True)),
                ('limit_child_e', models.DecimalField(blank=True, db_column='LimitChildE', decimal_places=2, max_digits=18, null=True)),
                ('ceiling_exclusion_adult', models.CharField(blank=True, db_column='CeilingExclusionAdult', max_length=1, null=True)),
                ('ceiling_exclusion_child', models.CharField(blank=True, db_column='CeilingExclusionChild', max_length=1, null=True)),
                ('audit_user_id', models.IntegerField(db_column='AuditUserID')),
            ],
            options={
                'db_table': 'tblProductServices',
                'managed': False,
            },
            bases=(models.Model, product.models.ProductItemOrService),
        ),
    ]
