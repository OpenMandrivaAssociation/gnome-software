%define url_ver	%(echo %{version}|cut -d. -f1,2)

# don't provide plugin .so
%global __provides_exclude_from %{_libdir}/gs-plugins-3/.*\\.so

%global plugin_major 16

#define _disable_ld_no_undefined 1
#define _disable_lto 1

Summary:	A software center for GNOME
Name:		gnome-software
Version:	40.4
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		https://wiki.gnome.org/Apps/Software
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	cmake
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(appstream)
BuildRequires:	pkgconfig(appstream-glib) >= 0.2.4
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.9.12
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(libdnf)
BuildRequires:	pkgconfig(libhandy-1)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(packagekit-glib2) >= 1.0.0
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(gsettings-desktop-schemas) >= 3.11.4
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(gspell-1)
BuildRequires:	autoconf
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(fwupd)
BuildRequires:	pkgconfig(flatpak)
BuildRequires:	pkgconfig(valgrind)
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(oauth)
BuildRequires:	gnome-common
BuildRequires:	meson
BuildRequires:	pkgconfig(xmlb)
BuildRequires:	pkgconfig(goa-1.0)
BuildRequires:  pkgconfig(gtk-doc)
Requires:	adwaita-icon-theme
Requires:	gnome-packagekit
Requires:	flatpak
Requires:	fwupd


%description
Gnome-software is an application that makes it easy to add, remove
and update software in the GNOME desktop.

%package devel
Summary: Headers for building external gnome-software plugins
Group:	Development/GNOME and GTK+
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
These development files are for building gnome-software plugins outside
the source tree. Most users do not need this subpackage installed.


%prep
%setup -q

%build
# with clang gnome-software dont want launch.
export CC=gcc
export CXX=g++

# Fix build error on GCC after linker switch to LDD.
%global ldflags %{ldflags} -fuse-ld=gold
# Fix build error at i686 with gcc and gold. 
%ifarch %{ix86}
%global ldflags %{ldflags} -Wl,-z,notext
%endif

%meson		\
	-Dmalcontent=false \
	-Denable-polkit=true \
	-Denable-gnome-desktop=true \
	-Dgsettings_desktop_schemas=enabled \
	-Denable-packagekit=true \
	-Denable-flatpak=true \
	-Denable-ostree=true \
	-Denable-rpm=true \
	-Denable-shell-extensions=true \
	-Denable-gudev=true \
	-Denable-webapps=true \
	-Dfwupd=true
%meson_build

%install
%meson_install

#we don't want these
find %{buildroot} -name "*.la" -delete

# remove unneeded static library
#rm %{buildroot}%{_libdir}/libgnomesoftware.a

desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

# set up for Mandriva
cat >> %{buildroot}%{_datadir}/glib-2.0/schemas/org.gnome.software-openmandriva.gschema.override << FOE
[org.gnome.software]
official-repos = [ 'cooker-*', 'main-*', 'unsupported-*', 'restricted-*', 'non-free-*' ]
FOE

%find_lang %name --with-gnome

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*.png
%{_iconsdir}/*/*/*/carousel-*.svg
%{_mandir}/man1/%{name}.1.*
%{_iconsdir}/*/*/apps/*
%{_iconsdir}/hicolor/scalable/status/software-installed-symbolic.svg
%{_datadir}/metainfo/org.gnome.Software.appdata.xml
%{_datadir}/metainfo/org.gnome.Software.Plugin.Fwupd.metainfo.xml
%{_sysconfdir}/xdg/autostart/%{name}-service.desktop
%{_datadir}/dbus-1/services/org.gnome.Software.service
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%{_datadir}/glib-2.0/schemas/org.gnome.software.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.software-openmandriva.gschema.override
%{_datadir}/gnome-shell/search-providers/*-search-provider.ini
%{_libexecdir}/gnome-software-cmd
%{_libexecdir}/gnome-software-restarter
#{_datadir}/metainfo/org.gnome.Software.Plugin.Epiphany.metainfo.xml
%{_datadir}/metainfo/org.gnome.Software.Plugin.Flatpak.metainfo.xml
%{_datadir}/metainfo/org.gnome.Software.Plugin.Odrs.metainfo.xml
%{_datadir}/app-info/xmls/org.gnome.Software.Featured.xml
%{_libdir}/%{name}/libgnomesoftware.so
%{_libdir}/%{name}/plugins-%{plugin_major}/libgs_plugin_*.so

%files devel
%{_libdir}/pkgconfig/gnome-software.pc
%dir %{_includedir}/gnome-software
%{_includedir}/gnome-software/*.h
%{_datadir}/gtk-doc/html/gnome-software
