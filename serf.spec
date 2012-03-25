%define	major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A high-performance asynchronous HTTP client library
Name:		serf
Version:	1.0.3
Release:	1
License:	Apache License
Group:		System/Libraries
URL:		http://code.google.com/p/serf/
Source0:	http://serf.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	db2-devel

%description
The serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package -n	%{libname}
Summary:	A high-performance asynchronous HTTP client library
Group:          System/Libraries

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
perl -pi -e "s|apu_config --link-libtool --libs|apu_config --link-libtool --avoid-ldap --libs|g" configure*

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

# no static builds
perl -pi -e "s|-static||g" Makefile*

%build
%serverbuild
export CFLAGS="$CFLAGS -fPIC"

%configure2_5x

%make

#%%check
#make check

%install
%makeinstall_std

# enable strip and debug packages
chmod 755 %{buildroot}%{_libdir}/libserf*.so*

%files -n %{libname}
%doc CHANGES LICENSE NOTICE README design-guide.txt
%attr(0755,root,root) %{_libdir}/libserf-%{major}.so.*

%files -n %{develname}
%attr(0644,root,root) %{_includedir}/*.h
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.*a
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
