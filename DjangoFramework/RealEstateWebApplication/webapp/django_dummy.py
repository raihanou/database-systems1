from djongo import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        abstract = True

class Entry(models.Model):
    _id = models.ObjectIdField()
    blog = models.EmbeddedField(
        model_container=Blog
    )
    
    headline = models.CharField(max_length=255)    
    objects = models.DjongoManager()

e = Entry.objects.create(
    headline='h1',
    blog={
        'name': 'b1',
        'tagline': 't1'
    })

g = Entry.objects.get(headline='h1')
assert e == g

e = Entry()
e.blog = {
    'name': 'b2',
    'tagline': 't2'
}
e.headline = 'h2'
e.save()