from django.core.urlresolvers import reverse
from django.contrib import sitemaps


class StaticPagesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'about', ]

    def location(self, item):
        return reverse(item)



sitemaps_dict = {
    'static': StaticPagesSitemap,
}

