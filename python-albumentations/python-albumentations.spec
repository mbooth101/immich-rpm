%global pypi_name albumentations

Name:           python-%{pypi_name}
Version:        2.0.5
Release:        %autorelease
Summary:        Fast and flexible image augmentation library

License:        MIT
URL:            https://github.com/albumentations-team/albumentations
Source0:        %{url}/archive/%{version}/albumentations-%{version}.tar.gz

BuildArch: noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
Albumentations is a Python library for image augmentation. Image augmentation
is used in deep learning and computer vision tasks to increase the quality of
trained models. The purpose of image augmentation is to create new training
samples from the existing data.

%package -n     python3-%{pypi_name}
Summary:        Fast and flexible image augmentation library

%description -n python3-%{pypi_name}
Albumentations is a Python library for image augmentation. Image augmentation
is used in deep learning and computer vision tasks to increase the quality of
trained models. The purpose of image augmentation is to create new training
samples from the existing data.

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
