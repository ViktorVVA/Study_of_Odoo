{
    'name': 'My theme',
    'description': 'Create a theme.',
    'version': '1.0',
    'author': 'Viktor',
    'category': 'Theme/Creative',

    'depends': ['website', ],
    'data': [
        # 'views/assets.xml',
        'views/layout.xml',
        'views/pages.xml',
        'views/options.xml',
        'views/snippets.xml',


    ],
        'assets': {
        'web.assets_frontend': [
            'theme_tutorial/static/scss/style.scss',
        ],
        'web._assets_primary_variables': [
            "/theme_tutorial/static/scss/primary_variables.scss",
        ],
        'web._assets_frontend_helpers': [
            "/theme_tutorial/static/scss/bootstrap_overridden.scss",
        ],
        'website.assets_editor': [
            'theme_tutorial/static/js/tutorial_editor.js',
        ],
    },

    'installable': True,
    'auto_install': False,

}