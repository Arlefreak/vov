from django.db                  import models
from uuslug                     import uuslug
from datetime                   import date
from taggit.managers            import TaggableManager
from django.contrib.auth.models import User
from django_countries.fields    import CountryField
from django.utils.translation   import ugettext_lazy as _
from ordered_model.models       import OrderedModel
from solo.models                import SingletonModel
from embed_video.fields         import EmbedVideoField
from ckeditor.fields            import RichTextField
import os

def upload_image_to(instance, filename):
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return 'uploads/%s%s%s' % (
        filename_base,
        now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),)

class Product (OrderedModel):
    sku           = models.SlugField('SKU', unique=True, max_length=50, editable=False)
    name          = models.CharField('Name',default='', max_length=140)
    description   = models.TextField('Description', default='', blank=True)
    image         = models.ImageField('Main image', upload_to=upload_image_to, blank=True, null=True)
    price         = models.FloatField('Price', default=0.0)
    discount      = models.FloatField('Discount', default=0.0)
    tags          = TaggableManager(blank=True)
    category      = models.ForeignKey('Category')
    statusChoices = (('IN','In stock'),('OUT','Out of stock'))
    status        = models.CharField('Status', choices=statusChoices, max_length=3, default='OUT', editable=False)
    date          = models.DateField('Date added', auto_now_add=True)
    updated       = models.DateField('Date updated', auto_now=True)
    class Meta:
        ordering  = ['order', 'date', 'sku']
        verbose_name = 'product'
        verbose_name_plural = 'products'
    def __unicode__(self):
        return u'%s' % (self.sku)
    def __str__(self):
        return u'%s' % (self.sku)
    def save(self, *args, **kwargs):
        self.sku = uuslug(self.name, instance=self, slug_field='sku')
        variants = ProductVariant.objects.filter(product=self)
        stock = 0
        for item in variants:
            stock += item.inventory
        if( stock > 0):
            self.status = 'IN'
        else:
            self.status = 'OUT'
        super(Product, self).save(**kwargs)
    def image_img(self):
        if self.image:
            return u'<img src="%s" style="width: 100px;'\
                ' height: auto; display: block;"/>' % self.image.url
        else:
            return 'No Image'
    def stock(self):
        variants = ProductVariant.objects.filter(product=self)
        stock = 0
        for item in variants:
            stock += item.inventory
        return stock

    image_img.short_description = 'image'
    image_img.allow_tags = True

    def variants(self):
        variants = ProductVariant.objects.filter(product=self)
        if variants:
            return variants
        else:
            return 'No Variants'

class ProductVariant(OrderedModel):
    product      = models.ForeignKey('Product')
    name         = models.CharField('Name',default='', max_length=140)
    sku           = models.SlugField('SKU', unique=True, max_length=50, editable=False)
    inventory     = models.IntegerField('Inventory', default=0)
    date          = models.DateField('Date added', auto_now_add=True)
    updated       = models.DateField('Date updated', auto_now=True)
    def __unicode__(self):
        return u'%s' % (self.name)
    def __str__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.sku = uuslug(self.name, instance=self, slug_field='sku')
        super(ProductVariant, self).save(**kwargs)
    def gallery(self):
        gal = ProductImages.objects.filter(product=self)
        return gal
    def video_gallery(self):
        gal = ProductVideo.objects.filter(product=self)
        return gal
    def image(self):
        img = ProductImages.objects.filter(product=self).first()
        if(img):
            return img
        else:
            return 'No Image'
        return
    def image_img(self):
        image = ProductImages.objects.filter(product=self).first()
        if image:
            return u'<img src="%s" style="width: 100px;'\
                ' height: auto; display: block;"/>' % image.image.url
        else:
            return 'No Image'
    image_img.short_description = 'image'
    image_img.allow_tags = True

