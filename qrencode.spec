Summary:	QR Code encoder into PNG image
Name:		qrencode
Version:	3.1.1
Release:	1
License:	LGPL v2+
Group:		Applications/File
URL:		http://megaui.net/fukuchi/works/qrencode/index.en.html
Source0:	http://megaui.net/fukuchi/works/qrencode/%{name}-%{version}.tar.bz2
# Source0-md5:	e7feb2c2c65d0f2f4010a14da3ecdb89
Patch0:		%{name}-libpng.patch
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qrencode is a utility software using libqrencode to encode string data
in a QR Code and save as a PNG image.

%package libs
Summary:	A C library for encoding data in a QR Code symbol
Group:		Libraries

%description libs
Libqrencode is a C library for encoding data in a QR Code symbol, a
kind of 2D symbology that can be scanned by handy terminals such as a
mobile phone with CCD. The capacity of QR Code is up to 7000 digits or
4000 characters, and is highly robustness.

Libqrencode supports QR Code model 2, described in JIS (Japanese
Industrial Standards) X0510:2004 or ISO/IEC 18004.

%package devel
Summary:	The development files for the qrencode library
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

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-tests \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# manual
doxygen

# clean
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qrencode
%{_mandir}/man1/qrencode.1*

%files libs
%defattr(644,root,root,755)
%doc COPYING ChangeLog NEWS README TODO html
%attr(755,root,root) %ghost %{_libdir}/libqrencode.so.3
%attr(755,root,root) %{_libdir}/libqrencode.so.*.*.*


%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqrencode.so
%{_includedir}/qrencode.h
%{_pkgconfigdir}/libqrencode.pc
