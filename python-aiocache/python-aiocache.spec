%global pypi_name aiocache

Name:           python-%{pypi_name}
Version:        0.12.3
Release:        1%{?dist}
Summary:        Multi-backend async IO cache

License:        BSD-3-Clause
URL:            https://github.com/aio-libs/aiocache
Source:         %{pypi_source %{pypi_name}}

BuildArch: noarch
BuildRequires:  python3-devel

%description
Asyncio cache manager for redis, memcached and memory.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
Asyncio cache manager for redis, memcached and memory.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Thu Oct 30 2025 Mat Booth <mat.booth@gmail.com> - 0.12.3-1
- Rebuild package

