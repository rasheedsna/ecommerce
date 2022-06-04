import uuid
from django.db import models
from django.utils.text import slugify


def generate_unique_slug(model_class, field, instance=None):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`
    :param `klass` is Class model.
    :param `field` is specific field for title.
    :param `instance` is instance object for excluding specific object.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    if instance is not None:
        while model_class.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
            unique_slug = '%s-%d' % (origin_slug, numb)
            numb += 1
    else:
        while model_class.objects.filter(slug=unique_slug).exists():
            unique_slug = '%s-%d' % (origin_slug, numb)
            numb += 1
    return unique_slug


class Type(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        ordering = ('type',)
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

    def __str__(self):
        return '{}'.format(self.type)


class Category(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='product', blank=True)

    class Meta:
        ordering = ('parent',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}'.format(self.parent)


class SubCategory(models.Model):
    children = models.CharField(max_length=100)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='children')

    class Meta:
        ordering = ('children',)
        verbose_name = 'Sub-Category'
        verbose_name_plural = 'Sub-Categories'

    def __str__(self):
        return '{}'.format(self.children)


class Product(models.Model):
    STATUS_CHOICES = [
        ('Show', 'Show'),
        ('Hide', 'Hide')
    ]

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250, blank=True)
    image = models.ImageField(upload_to='product', blank=True)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)
    children = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True)
    SKU = models.CharField(max_length=50, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='Show',)
    quantity = models.IntegerField()
    popular = models.BooleanField(default=False,)
    originalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    flashSale = models.BooleanField(default=False, )
    slug = models.SlugField(max_length=200, unique=True)
    unit = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Product, self.title)
        else:  # create
            self.slug = generate_unique_slug(Product, self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return '{}'.format(self.title)


class Tag(models.Model):
    tag = models.CharField(max_length=100)
    product = models.ManyToManyField(Product, related_name='tags')

    class Meta:
        ordering = ('tag',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return '{}'.format(self.tag)

