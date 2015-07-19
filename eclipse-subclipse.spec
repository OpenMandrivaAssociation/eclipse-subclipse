%{?_javapackages_macros:%_javapackages_macros}
%global install_loc        %{_datadir}/eclipse/dropins

Name:           eclipse-subclipse
Version:        1.10.5
Release:        1.2
Summary:        Subversion Eclipse plugin
Group:		Development/Java
License:        EPL and CC-BY
URL:            http://subclipse.tigris.org/
Source0:        subclipse-%{version}.tar.xz
# Script to fetch the source code
Source10:       subclipse-fetch.sh
Patch0:         eclipse-subclipse-1.8.13-dependencies.patch

BuildArch:              noarch

BuildRequires:          eclipse-pde >= 4.3.2
BuildRequires:          eclipse-gef
Requires:               eclipse-platform >= 4.3.2

BuildRequires:          subversion-javahl >= 1.8.9
Requires:               subversion-javahl >= 1.8.9

%description
Subclipse is an Eclipse plugin that adds Subversion integration to the Eclipse
IDE.

%package graph
Summary:        Subversion Revision Graph
Requires:       %{name} = %{version}
Requires:       eclipse-gef

%description graph
Subversion Revision Graph for Subclipse.

%prep
%setup -q -n subclipse-%{version}
%patch0 -p0 -b .sav

# remove javahl sources
rm -rf org.tigris.subversion.clientadapter.javahl/src/org/tigris/subversion/javahl
ln -s %{_javadir}/svn-javahl.jar org.tigris.subversion.clientadapter.javahl

# fixing wrong-file-end-of-line-encoding warnings
sed -i 's/\r//' org.tigris.subversion.subclipse.graph/icons/readme.txt

%build
eclipse-pdebuild -f org.tigris.subversion.clientadapter.feature 

eclipse-pdebuild -f org.tigris.subversion.clientadapter.javahl.feature
 
# Do not build svnkit as our svnkit package is outdated
#eclipse-pdebuild -f org.tigris.subversion.clientadapter.svnkit.feature -d svnkit

eclipse-pdebuild -f org.tigris.subversion.subclipse
  
eclipse-pdebuild -f org.tigris.subversion.subclipse.graph.feature -d gef


%install
install -d -m 755 $RPM_BUILD_ROOT%{install_loc}

# installing features
install -d -m 755 $RPM_BUILD_ROOT%{install_loc}/subclipse-clientadapter
unzip -q -d $RPM_BUILD_ROOT%{install_loc}/subclipse-clientadapter build/rpmBuild/org.tigris.subversion.clientadapter.feature.zip
unzip -q -d $RPM_BUILD_ROOT%{install_loc}/subclipse-clientadapter build/rpmBuild/org.tigris.subversion.clientadapter.javahl.feature.zip
#unzip -q -d $RPM_BUILD_ROOT%{install_loc}/subclipse-clientadapter build/rpmBuild/org.tigris.subversion.clientadapter.svnkit.feature.zip
install -d -m 755 $RPM_BUILD_ROOT%{install_loc}/subclipse
unzip -q -d $RPM_BUILD_ROOT%{install_loc}/subclipse build/rpmBuild/org.tigris.subversion.subclipse.zip
install -d -m 755 $RPM_BUILD_ROOT%{install_loc}/subclipse-graph
unzip -q -d $RPM_BUILD_ROOT%{install_loc}/subclipse-graph build/rpmBuild/org.tigris.subversion.subclipse.graph.feature.zip

# replacing jar with links to system libraries
pushd $RPM_BUILD_ROOT%{install_loc}/subclipse-clientadapter/eclipse/plugins/
ADAPTER_JAVAHL=$(ls org.tigris.subversion.clientadapter.javahl_*.jar)
unzip $ADAPTER_JAVAHL -d ${ADAPTER_JAVAHL%.jar}
rm $ADAPTER_JAVAHL
cd ${ADAPTER_JAVAHL%.jar}
rm svn-javahl.jar
ln -s /usr/share/java/svn-javahl.jar
popd

%files
%doc org.tigris.subversion.subclipse.feature/license.html
%{install_loc}/subclipse
%{install_loc}/subclipse-clientadapter

