#
# Conditional build:
%bcond_with	ssp	# disable stack-smashing protector 'coz dietlibc will not work with it!
#
Summary:	C library optimized for size
Summary(pl):	Biblioteka standardowa C zoptymalizowana na rozmiar
Summary(pt_BR):	libc pequena otimizada para tamanho
Name:		dietlibc
Version:	0.28
Release:	1
Epoch:		2
License:	GPL v2
Group:		Development/Libraries
Source0:	http://www.kernel.org/pub/linux/libs/dietlibc/%{name}-%{version}.tar.bz2
# Source0-md5:	5be8e221a438817f83f73d09ce655883
Source1:	%{name}-divrem.m4
Patch0:		%{name}-ppc.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-athlon.patch
Patch3:		%{name}-amd64.patch
Patch4:		%{name}-pentiumX.patch
URL:		http://www.fefe.de/dietlibc/
%ifarch sparc
BuildRequires:	m4
BuildRequires:	perl-base
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dietprefix	%{_prefix}/%{_target_cpu}-linux-dietlibc
# for some reason known only to rpm there must be "\\|" not "\|" here
%define		libarch		%(echo %{_target_cpu} | sed -e 's/i.86\\|pentium.\\|athlon/i386/;s/amd64/x86_64/')

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
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Small libc for building embedded applications - development files.

%description devel -l pl
Niewielka libc do budowania aplikacji wbudowanych - pliki dla
programistów.

%package static
Summary:	Static libraries for dietlibc
Summary(pl):	Biblioteki statyczne dla dietlibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Small libc for building embedded applications - static libraries.

%description static -l pl
Niewielka libc do budowania aplikacji wbudowanych - biblioteki
statyczne.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%ifarch sparc
# generate missing functions
(echo "define(NAME,\`.div')define(OP,\`div')define(S,\`true')"; cat %{SOURCE1}) \
	| m4 > sparc/sdiv.S
(echo "define(NAME,\`.rem')define(OP,\`rem')define(S,\`true')"; cat %{SOURCE1}) \
	| m4 > sparc/srem.S
%{__perl} -pi -e 's@(^LIBOBJ.*$)@$1 \$(OBJDIR)/sdiv.o \$(OBJDIR)/srem.o@' sparc/Makefile.add
%endif

%build
export OPTFLAGS="%{rpmcflags}%{?with_ssp: -fno-stack-protector} -fno-strict-aliasing"
%ifarch sparc sparcv9
sparc32 \
%endif
%{__make} all \
	prefix=%{dietprefix}
%ifarch %{ix86}
%{__make} dyn \
	prefix=%{dietprefix}
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
%doc AUTHOR BUGS CAVEAT CHANGES FAQ README THANKS TODO
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
