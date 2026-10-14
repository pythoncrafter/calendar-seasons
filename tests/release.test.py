import importlib.util
import os
import plistlib
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release_config',ROOT/'scripts/configure-release.py')
config=importlib.util.module_from_spec(spec);spec.loader.exec_module(config)
ENV={'APPLE_TEAM_ID':'ABCDEFGHIJ','APP_BUNDLE_ID':'com.test.CalendarSeasons','ASC_KEY_ID':'ABCDEFGHIJ','ASC_ISSUER_ID':'11111111-2222-3333-4444-555555555555','BUILD_NUMBER':'42'}
class ReleaseTests(unittest.TestCase):
 def test_configuration(self):self.assertEqual(config.configuration(ENV),('com.test.CalendarSeasons','42'))
 def test_invalid_configuration(self):
  for key,value in [('APPLE_TEAM_ID',''),('APP_BUNDLE_ID','com.example.CalendarSeasons'),('APP_BUNDLE_ID','com.test;evil'),('BUILD_NUMBER','0'),('BUILD_NUMBER','x'),('ASC_ISSUER_ID','invalid')]:
   with self.subTest(key=key,value=value),self.assertRaises(ValueError):config.configuration({**ENV,key:value})
 def test_both_targets_and_build_number(self):
  source=(ROOT/'safari/CalendarSeasons.xcodeproj/project.pbxproj').read_text()
  rendered=config.render_project(source,'com.test.CalendarSeasons','42')
  self.assertEqual(rendered.count('PRODUCT_BUNDLE_IDENTIFIER = com.test.CalendarSeasons;'),2)
  self.assertEqual(rendered.count('PRODUCT_BUNDLE_IDENTIFIER = com.test.CalendarSeasons.Extension;'),2)
  self.assertEqual(rendered.count('CURRENT_PROJECT_VERSION = 42;'),4)
  self.assertNotIn('com.example.',rendered)
 def test_plist_build_number_follows_signing_configuration(self):
  for name in ['ios-app/Info.plist','safari/Info.plist']:
   info=plistlib.loads((ROOT/name).read_bytes());self.assertEqual(info['CFBundleVersion'],'$(CURRENT_PROJECT_VERSION)')
 def test_workflows(self):
  try:import yaml
  except ImportError:self.skipTest('Install PyYAML to parse workflow YAML.')
  for path in (ROOT/'.github/workflows').glob('*.yml'):
   workflow=yaml.load(path.read_text(),Loader=yaml.BaseLoader)
   self.assertIn('on',workflow);self.assertEqual(workflow['permissions'],{'contents':'read'})
  release=yaml.load((ROOT/'.github/workflows/testflight.yml').read_text(),Loader=yaml.BaseLoader)
  self.assertEqual(set(release['on']),{'workflow_dispatch'})
  job=release['jobs']['release'];self.assertEqual(job['environment'],'testflight')
  self.assertTrue(any('ruby -c' in step.get('run','') for step in job['steps']))
if __name__=='__main__':unittest.main()
