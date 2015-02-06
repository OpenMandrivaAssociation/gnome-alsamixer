%define	name	gnome-alsamixer
%define version 0.9.7
# Many other major distros are also using SVN snapshots (inc. Debian).
# It includes useful updates and apparently no regressions from 0.9.6.
# - AdamW 2007/06
%define svn	205
%if %svn
%define release %mkrel 0.%svn.5
%else
%define release 5
%endif
%define schemas %name

Name:		%{name}
Summary:	ALSA mixer (volume control) for GNOME
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sound 
URL:		http://www.paw.co.za/projects/gnome-alsamixer/
%if %svn
Source0:	%{name}-%{svn}.tar.bz2
%else
Source0:	ftp://ftp.paw.co.za/pub/PAW/sources/%{name}-%{version}.tar.bz2
%endif
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}-48.png
Patch0:	gnome-alsamixer-0.9.6-deprecation.patch
# From ALT Linux: introduce the gconf schema, which is missing 
# upstream, and correct the paths to it - AdamW 2007/06
Patch1:	change_gconf-keys_path.diff
Patch2:	gnome-alsamixer.schemas.diff
BuildRequires:	alsa-oss-devel >= 0.9.0 pkgconfig(libgnomeui-2.0)
%if %svn
BuildRequires:	autoconf
%else
BuildRequires:	automake1.4
%endif

%description
A sound mixer (volume control) for ALSA, built for the GNOME desktop
environment.

%prep
%if %svn
%setup -q -n %{name}
%else
%setup -q
%endif
%patch0 -p1 -b .deprecated
%patch1 -p1 -b .gconf_keys
%patch2 -p1 -b .schema

%build
%if %svn
./autogen.sh
%else
automake-1.4
%endif
export CPPFLAGS=-I%_includedir/alsa
%configure2_5x --disable-schemas-install
%make LIBS="-lm"

%install
%makeinstall_std

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GNOME ALSA mixer
Comment=GNOME ALSA mixer (volume control)
Exec=%{name}
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=Audio;Mixer;GTK;GNOME;
EOF

# icon
install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%{find_lang} %{name}


%preun
%preun_uninstall_gconf_schemas %{schemas}

%files -f %name.lang
%doc COPYING ChangeLog AUTHORS INSTALL 
%{_bindir}/%{name}
%{_sysconfdir}/gconf/schemas/%name.schemas
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/pixmaps/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
