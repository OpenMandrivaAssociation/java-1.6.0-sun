%define        origin           sun
%define        priority         1600
%define        javaver          1.6.0
%define        cvsver           6u13
%define        over             %{cvsver}
%define        buildver         13

%define        cvsversion       %{cvsver}

%define        javaws_ver       %{javaver}
%define        javaws_version   %{cvsversion}

%define        ubuntu_svnrev    r273

%define        jdkbundle        jdk%{javaver}_%{buildver}
%define        sdklnk           java-%{javaver}-%{origin}
%define        jrelnk           jre-%{javaver}-%{origin}
%define        sdkdir           %{name}-%{version}
%define        jredir           %{sdkdir}/jre
%define        sdkbindir        %{_jvmdir}/%{sdklnk}/bin
%define        sdklibdir        %{_jvmdir}/%{sdklnk}/lib
%define        jrebindir        %{_jvmdir}/%{jrelnk}/bin
%define        jvmjardir        %{_jvmjardir}/%{name}-%{version}

%define fontdir                 %{_datadir}/fonts/java

%ifarch %{ix86}
%define        target_cpu       i586
%define        pluginname       %{_jvmdir}/%{jredir}/lib/i386/libnpjp2.so
%define        oldpluginname    %{_jvmdir}/%{jredir}/plugin/i386/ns7/libjavaplugin_oji.so
%define        priority2        1590
%define        javaplugin       libjavaplugin.so
%endif
%ifarch x86_64
%define        target_cpu       amd64
%define        pluginname       %{_jvmdir}/%{jredir}/lib/amd64/libnpjp2.so
%define        javaplugin       libjavaplugin.so.%{_arch}
%endif

%define        cgibindir        %{_var}/www/cgi-bin

# Avoid RPM 4.2+'s internal dep generator, it may produce bogus
# Provides/Requires here.
%define _use_internal_dependency_generator 0

