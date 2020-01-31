Name:		geos
Version:	3.8.0
Release:	mtx.5%{?dist}
Summary:	GEOS is a C++ port of the Java Topology Suite

License:	LGPLv2
URL:		http://trac.osgeo.org/geos/
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	doxygen
BuildRequires:	libtool
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc-c++

%global pkg_libgeos	libgeos38
%global pkg_libgeos_c1	libgeos38_c1
%global pkg_devel	geos-devel

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

%package -n %pkg_libgeos_c1
Summary:	C language interface for the GEOS library

%description -n %pkg_libgeos_c1
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

%post -n %pkg_libgeos_c1
/sbin/ldconfig

%postun -n %pkg_libgeos_c1
/sbin/ldconfig

%files -n %pkg_libgeos_c1
%defattr(-,root,root,-)
%{_libdir}/libgeos_c*.so.*

%package -n %pkg_libgeos
Summary:	GEOS is a C++ port of the Java Topology Suite

%description -n %pkg_libgeos
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

%post -n %pkg_libgeos
/sbin/ldconfig

%postun -n %pkg_libgeos
/sbin/ldconfig

%files -n %pkg_libgeos
%defattr(-,root,root,-)
%{_libdir}/libgeos-*.so

%package -n %pkg_devel
Summary:	Development files for GEOS
Requires:	%pkg_libgeos = %{version}-%{release}
Requires:	%pkg_libgeos_c1 = %{version}-%{release}
Obsoletes:	geos36-devel >= 3.6.0
Provides:	geos36-devel >= 3.6.0

%description -n %pkg_devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

This package contains the development files to build applications that
use GEOS

%files -n %pkg_devel
%doc AUTHORS COPYING NEWS README.md
%defattr(-,root,root,-)
%doc doc/doxygen_docs
%{_bindir}/geos-config
%{_includedir}/*
%{_libdir}/libgeos.so
%{_libdir}/libgeos_c.so
%exclude %{_libdir}/*.la

%prep
%setup -q -n %{name}-%{version}
autoreconf -fi

%build
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--disable-static \
	--disable-dependency-tracking \
	--disable-python
# Touch the file, since we are not using ruby bindings anymore:
# Per http://lists.osgeo.org/pipermail/geos-devel/2009-May/004149.html
touch swig/python/geos_wrap.cxx

%{__make} %{?_smp_mflags}

# Make doxygen documentation files
cd doc
%{__make} doxygen-html

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}



%changelog
%changelog
* Fri Oct 11 2019 Devrim Gündüz <devrim@gunduz.org> - 3.8.0
- Update to 3.8.0

* Sat Oct 5 2019 John K. Harvey <john.harvey@crunchydata.com> - 3.8.0rc2_2
- Small Provides: fix to support legacy postgis22 / 23

* Fri Oct 4 2019 Devrim Gündüz <devrim@gunduz.org> - 3.8.0rc2
- Initial packaging of 3.8 for PostgreSQL RPM Repository,
  which is to satisfy PostGIS on older platforms, so that
  users can benefit from all PostGIS features.
