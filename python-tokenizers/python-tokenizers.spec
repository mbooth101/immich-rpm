%bcond check 1
%global debug_package %{nil}

%global pypi_name tokenizers

Name:           python-%{pypi_name}
Version:        0.22.1
Release:        1%{?dist}
Summary:        Fast state-of-the-art tokenizers

License:        Apache-2.0
URL:            https://github.com/huggingface/tokenizers
Source:         %{pypi_source %{pypi_name}}

BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  cargo-rpm-macros >= 24

%description
Provides an implementation of today's most used tokenizers, with a focus
on performance and versatility.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
Provides an implementation of today's most used tokenizers, with a focus
on performance and versatility.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# Use tokenizers library from Fedora repos instead
sed -i -e 's|path = "../../tokenizers"|version = "=%{version}"|' bindings/python/Cargo.toml

%cargo_prep
cd bindings/python && rm Cargo.lock

%generate_buildrequires
pushd bindings/python 2>&1 >/dev/null
%cargo_generate_buildrequires
popd 2>&1 >/dev/null
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pyproject_check_import

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc bindings/python/README.md bindings/python/CHANGELOG.md

%changelog
* Thu Oct 30 2025 Mat Booth <mat.booth@gmail.com> - 0.22.1-1
- Update to match rust-tokenizers version in Fedora

* Thu Oct 30 2025 Mat Booth <mat.booth@gmail.com> - 0.21.0-1
- Rebuild package

