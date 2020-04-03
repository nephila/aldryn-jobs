# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    CategoryJobOpeningList,
    JobOpeningDetail,
    JobOpeningList,
    ConfirmNewsletterSignup,
    SuccessRegistrationMessage,
    RegisterJobNewsletter,
    UnsubscibeNewsletterSignup,
    ResendNewsletterConfirmation,
)

# default view (root url) which is pointing to ^$ url
DEFAULT_VIEW = 'job-opening-list'

urlpatterns = [
    url(r'^$', JobOpeningList.as_view(),
        name='job-opening-list'),
    url(r'^(?P<category_slug>\w[-_\w]*)/$',
        CategoryJobOpeningList.as_view(),
        name='category-job-opening-list'),
    url(r'^(?P<category_slug>\w[-_\w]*)/(?P<job_opening_slug>\w[-_\w]*)/$',
        JobOpeningDetail.as_view(),
        name='job-opening-detail'),
    url(r'^confirm-newsletter/$',
        RegisterJobNewsletter.as_view(),
        name="register_newsletter"),

    url(r'^confirm-newsletter/registration-notification/$',
        SuccessRegistrationMessage.as_view(),
        name="newsletter_registration_notification"),

    url(r'^confirm-newsletter/(?P<key>\w+)/$',
        ConfirmNewsletterSignup.as_view(),
        name="confirm_newsletter_email"),

    url(r'^unsubscribe-newsletter/(?P<key>\w+)/$',
        UnsubscibeNewsletterSignup.as_view(),
        name="unsubscribe_from_newsletter"),

    url(r'^resend-newsletter-confirmation/(?P<key>\w+)/$',
        ResendNewsletterConfirmation.as_view(),
        name="resend_confirmation_link"),
]
