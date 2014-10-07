%define	major 1
%define libname %mklibname %{name}1_ %{major}
%define develname %mklibname %{name} -d

Summary:	A high-performance asynchronous HTTP client library
Name:		serf
Version:	1.3.7
Release:	1
License:	Apache License
Group:		System/Libraries
URL:		http://code.google.com/p/serf/
Source0:	http://serf.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(apr-util-1)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	zlib-devel
BuildRequires:	db-devel
BuildRequires:	openldap-devel
BuildRequires:	scons

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

%build
%serverbuild
scons \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir} \
    APR=%{_prefix} \
    CC=%{__cc} \
    OPENSSL=%{_prefix} \
    ZLIB=%{_prefix} \
    DEBUG=yes \
    CFLAGS="%{optflags}" \
    APR_STATIC=no

%scons

%check
%scons \
    CFLAGS="%{optflags}" \
    check

%install
scons install --install-sandbox=%{buildroot}

# enable strip and debug packages
chmod 755 %{buildroot}%{_libdir}/libserf*.so*

# Don't ship static libs
rm -fR %{buildroot}%{_libdir}/*.a
rm -fR %{buildroot}%{_libdir}/*.la

%files -n %{libname}
%doc CHANGES LICENSE NOTICE README design-guide.txt
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%{_includedir}/%{name}-%{major}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/serf-1.pc
