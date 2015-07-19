%define url_ver	%(echo %{version}|cut -d. -f1,2)

# don't provide plugin .so
%global __provides_exclude_from %{_libdir}/gs-plugins-3/.*\\.so

Summary:	A software center for GNOME
Name:		gnome-software
Version:	3.16.1
Release:	2
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
BuildRequires:	gnome-common
BuildRequires:	autoconf
Requires:	adwaita-icon-theme

%description
%{name} is an application that makes it easy to add, remove
and update software in the GNOME desktop.

%prep
%setup -q

%build
autoreconf -vfi
%configure --disable-static
%make

%install
%makeinstall_std

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
%{_datadir}/%{name}/featured.ini
%dir %{_datadir}/%{name}/modulesets.d/
%{_datadir}/%{name}/modulesets.d/*.xml
%{_mandir}/man1/%{name}.1.*
%{_iconsdir}/*/*/apps/*
%{_datadir}/appdata/*.appdata.xml
%{_sysconfdir}/xdg/autostart/%{name}-service.desktop
%{_datadir}/dbus-1/services/org.gnome.Software.service
%{_datadir}/glib-2.0/schemas/org.gnome.software.gschema.xml
%{_datadir}/gnome-shell/search-providers/%{name}-search-provider.ini
%dir %{_libdir}/gs-plugins-*/
%{_libdir}/gs-plugins-*/*.so


%changelog
* Wed Oct 15 2014 umeabot <umeabot> 3.14.1-2.mga5
+ Revision: 750806
- Second Mageia 5 Mass Rebuild

* Mon Oct 13 2014 ovitters <ovitters> 3.14.1-1.mga5
+ Revision: 738315
- new version 3.14.1

* Sun Sep 28 2014 wally <wally> 3.14.0-1.mga5
+ Revision: 731360
- new version 3.14.0

  + umeabot <umeabot>
    - Mageia 5 Mass Rebuild

  + ovitters <ovitters>
    - new version 3.13.92

* Wed Sep 03 2014 ovitters <ovitters> 3.13.91-1.mga5
+ Revision: 671191
- new version 3.13.91

* Tue Aug 19 2014 fwang <fwang> 3.13.90-1.mga5
+ Revision: 665488
- update file list
- bump br

  + ovitters <ovitters>
    - new version 3.13.90

* Mon Aug 11 2014 fwang <fwang> 3.13.4-2.mga5
+ Revision: 661623
- rebuild for new packagekit

* Tue Jul 29 2014 ovitters <ovitters> 3.13.4-1.mga5
+ Revision: 657920
- new version 3.13.4

* Tue Jun 24 2014 ovitters <ovitters> 3.13.3-1.mga5
+ Revision: 639430
- new version 3.13.3

* Wed May 28 2014 wally <wally> 3.13.2-1.mga5
+ Revision: 627269
- exclude plugin .so from provides

  + ovitters <ovitters>
    - new version 3.13.2

* Mon May 12 2014 ovitters <ovitters> 3.12.2-1.mga5
+ Revision: 622159
- new version 3.12.2

  + wally <wally>
    - require adwaita-icon-theme instead of obsolete gnome-icon-theme

* Fri Apr 11 2014 ovitters <ovitters> 3.12.1-1.mga5
+ Revision: 613454
- new version 3.12.1

* Mon Mar 24 2014 ovitters <ovitters> 3.12.0-1.mga5
+ Revision: 607830
- new version 3.12.0

* Thu Mar 20 2014 ovitters <ovitters> 3.11.92-1.mga5
+ Revision: 606208
- new version 3.11.92

* Fri Mar 14 2014 dams <dams> 3.11.91-1.mga5
+ Revision: 603452
- use autoreconf

  + ovitters <ovitters>
    - new version 3.11.91
    - new version 3.11.90

* Thu Feb 06 2014 dams <dams> 3.11.5-1.mga5
+ Revision: 584124
- new version 3.11.5

* Tue Nov 26 2013 ovitters <ovitters> 3.10.4-1.mga4
+ Revision: 553516
- new version 3.10.4

* Mon Oct 28 2013 ovitters <ovitters> 3.10.3-1.mga4
+ Revision: 547637
- new version 3.10.3

* Tue Oct 22 2013 umeabot <umeabot> 3.10.2-2.mga4
+ Revision: 542209
- Mageia 4 Mass Rebuild

* Fri Oct 18 2013 ovitters <ovitters> 3.10.2-1.mga4
+ Revision: 520415
- new version 3.10.2

* Mon Oct 14 2013 ovitters <ovitters> 3.10.1-1.mga4
+ Revision: 497094
- new version 3.10.1

* Wed Sep 25 2013 ovitters <ovitters> 3.10.0-1.mga4
+ Revision: 485754
- based on Fedora

