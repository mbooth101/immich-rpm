%global pypi_name tokenizers

Name:           python-%{pypi_name}
Version:        0.21.0
Release:        %autorelease
Summary:        Fast state-of-the-art tokenizers

License:        Apache-2.0
URL:            https://github.com/huggingface/tokenizers
Source0:        %{url}/archive/v%{version}/tokenizers-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  maturin
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  cargo-rpm-macros

BuildRequires:  (crate(env_logger/default) >= 0.11.0 with crate(env_logger/default) < 0.12.0~)
BuildRequires:  (crate(itertools/default) >= 0.12.0 with crate(itertools/default) < 0.13.0~)
BuildRequires:  (crate(libc/default) >= 0.2.0 with crate(libc/default) < 0.3.0~)
BuildRequires:  (crate(ndarray/default) >= 0.15.0 with crate(ndarray/default) < 0.17.0~)
BuildRequires:  (crate(numpy/default) >= 0.22.0 with crate(numpy/default) < 0.23.0~)
BuildRequires:  (crate(pyo3/abi3) >= 0.22.0 with crate(pyo3/abi3) < 0.23.0~)
BuildRequires:  (crate(pyo3/abi3-py39) >= 0.22.0 with crate(pyo3/abi3-py39) < 0.23.0~)
BuildRequires:  (crate(pyo3/default) >= 0.22.0 with crate(pyo3/default) < 0.23.0~)
BuildRequires:  (crate(rayon/default) >= 1.10.0 with crate(rayon/default) < 2.0.0~)
BuildRequires:  (crate(serde/default) >= 1.0.0 with crate(serde/default) < 2.0.0~)
BuildRequires:  (crate(serde/derive) >= 1.0.0 with crate(serde/derive) < 2.0.0~)
BuildRequires:  (crate(serde/rc) >= 1.0.0 with crate(serde/rc) < 2.0.0~)
BuildRequires:  (crate(serde_json/default) >= 1.0.0 with crate(serde_json/default) < 2.0.0~)

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
%license LICENSE
%doc README.md

%changelog
%autochangelog