class ProductImages(OrderedModel):
    product      = models.ForeignKey('ProductVariant')
    name         = models.CharField('Name',default='', max_length=140)
    image         = models.ImageField('Image', upload_to=upload_image_to)
    date         = models.DateField('Date added', auto_now_add=True)
    updated      = models.DateField('Date updated', auto_now=True)
    order_with_respect_to = 'product'
    class Meta:
        ordering = ['order', 'date']
        verbose_name = 'image'
        verbose_name_plural = 'images'
    def __unicode__(self):
        return u'%s' % (self.image.url)
    def __str__(self):
        return u'%s' % (self.image.url)

    def image_img(self):
        if self.image:
            return u'<a href="{0}" target="_blank">\
                        <img src="{0}" \
                        style="width: 100px; height: auto; display: block;"/>\
                </a>'.format(self.image.url)
        else:
            return 'No Image'
    image_img.short_description = 'image'
    image_img.allow_tags = True

class ProductVideo(OrderedModel):
    product      = models.ForeignKey('ProductVariant')
    name        = models.CharField('Name',default='', max_length=140)
    video       = EmbedVideoField()
    date         = models.DateField('Date added', auto_now_add=True)
    updated      = models.DateField('Date updated', auto_now=True)
    class Meta:
        ordering = ['order', 'date']
        verbose_name = 'video'
        verbose_name_plural = 'video'
    def __unicode__(self):
        return u'%s' % (self.video.url)
    def __str__(self):
        return u'%s' % (self.name)
class Category(OrderedModel):
    sku          = models.SlugField('SKU', unique=True, max_length=50, editable=False)
    publish      = models.BooleanField('Publish', default=False)
    name         = models.CharField('Name',default='', max_length=140)
    description   = models.TextField('Description', default='', blank=True)
    image        = models.ImageField('Image', upload_to=upload_image_to, blank=True, null=True)
    date         = models.DateField('Date added', auto_now_add=True)
    updated      = models.DateField('Date updated', auto_now=True)
    class Meta:
        ordering = ['order', 'date']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __unicode__(self):
        return u'%s' % (self.name)
    def __str__(self):
        return u'%s' % (self.name)
    def save(self, *args, **kwargs):
        self.sku = uuslug(self.name, instance=self, slug_field='sku')
        super(Category, self).save(**kwargs)
    def image_img(self):
        if self.image:
            return u'<img src="%s" style="width: 100px;'\
                ' height: auto; display: block;"/>' % self.image.url
        else:
            return 'No Image'
    image_img.short_description = 'Image'
    image_img.allow_tags = True

class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    class Meta:
        ordering = ['user']
        verbose_name = 'client'
        verbose_name_plural = 'clients'
    def __unicode__(self):
        return u'%s' % (self.user.username)
    def __str__(self):
        return u'%s' % (self.user.username)

class ShoppingCartProduct(models.Model):
    client   = models.ForeignKey('Client')
    product  = models.ForeignKey('Product')
    cuantity = models.IntegerField()
    class Meta:
        ordering  = ['cuantity',]
        verbose_name = 'shopping cart product'
        verbose_name_plural = 'shopping cart products'
    def __unicode__(self):
        return u'%s' % (self.product.name)
    def __str__(self):
        return u'%s' % (self.product.name)
    def save(self, *args, **kwargs):
        product = ShoppingCartProduct.objects.filter(client = self.client, product = self.product)
        if(product):
            for p in product:
                self.cuantity += p.cuantity
                p.delete()
        super(ShoppingCartProduct, self).save(**kwargs)

