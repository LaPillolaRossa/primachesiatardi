from django.contrib.sitemaps import Sitemap
from news.models import Articolo


class NewsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Articolo.objects.all()

    #def lastmod(self, obj):
        #return obj.pub_date