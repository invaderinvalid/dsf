from django.db import migrations, models

def add_default_channel_description(apps, schema_editor):
    TrendAnalysis = apps.get_model('trend_analysis', 'TrendAnalysis')
    for analysis in TrendAnalysis.objects.all():
        analysis.channel_description = ''
        analysis.save()

class Migration(migrations.Migration):

    dependencies = [
        ('trend_analysis', '0001_initial'),  # Replace '0001_initial' with the actual previous migration file name
    ]

    operations = [
        migrations.AddField(
            model_name='trendanalysis',
            name='channel_description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.RunPython(add_default_channel_description),
    ]
