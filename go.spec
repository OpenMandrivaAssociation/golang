%define debug_package %{nil}
%define __debug_install_post echo
%define _disable_lto 1
%bcond_with bootstrap

# eol 'fix' corrupts some .a files makes 6l give 'out of memory'
%define dont_fix_eol 1

%define goversion go1.7

Summary:	A compiled, garbage-collected, concurrent programming language
Name:		go
Version:	1.9.6
Release:	1
Epoch:		1
License:	BSD-3-Clause
Group:		Development/Other
Url:		http://golang.org
Source0:	https://storage.googleapis.com/golang/%{name}%{version}.src.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	go.sh
Source3:	macros.go
Source5:	godoc.service
#Patch0:		golang-1.2-verbose-build.patch
BuildRequires:	bison
%if %{with bootstrap}
BuildRequires:	gcc-go
%endif
%if !%{with bootstrap}
BuildRequires:	go
%endif
BuildRequires:	ed
BuildRequires:	systemd
BuildRequires:	diffutils
# We need to manually specify the release version string here. All code compiled
# with this package will have the release string specified by the VERSION file
# in this source tarball baked into it, libs compiled with a different version
# cannot be linked anyway so all library packages will depend on this version string.
# the version string is pulled into the %godepends macro using the "go version" command.
Provides:	go-devel = %{goversion}
Provides:	go-devel-static = %{goversion}
Provides:	golang = %{version}-%{release}
Obsoletes:	go-devel < %{goversion}
Obsoletes:	%{name}-kate < 1.2.1

%description
Go is an expressive, concurrent, garbage collected systems programming language
that is type safe and memory safe. It has pointers but no pointer arithmetic.
Go has fast builds, clean syntax, garbage collection, methods for any type, and
run-time reflection. It feels like a dynamic language but has the speed and
safety of a static language.

