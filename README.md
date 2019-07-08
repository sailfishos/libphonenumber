# Sailfish OS libphonenumber package

This package contains Google's libphonenumber, with a few minor modifications that make it fit better with Sailfish OS:

* Alternate formats are OFF, since we won't need them in the foreseeable future.
* The geocoding library currently not built, in order to save space. It is of limited usefulness, since it only works in countries where the phone numbers correlate with your geographic location.
* We don't want to regenerate the metadata during the build, since we don't have java in our build system.
* We link to `protobuf-lite` instead of full `protobuf` in order to save space on the default OS install.

## Note about ports

libphonenumber has been ported to multiple languages, the official source tree contains several of these. We only package the C++ version.

## Note about metadata

The metadata contains a huge database of phone number related information for most countries of the world. It is located in a few **huge** XML files which are turned into protobuf-based C++ code by a java tool.
Fortunately, the authors keep the C++ version of the metadata in the source tree so we can skip re-generating it.
If, for any reason, the C++ metadata is out of date with the XML, it needs manual intervention and you have to create a patch to this package after running the code generation tool manually.

