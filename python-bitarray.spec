
# TODO:
#	- tests fail under Python 3.5
#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # Python 3.x module
%bcond_without	python3 # Python 3.x module

%define		module	bitarray
Summary:	Efficient arrays of booleans -- C extension
Name:		python-%{module}
Version:	0.8.1
Release:	5
License:	PSF
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/b/bitarray/%{module}-%{version}.tar.gz
# Source0-md5:	3825184f54f4d93508a28031b4c65d3b
URL:		https://pypi.python.org/pypi/bitarray/
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.710
# when python3 present
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
Requires:	python-libs
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module provides an object type which efficiently represents an
array of booleans. Bitarrays are sequence types and behave very much
like usual lists. Eight bits are represented by one byte in a
contiguous block of memory. The user can select between two
representations; little-endian and big-endian. All of the
functionality is implemented in C. Methods for accessing the machine
representation are provided. This can be useful when bit level access
to binary files is required, such as portable bitmap image files
(.pbm). Also, when dealing with compressed data which uses variable
bit length encoding, you may find this module useful.

%package apidoc
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidoc
API documentation for %{module}.

%description apidoc -l pl.UTF-8
Dokumentacja API %{module}.

%package -n python3-%{module}
Summary:	Efficient arrays of booleans -- C extension
Group:		Libraries/Python
Requires:	python3-libs
Requires:	python3-modules

%description -n python3-%{module}
This module provides an object type which efficiently represents an
array of booleans. Bitarrays are sequence types and behave very much
like usual lists. Eight bits are represented by one byte in a
contiguous block of memory. The user can select between two
representations; little-endian and big-endian. All of the
functionality is implemented in C. Methods for accessing the machine
representation are provided. This can be useful when bit level access
to binary files is required, such as portable bitmap image files
(.pbm). Also, when dealing with compressed data which uses variable
bit length encoding, you may find this module useful.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test --test-suite bitarray}
%endif
%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%if %{with python3}
%py3_install
%endif

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGE_LOG README.rst TODO
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/bitarray-*.egg-info
%{_examplesdir}/%{name}-%{version}

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGE_LOG README.rst TODO
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py*
%{py3_sitedir}/%{module}/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidoc
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