%files graph
%doc org.tigris.subversion.subclipse.graph.feature/license.html
%doc org.tigris.subversion.subclipse.graph/icons/readme.txt
%{install_loc}/subclipse-graph

%changelog
* Fri Jul 18 2014 Mat Booth <mat.booth@redhat.com> - 1.10.5-1
- Update to latest upstream release
- Drop ancient obsoletes on subclipse-book, drop unnecessary BRs
- Fix bogus dates in changelog
- Install license files as %%doc

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 1 2013 Krzysztof Daniel <kdaniel@redhat.com> 1.10.2-2
- Fix the javahl version.

* Tue Oct 1 2013 Krzysztof Daniel <kdaniel@redhat.com> 1.10.2-1
- Update to 1.10.2.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Krzysztof Daniel <kdaniel@redhat.com> 1.10.0-2
- Upload sources.

* Wed Jun 19 2013 Krzysztof Daniel <kdaniel@redhat.com> 1.10.0-1
- Update to 1.10.0.

* Wed Jun 19 2013 Krzysztof Daniel <kdaniel@redhat.com> 1.8.21-1
- Update to 1.8.21.

* Fri May 3 2013 Krzysztof Daniel <kdaniel@redhat.com> 1.8.20-1
- Update to latest upstream release.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Sami Wagiaalla <swagiaal@redhat.com> 1.8.16-1
- Update to release 1.8.16.

* Wed Aug 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 1.8.13-2
- Get rid off eclipse-svnkit dependency.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Krzysztof Daniel <kdaniel@redhat.com> 1.8.13-1
- Update to latest upstream release.

* Thu May 3 2012 Krzysztof Daniel <kdaniel@redhat.com> 1.8.9-2
- Bug 818472 - Bump javahl BR/R.

* Wed May 2 2012 Krzysztof Daniel <kdaniel@redhat.com> 1.8.9-1
- Update to latest upstream release.

* Wed Feb 29 2012 Alexander Kurtakov <akurtako@redhat.com> 1.8.5-1
- Update to latest upstream release.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Alexander Kurtakov <akurtako@redhat.com> 1.6.18-1
- Update to 1.6.18.

* Fri Feb 25 2011 Alexander Kurtakov <akurtako@redhat.com> 1.6.17-1
- Update to 1.6.17.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Alexander Kurtakov <akurtako@redhat.com> 1.6.16-1
- Update to 1.6.16.

* Tue Nov 9 2010 Alexander Kurtakov <akurtako@redhat.com> 1.6.15-1
- Update to 1.6.15.

* Tue Jul 13 2010 Alexander Kurtakov <akurtako@redhat.com> 1.6.12-1
- Update to 1.6.12.

* Thu Mar 11 2010 Alexander Kurtakov <akurtako@redhat.com> 1.6.10-1
- Update to 1.6.10.

* Tue Feb 23 2010 Alexander Kurtakov <akurtako@redhat.com> 1.6.8-1
- Update to upstream 1.6.8.

* Fri Feb 19 2010 Alexander Kurtakov <akurtako@redhat.com> 1.6.7-1
- Update to upstream 1.6.7.

* Thu Feb 4 2010 Alexander Kurtakov <akurtako@redhat.com> 1.6.6-1
- Update to upstream 1.6.6.

* Sun Nov 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.5-3
- Fix typo.

* Sun Nov 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.5-2
- Do not pass non-existing folders to pdebuild -o.
- Switch to using %%global instead of %%define.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.5-1
- Update to upstream 1.6.5.

* Mon Aug 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.4-1
- Update to upstream 1.6.4.

* Mon Jul 27 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.2-1
- Update to upstream 1.6.2.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 26 2009 Robert Marcano <robert@marcanoonline.com> 1.6.0-1
- Update to upstream 1.6.0

* Mon Mar 23 2009 Alexander Kurtakov <akurtako@redhat.com> 1.4.7-4
- Rebuild to not ship p2 context.xml.

* Tue Feb 24 2009 Robert Marcano <robert@marcanoonline.com> 1.4.7-3
- Update to upstream 1.4.7
- eclipse-subclipse-book is obsoleted, not provided upstream
- New eclipse-subclipse-graph subpackage

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 13 2008 Alexander Kurtakov <akurtako@redhat.com> - 1.2.4-12
- Bump revision.

