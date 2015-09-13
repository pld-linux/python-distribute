#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

%define		pname	distribute
Summary:	distribute compatibility wrapper for setuptools
Summary(pl.UTF-8):	Nakładka na python-setuptools zastępujące distribute
Name:		python-distribute
Version:	0.7.3
Release:	2
License:	PSF or ZPL
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/d/distribute/distribute-%{version}.zip
# Source0-md5:	c6c59594a7b180af57af8a0cc0cf5b4a
URL:		https://pypi.python.org/pypi/distribute
%if %{with python2}
BuildRequires:	python-setuptools > 7.0
BuildConflicts:	python-distribute < 0.7
%endif
%if %{with python3}
BuildRequires:	python3-setuptools > 7.0
BuildConflicts:	python3-distribute < 0.7
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.523
Requires:	python-setuptools > 7.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Distribute was a fork of the Setuptools project. This package replaces
this fork with current Setuptools wrapper.

%description -l pl.UTF-8
Distribute było odgałęzieniem (forkiem) projektu Setuptools. Teraz
jest tylko nakładką na współczesne Setuptools.

%package -n python3-%{pname}
Summary:	Easily download, build, install, upgrade, and uninstall Python 3.x packages
Summary(pl.UTF-8):	Łatwe ściąganie, budowanie, instalowanie, uaktualnianie i usuwanie pakietów Pythona 3.x
Group:		Development/Languages/Python
Provides:	python3-setuptools = 1:0.6-3

%description -n python3-%{pname}
Distribute was a fork of the Setuptools project. This package replaces
this fork with current Setuptools wrapper.

%description -n python3-%{pname} -l pl.UTF-8
Distribute było odgałęzieniem (forkiem) projektu Setuptools. Teraz
jest tylko nakładką na współczesne Setuptools.

%prep
%setup -q -n %{pname}-%{version}

%build
%if %{with python2}
%{__python} setup.py \
	build -b build-2
%endif

%if %{with python3}
%{__python3} setup.py \
	build -b build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} -- setup.py \
	build -b build-2 \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
%py_postclean
%endif

%if %{with python3}
%{__python3} -- setup.py \
	build -b build-3 \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/distribute-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pname}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/distribute-%{version}-py*.egg-info
%endif
