# Generated by Django 2.2.4 on 2019-10-03 09:22

from django.db import migrations, transaction
from django.db.models import Count


def remove_duplicated_attribute_values(apps, schema_editor):
    """Remove duplicated attribute values.

    Before this migration Saleor allows create many attribute values with the same slug
    and different names(eg.Names  `Orange` and `ORANGE` give the same slug `orange`).
    After this migration values for each attribute should have a unique slug.
    Before removing these duplicated values we need to assign proper values
    to all `Product` and `ProductVariant` witch use duplicated values.
    """
    AttributeValue = apps.get_model("product", "AttributeValue")
    duplicated_pk_for_attribute_values = (
        AttributeValue.objects.values("slug", "attribute")
        .order_by()
        .annotate(count_id=Count("id"))
        .filter(count_id__gt=1)
    )
    for duplicated_pk_for_attribute_value in duplicated_pk_for_attribute_values:
        attribute_values = AttributeValue.objects.filter(
            attribute=duplicated_pk_for_attribute_value["attribute"],
            slug=duplicated_pk_for_attribute_value["slug"],
        )
        final_value = attribute_values[0]
        values_to_be_removed = attribute_values[1:]
        with transaction.atomic():
            for value_to_be_removed in values_to_be_removed:
                invalid_assigned_attributes = list(
                    value_to_be_removed.assignedvariantattribute_set.all()
                )
                invalid_assigned_attributes.extend(
                    list(value_to_be_removed.assignedproductattribute_set.all())
                )
                for invalid_assigned_attribute in invalid_assigned_attributes:
                    invalid_assigned_attribute.values.remove(value_to_be_removed)
                    invalid_assigned_attribute.values.add(final_value)
            ids_to_be_removed = values_to_be_removed.values_list("id", flat=True)
            AttributeValue.objects.filter(id__in=ids_to_be_removed).delete()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [("product", "0107_attributes_map_to_m2m")]

    operations = [
        migrations.RunPython(
            remove_duplicated_attribute_values, migrations.RunPython.noop
        ),
        migrations.AlterUniqueTogether(
            name="attributevalue", unique_together={("slug", "attribute")}
        ),
    ]
