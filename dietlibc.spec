%define name	dietlibc
%define version	0.7.3
%define release	2mdk
%define snapver	20010309

Summary:	C library optimized for size
Name:		%{name}
Version:	%{version}
Release:	%{release}
Copyright:	GPL
Group:		Development/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:	common-licenses

Source0:	http://www.fefe.de/dietlibc/%{name}-%{snapver}.tar.bz2
Patch0:		dietlibc-20010308-install-includes.patch.bz2

%description
Small libc for building embedded applications.

%package devel
Group:          Development/C
Summary:        Development files for dietlibc
Requires:       %name = %version-%release

%description devel
Small libc for building embedded applications.

%prep
%setup -q -n %{name}-%{snapver}
%patch0 -p1
( cd include ; ln -s /usr/src/linux/include/linux . )
( cd include ; ln -s /usr/src/linux/include/asm-i386 asm )

%build
# Override normal cflags with optimization for size
%make "CFLAGS=-nostdinc -march=i586 -fomit-frame-pointer -Os -I/usr/lib/gcc-lib/i586-mandrake-linux/2.96/include"

%install
rm include/asm include/linux
make prefix=%{_prefix} INSTALLPREFIX=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README THANKS CAVEAT BUGS AUTHOR

%files devel
%defattr(-,root,root)
%doc CHANGES TODO
%{_prefix}/share/dietlibc/*
%{_libdir}/*

%changelog
* Thu Mar  9 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.7.3-2mdk
- new cvs snapshot, adds mkstemp and syslog support among other things
- install includes in /usr/share/dietlibc/include (gc suggest)

* Thu Mar  8 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.7.3-1mdk
- first mdk contribs version: pre-0.7.3 cvs snapshot 20010308.
