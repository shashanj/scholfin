"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from scholarships import views
from scholarships import sorting
from scholarships import gov_pri_comp
from scholarships.sitemaps import ScholarshipSitemap
from scholarships.rssfeed import *
from scholfin import settings

from django.conf.urls.i18n import i18n_patterns

sitemaps = {
    'scholarships' : ScholarshipSitemap()
}
urlpatterns = i18n_patterns(
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url("^admin/", include(admin.site.urls)),
)
urlpatterns += [
    url(r'^home/next=(?P<next>[a-z,A-Z,0-9-/]+)$', views.index_organic , name='index_organic' ),
    url(r'^$', views.index , name='index' ),
    url(r'^login/' , views.login_page , name='login'),
    url(r'^logins/next=(?P<next>[a-z,A-Z,0-9-/]+)/$' , views.login_page_organic , name='loginorganic'),
    url(r'^forgotpassword/' , views.forgot_password , name='forgotpassword'),
    url(r'^changePassword/' , views.change_password , name='changePassword'),
    url(r'^signup/next=(?P<next>[a-z,A-Z,0-9-/]+)/$' , views.signup_organic , name='signup_organic'),
    url(r'^signup/' , views.signup , name='signup'),
    url(r'^fbsignup/' , views.fbsignup , name='fbsignup'),
    url(r'^fbsignups/next=(?P<next>[a-z,A-Z,0-9-/]+)/$' , views.fbsignup_organic , name='fbsignup_organic'),
    url(r'^googlesignup_process/' , views.googlesignup_process , name='googlesignup_process'),
    url(r'^googlesignup_processs/next=(?P<next>[a-z,A-Z,0-9-/]+)/$' , views.googlesignup_process_organic , name='googlesignup_process_organic'),
    url(r'^fbsignup_process/' , views.fbsignup_process , name='fbsignup_process'),
    url(r'^fbsignup_processs/next=(?P<next>[a-z,A-Z,0-9-/]+)/$' , views.fbsignup_process_organic , name='fbsignusp_process'),
    url(r'^signup-completes/next=(?P<next>[a-z,A-Z,0-9-/]+)/$' , views.signup_complete_organic , name='signup_complete_organic'),
    url(r'^signup-complete/' , views.signup_complete , name='signup_complete'),
    url(r'^a78shfbwifhbiwh324b2r2kjvr3h4brl3hb4r13hbrl/', include(admin.site.urls)),
    url(r'^signupdone/next=(?P<next>[a-z,A-Z,0-9-/]+)/$' , views.signupprocess_organic , name='signup_organics'),
    url(r'^signupprocess/' , views.signupprocess , name='signup'),
    url(r'^dashboard/',views.dashboard , name='dashboard'),
    url(r'^logout/',views.logout_user , name='logout'),
    url(r'^scholarships/government/' ,gov_pri_comp.gov , name='government'),
    url(r'^scholarships/private/' ,gov_pri_comp.pri , name='private'),
    url(r'^scholarships/abroad/' ,sorting.abroad_only , name='abroad'),
    url(r'^scholarships/india/' ,sorting.india_only , name='india'),
    url(r'^scholarships/competitions/' ,gov_pri_comp.comp , name='competition'),
    url(r'^scholarship-details/(?P<scholarship_name>[a-z,A-Z,0-9-]+)/$', views.detail,name='detail'),
    url(r'^scholarships/state/(?P<scholarship_state>[a-z,A-Z -]+)/$', sorting.state_only, name='states'),
    url(r'^scholarships/interests/$', sorting.interest_only, name='interests'),
    url(r'^scholarships/caste/$', sorting.caste_only , name='caste'),
    url(r'^scholarships/religion/$', sorting.religion_only , name='religion'),
    url(r'^profile/$', views.profilepage , name='profile'),
    url(r'^profilechange/$', views.profilechange , name='profilechange'),
    url(r'^sitemap\.xml$','django.contrib.sitemaps.views.sitemap',{'sitemaps':sitemaps}),
    url(r'^rssfeed/$', LatestEntriesFeed()),
    url(r'^atom/$', AtomSiteNewsFeed()),
    url(r'^contact_us/$', views.contact_us , name='contact_us'),
    url(r'^about_us/$',views.about_us),
    url(r'^old_scholarship/$',views.old_scholarship, name='old_scholarship'),
    url(r'^internship/$',views.internship,name='internship'),
    url(r'^apply/vnit-aa/$',views.apply_aa,name='vnitalumni'),
    url(r'^reset/$',views.resetnexturl,name='reset'),
    url(r'^apply/(?P<scholarship_name>[a-z,A-Z,0-9-]+)/$',views.apply,name='apply'),
    url(r'^a78shfbwifhbiwh324b2r2kjvr3h4brl3hb4r13hbrl/custom_admin/', include('custom_admin.urls'), name='custom_admin'),
    url(r'^provider/', include('provider.urls'), name='provider'),
    url(r'^api/', include('api.urls'), name='api'),
    url(r'^submit-application/', views.submit, name='submit'),
    url(r'^searchsch/', views.schresult, name='result'),

]


from django.views.i18n import set_language

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings






if settings.USE_MODELTRANSLATION:
    urlpatterns += [
        url('^i18n/$', set_language, name='set_language'),
    ]

urlpatterns += [
    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    url("^blog/$", direct_to_template, {"template": "index.html"}, name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part.
    # Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html"
    # should be used if you want to customize the homepage's template.
    # NOTE: Don't forget to import the view function too!

    # url("^$", mezzanine.pages.views.page, {"slug": "/"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.
    # NOTE: Don't forget to import the view function too!

    # url("^$", mezzanine.blog.views.blog_post_list, name="home"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    url("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # You can also mount all of Mezzanine's urlpatterns under a
    # URL prefix if desired. When doing this, you need to define the
    # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
    # SITE_PREFIX = "my/site/prefix"
    # For convenience, and to avoid repeating the prefix, use the
    # commented out pattern below (commenting out the one above of course)
    # which will make use of the ``SITE_PREFIX`` setting. Make sure to
    # add the import ``from django.conf import settings`` to the top
    # of this file as well.
    # Note that for any of the various homepage patterns above, you'll
    # need to use the ``SITE_PREFIX`` setting as well.

    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

]

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
