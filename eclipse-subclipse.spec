%global eclipse_name       eclipse
%global eclipse_base       %{_libdir}/%{eclipse_name}
%global install_loc        %{_datadir}/eclipse/dropins
%global javahl_plugin_name org.tigris.subversion.clientadapter.javahl_1.6.15

# Add a comment to have something to commit to try to reproduce Adam
# Williamson's deadlock bug.

Name:           eclipse-subclipse
Version:        1.6.17
Release:        3
Summary:        Subversion Eclipse plugin

Group:          Development/Java
License:        EPL and CC-BY
URL:            http://subclipse.tigris.org/
Source0:        subclipse-%{version}.tar.xz
# Script to fetch the source code
Source10:       subclipse-fetch.sh
Patch0:         eclipse-subclipse-1.6.0-dependencies.patch

BuildArch:              noarch

BuildRequires:          ant
BuildRequires:          jpackage-utils >= 0:1.6
BuildRequires:          coreutils
BuildRequires:          eclipse-pde
BuildRequires:          eclipse-gef
Requires:               eclipse-platform

BuildRequires:          eclipse-svnkit >= 1.2.2
Requires:               eclipse-svnkit >= 1.2.2
BuildRequires:          svn-javahl >= 1.6
Requires:               svn-javahl >= 1.6

Obsoletes:              eclipse-subclipse-book < 1.4

%description
Subclipse is an Eclipse plugin that adds Subversion integration to the Eclipse
IDE.

%package graph
Summary:        Subversion Revision Graph
Group:          Development/Java
Requires:               %{name} = %{version}
Requires:               eclipse-gef

%description graph
Subversion Revision Graph for Subclipse.


%prep
%setup -q -n subclipse-%{version}
%patch0 -p1

# remove javahl sources
rm -rf org.tigris.subversion.clientadapter.javahl/src/org/tigris/subversion/javahl
ln -s %{_javadir}/svn-javahl.jar org.tigris.subversion.clientadapter.javahl

# fixing wrong-file-end-of-line-encoding warnings
sed -i 's/\r//' org.tigris.subversion.subclipse.graph/icons/readme.txt


%build
%{eclipse_base}/buildscripts/pdebuild -a "-DjavacSource=1.5 -DjavacTarget=1.5"      \
  -f org.tigris.subversion.clientadapter.feature 
%{eclipse_base}/buildscripts/pdebuild -a "-DjavacSource=1.5 -DjavacTarget=1.5"      \
  -f org.tigris.subversion.clientadapter.javahl.feature 
%{eclipse_base}/buildscripts/pdebuild -a "-DjavacSource=1.5 -DjavacTarget=1.5"     \
  -f org.tigris.subversion.clientadapter.svnkit.feature \
  -d svnkit
%{eclipse_base}/buildscripts/pdebuild -a "-DjavacSource=1.5 -DjavacTarget=1.5" \
  -f org.tigris.subversion.subclipse  
%{eclipse_base}/buildscripts/pdebuild -a "-DjavacSource=1.5 -DjavacTarget=1.5" \
  -f org.tigris.subversion.subclipse.graph.feature \
  -d gef


%install
install -d -m 755 $RPM_BUILD_ROOT%{install_loc}

installBase=$RPM_BUILD_ROOT%{install_loc}
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

%files
%defattr(-,root,root)
%{install_loc}/subclipse
%{install_loc}/subclipse-clientadapter*
%doc org.tigris.subversion.subclipse.graph/icons/readme.txt


%files graph
%defattr(-,root,root)
%{install_loc}/subclipse-graph


