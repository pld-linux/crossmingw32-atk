%define		realname   atk
Summary:	ATK - Accessibility Toolkit - cross MinGW32 version
Summary(pl.UTF-8):	ATK - biblioteka ułatwiająca niepełnosprawnym korzystanie z komputerów - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	2.32.0
Release:	2
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/atk/2.32/%{realname}-%{version}.tar.xz
# Source0-md5:	c10b0b2af3c199e42caa6275b845c49d
URL:		https://developer.gnome.org/atk/
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-glib2 >= 2.32.0
# glib-genmarshal, glib-mkenums
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	meson >= 0.46.0
BuildRequires:	ninja
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	python >= 1:2.5
BuildRequires:	rpmbuild(macros) >= 1.737
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-glib2 >= 2.32.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}
# for meson 0.50+, keep __cc/__cxx as host compiler and pass %{target}-* in meson-cross.txt

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits. By
supporting the ATK interfaces, an application or toolkit can be used
as tools such as screen readers and magnifiers, and alternative input
devices.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Biblioteka ATK udostępnia zestaw interfejsów ułatwiających
niepełnosprawnym korzystanie z aplikacji i poszczególnych elementów
graficznego interfejsu użytkownika. Poprzez wykorzystanie interfejsów
ATK, aplikacja lub element interfejsu może być używany z takimi
narzędziami jak czytniki ekranu i narzędzia powiększające oraz
alternatywnymi urządzeniami wejściowymi.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static atk library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka atk (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static atk library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka atk (wersja skrośna MinGW32).

%package dll
Summary:	DLL atk library for Windows
Summary(pl.UTF-8):	Biblioteka DLL atk dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-glib2-dll >= 2.32.0
Requires:	wine

%description dll
DLL atk library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL atk dla Windows.

%prep
%setup -q -n %{realname}-%{version}

# enable static library
%{__sed} -i -e '/^libatk/ s/shared_library/library/' atk/meson.build

cat > meson-cross.txt <<'EOF'
[host_machine]
system = 'windows'
cpu_family = 'x86'
cpu = 'i386'
endian='little'
[binaries]
c = '%{target}-gcc'
ar = '%{target}-ar'
windres = '%{target}-windres'
pkgconfig = 'pkg-config'
[properties]
c_args = ['%(echo %{rpmcflags} | sed -e "s/ \+/ /g;s/ /', '/g")']
EOF

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%meson build \
	--cross-file meson-cross.txt \
	-Ddocs=false

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

# runtime
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%{_libdir}/libatk-1.0.dll.a
%{_includedir}/atk-1.0
%{_pkgconfigdir}/atk.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libatk-1.0.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libatk-1.0-*.dll
