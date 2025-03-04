# Disable debuginfo, since we package a stripped upstream binary
%global debug_package %{nil}

Name:           immich
Version:        1.128.0
Release:        1%{?dist}
Summary:        Self-hosted photo and video management solution

License:        AGPL-3.0
URL:            https://immich.app/
Source0:        v%{version}.tar.gz
Source1:        sysusers
Source2:        systemd.service
Source3:        environment

ExclusiveArch:  %{nodejs_arches}

Requires:      nodejs
Requires:      mimalloc
Requires:      postgresql-server
Requires:      postgresql-contrib
Requires:      valkey
BuildRequires: nodejs-devel
BuildRequires: systemd-rpm-macros

%{?sysusers_requires_compat}

%description
Easily back up, organize, and manage your photos on your own server. Immich
helps you browse, search and organize your photos and videos with ease,
without sacrificing your privacy.

%prep
%setup -q -n %{name}-%{version}

# Fix hard-coded script paths
sed -i -e 's|/usr/src/app|%{_prefix}/lib/node_modules/%{name}|' server/bin/immich* server/start.sh
sed -i -e 's|^lib_path=.*|lib_path=%{_libdir}/libmimalloc.so.2|' server/start.sh

%build
# These build steps essentially mirroe those performed in the Dockerfile

# Build server component
pushd server
npm ci
rm -rf node_modules/@img/sharp-libvips*
rm -rf node_modules/@img/sharp-linuxmusl-x64
npm run build
mkdir tmp
mv node_modules/{@img,exiftool-vendored.pl} tmp
npm prune --omit=dev --omit=optional
mv tmp/{@img,exiftool-vendored.pl} node_modules
popd

# Build web component
pushd open-api/typescript-sdk
npm ci
npm run build
popd
pushd web
npm ci
npm run build
popd

%install
# User/Group configuration
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf
# Systemd service files
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Install server component
install -m 0755 -d %{buildroot}%{nodejs_sitelib}/%{name}
cp -pr server/{node_modules,dist,bin,resources} %{buildroot}%{nodejs_sitelib}/%{name}
install -Dpm 0644 server/{package.json,package-lock.json} %{buildroot}%{nodejs_sitelib}/%{name}
install -Dpm 0755 server/start.sh docker/scripts/get-cpus.sh %{buildroot}%{nodejs_sitelib}/%{name}
install -m 0755 -d %{buildroot}%{_bindir}
npm set prefix %{buildroot}%{_prefix}
npm install -g @immich/cli
mv %{buildroot}%{_prefix}/lib/node_modules/@immich %{buildroot}%{nodejs_sitelib}/@immich
rm -rf %{buildroot}%{_prefix}/lib/node_modules

# Install web component
install -m 0755 -d %{buildroot}%{_prefix}/lib/%{name}
cp -pr web/build/* %{buildroot}%{_prefix}/lib/%{name}

# User data
install -d %{buildroot}%{_sharedstatedir}/%{name}/backups
install -d %{buildroot}%{_sharedstatedir}/%{name}/encoded-video
install -d %{buildroot}%{_sharedstatedir}/%{name}/library
install -d %{buildroot}%{_sharedstatedir}/%{name}/profile
install -d %{buildroot}%{_sharedstatedir}/%{name}/thumbs
install -d %{buildroot}%{_sharedstatedir}/%{name}/upload

%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md SECURITY.md
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_sysconfdir}/sysconfig/%{name}
%{nodejs_sitelib}/%{name}
%{nodejs_sitelib}/@%{name}
%{_bindir}/%{name}
%{_prefix}/lib/%{name}
%attr(0750,immich,immich) %{_sharedstatedir}/%{name}

%changelog
* Mon Mar 03 2025 Mat Booth <mat.booth@gmail.com> - 1.128.0-1
- Initial release

