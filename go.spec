#
# spec file for package go
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2011, Sascha Peilicke <saschpe@gmx.de>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.


%define goversion go1

Name:           go
Version:        1
Release:        1
Summary:        A compiled, garbage-collected, concurrent programming language
License:        BSD-3-Clause
Group:          Development/Other
Url:            http://golang.org
Source0:        go-1.0.tar.bz2
Source1:        go.rpmlintrc
Source2:        go.sh
Source3:        macros.go
# This file is otherwise generated at build-time from the .hg directory, which was
# stripped from the tarball to save space. TODO: Update contents after version update!
Source4:        VERSION
Source5:        godoc.service
# PATCH-FIX-OPENSUSE adjust documentation paths for API/doc server
Patch1:         godoc-path-locations.patch
# PATCH-FIX-OPENSUSE add -s flag to 'go install' (don't rebuild/install std libs)
Patch3:         go-build-dont-reinstall-stdlibs.patch
# PATCH-FIX-OPENSUSE re-enable build binary only packages (we are binary distro)
# see http://code.google.com/p/go/issues/detail?id=2775 & also issue 3268
Patch4:         allow-binary-only-packages.patch
BuildRequires:  bison
BuildRequires:  ed
BuildRequires:  systemd
# We need to manually specify the release version string here. All code compiled
# with this package will have the release string specified by the VERSION file
# in this source tarball baked into it, libs compiled with a different version
# cannot be linked anyway so all library packages will depend on this version string.
# the version string is pulled into the %godepends macro using the "go version" command.
Provides:       go-devel = %{goversion}
Provides:       go-devel-static = %{goversion}
Obsoletes:      go-devel < %{goversion}

%description
Go is an expressive, concurrent, garbage collected systems programming language
that is type safe and memory safe. It has pointers but no pointer arithmetic.
Go has fast builds, clean syntax, garbage collection, methods for any type, and
run-time reflection. It feels like a dynamic language but has the speed and
safety of a static language.

%package doc
Summary:        Go documentation
Requires:       %{name} = %{version}
Requires:	locales-doc

%description doc
Go examples and documentation.

%package vim
Summary:        Go syntax files for Vim
Group:          Editors
Requires:       %{name} = %{version}

%description vim
Vim syntax highlighting scheme for the Go programming language.

%package emacs
Summary:        Go language syntax files for Emacs
Group:          Editors
Requires:       %{name} = %{version}

%description emacs
Emacs syntax highlighting scheme for the Go programming language.

%package kate
Summary:        Go syntax files for Kate and KWrite editors
Group:          Editors
Requires:       %{name} = %{version}

%description kate
Kate syntax highlighting scheme for the Go programming language.

%prep
%setup -q -n %{name}
echo %{requiretest}
%patch1 -p1
%patch3 -p1
%patch4 -p1
cp %{SOURCE4} .
cp %{SOURCE5} .

# setup go_arch (BSD-like scheme)
%ifarch %ix86
sed -i 's|GOARCH|386|' %{SOURCE3}
%define go_arch 386
%endif
%ifarch x86_64
sed -i 's|GOARCH|amd64|' %{SOURCE3}
%define go_arch amd64
%endif
%ifarch %arm
sed -i 's|GOARCH|arm|' %{SOURCE3}
%define go_arch arm
%endif

%build
export GOROOT="`pwd`"
export GOROOT_FINAL=%{_libdir}/go
export GOBIN="$GOROOT/bin"
mkdir -p "$GOBIN"
cd src
export GDB_PRINTER="%{gdb_printer}"
HOST_EXTRA_CFLAGS="%{optflags} -Wno-error" ./make.bash

%install
export GOROOT="%{buildroot}%{_libdir}/%{name}"
install -Dm644 misc/bash/go %{buildroot}%{_sysconfdir}/bash_completion.d/go
install -Dm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/go.sh
install -Dm644 misc/emacs/go-mode-load.el %{buildroot}%{_datadir}/emacs/site-lisp/go-mode-load.el
install -Dm644 misc/emacs/go-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/go-mode.el
install -Dm644 misc/vim/autoload/go/complete.vim %{buildroot}%{_datadir}/vim/site/autoload/go/complete.vim
install -d %{buildroot}%{_datadir}/vim/site/ftplugin/go
install -Dm644 misc/vim/ftplugin/go/{fmt,godoc,import}.vim %{buildroot}%{_datadir}/vim/site/ftplugin/go/
install -Dm644 misc/vim/indent/go.vim %{buildroot}%{_datadir}/vim/site/indent/go.vim
install -Dm644 misc/vim/plugin/godoc.vim %{buildroot}%{_datadir}/vim/site/plugin/godoc.vim
install -Dm644 misc/vim/syntax/godoc.vim %{buildroot}%{_datadir}/vim/site/syntax/godoc.vim
install -Dm644 misc/vim/syntax/go.vim %{buildroot}%{_datadir}/vim/site/syntax/go.vim
install -Dm644 misc/vim/ftdetect/gofiletype.vim %{buildroot}%{_datadir}/vim/site/ftdetect/gofiletype.vim
install -Dm644 misc/kate/go.xml %{buildroot}%{_datadir}/kde4/apps/katepart/syntax/go.xml

