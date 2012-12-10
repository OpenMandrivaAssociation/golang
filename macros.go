# Macros for Go module building.
#
# Copyrigh: (c) 2011 Sascha Peilicke <saschpe@gmx.de>
#

%go_ver         %(LC_ALL=C rpm -q --qf '%%{epoch}:%%{version}\\n' go | sed -e 's/ (none):/ /' -e 's/ 0:/ /' | grep -v "is not")
%go_arch        386
%go_build_ver   %(go version | sed 's/^go version //' | tr -d ' ')

%go_dir         %{_libdir}/go
%go_sitedir     %{_libdir}/go/pkg
%go_sitearch    %{_libdir}/go/pkg/linux_%{go_arch}

%go_requires    Requires: go-devel = %go_build_ver

%go_provides \
Provides:       %{name}-devel = %{version} \
Provides:       %{name}-devel-static = %{version}

%go_disable_brp_strip_static_archive \
%define __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib/rpm/[^/]*/?brp-strip-static-archive %{__strip}!!g')


# Prepare the expected Go package build environement.
# We need a $GOPATH: go help gopath
# We need a valid importpath: go help packages
%goprep() \
export GOPATH=%{_builddir}/go \
if [ %# -eq 0 ]; then \
  echo "goprep: please specify a valid importpath, see: go help packages" \
  exit 1 \
else \
  export IMPORTPATH=%1 \
fi \
# create the importpath and move the package there \
mkdir -p $GOPATH/src/$IMPORTPATH && mv ./* $GOPATH/src/$IMPORTPATH \
# now link the old location to the new (for compatibility) \
cd %{_builddir} && rmdir %{_builddir}/%(basename %1) \
ln -s $GOPATH/src/$IMPORTPATH %{_builddir}/%(basename %1) \
# we'll be installing packages/binaries, make the targ dirs \
install -d %{buildroot}%{go_sitearch} \
install -d %{buildroot}%{_bindir} \
%{nil}

# %%gobuild macro actually performs the command "go install", but the go
# toolchain will install to the $GOPATH which allows us then customise the final
# install for the distro default locations.
#
# gobuild accepts zero or more arguments. Each argument corresponds to
# a modifier of the importpath. If no arguments are passed, this is equivalent
# to the following go install statement:
#
#     go install [importpath]
#
# Only the first or last arguement may be ONLY the wildcard argument "..."
# if the wildcard argument is passed then the importpath expands to all packages
# and binaries underneath it. If the argument contains only the wildcard no further
# arguments are considered.
#
# If no wildcard argument is passed, go install will be invoked on each $arg
# subdirectory under the importpath.
#
# Valid importpath modifier examples:
#
#    example:  %gobuild ...
#    command:  go install importpath...
#
#    example:  %gobuild /...
#    command:  go install importpath/...      (All subdirs NOT including importpath)
#
#    example:  %gobuild foo...
#    command:  go install importpath/foo...   (All subdirs INCLUDING foo)
#
#    example:  %gobuild foo ...               (same as foo...)
#    command:  go install importpath/foo...   (All subdirs INCLUDING foo)
#
#    example:  %gobuild foo/...
#    commands: go install importpath/foo/...  (All subdirs NOT including foo)
#
#    example:  %gobuild foo bar
#    commands: go install importpath/foo
#              go install importpath/bar
#
#    example:  %gobuild foo ... bar
#    commands: go install importpath/foo...   (bar is ignored)
#
#    example:  %gobuild foo bar... baz
#    commands: go install importpath/foo
#              go install importpath/bar...
#              go install importpath/baz
#
# See: go help install, go help packages
%gobuild() \
export BUILDFLAGS="-s -v -p 4" \
export GOBIN=%{_builddir}/go/bin \
MOD="" \
if [ %# -gt 0 ]; then \
  for mod in %*; do \
    if [ $mod == "..." ]; then \
      MOD=$MOD... \
      go install $BUILDFLAGS $IMPORTPATH$MOD \
      break \
    else \
      MOD=/$mod \
      go install $BUILDFLAGS $IMPORTPATH$MOD \
    fi \
  done \
else \
  go install $BUILDFLAGS $IMPORTPATH \
fi \
%{nil}

# Install all compiled packages and binaries to the buildroot
%goinstall() \
export GOPATH=%{_builddir}/go \
TMPPKG=%{_builddir}/go/pkg \
if [ "$(ls -A $TMPPKG)" ]; then \
	cp -ar %{_builddir}/go/pkg/linux_%{go_arch}/* %{buildroot}%{go_sitearch} \
fi \
TMPBIN=%{_builddir}/go/bin \
if [ "$(ls -A $TMPBIN)" ]; then \
     install -m755 $TMPBIN/* %{buildroot}%{_bindir} \
fi \
%{nil}

%gofix() \
export GOPATH=%{_builddir}/go \
if [ %# -eq 0 ]; then \
  echo "gofix: please specify a valid importpath, see: go help fix" \
  exit 1 \
else \
  go fix %1... \
fi \
%{nil}

%gotest() \
export GOPATH=%{_builddir}/go \
if [ %# -eq 0 ]; then \
  echo "gotest: please specify a valid importpath, see: go help test" \
  exit 1 \
else \
  go test %1... \
fi \
%{nil}

%godoc() \
install -d %{buildroot}%{_datadir}/go/src/pkg \
cd %{_builddir}/go/src \
find . -name *.go -exec install -Dm644 \{\} %{buildroot}%{_datadir}/go/src/pkg/\{\} \\; \
%{nil}

