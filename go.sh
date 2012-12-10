# go toolchain env paths
gopath=lib
arch=386
if [ -x /usr/lib64/go ] ; then
  gopath=lib64
  arch=amd64
fi  

export GOOS="linux"
export GOARCH=$arch
export GOROOT=/usr/$gopath/go
export GOBIN=/usr/bin

if [ `id -u` != 0 ]; then
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
fi