%global commit0 bbc8608755da42e7494c00dce24a636007972def
%global date 20170915
%global shortcommit0 %%(c=%%{commit0}; echo ${c:0:7})

# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels akmod

%global debug_package %{nil}

%global zipmodules 1

%define __spec_install_post \
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__mod_compress_install_post}

%define __mod_compress_install_post \
  if [ "%{zipmodules}" -eq "1" ]; then \
    find %{buildroot}/usr/lib/modules/ -type f -name '*.ko' | xargs xz; \
  fi

Name:       xpad-kmod
Version:    4.14
Release:    1%{?snapshot:.%{snapshot}}%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Summary:    X-Box gamepad driver
License:    GPLv2+
URL:        http://www.kernel.org/

# Source file:
# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/input/joystick/xpad.c

Source0:    https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/input/joystick/xpad.c?id=%{commit0}#/xpad.c
Source1:    Makefile
Source11:   xpad-kmodtool-excludekernel-filterfile

# Get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
X-Box gamepad driver from latest upstream kernel.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -T -c -n %{name}-%{version}
cp %{SOURCE0} %{SOURCE1} .

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp xpad.c _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
make -C /lib/modules/${kernel_version%%___*}/build V=1 M=$(pwd) modules
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 xpad.ko %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Thu Sep 21 2017 Simone Caronni <negativo17@gmail.com> - 4.14-1.20170915gitbbc8608
- Update to latest snapshot.

* Sat Apr 15 2017 Simone Caronni <negativo17@gmail.com> - 4.11-1.20170410git5376366
- Update to latest snapshot from the official kernel repository.

* Tue Feb 21 2017 Simone Caronni <negativo17@gmail.com> - 4.1-5
- Update to latest commits.

* Mon Sep 12 2016 Simone Caronni <negativo17@gmail.com> - 4.1-4
- Update to latest commits.

* Sat May 28 2016 Simone Caronni <negativo17@gmail.com> - 4.1-3
- Make sure installed modules are compressed with xz (default since May 2014 in
  Fedora...). Thanks leigh123linux.

* Sun Jan 31 2016 Simone Caronni <negativo17@gmail.com> - 4.1-2
- Update to latest commits.

* Sat Nov 14 2015 Simone Caronni <negativo17@gmail.com> - 4.1-1
- Update to version from 4.1 branch (SteamOS 2.x).

* Sat Oct 31 2015 Simone Caronni <negativo17@gmail.com> - 0.2-4
- Update to the latest commits prior to rebase on 4.x branch.

* Fri Jul 31 2015 Simone Caronni <negativo17@gmail.com> - 0.2-3
- Update to latest commits.

* Thu Jul 16 2015 Simone Caronni <negativo17@gmail.com> - 0.2-2
- Update to latest commits.

* Wed Jul 08 2015 Simone Caronni <negativo17@gmail.com> - 0.2-1
- Rebase to brewmaster 3.18 kernel.
- Drop integrated patches.

* Sat May 23 2015 Simone Caronni <negativo17@gmail.com> - 0.1-3
- Apply patche from tjormola tree which includes extra fixes:
  https://github.com/tjormola/steamos_kernel/commits/xpad_fixes_from_linus_tree/drivers/input/joystick/xpad.c

* Wed Oct 01 2014 Simone Caronni <negativo17@gmail.com> - 0.1-2
- Use directly SteamOS kernel source, remove patches:
  https://github.com/ValveSoftware/steamos_kernel/commits/alchemist-3.10/drivers/input/joystick/xpad.c

* Thu May 29 2014 Simone Caronni <negativo17@gmail.com> - 0.1-1
- First build, with Valve patches.
