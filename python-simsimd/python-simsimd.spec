%global pypi_name simsimd

Name:           python-%{pypi_name}
Version:        5.9.11
Release:        1%{?dist}
Summary:        Mixed-precision math library

License:        MIT
URL:            https://github.com/ashvardanian/SimSIMD
Source:         %{pypi_source %{pypi_name}}

BuildRequires:  gcc
BuildRequires:  python3-devel

%description
Up to 200x Faster Dot Products & Similarity Metrics supporting f64, f32, f16
real & complex, i8, and bit vectors using SIMD for both AVX2, AVX-512, NEON,
SVE, & SVE2

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
Up to 200x Faster Dot Products & Similarity Metrics supporting f64, f32, f16
real & complex, i8, and bit vectors using SIMD for both AVX2, AVX-512, NEON,
SVE, & SVE2

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

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
* Thu Oct 30 2025 Mat Booth <mat.booth@gmail.com> - 5.9.11-1
- Rebuild package

