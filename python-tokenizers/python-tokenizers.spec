%global pypi_name tokenizers

Name:           python-%{pypi_name}
Version:        0.21.0
Release:        %autorelease
Summary:        Fast state-of-the-art tokenizers

License:        Apache-2.0
URL:            https://github.com/huggingface/tokenizers
Source0:        %{url}/archive/v%{version}/tokenizers-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  cargo-rpm-macros

%description
Provides an implementation of today's most used tokenizers, with a focus
on performance and versatility.

%package -n     python3-%{pypi_name}
Summary:        Fast state-of-the-art tokenizers

%description -n python3-%{pypi_name}
Provides an implementation of today's most used tokenizers, with a focus
on performance and versatility.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# Use same dep range for ndarray as numpy does
sed -i -e '/^ndarray/s/.*/ndarray = ">= 0.15, < 0.17"/' bindings/python/Cargo.toml

pushd bindings/python 2>&1 >/dev/null
%cargo_prep
popd 2>&1 >/dev/null

%generate_buildrequires
pushd tokenizers 2>&1 >/dev/null
%cargo_generate_buildrequires
popd 2>&1 >/dev/null
pushd bindings/python 2>&1 >/dev/null
%cargo_generate_buildrequires
%pyproject_buildrequires
popd 2>&1 >/dev/null

%build
pushd bindings/python 2>&1 >/dev/null
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies
%pyproject_wheel
popd 2>&1 >/dev/null

%install
pushd bindings/python 2>&1 >/dev/null
%pyproject_install
%pyproject_save_files %{pypi_name}
popd 2>&1 >/dev/null

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE LICENSES.dependencies
%doc README.md

%changelog
%autochangelog
