Name:           libphonenumber
Version:        8.10.14
Release:        1
License:        Apache-2.0
Summary:        A library for manipulating international phone numbers
URL:           https://github.com/googlei18n/libphonenumber/
Source0:       %{name}-%{version}.tar.gz

# Submitted upstream: https://github.com/google/libphonenumber/pull/2363
Patch1:        0001-Add-ability-for-the-C-library-to-link-against-protob.patch
Patch2:        0002-Add-build-option-to-disable-regenerating-the-metadat.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  gtest-devel
BuildRequires:  protobuf-lite-devel
BuildRequires:  protobuf-compiler
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(icu-i18n)

Requires:  protobuf-lite

%description
Google's common Java, C++ and Javascript library for parsing,
formatting, storing and validating international phone numbers. The
Java version is optimized for running on smartphones, and is used by
the Android framework since 4.0 (Ice Cream Sandwich).

%package doc
Summary:        Documentation of %{name}

%description doc
Contains documentation files of %{name}.

%package devel
Summary:        Development package of %{name}
Requires:       libphonenumber = %{version}
Requires:       protobuf-devel

%description devel
Contains files needed to development with %{name}.

%prep
%setup -q -n %{name}-%{version}/%{name}
%patch1 -p1
%patch2 -p1

%build

# Explanation of cmake options:
# BUILD_GEOCODER=OFF - we currently don't need the offline geocoder library
# USE_ALTERNATE_FORMATS=OFF - we don't want to use alternate formatting
# USE_LITE_METADATA=OFF - remove some unnecessary data, see https://github.com/google/libphonenumber/blob/master/FAQ.md#what-is-the-metadatalitejsmetadata_lite-option
# USE_ICU_REGEXP=ON - Use ICU regexes
# USE_RE2=OFF - don't use google's re2 library (ICU is already in our default install, RE2 isn't)
# USE_PROTOBUF_LITE=ON - link to protobuf-lite to save some disk space
# REGENERATE_METADATA=OFF - don't regenerate metadata with the java based tool

cmake -DCMAKE_SKIP_RPATH=ON \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_CXX_STANDARD=11 \
      -DCMAKE_PROGRAM_PATH=$PWD/.. \
      -DBUILD_GEOCODER=OFF \
      -DUSE_ALTERNATE_FORMATS=OFF \
      -DUSE_LITE_METADATA=ON \
      -DUSE_ICU_REGEXP=ON \
      -DUSE_RE2=OFF \
      -DUSE_PROTOBUF_LITE=ON \
      -DREGENERATE_METADATA=OFF \
      cpp

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}/%{_libdir}/*.a

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%license LICENSE
%doc AUTHORS
%doc README.md
%{_libdir}/libphonenumber.so.*

%files doc
%doc AUTHORS
%doc CONTRIBUTORS
%doc README.md
%doc FALSEHOODS.md

%files devel
%defattr(-, root, root, -)
%dir %{_includedir}/phonenumbers
%dir %{_includedir}/phonenumbers/base
%dir %{_includedir}/phonenumbers/base/memory
%dir %{_includedir}/phonenumbers/base/synchronization
%dir %{_includedir}/phonenumbers/utf
%{_includedir}/phonenumbers/*.h
%{_includedir}/phonenumbers/base/*.h
%{_includedir}/phonenumbers/base/memory/*.h
%{_includedir}/phonenumbers/base/synchronization/*.h
%{_includedir}/phonenumbers/utf/*.h
%{_libdir}/libphonenumber.so