# This prevents aggressive stripping.
%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Name:           java-%{javaver}-%{origin}
Version:        %{javaver}.%{buildver}
Release:        %mkrel 1
Summary:        Java Runtime Environment for %{name}
License:        Operating System Distributor License for Java (DLJ)
Group:          Development/Java
URL:            http://java.sun.com/j2se/%{javaver}
Source0:        http://dlc.sun.com/dlj/binaries/jdk-%{cvsversion}-dlj-linux-i586.bin
Source1:        http://dlc.sun.com/dlj/binaries/jdk-%{cvsversion}-dlj-linux-amd64.bin
# svn co -%{ubuntu_svnrev} --username guest --password "" https://jdk-distros.dev.java.net/svn/jdk-distros/trunk/linux/ubuntu/sun-java6/debian/
Source2:        jdk-6-dlj-ubuntu-%{ubuntu_svnrev}.tar.bz2
# (anssi) make javaws entry really point to javaws and create a different
# entry for the cache viewer where to it pointed previously (#31347):
Patch0:         jdk6-fix-javaws-desktop.patch
Provides:       jre-%{javaver}-%{origin} = %{version}-%{release}
Provides:       jre-%{origin} = %{version}-%{release}
Provides:       jre-%{javaver} java-%{javaver} jre = %{javaver}
Provides:       java-%{origin} = %{version}-%{release}
Provides:       java = %{javaver}
Provides:       %{_lib}%{name} = %{version}-%{release}
Requires(post): update-alternatives
Requires(postun): update-alternatives
Requires:       jpackage-utils >= 0:1.5.38
ExclusiveArch:  %{ix86} x86_64
BuildRequires:  jpackage-utils >= 0:1.5.38 sed desktop-file-utils
Provides:       javaws = %{javaws_ver}
Provides:       jndi = %{version} jndi-ldap = %{version}
Provides:       jndi-cos = %{version} jndi-rmi = %{version}
Provides:       jndi-dns = %{version}
Provides:       jaas = %{version}
Provides:       jsse = %{version}
Provides:       jce = %{version}
Provides:       jdbc-stdext = 3.0 jdbc-stdext = %{version}
Provides:       java-sasl = %{version}
%ifnarch x86_64
Obsoletes:      javaws-menu
Provides:       javaws-menu
%endif
# DLJ license requires these to be part of the JRE
Requires:       %{_lib}%{name}-plugin = %{version}-%{release}
Requires:       %{_lib}%{name}-alsa = %{version}-%{release}
Requires:       %{_lib}%{name}-jdbc = %{version}-%{release}
Requires:       %{name}-fonts = %{version}-%{release}
Provides:       j2re = %{version}-%{release}
Provides:       jre2 = %{version}-%{release}
Obsoletes:      j2re < %{version}-%{release}
Obsoletes:      jre2 < %{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
This package contains the Java Runtime Environment for %{name}

%package devel
Summary:        Java Development Kit for %{name}
Group:          Development/Java
Requires(post): update-alternatives
Requires(postun): update-alternatives
Provides:       java-sdk-%{javaver}-%{origin} = %{version}-%{release}
Provides:       java-sdk-%{origin} = %{version}-%{release}
Provides:       java-sdk-%{javaver} java-sdk = %{javaver} jdk = %{javaver}
Provides:       java-devel-%{origin} = %{version}-%{release}
Provides:       java-%{javaver}-devel java-devel = %{javaver}
Requires:       %{_lib}%{name} = %{version}-%{release}
Provides:       jdk = %{version}-%{release}
Provides:       jdk2 = %{version}-%{release}
Provides:       j2sdk = %{version}-%{release}
Obsoletes:      jdk < %{version}-%{release}
Obsoletes:      jdk2 < %{version}-%{release}
Obsoletes:      j2sdk < %{version}-%{release}

%description devel
The Java(tm) Development Kit (JDK(tm)) contains the software and tools that
developers need to compile, debug, and run applets and applications
written using the Java programming language.

%package src
Summary:        Source files for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description src
This package contains source files for %{name}.

%package demo
Summary:        Demonstration files for %{name}
Group:          Development/Java
Requires:       %{_lib}%{name} = %{version}-%{release}
# Without this a requirement on libjava_crw_demo_g.so is added which
# is not in the main java package. libjava_crw_demo.so is but not "_g".
AutoReq:        0

%description demo
This package contains demonstration files for %{name}.

%package plugin
Summary:        Browser plugin files for %{name}
Group:          Networking/WWW
Requires(post): update-alternatives
Requires(postun): update-alternatives
Requires:       %{_lib}%{name} = %{version}-%{release}
Provides:       java-plugin = %{javaver} java-%{javaver}-plugin = %{version}
Provides:       %{_lib}%{name}-plugin = %{version}-%{release}
Conflicts:      java-%{javaver}-ibm-plugin java-%{javaver}-blackdown-plugin
Conflicts:      java-%{javaver}-bea-plugin
Obsoletes:      java-1.3.1-plugin java-1.4.0-plugin java-1.4.1-plugin java-1.4.2-plugin

%description plugin
This package contains browser plugin files for %{name}.
Note!  This package supports browsers built with GCC 3.2 and later.

%package fonts
Summary:        TrueType fonts for %{origin} JVMs
Group:          System/Fonts/True type
Requires(post): update-alternatives
Requires(postun): update-alternatives
Requires:       %{name} = %{version}-%{release} freetype-tools
Requires:       mkfontdir
Requires(post): fontconfig
Requires(postun): fontconfig
Provides:       java-fonts = %{javaver} java-%{javaver}-fonts
Conflicts:      java-%{javaver}-ibm-fonts java-%{javaver}-blackdown-fonts
Conflicts:      java-%{javaver}-bea-fonts
Obsoletes:      java-1.3.1-fonts java-1.4.0-fonts java-1.4.1-fonts java-1.4.2-fonts

%description fonts
This package contains the TrueType fonts for %{origin} JVMs.

%package alsa
Summary:        ALSA support for %{name}
Group:          Development/Java
Requires:       %{_lib}%{name} = %{version}-%{release}
Provides:       %{_lib}%{name}-alsa = %{version}-%{release}

%description alsa
This package contains Advanced Linux Sound Architecture (ALSA) support
libraries for %{name}.

%package jdbc
Summary:        JDBC/ODBC bridge driver for %{name}
Group:          Development/Java
Requires:       %{_lib}%{name} = %{version}-%{release}
Provides:       %{_lib}%{name}-jdbc = %{version}-%{release}
AutoReq:        0

%description jdbc
This package contains the JDBC/ODBC bridge driver for %{name}.

%prep
%setup -q -T -c -n %{name}-%{version} -a2
%patch0 -p0
%ifarch i586
sh %{SOURCE0} --accept-license --unpack
%else
sh %{SOURCE1} --accept-license --unpack
%endif
cd %{jdkbundle}
%ifarch x86_64
rm -f man/man1/javaws.1
%endif

# fix perms
chmod -R go=u-w *
chmod -R u+w *

%build
for xdgmenu in debian/*desktop.in; do
        sed $xdgmenu \
        -e "s#@vendor@#Sun#g" \
        -e "s#@RELEASE@#%{javaver}#g" \
        -e "s#/@basedir@/bin#%{jrebindir}#g" \
        -e "s#Icon=.*#Icon=%{name}#g" \
        -e "s#@ia32txt@##g" \
        > %{name}-`echo $xdgmenu|cut -d- -f2|cut -d. -f1-2`
done
sed -i -e "s#%{jrebindir}#%{sdkbindir}#g" %{name}-jconsole.desktop
mv %{name}-java.desktop debian/sharedmimeinfo %{jdkbundle}/jre/lib

%install
rm -rf %{buildroot}

export DONT_STRIP=1

cd %{jdkbundle}
%ifnarch x86_64
# install java-rmi-cgi
install -m755 bin/java-rmi.cgi -D %{buildroot}%{cgibindir}/java-rmi-%{version}.cgi
%endif

# main files
install -d %{buildroot}%{_jvmdir}/%{sdkdir}
cp -a COPYRIGHT LICENSE THIRDPARTYLICENSEREADME.txt bin include lib %{buildroot}%{_jvmdir}/%{sdkdir}
install -m644 src.zip -D %{buildroot}%{_prefix}/src/%{name}-%{version}.zip
ln -s %{_prefix}/src/%{name}-%{version}.zip %{buildroot}%{_jvmdir}/%{sdkdir}/src.zip

install -d %{buildroot}%{_jvmdir}/%{jredir}

# extensions handling
install -d %{buildroot}%{jvmjardir}
pushd %{buildroot}%{jvmjardir}
   ln -s %{_jvmdir}/%{jredir}/lib/jsse.jar jsse-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/jce.jar jce-%{version}.jar
   for jar in jndi jndi-ldap jndi-cos jndi-rmi jaas jdbc-stdext sasl; do
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar $jar-%{version}.jar; done
   ln -s jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
   for jar in *-%{version}.jar ; do
      if [ x%{version} != x%{javaver} ]; then
         ln -fs ${jar} $(echo $jar | sed "s|-%{version}.|-%{javaver}.|g")
      fi
      ln -fs ${jar} $(echo $jar | sed "s|-%{version}.|.|g")
   done
popd

# rest of the jre
cp -a jre/bin jre/lib %{buildroot}%{_jvmdir}/%{jredir}
cp -a jre/javaws jre/plugin %{buildroot}%{_jvmdir}/%{jredir}
install -d %{buildroot}%{_jvmdir}/%{jredir}/lib/endorsed

# jce policy file handling
install -d %{buildroot}%{_jvmprivdir}/%{name}/jce/vanilla
for file in local_policy.jar US_export_policy.jar; do
  mv %{buildroot}%{_jvmdir}/%{jredir}/lib/security/$file \
    %{buildroot}%{_jvmprivdir}/%{name}/jce/vanilla
  # for ghosts
  touch %{buildroot}%{_jvmdir}/%{jredir}/lib/security/$file
done

# versionless symlinks
pushd %{buildroot}%{_jvmdir}
ln -s %{jredir} %{jrelnk}
ln -s %{sdkdir} %{sdklnk}
popd

pushd %{buildroot}%{_jvmjardir}
ln -s %{sdkdir} %{jrelnk}
ln -s %{sdkdir} %{sdklnk}
popd

install -m644 jre/plugin/desktop/sun_java.png -D %{buildroot}%{_datadir}/pixmaps/%{name}.png

for desktop in ../*.desktop; do
        desktop-file-install        --vendor="" \
                                --remove-category="Application" \
                                --remove-category="X-Red-Hat-Base" \
                                --remove-category="AdvancedSettings" \
                                --add-category="X-MandrivaLinux-System-SunJava%{over}" \
                                --dir %{buildroot}%{_datadir}/applications $desktop
done

# make sure that this directory exist so update-alternatvies won't fail if shared-mime-info isn't installed
install -d %{buildroot}%{_datadir}/mime/packages

# man pages
install -d %{buildroot}%{_mandir}/man1
pushd man
for manpage in man1/*; do
        iconv -f iso-8859-1 -t utf-8 $manpage -o %{buildroot}%{_mandir}/man1/`basename $manpage .1`-%{name}.1
        install -m644 ja_JP.eucJP/$manpage -D %{buildroot}%{_mandir}/ja_JP.eucJP/man1/`basename $manpage .1`-%{name}.1
done
popd

# demo
install -d %{buildroot}%{_datadir}/%{name}
cp -a demo %{buildroot}%{_datadir}/%{name}
ln -s %{_datadir}/%{name}/demo %{buildroot}%{_jvmdir}

### font handling
# (anssi) This dir is used with java-1.5.0-sun as well, do not modify to avoid conflicts
install -d %{buildroot}%{fontdir}
#mv %{buildroot}%{_jvmdir}/%{jredir}/lib/fonts %{buildroot}%{fontdir}
#ln -s %{fontdir} %{buildroot}%{_jvmdir}/%{jredir}/lib/fonts
ln -s %{_sysconfdir}/java/font.properties %{buildroot}%{_jvmdir}/%{jredir}/lib

# These %ghost'd files are created properly in %post  -- Rex
touch %{buildroot}%{fontdir}/{fonts.{alias,dir,scale,cache-1},XftCache,encodings.dir}

# fontpath.d symlink
mkdir -p %{buildroot}%_sysconfdir/X11/fontpath.d/
ln -s ../../..%{fontdir} \
    %{buildroot}%_sysconfdir/X11/fontpath.d/java:pri=50

# make sure that plugin dir exists so update-alternatives won't fail if mozilla/firefox isn't installed
install -d %{buildroot}%{_libdir}/mozilla/plugins

cd ..

# Most of this shamelessly stolen from redhat's kdebase-2.2.2 specfile
find %{buildroot}%{_jvmdir}/%{jredir} -type d \
| sed 's|'%{buildroot}'|%dir |' >  %{name}-%{version}-all.files
find %{buildroot}%{_jvmdir}/%{jredir} -type f -o -type l \
| sed 's|'%{buildroot}'||'      >> %{name}-%{version}-all.files

grep "plugin\|libnpjp2"  %{name}-%{version}-all.files | sort \
> %{name}-%{version}-plugin.files
grep Jdbc    %{name}-%{version}-all.files | sort \
> %{name}-%{version}-jdbc.files
grep -F alsa.so %{name}-%{version}-all.files | sort \
> %{name}-%{version}-alsa.files
cat %{name}-%{version}-all.files \
| grep -v plugin \
| grep -v libnpjp2 \
| grep -v Jdbc \
| grep -v lib/fonts \
| grep -vF alsa.so \
| grep -v jre/lib/security \
> %{name}-%{version}.files

%ifarch x86_64
%define        jreext        %{nil}
%else
%define        jreext        javaws
%endif
%define        jrebin        keytool orbd policytool rmid rmiregistry servertool tnameserv
%define        jreman        java %{jreext} %{jrebin} jvisualvm
%ifarch        x86_64
%define        jdkext        %{nil}
%else
%define        jdkext        HtmlConverter
%endif
%define        jdkboth        appletviewer extcheck idlj jar jarsigner javadoc javah javap jdb native2ascii rmic serialver jconsole pack200 unpack200 apt jinfo jmap jps jsadebugd jstack jstat jstatd jhat jrunscript schemagen wsgen wsimport xjc
%define        jdkman        %{jdkboth} javac
%define        jdkbin        %{jdkboth} %{jdkext}

for man in %{jreman}; do
echo %{_mandir}/man1/${man}-%{name}.1%{_extension} >> %{name}-%{version}.files
echo %{_mandir}/ja_JP.eucJP/man1/${man}-%{name}.1%{_extension} >> %{name}-%{version}.files
done
rm -f %{name}-%{version}-devel.files
for man in %{jdkman}; do
echo %{_mandir}/man1/${man}-%{name}.1%{_extension} >> %{name}-%{version}-devel.files
echo %{_mandir}/ja_JP.eucJP/man1/${man}-%{name}.1%{_extension} >> %{name}-%{version}-devel.files
done

%clean
rm -rf %{buildroot}

%post
update-alternatives --install %{_bindir}/java java %{jrebindir}/java %{priority}%{expand:%(for bin in %{jrebin}; do echo -n -e \ \\\\\\n\
--slave %{_bindir}/${bin}                        ${bin}                        %{jrebindir}/${bin}; done)}%{expand:%(for man in %{jreman}; do echo -n -e \ \\\\\\n\
--slave %{_mandir}/man1/${man}.1%{_extension}        ${man}.1%{_extension}        %{_mandir}/man1/${man}-%{name}.1%{_extension}; done)}%{expand:%(for man in %{jreman}; do echo -n -e \ \\\\\\n\
--slave %{_mandir}/ja_JP.eucJP/man1/${man}.1%{_extension}        ${man}%{_extension}.ja_JP.eucJP        %{_mandir}/ja_JP.eucJP/man1/${man}-%{name}.1%{_extension}; done)} \
--slave        %{_bindir}/ControlPanel                        ControlPanel                %{jrebindir}/ControlPanel \
--slave        %{_bindir}/javaws                        javaws                        %{jrebindir}/javaws \
--slave %{_datadir}/mime/packages/java.xml        java.xml                %{_jvmdir}/%{jrelnk}/lib/sharedmimeinfo \
--slave        %{_jvmdir}/jre                                jre                        %{_jvmdir}/%{jrelnk} \
--slave        %{_jvmjardir}/jre                        jre_exports                %{_jvmjardir}/%{jrelnk}

# (Anssi 04/2008) bug #40201
# These used to be broken real files:
for file in %{_jvmdir}/%{jredir}/lib/security/local_policy.jar %{_jvmdir}/%{jrelnk}/lib/security/US_export_policy.jar; do
        [ -L "$file" ] || rm -f "$file"
done
update-alternatives \
--install \
        %{_jvmdir}/%{jrelnk}/lib/security/local_policy.jar \
        jce_%{javaver}_%{origin}_local_policy \
        %{_jvmprivdir}/%{name}/jce/vanilla/local_policy.jar \
        %{priority} \
--slave \
        %{_jvmdir}/%{jrelnk}/lib/security/US_export_policy.jar \
        jce_%{javaver}_%{origin}_us_export_policy \
        %{_jvmprivdir}/%{name}/jce/vanilla/US_export_policy.jar

update-alternatives --install %{_jvmdir}/jre-%{origin} jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{origin}        jre_%{origin}_exports        %{_jvmjardir}/%{jrelnk}

update-alternatives --install %{_jvmdir}/jre-%{javaver} jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{javaver}        jre_%{javaver}_exports      %{_jvmjardir}/%{jrelnk}


%{update_desktop_database}
%{update_mime_database}

%post devel
update-alternatives --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority}%{expand:%(for bin in %{jdkbin}; do echo -n -e \ \\\\\\n\
--slave %{_bindir}/${bin}                        ${bin}                        %{sdkbindir}/${bin}; done)}%{expand:%(for man in %{jdkman}; do echo -n -e \ \\\\\\n\
--slave %{_mandir}/man1/${man}.1%{_extension}        ${man}.1%{_extension}        %{_mandir}/man1/${man}-%{name}.1%{_extension}; done)}%{expand:%(for man in %{jdkman}; do echo -n -e \ \\\\\\n\
--slave %{_mandir}/ja_JP.eucJP/man1/${man}.1%{_extension}        ${man}%{_extension}.ja_JP.eucJP        %{_mandir}/ja_JP.eucJP/man1/${man}-%{name}.1%{_extension}; done)} \
--slave %{_jvmdir}/java                         java_sdk                %{_jvmdir}/%{sdklnk} \
--slave %{_jvmjardir}/java                      java_sdk_exports        %{_jvmjardir}/%{sdklnk}

update-alternatives --install %{_jvmdir}/java-%{origin} java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{origin}        java_sdk_%{origin}_exports        %{_jvmjardir}/%{sdklnk}

update-alternatives --install %{_jvmdir}/java-%{javaver} java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{javaver}        java_sdk_%{javaver}_exports      %{_jvmjardir}/%{sdklnk}

%post plugin
%ifarch %ix86
update-alternatives --install %{_libdir}/mozilla/plugins/libjavaplugin.so %{javaplugin} %{pluginname} %{priority}
update-alternatives --install %{_libdir}/mozilla/plugins/libjavaplugin.so %{javaplugin} %{oldpluginname} %{priority2}
%endif

%ifarch x86_64
update-alternatives --install %{_libdir}/mozilla/plugins/libjavaplugin.so %{javaplugin} %{pluginname} %{priority}
%endif

%postun plugin
%ifarch %ix86
if ! [ -e "%{oldpluginname}" ]; then
update-alternatives --remove %{javaplugin} %{oldpluginname}
fi
%endif
if ! [ -e "%{pluginname}" ]; then
update-alternatives --remove %{javaplugin} %{pluginname}
fi

%postun
if ! [ -e "%{jrebindir}/java" ]; then
update-alternatives --remove java %{jrebindir}/java
update-alternatives --remove \
        jce_%{javaver}_%{origin}_local_policy \
        %{_jvmprivdir}/%{name}/jce/vanilla/local_policy.jar
update-alternatives --remove jre_%{origin}  %{_jvmdir}/%{jrelnk}
update-alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi

%{clean_desktop_database}
%{clean_mime_database}

%postun devel
if ! [ -e "%{sdkbindir}/javac" ]; then
update-alternatives --remove javac %{sdkbindir}/javac
update-alternatives --remove java_sdk_%{origin}  %{_jvmdir}/%{sdklnk}
update-alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi

%post fonts
%define fonts   LucidaBrightItalic.ttf LucidaSansDemiBold.ttf LucidaTypewriterBold.ttf LucidaBrightDemiItalic.ttf LucidaBrightRegular.ttf LucidaSansRegular.ttf LucidaTypewriterRegular.ttf

update-alternatives --install %{fontdir}/LucidaBrightDemiBold.ttf LucidaBrightDemiBold.ttf  %{_jvmdir}/%{jredir}/lib/fonts/LucidaBrightDemiBold.ttf %{priority} \
%{expand:%(for font in %{fonts}; do echo -n -e \ \\\\\\n\
--slave %{fontdir}/$font        $font        %{_jvmdir}/%{jredir}/lib/fonts/$font; done)}

mkfontscale %{fontdir}
mkfontdir %{fontdir}
fc-cache

%postun fonts
if ! [ -e %{_jvmdir}/%{jredir}/lib/fonts/LucidaBrightDemiBold.ttf ]; then
update-alternatives --remove LucidaBrightDemiBold.ttf %{_jvmdir}/%{jredir}/lib/fonts/LucidaBrightDemiBold.ttf
fc-cache
fi

if [ -d %{fontdir} ]; then
mkfontscale %{fontdir}
mkfontdir %{fontdir}
fi


# (Anssi 02/2008) The previous versions of this package were buggy and did
# not always remove the old alternative, causing it to be left enabled,
# leading to broken symlinks.
%posttrans
if ! [ -e %{_bindir}/java ]; then
	update-alternatives --auto java
fi
%posttrans devel
if ! [ -e %{_bindir}/javac ]; then
	update-alternatives --auto javac
fi
%posttrans plugin
if ! [ -e %{_libdir}/mozilla/plugins/libjavaplugin.so ]; then
	update-alternatives --auto %{javaplugin}
fi

%posttrans fonts
if ! [ -e %{fontdir}/LucidaBrightDemiBold.ttf ]; then
	update-alternatives --auto LucidaBrightDemiBold.ttf
fi

%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%doc %{jdkbundle}/jre/{COPYRIGHT,LICENSE,README}
%doc %{jdkbundle}/jre/Welcome.html
%dir %{_jvmdir}/%{sdkdir}
%{_jvmdir}/%{sdkdir}/COPYRIGHT
%{_jvmdir}/%{sdkdir}/LICENSE
%{_jvmdir}/%{sdkdir}/THIRDPARTYLICENSEREADME.txt
%{jvmjardir}
%{_jvmdir}/%{jredir}/lib/fonts
%dir %{_jvmdir}/%{jredir}/lib/security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/javaws.policy
%ghost %{_jvmdir}/%{jredir}/lib/security/local_policy.jar
%ghost %{_jvmdir}/%{jredir}/lib/security/US_export_policy.jar
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{_datadir}/applications/*.desktop
%exclude %{_datadir}/applications/%{name}-jconsole.desktop
%{_datadir}/pixmaps/*.png
%dir %{_datadir}/mime
%dir %{_datadir}/mime/packages

%files devel -f %{name}-%{version}-devel.files
%defattr(-,root,root,-)
%doc %{jdkbundle}/{COPYRIGHT,LICENSE,README.html}
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%ifnarch x86_64
%{cgibindir}/java-rmi-%{version}.cgi
%endif
%{_datadir}/applications/%{name}-jconsole.desktop

%files src
%defattr(-,root,root,-)
%{_jvmdir}/%{sdkdir}/src.zip
%{_prefix}/src/%{name}-%{version}.zip

%files demo
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/demo
%{_jvmdir}/demo

%files alsa -f %{name}-%{version}-alsa.files
%defattr(-,root,root,-)

%files jdbc -f %{name}-%{version}-jdbc.files
%defattr(-,root,root,-)

%files plugin -f %{name}-%{version}-plugin.files
%defattr(-,root,root,-)
%dir %{_libdir}/mozilla
%dir %{_libdir}/mozilla/plugins

%files fonts
%defattr(0644,root,root,0755)
%{_jvmdir}/%{jredir}/lib/fonts/*.ttf
%dir %{fontdir}
%config(noreplace) %{fontdir}/fonts.alias
%ghost %{fontdir}/fonts.dir
%ghost %{fontdir}/fonts.scale
%ghost %{fontdir}/fonts.cache-1
%ghost %{fontdir}/XftCache
%ghost %{fontdir}/encodings.dir
%{_sysconfdir}/X11/fontpath.d/java:pri=50
