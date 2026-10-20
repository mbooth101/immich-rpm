%global pypi_name omegaconf

Name:           python-%{pypi_name}
Version:        2.4.0
Release:        1%{?dist}
Summary:        A flexible configuration library

License:        BSD-3-Clause
URL:            https://github.com/hydra-ecosystem/omegaconf
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

# Generate the parser with Fedora's antlr4 and use the system antlr4 runtime
# instead of the bundled jar and vendored copy of the runtime
Patch:          0001-use-system-antlr4.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  antlr4

# Test dependencies
BuildRequires:  python3dist(attrs)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(typing-extensions)

%description
OmegaConf is a hierarchical configuration system, with support for merging
configurations from multiple sources (YAML config files, dataclasses/objects
and CLI arguments) providing a consistent API regardless of how the
configuration was created.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
OmegaConf is a hierarchical configuration system, with support for merging
configurations from multiple sources (YAML config files, dataclasses/objects
and CLI arguments) providing a consistent API regardless of how the
configuration was created.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# Remove bundled antlr4 tool and runtime
rm -rf build_helpers/bin omegaconf/vendor/antlr4

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pyproject_check_import
# Skip tests for upstream's CI and release tooling
%pytest tests \
  --ignore-glob='tests/test_dependency_audit*.py' \
  --ignore=tests/test_release_workflow.py

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md NEWS.md

%changelog
* Tue Oct 20 2026 Mat Booth <mat.booth@gmail.com> - 2.4.0-1
- Initial package
