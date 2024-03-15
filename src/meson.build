pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'gconvert'
gnome = import('gnome')

gnome.compile_resources('gconvert',
  'gconvert.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

pillow_dep = dependency('python3', modules: 'PIL')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'gconvert.in',
  output: 'gconvert',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

gconvert_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'test.py',
]


install_data(gconvert_sources, install_dir: moduledir)
