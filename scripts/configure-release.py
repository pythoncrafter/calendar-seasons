"""Configure a disposable CI checkout; never requests or stores credentials."""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def configuration(env):
    names = ['APPLE_TEAM_ID', 'APP_BUNDLE_ID', 'ASC_KEY_ID', 'ASC_ISSUER_ID', 'BUILD_NUMBER']
    missing = [name for name in names if not env.get(name)]
    if missing:
        raise ValueError('Missing GitHub Actions configuration: ' + ', '.join(missing))
    team, bundle, key, issuer, build = (env[name] for name in names)
    if not re.fullmatch(r'[A-Z0-9]{10}', team):
        raise ValueError('APPLE_TEAM_ID must be the 10-character Apple team identifier.')
    if not re.fullmatch(r'[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+){2,}', bundle) or bundle.startswith('com.example.'):
        raise ValueError('APP_BUNDLE_ID must be your registered explicit app identifier, not com.example.')
    if not re.fullmatch(r'[A-Z0-9]{10}', key):
        raise ValueError('ASC_KEY_ID must be the 10-character App Store Connect key identifier.')
    if not re.fullmatch(r'[a-fA-F0-9]{8}(?:-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}', issuer):
        raise ValueError('ASC_ISSUER_ID must be the team API-key issuer UUID.')
    if not re.fullmatch(r'[1-9][0-9]{0,5}', build):
        raise ValueError('BUILD_NUMBER must be a positive integer of at most six digits.')
    return bundle, build

def render_project(text, bundle, build):
    expected = [('PRODUCT_BUNDLE_IDENTIFIER = com.example.CalendarSeasons.Extension;',
                 f'PRODUCT_BUNDLE_IDENTIFIER = {bundle}.Extension;'),
                ('PRODUCT_BUNDLE_IDENTIFIER = com.example.CalendarSeasons;',
                 f'PRODUCT_BUNDLE_IDENTIFIER = {bundle};'),
                ('CURRENT_PROJECT_VERSION = 1;', f'CURRENT_PROJECT_VERSION = {build};')]
    for before, after in expected:
        if before not in text:
            raise ValueError('Project defaults have changed; review release configuration before signing.')
        text = text.replace(before, after)
    return text

if __name__ == '__main__':
    try:
        bundle, build = configuration(os.environ)
        if '--check' not in sys.argv:
            project = ROOT / 'safari/CalendarSeasons.xcodeproj/project.pbxproj'
            project.write_text(render_project(project.read_text(), bundle, build))
        print('Release configuration valid.' if '--check' in sys.argv else 'Disposable CI project configured.')
    except ValueError as error:
        sys.exit(str(error))
