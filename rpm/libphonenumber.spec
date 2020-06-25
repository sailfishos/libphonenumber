Name:           libphonenumber
Summary:        A library for manipulating international phone numbers
Version:        8.12.6
Release:        1
License:        ASL 2.0 and BSD and MIT
URL:            https://github.com/googlei18n/libphonenumber/
Source0:        %{name}-%{version}.tar.gz

# Submitted upstream: https://github.com/google/libphonenumber/pull/2363
# https://github.com/google/libphonenumber/pull/2482
Patch1:        0001-Add-ability-for-the-C-library-to-link-against-protob.patch

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
%autosetup -p1 -n %{name}-%{version}/%{name}

%build

# Explanation of cmake options:
# BUILD_GEOCODER=OFF - we currently don't need the offline geocoder library
# USE_ALTERNATE_FORMATS=OFF - we don't want to use alternate formatting
# USE_LITE_METADATA=OFF - remove some unnecessary data, see https://github.com/google/libphonenumber/blob/master/FAQ.md#what-is-the-metadatalitejsmetadata_lite-option
# USE_ICU_REGEXP=ON - Use ICU regexes
# USE_RE2=OFF - don't use google's re2 library (ICU is already in our default install, RE2 isn't)
# USE_PROTOBUF_LITE=ON - link to protobuf-lite to save some disk space
# REGENERATE_METADATA=OFF - don't regenerate metadata with the java based tool

%cmake -DCMAKE_PROGRAM_PATH=$PWD/.. \
       -DCMAKE_CXX_STANDARD=11 \
       -DBUILD_GEOCODER=OFF \
       -DUSE_ALTERNATE_FORMATS=OFF \
       -DUSE_LITE_METADATA=ON \
       -DUSE_ICU_REGEXP=ON \
       -DUSE_RE2=OFF \
       -DUSE_PROTOBUF_LITE=ON \
       -DREGENERATE_METADATA=OFF \
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
