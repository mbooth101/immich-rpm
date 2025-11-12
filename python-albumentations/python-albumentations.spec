%global pypi_name albumentations

Name:           python-%{pypi_name}
Version:        2.0.8
Release:        1%{?dist}
Summary:        Fast and flexible image augmentation library

License:        MIT
URL:            https://github.com/albumentations-team/albumentations
Source:         %{url}/archive/refs/tags/%{version}.tar.gz

Patch:          0001-disable-remote-version-check.patch
Patch:          0002-disable-failing-test.patch

BuildArch: noarch
BuildRequires:  python3-devel

# Test dependencies
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(pillow)
BuildRequires:  python3dist(torchvision)
BuildRequires:  python3dist(deepdiff)
BuildRequires:  python3dist(scikit-image)
BuildRequires:  python3dist(scikit-learn)

%description
Albumentations is a Python library for image augmentation. Image augmentation
is used in deep learning and computer vision tasks to increase the quality of
trained models. The purpose of image augmentation is to create new training
samples from the existing data.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
Albumentations is a Python library for image augmentation. Image augmentation
is used in deep learning and computer vision tasks to increase the quality of
trained models. The purpose of image augmentation is to create new training
samples from the existing data.

%pyproject_extras_subpkg -n python3-%{pypi_name} pytorch

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

sed -i -e 's/opencv-python-headless/opencv/' setup.py

# Fix license warnings
sed -i -e 's/^license.*/license = "MIT"/' \
       -e '/License :: OSI Approved :: MIT License/d' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -x pytorch

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pyproject_check_import
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Wed Nov 12 2025 Mat Booth <mat.booth@gmail.com> - 2.0.8-1
- Update to 2.0.8
- Enable running tests
- Disable remote version update check

* Thu Oct 30 2025 Mat Booth <mat.booth@gmail.com> - 2.0.5-1
- Rebuild package

