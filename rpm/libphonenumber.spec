Name:           libphonenumber
Summary:        A library for manipulating international phone numbers
Version:        8.13.6
Release:        1
License:        ASL 2.0 and BSD and MIT
URL:            https://github.com/google/libphonenumber
Source0:        %{name}-%{version}.tar.gz
Patch0:         0001-Ensure-build-reproducibility.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  protobuf-compiler
BuildRequires:  pkgconfig(protobuf-lite)
BuildRequires:  abseil-cpp-devel
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(gtest)

%description
Google's common Java, C++ and Javascript library for parsing,
formatting, storing and validating international phone numbers. The
Java version is optimized for running on smartphones, and is used by
the Android framework since 4.0 (Ice Cream Sandwich).

%package geocoding
Summary:        Geocoding library of %{name}
Requires:       %{name} = %{version}

%description geocoding
Contains geocoding information of %{name}, which can be used to
decide which phone number belongs to which region.

%package doc
Summary:        Documentation of %{name}
BuildArch:      noarch

%description doc
Contains documentation files of %{name}.

%package devel
Summary:        Development package of %{name}
Requires:       %{name} = %{version}
Requires:       %{name}-geocoding = %{version}
Requires:       abseil-cpp-devel
Requires:       pkgconfig(protobuf-lite)

%description devel
Contains files needed to development with %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build

# Explanation of cmake options:
# BUILD_GEOCODER=ON - enable the geocoder library
# REGENERATE_METADATA=OFF - don't regenerate metadata with the java based tool
# USE_ALTERNATE_FORMATS=OFF - we don't want to use alternate formatting
# USE_PROTOBUF_LITE=ON - link to protobuf-lite to save some disk space
# USE_ICU_REGEXP=ON - Use ICU regexes
# USE_LITE_METADATA=ON - remove some unnecessary data, see https://github.com/google/libphonenumber/blob/master/FAQ.md#what-is-the-metadatalitejsmetadata_lite-option
# USE_RE2=OFF - don't use google's re2 library (ICU is already in our default install, RE2 isn't)
# BUILD_STATIC_LIB=OFF - we don't need static libraries
# CMAKE_BUILD_TYPE=RelWithDebInfo - among other things this helps to achieve build reproducibility by defining the NDEBUG macro

touch cpp/src/phonenumbers/test_metadata.h
%cmake -DBUILD_GEOCODER=ON \
       -DREGENERATE_METADATA=OFF \
       -DUSE_ALTERNATE_FORMATS=OFF \
       -DUSE_PROTOBUF_LITE=ON \
       -DUSE_ICU_REGEXP=ON \
       -DUSE_LITE_METADATA=ON \
       -DUSE_RE2=OFF \
       -DBUILD_STATIC_LIB=OFF \
       -DBUILD_TESTING=OFF \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_CXX_STANDARD=17 \
       cpp

%make_build

%install
%make_install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%license cpp/LICENSE
%license LICENSE.Chromium
%{_libdir}/libphonenumber.so.*

%files geocoding
%defattr(-, root, root, -)
%{_libdir}/libgeocoding.so.*

%files doc
%defattr(-, root, root, -)
%doc AUTHORS
%doc CONTRIBUTORS
%doc README.md
%doc FALSEHOODS.md
%doc cpp/README

%files devel
%defattr(-, root, root, -)
%{_includedir}/phonenumbers
%{_libdir}/cmake/libphonenumber
%{_libdir}/libphonenumber.so
%{_libdir}/libgeocoding.so
