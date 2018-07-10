%define	major 1
%define libname %mklibname %{name}1_ %{major}
%define develname %mklibname %{name} -d
%define _disable_lto 1

Summary:	A high-performance asynchronous HTTP client library
Name:		serf
Version:	1.3.9
Release:	3
License:	Apache License
Group:		System/Libraries
URL:		http://code.google.com/p/serf/
Source0:	https://www.apache.org/dist/serf/%{name}-%{version}.tar.bz2
Patch0:		serf-1.3.9-lib64.patch
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(apr-util-1)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libxcrypt)
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
%if "%{_lib}" == "lib64"
%patch0 -p1 -b .lib64~
%endif

%build
%serverbuild
scons \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir} \
    APR=%{_prefix} \
    CC=%{__cc} \
    OPENSSL=%{_prefix} \
    ZLIB=%{_prefix} \
    CFLAGS="%{optflags}" \
    APR_STATIC=no

%scons

%check
# FIXME as of 1.3.9, checks fail -- needs to be debugged
#scons \
#    CFLAGS="%{optflags}" \
#    check

%install
scons install --install-sandbox=%{buildroot}

# enable strip and debug packages
chmod 755 %{buildroot}%{_libdir}/libserf*.so*

# No need to package static libs for now
rm %{buildroot}%{_libdir}/*.a

%files -n %{libname}
%doc CHANGES LICENSE NOTICE README design-guide.txt
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%{_includedir}/%{name}-%{major}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/serf-1.pc
