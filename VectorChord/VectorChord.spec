Name:           VectorChord

Version:        1.1.1
Release:        1%{?dist}
Summary:        High-performance, and disk-efficient vector similarity search

License:        AGPL-3.0 OR Elastic-2.0
URL:            https://github.com/supervc-stack/%{name}/
Source:         https://github.com/supervc-stack/%{name}/archive/refs/tags/%{version}.tar.gz

Patch:          0001-Fix-dependency-requirements-according-to-what-s-avai.patch
Patch:          0002-Patch-out-unused-wasm-support.patch
# Fedora 43's rust is built against LLVM 21, which can't compile the AVX-512 VNNI
# intrinsics from its stdarch; drop this once F43 is EOL
%if 0%{?fedora} && 0%{?fedora} < 44
Patch:          0003-Remove-AVX-512-VNNI-code-paths.patch
%endif

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  postgresql18-server-devel
BuildRequires:  postgresql18-private-devel
BuildRequires:  rustfmt

Requires: postgresql18-server
Requires: postgresql18-pgvector

%description
VectorChord (vchord) is a PostgreSQL extension designed for scalable,
high-performance, and disk-efficient vector similarity search.

%files
%{_libdir}/pgsql/vchord.so
%{_datadir}/pgsql/extension/*

%prep
%autosetup -p1
%cargo_prep
mkdir .pgrx
echo '[configs]' >> .pgrx/config.toml
echo 'pg18 = "/usr/bin/pg_config"' >> .pgrx/config.toml

%generate_buildrequires
%cargo_generate_buildrequires -f pg18

%build
export PGRX_HOME=$(pwd)/.pgrx
%cargo_build -f pg18

%install
install -Dm 0755 target/rpm/libvchord.so %{buildroot}%{_libdir}/pgsql/vchord.so
mkdir -p %{buildroot}%{_datadir}/pgsql/extension
install -m 0644 ./sql/upgrade/*.sql %{buildroot}%{_datadir}/pgsql/extension
install -m 0644 ./sql/install/vchord--%{version}.sql %{buildroot}%{_datadir}/pgsql/extension
install -m 0644 vchord.control %{buildroot}%{_datadir}/pgsql/extension

%changelog
* Mon Oct 19 2026 Mat Booth <mat.booth@gmail.com> - 1.1.1-1
- Update to latest upstream release

* Wed Oct 29 2025 Mat Booth <mat.booth@gmail.com> - 0.5.3-1
- Update to 0.5.3

* Wed Oct 22 2025 Mat Booth <mat.booth@gmail.com> - 0.5.1-1
- Initial package

