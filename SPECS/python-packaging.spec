# Tests are disabled to remove the test dependencies
# Specify --with tests to run the tests on e.g. EPEL
%bcond_with tests

%global pypi_name packaging

# Specify --with bootstrap to build in bootstrap mode
# This mode is needed, because python3-rpm-generators need packaging
# When bootstrapping, disable tests and docs as well.
%bcond_with bootstrap

%if %{without bootstrap}
# Specify --without docs to prevent the dependency loop on python-sphinx
%bcond_without docs

%else
%bcond_with docs
%endif

Name:           python-%{pypi_name}
Version:        20.9
Release:        5%{?dist}
Summary:        Core utilities for Python packages

License:        BSD or ASL 2.0
URL:            https://github.com/pypa/packaging
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros

%if %{with bootstrap}
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

# Upstream uses nox for testing, we specify the test deps manually as well.
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pretend
%endif
%if %{with docs}
BuildRequires:  python%{python3_pkgversion}-sphinx
%endif


%global _description %{expand:
python-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.}

%description %_description


%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}

# This is kept for compatibility with Fedora < 33 only:
%py_provides    python%{python3_pkgversion}-%{pypi_name}

%if %{with bootstrap}
Provides:       python%{python3_pkgversion}dist(packaging) = %{version}
Provides:       python%{python3_version}dist(packaging) = %{version}
Requires:       python%{python3_version}dist(pyparsing)
%endif

%description -n python%{python3_pkgversion}-%{pypi_name}  %_description


%if %{with docs}
%package -n python-%{pypi_name}-doc
Summary:        python-packaging documentation

%description -n python-%{pypi_name}-doc
Documentation for python-packaging
%endif


%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# Do not use furo as HTML theme in docs
# furo is not available in Fedora
sed -i '/html_theme = "furo"/d' docs/conf.py

%if %{without bootstrap}
%generate_buildrequires
%pyproject_buildrequires -r
%endif


%build
%if %{with bootstrap}
%py3_build
%else
%pyproject_wheel
%endif

%if %{with docs}
# generate html docs
sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/
%endif


%install
%if %{with bootstrap}
%py3_install
echo '%{python3_sitelib}/packaging*' > %{pyproject_files}
%else
%pyproject_install
%pyproject_save_files %{pypi_name}
%endif


%if %{with tests}
%check
%pytest
%endif


%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst


%if %{with docs}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE LICENSE.APACHE LICENSE.BSD
%endif


%changelog
* Tue Feb 08 2022 Tomas Orsava <torsava@redhat.com> - 20.9-5
- Add automatically generated Obsoletes tag with the python39- prefix
  for smoother upgrade from RHEL8
- Related: rhbz#1990421

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com>
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com>
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Mon Mar 08 2021 Charalampos Stratakis <cstratak@redhat.com> - 20.9-2
- Disable tests on RHEL9 to remove the test dependencies

* Mon Feb 01 2021 Lumír Balhar <lbalhar@redhat.com> - 20.9-1
- Update to 20.9
Resolves: rhbz#1922545

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Lumír Balhar <lbalhar@redhat.com> - 20.8-1
- Update to 20.8 (#1906985)

* Mon Nov 30 2020 Lumír Balhar <lbalhar@redhat.com> - 20.7-1
- Update to 20.7 (#1902369)

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
