Summary:	C library optimized for size
Name:		dietlibc
Version:	0.8
Release:	1
License:	GPL
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Source0:	http://www.fefe.de/dietlibc/%{name}-%{version}.tar.bz2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Small libc for building embedded applications.

%package devel
Summary:	Development files for dietlibc
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Small libc for building embedded applications.

%prep
%setup -q -n %{name}
( cd include ; ln -s /usr/src/linux/include/linux . )
( cd include ; ln -s /usr/src/linux/include/asm-i386 asm )

%build
# Override normal cflags with optimization for size
%{__make} "CFLAGS=-nostdinc -march=i586 -fomit-frame-pointer -Os -I%{_libdir}/gcc-lib/i586-mandrake-linux/2.96/include"

%install
rm -rf $RPM_BUILD_ROOT
rm include/asm include/linux
%{__make} prefix=%{_prefix} INSTALLPREFIX=$RPM_BUILD_ROOT install

gzip -9nf README THANKS CAVEAT BUGS AUTHOR

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz

%files devel
%defattr(644,root,root,755)
%doc CHANGES TODO
%{_datadir}/dietlibc/*
%{_libdir}/*