* Mon Oct 13 2008 Alexander Kurtakov <akurtako@redhat.com> - 1.2.4-11
- Fix build with eclipse 3.4.
- Rediff plugin-classpath.patch.

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.2.4-10
- Fix Patch0:/%%patch mismatch.

* Fri Apr 04 2008 Robert Marcano <robert@marcanoonline.com> 1.2.4-9
- Fix Bug 440818: changed links to svn-javahl.jar

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-7
- Autorebuild for GCC 4.3

* Mon Nov 12 2007 Robert Marcano <robert@marcanoonline.com> 1.2.4-6
- Build for all supported arquitectures

* Fri Oct 19 2007 Robert Marcano <robert@marcanoonline.com> 1.2.4-3
- Disable ppc64 build for f8, see Bug #298071

* Wed Sep 19 2007 Robert Marcano <robert@marcanoonline.com> 1.2.4-2
- Fix wrong applied classpath patch, fixing error: An error occurred while
automatically activating bundle org.tigris.subversion.subclipse.core

* Mon Sep 10 2007 Robert Marcano <robert@marcanoonline.com> 1.2.4-1
- Update to upstream 1.2.4
- Build for all supported arquitectures

* Sun Sep 09 2007 Robert Marcano <robert@marcanoonline.com> 1.2.2-6
- Change MANIFEST.MF patch to be applied on prep stage

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.2-4
- Rebuild for selinux ppc32 issue.

* Wed Jun 20 2007 Robert Marcano <robert@marcanoonline.com> 1.2.2-2
- Update to upstream 1.2.2
- Dependency changed from javasvn to svnkit
- Patch to support EPEL5 sent by Rob Myers

* Thu Dec 21 2006 Robert Marcano <robert@marcanoonline.com> 1.1.9-2
- Update to upstream 1.1.9
- Removed patch that added source attribute to the javac ant task
- Using the "eclipse" launcher

* Wed Nov 08 2006 Robert Marcano <robert@marcanoonline.com> 1.1.8-2
- Update to upstream 1.1.8

* Mon Aug 28 2006 Robert Marcano <robert@marcanoonline.com> 1.1.5-2
- Rebuild

* Mon Aug 21 2006 Robert Marcano <robert@marcanoonline.com> 1.1.5-1
- Update to upstream 1.1.5
- svnClientAdapter documentation files added. Subclipse includes an eclipse
  based documentation for the plugins

* Sun Aug 06 2006 Robert Marcano <robert@marcanoonline.com> 1.1.4-1
- Update to upstream 1.1.4
- License changed to EPL
- svnClientAdapter-1.1.4-javac-target.patch added fix to svnClientAdapter ant
  script

* Tue Jul 04 2006 Andrew Overholt <overholt@redhat.com> 1.0.3-2
- Use versionless pde.build.
- Remove strict SDK version requirement due to above.

* Sun Jul 02 2006 Robert Marcano <robert@marcanoonline.com> 1.0.3-2
- Embeeding the script that fetch the source code

* Sun Jun 25 2006 Robert Marcano <robert@marcanoonline.com> 1.0.3-1
- Update to 1.0.3
- Dependency name changed to ganymed-ssh2

* Sun Jun 11 2006 Robert Marcano <robert@marcanoonline.com> 1.0.1-6
- rpmlint fixes and debuginfo generation workaround

* Thu Jun 01 2006 Robert Marcano <robert@marcanoonline.com> 1.0.1-5
- Use package-build from eclipse SDK

* Sun May 28 2006 Robert Marcano <robert@marcanoonline.com> 1.0.1-4
- Integrated svnClientAdapter inside this package

* Tue May 23 2006 Ben Konrath <bkonrath@redhat.com> 1.0.1-3
- Rename package to eclipse-subclipse.
- Use copy-platform script for now.

* Sun May 07 2006 Robert Marcano <robert@marcanoonline.com> 1.0.1-2
- use external libraries from dependent packages

* Wed Apr 26 2006 Ben Konrath <bkonrath@redhat.com> 1.0.1-1
- initial version based on the work of Robert Marcano

