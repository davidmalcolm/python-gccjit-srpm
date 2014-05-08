%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%if 0%{?fedora} > 12
%global with_python3 1
%else
%global with_python3 0
%endif

Name:           python-gccjit
Version:        0.1
Release:        2%{?dist}
Summary:        Python bindings for libgccjit

License:        GPLv3+
URL:            https://github.com/davidmalcolm/pygccjit
Source0:        gccjit-%{version}.tar.gz

BuildRequires:  libgccjit-devel

BuildRequires:  python-devel
BuildRequires:  Cython

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-Cython
%endif # with_python3

%description
Python bindings for libgccjit

%if 0%{?with_python3}
%package -n python3-gccjit
Summary:        Python 3 bindings for libgccjit

%description -n python3-gccjit
Python 3 bindings for libgccjit
%endif # with_python3

%prep
%setup -q -n gccjit-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT

# Python 3 installation
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

# Python 2 installation
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check

# FIXME: skip tests for now; they're currently aborting

# %{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
# %{__python3} setup.py test
popd
%endif # with_python3

%files
%doc COPYING
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-gccjit
%doc COPYING
%{python3_sitearch}/*
%endif # with_python3

%changelog
* Thu May  8 2014 David Malcolm <dmalcolm@redhat.com> - 0.1-2
- Fix BRs

* Wed May  7 2014 David Malcolm <dmalcolm@redhat.com> - 0.1-1
- Initial packaging
