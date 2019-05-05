%define url_ver	%(echo %{version}|cut -d. -f1,2)

# don't provide plugin .so
%global __provides_exclude_from %{_libdir}/gs-plugins-3/.*\\.so

Summary:	A software center for GNOME
Name:		gnome-software
Version:	3.32.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		https://wiki.gnome.org/Apps/Software
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(appstream-glib) >= 0.2.4
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.9.12
BuildRequires:	pkgconfig(sqlite3)
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
BuildRequires:	pkgconfig(flatpak)
BuildRequires:	pkgconfig(valgrind)
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(oauth)
BuildRequires:	gnome-common
BuildRequires:	meson
Requires:	adwaita-icon-theme
Requires:	gnome-packagekit
Requires:	flatpak


%description
%{name} is an application that makes it easy to add, remove
and update software in the GNOME desktop.

%prep
%setup -q

%build
export CC=gcc
export CXX=g++

%meson		\
	-Denable-polkit=true \
	-Denable-gnome-desktop=true \
	-Denable-packagekit=true \
	-Denable-flatpak=true \
	-Denable-ostree=true \
	-Denable-rpm=true \
	-Denable-shell-extensions=true \
	-Denable-gudev=true \
	-Denable-webapps=true \
	-Dfwupd=false
%meson_build

%install
%meson_install

#we don't want these
find %{buildroot} -name "*.la" -delete

desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%find_lang %name --with-gnome

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.svg
%{_datadir}/%{name}/featured.ini
%dir %{_datadir}/%{name}/modulesets.d/
%{_datadir}/%{name}/modulesets.d/*.xml
%{_mandir}/man1/%{name}.1.*
%{_iconsdir}/*/*/apps/*
%{_datadir}/appdata/*.appdata.xml
%{_sysconfdir}/xdg/autostart/%{name}-service.desktop
%{_datadir}/dbus-1/services/org.gnome.Software.service
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%{_datadir}/glib-2.0/schemas/org.gnome.software.gschema.xml
%{_datadir}/gnome-shell/search-providers/%{name}-search-provider.ini
%dir %{_libdir}/gs-plugins-*/
%{_libdir}/gs-plugins-*/*.so

