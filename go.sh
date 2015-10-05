# go toolchain env paths
gopath=LIBDIR
arch=GOARCH

export GOOS="linux"
export GOARCH=$arch
export GOROOT=/usr/$gopath/go
export GOBIN=/usr/bin

if [ `id -u` != 0 ]; then
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
fi