class Order(models.Model):
    sku               = models.SlugField('SKU', unique=True, max_length=50, editable=False)
    client            = models.ForeignKey('Client')
    shippingAdress    = models.ForeignKey('Adress',limit_choices_to={'type': 'SHI'}, related_name='shippingAdress')
    billingAdress     = models.ForeignKey('Adress',limit_choices_to={'type': 'BIL'}, related_name='billingAdress')
    items_subTotal    = models.FloatField(_('Items subtotal'), default=0)
    shipping_cost     = models.FloatField(_('Shipping cost'), default=0)
    taxes_cost        = models.FloatField(_('Taxes costs'), default =0)
    total             = models.FloatField(_('Total'), default=0)
    shipping_carrier  = models.CharField(_('Shipping carrier'), max_length=50)
    shipping_tracking = models.CharField(_('Shipping tracking numer'), max_length=50)
    date              = models.DateField('Date placed', auto_now_add=True)
    updated           = models.DateField('Date updated', auto_now=True)
    statusChoices     = (('PRO','processing'),('SHI','shipped'),('COM','complete'))
    status            = models.CharField(_('status'), choices=statusChoices, max_length=3, default='PRO', editable=False)
    class Meta:
        ordering  = ['date', 'sku']
        verbose_name = 'order'
        verbose_name_plural = 'orders'
    def __unicode__(self):
        return u'%s' % (self.sku)
    def __str__(self):
        return u'%s' % (self.sku)
    def save(self, *args, **kwargs):
        tmp = "%s%i%i%i" % (self.client.user.username[:3], date.today().day, date.today().month, date.today().year)
        self.sku = uuslug(tmp, instance=self, slug_field='sku')
        super(Order, self).save(**kwargs)

class OrderProduct(models.Model):
    product  = models.ForeignKey('Product')
    cuantity = models.IntegerField()
    class Meta:
        ordering  = ['cuantity',]
        verbose_name = 'order product'
        verbose_name_plural = 'order products'
    def __unicode__(self):
        return u'%s' % (self.product.name)
    def __str__(self):
        return u'%s' % (self.product.name)

class Adress(models.Model):
    client         = models.ForeignKey('Client')
    name           = models.CharField('Name',default='', max_length=140)
    typeChoices    = (('BIL','Billing'),('SHI', 'Shipping'))
    type           = models.CharField('Type', choices=typeChoices, max_length=3, default='BIL')
    default        = models.BooleanField()
    firstname      = models.CharField(_('Firstname'), max_length=50)
    lastname       = models.CharField(_('Lastname'), max_length=50)
    adress_line1   = models.CharField(_('Address 1'), max_length=140)
    adress_line2   = models.CharField(_('Address 2'), max_length=140, blank=True)
    city           = models.CharField(_('City'), max_length=50)
    state_province = models.CharField(_('State/Providence'), max_length=50)
    country        = CountryField()
    zipcode        = models.CharField(_('ZIP code'), max_length=32)
    phone_number   = models.CharField(_('Phone number'), max_length=40)
    date           = models.DateField('Date added', auto_now_add=True)
    class Meta:
        ordering = ['client','default', 'date', 'name']
        verbose_name = 'adress'
        verbose_name_plural = 'adresses'
    def __unicode__(self):
        return u'%s - %s' % (self.client,self.name)
    def __str__(self):
        return u'%s - %s' % (self.client,self.name)
    def save(self, *args, **kwargs):
        if self.default:
            Adress.objects.filter(default=True,type=self.type,client=self.client).update(default=False)
        super(Adress, self).save(*args, **kwargs)

class Transaction(models.Model):
    card        = models.CharField(_('Token'), max_length=50)

class Store(SingletonModel):
    name = models.CharField('Name',default='', max_length=140)
    small_description = models.CharField('Small description', default='', max_length=140)
    big_description = RichTextField('Description', default='')
    mail = models.EmailField('Email',default='', blank=True)
    phone = models.CharField('Phone',default='', max_length=140, blank=True)
    instagram = models.CharField('Instagram', default='', max_length=140,blank=True)
    facebook = models.CharField('Facebook', default='', max_length=140, blank=True)
    twitter = models.CharField('Twitter', default='', max_length=140, blank=True)
    class Meta:
        verbose_name = 'VOV'
        verbose_name_plural = 'VOV'
    def __unicode__(self):
        return u'%s' % (self.name)
    def __str__(self):
        return u'%s' % (self.name)

