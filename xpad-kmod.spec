%global commit0 5376366886251e2f8f248704adb620a4bc4c0937
%global date 20170410
%global shortcommit0 %%(c=%%{commit0}; echo ${c:0:7})

# Define the kmod package name here.
%global	kmod_name xpad

# If kversion isn't defined on the rpmbuild line, define it here. For Fedora,
# kversion needs always to be defined as there is no kABI support.

# RHEL 7.3
%if 0%{?rhel} == 7
%{!?kversion: %global kversion 3.10.0-514.el7.%{_target_cpu}}
%endif

Name:           %{kmod_name}-kmod
Version:        4.11
Release:        1%{?snapshot:.%{snapshot}}%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Summary:        X-Box gamepad driver
License:        GPLv2+
URL:            http://www.kernel.org/

# Source file:
# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/input/joystick/xpad.c
Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/input/joystick/xpad.c?id=%{commit0}#/xpad.c
Source1:        Makefile
Source10:       kmodtool-%{kmod_name}-el6.sh

BuildRequires:  redhat-rpm-config
BuildRequires:  kernel-abi-whitelists

%if 0%{?rhel} == 6
BuildRequires:  module-init-tools
%else
BuildRequires:  kmod
%endif

# Magic hidden here.
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

# Disable building of the debug package(s).
%global	debug_package %{nil}

%description
X-Box gamepad driver from latest upstream kernel. It is built to depend upon the
specific ABI provided by a range of releases of the same variant of the Linux
kernel and not on any one specific build.

%prep
%setup -q -T -c -n %{kmod_name}-%{version}
cp %{SOURCE0} %{SOURCE1} .

echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
make -C %{_usrsrc}/kernels/%{kversion} M=$PWD modules

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}
make -C %{_usrsrc}/kernels/%{kversion} M=$PWD modules_install

install -d %{buildroot}%{_sysconfdir}/depmod.d/
install kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
# Remove the unrequired files.
rm -f %{buildroot}/lib/modules/%{kversion}/modules.*

%changelog
* Sat Apr 15 2017 Simone Caronni <negativo17@gmail.com> - 4.11-1.20170410git5376366
- Update to latest snapshot from the official kernel repository.

* Tue Feb 21 2017 Simone Caronni <negativo17@gmail.com> - 0.1-6
- Update to latest commits.

* Fri Jul 31 2015 Simone Caronni <negativo17@gmail.com> - 0.1-5
- Update to latest commits.

* Thu Jul 16 2015 Simone Caronni <negativo17@gmail.com> - 0.1-4
- Update to latest commits.

* Wed Oct 01 2014 Simone Caronni <negativo17@gmail.com> - 0.1-3
- Use directly SteamOS kernel source, remove patches:
  https://github.com/ValveSoftware/steamos_kernel/commits/alchemist-3.10/drivers/input/joystick/xpad.c

* Thu May 29 2014 Simone Caronni <negativo17@gmail.com> - 0.1-1
- First build, with Valve patches.
