Summary:	C library optimized for size
Summary(pl):	Biblioteka standardowa C zoptymalizowana na rozmiar
Name:		dietlibc
Version:	0.15
Release:	1
Epoch:		2
License:	GPL
Group:		Development/Libraries
Source0:	http://www.fefe.de/dietlibc/%{name}-%{version}.tar.bz2
URL:		http://www.fefe.de/dietlibc/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Small libc for building embedded applications.

%description -l pl
Niewielka libc do budowania aplikacji wbudowanych.

%package devel
Summary:	Development files for dietlibc
Summary(pl):	Pliki dla programistów u¿ywaj±cych dietlibc
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Small libc for building embedded applications - development files.

%description devel -l pl
Niewielka libc do budowania aplikacji wbudowanych - pliki dla
programistów.

%package static
Summary:	Static libraries for dietlibc
Summary(pl):	Biblioteki statyczne dla dietlibc
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description static
Small libc for building embedded applications - static libraries.

%description static -l pl
Niewielka libc do budowania aplikacji wbudowanych - biblioteki
statyczne.

%prep
%setup -q 

%build
%define dietprefix %{_prefix}/%{_arch}-linux-dietlibc
%{__make} prefix=%{dietprefix} all dyn

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_mandir}/man1}

%{__make} install DESTDIR=$RPM_BUILD_ROOT prefix=%{dietprefix}

mv $RPM_BUILD_ROOT%{dietprefix}/bin/* $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{dietprefix}/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
rm -rf $RPM_BUILD_ROOT%{dietprefix}/{bin,man}
rm -f $RPM_BUILD_ROOT%{_bindir}/diet-dyn

cat > $RPM_BUILD_ROOT%{_bindir}/%{_arch}-dietlibc-gcc <<EOF
#!/bin/sh
exec %{_bindir}/diet gcc "\$@"
EOF

rm -rf $RPM_BUILD_ROOT%{dietprefix}/include/{asm,linux}

gzip -9nf TODO README THANKS CAVEAT CHANGES FAQ BUGS AUTHOR

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%dir %{dietprefix}
%dir %{dietprefix}/lib-%{_arch}
%attr(755,root,root) %{dietprefix}/lib-%{_arch}/*.so
%{_sysconfdir}/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{dietprefix}/include
%attr(755,root,root) %{dietprefix}/lib-%{_arch}/*.o
%{_mandir}/man*/*

%files static
%defattr(644,root,root,755)
%{dietprefix}/lib-%{_arch}/*.a