class StoreImage(OrderedModel):
    store = models.ForeignKey('Store')
    name  = models.CharField('Name',default='', max_length=140)
    image = models.ImageField('Image', upload_to=upload_image_to)
    date  = models.DateField('Date added', auto_now_add=True)
    updated = models.DateField('Date updated', auto_now=True)
    class Meta:
        ordering = ['order', 'date']
        verbose_name = 'image'
        verbose_name_plural = 'images'
    def __unicode__(self):
        return u'%s' % (self.image.url)
    def __str__(self):
        return u'%s' % (self.image.url)
    def image_img(self):
        if self.image:
            return u'<img src="%s" style="width: 100px;'\
                ' height: auto; display: block;"/>' % self.image.url
        else:
            return 'No Image'
    image_img.short_description = 'image'
    image_img.allow_tags = True

class Press (OrderedModel):
    slug          = models.SlugField('Slug', unique=True, max_length=50, editable=False)
    publish       = models.BooleanField('Publish', default=False)
    title         = models.CharField('Title',default='', max_length=140)
    text          = models.TextField('Text', default='', blank=True)
    date_article  = models.DateField('Date article')
    date          = models.DateField('Date added', auto_now_add=True)
    updated       = models.DateField('Date updated', auto_now=True)
    class Meta:
        ordering  = ['order', 'date_article', 'slug']
        verbose_name = 'press'
        verbose_name_plural = 'press items'
    def __unicode__(self):
        return u'%s' % (self.slug)
    def __str__(self):
        return u'%s' % (self.slug)
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self, slug_field='slug')
        super(Press, self).save(**kwargs)
    def gallery(self):
        gal = PressImage.objects.filter(press=self)
        return gal
    def videos(self):
        vids =  VideoPress.objects.filter(press=self)
        return vids

class PressImage(OrderedModel):
    press      = models.ForeignKey('Press')
    name         = models.CharField('Name',default='', max_length=140)
    image         = models.ImageField('Image', upload_to=upload_image_to)
    date         = models.DateField('Date added', auto_now_add=True)
    updated      = models.DateField('Date updated', auto_now=True)
    class Meta:
        ordering = ['order', 'date']
        verbose_name = 'image'
        verbose_name_plural = 'images'
    def __unicode__(self):
        return u'%s' % (self.image.url)
    def __str__(self):
        return u'%s' % (self.image.url)
    def image_img(self):
        if self.image:
            return u'<img src="%s" style="width: 100px;'\
                ' height: auto; display: block;"/>' % self.image.url
        else:
            return 'No Image'
    image_img.short_description = 'image'
    image_img.allow_tags = True

class VideoPress(OrderedModel):
    press      = models.ForeignKey('Press')
    name         = models.CharField('Name',default='', max_length=140)
    video       = EmbedVideoField()
    date         = models.DateField('Date added', auto_now_add=True)
    updated      = models.DateField('Date updated', auto_now=True)
    class Meta:
        ordering = ['order', 'date']
        verbose_name = 'video'
        verbose_name_plural = 'video'
    def __unicode__(self):
        return u'%s' % (self.video.url)
    def __str__(self):
        return u'%s' % (self.name)

class Stores(OrderedModel):
    publish = models.BooleanField('Publish', default=False)
    slug = models.SlugField('Slug', unique=True, max_length=50, editable=False)
    name = models.CharField('Name',default='', max_length=140)
    adress = models.CharField('Adress',default='', max_length=500, blank=True)
    mail = models.EmailField('Email',default='', blank=True)
    phone = models.CharField('Phone',default='', max_length=140, blank=True)
    notes = models.CharField('Notes',default='', max_length=500, blank=True)
    date = models.DateField('Date added', auto_now_add=True, blank=True)
    class Meta:
        ordering  = ['order', 'date', 'slug']
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
    def __unicode__(self):
        return u'%s' % (self.slug)
    def __str__(self):
        return u'%s' % (self.slug)
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self, slug_field='slug')
        super(Stores, self).save(**kwargs)
