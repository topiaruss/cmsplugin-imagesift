import os
import sys

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
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            #"django.contrib.sessions",
            #"django.contrib.admin",
            #"django.contrib.messages",
            "django.contrib.sites",
            #"django.contrib.staticfiles",
            "imagestore",
            "imagesift",
            'sorl.thumbnail',
            'tagging',
            #'autocomplete_light',
            'south',
            'django_nose', # after south
        ],
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