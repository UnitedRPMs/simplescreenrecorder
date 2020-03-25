%define shortname ssr
%global debug_package %{nil}
%global commit0 0b17180525a16f8126fd645418c9213649a503e0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           simplescreenrecorder
Version:        0.3.11
Release:        5%{?gver}%{dist}
Summary:        SimpleScreenRecorder is a screen recorder for Linux

License:        GPLv3
URL:            http://www.maartenbaert.be/simplescreenrecorder/
Source0:        https://github.com/MaartenBaert/ssr/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Patch0:         fix_ldpath.patch
Patch1:	simplescreenrecorder-0.3.6-fix-build.patch

BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel >= 4.1
BuildRequires:  qt4-devel
BuildRequires:  qt5-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libX11-devel
BuildRequires:  libXfixes-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:	cmake
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
SimpleScreenRecorder is a screen recorder for Linux.
Despite the name, this program is actually quite complex.
It's 'simple' in the sense that it's easier to use than ffmpeg/avconv or VLC

%package libs
Summary: SimpleScreenRecorder opengl injection library

%description libs
SimpleScreenRecorder is a screen recorder for Linux.
Despite the name, this program is actually quite complex.
It's 'simple' in the sense that it's easier to use than ffmpeg/avconv or VLC
This is a package for opengl capture

%prep
%autosetup -n %{shortname}-%{commit0} -p1

# glinject FIX
sed -i 's|libssr-glinject.so|/usr/\$LIB/simplescreenrecorder/libssr-glinject.so|g' scripts/ssr-glinject
sed -i 's|libssr-glinject.so|/usr/\\$LIB/simplescreenrecorder/libssr-glinject.so|g' src/AV/Input/GLInjectInput.cpp

%build
%cmake -DWITH_QT5=on .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
ctest -V %{?_smp_mflags}

%files
%doc COPYING README.md AUTHORS.md CHANGELOG.md notes.txt todo.txt
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_bindir}/%{shortname}-glinject
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/%{shortname}-glinject.1.*
%{_datadir}/appdata/simplescreenrecorder.appdata.xml

%files libs
%doc COPYING README.md AUTHORS.md CHANGELOG.md notes.txt todo.txt
%{_libdir}/lib%{shortname}-glinject.so

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%changelog

* Wed Mar 25 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.11-5.git0b17180
- Updated to current commit

* Sat Feb 02 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.11-4.git973cc00
- Updated to current commit

* Thu Dec 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.11-3.gitf5c5897 
- Updated to current commit
- Changed to qt5
- Rebuilt for ffmpeg

* Tue May 22 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.11-2.git4b5f572 
- Updated to 0.3.11-2.git4b5f572

* Thu Apr 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.10-4.giteb72d80  
- Automatic Mass Rebuild

* Sat Apr 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.10-3.giteb72d80  
- Updated to 0.3.10-3.giteb72d80

* Wed Mar 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.10-2  
- Updated to 0.3.10

* Mon Dec 11 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.9-2  
- Updated to 0.3.9

* Sat Nov 11 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.8.26-2  
- Updated to 0.3.8.26

* Tue Apr 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.3.8-3  
- Automatic Mass Rebuild

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.3.8-2
- Rebuilt for libbluray

* Sun Feb 26 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.3.8-1
- Updated to 0.3.8-1

* Thu Jul 07 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.3.6-5
- Rebuilt for FFmpeg 3.1

* Sat Jun 18 2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.3.6-4
- Rebuild for F24

* Tue Jun 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.3.6-3.R
- rebuilt against new ffmpeg

* Sun Nov  8 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.6-2.R
- Update icon cache

* Wed Nov  4 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.6-1.R
- Update to 0.3.6

* Mon Mar 23 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.3-1.R
- Update to 0.3.3

* Tue Dec 16 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.1-1.R
- Update to 0.3.1

* Thu Jul  3 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.0-2.R
- Move gl-inject library to subdir

* Thu Jul  3 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.0-1.R
- Initial spec for fedora
