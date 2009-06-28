#
# Conditional build:
%bcond_with	ssp	# disable stack-smashing protector 'coz dietlibc will not work with it!
#
Summary:	C library optimized for size
Summary(pl.UTF-8):	Biblioteka standardowa C zoptymalizowana na rozmiar
Summary(pt_BR.UTF-8):	libc pequena otimizada para tamanho
Name:		dietlibc
Version:	0.32
Release:	1
Epoch:		2
License:	GPL v2
Group:		Development/Libraries
Source0:	http://www.kernel.org/pub/linux/libs/dietlibc/%{name}-%{version}.tar.bz2
# Source0-md5:	0098761c17924c15e21d25acdda4a8b5
Patch0:		%{name}-ppc.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-platform.patch
# workaround for http://gcc.gnu.org/PR26374
Patch3:		%{name}-gcc4.patch
Patch4:		%{name}-guard.patch
Patch5:		%{name}-arm.patch
Patch6:		%{name}-diet-m.patch
Patch7:		%{name}-nice.patch
Patch8:		%{name}-nostrip.patch
Patch9:		%{name}-stackgap-instead-of-ssp.patch
Patch10:	%{name}-fflush-null.patch
Patch11:	%{name}-_syscall-no-arch.patch
Patch12:	%{name}-noexecstacks.patch
Patch13:	%{name}-strcoll.patch
Patch15:	%{name}-memalign.patch
Patch16:	%{name}-getsubopt.patch
URL:		http://www.fefe.de/dietlibc/
%ifarch sparc sparcv9
BuildRequires:	sparc32
%endif
BuildRequires:	dos2unix
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dietprefix	%{_prefix}/lib/dietlibc
# for some reason known only to rpm there must be "\\|" not "\|" here
%define		libarch		%(echo %{_target_cpu} | sed -e 's/i.86\\|pentium.\\|athlon/i386/;s/amd64/x86_64/;s/armv.*/arm/;s/sparcv.*/sparc/')

%description
Small libc for building embedded applications.

%description -l pl.UTF-8
Niewielka libc do budowania aplikacji wbudowanych.

%description -l pt_BR.UTF-8
A diet libc e' uma libc otimizada para criar pequenos binários
estaticamente linkados para Linux.

%package devel
Summary:	Development files for dietlibc
Summary(pl.UTF-8):	Pliki dla programistów używających dietlibc
Summary(pt_BR.UTF-8):	libc pequena otimizada para tamanho
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Small libc for building embedded applications - development files.

%description devel -l pl.UTF-8
Niewielka libc do budowania aplikacji wbudowanych - pliki dla
programistów.

%package static
Summary:	Static libraries for dietlibc
Summary(pl.UTF-8):	Biblioteki statyczne dla dietlibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Small libc for building embedded applications - static libraries.

%description static -l pl.UTF-8
Niewielka libc do budowania aplikacji wbudowanych - biblioteki
statyczne.

%prep
%setup -q
dos2unix arm/md5asm.S
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%{!?with_ssp:%patch9 -p1}
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch15 -p1
%patch16 -p1

%build
export OPTFLAGS="%{rpmcflags}%{?with_ssp: -fno-stack-protector} -fno-strict-aliasing"
%ifarch sparc sparcv9
sparc32 \
%endif
%{__make} -j1 all \
	prefix=%{dietprefix} \
	CC="%{__cc}"
%ifarch %{ix86}
%{__make} -j1 dyn \
	prefix=%{dietprefix} \
	CC="%{__cc}"
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHOR BUGS CAVEAT CHANGES FAQ README THANKS TODO
%dir %{dietprefix}
%dir %{dietprefix}/lib-%{libarch}
%ifarch %{ix86}
%attr(755,root,root) %{dietprefix}/lib-%{libarch}/*.so
%{_sysconfdir}/diet.ld.conf
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*-dietlibc-gcc
%attr(755,root,root) %{_bindir}/diet
%attr(755,root,root) %{_bindir}/dnsd
%attr(755,root,root) %{_bindir}/elftrunc
%{dietprefix}/lib-%{libarch}/*.o
%{dietprefix}/include
%{_mandir}/man1/diet.1*

%files static
%defattr(644,root,root,755)
%{dietprefix}/lib-%{libarch}/*.a
