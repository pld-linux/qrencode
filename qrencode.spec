#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	QR Code encoder into PNG image
Summary(pl.UTF-8):	Koder kodu QR do obrazów PNG
Name:		qrencode
Version:	4.0.2
Release:	1
License:	LGPL v2.1+
Group:		Applications/File
Source0:	https://fukuchi.org/works/qrencode/%{name}-%{version}.tar.bz2
# Source0-md5:	3eb64357f6fbdb68c27cb2e44e97280a
URL:		https://fukuchi.org/works/qrencode/index.en.html
BuildRequires:	SDL2-devel >= 2.0.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libpng-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qrencode is a utility software using libqrencode to encode string data
in a QR Code and save as a PNG image.

%description -l pl.UTF-8
Qrencode to program wykorzystujący libqrencode do kodowania danych
tekstowych w postaci kodu QR i zapisywania do obrazu PNG.

%package libs
Summary:	A C library for encoding data in a QR Code symbol
Summary(pl.UTF-8):	Biblioteka C do kodowania danych w postaci symboli kodu QR
Group:		Libraries

%description libs
Libqrencode is a C library for encoding data in a QR Code symbol, a
kind of 2D symbology that can be scanned by handy terminals such as a
mobile phone with CCD. The capacity of QR Code is up to 7000 digits or
4000 characters, and is highly robustness.

Libqrencode supports QR Code model 2, described in JIS (Japanese
Industrial Standards) X0510:2004 or ISO/IEC 18004.

%description libs -l pl.UTF-8
Libqrencode to biblioteka C do kodowania danych w postaci symboli kodu
QR. Są to dwuwymiarowe symbole, które można skanować podręcznymi
terminalami, takimi jak telefony komórkowe z czujnikiem CCD. Pojemność
kodu QR wynosi do 7000 cyfr lub 4000 znaków.

Libqrencode obsługuje kod QR w modelu 2, opisany w japońskim
standardzie JIS X0510:2004 oraz w ISO/IEC 18004.

%package devel
Summary:	The development files for the qrencode library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki qrencode
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Libqrencode is a C library for encoding data in a QR Code symbol, a
kind of 2D symbology that can be scanned by handy terminals such as a
mobile phone with CCD. The capacity of QR Code is up to 7000 digits or
4000 characters, and is highly robustness.

Libqrencode supports QR Code model 2, described in JIS (Japanese
Industrial Standards) X0510:2004 or ISO/IEC 18004.

This package contains the development files for the qrencode library.

%description devel -l pl.UTF-8
Libqrencode to biblioteka C do kodowania danych w postaci symboli kodu
QR. Są to dwuwymiarowe symbole, które można skanować podręcznymi
terminalami, takimi jak telefony komórkowe z czujnikiem CCD. Pojemność
kodu QR wynosi do 7000 cyfr lub 4000 znaków.

Libqrencode obsługuje kod QR w modelu 2, opisany w japońskim
standardzie JIS X0510:2004 oraz w ISO/IEC 18004.

Ten pakiet zawiera pliki programistyczne biblioteki qrencode.

%package static
Summary:	Static qrencode library
Summary(pl.UTF-8):	Statyczna biblioteka qrencode
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static qrencode library.

%description static -l pl.UTF-8
Statyczna biblioteka qrencode.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static} \
	--with-tests

%{__make}

# manual
doxygen

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

install -d $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libqrencode.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libqrencode.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libqrencode.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qrencode
%{_mandir}/man1/qrencode.1*

%files libs
%defattr(644,root,root,755)
%doc ChangeLog NEWS README TODO
%attr(755,root,root) /%{_lib}/libqrencode.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libqrencode.so.4

%files devel
%defattr(644,root,root,755)
%doc html/*.{css,html,js,png}
%attr(755,root,root) %{_libdir}/libqrencode.so
%{_includedir}/qrencode.h
%{_pkgconfigdir}/libqrencode.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libqrencode.a
%endif
