Name:           libphonenumber
Summary:        A library for manipulating international phone numbers
Version:        8.12.12
Release:        1
License:        ASL 2.0 and BSD and MIT
URL:            https://github.com/googlei18n/libphonenumber/
Source0:        %{name}-%{version}.tar.gz

# Submitted upstream: https://github.com/google/libphonenumber/pull/2363
# https://github.com/google/libphonenumber/pull/2482
Patch1:        0001-Add-ability-for-the-C-library-to-link-against-protob.patch

# https://github.com/google/libphonenumber/pull/2556
Patch2:        0001-Fix-geocoding-build-when-static-libraries-are-off.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  protobuf-compiler
BuildRequires:  protobuf-lite-devel
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(gtest)
Requires:  protobuf-lite

%description
Google's common Java, C++ and Javascript library for parsing,
formatting, storing and validating international phone numbers. The
Java version is optimized for running on smartphones, and is used by
the Android framework since 4.0 (Ice Cream Sandwich).

%package geocoding
Summary:        Geocoding library of %{name}
Requires:       %{name} = %{version}

%package doc
Summary:        Documentation of %{name}
BuildArch:      noarch

%description geocoding
Contains geocoding information of %{name}, which can be used to
decide which phone number belongs to which region.

%description doc
Contains documentation files of %{name}.

%package devel
Summary:        Development package of %{name}
Requires:       %{name} = %{version}
Requires:       %{name}-geocoding = %{version}
Requires:       protobuf-devel

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

%cmake -DBUILD_GEOCODER=ON \
       -DREGENERATE_METADATA=OFF \
       -DUSE_ALTERNATE_FORMATS=OFF \
       -DUSE_PROTOBUF_LITE=ON \
       -DUSE_ICU_REGEXP=ON \
       -DUSE_LITE_METADATA=ON \
       -DUSE_RE2=OFF \
       -DBUILD_STATIC_LIB=OFF \
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
%{_libdir}/libphonenumber.so
%{_libdir}/libgeocoding.so
