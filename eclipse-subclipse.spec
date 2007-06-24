%define gcj_support     1

%define eclipse_name    eclipse
%define eclipse_base    %{_datadir}/%{eclipse_name}
%define core_plugin_jar %{eclipse_base}/plugins/org.tigris.subversion.subclipse.core_%{version}.jar
%define core_plugin_dir %{eclipse_base}/plugins/org.tigris.subversion.subclipse.core_%{version}


Name:           eclipse-subclipse
Version:        1.1.9
Release:        %mkrel 2.3
Epoch:          0
Summary:        Subversion Eclipse plugin
Group:          Development/Java
License:        EPL
URL:            http://subclipse.tigris.org/
Source0:        subclipse-%{version}.tar.bz2
# Script to fetch the source code
# the new source tarball does not includes the book feature and the layout is
# different than the source repository
Source10:       subclipse-fetch-1.1.9.sh
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:          ant
BuildRequires:          jpackage-utils
BuildRequires:          coreutils
BuildRequires:          eclipse-pde
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%else
BuildRequires:          java-devel >= 0:1.4.2
%endif
%if %{gcj_support}
ExclusiveArch:          %{ix86} x86_64 ppc ia64
%else
BuildArch:              noarch
%endif
Requires:               eclipse-platform
BuildRequires:          svn-javahl
Requires:               svn-javahl
BuildRequires:          svnkit
Requires:               svnkit
BuildRequires:          ganymed-ssh2
Requires:               ganymed-ssh2

%package book
Summary:        Subversion book
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description
Subclipse is an Eclipse plugin that adds Subversion integration to the Eclipse
IDE.

%description book
The Subversion book as an Eclipse documentation plugin.

%prep
%setup -q -n subclipse-%{version}
%if 0
%{__perl} -pi -e 's/JhlClientAdapterFactory\.JAVAHL_CLIENT/SvnKitClientAdapterFactory.SVNKIT_CLIENT/' \
  subclipse/ui/src/org/tigris/subversion/subclipse/ui/Preferences.java
%endif

# delete the jars that are in the archive
rm svnClientAdapter/lib/svnjavahl.jar
ln -sf %{_jnidir}/svn-javahl.jar svnClientAdapter/lib/svnjavahl.jar
rm -f svnClientAdapter/lib/svnkit.jar
ln -sf %{_javadir}/svnkit.jar svnClientAdapter/lib/svnkit.jar
rm -f svnClientAdapter/lib/ganymed.jar
ln -sf %{_javadir}/ganymed-ssh2.jar svnClientAdapter/lib/ganymed.jar

rm -f subclipse/core/lib/svnjavahl.jar
ln -sf %{_jnidir}/svn-javahl.jar subclipse/core/lib/svnjavahl.jar
rm -f subclipse/core/lib/svnClientAdapter.jar
# svnClientAdapter.jar is copied after being built
rm -f subclipse/core/lib/svnkit.jar
ln -sf %{_javadir}/svnkit.jar subclipse/core/lib/svnkit.jar
rm -f subclipse/core/lib/ganymed.jar
ln -sf %{_javadir}/ganymed-ssh2.jar subclipse/core/lib/ganymed.jar

%build
# ---------------------------------
# building svnClientAdapter
pushd svnClientAdapter
%{ant} svnClientAdapter.jar
popd

# copying svnClientAdapter inside subclipse module
cp svnClientAdapter/build/lib/svnClientAdapter.jar subclipse/core/lib/svnClientAdapter.jar

# ---------------------------------
# building subclipse
pushd subclipse
# See comments in the script to understand this.
/bin/sh -x %{eclipse_base}/buildscripts/copy-platform SDK %{eclipse_base}
SDK=$(cd SDK > /dev/null && pwd)

# Eclipse may try to write to the home directory.
mkdir home
homedir=$(cd home > /dev/null && pwd)

# build the main subclipse feature
%{java} -cp %{eclipse_base}/startup.jar                \
     -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration \
     -Duser.home=$homedir                              \
     org.eclipse.core.launcher.Main                    \
     -application org.eclipse.ant.core.antRunner       \
     -Dtype=feature                                    \
     -Did=org.tigris.subversion.subclipse              \
     -DsourceDirectory=$(pwd)                          \
     -DbaseLocation=$SDK                               \
     -Dbuilder=%{eclipse_base}/plugins/org.eclipse.pde.build/templates/package-build  \
     -f %{eclipse_base}/plugins/org.eclipse.pde.build/scripts/build.xml

