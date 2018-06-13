# Disable the stupid stuff rpm distros include in the build process by default:
#   Disable any prep shell actions. replace them with simply 'true'
%define __spec_prep_post true
%define __spec_prep_pre true
#   Disable any build shell actions. replace them with simply 'true'
%define __spec_build_post true
%define __spec_build_pre true
#   Disable any install shell actions. replace them with simply 'true'
%define __spec_install_post true
%define __spec_install_pre true
#   Disable any clean shell actions. replace them with simply 'true'
%define __spec_clean_post true
%define __spec_clean_pre true
# Disable checking for unpackaged files ?
#%undefine __check_files
%{?systemd_requires}
# Use md5 file digest method.
# The first macro is the one used in RPM v4.9.1.1
%define _binary_filedigest_algorithm 1
# This is the macro I find on OSX when Homebrew provides rpmbuild (rpm v5.4.14)
%define _build_binary_file_digest_algo 1

# Use gzip payload compression
%define _binary_payload w9.gzdio


Name: penstock
Version: 0.3
Release: xxx
Summary: no description given
AutoReqProv: no
BuildRoot: %buildroot

Prefix: /

Group: default
License: Apache License Version 2.0
Vendor: Quintagroup, Ltd.
URL: http://quintagroup.com/
Packager: <info@quintagroup.com>

BuildRequires: systemd
Requires: systemd python2-libs libyaml libffi

%description
no description given

%prep
# noop
rm -rf %{buildroot}
mkdir %{buildroot}
cp -r --parents /opt/penstock  %{buildroot}/
mkdir -p %{buildroot}/etc/systemd/system/
mkdir -p %{buildroot}/etc/penstock/
cp /opt/penstock/rpm/penstock.service %{buildroot}/etc/systemd/system/penstock.service
cp /opt/penstock/etc/penstock.yml %{buildroot}/etc/penstock/penstock.yml 
%build
# noop

%install
# noop

%clean
# noop

%pre
getent group penstock >/dev/null || groupadd -r penstock
getent passwd penstock >/dev/null || \
    useradd -r -g penstock -s /sbin/nologin penstock
exit 0

%post
%systemd_user_post penstock.service

%preun
%systemd_user_preun penstock.service


%files
%defattr(-,penstock,penstock,-)
%config(noreplace) /etc/systemd/system/penstock.service
%config(noreplace) /etc/penstock
%attr(0755,penstock,penstock) /opt/penstock

%changelog


