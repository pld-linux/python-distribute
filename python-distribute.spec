#
# Conditional build:
%bcond_with		tests	# perform "make test"
%bcond_without	python2
%if "%{pld_release}" == "ac"
%bcond_with	python3
%bcond_without	pypy
%else
%bcond_without	python3
%bcond_without	pypy
%endif

%define	__pypy	/usr/bin/pypy
%define pypy_ver	%{expand:%%global pypy_ver %(%{__pypy} -c "import sys; print '{0}.{1}'.format(*sys.pypy_version_info[:2])" 2>/dev/null || echo ERROR)}%pypy_ver
%define pypy_py_ver	%{expand:%%global pypy_py_ver %(%{__python} -c "import sys; print sys.version[:3]" 2>/dev/null || echo ERROR)}%pypy_py_ver
%define pypy_libdir	%{expand:%%global pypy_libdir %(%{__pypy} -c "import sys; print sys.prefix" 2>/dev/null || echo ERROR)}%pypy_libdir
%define pypy_sitedir	%{pypy_libdir}/site-packages

%define		pname	distribute
Summary:	Easily download, build, install, upgrade, and uninstall Python packages
Name:		python-distribute
Version:	0.6.19
Release:	3
License:	PSF or ZPL
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/d/distribute/distribute-%{version}.tar.gz
# Source0-md5:	45a17940eefee849d4cb8cc06d28d96f
URL:		http://pypi.python.org/pypi/distribute
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
Provides:	python-setuptools = 1:0.6-3
Obsoletes:	python-setuptools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Distribute is a fork of the Setuptools project.

Distribute is intended to replace Setuptools as the standard method
for working with Python module distributions.

%package -n python3-%{pname}
Summary:	Easily download, build, install, upgrade, and uninstall Python packages
Group:		Development/Languages/Python

%description -n python3-%{pname}
Distribute is a fork of the Setuptools project.

Distribute is intended to replace Setuptools as the standard method
for working with Python module distributions.

%package -n pypy-%{pname}
Summary:	Easily download, build, install, upgrade, and uninstall Python packages
Group:		Development/Languages/Python

%description -n pypy-%{pname}
Distribute is a fork of the Setuptools project.

Distribute is intended to replace Setuptools as the standard method
for working with Python module distributions.

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
rm $RPM_BUILD_ROOT%{_bindir}/easy_install
rm $RPM_BUILD_ROOT%{py_sitescriptdir}/setuptools/*.exe
rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/setuptools/tests
# reinstall site.py deleted by py_postclean
cp build-2/lib/site.py $RPM_BUILD_ROOT%{py_sitescriptdir}/site.py

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

rm $RPM_BUILD_ROOT%{_bindir}/easy_install
rm $RPM_BUILD_ROOT%{py3_sitescriptdir}/setuptools/*.exe
rm -rf $RPM_BUILD_ROOT%{py3_sitescriptdir}/setuptools/tests
%endif

%if %{with pypy}
%{__pypy} -- setup.py \
	build -b build-pypy \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=1

rm $RPM_BUILD_ROOT%{pypy_sitedir}/setuptools/*.exe
rm -rf $RPM_BUILD_ROOT%{pypy_sitedir}/setuptools/tests
mv $RPM_BUILD_ROOT%{pypy_libdir}/bin/easy_install $RPM_BUILD_ROOT%{_bindir}/easy_install-pypy-%{pypy_ver}
rm $RPM_BUILD_ROOT%{pypy_libdir}/bin/easy_install*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/easy_install-2.*
%{py_sitescriptdir}/distribute-%{version}-py*.egg-info
%{py_sitescriptdir}/Setuptools-*.egg-info
%dir %{py_sitescriptdir}/setuptools
%dir %{py_sitescriptdir}/setuptools/command
%{py_sitescriptdir}/site.py
%{py_sitescriptdir}/setuptools.pth
%{py_sitescriptdir}/pkg_resources.py[co]
%{py_sitescriptdir}/easy_install.py[co]
%{py_sitescriptdir}/site.py[co]
%{py_sitescriptdir}/setuptools/*.py[co]
%{py_sitescriptdir}/setuptools/command/*.py[co]
%endif

%if %{with python3}
%files -n python3-%{pname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/easy_install-3.*
%{py3_sitescriptdir}/distribute-%{version}-py*.egg-info
%{py3_sitescriptdir}/setuptools-*.egg-info
%dir %{py3_sitescriptdir}/setuptools
%dir %{py3_sitescriptdir}/setuptools/command
%{py3_sitescriptdir}/site.py
%{py3_sitescriptdir}/setuptools.pth
%dir %{py3_sitescriptdir}/__pycache__
%{py3_sitescriptdir}/pkg_resources.py
%{py3_sitescriptdir}/__pycache__/pkg_resources.*.py[co]
%{py3_sitescriptdir}/easy_install.py
%{py3_sitescriptdir}/__pycache__/easy_install.*.py[co]
%{py3_sitescriptdir}/__pycache__/site.*.py[co]
%dir %{py3_sitescriptdir}/setuptools/__pycache__
%{py3_sitescriptdir}/setuptools/*.py
%{py3_sitescriptdir}/setuptools/__pycache__/*.py[co]
%dir %{py3_sitescriptdir}/setuptools/command/__pycache__
%{py3_sitescriptdir}/setuptools/command/*.py
%{py3_sitescriptdir}/setuptools/command/__py[co]ache__/*.py[co]
%endif

%if %{with pypy}
%files -n pypy-%{pname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/easy_install-pypy*
%{pypy_sitedir}/distribute-%{version}-py*.egg-info
%{pypy_sitedir}/setuptools-*.egg-info
%dir %{pypy_sitedir}/setuptools
%dir %{pypy_sitedir}/setuptools/command
%{pypy_sitedir}/site.py*
%{pypy_sitedir}/setuptools.pth
%{pypy_sitedir}/pkg_resources.py*
%{pypy_sitedir}/easy_install.py*
%{pypy_sitedir}/setuptools/*.py*
%{pypy_sitedir}/setuptools/command/*.py*
%endif
