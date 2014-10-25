#
# Conditional build:
%bcond_with	tests	# perform "make test"
%bcond_without	python2	# CPython 2.x module
%if "%{pld_release}" == "ac"
%bcond_with	python3	# CPython 3.x module
%bcond_without	pypy	# PyPy module
%else
%bcond_without	python3	# CPython 3.x module
%bcond_without	pypy	# PyPy module
%endif

%define	__pypy	/usr/bin/pypy
%define pypy_ver	%{expand:%%global pypy_ver %(%{__pypy} -c "import sys; print '{0}.{1}'.format(*sys.pypy_version_info[:2])" 2>/dev/null || echo ERROR)}%pypy_ver
%define pypy_py_ver	%{expand:%%global pypy_py_ver %(%{__python} -c "import sys; print sys.version[:3]" 2>/dev/null || echo ERROR)}%pypy_py_ver
%define pypy_libdir	%{expand:%%global pypy_libdir %(%{__pypy} -c "import sys; print sys.prefix" 2>/dev/null || echo ERROR)}%pypy_libdir
%define pypy_sitedir	%{pypy_libdir}/site-packages

%define		pname	distribute
Summary:	Easily download, build, install, upgrade, and uninstall Python packages
Summary(pl.UTF-8):	Łatwe ściąganie, budowanie, instalowanie, uaktualnianie i usuwanie pakietów Pythona
Name:		python-distribute
Version:	0.6.49
Release:	1
License:	PSF or ZPL
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/d/distribute/distribute-%{version}.tar.gz
# Source0-md5:	89e68df89faf1966bcbd99a0033fbf8e
URL:		https://pypi.python.org/pypi/distribute
%if %{with python2}
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	python-modules
%endif
%if %{with python3}
BuildRequires:	python3
BuildRequires:	python3-2to3 >= 1:3.1.1-3
BuildRequires:	python3-devel
BuildRequires:	python3-modules
%endif
%if %{with pypy}
BuildRequires:	pypy
%endif
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.523
Requires:	python-modules
Provides:	python-setuptools = 1:0.6-3
Obsoletes:	python-setuptools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Distribute is a fork of the Setuptools project.

Distribute is intended to replace Setuptools as the standard method
for working with Python module distributions.

%description -l pl.UTF-8
Distribute to odgałęzienie (fork) projektu Setuptools.

Distribute ma na celu zastąpienie Setuptools jako standardowej metody
pracy z dystrybucjami modułów Pythona.

%package -n python3-%{pname}
Summary:	Easily download, build, install, upgrade, and uninstall Python 3.x packages
Summary(pl.UTF-8):	Łatwe ściąganie, budowanie, instalowanie, uaktualnianie i usuwanie pakietów Pythona 3.x
Group:		Development/Languages/Python
Provides:	python3-setuptools = 1:0.6-3

%description -n python3-%{pname}
Distribute is a fork of the Setuptools project.

Distribute is intended to replace Setuptools as the standard method
for working with Python module distributions.

%description -n python3-%{pname} -l pl.UTF-8
Distribute to odgałęzienie (fork) projektu Setuptools.

Distribute ma na celu zastąpienie Setuptools jako standardowej metody
pracy z dystrybucjami modułów Pythona.

%package -n pypy-%{pname}
Summary:	Easily download, build, install, upgrade, and uninstall Python PyPy packages
Summary(pl.UTF-8):	Łatwe ściąganie, budowanie, instalowanie, uaktualnianie i usuwanie pakietów Pythona PyPy
Group:		Development/Languages/Python

%description -n pypy-%{pname}
Distribute is a fork of the Setuptools project.

Distribute is intended to replace Setuptools as the standard method
for working with Python module distributions.

%description -n pypy-%{pname} -l pl.UTF-8
Distribute to odgałęzienie (fork) projektu Setuptools.

Distribute ma na celu zastąpienie Setuptools jako standardowej metody
pracy z dystrybucjami modułów Pythona.

%prep
%setup -q -n %{pname}-%{version}

%build
%if %{with python2}
%{__python} setup.py \
	build -b build-2

%if %{with tests}
%{__python} setup.py test
%endif
%endif

%if %{with python3}
%{__python3} setup.py \
	build -b build-3

%if %{with tests}
%{__python3} setup.py test
%endif
%endif

%if %{with pypy}
%{__pypy} setup.py \
	build -b build-pypy

%if %{with tests}
%{__pypy} setup.py test
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} -- setup.py \
	build -b build-2 \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

