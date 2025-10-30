%global pypi_name albumentations

Name:           python-%{pypi_name}
Version:        2.0.5
Release:        1%{?dist}
Summary:        Fast and flexible image augmentation library

License:        MIT
URL:            https://github.com/albumentations-team/albumentations
Source:         %{pypi_source %{pypi_name}}

BuildArch: noarch
BuildRequires:  python3-devel

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

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

sed -i -e 's/opencv-python-headless/opencv/' setup.py

# Fix license warnings
sed -i -e 's/^license.*/license = "MIT"/' \
       -e '/License :: OSI Approved :: MIT License/d' pyproject.toml

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
* Thu Oct 30 2025 Mat Booth <mat.booth@gmail.com> - 2.0.5-1
- Rebuild package

