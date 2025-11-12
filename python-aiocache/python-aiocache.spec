%global pypi_name aiocache

Name:           python-%{pypi_name}
Version:        0.12.3
Release:        2%{?dist}
Summary:        Multi-backend async IO cache

License:        BSD-3-Clause
URL:            https://github.com/aio-libs/aiocache
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

Patch:          0001-fix-deprecated-API-usage.patch
Patch:          0002-disable-failing-performance-tests.patch

BuildArch: noarch
BuildRequires:  python3-devel

# Test dependencies
BuildRequires:  httpd-tools
BuildRequires:  memcached
BuildRequires:  valkey
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
BuildRequires:  python3dist(pytest-cov)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(aiohttp)
BuildRequires:  python3dist(marshmallow)
BuildRequires:  python3dist(msgpack)

%description
Asyncio cache manager for redis, memcached and memory.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
Asyncio cache manager for redis, memcached and memory.

%pyproject_extras_subpkg -n python3-%{pypi_name} redis memcached

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -x redis,memcached

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
# Memcached required to be running for tests
memcached -p 11211 -u memcached -d
# Redis required to be running for tests
valkey-server "" --daemonize yes

%pyproject_check_import
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Wed Nov 12 2025 Mat Booth <mat.booth@gmail.com> - 0.12.3-2
- Enable running unittests

* Thu Oct 30 2025 Mat Booth <mat.booth@gmail.com> - 0.12.3-1
- Rebuild package

