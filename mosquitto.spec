%define git_repo mosquitto
%define git_head HEAD

%define major           1

# Library names
%define libname         %mklibname %{name} %{major}
%define libcpp     %mklibname %{name}pp %{major}

%if %{_target_vendor} == mageia
%define develname       %mklibname %{name} -d
%define libcpp_devel    %mklibname %{name}pp -d

%else
%define develname       %{name}-devel
%define libcpp_devel    %mklibname %{name}pp-devel %{major}
%endif

Name:       mosquitto
Version:    %git_get_ver
Release:    %mkrel %git_get_rel2
License:    BSD
Group:      Productivity/Networking/Other
URL:        http://mosquitto.org
Source:     %git_bs_source %{name}-%{version}.tar.gz
Summary:    MQTT version 3.1/3.1.1 compatible message broker
Source1:        %{name}-gitrpm.version
Source2:        %{name}-changelog.gitrpm.txt

Requires:  libwrap0, c-ares
BuildRequires:  libwrap-devel, gcc-c++, python, python-devel, libopenssl-devel, c-ares-devel


%description
A message broker that supports version 3.1 of the MQ Telemetry Transport  
protocol. MQTT provides a method of carrying out messaging using a   
publish/subscribe model. It is lightweight, both in terms of bandwidth   
usage and ease of implementation. This makes it particularly useful at  
the edge of the network where simple embedded devices are in use, such   
as an arduino implementing a sensor.  

%package clients
Summary: Mosquitto command line publish/subscribe clients
Group: Productivity/Networking/Other

%description clients
This is two MQTT version 3.1 command line clients. mosquitto_pub can be used
to publish messages to a broker and mosquitto_sub can be used to subscribe to
a topic to receive messages.

%package -n %{libname}
Summary: MQTT C client library
Group: Development/Libraries/C and C++

%description -n %{libname}
This is a library that provides a means of implementing MQTT version 3.1
clients. MQTT provides a lightweight method of carrying out messaging using a
publish/subscribe model.

%package -n %{develname}
Summary: MQTT C client library development files
Requires: %{libname}
Group: Development/Libraries/C and C++

%description -n %{develname}
This is a library that provides a means of implementing MQTT version 3.1
clients. MQTT provides a lightweight method of carrying out messaging using a
publish/subscribe model.

%package -n %{libcpp}
Summary: MQTT C++ client library
Group: Development/Libraries/C and C++

%description -n %{libcpp}
This is a library that provides a means of implementing MQTT version 3.1
clients. MQTT provides a lightweight method of carrying out messaging using a
publish/subscribe model.

%package -n %{libcpp_devel}
Summary: MQTT C++ client library development files
Group: Development/Libraries/C and C++

%description -n %{libcpp_devel}
This is a library that provides a means of implementing MQTT version 3.1
clients. MQTT provides a lightweight method of carrying out messaging using a
publish/subscribe model.

%prep
%git_get_source
%setup -q

%build
# cmake
# tmp solution, just fix the prefix:
sed -i 's|prefix=/usr/local|prefix=/usr|' config.mk
%make


%install
%makeinstall_std

install -d %{buildroot}%{_localstatedir}/lib/mosquitto
cp mosquitto.conf %{buildroot}%{_sysconfdir}/%{name}/mosquitto.conf

%if "%{_libdir}" != "/usr/lib" 
    mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
%endif

# install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.d/
# install -m 644 %SOURCE4 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.d/README
# install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ca_certificates/
# install -m 644 %SOURCE5 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ca_certificates/README
# install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/certs/
# install -m 644 %SOURCE6 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/certs/README


# install -m 0755 %SOURCE1 $RPM_BUILD_ROOT/etc/init.d/mosquitto
# ln -sf /etc/init.d/mosquitto $RPM_BUILD_ROOT%{_sbindir}/rcmosquitto
install -d %{buildroot}%{_unitdir}/
cat '-' <<EOF > %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=MQTT message broker
After=network.target

[Service]
Type=simple
User=%{name}
Group=nogroup
ExecStart=%{_sbindir}/mosquitto

[Install]
WantedBy=multi-user.target

EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd %{name} /dev/null /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun


%files
%defattr(-,root,root,-)
%{_sbindir}/mosquitto
%{_bindir}/mosquitto_passwd
#                     /etc/init.d/mosquitto  
# {_sbindir}/rcmosquitto
%dir %{_sysconfdir}/%{name}
#%{_sysconfdir}/%{name}/conf.d/README
#%{_sysconfdir}/%{name}/ca_certificates/README
#%{_sysconfdir}/%{name}/certs/README
%config %{_sysconfdir}/%{name}/mosquitto.conf
%{_sysconfdir}/%{name}/mosquitto.conf.example
%{_sysconfdir}/%{name}/pwfile.example
%{_sysconfdir}/%{name}/aclfile.example
%{_sysconfdir}/%{name}/pskfile.example
%{_unitdir}/%{name}.service
%{_includedir}/mosquitto_plugin.h
%doc %{_mandir}/man5/mosquitto.conf.5.*
%doc %{_mandir}/man7/mqtt.7.*
%doc %{_mandir}/man7/mosquitto-tls.7.*
%doc %{_mandir}/man1/mosquitto_passwd.1.*
%doc %{_mandir}/man8/mosquitto.8.*
%attr(755,mosquitto,mosquitto) %{_localstatedir}/lib/mosquitto/

%files clients
%defattr(-,root,root,-)
%{_bindir}/mosquitto_pub
%{_bindir}/mosquitto_sub
%doc %{_mandir}/man1/mosquitto_pub.1.*
%doc %{_mandir}/man1/mosquitto_sub.1.*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libmosquitto.so.*
%doc %{_mandir}/man3/libmosquitto.3.*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/mosquitto.h
%{_libdir}/libmosquitto.so

%files -n %{libcpp}
%defattr(-,root,root,-)
%{_libdir}/libmosquittopp.so.*

%files -n %{libcpp_devel}
%defattr(-,root,root,-)
%{_includedir}/mosquittopp.h
%{_libdir}/libmosquittopp.so

%changelog -f %{_sourcedir}/%{name}-changelog.gitrpm.txt
