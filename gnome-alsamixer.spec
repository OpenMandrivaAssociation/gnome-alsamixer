%define	name	gnome-alsamixer
%define version 0.9.6
%define release %mkrel 5

Name:		%{name}
Summary:	An ALSA mixer for GNOME written for ALSA 0.9.x
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sound 
URL:		http://www.paw.co.za/projects/gnome-alsamixer/
Source0:	ftp://ftp.paw.co.za/pub/PAW/sources/%{name}-%{version}.tar.bz2
Source1:	gnome-alsamixer-nb.po.bz2
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}-48.png
Patch:	gnome-alsamixer-0.9.6-deprecation.patch.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	alsa-lib-devel >= 0.9.0 desktop-file-utils libgnomeui2-devel
BuildRequires: automake1.4

%description
A sound mixer for GNOME2 which is written for the Advanced Linux Sound
Architecture (ALSA), which supports ALSA 0.9.x.

%prep
%setup -q
%patch -p1
automake-1.4
bzcat %{SOURCE1} > po/nb.po

%build
export CPPFLAGS=-I%_includedir/alsa
%configure2_5x
%make
msgfmt po/nb.po -o po/nb.gmo

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
install -m644 po/nb.gmo -D $RPM_BUILD_ROOT%{_datadir}/locale/nb/LC_MESSAGES/%{name}.mo

# Menu
install -d $RPM_BUILD_ROOT%{_menudir}
cat <<EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%name): \
	command="%{name}" \
	needs="X11" \
	icon="%{name}.png" \
	section="Multimedia/Sound" \
	title="Gnome-ALSA-Mixer" \
	longtitle="A gnome ALSA Mixer" xdg="true"
EOF
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Gnome-ALSA-Mixer
Comment=A gnome ALSA Mixer
Exec=%{name}
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-Multimedia-Sound;Audio;Mixer;GTK;GNOME;
EOF

# icon
install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

%{find_lang} %{name}

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-, root, root)
%doc COPYING ChangeLog AUTHORS INSTALL 
%{_bindir}/%{name}
%{_datadir}/applications/mandriva*
%{_datadir}/pixmaps/*
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
