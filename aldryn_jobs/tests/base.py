from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.test import TransactionTestCase
from django.utils.timezone import get_current_timezone
from django.utils.translation import override

from cms import api
from cms.middleware.toolbar import ToolbarMiddleware
from cms.utils.i18n import force_language
from cms.utils import get_cms_setting

from ..models import JobsConfig, JobCategory, JobOffer


def tz_datetime(*args, **kwargs):
    """ Return datetime with arguments in UTC timezone """
    return datetime(tzinfo=get_current_timezone(), *args, **kwargs)


class JobsBaseTestCase(TransactionTestCase):

    default_category_values = {
        'en': {
            'name': 'Default category name en',
            'slug': 'default-category-name-en',
        },
        'de': {
            'name': 'Default category name de',
            'slug': 'default-category-name-de',
        },
    }
    default_job_values = {
        'en': {
            'title': 'Default job offer en',
            'slug': 'default-job-offer-en',
            'lead_in': '<p>Default job for default people! <br/> Apply now!</p>',
        },
        'de': {
            'title': 'Default job offer de',
            'slug': 'default-job-offer-de',
            'lead_in': '<p>Default job for default people! Now in German! <br/> Apply now!</p>',
        },
    }
    default_plugin_content = {
        'en': 'Awesome job details here EN',
        'de': 'Awesome German job details here DE',
    }
    plugin_values_raw = {
        'en': 'English New, revision {0}, content en',
        'de': 'German revision {0}, new content de',
    }
    offer_values_raw = {
        'en': {
            'title': 'Title revision {0} en',
            'slug': 'title-revision-{0}-en',
            'lead_in': '<p>Job revision {0}! EN</p>',
        },
        'de': {
            'title': 'Title revision {0} de',
            'slug': 'title-revision-{0}-de',
            'lead_in': '<p>Job revision {0}! DE</p>',
        },
    }
    category_values_raw = {
        'en': {
            'name': 'Revision {0} category name en',
            'slug': 'revision-{0}-category-name-en',
        },
        'de': {
            'name': 'Revision {0} category name de',
            'slug': 'revision-{0}-category-name-de',
        },
    }
    default_publication_start = {
        'publication_start': datetime.now(tz=get_current_timezone()),
    }
    default_publication_end = {
        'publication_end': datetime.now(tz=get_current_timezone()) + timedelta(days=1),
    }
    application_default_values = {
        'first_name': 'Default_first_name',
        'last_name': 'Default_last_name',
        'email': 'example@example.com',
    }
    application_values_raw = {
        'first_name': 'First_name_{0}',
        'last_name': 'Last_name_{0}',
        'email': 'example_{0}@example.com',
    }
    signup_default_values = {
        'recipient': 'initial@example.com',
        'is_verified': False,
        'is_disabled': False,
        'confirmation_key': 'default confirmation key',
    }
    signup_values_raw = {
        'confirmation_key': 'confirmation key {0}{0}{0}',
        'recipient': 'recipient_{0}@example.com'
    }

    def setUp(self):
        super(JobsBaseTestCase, self).setUp()
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.app_config = JobsConfig.objects.create(
            namespace='jobs_test_namespace'
        )
        self.default_category = self.create_default_job_category(translated=True)
        self.root_page = self.create_root_page()
        self.page = self.create_page()

        self.staff_user_password = 'staff_pw'
        self.staff_user = self.create_staff_user('staff', self.staff_user_password)
        self.super_user_password = 'super_pw'
        self.super_user = self.create_super_user('super', self.super_user_password)

    def create_root_page(self):
        root_page = api.create_page(
            'root page', self.template, self.language, published=True)
        api.create_title('de', 'root page de', root_page)
        root_page.publish('en')
        root_page.publish('de')
        return root_page.reload()

    def create_page(self):
        page = api.create_page(
            title='Jobs en',
            slug='jobs-app-en',
            template=self.template,
            language=self.language,
            published=True,
            parent=self.root_page,
            apphook='JobsApp',
            apphook_namespace=self.app_config.namespace)
        api.create_title('de', 'Jobs de', page, slug='jobs-app-de')
        page.publish('en')
        page.publish('de')
        # unfortunately aphook reload doesn't restart server fast,
        # so we do an empty request otherwise tests might
        # fail because it can't get correct url
        with override('en'):
            empty_url = page.get_absolute_url()
        self.client.get(empty_url)
        return page.reload()

    def tearDown(self):
        super(JobsBaseTestCase, self).tearDown()
        self.app_config.delete()
        cache.clear()

    def create_user(self, user_name, user_password, is_staff=False, is_superuser=False):
        return User.objects.create(
            username=user_name,
            first_name='{0} first_name'.format(user_name),
            last_name='{0} last_name'.format(user_name),
            password=make_password(user_password),
            is_staff=is_staff,
            is_superuser=is_superuser
        )

    def create_staff_user(self, user_name, user_password):
        staff_user = self.create_user(user_name, user_password, is_staff=True)
        return staff_user

    def create_super_user(self, user_name, user_password):
        super_user = self.create_user(user_name, user_password, is_superuser=True)
        return super_user

    def create_default_job_category(self, translated=False):
        # ensure that we always start with english, since it looks
        # like there is some issues with handling active language
        # between tests cases run
        with override('en'):
            job_category = JobCategory.objects.create(
                app_config=self.app_config,
                **self.default_category_values['en'])

        # check if we need a translated job_category
        if translated:
            job_category.create_translation('de', **self.default_category_values['de'])

        return JobCategory.objects.language('en').get(pk=job_category.pk)

    def create_default_job_offer(self, translated=False):
        # ensure that we always start with english, since it looks
        # like there is some issues with handling active language
        # between tests cases run
        with override('en'):
            job_offer = JobOffer.objects.create(
                category=self.default_category,
                app_config=self.app_config,
                **self.default_job_values['en'])
            api.add_plugin(
                job_offer.content,
                'TextPlugin',
                'en',
                body=self.default_plugin_content['en'])

        # check if we need a translated job offer
        if translated:
            job_offer.create_translation('de', **self.default_job_values['de'])
            with override('de'):
                api.add_plugin(job_offer.content, 'TextPlugin', 'de',
                               body=self.default_plugin_content['de'])

        return JobOffer.objects.language('en').get(pk=job_offer.pk)