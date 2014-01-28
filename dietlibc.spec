#
# Conditional build:
%bcond_without	ssp	# stack-smashing protector
%bcond_without	dynamic	# dynamic lib support

%ifnarch %{ix86} %{x8664} arm
%undefine	with_dynamic
%endif

Summary:	C library optimized for size
Summary(pl.UTF-8):	Biblioteka standardowa C zoptymalizowana na rozmiar
Summary(pt_BR.UTF-8):	libc pequena otimizada para tamanho
Name:		dietlibc
Version:	0.33
Release:	2
Epoch:		2
License:	GPL v2
Group:		Development/Libraries
Source0:	http://www.fefe.de/dietlibc/%{name}-%{version}.tar.bz2
# Source0-md5:	9d541b9a6623b04ec12e5248b82db7c0
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
Patch12:	%{name}-dynamic.patch
Patch13:	%{name}-strcoll.patch
Patch14:	umount-arch.patch
Patch15:	%{name}-memalign.patch
Patch16:	%{name}-getsubopt.patch
Patch17:	%{name}-devmacros.patch
Patch19:	%{name}-notify.patch
URL:		http://www.fefe.de/dietlibc/
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
%ifarch sparc sparcv9
BuildRequires:	sparc32
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dietprefix	%{_prefix}/lib/dietlibc
# for some reason known only to rpm there must be "\\|" not "\|" here
%define		libarch		%(echo %{_target_cpu} | sed -e 's/i.86\\|pentium.\\|athlon/i386/;s/amd64/x86_64/;s/armv.*/arm/;s/sparcv.*/sparc/')

%description
The diet libc is a libc that is optimized for small size. It can be
used to create small statically linked binaries for Linux on alpha,
arm, hppa, ia64, i386, mips, s390, sparc, sparc64, ppc and x86_64.

%description -l pl.UTF-8
diet libc to biblioteka libc zoptymalizowana pod kątem rozmiaru.
Może być używana do tworzenia małych, statycznie zlinkowanych
binariów dla Linuksa na architekturach alpha, arm, hppa, ia64, i386,
mips, s390, sparc, sparc64, ppc i x86_64.

%description -l pt_BR.UTF-8
A diet libc e' uma libc otimizada para criar pequenos binários
estaticamente linkados para Linux.

%package libs
Summary:	Shared dietlibc libraries
Summary(pl.UTF-8):	Biblioteki współdzielone dietlibc
Group:		Libraries

%description libs
This package contains the shared dietlibc libraries.

%description libs -l pl.UTF-8
Ten pakiet zawiera biblioteki współdzielone dietlibc.

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
%undos arm/md5asm.S
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
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch19 -p1

%if "%{cc_version}" < "3.4"
%{__sed} -i -e '/CFLAGS/ s/-Wextra//' Makefile
%endif

# there is unconditional nice.c already; __nice.c breaks x86_64 build
%{__rm} lib/__nice.c

%build
export OPTFLAGS="%{rpmcflags}%{?with_ssp: -fno-stack-protector} -fno-strict-aliasing -Wa,--noexecstack"
CC="%{__cc}"
%ifarch sparc sparcv9
sparc32 \
%endif
%{__make} -j1 all \
	prefix=%{dietprefix} \
	CC="${CC#*ccache }"

%if %{with dynamic}
# 'dyn' target is not SMP safe
%{__make} -j1 dyn \
	prefix=%{dietprefix} \
	CC="${CC}"
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
rm -f $RPM_BUILD_ROOT%{_bindir}/dnsd

cat > $RPM_BUILD_ROOT%{_bindir}/%{_target_cpu}-dietlibc-gcc <<'EOF'
#!/bin/sh
exec %{_bindir}/diet gcc "$@"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHOR BUGS CAVEAT CHANGES FAQ README THANKS TODO
%dir %{dietprefix}
%dir %{dietprefix}/lib-%{libarch}

%if %{with dynamic}
%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{dietprefix}/lib-%{libarch}/*.so
%{_sysconfdir}/diet.ld.conf
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*-dietlibc-gcc
%attr(755,root,root) %{_bindir}/diet
%attr(755,root,root) %{_bindir}/elftrunc
%{dietprefix}/lib-%{libarch}/*.o
%{dietprefix}/include
%{_mandir}/man1/diet.1*

%files static
%defattr(644,root,root,755)
%{dietprefix}/lib-%{libarch}/*.a
