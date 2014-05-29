import os
import sys
gettext = lambda s: s

BASE_DIR = os.path.join( os.path.dirname(__file__), 'imagesift')

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                'NAME': os.path.join(os.path.dirname(__file__), 'test.db'),
            }
        },
        ROOT_URLCONF="imagesift.urls",
        STATIC_ROOT = os.path.join(BASE_DIR, 'static'),
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            #"django.contrib.admin",
            #"django.contrib.messages",
            "django.contrib.sites",
            #"django.contrib.staticfiles",



            'djangocms_admin_style',
            'djangocms_text_ckeditor',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.sites',
            'django.contrib.sitemaps',
            'django.contrib.staticfiles',
            'django.contrib.messages',
            'cms',
            'mptt',
            'menus',
            'south',
            'sekizai',
            'djangocms_style',
            'djangocms_column',
            'djangocms_file',
            'djangocms_flash',
            'djangocms_googlemap',
            'djangocms_inherit',
            'djangocms_link',
            'djangocms_picture',
            'djangocms_teaser',
            'djangocms_video',
            'reversion',



            "imagestore",
            "imagesift",
            'sorl.thumbnail',
            'tagging',
            #'autocomplete_light',
            'south',
            'django_nose', # after south
        ],
        TEMPLATE_CONTEXT_PROCESSORS =(
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.static",
            "django.contrib.messages.context_processors.messages",
            "django.core.context_processors.request",
            "imagestore.context_processors.imagestore_processor",
        ),
        LANGUAGES = (
            ## Customize this
            ('en', gettext('en')),
            ('en-us', gettext('en-us')),
        ),

        SITE_ID=1,
        NOSE_ARGS=['-s'],
        #SOUTH_TESTS_MIGRATE = False,

    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


class TestSuiteRunner(NoseTestSuiteRunner):
    """
    FIXME: startup south migrate here, because settings.SOUTH_TESTS_MIGRATE doesn't work.
    http://south.readthedocs.org/en/latest/unittests.html

    https://github.com/jedie/django-reversion-compare/blob/master/reversion_compare_test_project/runtests.py
    """
    def setup_databases(self, **kwargs):
        result = super(TestSuiteRunner, self).setup_databases()
        from django.core import management
        management.call_command("migrate", verbosity=self.verbosity - 1, traceback=True, interactive=False)
        return result


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = TestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])