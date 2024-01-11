%global pypi_name packaging

# Specify --without docs to prevent the dependency loop on python-sphinx
# RHEL: Disabled due to missing deps
%bcond_with docs

# Specify --without tests to prevent the dependency loop on python-pytest
# RHEL: Disabled due to missing deps
%bcond_with tests

%global python_wheelname %{pypi_name}-%{version}-py2.py3-none-any.whl

Name:           python-%{pypi_name}
Version:        20.4
Release:        4%{?dist}
Summary:        Core utilities for Python packages

License:        BSD or ASL 2.0
URL:            https://github.com/pypa/packaging
Source0:        %{pypi_source}
BuildArch:      noarch
# Exclude i686 arch. Due to a modularity issue it's being added to the
# x86_64 compose of CRB, but we don't want to ship it at all.
# See: https://projects.engineering.redhat.com/browse/RCM-72605
ExcludeArch:    i686

# Remove dependency on six to make package lighter, backported from upstream
Patch1:         %{url}/commit/39a70cce.patch

BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  python%{python3_pkgversion}-pyparsing
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pretend
%endif
%if %{with docs}
BuildRequires:  python%{python3_pkgversion}-sphinx
%endif

BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel

%description
python-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

Requires:       python%{python3_pkgversion}-pyparsing

%description -n python%{python3_pkgversion}-%{pypi_name}
python%{python3_pkgversion}-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%if %{with docs}
%package -n python%{python3_pkgversion}-%{pypi_name}-doc
Summary:        python-packaging documentation

%description -n python%{python3_pkgversion}-%{pypi_name}-doc
Documentation for python-packaging
%endif

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build_wheel

%if %{with docs}
# generate html docs
sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/
%endif

%install
%py3_install_wheel %{python_wheelname}

%if %{with tests}
%check
%pytest
%endif

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*-info/

%if %{with docs}
%files -n python%{python3_pkgversion}-%{pypi_name}-doc
%doc html
%license LICENSE LICENSE.APACHE LICENSE.BSD
%endif

%changelog
* Tue Jan 12 2021 Tomas Orsava <torsava@redhat.com> - 20.4-4
- Convert from Fedora to the python39 module in RHEL8
- Resolves: rhbz#1877430

* Fri Oct 02 2020 Miro Hrončok <mhroncok@redhat.com> - 20.4-3
- Drop the dependency on six to make the package lighter

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 01 2020 Lumír Balhar <lbalhar@redhat.com> - 20.4-1
- Update to 20.4 (#1838285)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 20.3-3
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 20.3-2
- Bootstrap for Python 3.9

* Fri Mar 06 2020 Lumír Balhar <lbalhar@redhat.com> - 20.3-1
- Update to 20.3 (#1810738)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Lumír Balhar <lbalhar@redhat.com> - 20.1-1
- Update to 20.1 (#1794865)

* Mon Jan 06 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0-2
- Ignore broken tests

* Mon Jan 06 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0-1
- Update to 20.0 (#1788012)

* Thu Sep 26 2019 Lumír Balhar <lbalhar@redhat.com> - 19.2-1
- New upstream version 19.2 (bz#1742388)

* Mon Sep 23 2019 Lumír Balhar <lbalhar@redhat.com> - 19.0-6
- Remove Python 2 subpackage
- Make spec fedora-specific

* Mon Sep 02 2019 Miro Hrončok <mhroncok@redhat.com> - 19.0-5
- Reduce Python 2 build time dependencies

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 19.0-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 19.0-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Lumír Balhar <lbalhar@redhat.com> - 19.0-1
- New upstream version

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Charalampos Stratakis <cstratak@redhat.com> - 17.1-1
- Update to 17.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 16.8-10
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 16.8-9
- Bootstrap for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 16.8-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Lumir Balhar <lbalhar@redhat.com> - 16.8-5
- Epel7 compatible spec/package

* Mon Feb 13 2017 Charalampos Stratakis <cstratak@redhat.com> - 16.8-4
- Rebuild as wheel

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 16.8-2
- Rebuild for Python 3.6

* Wed Nov 02 2016 Lumir Balhar <lbalhar@redhat.com> - 16.8-1
- New upstream version

* Fri Sep 16 2016 Lumir Balhar <lbalhar@redhat.com> - 16.7-1
- Initial package.
