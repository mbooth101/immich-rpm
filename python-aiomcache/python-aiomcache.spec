%global pypi_name aiomcache

Name:           python-%{pypi_name}
Version:        0.8.2
Release:        1%{?dist}
Summary:        Minimal asyncio memcached client

License:        BSD-2-Clause
URL:            https://github.com/aio-libs/aiomcache
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

Patch:          0001-remove-docker-tests.patch

BuildArch: noarch
BuildRequires:  python3-devel

# Test dependencies
BuildRequires:  memcached
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
BuildRequires:  python3dist(python-memcached)

%description
An asyncio (PEP 3156) library to work with memcached.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
An asyncio (PEP 3156) library to work with memcached.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
# Memcached required to be running for tests
memcached -p 11211 -u memcached -d

%pyproject_check_import
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Wed Nov 12 2025 Mat Booth <mat.booth@gmail.com> - 0.8.2-1
- Initial package