# godoc service
mkdir -p %{buildroot}%{_unitdir}
install -Dm644 godoc.service %{buildroot}%{_unitdir}/godoc.service

# copy document templates, packages, obj libs and command utilities
mkdir -p %{buildroot}%{_bindir}
mkdir -p $GOROOT/lib
cp -ar lib/godoc $GOROOT/lib
mv pkg $GOROOT
mv bin/* %{buildroot}%{_bindir}
rm -f %{buildroot}%{_bindir}/{hgpatch,quietgcc}

# source files for go install, godoc, etc
install -d %{buildroot}%{_datadir}/go
for ext in *.{go,c,h,s,S,py}; do
  find src -name ${ext} -exec install -Dm644 \{\} %{buildroot}%{_datadir}/go/\{\} \;
done
mkdir -p $GOROOT/src
ln -s /usr/share/go/src/pkg $GOROOT/src/pkg
ln -s /usr/share/go/src/cmd $GOROOT/src/cmd

# documentation and examples
# fix documetation permissions (rpmlint warning)
find doc/ misc/ -type f -exec chmod 0644 '{}' \;
# remove unwanted arch-dependant binaries (rpmlint warning)
rm -rf misc/cgo/test/{_*,*.o,*.out,*.6,*.8}
rm -f misc/dashboard/builder/{gobuilder,*6,*.8}
rm -f misc/goplay/{goplay,*.6,*.8}
rm -rf misc/windows
rm -rf misc/cgo/test/{_*,*.o,*.out,*.6,*.8}
# fix bnc#686557, contains image licensed under non-commercial license
rm doc/talks/go_talk-20091030.pdf

# install RPM macros ($GOARCH prepared in %%prep section)
install -Dm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rpm/macros.go

# break hard links
rm %{buildroot}%{_libdir}/go/pkg/linux_%{go_arch}/{cgocall,runtime}.h
ln -s %{_datadir}/go/src/pkg/runtime/{cgocall,runtime}.h %{buildroot}%{_libdir}/go/pkg/linux_%{go_arch}/

%pre

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%preun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc AUTHORS CONTRIBUTORS LICENSE PATENTS README
%{_libdir}/go/lib/godoc/codewalk.html
%{_libdir}/go/lib/godoc/codewalkdir.html
%{_libdir}/go/lib/godoc/dirlist.html
%{_libdir}/go/lib/godoc/error.html
%{_libdir}/go/lib/godoc/example.html
%{_libdir}/go/lib/godoc/godoc.html
%{_libdir}/go/lib/godoc/opensearch.xml
%{_libdir}/go/lib/godoc/package.html
%{_libdir}/go/lib/godoc/package.txt
%{_libdir}/go/lib/godoc/search.html
%{_libdir}/go/lib/godoc/search.txt
%ifarch %ix86 %arm
%{_libdir}/go/pkg/tool/linux_%{go_arch}/8*
%endif
%ifarch x86_64
%{_libdir}/go/pkg/tool/linux_%{go_arch}/6*
%endif
%ifarch %arm
%{_libdir}/go/pkg/tool/linux_%{go_arch}/5*
%endif
%{_libdir}/go/src/cmd
%{_libdir}/go/src/pkg
%{_libdir}/go/pkg/linux_%{go_arch}/archive/tar.a
%{_libdir}/go/pkg/linux_%{go_arch}/archive/zip.a
%{_libdir}/go/pkg/linux_%{go_arch}/bufio.a
%{_libdir}/go/pkg/linux_%{go_arch}/bytes.a
%{_libdir}/go/pkg/linux_%{go_arch}/cgocall.h
%{_libdir}/go/pkg/linux_%{go_arch}/compress/bzip2.a
%{_libdir}/go/pkg/linux_%{go_arch}/compress/flate.a
%{_libdir}/go/pkg/linux_%{go_arch}/compress/gzip.a
%{_libdir}/go/pkg/linux_%{go_arch}/compress/lzw.a
%{_libdir}/go/pkg/linux_%{go_arch}/compress/zlib.a
%{_libdir}/go/pkg/linux_%{go_arch}/container/heap.a
%{_libdir}/go/pkg/linux_%{go_arch}/container/list.a
%{_libdir}/go/pkg/linux_%{go_arch}/container/ring.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/aes.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/cipher.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/des.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/dsa.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/ecdsa.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/elliptic.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/hmac.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/md5.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/rand.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/rc4.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/rsa.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/sha1.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/sha256.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/sha512.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/subtle.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/tls.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/x509.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/x509/pkix.a
%{_libdir}/go/pkg/linux_%{go_arch}/database/sql.a
%{_libdir}/go/pkg/linux_%{go_arch}/database/sql/driver.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/dwarf.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/elf.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/gosym.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/macho.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/pe.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/ascii85.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/asn1.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/base32.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/base64.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/binary.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/csv.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/gob.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/hex.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/json.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/pem.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding/xml.a
%{_libdir}/go/pkg/linux_%{go_arch}/errors.a
%{_libdir}/go/pkg/linux_%{go_arch}/expvar.a
%{_libdir}/go/pkg/linux_%{go_arch}/flag.a
%{_libdir}/go/pkg/linux_%{go_arch}/fmt.a
%{_libdir}/go/pkg/linux_%{go_arch}/go/ast.a
%{_libdir}/go/pkg/linux_%{go_arch}/go/build.a
%{_libdir}/go/pkg/linux_%{go_arch}/go/doc.a
%{_libdir}/go/pkg/linux_%{go_arch}/go/parser.a
%{_libdir}/go/pkg/linux_%{go_arch}/go/printer.a
%{_libdir}/go/pkg/linux_%{go_arch}/go/scanner.a
%{_libdir}/go/pkg/linux_%{go_arch}/go/token.a
%{_libdir}/go/pkg/linux_%{go_arch}/hash.a
%{_libdir}/go/pkg/linux_%{go_arch}/hash/adler32.a
%{_libdir}/go/pkg/linux_%{go_arch}/hash/crc32.a
%{_libdir}/go/pkg/linux_%{go_arch}/hash/crc64.a
%{_libdir}/go/pkg/linux_%{go_arch}/hash/fnv.a
%{_libdir}/go/pkg/linux_%{go_arch}/html.a
%{_libdir}/go/pkg/linux_%{go_arch}/html/template.a
%{_libdir}/go/pkg/linux_%{go_arch}/image.a
%{_libdir}/go/pkg/linux_%{go_arch}/image/color.a
%{_libdir}/go/pkg/linux_%{go_arch}/image/draw.a
%{_libdir}/go/pkg/linux_%{go_arch}/image/gif.a
%{_libdir}/go/pkg/linux_%{go_arch}/image/jpeg.a
%{_libdir}/go/pkg/linux_%{go_arch}/image/png.a
%{_libdir}/go/pkg/linux_%{go_arch}/index/suffixarray.a
%{_libdir}/go/pkg/linux_%{go_arch}/io.a
%{_libdir}/go/pkg/linux_%{go_arch}/io/ioutil.a
%{_libdir}/go/pkg/linux_%{go_arch}/log.a
%{_libdir}/go/pkg/linux_%{go_arch}/log/syslog.a
%{_libdir}/go/pkg/linux_%{go_arch}/math.a
%{_libdir}/go/pkg/linux_%{go_arch}/math/big.a
%{_libdir}/go/pkg/linux_%{go_arch}/math/cmplx.a
%{_libdir}/go/pkg/linux_%{go_arch}/math/rand.a
%{_libdir}/go/pkg/linux_%{go_arch}/mime.a
%{_libdir}/go/pkg/linux_%{go_arch}/mime/multipart.a
%{_libdir}/go/pkg/linux_%{go_arch}/net.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/http.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/http/cgi.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/http/fcgi.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/http/httptest.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/http/httputil.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/http/pprof.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/mail.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/rpc.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/rpc/jsonrpc.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/smtp.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/textproto.a
%{_libdir}/go/pkg/linux_%{go_arch}/net/url.a
%{_libdir}/go/pkg/linux_%{go_arch}/os.a
%{_libdir}/go/pkg/linux_%{go_arch}/os/exec.a
%{_libdir}/go/pkg/linux_%{go_arch}/os/signal.a
%{_libdir}/go/pkg/linux_%{go_arch}/os/user.a
%{_libdir}/go/pkg/linux_%{go_arch}/path.a
%{_libdir}/go/pkg/linux_%{go_arch}/path/filepath.a
%{_libdir}/go/pkg/linux_%{go_arch}/reflect.a
%{_libdir}/go/pkg/linux_%{go_arch}/regexp.a
%{_libdir}/go/pkg/linux_%{go_arch}/regexp/syntax.a
%{_libdir}/go/pkg/linux_%{go_arch}/runtime.a
%{_libdir}/go/pkg/linux_%{go_arch}/runtime.h
%{_libdir}/go/pkg/linux_%{go_arch}/runtime/cgo.a
%{_libdir}/go/pkg/linux_%{go_arch}/runtime/debug.a
%{_libdir}/go/pkg/linux_%{go_arch}/runtime/pprof.a
%{_libdir}/go/pkg/linux_%{go_arch}/sort.a
%{_libdir}/go/pkg/linux_%{go_arch}/strconv.a
%{_libdir}/go/pkg/linux_%{go_arch}/strings.a
%{_libdir}/go/pkg/linux_%{go_arch}/sync.a
%{_libdir}/go/pkg/linux_%{go_arch}/sync/atomic.a
%{_libdir}/go/pkg/linux_%{go_arch}/syscall.a
%{_libdir}/go/pkg/linux_%{go_arch}/testing.a
%{_libdir}/go/pkg/linux_%{go_arch}/testing/iotest.a
%{_libdir}/go/pkg/linux_%{go_arch}/testing/quick.a
%{_libdir}/go/pkg/linux_%{go_arch}/text/scanner.a
%{_libdir}/go/pkg/linux_%{go_arch}/text/tabwriter.a
%{_libdir}/go/pkg/linux_%{go_arch}/text/template.a
%{_libdir}/go/pkg/linux_%{go_arch}/text/template/parse.a
%{_libdir}/go/pkg/linux_%{go_arch}/time.a
%{_libdir}/go/pkg/linux_%{go_arch}/unicode.a
%{_libdir}/go/pkg/linux_%{go_arch}/unicode/utf16.a
%{_libdir}/go/pkg/linux_%{go_arch}/unicode/utf8.a
%{_libdir}/go/pkg/obj/linux_%{go_arch}/lib9.a
%{_libdir}/go/pkg/obj/linux_%{go_arch}/libbio.a
%{_libdir}/go/pkg/obj/linux_%{go_arch}/libcc.a
%{_libdir}/go/pkg/obj/linux_%{go_arch}/libgc.a
%{_libdir}/go/pkg/obj/linux_%{go_arch}/libmach.a
%{_libdir}/go/pkg/tool/linux_%{go_arch}/addr2line
%{_libdir}/go/pkg/tool/linux_%{go_arch}/api
%{_libdir}/go/pkg/tool/linux_%{go_arch}/cgo
%{_libdir}/go/pkg/tool/linux_%{go_arch}/dist
%{_libdir}/go/pkg/tool/linux_%{go_arch}/fix
%{_libdir}/go/pkg/tool/linux_%{go_arch}/nm
%{_libdir}/go/pkg/tool/linux_%{go_arch}/objdump
%{_libdir}/go/pkg/tool/linux_%{go_arch}/pack
%{_libdir}/go/pkg/tool/linux_%{go_arch}/pprof
%{_libdir}/go/pkg/tool/linux_%{go_arch}/vet
%{_libdir}/go/pkg/tool/linux_%{go_arch}/yacc
%{_bindir}/go*
%{_datadir}/go
%config %{_sysconfdir}/bash_completion.d/go
%config %{_sysconfdir}/profile.d/go.sh
%config %{_sysconfdir}/rpm/macros.go
%{_unitdir}/godoc.service

%files doc
%defattr(-,root,root,-)
%doc doc misc

%files vim
%defattr(-,root,root,-)
%dir %{_datadir}/vim
%{_datadir}/vim/*

%files emacs
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/go-mode*

%files kate
%defattr(-,root,root,-)
%dir %{_datadir}/kde4
%dir %{_datadir}/kde4/apps
%dir %{_datadir}/kde4/apps/katepart
%dir %{_datadir}/kde4/apps/katepart/syntax
%{_datadir}/kde4/apps/katepart/syntax/go.xml