# shutup check-files
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{_bindir}/easy_install
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/setuptools/*.exe
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/setuptools/tests
# reinstall files deleted by py_postclean
cp build-2/lib/setuptools/site-patch.py $RPM_BUILD_ROOT%{py_sitescriptdir}/setuptools
cp build-2/lib/setuptools/'script template'*.py $RPM_BUILD_ROOT%{py_sitescriptdir}/setuptools

# rename to avoid rpm dir-to-file conflict from upgrade from python-setuptools
egg=$(basename $RPM_BUILD_ROOT%{py_sitescriptdir}/setuptools-*.egg-info)
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/$egg $RPM_BUILD_ROOT%{py_sitescriptdir}/S${egg#?}
%endif

%if %{with python3}
%{__python3} -- setup.py \
	build -b build-3 \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%{__rm} $RPM_BUILD_ROOT%{_bindir}/easy_install
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/setuptools/*.exe
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/setuptools/tests
%endif

%if %{with pypy}
%{__pypy} -- setup.py \
	build -b build-pypy \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=1

mv $RPM_BUILD_ROOT%{pypy_libdir}/bin/easy_install $RPM_BUILD_ROOT%{_bindir}/easy_install-pypy-%{pypy_ver}
%{__rm} $RPM_BUILD_ROOT%{pypy_libdir}/bin/easy_install*
%{__rm} $RPM_BUILD_ROOT%{pypy_sitedir}/setuptools/*.exe
%{__rm} -r $RPM_BUILD_ROOT%{pypy_sitedir}/setuptools/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/easy_install-2.*
%{py_sitescriptdir}/distribute-%{version}-py*.egg-info
%{py_sitescriptdir}/Setuptools-0.6c11-py*.egg-info
%{py_sitescriptdir}/easy_install.py[co]
%{py_sitescriptdir}/pkg_resources.py[co]
%dir %{py_sitescriptdir}/_markerlib
%{py_sitescriptdir}/_markerlib/*.py[co]
%dir %{py_sitescriptdir}/setuptools
%{py_sitescriptdir}/setuptools/*.py[co]
%{py_sitescriptdir}/setuptools/script*template*.py
%{py_sitescriptdir}/setuptools/site-patch.py
%dir %{py_sitescriptdir}/setuptools/command
%{py_sitescriptdir}/setuptools/command/*.py[co]
%{py_sitescriptdir}/setuptools/command/launcher*manifest.xml
%{py_sitescriptdir}/setuptools.pth
%endif

%if %{with python3}
%files -n python3-%{pname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/easy_install-3.*
%{py3_sitescriptdir}/distribute-%{version}-py*.egg-info
%{py3_sitescriptdir}/setuptools-0.6c11-py*.egg-info
%{py3_sitescriptdir}/easy_install.py
%{py3_sitescriptdir}/pkg_resources.py
%{py3_sitescriptdir}/__pycache__/easy_install.*.py[co]
%{py3_sitescriptdir}/__pycache__/pkg_resources.*.py[co]
%dir %{py3_sitescriptdir}/_markerlib
%{py3_sitescriptdir}/_markerlib/*.py
%dir %{py3_sitescriptdir}/_markerlib/__pycache__
%{py3_sitescriptdir}/_markerlib/__pycache__/*.py[co]
%dir %{py3_sitescriptdir}/setuptools
%{py3_sitescriptdir}/setuptools/*.py
%dir %{py3_sitescriptdir}/setuptools/__pycache__
%{py3_sitescriptdir}/setuptools/__pycache__/*.py[co]
%dir %{py3_sitescriptdir}/setuptools/command
%{py3_sitescriptdir}/setuptools/command/*.py
%dir %{py3_sitescriptdir}/setuptools/command/__pycache__
%{py3_sitescriptdir}/setuptools/command/__pycache__/*.py[co]
%{py3_sitescriptdir}/setuptools/command/launcher*manifest.xml
%{py3_sitescriptdir}/setuptools.pth
%endif

%if %{with pypy}
%files -n pypy-%{pname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/easy_install-pypy*
%{pypy_sitedir}/distribute-%{version}-py*.egg-info
%{pypy_sitedir}/setuptools-0.6c11-py*.egg-info
%{pypy_sitedir}/easy_install.py*
%{pypy_sitedir}/pkg_resources.py*
%dir %{pypy_sitedir}/_markerlib
%{pypy_sitedir}/_markerlib/*.py*
%dir %{pypy_sitedir}/setuptools
%{pypy_sitedir}/setuptools/*.py*
%dir %{pypy_sitedir}/setuptools/command
%{pypy_sitedir}/setuptools/command/*.py*
%{pypy_sitedir}/setuptools/command/launcher*manifest.xml
%{pypy_sitedir}/setuptools.pth
%endif