%files
%doc AUTHORS CONTRIBUTORS LICENSE PATENTS
%dir %{_libdir}/go
%{_libdir}/go/src
%dir %{_libdir}/go/pkg
%if %{with bootstrap}
%dir %{_libdir}/go/pkg/bootstrap/pkg/gccgo_linux_%{go_arch}
%{_libdir}/go/pkg/bootstrap/pkg/gccgo_linux_%{go_arch}/bootstrap/
%else
%dir %{_libdir}/go/pkg/bootstrap/pkg/%{_os}_%{go_arch}
%{_libdir}/go/pkg/bootstrap/pkg/%{_os}_%{go_arch}/bootstrap/
%endif
%ifarch x86_64
%dir %{_libdir}/go/pkg/%{_os}_%{go_arch}_dynlink
%{_libdir}/go/pkg/%{_os}_%{go_arch}_dynlink/*
%endif
%dir %{_libdir}/go/pkg/linux_%{go_arch}
%dir %{_libdir}/go/pkg/linux_%{go_arch}/archive
%{_libdir}/go/pkg/linux_%{go_arch}/archive/tar.a
%{_libdir}/go/pkg/linux_%{go_arch}/archive/zip.a
%{_libdir}/go/pkg/linux_%{go_arch}/bufio.a
%{_libdir}/go/pkg/linux_%{go_arch}/bytes.a
%{_libdir}/go/pkg/linux_%{go_arch}/cgocall.h
%dir %{_libdir}/go/pkg/linux_%{go_arch}/cmd
%{_libdir}/go/pkg/linux_%{go_arch}/cmd/*
%dir %{_libdir}/go/pkg/linux_%{go_arch}/compress
%{_libdir}/go/pkg/linux_%{go_arch}/compress/bzip2.a
%{_libdir}/go/pkg/linux_%{go_arch}/compress/flate.a
%{_libdir}/go/pkg/linux_%{go_arch}/compress/gzip.a
%{_libdir}/go/pkg/linux_%{go_arch}/compress/lzw.a
%{_libdir}/go/pkg/linux_%{go_arch}/compress/zlib.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/container
%{_libdir}/go/pkg/linux_%{go_arch}/container/heap.a
%{_libdir}/go/pkg/linux_%{go_arch}/container/list.a
%{_libdir}/go/pkg/linux_%{go_arch}/container/ring.a
%{_libdir}/go/pkg/linux_%{go_arch}/context.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/crypto
%dir %{_libdir}/go/pkg/linux_%{go_arch}/crypto/internal
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/internal/*.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/crypto/x509
%{_libdir}/go/pkg/linux_%{go_arch}/crypto/x509/pkix.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/database
%dir %{_libdir}/go/pkg/linux_%{go_arch}/database/sql
%{_libdir}/go/pkg/linux_%{go_arch}/database/sql.a
%{_libdir}/go/pkg/linux_%{go_arch}/database/sql/driver.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/debug
%{_libdir}/go/pkg/linux_%{go_arch}/debug/dwarf.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/elf.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/gosym.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/macho.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/plan9obj.a
%{_libdir}/go/pkg/linux_%{go_arch}/debug/pe.a
%{_libdir}/go/pkg/linux_%{go_arch}/encoding.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/encoding
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
%{_libdir}/go/pkg/linux_%{go_arch}/net.a
%{_libdir}/go/pkg/linux_%{go_arch}/flag.a
%{_libdir}/go/pkg/linux_%{go_arch}/fmt.a
%{_libdir}/go/pkg/linux_%{go_arch}/funcdata.h
%dir %{_libdir}/go/pkg/linux_%{go_arch}/go
%{_libdir}/go/pkg/linux_%{go_arch}/go/*.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/go/internal
%{_libdir}/go/pkg/linux_%{go_arch}/go/internal/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/hash.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/hash
%{_libdir}/go/pkg/linux_%{go_arch}/hash/adler32.a
%{_libdir}/go/pkg/linux_%{go_arch}/hash/crc32.a
%{_libdir}/go/pkg/linux_%{go_arch}/hash/crc64.a
%{_libdir}/go/pkg/linux_%{go_arch}/hash/fnv.a
%{_libdir}/go/pkg/linux_%{go_arch}/html.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/html
%{_libdir}/go/pkg/linux_%{go_arch}/html/template.a
%{_libdir}/go/pkg/linux_%{go_arch}/image.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/image
%{_libdir}/go/pkg/linux_%{go_arch}/image/color.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/image/color
%{_libdir}/go/pkg/linux_%{go_arch}/image/color/palette.a
%{_libdir}/go/pkg/linux_%{go_arch}/image/draw.a
%{_libdir}/go/pkg/linux_%{go_arch}/image/gif.a
%{_libdir}/go/pkg/linux_%{go_arch}/image/jpeg.a
%{_libdir}/go/pkg/linux_%{go_arch}/image/png.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/image/internal
%{_libdir}/go/pkg/linux_%{go_arch}/image/internal/*.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/index
%{_libdir}/go/pkg/linux_%{go_arch}/index/suffixarray.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/internal
%{_libdir}/go/pkg/linux_%{go_arch}/internal/*.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/internal/syscall
%{_libdir}/go/pkg/linux_%{go_arch}/internal/syscall/*.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/internal/syscall/windows
%{_libdir}/go/pkg/linux_%{go_arch}/internal/syscall/windows/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/io.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/io
%{_libdir}/go/pkg/linux_%{go_arch}/io/ioutil.a
%{_libdir}/go/pkg/linux_%{go_arch}/log.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/log
%{_libdir}/go/pkg/linux_%{go_arch}/log/syslog.a
%{_libdir}/go/pkg/linux_%{go_arch}/math.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/math
%{_libdir}/go/pkg/linux_%{go_arch}/math/big.a
%{_libdir}/go/pkg/linux_%{go_arch}/math/bits.a
%{_libdir}/go/pkg/linux_%{go_arch}/math/cmplx.a
%{_libdir}/go/pkg/linux_%{go_arch}/math/rand.a
%{_libdir}/go/pkg/linux_%{go_arch}/mime.a
%{_libdir}/go/pkg/linux_%{go_arch}/plugin.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/net
%{_libdir}/go/pkg/linux_%{go_arch}/net/*
%dir %{_libdir}/go/pkg/linux_%{go_arch}/mime
%{_libdir}/go/pkg/linux_%{go_arch}/mime/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/os.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/os
%{_libdir}/go/pkg/linux_%{go_arch}/os/exec.a
%{_libdir}/go/pkg/linux_%{go_arch}/os/signal.a
%{_libdir}/go/pkg/linux_%{go_arch}/os/user.a
%{_libdir}/go/pkg/linux_%{go_arch}/path.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/path
%{_libdir}/go/pkg/linux_%{go_arch}/path/filepath.a
%{_libdir}/go/pkg/linux_%{go_arch}/reflect.a
%{_libdir}/go/pkg/linux_%{go_arch}/regexp.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/regexp
%{_libdir}/go/pkg/linux_%{go_arch}/regexp/syntax.a
%{_libdir}/go/pkg/linux_%{go_arch}/runtime.a
%{_libdir}/go/pkg/linux_%{go_arch}/runtime.h
%dir %{_libdir}/go/pkg/linux_%{go_arch}/runtime
%dir %{_libdir}/go/pkg/linux_%{go_arch}/runtime/pprof
%dir %{_libdir}/go/pkg/linux_%{go_arch}/runtime/pprof/internal
%{_libdir}/go/pkg/linux_%{go_arch}/runtime/pprof/internal/profile.a
%{_libdir}/go/pkg/linux_%{go_arch}/runtime/*.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/runtime/internal
%{_libdir}/go/pkg/linux_%{go_arch}/runtime/internal/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/sort.a
%{_libdir}/go/pkg/linux_%{go_arch}/strconv.a
%{_libdir}/go/pkg/linux_%{go_arch}/strings.a
%{_libdir}/go/pkg/linux_%{go_arch}/sync.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/sync
%{_libdir}/go/pkg/linux_%{go_arch}/sync/atomic.a
%{_libdir}/go/pkg/linux_%{go_arch}/syscall.a
%{_libdir}/go/pkg/linux_%{go_arch}/testing.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/testing
%dir %{_libdir}/go/pkg/linux_%{go_arch}/testing/internal
%{_libdir}/go/pkg/linux_%{go_arch}/testing/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/testing/internal/*.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/text
%{_libdir}/go/pkg/linux_%{go_arch}/text/scanner.a
%{_libdir}/go/pkg/linux_%{go_arch}/text/tabwriter.a
%{_libdir}/go/pkg/linux_%{go_arch}/text/template.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/text/template
%{_libdir}/go/pkg/linux_%{go_arch}/text/template/parse.a
%{_libdir}/go/pkg/linux_%{go_arch}/textflag.h
%{_libdir}/go/pkg/linux_%{go_arch}/time.a
%{_libdir}/go/pkg/linux_%{go_arch}/unicode.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/unicode
%{_libdir}/go/pkg/linux_%{go_arch}/unicode/utf16.a
%{_libdir}/go/pkg/linux_%{go_arch}/unicode/utf8.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/net
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/crypto
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/text
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/text/secure
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/text/unicode
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/net/http2
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/crypto/chacha20poly1305/internal/
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/crypto/chacha20poly1305/
%{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/crypto/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/crypto/chacha20poly1305/internal/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/text/unicode/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/text/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/text/secure/*.a
%{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/net/http2/hpack.a
%dir %{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/net/lex
%{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/net/lex/httplex.a
%{_libdir}/go/pkg/linux_%{go_arch}/vendor/golang_org/x/net/*.a
%dir %{_libdir}/go/pkg/tool
%dir %{_libdir}/go/pkg/tool/linux_%{go_arch}
%{_libdir}/go/pkg/tool/linux_%{go_arch}/*
%dir %{_libdir}/go/pkg/bootstrap
%dir %{_libdir}/go/pkg/bootstrap/bin
%dir %{_libdir}/go/pkg/bootstrap/pkg
%dir %{_libdir}/go/pkg/bootstrap/src
%dir %{_libdir}/go/pkg/bootstrap/src/bootstrap
%{_libdir}/go/pkg/bootstrap/src/bootstrap/*
%{_libdir}/go/pkg/bootstrap/bin/*
%dir %{_libdir}/go/pkg/include
%{_libdir}/go/pkg/include/*.h
%dir %{_libdir}/%{name}/bin
%{_libdir}/%{name}/bin/%{name}
%{_bindir}/go*
%{_datadir}/go
%config %{_sysconfdir}/rpm/macros.go
%config %{_sysconfdir}/profile.d/go.sh
%{_unitdir}/godoc.service

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%preun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

#----------------------------------------------------------------------------

%package doc
Summary:	Go documentation
Requires:	%{name} = %{EVRD}

%description doc
Go examples and documentation.

%files doc
%doc doc misc

%prep
%setup -q -n %{name}
%apply_patches
cp %{SOURCE5} .

# setup go_arch (BSD-like scheme)
%ifarch %{ix86}
%define go_arch 386
%endif
%ifarch x86_64
%define go_arch amd64
%endif
%ifarch %{arm}
%define go_arch arm
%endif
%ifarch aarch64
%define go_arch arm64
%endif

%build
export GOROOT="$(pwd)"
export GOBIN="${GOROOT}/bin"
mkdir -p "$GOBIN"

# go1.5 bootstrapping. The compiler is written in golang.
%if !%{with bootstrap}
export GOROOT_BOOTSTRAP=%{_libdir}/%{name}
%else
export GOROOT_BOOTSTRAP=%{_prefix}
%endif

# set up final install location
export GOROOT_FINAL=%{_libdir}/%{name}

# TODO use the system linker to get the system link flags and build-id
# when https://code.google.com/p/go/issues/detail?id=5221 is solved
#export GO_LDFLAGS="-linkmode external -extldflags $RPM_LD_FLAGS"

export GOHOSTOS=linux
export GOHOSTARCH=%{go_arch}


pushd src
# use our gcc options for this build, but store gcc as default for compiler
CFLAGS="%{optflags}" \
LDFLAGS="%{ldflags}" \
CC="%{__cc}" \
%ifarch %{arm} %{ix86}
CC_FOR_TARGET="gcc" \
%else
CC_FOR_TARGET="%{__cc}" \
%endif
CXX_FOR_TARGET="%{__cxx}" \
%ifarch %arm
GOARM=7 \
%endif
GOOS=%{_os} \
GOARCH=%{go_arch} \
        ./make.bash --no-clean
popd

%ifarch %ix86
strip $GOBIN/go # bnc#818502
%endif

%ifarch x86_64
# TODO get linux/386 support for shared objects.
# golang shared objects for stdlib
GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -buildmode=shared std
%endif

%check
#chmod 755 doc/progs/run.go
#chmod +x doc/articles/wiki/test.bash
#chmod +x doc/codewalk/run

#export GOROOT="$(pwd)"
#export GOBIN="${GOROOT}/bin"

#pushd src
# For now test 3729,5603 doesn't pass so skiping it
#perl -pi -e 's/!windows/!windows,!linux/' ../misc/cgo/test/issue3729.go
#perl -pi -e 's/func Test3729/\/\/func Test3729/' ../misc/cgo/test/cgo_test.go
#perl -pi -e 's/^package/\/\/ +build !linux^Mpackage/' ../misc/cgo/test/issue5603.go
#perl -pi -e 's/func Test5603/\/\/func Test5603/' ../misc/cgo/test/cgo_test.go
#rm -f cmd/go/note_test.go
#rm -f cmd/go/vendor_test.go
#rm -f syscall/exec_linux_test.go
#rm -f ./cmd/go/go_test.go
#./run.bash --no-rebuild --banner
#PATH="${GOBIN}:${PATH}" CGO_ENABLED=0 ./run.bash --no-rebuild
#popd
export GOROOT=$(pwd -P)
export PATH="$GOROOT"/bin:"$PATH"
pushd src

export CC="gcc"
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"
#%if !%{external_linker}
#export GO_LDFLAGS="-linkmode internal"
#%endif
#%if !%{cgo_enabled} || !%{external_linker}
#export CGO_ENABLED=0
#%endif

# make sure to not timeout
export GO_TEST_TIMEOUT_SCALE=2

#%if %{fail_on_tests}
#./run.bash --no-rebuild -v -v -v -k
#%else
#./run.bash --no-rebuild -v -v -v -k || :
#%endif
popd


%install
export GOROOT="%{buildroot}%{_libdir}/%{name}"
install -Dm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/go.sh

# godoc service
mkdir -p %{buildroot}%{_unitdir}
install -Dm644 godoc.service %{buildroot}%{_unitdir}/godoc.service

# source files for go install, godoc, etc
install -d %{buildroot}%{_datadir}/go
for ext in *.{go,c,h,s,S,py}; do
  find src -name ${ext} -exec install -Dm644 \{\} %{buildroot}%{_datadir}/go/\{\} \;
done
mkdir -p $GOROOT
ln -s /usr/share/go/src $GOROOT/src

# copy document templates, packages, obj libs and command utilities
mkdir -p %{buildroot}%{_bindir}
mkdir -p $GOROOT/lib
cp -Rp pkg $GOROOT
cp bin/* %{buildroot}%{_bindir}
rm -f %{buildroot}%{_bindir}/{hgpatch,quietgcc}

mkdir -p %{buildroot}/%{_libdir}/%{name}/bin/
ln -s %{_bindir}/%{name} %{buildroot}/%{_libdir}/%{name}/bin/%{name}

# documentation and examples
# fix documetation permissions (rpmlint warning)
find doc/ misc/ -type f -exec chmod 0644 '{}' \;
# remove unwanted arch-dependant binaries (rpmlint warning)
rm -rf misc/cgo/test/{_*,*.o,*.out,*.6,*.8}
rm -f misc/dashboard/builder/{gobuilder,*6,*.8}
rm -f misc/goplay/{goplay,*.6,*.8}
rm -rf misc/windows
rm -rf misc/cgo/test/{_*,*.o,*.out,*.6,*.8}

# install RPM macros
install -Dm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rpm/macros.go
sed -i s!GOARCH!%{go_arch}! %{buildroot}%{_sysconfdir}/rpm/macros.go
sed -i s!GOARCH!%{go_arch}! %{buildroot}%{_sysconfdir}/profile.d/go.sh
sed -i s!LIBDIR!%{_lib}! %{buildroot}%{_sysconfdir}/profile.d/go.sh

# break hard links
#rm %{buildroot}%{_libdir}/go/pkg/linux_%{go_arch}/{textflag,funcdata,cgocall,runtime}.h
ln -s %{_datadir}/go/src/cmd/ld/textflag.h %{buildroot}%{_libdir}/go/pkg/linux_%{go_arch}
ln -s %{_datadir}/go/src/runtime/{runtime,cgocall,funcdata}.h %{buildroot}%{_libdir}/go/pkg/linux_%{go_arch}/
