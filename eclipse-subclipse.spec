%define gcj_support     0

%define eclipse_name    eclipse
%define eclipse_base    %{_libdir}/%{eclipse_name}
%define eclipse_inst	%{_datadir}/%{eclipse_name}
%define javahl_plugin_name org.tigris.subversion.clientadapter.javahl_1.5.4.1

Name:           eclipse-subclipse
Version:        1.4.7
Release:        %mkrel 0.3.0
Epoch:          0
Summary:        Subversion Eclipse plugin
Group:          Development/Java
License:        EPL and CC-BY
URL:            http://subclipse.tigris.org/
Source0:        subclipse-%{version}.tgz
# Script to fetch the source code
# the new source tarball does not includes the book feature and the layout is
# different than the source repository
Source10:       subclipse-fetch-1.2.4.sh
Patch0:         eclipse-subclipse-1.4.7-dependencies.patch
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

BuildArch:              noarch

Obsoletes:              eclipse-subclipse-book < 1.4

%description
Subclipse is an Eclipse plugin that adds Subversion integration to the Eclipse
IDE.

%package graph
Summary:        Subversion Revision Graph
Group:          Development/Java
Requires:       %{name} = %{version}
Requires:       eclipse-gef

%description graph
Subversion Revision Graph for Subclipse.

%prep
%setup -q -n subclipse-%{version}
%patch0 -p1
# fixing wrong-file-end-of-line-encoding warnings
sed -i 's/\r//' org.tigris.subversion.subclipse.graph/icons/readme.txt

# remove javahl sources
rm -rf org.tigris.subversion.clientadapter.javahl/src/org/tigris/subversion/javahl
ln -s %{_javadir}/svn-javahl.jar org.tigris.subversion.clientadapter.javahl

%build
%{eclipse_base}/buildscripts/pdebuild            \
  -f org.tigris.subversion.clientadapter.feature \
  -o `pwd`/orbitDeps
%{eclipse_base}/buildscripts/pdebuild                   \
  -f org.tigris.subversion.clientadapter.javahl.feature \
  -o `pwd`/orbitDeps
%{eclipse_base}/buildscripts/pdebuild                   \
  -f org.tigris.subversion.clientadapter.svnkit.feature \
  -o `pwd`/orbitDeps                                    \
  -d svnkit
%{eclipse_base}/buildscripts/pdebuild \
  -f org.tigris.subversion.subclipse  \
  -o `pwd`/orbitDeps
%{eclipse_base}/buildscripts/pdebuild              \
  -f org.tigris.subversion.subclipse.graph.feature \
  -o `pwd`/orbitDeps                               \
  -d gef

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{eclipse_inst}

installBase=$RPM_BUILD_ROOT%{eclipse_inst}
install -d -m 755 $installBase

# installing features
install -d -m 755 $installBase/subclipse-clientadapter
unzip -q -d $installBase/subclipse-clientadapter build/rpmBuild/org.tigris.subversion.clientadapter.feature.zip
install -d -m 755 $installBase/subclipse-clientadapter-javahl
unzip -q -d $installBase/subclipse-clientadapter-javahl build/rpmBuild/org.tigris.subversion.clientadapter.javahl.feature.zip
install -d -m 755 $installBase/subclipse-clientadapter-svnkit
unzip -q -d $installBase/subclipse-clientadapter-svnkit build/rpmBuild/org.tigris.subversion.clientadapter.svnkit.feature.zip
install -d -m 755 $installBase/subclipse
unzip -q -d $installBase/subclipse build/rpmBuild/org.tigris.subversion.subclipse.zip
install -d -m 755 $installBase/subclipse-graph
unzip -q -d $installBase/subclipse-graph build/rpmBuild/org.tigris.subversion.subclipse.graph.feature.zip

# replacing jar with links to system libraries
rm $installBase/subclipse-clientadapter-javahl/eclipse/plugins/%{javahl_plugin_name}/svn-javahl.jar
ln -s %{_javadir}/svn-javahl.jar $installBase/subclipse-clientadapter-javahl/eclipse/plugins/%{javahl_plugin_name}

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
%{eclipse_inst}/subclipse
%{eclipse_inst}/subclipse-clientadapter*
%doc org.tigris.subversion.subclipse.graph/icons/readme.txt

%files graph
%defattr(-,root,root)
%{eclipse_inst}/subclipse-graph
