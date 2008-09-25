%define gcj_support     0

%define disable_javahl  0
%define eclipse_name    eclipse
%define eclipse_base    %{_libdir}/%{eclipse_name}
%define eclipse_inst	%{_datadir}/%{eclipse_name}
%define core_plugin_jar %{eclipse_inst}/dropins/subclipse/eclipse/plugins/org.tigris.subversion.subclipse.core_%{version}.jar
%define core_plugin_dir %{eclipse_inst}/dropins/subclipse/eclipse/plugins/org.tigris.subversion.subclipse.core_%{version}

%define javahl_dir      %{_javadir}


Name:           eclipse-subclipse
Version:        1.2.4
Release:        %mkrel 0.1.2
Epoch:          0
Summary:        Subversion Eclipse plugin
Group:          Development/Java
License:        EPL
URL:            http://subclipse.tigris.org/
Source0:        subclipse-%{version}.tgz
# Script to fetch the source code
# the new source tarball does not includes the book feature and the layout is
# different than the source repository
Source10:       subclipse-fetch-1.2.4.sh
# Disable javahl support temporaly until apparent classloader problem is fixed
Patch0:         eclipse-subclipse-1.2.2-default-svnkit.patch
Patch1:         eclipse-subclipse-1.2.2-plugin-classpath.patch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
%if %mdkversion == 200800
# For fixed EOL handling:
# you may remove this on 2007-06-25 when iurt chroots are updated
BuildRequires: spec-helper >= 0.26
%endif
BuildRequires:          ant
BuildRequires:          zip
BuildRequires:          java-rpmbuild
BuildRequires:          eclipse-pde
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%else
BuildArch:              noarch
BuildRequires:          java-devel
%endif
Requires:               eclipse-platform
BuildRequires:          svn-javahl
Requires:               svn-javahl
BuildRequires:          svnkit
Requires:               svnkit
BuildRequires:          trilead-ssh2
Requires:               trilead-ssh2

%package book
Summary:        Subversion book
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description
Subclipse is an Eclipse plugin that adds Subversion integration to the Eclipse
IDE.

%description book
The Subversion book as an Eclipse documentation plugin.

%prep
%setup -q -n subclipse-%{version}
%if %{disable_javahl}
%patch -p1
%endif
%patch1 -p1

# delete the jars that are in the archive
rm svnClientAdapter/lib/svnjavahl.jar
ln -s %{javahl_dir}/svn-javahl.jar svnClientAdapter/lib/svnjavahl.jar
rm -f svnClientAdapter/lib/svnkit.jar
ln -s %{_javadir}/svnkit.jar svnClientAdapter/lib/svnkit.jar
rm -f svnClientAdapter/lib/ganymed.jar
ln -s %{_javadir}/trilead-ssh2.jar svnClientAdapter/lib/ganymed.jar

rm -f subclipse/core/lib/svnjavahl.jar
ln -s %{javahl_dir}/svn-javahl.jar subclipse/core/lib/svnjavahl.jar
rm -f subclipse/core/lib/svnClientAdapter.jar
# svnClientAdapter.jar is copied after being built
rm -f subclipse/core/lib/svnkit.jar
ln -s %{_javadir}/svnkit.jar subclipse/core/lib/svnkit.jar
rm -f subclipse/core/lib/ganymed.jar
ln -s %{_javadir}/trilead-ssh2.jar subclipse/core/lib/ganymed.jar

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

%{eclipse_base}/buildscripts/pdebuild -f org.tigris.subversion.subclipse
%{eclipse_base}/buildscripts/pdebuild -f org.tigris.subversion.book

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
install -d -m 755 $RPM_BUILD_ROOT%{eclipse_inst}

installDir=$RPM_BUILD_ROOT%{eclipse_inst}/dropins/subclipse
install -d -m 755 $installDir
install -d -m 755 ${installDir}-book
pushd subclipse
unzip -q -d $installDir build/rpmBuild/org.tigris.subversion.subclipse.zip
unzip -q -d ${installDir}-book build/rpmBuild/org.tigris.subversion.book.zip
popd

# repacking core plugin as a directory based plugin, needed in order to replace some jars with symlinks
mkdir $RPM_BUILD_ROOT%{core_plugin_dir}
unzip -q -d $RPM_BUILD_ROOT%{core_plugin_dir} $RPM_BUILD_ROOT%{core_plugin_jar}
rm $RPM_BUILD_ROOT%{core_plugin_jar}
# packaging .class files as a jar file
jar -cf $RPM_BUILD_ROOT%{core_plugin_dir}/lib/subclipse-core.jar -C $RPM_BUILD_ROOT%{core_plugin_dir} org
rm -rf $RPM_BUILD_ROOT%{core_plugin_dir}/org

# removing core plugin internal jars
rm -f $RPM_BUILD_ROOT%{core_plugin_dir}/lib/svnjavahl.jar
rm -f $RPM_BUILD_ROOT%{core_plugin_dir}/lib/svnkit.jar
rm -f $RPM_BUILD_ROOT%{core_plugin_dir}/lib/ganymed.jar

%{gcj_compile}

# We need to setup the symlink because the ant copy task doesn't preserve symlinks
# TODO file a bug about this
ln -s %{javahl_dir}/svn-javahl.jar $RPM_BUILD_ROOT%{core_plugin_dir}/lib/svnjavahl.jar
ln -s %{_javadir}/svnkit.jar $RPM_BUILD_ROOT%{core_plugin_dir}/lib/svnkit.jar
ln -s %{_javadir}/trilead-ssh2.jar $RPM_BUILD_ROOT%{core_plugin_dir}/lib/ganymed.jar

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
%{eclipse_inst}/dropins/subclipse
%doc svnClientAdapter/readme.txt svnClientAdapter/changelog.txt svnClientAdapter/license.txt 
%{gcj_files}

%files book
%defattr(-,root,root)
%{eclipse_inst}/dropins/subclipse-book
