%define	major 0
%define libname %mklibname %{name}1_ %{major}
%define develname %mklibname %{name} -d

Summary:	A high-performance asynchronous HTTP client library
Name:		serf
Version:	1.1.0
Release:	1
License:	Apache License
Group:		System/Libraries
URL:		http://code.google.com/p/serf/
Source0:	http://serf.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(apr-util-1)
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig(openssl)
BuildRequires:	zlib-devel
BuildRequires:	db-devel

%description
The serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package -n	%{libname}
Summary:	A high-performance asynchronous HTTP client library
Group:		System/Libraries

%description -n	%{libname}
The serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package -n	%{develname}
Summary:	Development libraries and headers for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
The serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

This package contains all of the development files that you will need in order
to compile %{name} applications.

%prep
%setup -q

# don't link against ldap libs
perl -pi -e "s|apu_config --link-libtool --libs|apu_config --link-ld --avoid-ldap --libs|g" configure*

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

# no static builds
perl -pi -e "s|-static||g" Makefile*

%build
%serverbuild
export CFLAGS="$CFLAGS -fPIC"

%configure2_5x --disable-static

%make

%check
make check

%install
%makeinstall_std

# enable strip and debug packages
chmod 755 %{buildroot}%{_libdir}/libserf*.so*

%files -n %{libname}
%doc CHANGES LICENSE NOTICE README design-guide.txt
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/serf-1.pc

%changelog
* Sun Mar 27 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7.2-1mdv2011.0
+ Revision: 648633
- 0.7.2

* Sun Feb 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7.1-1
+ Revision: 636366
- 0.7.1

* Sun Jan 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-3mdv2011.0
+ Revision: 627641
- don't force the usage of automake1.7

* Thu Dec 02 2010 Paulo Andrade <pcpa@mandriva.com.br> 0.7.0-2mdv2011.0
+ Revision: 605059
- Rebuild with apr with workaround to issue with gcc type based alias analysis

* Sun Oct 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-1mdv2011.0
+ Revision: 582649
- 0.7.0

* Thu Apr 08 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.3.1-4mdv2010.1
+ Revision: 533209
- resubmit due to BS weirdness

* Wed Apr 07 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.3.1-3mdv2010.1
+ Revision: 532836
- rebuild for new openssl-1.0.0

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-2mdv2010.1
+ Revision: 511637
- rebuilt against openssl-0.9.8m

* Tue Feb 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-1mdv2010.1
+ Revision: 506520
- 0.3.1

* Sat Jun 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-2mdv2010.0
+ Revision: 383254
- rebuilt against new apr/apr-util libs

* Sat Mar 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-1mdv2009.1
+ Revision: 359994
- 0.3.0

* Mon Dec 15 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-4mdv2009.1
+ Revision: 314525
- rebuilt to make it pickup the correct bdb in the libserf-0.la file...

* Sun Nov 23 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-3mdv2009.1
+ Revision: 305988
- more backport fixes

* Fri Nov 21 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-2mdv2009.1
+ Revision: 305515
- fix linkage

* Wed Aug 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-1mdv2009.0
+ Revision: 264250
- import serf


* Wed Aug 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-1mdv2009.0
- initial Mandriva package
