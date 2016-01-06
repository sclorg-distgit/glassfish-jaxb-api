%global pkg_name glassfish-jaxb-api
%{?scl:%scl_package %{pkg_name}}
%global oname jaxb-api
%{?java_common_find_provides_and_requires}
Name:          %{?scl_prefix}glassfish-jaxb-api
Version:       2.2.12
Release:       3.2%{?dist}
Summary:       Java Architecture for XML Binding
License:       CDDL or GPLv2 with exception
URL:           http://jaxb.java.net/
# jaxb api and impl have different version
# svn export https://svn.java.net/svn/jaxb~version2/tags/jaxb-2_2_6/tools/lib/redist/jaxb-api-src.zip

Source0:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}-b141001.1542-sources.jar
Source1:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}-b141001.1542.pom

BuildRequires: java-1.7.0-openjdk-devel
BuildRequires: %{?scl_prefix_maven}jvnet-parent

BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix_maven}maven-enforcer-plugin
BuildRequires: %{?scl_prefix_maven}maven-plugin-bundle
BuildRequires: %{?scl_prefix_maven}maven-resources-plugin
BuildArch:     noarch

# The Fedora Packaging Committee granted openjdk a bundling exception to carry JAXP and
# JAX-WS (glassfish doesn't need one, since it is the upstream for these files).
# Reference: https://fedorahosted.org/fpc/ticket/292

%description
Glassfish - JAXB (JSR 222) API.

%package javadoc
Summary:       Javadoc for %{oname}
Requires:      %{name} = %{version}-%{release}

%description javadoc
Glassfish - JAXB (JSR 222) API.

This package contains javadoc for %{pkg_name}.

%prep

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -T -q -c

# fixing incomplete source directory structure
mkdir -p src/main/java

(
  cd src/main/java
  unzip -qq %{SOURCE0}
  rm -rf META-INF
)

cp -p %{SOURCE1} pom.xml

%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin
%pom_remove_plugin org.glassfish.copyright:glassfish-copyright-maven-plugin
%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-gpg-plugin
%pom_remove_plugin org.glassfish.build:gfnexus-maven-plugin


sed -i 's|<location>${basedir}/offline-javadoc</location>|<location>%{_javadocdir}/java</location>|' pom.xml

%{?scl:EOF}

%build

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}

%mvn_file :%{oname} %{oname}
%mvn_build

%{?scl:EOF}

%install

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install

mv %{buildroot}%{_javadocdir}/%{pkg_name} \
 %{buildroot}%{_javadocdir}/%{oname}

%{?scl:EOF}

%files -f .mfiles

%files javadoc
%{_javadocdir}/%{oname}

%changelog
* Thu Jul 16 2015 Mat Booth <mat.booth@redhat.com> - 2.2.12-3.2
- Fix broken requires in javadoc package

* Tue Jul 07 2015 Roland Grunberg <rgrunber@redhat.com> - 2.2.12-3.1
- SCL-ize.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 gil cattaneo <puntogil@libero.it> 2.2.12-2
- Update to 2.2.12-b141001.1542

* Tue Jan 20 2015 gil cattaneo <puntogil@libero.it> 2.2.12-1
- Update to 2.2.12

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.9-5
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 gil cattaneo <puntogil@libero.it> 2.2.9-3
- switch to XMvn
- minor changes to adapt to current guideline

* Mon Jun 10 2013 Orion Poplawski <orion@cora.nwra.com> 2.2.9-2
- Add requires jvnet-parent

* Thu May 02 2013 gil cattaneo <puntogil@libero.it> 2.2.9-1
- update to 2.2.9

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.7-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Aug 04 2012 gil cattaneo <puntogil@libero.it> 2.2.7-1
- update to 2.2.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 gil cattaneo <puntogil@libero.it> 2.2.6-1
- update to 2.2.6
- remove Build/Requires: bea-stax-api

* Tue Jan 24 2012 gil cattaneo <puntogil@libero.it> 2.2.3-2
- revert to 2.2.3 (stable release)
- fix License field

* Fri Jul 22 2011 gil cattaneo <puntogil@libero.it> 2.2.3-1
- initial rpm
