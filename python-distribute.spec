%bcond_with	tests	# enble tests
#
%define		pname	distribute
Summary:	Easily download, build, install, upgrade, and uninstall Python packages
Name:		python-distribute
Version:	0.6.9
Release:	1
License:	PSF or ZPL
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/d/distribute/distribute-%{version}.tar.gz
# Source0-md5:	5b1a2fde063a361aa241f98e0f9e1931
URL:		http://pypi.python.org/pypi/distribute
BuildRequires:  python
BuildRequires:	python-modules
BuildRequires:	python-devel
BuildRequires:	rpm-build-macros >= 1.523
Provides:	python-setuptools = 1:0.6-3
Obsoletes:	python-setuptools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Distribute is a fork of the Setuptools project.

Distribute is intended to replace Setuptools as the standard method for working
with Python module distributions.
 
%prep
%setup -q -n %{pname}-%{version}

%build
python setup.py \
	build

%if %{with tests}
python setup.py test
%endif

%install
rm -rf $RPM_BUILD_ROOT
python -- setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

# shutup check-files
%py_postclean
rm $RPM_BUILD_ROOT%{_bindir}/easy_install
rm $RPM_BUILD_ROOT%{py_sitescriptdir}/setuptools/*.exe
rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/setuptools/tests
# reinstall site.py deleted by py_postclean
cp site.py $RPM_BUILD_ROOT%{py_sitescriptdir}/site.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc *.txt docs
%attr(755,root,root) %{_bindir}/easy_install-2.*
%{py_sitescriptdir}/*.egg-info
%dir %{py_sitescriptdir}/setuptools
%dir %{py_sitescriptdir}/setuptools/command
%{py_sitescriptdir}/pkg_resources.py[co]
%{py_sitescriptdir}/easy_install.py[co]
%{py_sitescriptdir}/site.py
%{py_sitescriptdir}/site.py[co]
%{py_sitescriptdir}/setuptools.pth
%{py_sitescriptdir}/setuptools/*.py[co]
%{py_sitescriptdir}/setuptools/command/*.py[co]
