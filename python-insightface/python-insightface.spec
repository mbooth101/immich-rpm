%global pypi_name insightface

Name:           python-%{pypi_name}
Version:        0.7.3
Release:        1%{?dist}
Summary:        2D and 3D face analysis

License:        MIT
URL:            https://github.com/deepinsight/insightface
Source:         %{pypi_source %{pypi_name}}

BuildRequires:  gcc-c++
BuildRequires:  python3-devel

%description
InsightFace is an open source 2D & 3D deep face analysis toolbox. InsightFace
efficiently implements a rich variety of state of the art algorithms of face
recognition, face detection and face alignment, which optimized for both
training and deployment.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
InsightFace is an open source 2D & 3D deep face analysis toolbox. InsightFace
efficiently implements a rich variety of state of the art algorithms of face
recognition, face detection and face alignment, which optimized for both
training and deployment.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

# Duplicate data installation
rm -rf %{buildroot}%{_prefix}/insightface
# Remove headers
rm -rf %{buildroot}%{_includedir}

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%{_bindir}/insightface-cli

%changelog
* Thu Oct 30 2025 Mat Booth <mat.booth@gmail.com> - 0.7.3-1
- Rebuild package

