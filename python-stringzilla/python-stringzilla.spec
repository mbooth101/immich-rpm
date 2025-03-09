%global pypi_name stringzilla

Name:           python-%{pypi_name}
Version:        3.10.11

Release:        %autorelease
Summary:        The GodZilla of string libraries

License:        MIT
URL:            https://github.com/ashvardanian/StringZilla
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
Up to 10x faster strings, leveraging NEON, AVX2, AVX-512, SVE, & SWAR to
accelerate search, hashing, sort, edit distances, and memory ops.

%package -n     python3-%{pypi_name}
Summary:        The GodZilla of string libraries

%description -n python3-%{pypi_name}
Up to 10x faster strings, leveraging NEON, AVX2, AVX-512, SVE, & SWAR to
accelerate search, hashing, sort, edit distances, and memory ops.

%prep
%autosetup -p1 -n StringZilla-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

# Don't package the CLI
rm -rf %{buildroot}%{_bindir} %{buildroot}%{python3_sitearch}/cli

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
%autochangelog
