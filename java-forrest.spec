# TODO
# - can run as servlet and cli -- package serviet and cli
# - rename to java-xml-forrest? or rename to forrest when main pkg target is cli?
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests

%define		srcname		xml-forrest
Summary:	Apache Forrest software is a publishing framework
Name:		java-forrest
Version:	0.8
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/forrest/apache-forrest-%{version}.tar.gz
# Source0-md5:	56799bac54f79cd26a8ba29b10904259
URL:		http://forrest.apache.org/
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache Forrest is a publishing framework that transforms input from
various sources into a unified presentation in one or more output
formats. The modular and extensible plugin architecture is based on
Apache Cocoon and relevant standards, which separates presentation
from content. Forrest can generate static documents, or be used as a
dynamic server, or be deployed by its automated facility.

%package javadoc
Summary:	Online manual for Apache Forrest
Summary(pl.UTF-8):	Dokumentacja online do Apache Forrest
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for Apache Forrest.

%description javadoc -l pl.UTF-8
Dokumentacja do Apache Forrest.

%description javadoc -l fr.UTF-8
Javadoc pour Apache Forrest.

%prep
%setup -q -n apache-forrest-%{version}

%build
cd main
%ant

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a build/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc NOTICE.txt README.txt
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
