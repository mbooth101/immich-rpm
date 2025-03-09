%global pypi_name albucore

Name:           python-%{pypi_name}
Version:        0.0.23
Release:        %autorelease
Summary:        Library of optimized atomic functions for image processing

License:        MIT
URL:            https://github.com/albumentations-team/albucore
Source0:        %{url}/archive/%{version}/albucore-%{version}.tar.gz

BuildArch: noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
Albucore is a library of optimized atomic functions designed for efficient
image processing. These functions serve as the foundation for Albumentations,
a popular image augmentation library.

%package -n     python3-%{pypi_name}
Summary:        Library of optimized atomic functions for image processing

%description -n python3-%{pypi_name}
Albucore is a library of optimized atomic functions designed for efficient
image processing. These functions serve as the foundation for Albumentations,
a popular image augmentation library.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

sed -i -e 's/opencv-python-headless/opencv/' setup.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
%autochangelog
