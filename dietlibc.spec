Summary:	C library optimized for size
Summary(pl):	Biblioteka standardowa C zoptymalizowana na rozmiar
Summary(pt_BR):	libc pequena otimizada para tamanho
Name:		dietlibc
Version:	0.23
Release:	1
Epoch:		2
License:	GPL v2
Group:		Development/Libraries
Source0:	http://www.kernel.org/pub/linux/libs/dietlibc/%{name}-%{version}.tar.bz2
# Source0-md5:	6db6a89785f079a51bf6d93f618ceee8
Patch0:		%{name}-ppc.patch
Patch1:		%{name}-opt.patch
URL:		http://www.fefe.de/dietlibc/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dietprefix	%{_prefix}/%{_target_cpu}-linux-dietlibc
# for some reason known only to rpm there must be "\\|" not "\|" here
%define		libarch		%(echo %{_target_cpu} | sed -e 's/i.86\\|athlon/i386/')

%description
Small libc for building embedded applications.

%description -l pl
Niewielka libc do budowania aplikacji wbudowanych.

%description -l pt_BR
A diet libc e' uma libc otimizada para criar pequenos binários
estaticamente linkados para Linux.

%package devel
Summary:	Development files for dietlibc
Summary(pl):	Pliki dla programistów u¿ywaj±cych dietlibc
Summary(pt_BR):	libc pequena otimizada para tamanho
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
Small libc for building embedded applications - development files.

%description devel -l pl
Niewielka libc do budowania aplikacji wbudowanych - pliki dla
programistów.

%package static
Summary:	Static libraries for dietlibc
Summary(pl):	Biblioteki statyczne dla dietlibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}

%description static
Small libc for building embedded applications - static libraries.

%description static -l pl
Niewielka libc do budowania aplikacji wbudowanych - biblioteki
statyczne.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
OPTFLAGS="%{rpmcflags}"; export OPTFLAGS
%ifarch sparc sparcv9
sparc32 \
%endif
%{__make} prefix=%{dietprefix} all
%ifarch %{ix86}
%{__make} prefix=%{dietprefix} dyn
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_mandir}/man1}

%ifarch sparc sparcv9
sparc32 \
%endif
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{dietprefix}

mv $RPM_BUILD_ROOT%{dietprefix}/bin/* $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{dietprefix}/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
rm -rf $RPM_BUILD_ROOT%{dietprefix}/{bin,man}
rm -f $RPM_BUILD_ROOT%{_bindir}/diet-dyn

cat > $RPM_BUILD_ROOT%{_bindir}/%{_target_cpu}-dietlibc-gcc <<EOF
#!/bin/sh
exec %{_bindir}/diet gcc "\$@"
EOF

rm -rf $RPM_BUILD_ROOT%{dietprefix}/include/{asm,linux}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc TODO README THANKS CAVEAT CHANGES FAQ BUGS AUTHOR
%dir %{dietprefix}
%dir %{dietprefix}/lib-%{libarch}
%ifarch %{ix86}
%attr(755,root,root) %{dietprefix}/lib-%{libarch}/*.so
%{_sysconfdir}/*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{dietprefix}/include
%attr(755,root,root) %{dietprefix}/lib-%{libarch}/*.o
%{_mandir}/man*/*

%files static
%defattr(644,root,root,755)
%{dietprefix}/lib-%{libarch}/*.a
