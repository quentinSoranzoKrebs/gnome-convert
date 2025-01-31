pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'gconvert'
gnome = import('gnome')


python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)


subdir('widgets')

gconvert_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'filters.py',
  'utils.py',
  'filemanager.py'
]


install_data(gconvert_sources, install_dir: moduledir)