# build the subclipse book feature
%{java} -cp %{eclipse_base}/startup.jar                \
     -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration \
     -Duser.home=$homedir                              \
     org.eclipse.core.launcher.Main                    \
     -application org.eclipse.ant.core.antRunner       \
     -Dtype=feature                                    \
     -Did=org.tigris.subversion.book                   \
     -DsourceDirectory=$(pwd)                          \
     -DbaseLocation=$SDK                               \
     -Dbuilder=%{eclipse_base}/plugins/org.eclipse.pde.build/templates/package-build  \
     -f %{eclipse_base}/plugins/org.eclipse.pde.build/scripts/build.xml

# returning to base build directory
popd

# Link source files to fix -debuginfo generation.
rm -rf subclipse/org
mkdir -p subclipse/org/tigris/subversion
ln -s $(pwd)/svnClientAdapter/src/main/org/tigris/subversion/svnclientadapter subclipse/org/tigris/subversion
mkdir -p subclipse/org/tigris/subversion/subclipse
ln -s $(pwd)/subclipse/core/src/org/tigris/subversion/subclipse/core subclipse/org/tigris/subversion/subclipse
ln -s $(pwd)/subclipse/ui/src/org/tigris/subversion/subclipse/ui subclipse/org/tigris/subversion/subclipse


%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{eclipse_base}

pushd subclipse
unzip -q -d $RPM_BUILD_ROOT%{eclipse_base}/.. build/rpmBuild/org.tigris.subversion.subclipse.zip
unzip -q -d $RPM_BUILD_ROOT%{eclipse_base}/.. build/rpmBuild/org.tigris.subversion.book.zip

# repacking core plugin as a directory based plugin, needed in order to replace some jars with symlinks
mkdir $RPM_BUILD_ROOT%{core_plugin_dir}
unzip -q -d $RPM_BUILD_ROOT%{core_plugin_dir} $RPM_BUILD_ROOT%{core_plugin_jar}
rm $RPM_BUILD_ROOT%{core_plugin_jar}
# packaging .class files as a jar file
jar -cf $RPM_BUILD_ROOT%{core_plugin_dir}/lib/subclipse-core.jar -C $RPM_BUILD_ROOT%{core_plugin_dir} org
rm -rf $RPM_BUILD_ROOT%{core_plugin_dir}/org
# adding the recently created jar to the plugin manifestOB
%{__perl} -pi -e 's|^Bundle-ClassPath: \.|Bundle-ClassPath: lib/subclipse-core.jar|' $RPM_BUILD_ROOT%{core_plugin_dir}/META-INF/MANIFEST.MF

# removing core plugin internal jars
rm -f $RPM_BUILD_ROOT%{core_plugin_dir}/lib/svnjavahl.jar
rm -f $RPM_BUILD_ROOT%{core_plugin_dir}/lib/svnkit.jar
rm -f $RPM_BUILD_ROOT%{core_plugin_dir}/lib/ganymed.jar

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

# We need to setup the symlink because the ant copy task doesn't preserve symlinks
# TODO file a bug about this
ln -s %{_jnidir}/svn-javahl.jar $RPM_BUILD_ROOT%{core_plugin_dir}/lib/svnjavahl.jar
ln -s %{_javadir}/svnkit.jar $RPM_BUILD_ROOT%{core_plugin_dir}/lib/svnkit.jar
ln -s %{_javadir}/ganymed-ssh2.jar $RPM_BUILD_ROOT%{core_plugin_dir}/lib/ganymed.jar

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%{eclipse_base}/features/org.tigris.subversion.subclipse_*
%{eclipse_base}/plugins/org.tigris.subversion.subclipse.core_*
%{eclipse_base}/plugins/org.tigris.subversion.subclipse.ui_*
%{eclipse_base}/plugins/org.tigris.subversion.subclipse.doc_*
%doc svnClientAdapter/readme.txt svnClientAdapter/changelog.txt svnClientAdapter/license.txt 

%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif

%files book
%defattr(-,root,root)
%{eclipse_base}/features/org.tigris.subversion.book_*
%{eclipse_base}/plugins/org.tigris.subversion.book_*


