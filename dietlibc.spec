Summary:	C library optimized for size
Name:		dietlibc
Version:	20010410
Release:	1
License:	GPL
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Source0:	http://www.fefe.de/dietlibc/%{name}-%{version}.tar.gz
Patch0:		%{name}-install.patch
URL:		http://www.fefe.de/dietlibc/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%define	boot /usr/lib/bootdisk
%define	_prefix %{boot}/usr


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
%patch -p1


%build
make DIETHOME=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_bindir}
%{__make} prefix=%{_prefix} INSTALLPREFIX=$RPM_BUILD_ROOT install
cp -a include/ $RPM_BUILD_ROOT/%{_includedir}

#rm include/asm include/linux


gzip -9nf README THANKS CAVEAT BUGS AUTHOR

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
