Name:           VectorChord

# Versions higher than this require us to package libsqlite3 and rusqlite,
# which are in Fedora but not new enough. Maybe wait until they are updated
# in the distro
Version:        0.5.1
Release:        1%{?dist}
Summary:        High-performance, and disk-efficient vector similarity search

License:        AGPL-3.0 OR Elastic-2.0
URL:            https://github.com/tensorchord/%{name}/
Source:         https://github.com/tensorchord/%{name}/archive/refs/tags/%{version}.tar.gz

Patch:          0001-relax-dependency-requirements.patch
Patch:          0002-fix-mismatched-types-in-if-expression.patch

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
* Wed Oct 22 2025 Mat Booth <mat.booth@gmail.com> - 0.5.3-1
- Initial package

