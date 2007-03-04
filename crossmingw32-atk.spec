#
%define		_realname   atk
Summary:	ATK - Accessibility Toolkit - cross Mingw32 version
Summary(pl.UTF-8):	ATK - biblioteka ułatwiająca niepełnosprawnym korzystanie z komputerów - wersja skrośna dla Mingw32
Summary(pt_BR.UTF-8):	Interfaces para suporte a acessibilidade
Name:		crossmingw32-%{_realname}
Version:	1.12.4
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/atk/1.12/%{_realname}-%{version}.tar.bz2
# Source0-md5:	0a2c6a7bbc380e3a3d94e9061f76a849
URL:		http://developer.gnome.org/projects/gap/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	crossmingw32-gettext
BuildRequires:	crossmingw32-glib2 >= 2.12.4
BuildRequires:	crossmingw32-pkgconfig
BuildRequires:	libtool >= 2:1.5.16
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	crossmingw32-glib2 >= 2.12.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits. By
supporting the ATK interfaces, an application or toolkit can be used
as tools such as screen readers and magnifiers, and alternative input
devices.

%description -l pl.UTF-8
Biblioteka ATK udostępnia zestaw interfejsów ułatwiających
niepełnosprawnym korzystanie z aplikacji i poszczególnych elementów
graficznego interfejsu użytkownika. Poprzez wykorzystanie
interfejsów ATK, aplikacja lub element interfejsu może być używany
z takimi narzędziami jak czytniki ekranu i narzędzia powiększające
oraz alternatywnymi urządzeniami wejściowymi.

%description -l pt_BR.UTF-8
A biblioteca ATK provê um conjunto de interfaces para adicionar
suporte a acessibilidade para aplicações e interfaces gráficas.
Suportando a interface ATK, uma aplicação ou interface gráfica pode
ser utilizada como ferramentas de leitura e aumento de tela,
dispositivos de entrada alternativos, etc.

%prep
%setup -q -n %{_realname}-%{version}

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-gtk-doc \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang atk10

%clean
rm -rf $RPM_BUILD_ROOT

%files -f atk10.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_bindir}/*.dll
%{_includedir}/atk*
%{_pkgconfigdir}/atk*
